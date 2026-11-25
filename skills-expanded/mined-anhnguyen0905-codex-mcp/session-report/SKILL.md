---
name: session-report
description: Create the six per-session codex-flow reports with fixed timing, templates, PIC attribution, measured Codex cost, and session-language rules.
---

# Session Reports

**Helpers**: required — session-cost.mjs (helper rule: missing → STOP; non-zero → surface error and STOP).

## Start the report bundle

At Phase 0, create `.codex-flow/reports/<YYYYMMDD-HHMMSS>/`.
Derive `<YYYYMMDD-HHMMSS>` from the session start in local time and keep it unchanged for the whole flow.

Start every report file with exactly this block:

```markdown
# <Report title>
- Session: <YYYYMMDD-HHMMSS>
- Generated: <ISO 8601>
- PIC: claude | codex | both (claude: <part>, codex: <part>)
```

## Write reports at their gates

- Write `planning.md` after Phase 2 plan approval. Capture interview outcomes, architecture decisions, and research findings. Set PIC to `claude`.
- Write `allocation.md` after Phase 3 backlog approval. Include a task → PIC table with execution PIC and review PIC, execution mode, and checkpoint choice. Set PIC to `claude`.
- Append to `tasks.md` after each task passes review or when a task is dropped or abandoned. At the moment of that decision, record it with `Result: dropped`. Add one section per task and never replace earlier task sections.
- Append to `reviews.md` immediately after each task's dual review resolves, at the same moment as the `tasks.md` append, and add a final-review section with its own `Codex review session:` line after the whole-feature dual review resolves. Set PIC to `both (claude: conformance/quality/security findings + verification verdicts, codex: codex_review findings)`.
- Write `cost.md` at the end of the flow. Include measured Codex data and qualitative Claude data.
- Write `SUMMARY.md` at the end of the flow. Include the delivered outcome, a PIC overview table covering every task and phase, and links to `planning.md`, `allocation.md`, `tasks.md`, `reviews.md`, and `cost.md`.

Use this section template in `tasks.md`:

```markdown
## T<n>: <title>
PIC: claude | codex | both (claude: <part>, codex: <part>)
Files: <files>
What was done: <summary>
Review PIC: both (claude: conformance/quality/security review + verification runs, codex: codex_review pass)
Review rounds: <n> (claude findings: <n>, codex findings: <n>)
Result: passed | passed-with-hand-fix | dropped
```

Use this section template in `reviews.md`:

```markdown
## T<n>: <title>
Codex review session: <sessionId | —>
### Claude findings
<numbered findings with severity + file:line, or "none">
### Codex findings
<numbered findings with severity + file:line, or "none">
### Comparison
Agreed: … | Unique to Claude: … | Unique to Codex: … | Conflicting: …
### Verdicts & conclusion
<per-finding verdict after verification (confirmed/rejected + evidence) and the chosen resolution>
```

## Enforce PIC semantics

Use only `claude`, `codex`, `both (claude: <part>, codex: <part>)`, or — for work done under the
command's Executor fallback — `claude (fallback: <reason>)` as PIC values.
Set planning and allocation PIC to `claude`.
Set each task implementation PIC to `codex`, or `claude (fallback: <reason>)` when the task ran
under the Executor fallback; set that task's review PIC to
`claude (fallback: conformance/quality/security + independent subagent review)`.
Always attribute the review line to `both (claude: conformance/quality/security review + verification runs, codex: codex_review pass)`.
After three failed review rounds and a Claude hand-fix, change the task PIC to `both (claude: hand-fix <what>, codex: implementation)`.

## Build the cost report

Set the `cost.md` PIC to `both (codex: measured tokens/duration from metrics.jsonl, claude: qualitative — phase durations, review rounds; tokens not measurable)`.
Read `<session-start ISO>` from the `- Session start: <ISO 8601>` line under `## Session report` in PLAN.md; if absent, fall back to the report-dir timestamp interpreted in local time.
Before running the helper, collect every Session id from TASKS.md (`- Session:` lines of all tasks,
worktree runs included — parallel tasks ran under other cwds, so a cwd filter would miss them) and
pass each as a `--session <id>` flag. Run the helper from the project root through the same absolute
plugin-root convention used for other runtime scripts:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/session-cost.mjs" --since "<session-start ISO>" --session <every task Session id> --session <review session ids from reviews.md> …
```

Use `--cwd <project root>` only when no session ids exist: `--cwd` misses worktree runs, and task ids alone miss review runs.

If the helper is not found, STOP and tell the user to reinstall the codex-flow plugin (its scripts/ directory is required); if it is present but exits non-zero, surface the error to the user and STOP. Never edit control files by hand.
Embed the helper's output in `cost.md` verbatim — `## Totals`, the nine-column `## Per model` table
(Model, Runs, Failed, Duration (ms), Input, Cached input, Output, Reasoning output, Sources), `## Per
tool`, the estimated-cost line, and `## Completeness` (Complete, Unpriced runs, Missing usage, Read
errors, History excluded). Never fabricate numbers and never embed raw stderr.
`Complete` is `no` whenever anything went unaccounted for: unpriced runs (usage reported without
`CODEX_MCP_PRICING`), entries missing usage, metrics-log read errors, or archived history left out —
re-run with `--history` to include the archives. Say in `cost.md` which of those made it `no`
instead of presenting an incomplete roll-up as the full session cost.
Always add Claude phase durations and the review rounds count, and mark Claude tokens explicitly as `not measurable`.

## Match the session language

Write narrative report text in the language the user used in the session.
When the user has used multiple languages, write each report in the language of the user's latest substantive request at the time the report is written.
Keep embedded `session-cost.mjs` output, including its tables and labels, in English as machine-generated content.

## Minimize report data

Summarize outcomes and review findings; never copy credentials, secrets, tokens, PII, or sensitive source excerpts into reports.
Reference file paths instead of pasting sensitive content.
