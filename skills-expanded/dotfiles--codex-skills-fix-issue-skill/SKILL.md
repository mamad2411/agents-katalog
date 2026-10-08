---
name: "fix-issue"
description: "Reproduce a bug, implement the smallest correct fix, and verify the result with focused testing."
---

# Fix Issue

## Workflow

1. Identify the failing behavior from the issue, logs, or reproduction steps.
2. Read the smallest set of files needed to understand the bug.
3. Reproduce the bug with a test, command, or concrete verification step.
4. Implement the smallest fix that addresses the root cause.
5. Run focused verification first, then broader checks when warranted.
6. Summarize the root cause, the fix, and the verification performed.

## Rules

- Do not refactor unrelated code while fixing the issue.
- Prefer a failing test before the fix when the repo has a test harness.
- If the bug cannot be reproduced, say so clearly and document what was checked.
- Remove only dead code made obsolete by the fix itself.
