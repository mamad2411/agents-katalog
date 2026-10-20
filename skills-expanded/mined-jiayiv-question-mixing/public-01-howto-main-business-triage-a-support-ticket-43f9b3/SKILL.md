---
name: triage-a-support-ticket
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

Triage a support ticket so it has the right urgency, category, owner, and next action.

## Preconditions

- You can view and update the support ticket.
- The helpdesk has queues, tags, priorities, or assignment rules.
- Customer account context is available if needed.

## Steps

1. **Open the ticket.** [BRANCH: Zendesk | generic] open the ticket in Zendesk or the helpdesk queue in a generic support tool. → *Expect:* the customer message, status, and metadata are visible.
2. **Read the latest customer request.** Identify the problem, affected product, customer impact, and requested outcome. → *Expect:* the ticket can be summarized in one sentence.
3. **Check account and history.** Review plan level, open related tickets, recent incidents, and prior replies. → *Expect:* repeated or high-impact issues are visible.
4. **Set priority.** Choose the urgency and impact level according to the support policy. → *Expect:* the ticket priority reflects business impact.
5. **Categorize the issue.** Add the product area, issue type, and relevant tags. → *Expect:* routing and reporting fields are complete.
6. **Assign the owner or queue.** Send the ticket to the right agent, team, or specialist queue. → *Expect:* the ticket has a responsible next handler.
7. **Record the next action.** Add an internal note with the summary, evidence, and next step. → *Expect:* another agent can continue without rereading everything.

## Decision points

- If the customer reports outage, security, or data loss → escalate according to the incident process.
- If the ticket lacks reproduction details → request the missing information before routing deeply.
- If multiple customers report the same symptom → link tickets or tag them to the known incident.

## Failure modes & recovery

- **F1 Misclassified priority:** detect mismatch between policy and assigned priority → recover by correcting the priority and noting the reason.
- **F2 Missing customer context:** detect uncertainty about plan, region, or affected account → recover by checking CRM or asking for account identifiers.
- **F3 Routed to wrong queue:** detect reassignment or queue rejection → recover by reading the queue rules and routing to the correct team.

## Verification

The ticket has a priority, category or tags, owner or queue, internal triage note, and a clear next action.

## Variations

- [BRANCH: Zendesk | generic] Zendesk commonly uses forms, tags, groups, and internal notes; generic helpdesks may use categories, queues, and custom fields.

## Safety & privacy

Customer messages may contain personal data, logs, or secrets. Do not paste sensitive content into broad channels or unrelated tracker issues.
