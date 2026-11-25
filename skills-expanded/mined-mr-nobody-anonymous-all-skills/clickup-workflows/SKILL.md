---
name: clickup-workflows
description: "Automate ClickUp: hierarchy (workspace, space, folder, list, task), custom fields, status transitions, and API-driven task hygiene."
type: procedural
category: project-management
domain: project-management
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: beginner
triggers:
  - clickup api task create
  - clickup custom fields
  - clickup status workflow
  - clickup automation script
  - sync issues to clickup
keywords:
  - clickup
  - tasks
  - custom-fields
  - statuses
  - api
  - project-management
source: custom
enabled: true
---

# ClickUp Workflows

## Purpose

Automate ClickUp: hierarchy (workspace, space, folder, list, task), custom fields, status transitions, and API-driven task hygiene.

## When to Use

- Work items must be created or synced into ClickUp from another system.
- Custom fields and statuses need a consistent model before automation.
- Stale tasks need a scheduled hygiene pass.

## When NOT to Use

- The team tracks work in GitHub Issues or Jira and ClickUp is incidental.
- You need gantt-level portfolio planning a human should own.
- The workspace has no agreed status model yet; define it first.

## Capabilities

- Map the ClickUp hierarchy correctly before creating anything.
- Use custom fields as typed data rather than text in descriptions.
- Transition statuses through valid paths without orphaning tasks.
- Sync with external trackers using stable external ids.

## Inputs

- The workspace/space/list ids and the API token scope.
- The status model and which transitions are legal.
- The external system's identifiers for idempotent sync.

## Workflow

1. List spaces and lists first to learn ids; never guess them.
2. Define custom fields with explicit types before writing data.
3. Create tasks with an idempotency key stored as a custom field.
4. Move tasks via the documented status endpoints, not by rewriting fields.
5. Schedule a hygiene pass for stale or unassigned tasks.

## Tools

- ClickUp API v2
- ClickUp MCP connector
- a scheduler

## Examples

- `allskills mcp install --harness cursor --servers clickup`
- `curl -s -H "Authorization: $CLICKUP_API_KEY" "https://api.clickup.com/api/v2/space"`
- `allskills route "create tasks from bug reports"`

## Safety

- Bulk status changes can trigger client-visible notifications; batch and stage them.
- Deleting a list deletes its tasks; archive instead.
- Tokens are workspace-wide by default; restrict by role where possible.

## Source

All-Skills canonical library (`skills/project-management/clickup-workflows`). First-party skill, maintained in this repository.

## Notes

- Hierarchy mistakes are expensive to undo; model spaces before lists.
- Custom field ids differ per workspace — resolve them at runtime.
- Pairs with: `productivity/airtable-workflows`, `productivity/issue-triage`.
