---
name: repo-issue-action-safety
description: Reviews issue-tracker write actions for safety. Use before creating, updating, assigning, labeling, closing, deleting, moving, bulk-editing, or commenting on issues through MCP tools, CLIs, APIs, or automation.
---

# Repo Issue Action Safety

Use this skill before any issue tracker write action.

## High-Risk Actions

Ask for explicit approval before:

- closing issues
- deleting issues
- bulk editing
- changing priority, severity, owner, sprint, milestone, or project
- adding customer-visible comments
- creating issues containing sensitive reports
- changing security vulnerability status
- moving work across teams

## Required Review

Before a write action, state:

- tracker
- project/team
- issue key or title
- exact action
- fields changed
- privacy risks
- reversibility
- reason
- validation

## Workflow

Use `workflows/issue-action-safety-workflow.md`.

## Resources

- `resources/tracker-action-safety-checklist.md`

## Scripts

This skill owns:

```text
scripts/guard-issue-action-command.py
scripts/issue-triage-final-reminder.py
```

Run scripts with `--help` before manual use.
