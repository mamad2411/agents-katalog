---
name: set-a-deal-reminder
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

Create a reminder on a deal so the responsible person follows up before momentum is lost.

## Preconditions

- CRM access to the deal.
- A clear reminder reason, owner, and due date.
- Knowledge of the next sales milestone or risk.

## Steps

1. **Open the deal.** Search for the deal by name, account, or owner. → *Expect:* the deal record and activity controls are visible.
2. **Choose reminder timing.** Pick a due date based on buyer commitment, close date, or internal review cadence. → *Expect:* the reminder timing supports the next sales action.
3. **Create the task.** [BRANCH: Salesforce | HubSpot | generic] create a Task in Salesforce; create a Task in HubSpot; in another CRM, add the equivalent reminder or activity. → *Expect:* a task editor opens.
4. **Enter task details.** Add owner, due date, subject, priority, and a short instruction. → *Expect:* the task clearly states what to do.
5. **Associate the task to the deal.** Link the task to the opportunity, company, contact, or related account as supported. → *Expect:* the reminder appears on the deal timeline.
6. **Save the reminder.** Save and confirm it appears in the owner's task list. → *Expect:* the owner can see the pending task.

## Decision points

- If the buyer agreed to a meeting → create a calendar event instead of a simple reminder.
- If the deal is stale with no next step → set a reminder to inspect or close out the deal.
- If the reminder is for another rep → include enough context for them to act.

## Failure modes & recovery

- **F1 Reminder not linked:** detect the task only appears in a personal task list → associate it with the deal record.
- **F2 Due date too late:** detect the reminder after the close date or buyer deadline → move it earlier.
- **F3 Wrong owner:** detect the task assigned to a former owner → reassign to the current deal owner.

## Verification

The deal timeline and owner's task list show a pending reminder with due date, owner, subject, and action detail.

## Variations

- Renewal reminder: set due dates relative to contract end date.
- Proposal reminder: schedule before quote expiration.
- Manager review: assign the reminder to the sales manager with a review note.

## Safety & privacy

Low risk. Keep reminder text business-focused and avoid placing sensitive customer information in task subjects that may appear in notifications.
