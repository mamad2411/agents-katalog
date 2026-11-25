---
name: review-feedback
description: Review verdict process — severity levels, the codex_continue feedback format that gets findings fixed in one round, and the 3-round escalation rule.
---

# Review Feedback Process

## Run status gate (before reviewing content)

Every `codex_execute`/`codex_continue`/`codex_review` result carries `schemaVersion: 1` and a
`status` field:

- `success` — completion marker seen, event stream parsed cleanly: review normally.
- `partial` (isError false) — the stream ended without a completion marker or had parse errors:
  treat Codex's output as suspect. Verify from the `diff` field and by running the acceptance
  checks yourself; prefer re-running via `codex_continue` over reviewing an incomplete result.
- `failed` / `aborted` (isError true) — do not review; handle as a failed run (report to the user,
  ask before retrying).

`unknownEvents` and `outputTruncated` are informational only — they never downgrade `status`.

## Severity levels

| Level | Meaning | Action |
|-------|---------|--------|
| CRITICAL | Security vulnerability, data loss, breaks existing behavior | Block — must fix this round |
| HIGH | Bug, unmet acceptance criterion, missing/false tests | Fix before task is done |
| MEDIUM | Maintainability concern, convention violation | Fix if the round is cheap; else note |
| LOW | Style/naming preference | Mention once; never spend a round on it alone |

## Improvements are non-blocking

Treat `IMP-n` items from `review-dual` as suggestions, not findings.
Never let them gate task completion or receive their own `codex_continue` round.
Append per-task items to `.codex-flow/IMPROVEMENTS.md`.
Execute them only after user approval at the `review-dual` improvement decision gate.

## Feedback format for `codex_continue`

Numbered, concrete, self-contained — Codex sees only what you send, not your reasoning:

```
Review findings to fix (address ALL, re-run the targeted tests for the touched files, do not change anything else):
1. [HIGH] src/api/users.ts:42 — `getUser` returns 200 with null body when the ID doesn't exist;
   acceptance criterion 2 requires 404. Fix the handler and add a test for the missing-ID case.
2. [MEDIUM] src/api/users.ts:15 — validation duplicates `validateId` from src/lib/validate.ts; use it.
```

Rules: exact file:line · observed vs expected behavior · which criterion/standard it violates · what "fixed" looks like. Group by file. Send CRITICAL/HIGH always; MEDIUM/LOW piggyback only on a round already being sent for CRITICAL/HIGH; otherwise record them in `.codex-flow/IMPROVEMENTS.md`.

## Round discipline

- Re-review after every round: pass the same `verifyCommand` on the `codex_continue` so acceptance re-runs mechanically, read `accepted`/`verification` from the fix-round result, verify each finding is actually fixed, and check nothing new broke — diff the diff.
- Max 3 rounds per task. Persisting findings after 3 rounds → stop sending to Codex; tell the user, then either fix by hand (flagging it) or re-plan the task.
- Never fix Codex's code yourself during rounds 1–3 — parallel edits desync the Codex session's view of the workspace.
- Clean review → proceed to the Phase 5 step 7 durable handoff, where `done` is the last write; state what was verified (verification passed, criteria met) — not just "looks good".
