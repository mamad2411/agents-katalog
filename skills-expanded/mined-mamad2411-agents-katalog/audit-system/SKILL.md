---
name: audit-system
description: "OBSERVE: run the profile-appropriate security audit by wrapping Lynis, fold warnings/suggestions into the journal, and track the hardening index over time."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# audit-system (Grammar / Observe)

Establishes *what is* about system hardening. Wraps **Lynis** — claude-watchman
does not re-detect what Lynis already detects; its value-add is journaling, dedup,
risk-tiering, and plain-language explanation. Read-only: it scans and journals, it
never fixes.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

Part of every `/watchman audit` and `/watchman loop` pass. Run it to refresh the
hardening picture and track the Lynis hardening index as a trend.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher —
   `bash lib/wm <function> [args…]` — which sources the libs under bash internally; never
   `source lib/…` directly (dontAsk refuses a dot-source). Initialize with
   `bash lib/wm journal_init`. Determine the machine's family and profile by running
   `bash lib/wm watchman_family` and `bash lib/wm watchman_profile` and reading the printed
   values — use them to decide which checks apply. You do NOT pass them to journal_upsert
   (it auto-resolves them; pass `"" ""`).
1b. **I/O courtesy gate (don't take down a busy server).** A full Lynis run is heavy.
   IF `bash lib/wm io_should_defer_heavy` → journal one `category=capacity`, `severity=info`,
   `risk_tier=safe`, `check_id=diagnostic_deferred`, `target=audit-system` finding whose detail
   is `"deferred: "` followed by the printed output of `bash lib/wm io_pressure_reason` (run it
   first; do not use `$(…)` substitution), then SKIP the Lynis run this pass (retry
   next pass). Do NOT pile heavy I/O onto an already-loaded box.

### Platform: Windows

If `bash lib/wm watchman_family` is `windows`, **SKIP the Lynis run in step 2 below and its
report-parsing entirely** (Lynis does not run on Windows and there is no
`/var/log/lynis-report.dat` to parse). Instead run **`bash lib/wm windows_hardening_scan`**,
which performs the native Defender / BitLocker / UAC / firewall / SMBv1 / RDP-NLA /
Windows Update / Guest checks, journals each finding directly through `lib/journal.sh`, and
records the tracked metric as **`windows_hardening_index`** (NOT the Lynis hardening index).
Because the Windows scan journals its own findings and metric, steps 2–4 below (the
Lynis-specific run, the `lynis_hardening_index` metric, and the `warning[]`/`suggestion[]`
report parsing) do **not** apply on Windows. The I/O-courtesy gate (step 1b) and the
self-footprint record (step 2c) still apply — run the scan through `bash lib/wm io_measure`
as you would Lynis. On all non-Windows families (`debian`/`rhel`/`arch`/`darwin`), continue
with the Lynis workflow below exactly as written.

2. **Run Lynis** (read-only system audit) through `io_measure`, which both prices it at
   the role's I/O priority AND records what it cost:
   `bash lib/wm io_measure sudo lynis audit system --quiet --no-colors`. Lynis writes machine-readable
   results to the Lynis report path, which `bash lib/wm log_path_lynis` prints (run it, use the
   literal path) (`/var/log/lynis-report.dat`). Do not parse human
   stdout — parse the report file. (Any whole-filesystem integrity verification reached
   through `bash lib/wm integrity_verify_all` is already priced at the role's priority when
   io-courtesy is sourced.)
2c. **Self-footprint.** Journal one `category=capacity`, `severity=info`, `risk_tier=safe`,
   `check_id=self_footprint`, `target=audit-system` finding whose detail is the printed output
   of `bash lib/wm io_footprint_summary` (run it first; use its output as the detail text) so the
   operator (and the loop's trend) can see what
   claude-watchman itself costs. IF `bash lib/wm io_footprint_over_budget`, raise it to `severity=low`
   and note the check is getting expensive (a cue to enable incremental reads / lengthen
   its cadence).
3. **Capture the hardening index** as a tracked metric:
   read `hardening_index=` from the report and
   `bash lib/wm journal_record_metric lynis_hardening_index "$value"` so the loop can chart drift.
4. **Fold findings in.** For each `warning[]` and `suggestion[]` line in the report:
   - `category=security` (or `config` for non-security hardening suggestions);
   - severity: warnings → `high`/`medium`, suggestions → `low`/`info`, adjusted by
     `bash lib/wm profile_severity` where a matching `check_id` exists; skip checks that
     `bash lib/wm profile_runs_check` says do not apply to this profile;
   - risk tier: default `manual` (Lynis suggestions are usually context-specific);
     only mark `safe` for unambiguous toggles;
   - `bash lib/wm journal_upsert "" "" "$category" "$severity" "$risk_tier" \
       "lynis_<test-id>" "" "$title" "$detail" "$remediation"` — pass `"" ""` for
     family/profile (journal_upsert auto-resolves them) and pass `target=""`.
     The `lynis_<test-id>` in `check_id` is already the stable per-finding key, so an
     empty target keeps the fingerprint identical across runs. Do NOT slug the title
     or description into target: a model-invented target varies run-to-run and the
     finding duplicates instead of folding.
5. **Never remediate here.** Hand fixes to `fix-redflag`. Re-running must update
   findings in place (the fingerprint guarantees no duplicates).
<!-- /origin -->

## Grounding

All claude-watchman functions below are reached via `bash lib/wm <function>` (never a
direct `source`); the lib files are where they live.

- `lib/journal.sh` — the only gate to findings.db (`journal_upsert`, `journal_record_metric`).
- `lib/distro.sh` — `log_path_lynis`, `watchman_family`.
- `lib/profile.sh` — `profile_severity`, `profile_runs_check`.
- `lib/io-courtesy.sh` — `io_run` / `io_measure` (role-priced heavy reads + self-cost),
  `io_should_defer_heavy` / `io_pressure_reason` (PSI-based, role-scaled deferral),
  `io_footprint_summary` / `io_footprint_over_budget`.
- `manifest.json` — declared permissions (lynis + the report path).
