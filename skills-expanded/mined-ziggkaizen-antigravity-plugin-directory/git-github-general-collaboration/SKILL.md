---
name: git-github-general-collaboration
description: Coordinates GitHub collaboration workflows for issues, branches, pull requests, review requests, maintainer handoffs, and stale PR triage. Use when connecting GitHub issues to implementation work, preparing collaboration updates, requesting review, handing work to maintainers, or using GitHub MCP tools for issue and PR coordination.
---

# GitHub Collaboration

Use this skill for repository collaboration work that involves GitHub issues, pull requests, branches, reviewers, maintainers, labels, milestones, and GitHub MCP tools.

This skill complements:

- `git-github-general-repository-maintenance` for local repository hygiene and branch safety.
- `git-github-general-pull-request-review` for PR review quality.
- `git-github-general-release-management` for releases, tags, hotfixes, and rollback planning.

## When to Use This Skill

Use this skill when asked to:

- connect an issue to a branch or pull request
- draft or improve a pull request description
- prepare a review request
- respond to maintainer or reviewer comments
- summarize issue or PR status
- hand work off to another maintainer
- triage stale pull requests
- propose labels, milestones, assignees, or reviewers
- use GitHub MCP tools to read or update issues and pull requests

## Safety Requirements

- Confirm repository owner/name before using GitHub MCP write tools.
- Confirm issue and pull request numbers before referencing or updating them.
- Draft comments before posting when the action affects collaborators.
- Do not close, merge, assign, label, reopen, retarget, or edit issues or PRs without explicit user intent.
- Do not expose secrets, customer data, security reports, private incident details, or internal links in GitHub comments.
- Keep public collaboration messages concise, factual, and action-oriented.
- Do not use GitHub collaboration workflows as a substitute for code review, CI/CD release gates, or issue-tracker-neutral triage.

## Collaboration Decision Points

Use `resources/collaboration-decision-matrix.md` when deciding whether to draft, comment, label, request review, hand off, or ask for more information.

Use `resources/issue-pr-linking-checklist.md` before linking issues, pull requests, commits, or releases.

Use `resources/maintainer-handoff-template.md` when preparing a handoff summary.

## Workflows

- `workflows/issue-to-pr-workflow.md`: Use when moving from a GitHub issue to an implementation branch and pull request.
- `workflows/review-request-workflow.md`: Use when requesting review or preparing a PR for reviewers.
- `workflows/maintainer-handoff-workflow.md`: Use when summarizing work for another maintainer or contributor.
- `workflows/stale-pr-triage-workflow.md`: Use when evaluating old or inactive pull requests.

## Examples

- `examples/issue-to-pr-summary.md`
- `examples/review-request-message.md`
- `examples/maintainer-status-update.md`

## Scripts

This skill intentionally includes no scripts.

GitHub collaboration actions usually require human judgment and, when MCP write tools are enabled, explicit confirmation before mutating remote repository state.
