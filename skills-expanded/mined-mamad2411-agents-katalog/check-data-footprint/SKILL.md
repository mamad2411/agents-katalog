---
name: check-data-footprint
description: "OBSERVE: claude-watchman's OWN collected-data footprint (journal DB, run log, cost ledger, backups, monitor-state) against retention windows. Read-only — surfaces a prune finding; never deletes."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# check-data-footprint (Grammar / Observe)

Establishes whether claude-watchman is being a disciplined guest on its host's
disk. It sizes the data claude-watchman itself collects under `journal/` — the
findings database, the headless `run.log`, the cost ledger, pre-migration/pre-prune
backups, and attended-monitor snapshot state — and checks how much of it has
outlived its retention window. When the footprint crosses a threshold, or stale
data has accumulated, it journals a single finding so the operator can prune it
later via `watchman fix`. Read-only: it measures and reports, and **never deletes a
byte**.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

Every `/watchman audit` / `/watchman loop`. It is the self-hygiene counterpart to
`check-capacity`: where `check-capacity` watches the HOST's disk, this watches
claude-watchman's OWN data so the monitor never becomes the thing filling the disk.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher —
   `bash lib/wm <function> [args…]` — which sources the libs (`lib/journal.sh`,
   `lib/retention.sh`) under bash internally; never `source lib/…` directly (dontAsk
   refuses a dot-source). Initialize with `bash lib/wm journal_init`. Load the retention
   tunables from `config/watchman.conf` (all have built-in defaults if unset): the footprint
   warn cap `WATCHMAN_DATA_FOOTPRINT_WARN_MB` (default 50), and the windows
   `WATCHMAN_RETAIN_FINDINGS_DAYS` (180), `WATCHMAN_RETAIN_METRICS_DAYS` (90),
   `WATCHMAN_RETAIN_RUNS_DAYS` (90), `WATCHMAN_RETAIN_RUNLOG_MB` (10),
   `WATCHMAN_RETAIN_BACKUPS` (5), `WATCHMAN_RETAIN_MONITOR_DAYS` (30).

   This check is platform-agnostic — `journal/` has the same shape on every family. On
   Windows the dispatcher is mechanically rewritten to `pwsh -NoProfile -File lib/wm.ps1
   <fn>` and the same logical functions run through the ported `lib/retention.ps1` /
   `lib/journal.ps1`; the steps below are unchanged.

2. **Measure the footprint (read-only).** Run `bash lib/wm retention_report` — it prints
   one `<bytes>\t<human>\t<label>` row per artifact class (active DB, WAL/SHM sidecars,
   `run.log`, the cost ledger, backups, `monitor-state/`, offsets) and a `TOTAL` row last.
   Run `bash lib/wm retention_total_mb` for the whole-MB total to compare against the cap
   and record as a metric. Both are pure sizing — they read file SIZES only, never the
   journal's contents.

3. **Enumerate what is prunable now (read-only).** Two read-only candidate scans, neither
   of which deletes anything:
   - **Database side:** `bash lib/wm journal_prune_candidates` — counts of terminal findings
     (`fixed`/`ignored`) past the findings window, plus `metrics` and `runs` rows past their
     windows. Active findings (`open`/`regressed`/`in-review`) are never counted — they are
     never pruned, whatever their age.
   - **File side:** `bash lib/wm retention_file_candidates` — `run.log` over its MB cap, db
     backups beyond the newest `WATCHMAN_RETAIN_BACKUPS`, and `monitor-state` snapshots older
     than the monitor window. Classes with nothing to prune are omitted.

4. **Journal one finding when it is worth the operator's attention.** Raise the finding when
   EITHER the total footprint is at/over `WATCHMAN_DATA_FOOTPRINT_WARN_MB`, OR any prunable
   data exists (a nonzero count/row from step 3). If the footprint is under the cap AND
   nothing is prunable, record the metric only and journal NO finding — a tidy monitor is a
   quiet monitor.

   Set severity by how far over the cap the total is: `medium` when the total is more than
   4× the cap (runaway growth), else `low` when at/over the cap, else `info` (only stale data
   to tidy, footprint still modest). Then journal via the dispatcher:

   `bash lib/wm journal_upsert "" "" capacity <severity> review data_footprint "" "<title>" "<detail>" "<remediation>"`

   - `check_id=data_footprint`, and **`target=""`** — `check_id` already uniquely identifies
     this finding, so per the deterministic-target rule do NOT slug anything into `target`
     (a stable empty target folds the finding into its prior self every run instead of
     duplicating). family/profile passed as `"" ""` so the journal resolves them.
   - `category=capacity`, `risk_tier=review`. Deleting collected forensic history is data
     loss, so it is **review** tier, never `safe`: the operator confirms the exact prune
     per finding in `watchman fix`, and the loop — which holds no mutating permission — can
     never apply it.
   - `detail`: the `TOTAL` human size and the per-class prunable summary from steps 2–3, in
     plain language (e.g. "journal/ holds 71MB; prunable now: 312 terminal findings >180d,
     8,640 metrics rows >90d, 11 old backups (~48MB), run.log 14MB"). Concrete numbers, no
     PIDs or timestamps in the target.
   - `remediation`: name the exact operator path —
     "Run `watchman fix`: it backs up findings.db, then `journal_prune` removes the old
     DB rows and `retention_prune_files` rotates run.log / removes old backups / clears
     stale monitor-state. Tune the windows in config/watchman.conf."

5. **Record the trend metric.** `bash lib/wm journal_record_metric watchman_data_footprint_mb <total-mb>`
   so the loop can chart whether claude-watchman's own footprint is climbing over time.

6. **Observe only.** Never run a prune from here. `journal_prune` and `retention_prune_files`
   are mutators the dispatcher refuses without `WM_APPLY=1`; pruning is the operator's
   confirmed call under `watchman fix` (fix-redflag) — not this skill. Note that
   `journal_prune` deletes findings-DB rows, which is the Prime Directive's
   destructive-database clause by name (not merely a `review`-tier op): it always
   backs up findings.db first and proceeds only on the stop-warn-ask consent.
<!-- /origin -->

## Grounding

All claude-watchman functions below are reached via `bash lib/wm <function>` — the
dispatcher sources these libs internally; never `source lib/…` directly.

- `lib/retention.sh` — `retention_report`, `retention_total_mb`, `retention_file_candidates`
  (all READ-ONLY sizing/enumeration); `retention_prune_files` is the MUTATOR the fixer runs,
  never this skill.
- `lib/journal.sh` — `journal_prune_candidates` (READ-ONLY counts), `journal_upsert`,
  `journal_record_metric`. `journal_prune` is the MUTATOR the fixer runs.
- `config/watchman.conf` — the retention windows and the footprint warn cap
  (`WATCHMAN_DATA_FOOTPRINT_WARN_MB`, `WATCHMAN_RETAIN_*`).
