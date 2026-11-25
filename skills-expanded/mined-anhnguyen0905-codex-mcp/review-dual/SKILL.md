---
name: review-dual
description: Run independent Codex and Claude reviews, reconcile findings by evidence, and track non-blocking improvements.
---

# Dual Review (Codex + Claude)

**Helpers**: required — none; optional — none.

Give every task TWO independent reviews: Claude reviews with the review-conformance, review-quality, and review-security skills; Codex reviews via `mcp__codex__codex_review` in a fresh read-only session so it never grades its own homework. Compare both reviews and select the optimal resolution supported by evidence.

## Codex reviewer role (focus block)

Paste this template into the `focus` parameter of `mcp__codex__codex_review`. Without checkpoint commits, each per-task `mcp__codex__codex_review` sees the cumulative uncommitted diff, so the `focus` block MUST name and enforce the task's `Files:` scope:

```text
Role: Act as an independent senior reviewer.
Task: <task id> — <task title>
Acceptance criteria: <paste the task's acceptance criteria>
Files: <paste the task's Files: list>
Review only the task's Files: list; report no findings outside it.
Review in this exact order:
1. Conformance to the task's .codex-flow/CONTEXT-T<n>.md slice and acceptance criteria.
Treat [verify]-stamped context as hypotheses to re-confirm against the current code before relying on it.
Read full .codex-flow/PLAN.md only as escalation when a finding disputes plan intent.
2. Quality: correctness hazards, silent failures, edge cases, and test quality.
3. Security: secrets, injection, validation, and unsafe patterns.
Output numbered findings tagged CRITICAL, HIGH, MEDIUM, or LOW.
For every finding, give file:line plus expected vs observed behavior.
Then add a SEPARATE `## Improvements` section.
Tag non-blocking suggestions IMP-1, IMP-2, ...: worthwhile refactors, better naming, missing nice-to-have tests, or documentation gaps that are not defects.
```

## Pass the task's scope, and route out-of-scope findings to the ledger

Call `mcp__codex__codex_review` with `scope: { files: <the task's `Files:` list>, contract: <the
PLAN Contracts the task lists> }` alongside `focus`. The server appends the contract and the file
list to the reviewer prompt and stamps each returned finding with `inScope`, counting the rest in
`reviewFindings.outOfScopeCount`.

A finding with `inScope: false` goes to the improvements ledger by default and never blocks the
task. It blocks only when the reviewer verifies, with evidence, that it affects THIS task's
acceptance criteria; say so explicitly when you promote one. Report `outOfScopeCount` with the
comparison result so a reviewer that ignored the declared scope is visible instead of silent.

## Run the two reviews concurrently

`mcp__codex__codex_review` is read-only and does not depend on Claude's pass, so never run the two
in series. Launch a background subagent whose single job is to call `mcp__codex__codex_review`
with the focus block above and return the result's `reviewFindings` and `status` verbatim; run
Claude's conformance → quality → security pass while it works; then compare. Only when the Agent
tool is unavailable call `mcp__codex__codex_review` directly after Claude's pass.

## Read Codex's findings from `reviewFindings`, not prose

The tool asks Codex to end with one fenced json block and parses it fail-closed into
`reviewFindings: { parsed, findings[], improvements[], dropped, droppedReasons[], parseError? }`.

- `parsed: true` → `findings[]` (severity ∈ CRITICAL/HIGH/MEDIUM/LOW, file, line, summary,
  expected, observed) and `improvements[]` (IMP ids) ARE the Codex review. Never re-grade a
  finding's severity from the surrounding prose.
- `dropped > 0` means Codex emitted malformed entries and **blocks acceptance**. The reviewer must
  read `droppedReasons` (one ordered reason per dropped entry, e.g. `findings[0].line`) and report
  them before treating the review as complete; a review with `dropped > 0` is incomplete, so the
  task stays not-accepted until the dropped entries are re-obtained in another reviewer round or the
  user explicitly waives them. Never reconstruct a dropped entry from the prose.
- `parsed: false` → say so to the user, work from the prose `agentMessage`, and mark every severity
  you assign yourself as unverified until the evidence check.

## Comparison protocol

- Bucket the union of Claude's and Codex's findings into agreed, unique-to-one, and conflicting.
- Verify EVERY finding with evidence: read the code and run the relevant test. Let the evidence determine the verdict, not the reviewer.
- Feed verified findings into the normal `mcp__codex__codex_continue` round per review-feedback severity rules (CRITICAL/HIGH always; MEDIUM/LOW piggyback only on a round already being sent for CRITICAL/HIGH; otherwise record them in `.codex-flow/IMPROVEMENTS.md`).
- Use AskUserQuestion ONLY when a CRITICAL/HIGH finding cannot be verified either way, or two mutually exclusive valid fixes exist.
- Give the verified outcome, including counts for each bucket and the resolution, to the single
  post-review Decision-log writer defined in `plan-architecture`; do not append from this review step.
- If `mcp__codex__codex_review` fails, times out, or returns status `partial`, proceed with Claude-only review, tell the user, and do not auto-retry because of quota.

## Improvements ledger

Append non-blocking improvements from BOTH reviews to `.codex-flow/IMPROVEMENTS.md`, one per line:
`- [ ] IMP-<n> (T<k>, source: codex|claude|both) <description> — <file:line>`
Allocate `IMP-<n>` from one global counter across the whole run, never from per-review counters.
When Claude and Codex suggest the same improvement, record ONE line with `source: both`.
The ledger NEVER blocks marking a task done and NEVER spends an `mcp__codex__codex_continue` round.

Optional Jev assist (off by default): load `codex-flow:jev-assist`.

## Improvement decision gate

- Consider only unchecked ledger entries without an `(approved: T<n>)` marker as pending. If `.codex-flow/IMPROVEMENTS.md` is missing or has no unchecked pending entries, skip AskUserQuestion and note "no improvements" in the delivery summary.
- After the final whole-feature review, compile those entries into a summary and proposed execution plan, grouped and effort-estimated, then present it via AskUserQuestion.
- Slice approved items into new tasks and append them to `.codex-flow/TASKS.md`. Mark each approved ledger line `(approved: T<n>)` when its task is created, then check it off when the task passes review.
- Run approved tasks through the normal Phase 4 → Phase 5 loop. Improvement tasks spawned by the gate do NOT re-trigger the decision gate themselves.
- Have the orchestrator record declined items once using `plan-architecture`'s non-task event-block
  schema, then check off each ledger line with `(declined)`.
