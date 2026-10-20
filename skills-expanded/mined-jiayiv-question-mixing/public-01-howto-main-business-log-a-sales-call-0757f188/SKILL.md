---
name: log-a-sales-call
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

Record a completed sales call in the CRM so the account history, next step, and forecast context stay current.

## Preconditions

- CRM access to the relevant lead, contact, account, or deal.
- The call date, participants, outcome, and agreed next step.
- Permission to record business call notes in the CRM.

## Steps

1. **Open the relevant record.** Find the lead, contact, account, or deal connected to the call. → *Expect:* the activity timeline for the right record is visible.
2. **Start a call log.** [BRANCH: Salesforce | HubSpot | generic] choose Log a Call in Salesforce; choose Log call in HubSpot; in another CRM, add a completed call activity. → *Expect:* a call activity editor opens.
3. **Enter call details.** Add date, time, call direction, participants, and disposition or outcome. → *Expect:* the activity describes when the call happened and what type it was.
4. **Summarize business substance.** Write concise notes covering pain, need, objection, decision process, and commitments. → *Expect:* another rep can understand the call without listening to it.
5. **Create the next step.** Add a follow-up task, meeting, email, or no-action reason. → *Expect:* the CRM shows what happens next.
6. **Save the activity.** Save the log and refresh the timeline if needed. → *Expect:* the completed call appears on the record timeline.

## Decision points

- If the call belongs to multiple records → log once and associate it to the relevant deal, account, and contacts if the CRM supports associations.
- If sensitive customer information was discussed → summarize only what is necessary for sales follow-up.
- If the call changed qualification or forecast → update those fields before leaving the record.

## Failure modes & recovery

- **F1 Wrong record:** detect the call on an unrelated person or deal → move, delete, or recreate the activity on the correct record.
- **F2 Missing next step:** detect no future task after a productive call → add the agreed action with owner and due date.
- **F3 Notes too vague:** detect notes like "good call" only → add concrete outcome, objection, and next action.

## Verification

The correct CRM record shows a completed call activity with date, outcome, useful notes, and a next step or explicit no-action reason.

## Variations

- VoIP-integrated CRM: calls may auto-log; review and enrich the auto-created activity.
- Team selling: tag or associate all participating reps so context is shared.
- No-show call: log the no-show disposition and schedule one retry if appropriate.

## Safety & privacy

Do not enter payment details, health information, credentials, or private personal facts in call notes. Follow call recording notices and local consent rules when recordings or transcripts are attached.
