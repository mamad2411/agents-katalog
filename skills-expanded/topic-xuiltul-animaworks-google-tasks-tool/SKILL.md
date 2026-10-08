---
name: google-tasks-tool
description: >-
  Google Tasks integration tool. Performs task list and task listing, addition, and updates using OAuth2.
  Use when: Use when: you need to fetch the TODO list, add tasks, update completion, or switch task lists.
tags: [tasks, google, todo, external]
---


# Google Tasks Tool

An external tool that operates on task lists and tasks via the Google Tasks API.

## How to Invoke

**Bash**: Run with `animaworks-tool google_tasks <サブコマンド> [引数]`

## List of Actions

### list_tasklists — List task lists
```bash
animaworks-tool google_tasks tasklists [-n 50]
```

| Parameter | Type | Default | Description |
|-----------|-----|---------|------|
| max_results | integer | 50 | Maximum number of results to retrieve |

### list_tasks — List tasks
```bash
animaworks-tool google_tasks list <タスクリストID> [-n 50] [--no-completed]
```

| Parameter | Type | Required | Description |
|-----------|-----|------|------|
| tasklist_id | string | Yes | Task list ID |
| max_results | integer | 50 | Maximum number of results to retrieve |
| show_completed | boolean | true | Whether to include completed tasks |

### insert_task — Add a task
```bash
animaworks-tool google_tasks add <タスクリストID> "タスク名" [--notes メモ] [--due 日時]
```

| Parameter | Type | Required | Description |
|-----------|-----|------|------|
| tasklist_id | string | Yes | Task list ID |
| title | string | Yes | Task name |
| notes | string | No | Notes |
| due | string | No | Deadline (RFC 3339) |

### insert_tasklist — Create a task list
```bash
animaworks-tool google_tasks new-list "リスト名"
```

| Parameter | Type | Required | Description |
|-----------|-----|------|------|
| title | string | Yes | List name |

### update_task — Update a task
Updates the title, notes, deadline, and completion status of the specified task (updates only the specified fields).

```bash
animaworks-tool google_tasks update <タスクリストID> <タスクID> [--title タイトル] [--notes メモ] [--due 日時] [--status completed|needsAction]
```

| Parameter | Type | Required | Description |
|-----------|-----|------|------|
| tasklist_id | string | Yes | Task list ID |
| task_id | string | Yes | Task ID |
| title | string | No | New title |
| notes | string | No | Notes |
| due | string | No | Deadline (RFC 3339) |
| status | string | No | `needsAction` (incomplete) or `completed` (completed). Specify at least one of title/notes/due/status. |

### update_tasklist — Update the task list name
```bash
animaworks-tool google_tasks update-list <タスクリストID> "新しいリスト名"
```

| Parameter | Type | Required | Description |
|-----------|-----|------|------|
| tasklist_id | string | Yes | Task list ID |
| title | string | Yes | New list name |

## Notes

- OAuth2 authentication flow is required on first use
- Place credentials.json in `~/.animaworks/credentials/google_tasks/` (you can copy the same OAuth client as Gmail/Calendar)
