---
name: agkan
description: Use when managing tasks with the agkan CLI tool - creating, listing, updating tasks, managing tags, blocking relationships, or tracking project progress with the kanban board.
---

# agkan

## Overview

`agkan` is an SQLite-based CLI task management tool. It is optimized for collaboration with AI agents.

**7 Statuses:** `icebox` → `backlog` → `ready` → `in_progress` → `review` → `done` → `closed`

---

## Quick Reference

### Agent Guide

```bash
# Display a comprehensive guide for AI agents (overview, commands, workflows)
agkan agent-guide
```

### Task Operations

```bash
# Create task
agkan task add "Title" "Body"
agkan task add "Title" --status ready --author "agent"
agkan task add "Subtask" --parent 1
agkan task add "Title" --file ./spec.md  # Read body from file
agkan task add "Title" --blocked-by 1,2  # Set tasks that block this task
agkan task add "Title" --blocks 3,4      # Set tasks that this task blocks
agkan task add "Title" --assignees "alice,bob"  # Set task assignees (comma-separated)

# List tasks
agkan task list                    # All tasks
agkan task list --status in_progress
agkan task list --tree             # Hierarchical view
agkan task list --root-only        # Root tasks only
agkan task list --tag 1,2          # Filter by tags
agkan task list --dep-tree         # Dependency (blocking) tree view
agkan task list --sort title       # Sort by field (id / title / status / created_at / updated_at), default: created_at
agkan task list --order asc        # Sort order (asc / desc), default: desc
agkan task list --assignees "alice,bob"  # Filter by assignees (comma-separated)
agkan task list --all              # Include all statuses (including done and closed)
agkan task list --priority high,critical  # Filter by priority
agkan task list --sort priority           # Sort by priority

# Get details
agkan task get <id>

# Search
agkan task find "keyword"
agkan task find "keyword" --all  # Include done/closed
agkan task find "keyword" --status todo,in_progress   # Filter by status

# Update (positional argument form - backward compatible)
agkan task update <id> status in_progress

# Update (named option form - v1.6.0+)
agkan task update <id> --status in_progress
agkan task update <id> --title "New Title"
agkan task update <id> --body "New body text"
agkan task update <id> --author "agent"
agkan task update <id> --assignees "alice,bob"
agkan task update <id> --file ./spec.md  # Read body from file
agkan task update <id> --status done --title "Updated Title"  # Multiple options

# Count
agkan task count
agkan task count --status ready --quiet  # Output numbers only

# Update parent-child relationship
agkan task update-parent <id> <parent_id>
agkan task update-parent <id> null  # Remove parent

# Copy task
agkan task copy <id>               # タスクをコピーしてbacklogステータスで作成
agkan task copy <id> -s ready      # ステータスを指定してコピー
agkan task copy <id> --no-tags     # タグをコピーしない
agkan task copy <id> --json        # JSON形式で出力

# Delete task
agkan task delete <id>

# Purge old done/closed tasks
agkan task purge                        # Delete done/closed tasks older than 3 days ago (default)
agkan task purge --before 2026-01-01    # Purge tasks last updated before the given date (ISO 8601)
agkan task purge --status done          # Target specific statuses (default: done,closed)
agkan task purge --dry-run              # Preview tasks that would be purged without deleting
agkan task purge --json                 # Output in JSON format
```

### Blocking Relationships

```bash
# task1 blocks task2 (task2 cannot be started until task1 is complete)
agkan task block add <blocker-id> <blocked-id>
agkan task block remove <blocker-id> <blocked-id>
agkan task block list <id>
```

### Comment Operations

```bash
# Add a comment to a task
agkan task comment add <task-id> <content>
agkan task comment add <task-id> <content> --author "agent"

# List all comments for a task
agkan task comment list <task-id>

# Delete a comment by ID
agkan task comment delete <comment-id>
```

### Tag Operations

```bash
# Tag management
agkan tag add "frontend"
agkan tag list
agkan tag delete <tag-id-or-name>
agkan tag rename <id-or-name> <new-name>

# Tag tasks
agkan tag attach <task-id> <tag-id-or-name>
agkan tag detach <task-id> <tag-id-or-name>
agkan tag show <task-id>
```

### Export / Import Operations

```bash
# Export all tasks to JSON (output to stdout)
agkan export

# Export to file
agkan export > backup.json

# Import tasks from a JSON export file
agkan import <file>
agkan import backup.json
```

**Export behavior:**
- Outputs all tasks in JSON format to stdout
- Redirect to a file for backup or migration

**Import behavior:**
- Imports tasks from a JSON file created by `agkan export`
- Preserves timestamps from the exported data
- Automatically creates any tags that are missing in the target project
- ID mapping is handled internally (new IDs are assigned in the target DB)

**Use cases:**
- Task backup before destructive operations
- Migrating tasks to another project
- CI/CD pipeline task management

### Process Operations

```bash
agkan ps                   # Show list of running Claude processes
agkan ps --port <number>   # Specify port
agkan ps --json            # Output in JSON format
```

### Board Operations

```bash
agkan board start [--port <number>] [--title <title>]   # Start the board
agkan board stop                                         # Stop the board
agkan board restart [--port <number>]                   # Restart the board
agkan board status [--port <number>]                    # Check board status
```

### Metadata Operations

```bash
# Set metadata
agkan task meta set <task-id> <key> <value>

# Get metadata
agkan task meta get <task-id> <key>

# List metadata
agkan task meta list <task-id>

# Delete metadata
agkan task meta delete <task-id> <key>
```

#### Priority (priority)

Task priority is managed with the `priority` key:

```bash
agkan task meta set <task-id> priority <value>
```

| Value | Meaning |
|-----|------|
| `critical` | Requires immediate attention. Blocking issue |
| `high` | Should be prioritized |
| `medium` | Normal priority (default) |
| `low` | Work on if there is time |

**When to set priority:** Priority is set during the planning phase (`agkan-planning-subtask`), at the same time the task is moved from `backlog` to `ready`. This is the responsibility of the planning skill. Skills that select tasks for execution (e.g., `agkan-run`) read this value to determine which task to work on next.

---

## Tag Priority

When selecting or tagging tasks, use the following priority order:

| Priority | Tag Name |
|----------|----------|
| 1 | bug |
| 2 | security |
| 3 | improvement |
| 4 | test |
| 5 | performance |
| 6 | refactor |
| 7 | docs |

This is the canonical definition. All skills refer to this table.

---

## JSON Output

Use the `--json` flag when machine processing is needed:

```bash
agkan task list --json
agkan task get 1 --json
agkan task count --json
agkan tag list --json

# Combine with jq
agkan task list --status ready --json | jq '.tasks[].id'
```

### JSON Output Schema

#### `agkan task list --json`

```json
{
  "totalCount": 10,
  "filters": {
    "status": "ready | null",
    "author": "string | null",
    "tagIds": [1, 2],
    "rootOnly": false
  },
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "body": "Body | null",
      "author": "string | null",
      "status": "icebox | backlog | ready | in_progress | review | done | closed",
      "parent_id": "number | null",
      "created_at": "2026-01-01T00:00:00.000Z",
      "updated_at": "2026-01-01T00:00:00.000Z",
      "parent": "object | null",
      "tags": [{ "id": 1, "name": "bug" }],
      "metadata": [{ "key": "priority", "value": "high" }]
    }
  ]
}
```

#### `agkan task get <id> --json`

```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Task Title",
    "body": "Body | null",
    "author": "string | null",
    "status": "backlog | ready | in_progress | review | done | closed",
    "parent_id": "number | null",
    "created_at": "2026-01-01T00:00:00.000Z",
    "updated_at": "2026-01-01T00:00:00.000Z"
  },
  "parent": "object | null",
  "children": [],
  "blockedBy": [{ "id": 2, "title": "..." }],
  "blocking": [{ "id": 3, "title": "..." }],
  "tags": [{ "id": 1, "name": "bug" }],
  "attachments": []
}
```

#### `agkan task count --json`

```json
{
  "counts": {
    "icebox": 0,
    "backlog": 0,
    "ready": 2,
    "in_progress": 1,
    "review": 0,
    "done": 8,
    "closed": 5
  },
  "total": 16
}
```

#### `agkan task find <keyword> --json`

```json
{
  "keyword": "Search keyword",
  "excludeDoneClosed": true,
  "totalCount": 3,
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "body": "Body | null",
      "author": "string | null",
      "status": "ready",
      "parent_id": "number | null",
      "created_at": "2026-01-01T00:00:00.000Z",
      "updated_at": "2026-01-01T00:00:00.000Z",
      "parent": "object | null",
      "tags": [],
      "metadata": []
    }
  ]
}
```

#### `agkan task block list <id> --json`

```json
{
  "task": {
    "id": 1,
    "title": "Task Title",
    "status": "ready"
  },
  "blockedBy": [{ "id": 2, "title": "...", "status": "in_progress" }],
  "blocking": [{ "id": 3, "title": "...", "status": "ready" }]
}
```

#### `agkan task meta list <id> --json`

```json
{
  "success": true,
  "data": [
    { "key": "priority", "value": "high" }
  ]
}
```

#### `agkan tag list --json`

```json
{
  "totalCount": 3,
  "tags": [
    {
      "id": 1,
      "name": "bug",
      "created_at": "2026-01-01T00:00:00.000Z",
      "taskCount": 2
    }
  ]
}
```

---

## Typical Workflows

### Icebox Review (agkan-icebox)

Icebox holds ideas and candidates that are not yet ready for planning. Review them periodically to decide whether to promote or close each one.

```bash
# Review icebox tasks
agkan task list --status icebox

# Promote to backlog when requirements become clear
agkan task update <id> status backlog

# Close if no longer needed
agkan task update <id> status closed
```

**Icebox → Backlog conditions:**
- Requirements or background are now clear enough to plan
- External blockers have been resolved
- Circumstances have changed and the task is now relevant

**Icebox → Closed conditions:**
- The need no longer exists
- A duplicate already exists in a later stage
- Superseded by another approach

### Receiving Tasks as an Agent

```bash
# Check assigned tasks
agkan task list --status ready
agkan task get <id>

# Start work
agkan task update <id> status in_progress

# Complete
agkan task update <id> status done
```

### Structuring Tasks

```bash
# Create parent task
agkan task add "Feature Implementation" --status ready

# Add subtasks
agkan task add "Design" --parent 1 --status ready
agkan task add "Implementation" --parent 1 --status backlog
agkan task add "Testing" --parent 1 --status backlog

# Set dependencies (Design → Implementation → Testing)
agkan task block add 2 3
agkan task block add 3 4

# View overall structure
agkan task list --tree
```

---

## Body Conventions

Skills that create branches and PRs write structured labels into the task body. These labels are used by subsequent skill executions to resume work on the correct branch and PR instead of starting fresh.

### Format

```
Branch: <branch-name>
PR: <URL>
```

### Rules

- **Branch label** is written by `agkan-subtask` after the branch is created (Step 3).
- **PR label** is written by `agkan-subtask` after the PR is opened (Step 7).
- Both labels are appended to the existing task body, separated by a blank line.
- Skills that start work on a task **must** parse these labels from the task body before creating a new branch or PR.
  - If a `Branch:` label is present → check out the existing branch and continue work on it.
  - If a `PR:` label is present → push to that branch to update the existing PR instead of opening a new one.
  - If neither label is present → proceed with the default flow (create a new branch, open a new PR).

---

## Configuration

Place `.agkan.yml` in the project root to customize the DB path:

```yaml
path: ./.agkan/data.db
```

Or use environment variable: `AGENT_KANBAN_DB_PATH=/custom/path/data.db`