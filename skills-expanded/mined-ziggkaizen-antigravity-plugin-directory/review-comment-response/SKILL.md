---
name: review-comment-response
description: Helps address reviewer comments safely and verify that review feedback was resolved without unrelated changes. Use when responding to PR comments, code review feedback, requested changes, or reviewer questions.
---

# Review Comment Response

Use this skill when responding to reviewer feedback or requested changes.

## When to Use This Skill

Use this skill when:

- a reviewer requested changes
- a review comment needs a code response
- a reviewer asked a question
- multiple comments need triage
- comments may conflict
- the agent must verify comments were resolved

## Response Principles

- Address the comment directly.
- Do not widen scope.
- Ask for clarification when the requested change is ambiguous or unsafe.
- Prefer minimal code changes.
- Explain when a requested change is not appropriate.
- Link the resolution to validation.
- Separate code changes from explanatory responses.

## Workflows

Use these workflows:

- `workflows/respond-to-review-comments-workflow.md`
- `workflows/verify-review-comment-resolution-workflow.md`

## Resources

Use:

- `resources/comment-response-template.md`
