---
name: correlate-findings
description: "ANALYZE: the delta engine. Dedup is automatic via the fingerprint; this computes what CHANGED since the last run — new high-severity findings and regressions — and writes a run summary."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# correlate-findings (Logic / Analyze)

The engine of the loop. The loop's value is noticing *change*, not re-reporting
steady state. Deduplication is already guaranteed by the fingerprint upsert in
`lib/journal.sh`; this skill computes the **delta** against the previous run and
records a run summary the loop uses to decide whether to email.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

After the observe skills in every `/watchman audit` / `/watchman loop`, before
`send-report`/`report-status`.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher — `bash lib/wm <function> [args…]` — which sources the libs under bash internally; never `source lib/…` directly (dontAsk refuses a dot-source). Initialize with `bash lib/wm journal_init`.
2. **Compute the delta** against the previous run (use `last_seen_at` / the prior
   `runs` row as the boundary). The signal events, per profile:
   - **server** → `regressed` findings (a fix that came back) and newly-`open`
     findings at/above the notify severity;
   - **workstation** → the same, plus new outbound destinations surfaced by
     `inspect-logs` against the `baseline-network` snapshot, plus log-retention regressions.
3. **Regressions are loudest.** A `fixed`→`regressed` transition (already set by the
   journal upsert) is the highest-signal event — count and surface it prominently.
4. **Record the run.** Open with `bash lib/wm journal_run_start`, write a one-line `summary`
   (counts of new/regressed/cleared) with `bash lib/wm journal_run_finish`. This summary is what
   the loop threshold-checks.
5. **Read-and-record only.** This skill changes no system state; its only writes are
   routine journal updates (run row + any status normalization) through `lib/journal.sh`.
<!-- /origin -->

## Grounding

- `lib/journal.sh` — `journal_run_start`, `journal_run_finish`, `journal_count_open`, `journal_count_regressed` (reached via `bash lib/wm <function>`).
- `lib/profile.sh` — which deltas matter per profile (reached via `bash lib/wm <function>`).
