---
name: multica-projects
description: Create and manage Multica projects — containers that group related issues (sprints, epics, workstreams). Covers project CRUD, status transitions, and attaching issues. Use when the user mentions a sprint, epic, project, or wants to group / filter issues by a larger initiative.
---

# Multica Projects

A **project** groups related issues (sprint, epic, workstream). Every project belongs to a workspace and can optionally have a lead (a human member or an agent).

Official docs: https://github.com/multica-ai/multica/blob/main/CLI_AND_DAEMON.md#projects

## When to use this skill

- The user wants to start a new sprint, epic, or initiative.
- Filtering the board by a container larger than a single issue.
- Assigning a lead (human or agent) responsible for a body of work.
- Closing out / archiving a completed sprint.

## Core commands

```bash
multica project list
multica project list --status in_progress
multica project list --output json

multica project get <id>
multica project get <id> --output json

multica project create --title "2026 Week 16 Sprint" --icon "S" --lead "Lambda"
multica project update <id> --title "New title" --status in_progress
multica project update <id> --lead "Lambda"

multica project status <id> in_progress
multica project delete <id>
```

Create flags: `--title` (required), `--description`, `--status`, `--icon`, `--lead`.
Update flags: same set, all optional.
Valid statuses: `planned`, `in_progress`, `paused`, `completed`, `cancelled`.

`--lead` takes a name or UUID (same resolution rules as `--assignee` on issues).

## Attaching issues to projects

Projects are associated via the `--project` flag on issue commands — there is no separate `project add-issue` command.

```bash
# New issue in a project
multica issue create --title "Login bug" --project <project-id>

# Move an existing issue
multica issue update <issue-id> --project <project-id>

# Filter issues by project
multica issue list --project <project-id>
multica issue list --project <project-id> --status in_progress --output json
```

## Common flows

**Spin up a weekly sprint and pre-populate it:**

```bash
PROJECT=$(multica project create \
  --title "2026-W17 Sprint" --icon "S" --lead "Lambda" \
  --output json | jq -r '.project.id')

multica issue create --title "Ship search redesign" --project "$PROJECT" --assignee "Lambda"
multica issue create --title "Audit auth middleware"  --project "$PROJECT" --assignee "Codex"
```

**Close out a sprint and reassign stragglers to the next one:**

```bash
OLD=<old-project-id>; NEW=<new-project-id>

# Move anything still open
multica issue list --project "$OLD" --output json |
  jq -r '.issues[] | select(.status != "done" and .status != "cancelled") | .id' |
  xargs -I {} multica issue update {} --project "$NEW"

multica project status "$OLD" completed
```

## Gotchas

- Deleting a project does **not** delete its issues — they just become project-less. Confirm intent before calling `project delete`.
- Icons are short strings, not emoji-only; any short glyph works.
- A project lead is informational (shown on the project card) and does not auto-assign issues to that lead.
