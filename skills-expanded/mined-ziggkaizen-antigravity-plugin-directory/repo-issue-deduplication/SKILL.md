---
name: repo-issue-deduplication
description: Reviews whether an issue is a duplicate, related item, regression, umbrella issue, or follow-up. Use before creating new tracker items or when merging, linking, closing, or commenting on similar issues.
---

# Repo Issue Deduplication

Use this skill before creating new issues when tracker search is available, or when evaluating whether to link, merge, close, or split similar issues.

## Deduplication Rules

- Similar symptoms are not always duplicates.
- Same root cause is not always same user-facing issue.
- Do not close as duplicate without confirming the target issue covers the affected environment, impact, and acceptance criteria.
- Prefer linking related issues when uncertainty remains.
- Preserve unique evidence from duplicates before closing or merging.

## Workflow

Use `workflows/duplicate-issue-review-workflow.md`.

## Resources

- `resources/duplicate-analysis-checklist.md`
