---
name: prioritize-redflags
description: "ANALYZE: severity scoring against the baseline and profile, so the report leads with what actually matters on THIS machine."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# prioritize-redflags (Logic / Analyze)

Orders the journal by what matters *here*. Raw severity is not enough: the same
finding ranks differently on a public server than a workstation, and a regression
outranks a long-standing known issue. Produces the ranking the report leads with.
Its only writes are routine journal updates through `lib/journal.sh`.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

After `correlate-findings`, before `report-status`/`send-report`.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher — `bash lib/wm <function> [args…]` — which sources the libs under bash internally; never `source lib/…` directly (dontAsk refuses a dot-source). Initialize with `bash lib/wm journal_init`.
2. **Score** each `open`/`regressed` finding from: base `severity`, profile weight
   (`bash lib/wm profile_severity` for its `check_id`), status (`regressed` gets a boost — a fix
   that came back is urgent), category, and exposure (a `security` finding on a
   public-facing `server` outranks the same on a workstation).
3. **Normalize severity where the profile demands it.** If `bash lib/wm profile_severity` says a
   check carries a different weight here than its default, update the finding's
   `severity` via `lib/journal.sh` so the report and thresholds agree.
4. **Emit the ranking** for `report-status`/`send-report` to consume (highest first).
5. **Never reclassify a finding's risk_tier downward to make a fix easier** — the
   risk tier is a safety boundary, not a priority knob.
<!-- /origin -->

## Grounding

- `lib/profile.sh` — `profile_severity`, profile exposure weighting (reached via `bash lib/wm <function>`).
- `lib/journal.sh` — finding reads and severity updates (reached via `bash lib/wm <function>`).
- `correlate-findings` — supplies the delta this ranking emphasizes.
