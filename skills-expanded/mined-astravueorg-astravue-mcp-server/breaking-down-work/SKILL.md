---
name: breaking-down-work
description: Decomposes a goal, feature, epic, or deliverable into a structured task tree (tasks, subtasks, checklists) with dependencies in Astravue. Use when the user wants to break down, decompose, or plan out work, turn an epic or feature into tasks, "split this into tasks", scope a deliverable, or build a work breakdown structure.
---

# Breaking Down Work

Turns a high-level goal into a complete, well-scoped task tree. The value is in the decomposition and sequencing — not in the tool calls — so spend effort on coverage and structure, then create in one confirmed pass.

## Workflow

1. **Understand the goal and scope**

   Clarify the deliverable and the target project. Use `astravue_list_projects` if the project is unclear. If the work hangs off an existing task, note its ID — the new tasks become subtasks of it.

2. **Decompose to full coverage**

   Break the goal into tasks, then subtasks, then checklist items where useful. Aim for the 100% rule: the children together fully cover the parent's scope with no overlap. A leaf is small enough when one person can finish it in a sitting and you can tell when it's done.

   - Tasks — the main units of deliverable work
   - Subtasks (`astravue_create_subtask`) — steps within a task
   - Checklist items (`astravue_create_checklist_item`) — acceptance criteria or fine-grained todos

3. **Sequence the work**

   Identify which tasks block others. Capture these as dependencies. Flag anything that can run in parallel so the plan doesn't serialize work that needn't be.

4. **Present the plan and confirm**

   Show the full tree (task → subtasks → checklist), proposed dependencies, and any estimates, as a structured outline. Ask the user to adjust or approve. Do not create anything before approval — decomposition is cheap to revise on paper and expensive to undo in the workspace.

5. **Create after approval**

   - `astravue_bulk_create_tasks` — create the top-level tasks in one call
   - `astravue_create_subtask` — add subtasks under each task
   - `astravue_create_checklist_item` — add checklist items
   - `astravue_add_dependency` — wire up the blocking relationships

   Report back what was created with IDs so the user can navigate to it.

## Important

- Decompose first, create once. The thinking is the deliverable; the writes are mechanical.
- Apply the 100% rule — if the children don't cover the parent, the breakdown is incomplete; if they overlap, it's redundant.
- Never create tasks before the user approves the plan.
- Only set estimates, assignees, or due dates the user actually provides — don't invent them.
