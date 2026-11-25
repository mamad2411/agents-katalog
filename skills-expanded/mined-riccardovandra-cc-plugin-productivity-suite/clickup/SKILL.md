---
name: clickup
description: Browse ClickUp tasks across spaces/folders/lists, view task details, update status, and read comments. Use when user mentions ClickUp, tasks, project management, task status, or asks "what's on my plate" or "show my tasks".
---

# ClickUp Skill

Browse your ClickUp workspace, view tasks, update status, and read comments. Read-focused with minimal write operations (status updates only).

## Quick Start

**See all spaces:**
> "What spaces do I have in ClickUp?"

**List tasks in a space:**
> "Show tasks in the Client Work space"

**Find a specific task:**
> "What's the status of the homepage redesign task?"

**Update task status:**
> "Mark the API integration task as complete"

**Read comments:**
> "Show me comments on task abc123"

## Available Operations

| Operation | Module | Script | Description |
|-----------|--------|--------|-------------|
| List Spaces | [LIST.md](modules/LIST.md) | `list_spaces.py` | Show all spaces in workspace |
| List Tasks | [TASKS.md](modules/TASKS.md) | `list_tasks.py` | List tasks with filters |
| Task Details | [TASKS.md](modules/TASKS.md) | `task.py` | Get full task details |
| Update Status | [STATUS.md](modules/STATUS.md) | `update_status.py` | Change task status |
| Read Comments | [COMMENTS.md](modules/COMMENTS.md) | `comments.py` | View task comments |

## Scripts

### List Spaces
```bash
uv run scripts/list_spaces.py              # All spaces
uv run scripts/list_spaces.py --with-folders   # Include folders
uv run scripts/list_spaces.py --with-lists     # Include all lists
```

### List Tasks
```bash
uv run scripts/list_tasks.py --space "Client Work"
uv run scripts/list_tasks.py --folder "ProjectX"
uv run scripts/list_tasks.py --list "Sprint 1"
uv run scripts/list_tasks.py --space "Client Work" --status "in progress"
uv run scripts/list_tasks.py --include-closed
```

### Get Task Details
```bash
uv run scripts/task.py abc123              # By task ID
uv run scripts/task.py --search "homepage"  # Search by name
uv run scripts/task.py --search "api" --space "Engineering"
```

### Update Task Status
```bash
uv run scripts/update_status.py abc123 --status "in progress"
uv run scripts/update_status.py abc123 --complete   # Shorthand for complete
uv run scripts/update_status.py --search "homepage" --status "review"
```

### Read Comments
```bash
uv run scripts/comments.py abc123          # All comments on task
uv run scripts/comments.py abc123 --limit 10
uv run scripts/comments.py --search "homepage"
```

## Conversational Patterns

| Request | Action |
|---------|--------|
| "What spaces do I have?" | Run `list_spaces.py` |
| "Show tasks in [space]" | Run `list_tasks.py --space "[space]"` |
| "What's in the [folder] folder?" | Run `list_tasks.py --folder "[folder]"` |
| "Tasks in progress in [space]" | Run `list_tasks.py --space "[space]" --status "in progress"` |
| "What's the status of [task]?" | Run `task.py --search "[task]"` |
| "Mark [task] as done" | Run `update_status.py --search "[task]" --complete` |
| "Show comments on [task]" | Run `comments.py --search "[task]"` |

## Activation Triggers

- "clickup", "tasks", "task list"
- "what's on my plate", "my tasks", "show tasks"
- "task status", "update status"
- "mark as complete", "mark done"
- "task comments"

## First-Time Setup

API key is configured in `.env` as `CLICKUP_API_KEY`.

To get your API key:
1. Go to ClickUp Settings > Apps
2. Click "Generate" under API Token
3. Copy the token (starts with `pk_`)
4. Add to `.env`: `CLICKUP_API_KEY=pk_your_token_here`

## Hierarchy Overview

```
Workspace (Team)
└── Space (e.g., "Client Work", "Internal")
    ├── Folder (optional grouping)
    │   └── List (contains tasks)
    └── List (folderless - directly in space)
```

## Module Reference

- [LIST.md](modules/LIST.md) - Hierarchy browsing
- [TASKS.md](modules/TASKS.md) - Task operations
- [STATUS.md](modules/STATUS.md) - Status updates
- [COMMENTS.md](modules/COMMENTS.md) - Reading comments
