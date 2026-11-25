---
name: asana
description: "Asana task & project management via REST API — create, search, update tasks; manage projects and sections."
version: 1.0.0
author: Hermes + Pat Diamitani
platforms: [linux, macos]
required_credential_files:
  - path: asana_token
    description: Asana Personal Access Token (stored in skill dir)
---

# Asana

Full Asana REST API integration for task & project management. Powers the Master Calendar pipeline.

## Setup

Run once to store your Personal Access Token:

```bash
python3 ~/.hermes/skills/productivity/asana/scripts/setup.py --token "YOUR_ASANA_PAT"
```

Get a token at: https://app.asana.com/0/my-apps

## Usage

Set a shorthand:

```bash
ASANA="python3 ~/.hermes/skills/productivity/asana/scripts/asana_cli.py"
```

### Tasks

```bash
# Create a task
$ASANA task create --name "Review Q4 deck" --project 1216602500278026 --due 2026-07-20
$ASANA task create --name "Call dentist" --project 1216602500278026 --due 2026-07-18 --notes "Dr. Smith, 312-555-0100" --section "Daily"

# Create with NPAO metadata in notes
$ASANA task create --name "Fix login bug" --project 1216602500278026 --due today \
  --notes "phase:debug|priority:9.2|impact:revenue|source:hermes"

# List tasks (with filters)
$ASANA task list --project 1216602500278026
$ASANA task list --project 1216602500278026 --due-today
$ASANA task list --project 1216602500278026 --due-this-week
$ASANA task list --project 1216602500278026 --due-on 2026-07-20
$ASANA task list --project 1216602500278026 --incomplete
$ASANA task list --project 1216602500278026 --section "Daily"

# Get task details
$ASANA task get TASK_GID

# Update task
$ASANA task update TASK_GID --name "New name" --due 2026-07-25 --completed
$ASANA task update TASK_GID --notes "Updated notes"
$ASANA task update TASK_GID --section SECTION_GID

# Delete task
$ASANA task delete TASK_GID

# Search across workspace
$ASANA task search --workspace 1206772437471958 --text "Q4 budget"
```

### Projects

```bash
# List projects in workspace
$ASANA project list --workspace 1206772437471958

# Get project
$ASANA project get 1216602500278026

# Update project (default view, name, etc.)
$ASANA project update 1216602500278026 --default-view calendar
$ASANA project update 1216602500278026 --name "New Name"
```

### Sections

```bash
# List sections
$ASANA section list --project 1216602500278026

# Create section
$ASANA section create --project 1216602500278026 --name "This Week"
```

### Calendar Operations

```bash
# Get all tasks for a date range (calendar view)
$ASANA calendar range --project 1216602500278026 --start 2026-07-15 --end 2026-07-21

# Get today's tasks
$ASANA calendar today --project 1216602500278026

# Upcoming tasks (next N days)
$ASANA calendar upcoming --project 1216602500278026 --days 7
```

## Output Format

All commands return JSON arrays. Parse with jq:

- **task list**: `[{gid, name, due_on, completed, assignee, notes, section, permalink_url}]`
- **task create**: `{gid, name, due_on, permalink_url}`
- **task get**: `{gid, name, due_on, completed, notes, assignee, section, projects, permalink_url, created_at}`
- **project get**: `{gid, name, default_view, sections, permalink_url}`
- **calendar range**: `[{gid, name, due_on, completed, section_name}]`

## NPAO Integration

When creating tasks from Hermes, the `--notes` field carries NPAO metadata:

```
phase:debug|priority:9.2|impact:revenue|source:hermes
```

Supported tags:
- `phase`: pred | design | dev | deploy | debug
- `priority`: 0.0-10.0 (NPAO composite score)
- `impact`: revenue | ux | team | internal | nice
- `source`: email | hermes | gcal | manual
- `blocked_by`: TASK_GID
- `est_hours`: float

## Reference

- Asana API docs: https://developers.asana.com/reference/rest-api-reference
- Master Calendar project: https://app.asana.com/0/1206772437471958/1216602500278026
