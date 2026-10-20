---
name: pr-issue-triage
description: Canonical PR/Issue triage pack combining repo review queues with work tracker context and approval-gated write-backs.
tags: [pr, pull request, issue, triage, github, gitlab, linear, jira]
keywords:
  - pr
  - pull request
  - issue
  - triage
  - github
  - gitlab
  - linear
  - jira
triggers:
  - triage repo work
  - review queue
  - stale issues
  - blocked pull requests
context_tags:
  - development
  - workflow
  - git
canonical_pack: true
delivery_modes:
  - manual
  - routine
prerequisite_hints:
  - "Repo connector required: `github` or `gitlab` should be ready."
  - "Tracker connector optional but preferred: `linear` or `jira` should be ready."
  - "Write actions require fresh approval even when read-only triage is available."
source_links:
  - plugins/zorai-plugin-github/README.md
  - plugins/zorai-plugin-gitlab/README.md
  - plugins/zorai-plugin-linear/README.md
  - plugins/zorai-plugin-jira/README.md
mobile_safe: true
approval_behavior: "Read-only triage is allowed without extra approval; comment/label/assign/merge/state-change actions must request fresh approval."
---

# PR / Issue Triage

## User story

I want one triage view across repo review items and issue tracker work, so I can see stale, blocked, and actionable items without manually stitching together GitHub/GitLab and Linear/Jira.

## Pack contract

### Prerequisites and readiness

- Requires one repo connector: `github` or `gitlab`
- Optionally enriches with one tracker connector: `linear` or `jira`
- If the tracker is unavailable, the pack still runs as repo-only triage and clearly marks tracker enrichment as degraded.

### Inputs and configuration fields

- `repo_connector`: `github` or `gitlab`
- `tracker_connector`: `linear`, `jira`, or `none`
- `owner` / `repo` or equivalent project coordinates
- `include_writeback_suggestions`: boolean
- `stale_days`: integer threshold

### Outputs and delivery targets

- merged queue showing:
  - open PRs / review items
  - open issues / work items
  - stale items
  - blocked items
  - suggested next actions
- source links should point back to the original PR/issue/tracker item
- write-back suggestions must be clearly marked `approval-required`

## Manual run recipe

1. List repo review items and work items from the chosen repo connector.
2. If tracker is ready, fetch tracker work items and merge by title/ID/reference where possible.
3. Summarize stale and blocked items.
4. Suggest write-backs separately from the read-only report.

## Example routine wiring

Schedule as a weekday triage routine or on-demand review block. Example payload description:

`Run the canonical PR/Issue Triage pack for the main repo, merge repo/tracker context, and surface approval-gated write-back suggestions.`

## Example prompt

`Run PR/Issue Triage for owner/repo using GitHub plus Linear. Show stale PRs, blocked issues, and suggested labels/comments, but do not perform write-backs without approval.`

## Failure and recovery behavior

- Missing repo connector -> fail closed with setup hint.
- Missing tracker connector -> continue with repo-only triage.
- Proposed write-back with no approval -> keep suggestion in the report, do not execute it.

## Verification checklist

- [ ] Manual repo-only proof passes.
- [ ] Manual repo + tracker proof passes.
- [ ] Missing tracker degrades gracefully.
- [ ] Write-back suggestions are clearly approval-gated.
- [ ] Source links are present for triaged items.
