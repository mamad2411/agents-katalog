---
name: vault-capture
description: Instant smart-routing capture of bugs, ideas, tasks, and notes into the Obsidian vault without leaving your current work context. Use this skill whenever the user says "log a bug", "capture this", "note this", "vault:", "add a task", "I had an idea", or any variation of wanting to remember or track something. Captures items in a format the new controller can reason about cleanly.
---

# vault-capture

Quick-capture items into the Obsidian vault with smart routing.

## Vault Path

`{{VAULT_PATH}}`

## Controller Contract

Every new governed item should be controller-friendly on creation.

Required fields:

- `id`
- `type`
- `priority`
- `project`
- `status`
- `created`
- `updated`
- `next_action`

Preferred fields:

- `module`
- `complexity`
- `blocked_by`
- `related`
- `owner_family`
- `owner_instance`
- `branch`
- `worktree_path`
- `claimed_at`
- `completed_at`
- `proof_state`

Use canonical statuses only:

- `open`
- `claimed`
- `in-progress`
- `blocked`
- `done`
- `wont-do`

## Step 1: Parse the input

Extract:

- `type`: bug, task, idea, feature, decision, note
- `project`: infer from cwd if not stated
- `priority`
- `module`
- `description`
- `blocked_by`
- `related`
- `next_action`

If `next_action` is not explicit, derive a concrete first step from the description.

## Step 2: Duplicate detection

Search with:

```text
mcp__vault-index__search_vault(query="{key terms from description}", project="{project}")
```

Only stop for clear duplicates.

## Step 3: Smart routing

| Condition | Folder |
|---|---|
| agent-ready bug | `01-Bugs/` |
| agent-ready task | `02-Tasks/` |
| idea | `03-Ideas/` |
| feature needing design | `00-Inbox/` |
| decision or note needing human review | `00-Inbox/` |
| vague / missing project | `00-Inbox/` |

## Step 4: Assess complexity

For bugs and tasks only:

- `low`
- `medium`
- `high`

## Step 5: Write the file

Filename:

`YYYYMMDD-HHmmss-{type}-{slug}.md`

Frontmatter:

```yaml
---
id: {stable id}
type: {type}
priority: {priority}
project: {project}
module: {module or null}
status: open
complexity: {low|medium|high|null}
owner_family: null
owner_instance: null
branch: n/a
worktree_path: null
claimed_at: null
completed_at: null
handoff_from: null
handoff_note: null
proof_state: null
blocked_by: []
related: []
next_action: {one concrete next step}
created: {ISO 8601 timestamp}
updated: {ISO 8601 timestamp}
tags: []
---
```

Body:

- summary
- context
- reproduction or rationale if relevant
- dependencies if known

### ID format

Prefer the existing vault style:

- `{type}_{project}_{timestamp}_{slug-or-hash}`

Keep it stable. Do not omit `id`.

### Decision items

Decision notes may still route to `00-Inbox/`, but include:

- `chosen`
- `rationale`
- `alternatives`
- `consequences`

## Step 6: Re-index

Call:

```text
mcp__vault-index__index_vault(incremental=true)
```

## Step 7: Confirm

Print one line:

```text
[TYPE] -> <folder> | <project>/<module> | complexity: <level> | next: <next_action>
```

