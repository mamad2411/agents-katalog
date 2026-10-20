---
name: auto-assign-tasks
description: "Pick the right digital employee for a task and assign it to them via the planning tools. Especially relevant to SCRUM Masters, Product, and Engineering leadership roles."
---

# Auto Assign tasks across agents

This initiative has opted in to **Agent Auto Assign**. Leadership roles (SCRUM Master, Product Manager, Engineering Manager, Project Manager, Shadow Engineering Lead) can move planning tasks between the digital employees clocked in to this initiative.

## When to assign

Assign work when you, as a leadership role, are deliberately distributing scope. Examples:
- A sprint plan exists and tasks need to be picked up by specific   agents based on skill (front-end vs back-end vs research).
- A blocked task needs to be re-routed to a different agent who has   the right tools/skills.
- A task lives in the wrong room and needs to be moved to a digital   employee in the right room.

Do **not** assign when:
- The task is yours to do — just do it.
- The user explicitly asked you to do it. Re-assigning would be   unsafe surface drift.
- The target agent is not currently clocked in to the relevant room   (call `agent_directory_list` first to verify).

## The loop

### Step 1 — `agent_directory_list`

Call `agent_directory_list` to see the digital employees on this initiative. You can filter by `room`, `agent_template`, or a free substring `filter`. The response includes each agent's `id`, `name`, `room_name`, and `agent_template_name` so you can pick the right one.

When the opt-in is off the response includes a `hint` reminding you that downstream `planning_tasks_bulk_assign` calls targeting another digital employee will be rejected. Don't try to circumvent the gate — surface the constraint back to the user.

### Step 2 — `planning_tasks_bulk_assign`

Pass the chosen `digital_employee_id` (and `room_name` when it is different from yours) along with the list of `task_ids` you are reassigning. The planning facade owns the actual write — you only build the payload.

Keep the batch size reasonable (the initiative-level `maxAssignmentsPerBatch` defaults to 25). For larger reshuffles, split into multiple calls and post a brief assistant message after each batch so the user can follow along.

### Step 3 — notify (when enabled)

When the initiative has `autoAssign.notifyAssignee` enabled (default on), the planning facade will surface an internal note to the assignee on top of the assignment write. You don't have to do that yourself — but you SHOULD add a one-liner in your reply summarizing what was moved and why so the user has audit context.

## Anti-patterns

- ❌ Mass-reassigning everything to the agent that looks like the   best fit on paper. Honour current workload; ask before stacking.
- ❌ Using `planning_tasks_bulk_assign` to pull tasks AWAY from a   human user without their consent. Only reassign between agents.
- ❌ Skipping `agent_directory_list` and guessing a   `digital_employee_id`. Always look the directory up first.
