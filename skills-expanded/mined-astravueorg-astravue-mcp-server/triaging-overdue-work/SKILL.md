---
name: triaging-overdue-work
description: Reviews overdue and at-risk tasks in Astravue, assesses why each is slipping, and proposes reschedule, reassign, deprioritize, or close actions before applying them. Use when the user asks what's overdue, behind schedule, slipping, or at risk, wants to catch up on a project, or clean up late work.
---

# Triaging Overdue Work

Read first, decide, then act. The goal is to turn a pile of late tasks into a short list of concrete decisions the user signs off on — not to silently mutate the board.

## Workflow

1. **Pull the overdue picture**

   - `astravue_list_overdue_tasks` — the late tasks with how far past due
   - `astravue_get_task_counts` — overall status distribution for context

   Confirm the project scope first if it isn't clear (`astravue_list_projects`).

2. **Assess each overdue task**

   For each, work out *why* it's late and what should happen:
   - Is it **blocked**? Check `astravue_list_dependencies` — a blocked task can't just be rescheduled; the blocker must move first.
   - Is it **still relevant**? Stale tasks may be closeable.
   - Is the **owner overloaded**? Group by assignee to spot pile-ups.
   - Is it **genuinely just late**? Then it needs a realistic new due date.

   Categorize each into: reschedule, reassign, deprioritize, or close.

3. **Propose a triage plan and confirm**

   Present the tasks grouped by recommended action, each with a one-line reason. Ask the user to approve, adjust, or drop items. Do not change any task before approval — rescheduling and reassigning are visible to the whole team.

4. **Apply after approval**

   - `astravue_bulk_update_tasks` — apply due-date, status, priority, or assignee changes in one pass
   - `astravue_mark_notification_read` / notification tools — only if the user wants to clear related noise

   Report what changed, and note any blocked tasks that still need their blocker resolved.

## Important

- Read and propose before mutating — these changes are team-visible.
- A blocked task's blocker must move first; don't just push the blocked task's date.
- Don't auto-close stale tasks — surface them and let the user decide.
- Give every proposed action a concrete reason, not just "overdue".
