---
name: set-a-task-due-date
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 2min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Set a due date on a task so the owner and stakeholders know when the work is expected.

## Preconditions

- You can edit the task.
- The target date is known or approved.
- The task owner and timezone assumptions are clear if time of day matters.

## Steps

1. **Open the task.** Go to the relevant task, issue, or card. → *Expect:* the task detail view is visible.
2. **Find the date field.** [BRANCH: Jira | Asana | Linear | generic] use Due date, Target date, Cycle date, or a custom date field depending on the tracker. → *Expect:* a calendar picker or date input is visible.
3. **Select the due date.** Enter the approved date and time if the tool supports time. → *Expect:* the chosen date appears on the task.
4. **Check related schedule fields.** Confirm sprint, milestone, dependency, or reminder fields do not contradict the due date. → *Expect:* scheduling fields are consistent.
5. **Save and comment if needed.** Save the task and add a short note when the date changed materially. → *Expect:* the task activity shows the updated due date.

## Decision points

- If the due date is a customer commitment → confirm it with the accountable owner before setting it.
- If only a target week is known → use the team's convention for approximate dates or leave a planning note.
- If the date conflicts with dependencies → flag the conflict rather than silently setting an unrealistic date.

## Failure modes & recovery

- **F1 Wrong date format:** detect the tool interprets day and month incorrectly → recover by using the calendar picker or ISO-style date.
- **F2 Date not saved:** detect the field reverts after navigation → recover by saving again and checking edit permission.
- **F3 Conflicting schedule:** detect milestone or sprint mismatch → recover by updating the related schedule or noting the exception.

## Verification

The task displays the intended due date in its detail view and activity history.

## Variations

- [BRANCH: Jira | Asana | Linear | generic] Jira may use Due date or custom fields; Asana has due dates and date ranges; Linear often uses cycle, project target date, or custom fields; generic tools vary by workspace setup.

## Safety & privacy

Low risk. Due dates can imply commitments, so avoid setting dates that have not been agreed for customer-facing work.
