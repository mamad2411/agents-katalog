---
name: tag-and-route-a-ticket
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 5min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Tag and route a support ticket so it reaches the correct queue and can be found in reports.

## Preconditions

- You can edit the support ticket.
- The support team's tagging and routing rules are available.
- The ticket content has enough information to identify topic and destination.

## Steps

1. **Open the ticket.** [BRANCH: Zendesk | generic] open the Zendesk ticket or generic helpdesk case. → *Expect:* ticket content and metadata fields are visible.
2. **Identify the issue type.** Read the customer request and determine product area, problem type, urgency, and language or region if relevant. → *Expect:* the routing target is clear.
3. **Apply required tags.** Add approved tags for product, issue type, plan, region, or campaign. → *Expect:* tags appear on the ticket.
4. **Set routing fields.** Choose the group, queue, category, form, or assignment rule target. → *Expect:* the ticket points to the intended support path.
5. **Add an internal note if helpful.** Summarize why the ticket was routed there. → *Expect:* the receiving team can see the routing reason.
6. **Save or submit the update.** Apply changes to the ticket. → *Expect:* the ticket remains in or moves to the expected queue.

## Decision points

- If the issue matches multiple queues → route to the team owning the next action and tag secondary areas.
- If required information is missing → ask the customer or leave it in triage with a missing-info tag.
- If routing rules conflict → follow the escalation policy or ask the queue owner.

## Failure modes & recovery

- **F1 Invalid tag:** detect tag autocomplete does not recognize the value → recover by using the approved tag list.
- **F2 Wrong queue:** detect the receiving queue rejects or reassigns the ticket → recover by updating tags and route based on queue rules.
- **F3 Automation overrides route:** detect the ticket moves after saving → recover by checking triggers or required fields and correcting the metadata.

## Verification

The ticket displays the approved tags, routing fields, and expected queue or group after saving.

## Variations

- [BRANCH: Zendesk | generic] Zendesk uses tags, groups, forms, and triggers; generic helpdesks may use labels, categories, inboxes, teams, or assignment rules.

## Safety & privacy

Low risk. Tags can expose sensitive topics in reports, so use approved labels and avoid free-text personal details.
