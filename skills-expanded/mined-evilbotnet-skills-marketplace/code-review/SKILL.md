---
name: code-review
description: Review code changes and report severity-ranked findings with file:line references and suggested fixes. Use when the user asks for a code review of staged changes, a diff, a branch, or specific files.
---

# Code Review

Review the requested changes and produce a structured report.

## Procedure

1. Determine the review scope:
   - If the user named files or directories, review those.
   - Otherwise run `git diff --staged` (fall back to `git diff HEAD` if
     nothing is staged) and review the changed hunks plus enough
     surrounding context to judge correctness.
2. Evaluate each change against, in priority order:
   - **Correctness** — logic errors, unhandled edge cases, race conditions,
     broken error handling.
   - **Security** — injection, path traversal, secrets in code, unsafe
     deserialization, missing authz checks.
   - **Maintainability** — dead code, duplicated logic, misleading names.
   Do NOT report pure style preferences.
3. Rank each finding: `blocker`, `major`, `minor`, or `nit`.

## Output format

For each finding:

```
[severity] file:line — one-line summary
  Why it matters: ...
  Suggested fix: ...
```

End with a one-paragraph verdict: safe to merge, merge after fixes, or
needs rework. If you found nothing, say so explicitly rather than
inventing findings.
