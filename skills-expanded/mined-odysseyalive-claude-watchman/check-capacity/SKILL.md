---
name: check-capacity
description: "OBSERVE: disk, inodes, memory, and log store size against configured thresholds. Handles both Linux (free/journalctl) and macOS (vm_stat/Unified Log)."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# check-capacity (Grammar / Observe)

Establishes whether the machine is about to run out of something. Disk, inodes,
memory pressure, and journal disk usage — measured against the thresholds in
`config/watchman.conf`. Read-only.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

Every `/watchman audit` / `/watchman loop`.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher —
   `bash lib/wm <function> [args…]` — which sources the libs (`lib/journal.sh`,
   `lib/profile.sh`, `lib/io-courtesy.sh`, `lib/capacity.sh`) under bash internally; never
   `source lib/…` directly (dontAsk refuses a dot-source). Initialize with
   `bash lib/wm journal_init`; load thresholds from `config/watchman.conf`: the warn band
   (`WATCHMAN_DISK_WARN_PCT`, `WATCHMAN_INODE_WARN_PCT`, `WATCHMAN_MEM_WARN_PCT`) and the
   danger band (`WATCHMAN_DISK_CRIT_PCT`, `WATCHMAN_INODE_CRIT_PCT`). A missing CRIT value
   falls back to `95`. Determine the family with `bash lib/wm watchman_family` and read the
   printed value — it selects the platform-appropriate memory and log-store commands in
   steps 4–5 (`darwin` ⇒ the macOS branch, otherwise the Linux branch).

### Platform: Windows

If `bash lib/wm watchman_family` is `windows`, the raw POSIX tools used below (`df`, `free`,
`journalctl --disk-usage`) do **not** exist. On Windows the dispatcher is mechanically
rewritten to `pwsh -NoProfile -File lib/wm.ps1 <fn>`, and the same logical steps run through
the **ported capacity functions** (the `lib/capacity.ps1` / `Get-Volume` path: per-volume
free space for step 2's disk bands, the memory-pressure values for step 4, and the
log-store / Event Log size for step 5). Use those `bash lib/wm` capacity functions exactly
where the Linux branch would shell out to `df`/`free`/`journalctl`; keep the same
`check_id`/`target`/`risk_tier` shapes and thresholds. **One difference: NTFS has no inode
table, so SKIP the `inode_capacity` check (step 3) on Windows** — there is nothing to
measure and no finding to journal. All other families run steps 2–5 as written below.

2. **Disk.** `df -P` per mounted filesystem (skip pseudo/`tmpfs`/`devtmpfs` and read-only
   mounts — they cannot be cleaned). Two bands, computed per mountpoint:
   - usage ≥ `WATCHMAN_DISK_CRIT_PCT` ⇒ **dangerously low: severity `critical` (red)** —
     escalated above the profile floor, because a filesystem this full breaks services
     silently and imminently. Put the free figure in human units (`df -Ph`) in `detail`,
     **then name what is filling it** (next bullet).
   - else usage ≥ `WATCHMAN_DISK_WARN_PCT` ⇒ run `bash lib/wm profile_severity disk_capacity`
     and use the printed level as the literal severity (the warn-band floor: high on a
     server, medium on a workstation).
   - below warn ⇒ no finding (record the metric only).

   **Critical band only — the largest-files enrichment (heavy read, deferrable).** A
   filesystem walk is heavy, so gate it: IF `bash lib/wm io_should_defer_heavy`, run
   `bash lib/wm io_pressure_reason` and append to `detail` the literal text
   `"top-consumers scan deferred: "` followed by its printed output (no `$(…)`), then skip the walk
   (the critical finding from `df` is cheap and is journaled regardless — only this
   enrichment defers). OTHERWISE run `bash lib/wm capacity_top_consumers "<mountpoint>"` and fold its
   output (largest files, `<human-size>\t<path>`, top `WATCHMAN_TOPFILES_COUNT`) into
   `detail` so the finding — and the email it triggers — answers "what do I delete?" The
   engine is read-only, stays on the one filesystem (`-xdev`), and reads metadata only; it
   NEVER frees space (that is the operator's call via `watchman fix`).

   Either band: `check_id=disk_capacity`, `target=<mountpoint>`, `risk_tier=safe` (the safe
   remediation is cleaning caches, not deleting user data — the fixer never deletes data).
   The fingerprint is stable across bands, so a filesystem that climbs from warn into the
   danger band UPDATES the existing finding in place (severity rises, the file list is
   added), never duplicates it.
3. **Inodes.** `df -iP`; ≥ `WATCHMAN_INODE_CRIT_PCT` ⇒ severity `critical` (red), else ≥
   `WATCHMAN_INODE_WARN_PCT` ⇒ run `bash lib/wm profile_severity inode_capacity` and use the
   printed level as the literal severity. `check_id=inode_capacity`
   (often the silent killer — a full inode table fails writes with space still free). On
   Darwin/APFS, `df -iP` still reports inodes, but APFS allocates them dynamically (a very
   large `ifree`, `%iused` ≈ 0), so this check self-suppresses on a healthy volume — which is
   correct; no Darwin special-casing is needed.
4. **Memory pressure** (`check_id=memory_pressure`; record current values — `diagnose-crash`
   correlates them with OOM/jetsam history):
   - **Linux** (family ≠ `darwin`): `free`; sustained low available memory ⇒ a finding.
   - **macOS** (family == `darwin`): `vm_stat` page counts × the LIVE page size from
     `bash lib/wm io_run sysctl -n hw.pagesize` (16384 on Apple Silicon, 4096 on Intel —
     never hardcode it), measured against `sysctl -n hw.memsize`. Low available percentage ⇒
     a finding; record `pages free`, `pages wired down`, and `pages active` (from `vm_stat`)
     in `detail`.
5. **Log store size** (`check_id=journal_size_unbounded`):
   - **Linux** (family ≠ `darwin`): `journalctl --disk-usage` vs `SystemMaxUse`; record as a
     capacity metric and a finding if unbounded growth is observed.
   - **macOS** (family == `darwin`): `du -sh /var/db/diagnostics 2>/dev/null` for the Unified
     Log store; record the size as an info metric. macOS sets no hard cap — note that to the
     operator.
6. **Journal each** with concrete numbers in `detail`. Never free space or delete
   files here — only observe.
<!-- /origin -->

## Grounding

All claude-watchman functions below are reached via `bash lib/wm <function>` — the
dispatcher sources these libs internally; never `source lib/…` directly.

- `lib/profile.sh` — `profile_severity`.
- `lib/journal.sh` — `journal_upsert`, `journal_record_metric`.
- `lib/capacity.sh` — `capacity_top_consumers <mountpoint>` (read-only largest-files walk,
  critical band only).
- `lib/io-courtesy.sh` — `io_should_defer_heavy` / `io_pressure_reason` (defer the walk
  under load); `capacity_top_consumers` itself runs via `io_run` when this is sourced.
- `config/watchman.conf` — capacity thresholds: the warn band (`*_WARN_PCT`) and the
  danger band (`WATCHMAN_DISK_CRIT_PCT` / `WATCHMAN_INODE_CRIT_PCT`) that escalates a
  finding to `critical` (red) when space is dangerously low.
