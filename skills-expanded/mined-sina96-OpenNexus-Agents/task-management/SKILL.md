---
name: task-management
description: Task management CLI for tracking and managing feature subtasks with status, dependencies, and validation
version: 1.0.0
author: opencode
type: skill
category: development
tags:
  - tasks
  - management
  - tracking
  - dependencies
  - cli
---

# Task Management Skill

> Purpose: Track, manage, and validate feature implementations with atomic task breakdowns, dependency resolution, and progress monitoring.

## What I Do

I provide a command-line interface for managing task breakdowns created by the Task Manager subagent. I help you:

- Track progress - See status of all features and their subtasks
- Find next tasks - Show eligible tasks (dependencies satisfied)
- Identify blocked tasks - See what's blocked and why
- Manage completion - Mark subtasks as complete with summaries
- Validate integrity - Check JSON files and dependency trees

## How to Use Me

### Quick Start

```bash
# Show all task statuses
bash .opencode/skills/task-management/router.sh status

# Show next eligible tasks
bash .opencode/skills/task-management/router.sh next

# Show blocked tasks
bash .opencode/skills/task-management/router.sh blocked

# Mark a task complete
bash .opencode/skills/task-management/router.sh complete <feature> <seq> "summary"

# Validate all tasks
bash .opencode/skills/task-management/router.sh validate
```

### Command Reference

| Command | Description |
|---------|-------------|
| `status [feature]` | Show task status summary for all features or specific one |
| `next [feature]` | Show next eligible tasks (dependencies satisfied) |
| `parallel [feature]` | Show parallelizable tasks ready to run |
| `deps <feature> <seq>` | Show dependency tree for a specific subtask |
| `blocked [feature]` | Show blocked tasks and why |
| `complete <feature> <seq> "summary"` | Mark subtask complete with summary |
| `validate [feature]` | Validate JSON files and dependencies |
| `help` | Show help message |

## Examples

### Check Overall Progress

```bash
$ bash .opencode/skills/task-management/router.sh status

[my-feature] My Feature Implementation
  Status: active | Progress: 45% (5/11)
  Pending: 3 | In Progress: 2 | Completed: 5 | Blocked: 1
```

### Find What's Next

```bash
$ bash .opencode/skills/task-management/router.sh next

=== Ready Tasks (deps satisfied) ===

[my-feature]
  06 - Implement API endpoint [sequential]
  08 - Write unit tests [parallel]
```

### Mark Complete

```bash
$ bash .opencode/skills/task-management/router.sh complete my-feature 05 "Implemented authentication module"

Marked my-feature/05 as completed
  Summary: Implemented authentication module
  Progress: 6/11
```

### Check Dependencies

```bash
$ bash .opencode/skills/task-management/router.sh deps my-feature 07

=== Dependency Tree: my-feature/07 ===

07 - Write integration tests [pending]
  - 05 - Implement authentication module [completed]
  - 06 - Implement API endpoint [in_progress]
```

### Validate Everything

```bash
$ bash .opencode/skills/task-management/router.sh validate

=== Validation Results ===

[my-feature]
  All checks passed
```

## Architecture

```
.opencode/skills/task-management/
  SKILL.md                          # This file
  router.sh                         # CLI router (entry point)
  scripts/
    task-cli.ts                     # Task management CLI implementation
```

## Task File Structure

Tasks are stored in `.tmp/tasks/` at the project root:

```
.tmp/tasks/
  {feature-slug}/
    task.json                     # Feature-level metadata
    subtask_01.json               # Subtask definitions
    subtask_02.json
    ...
  completed/
    {feature-slug}/               # Completed tasks
```

### task.json Schema

```json
{
  "id": "my-feature",
  "name": "My Feature",
  "status": "active",
  "objective": "Implement X",
  "context_files": ["docs/spec.md"],
  "reference_files": ["src/existing.ts"],
  "exit_criteria": ["Tests pass", "Code reviewed"],
  "subtask_count": 5,
  "completed_count": 2,
  "created_at": "2026-01-11T10:00:00Z",
  "completed_at": null
}
```

### subtask_##.json Schema

```json
{
  "id": "my-feature-05",
  "seq": "05",
  "title": "Implement authentication",
  "status": "pending",
  "depends_on": ["03", "04"],
  "parallel": false,
  "suggested_agent": "opencoder",
  "context_files": ["docs/auth.md"],
  "reference_files": ["src/auth-old.ts"],
  "acceptance_criteria": ["Login works", "JWT tokens valid"],
  "deliverables": ["auth.ts", "auth.test.ts"],
  "started_at": null,
  "completed_at": null,
  "completion_summary": null
}
```

## Integration with Task Manager

The Task Manager subagent creates task files using this format.

It creates:
- `.tmp/tasks/{feature}/task.json` - Feature metadata
- `.tmp/tasks/{feature}/subtask_XX.json` - Individual subtasks

You can then use this skill to track and manage progress.

## Key Concepts

### 1. Dependency Resolution

Subtasks can depend on other subtasks. A task is ready only when all its dependencies are complete.

### 2. Parallel Execution

Set `parallel: true` to indicate a subtask can run alongside other parallel tasks with satisfied dependencies.

### 3. Status Tracking

- pending - Not started, waiting for dependencies
- in_progress - Currently being worked on
- completed - Finished with summary
- blocked - Explicitly blocked (not waiting for deps)

### 4. Exit Criteria

Each feature can define exit_criteria that must be met before marking the feature complete.

### 5. Validation Rules

The `validate` command performs checks on task files:

- task.json exists for each feature
- Subtask count matches actual subtask files
- Required fields are present
- Dependencies reference existing subtasks
- No circular dependencies
- Status values are valid

Run `validate` regularly to catch issues early.

## File Locations

- Skill source (this repo): `core/skills/task-management/SKILL.md`
- Installed skill docs: `.opencode/skills/`
