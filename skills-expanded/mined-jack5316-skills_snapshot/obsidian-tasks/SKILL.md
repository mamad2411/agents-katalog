---
name: obsidian-tasks
description: Advanced task management using Obsidian's native task system. List tasks, filter by status, manage priorities, add tasks to daily notes, and track completion rates. Use when asked about tasks, todos, task management, or to check what needs to be done.
---

# Obsidian Task Manager Skill (/obsidian-tasks)

Comprehensive task management for your Obsidian vault including filtering, priority tracking, tag analysis, daily note integration, and completion statistics.

## Quick Start

```bash
python3 _scripts/obsidian_task_manager.py
```

## Features

1. **Task Filtering** - Show todo, done, in-progress, or daily tasks
2. **Priority Tracking** - 🔴 P1 (high), 🟡 P2 (medium), 🟢 P3 (low)
3. **Tag Analysis** - Tasks organized by #tags
4. **Daily Integration** - Add tasks directly to daily notes
5. **Search** - Find tasks by keywords
6. **Statistics** - Completion rates and trends

## Options

- `--todo`: Show only pending tasks
- `--done`: Show only completed tasks
- `--daily`: Show tasks from daily notes
- `--priority`: Show high-priority tasks only
- `--search TEXT`: Search tasks containing text
- `--add TEXT`: Add task to daily note
- `--save`: Save report to Sources/Task Manager Report - YYYY-MM-DD.md

## Examples

```bash
# Full task report
python3 _scripts/obsidian_task_manager.py

# Show only todo tasks
python3 _scripts/obsidian_task_manager.py --todo

# Show completed tasks
python3 _scripts/obsidian_task_manager.py --done

# Show high-priority tasks
python3 _scripts/obsidian_task_manager.py --priority

# Search tasks
python3 _scripts/obsidian_task_manager.py --search "project"

# Add task to daily note
python3 _scripts/obsidian_task_manager.py --add "Finish the report"

# Save report
python3 _scripts/obsidian_task_manager.py --save
```

## Task Formatting

The task manager recognizes:

- **Status**: `- [ ]` todo, `- [x]` done, `- [/]` in-progress
- **Priority**: 🔴 or P1 (high), 🟡 or P2 (medium), 🟢 or P3 (low)
- **Tags**: #tagname anywhere in task content

## Output

- **Terminal**: Markdown report with overview, todo list (priority sorted), tag breakdown, and recent completions
- **Saved report**: `Sources/Task Manager Report - YYYY-MM-DD.md`
