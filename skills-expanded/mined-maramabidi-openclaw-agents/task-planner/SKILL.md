---
name: "Task Planner"
description: "Manage local tasks, priorities, and deadlines with a private bash and Python workflow. Use when organizing daily work, planning projects, or tracking completion."
version: "3.0.5"
author: "BytesAgain"
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: ["productivity", "task-management", "scheduler", "todo-list", "efficiency"]
---

# Task Planner

Your local task manager. All data stays on the machine.

## Quick Start

Use it for:

- adding tasks with priority and optional due dates
- listing pending, done, or all tasks
- marking tasks complete by ID

## User Phrases

Treat these as task-planner requests:

- `lister mes taches`
- `afficher mes taches`
- `mes taches`
- `task list`
- `show tasks`
- `list tasks`
- `add a task`
- `ajoute une tache`
- `nouvelle tache`
- `marquer comme terminee`
- `complete task`

## How To List Tasks

Use the list command when the user wants to see tasks.

The exact script lives at:

```bash
C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/scripts/script.sh
```

Compatibility entrypoints also exist:

- `C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/task`
- `C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/task.py`
- `C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/scripts/list-tasks.sh`

Default view:

```bash
bash C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/scripts/script.sh list
```

Pending tasks only:

```bash
bash C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/scripts/script.sh list --status pending
```

Done tasks only:

```bash
bash C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/scripts/script.sh list --status done
```

All tasks:

```bash
bash C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/scripts/script.sh list --status all
```

## Requirements

- bash
- python3

## Safety & Privacy

- Data is stored locally in `~/.task-planner/tasks.json`
- No cloud sync
- No network calls

## Commands

### add

Add a new task with optional priority and due date.

```bash
bash C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/scripts/script.sh add "Finish report" --priority high --due 2026-12-31
```

### list

Display tasks. Default is pending tasks.

```bash
bash C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/scripts/script.sh list --status pending
```

### done

Complete a task by ID.

```bash
bash C:/Users/hp/.openclaw/workspace-preparation/skills/task-planner-3.0.5/scripts/script.sh done 1
```

## Notes

- Data file: `~/.task-planner/tasks.json`
- If the task list is empty, say so clearly instead of guessing.
- If the user only says "list my tasks", show pending tasks by default unless they ask for done or all.
