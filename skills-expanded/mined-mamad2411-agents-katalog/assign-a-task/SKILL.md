---
name: assign-a-task
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 3min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Assign an existing task to the person responsible for moving it forward.

## Preconditions

- You can edit the task.
- The intended owner is known and has access to the project.
- The task has enough context for the assignee to understand the work.

## Steps

1. **Open the task.** Go to the task, issue, or card that needs an owner. → *Expect:* the task detail view is visible.
2. **Check the task context.** Confirm the title, description, acceptance criteria, and attachments are sufficient. → *Expect:* the assignee will not need basic context before starting.
3. **Set the assignee.** [BRANCH: Jira | Asana | Linear | generic] use Assignee in Jira or Linear, Assignee in Asana tasks, or Owner/Assigned to in a generic tracker. → *Expect:* the intended person's name appears as the assignee.
4. **Set timing if needed.** Add or confirm the due date, sprint, milestone, or priority. → *Expect:* the owner can see when the work is expected.
5. **Notify the assignee.** Add a short comment naming the assignment and any immediate next action. → *Expect:* the assignee receives a visible notification.

## Decision points

- If the person lacks access → add them to the project before assigning.
- If ownership is unclear → assign to the team lead only as a temporary owner and request clarification.
- If the task needs multiple contributors → assign one accountable owner and mention contributors in the description.

## Failure modes & recovery

- **F1 Assignee not found:** detect the person missing from the picker → recover by checking spelling, inviting them, or assigning to the correct team queue.
- **F2 Task lacks context:** detect missing description or acceptance criteria → recover by adding context before or immediately after assignment.
- **F3 Duplicate ownership:** detect multiple people assuming they own it → recover by naming one owner and watchers separately.

## Verification

The task detail view shows one accountable assignee, and the activity log or comment stream records the assignment.

## Variations

- Some teams assign to queues first, then individuals during triage.
- In support-linked work, assign the engineering task owner separately from the ticket owner.

## Safety & privacy

Low risk. Do not assign work containing confidential customer or personnel details to someone without a need to know.
