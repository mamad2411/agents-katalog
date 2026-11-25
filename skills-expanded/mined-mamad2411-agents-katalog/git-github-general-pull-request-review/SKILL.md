---
name: git-github-general-pull-request-review
description: Prepares, reviews, and improves GitHub pull requests. Use when writing PR descriptions, reviewing diffs, running pre-push PR reviews, responding to comments, checking conflict resolution, or deciding whether a change is ready for merge.
license: MIT
compatibility: Requires access to repository diffs; optional GitHub CLI or GitHub MCP server for GitHub metadata.
---

# Git/GitHub Pull Request Review

This skill helps agents produce focused, reviewable pull requests and useful code reviews.

## When to Use This Skill

Use this skill for:

- preparing pull request descriptions;
- running pre-PR reviews before pushing branches;
- reviewing changed files;
- responding to review comments;
- resolving conflicts;
- deciding whether a PR is ready for merge;
- summarizing risks and testing evidence.

## Review Principles

1. Understand the intended change before judging implementation.
2. Compare behavior against requirements, not only code style.
3. Inspect tests, migrations, generated files, dependencies, and operational effects.
4. Run pre-PR reviews locally before pushing when possible.
5. Keep comments actionable and respectful.
6. Separate blockers from suggestions.
7. Avoid approving, merging, closing, or changing PR metadata without user intent.

## Pull Request Preparation Checklist

- State what changed and why.
- Link issue or context when available.
- Include test evidence.
- Include screenshots or logs only when useful and safe.
- Call out migrations, breaking changes, rollout risks, and rollback plan.
- Keep scope small enough to review.
- Run `workflows/pre-pr-review-before-push-workflow.md` before pushing when the change is non-trivial.

## Workflows

- `workflows/pre-pr-review-before-push-workflow.md`: Use before pushing a branch or opening a PR; collect a PR-style diff and invoke `repo-code-review-pre-pr-review`.
- `workflows/pull-request-review-workflow.md`: Use for reviewing PRs, local diffs, or agent-authored changes.
- `workflows/conflict-resolution-workflow.md`: Use for merge, rebase, cherry-pick, or PR conflict resolution.

## Resources

- `resources/pull-request-review-checklist.md`
- `resources/review-comment-style-guide.md`

## Examples

- `examples/pull-request-description-template.md`
- `examples/review-summary-example.md`