---
name: set-up-a-recurring-task
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Set up a recurring task so repeated operational work is created or reminded on a predictable schedule.

## Preconditions

- You can create or edit tasks in the tracker.
- The task owner, recurrence interval, due timing, and completion criteria are known.
- The tracker supports recurrence or there is an agreed manual workaround.

## Steps

1. **Open task creation.** [BRANCH: Jira | Asana | Linear | generic] create a task, issue, cycle item, or recurring template depending on the tracker. → *Expect:* a task form is visible.
2. **Define the task.** Add a clear title, description, owner, checklist, and acceptance criteria. → *Expect:* each occurrence will be understandable.
3. **Set the first due date.** Choose when the first occurrence should be completed. → *Expect:* the first deadline appears on the task.
4. **Configure recurrence.** Set the repeat interval, weekdays, monthly rule, or custom schedule. → *Expect:* the task shows a recurrence rule or automation.
5. **Choose completion behavior.** Confirm whether the next occurrence appears after completion, on a fixed schedule, or as separate future tasks. → *Expect:* future task behavior is predictable.
6. **Save and test visibility.** Save the task and check the calendar, board, or upcoming view. → *Expect:* the recurring task or next instance is visible.

## Decision points

- If the tracker does not support recurrence → create a template and calendar reminder to recreate it.
- If the schedule follows business days only → avoid calendar rules that fall on weekends or holidays unless acceptable.
- If ownership rotates → document the rotation instead of assigning all instances to one person.

## Failure modes & recovery

- **F1 Recurrence missing:** detect no repeat rule after saving → recover by reopening the task and enabling recurrence or automation.
- **F2 Wrong schedule:** detect future dates fall on the wrong day → recover by editing the recurrence rule before more instances are created.
- **F3 Duplicate recurring tasks:** detect multiple reminders for the same work → recover by disabling duplicates and keeping one source of truth.

## Verification

The task shows the correct owner, due date, recurrence rule, and expected next occurrence or upcoming reminder.

## Variations

- [BRANCH: Jira | Asana | Linear | generic] Asana has native recurring tasks; Jira often needs automation rules; Linear may need cycles, templates, or integrations; generic tools may use repeat settings or calendar reminders.

## Safety & privacy

Low risk. Recurring tasks can generate noise or duplicate work, so keep one clear owner and recurrence source.
