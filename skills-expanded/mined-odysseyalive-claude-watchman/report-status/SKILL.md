---
name: report-status
description: "EXPRESS: a human-readable summary of journal state — open, regressed, fixed, ignored — leading with what matters most. Read-only."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# report-status (Rhetoric / Express)

Turns the journal into something a person can act on. Reads the journal and prints
a plain-language summary, led by the `prioritize-redflags` ranking. Strictly
read-only — it makes no changes and sends no mail (that is `send-report`).

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

`/watchman report`, and as the body builder for `send-report`.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher — `bash lib/wm <function> [args…]` — which sources the libs under bash internally; never `source lib/…` directly (dontAsk refuses a dot-source). Initialize with `bash lib/wm journal_init`.
2. **Read** the journal through `lib/journal.sh` only (`bash lib/wm journal_list`, counts). Group
   by status: **regressed** first (loudest), then **open** by priority, then a tally
   of **fixed**/**ignored**.
3. **Explain in plain language.** For each surfaced finding: what it is, why it
   matters, its risk tier, and the suggested remediation — no jargon dumps.
4. **Lead with the trend.** Include the latest `lynis_hardening_index` and its
   direction since last run, and the regression count.
5. **Output text** suitable for a terminal and for the email body. Change nothing.
<!-- /origin -->

## Grounding

- `lib/journal.sh` — `journal_list`, `journal_count_open`, `journal_count_regressed`, metric reads (reached via `bash lib/wm <function>`).
- `prioritize-redflags` — supplies the ordering.
- `send-report` — wraps this output for email.
