---
name: todoist-operations
description: Complete Todoist integration for natural-language task management, daily planning workflows, task breakdowns, reviews, and productivity coaching.
when_to_use: |
  Use this skill when the user:
  - Mentions Todoist or their task list
  - Asks to see tasks, plan their day, or review progress
  - Requests task management operations (add, update, complete, delete)
  - Wants daily planning, morning review, evening review, or weekly review
  - Needs productivity coaching or help organizing work
  - Asks to "review" tasks before working on them or wants feedback on task quality
  - Has a task that's too big to execute directly and wants to "break it down"
  - Asks "plan this out for me" or "I don't know where to start"
---

# Todoist Operations Skill

Complete personal productivity manager integrating Todoist for natural-language task management, strategic planning, task readiness review, complex task breakdowns, and productivity coaching.

## Prerequisites

- `TODOIST_TOKEN` is injected natively by the MCP environment. You do not need to read it or parse it yourself.
- Use the `todoist_client` tool to interact with the API, instead of executing Python scripts directly.

## Using the Tool

All operations use the `todoist_client` tool which expects JSON parameters mapping to the underlying command-line interface logic.

**General Pattern:**
Call the `todoist_client` tool with the `args` array mapping to the resource and action, plus any options.

## Section A: Core Task Management

### List All Tasks
```json
{
  "args": ["tasks", "list", "--project-id", "12345"]
}
```

### Filter Tasks with Queries
```json
{
  "args": ["tasks", "filter", "--query", "today & p1"]
}
```
**See:** `references/filter-query-syntax.md` for complete query language.

### Add Task
```json
{
  "args": [
    "tasks", "add", 
    "--content", "Task title", 
    "--description", "Additional details",
    "--due-string", "tomorrow at 3pm",
    "--priority", "4"
  ]
}
```

### Update/Complete/Delete Task
```json
{
  "args": ["tasks", "update", "--task-id", "12345", "--due-string", "friday"]
}
{
  "args": ["tasks", "complete", "--task-id", "12345"]
}
{
  "args": ["tasks", "delete", "--task-id", "12345"]
}
```
*Always confirm before deleting unless explicitly requested.*

## Section B: Project & Organization

Use similar `args` patterns for `projects`, `sections`, `labels`, and `comments` (e.g. `["projects", "list"]`).

## Section C: Daily Planning

### Morning Review Workflow
1. Fetch overview: `["overview"]`
2. Present overview with priority grouping.
3. Coach for focus selection.
4. Generate time-blocked schedule.

### Evening Review Workflow
1. Fetch daily summary: `["daily-summary"]`
2. Celebrate wins.
3. Review incomplete tasks.
4. Prep for tomorrow.

**See:** `references/productivity-workflows.md` for complete templates.

## Section D: Task Breakdown (plan-task)

**When to trigger:**
- Task duration >60 minutes, or task deferred 2+ times.

**Process:**
1. Clarify outcome.
2. Identify subtasks (each <30 mins, starts with action verb).
3. Create parent task (if needed) and subtasks:
```json
{
  "args": ["tasks", "add", "--content", "Subtask 1", "--parent-id", "12345", "--duration", "30", "--duration-unit", "minute"]
}
```

## Section E: Task Readiness Review (task-review)

**When to trigger:**
- User asks to "review" tasks before working on them.

**Process:**
1. Fetch the task.
2. Score across 5 dimensions: Clarity, Actionability, Scope, Context, Outcome.
3. Present scorecard and offer improvements.

**See:** `references/readiness-rubric.md` and `references/task-templates.md` for scoring and templates.
