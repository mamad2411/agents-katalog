---
name: check-pr-review
description: Perform an in-depth review of a pull request branch, comparing it to the base branch and pointing out issues.
---

> **[Orchestrator Instructions]** Do NOT execute this skill yourself. You MUST use the invoke_subagent tool to spawn an independent subagent with the Role: **Tech Lead**.


Gather the PR diff to review. If $ARGUMENTS is a PR number, fetch it; otherwise review the current branch:

```bash
# If PR number provided, fetch it; otherwise use local diff
PR="${ARGUMENTS:-}"
if [ -n "$PR" ]; then
  gh pr diff "$PR"
  gh pr view "$PR" --json title,body,author,additions,deletions,changedFiles
else
  git diff main..HEAD 2>/dev/null || git diff master..HEAD
  git log main..HEAD --oneline 2>/dev/null || git log master..HEAD --oneline
fi
```

Review the diff thoroughly and write a structured report to `.harness/reports/pr-review.md`. Your chat response must ONLY be the path to this file (e.g. "Review complete. See .harness/reports/pr-review.md"). Do NOT output the report text in the chat.

## Correctness
- List logic bugs, off-by-one errors, null/undefined risks, race conditions
- Flag any data loss or destructive operations without guards

## Security
- SQL injection, XSS, command injection, hardcoded secrets
- Missing auth/authorization checks, insecure defaults

## Code Quality
- Dead code, duplicated logic, missing error handling
- Naming issues, overly complex functions

## Suggestions
- Quick wins for simplification or performance
- Patterns that could be extracted/reused

For each finding: file + line reference, severity (🔴 critical / 🟡 warning / 🔵 suggestion), and a one-line fix hint.

End with: **Overall verdict** — Approve / Request changes / Needs discussion.
