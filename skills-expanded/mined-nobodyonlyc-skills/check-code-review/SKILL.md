---
name: check-code-review
description: Review code changes for correctness, logic errors, security risks, and opportunities for simplification.
---

> **[Orchestrator Instructions]** Do NOT execute this skill yourself. You MUST use the invoke_subagent tool to spawn an independent subagent with the Role: **Principal Engineer**.


Gather the current changes to review:

```bash
git status
git diff --staged
git diff
```

If $ARGUMENTS is provided, treat it as a specific file or directory to focus on:
```bash
[ -n "$ARGUMENTS" ] && git diff -- "$ARGUMENTS" && git diff --staged -- "$ARGUMENTS"
```

Review the changes and write a report to `.harness/reports/code-review.md`. Your chat response must ONLY be the path to this file (e.g. "Review complete. See .harness/reports/code-review.md"). Do NOT output the report text in the chat.

## Bugs & Correctness
- Logic errors, edge cases not handled, broken error paths
- Incorrect assumptions about input types or ranges

## Security
- Any injection risks, exposed secrets, missing input validation

## Simplification
- Unnecessary complexity, duplicated logic, better built-ins available

## Format each finding as:
`[severity] file:line — description — suggested fix`

Severities (4-level, so the loop has a deterministic stop condition):
- **Critical** 🔴 — wrong logic, data loss, or a security vulnerability. Ships a broken product.
- **High** 🟠 — a real bug of lesser blast radius, or missing error handling on the main path.
- **Medium** 🟡 — maintainability problem, missing edge-case test, duplicated logic.
- **Low** 🔵 — style/nit not caught by a linter.

Keep the review concise — only findings worth acting on. Skip obvious style issues handled by linters.

## Exit criteria (the loop's stop condition)
The code-test-review loop (e.g. [workflow-feature](../workflow-feature/SKILL.md) Phase 2) needs an unambiguous definition of "clean". These exit criteria are that definition:
- **CLEAN** = zero Critical and zero High findings. Medium findings must be **recorded as a follow-up** (a new backlog item or the feature's notes) — never silently dropped. Low is optional.
- **NOT clean** = any Critical or High remains → the loop returns to implementation and re-reviews (counts against the iteration cap).

End the report with a machine-readable verdict on its own final line, so the orchestrator decides deterministically (not by re-reading prose):
```
VERDICT: CLEAN
```
or
```
VERDICT: ISSUES (critical: N, high: N, medium: N, low: N)
```
