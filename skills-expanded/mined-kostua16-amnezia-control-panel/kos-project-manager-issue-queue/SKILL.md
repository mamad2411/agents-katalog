---
name: kos-project-manager-issue-queue
description: Project-manager issue queue rules: latest standalone issues, safe /fix eligibility, active-fix dedupe, and terminal label skips.
user-invocable: true
when_to_use: "When implementing or reviewing project-manager issue queue behavior."
category: workflows
keywords: [project-manager, issue-queue, fix-issue, triage, github-issues]
metadata:
  author: project-manager
  license: repo
  version: "1.0"
---

# Project Manager Issue Queue

The issue queue route runs when PR pressure is low and standalone issue count is above the configured threshold.

## Selection

- Latest open standalone issues first.
- Default cap: 10 issues per run.
- Exclude pull requests.
- Exclude terminal/manual labels: `fixed`, `duplicate`, `canceled`, `keep-open`, `in-progress`, `needs-review`.
- Exclude issues with linked PR evidence in body/comments.
- Exclude issues with active `fix-issue.yml` runs or `claude-fix-issue-*` branches.
- Exclude issues with recent project-manager `/fix`.

## Action

Post exact `/fix` using maintainer `GH_PAT`. The `fix-issue.yml` workflow owns branch creation, validation, commit, PR creation, and reporting.

## Critical constraints

- Project-manager never edits code in the issue route.
- Do not batch more than the configured issue limit.
- Do not retrigger when a fix is already active.
