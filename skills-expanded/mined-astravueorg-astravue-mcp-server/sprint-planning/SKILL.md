---
name: sprint-planning
description: Plans sprints by analyzing project backlog, overdue tasks, and dependencies in Astravue. Use when planning a sprint, organizing upcoming work, asking "what should we work on next?", or reviewing the backlog.
---

# Sprint Planning

## Workflow

1. **Scope the project**

   Ask which project to plan for. Use `astravue_list_projects` if needed.

2. **Gather backlog state**

   - `astravue_list_project_tasks` — all tasks with status and priority
   - `astravue_list_overdue_tasks` — urgent carry-overs
   - `astravue_list_dependencies` — blocking relationships
   - `astravue_get_task_counts` — status distribution

3. **Prioritize**

   Rank tasks by:
   - Overdue tasks first
   - Tasks blocking other tasks second
   - High/Critical priority third
   - Approaching due dates fourth

4. **Present the sprint plan**

   Show a prioritized list with reasoning. Ask the user to confirm, adjust, or remove items before making changes.

5. **Apply changes**

   After confirmation, use `astravue_bulk_update_tasks` to update priorities or statuses. Never modify tasks without explicit approval.
