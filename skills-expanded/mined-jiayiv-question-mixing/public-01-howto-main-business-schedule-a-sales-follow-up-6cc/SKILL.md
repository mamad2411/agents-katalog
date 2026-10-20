---
name: schedule-a-sales-follow-up
domain: business
locale: [generic]
interface: mixed
difficulty: basic
est_time: 5min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Schedule a timely follow-up after a sales interaction and record it where the owner will act on it.

## Preconditions

- A lead, contact, account, or deal that needs follow-up.
- The reason for follow-up and the preferred channel.
- Permission to contact the prospect or customer by that channel.

## Steps

1. **Open the CRM record.** Find the relevant lead, contact, account, or deal. → *Expect:* the record and recent activity are visible.
2. **Choose the follow-up type.** Select task, email, call, meeting, or sequence based on what was agreed. → *Expect:* the action matches the buyer expectation.
3. **Set owner and due time.** Assign the responsible rep and choose a due date or meeting slot. → *Expect:* the follow-up has an accountable owner and deadline.
4. **Write the action detail.** Add a short subject and notes that explain what to say or send. → *Expect:* the owner can execute without reopening all prior context.
5. **Use the right tool path.** [BRANCH: Salesforce | HubSpot | generic] create a Task or Event in Salesforce; create a Task, Meeting, or Sequence step in HubSpot; in another CRM, create the equivalent reminder or activity. → *Expect:* the follow-up appears in the CRM task or calendar view.
6. **Send or save as appropriate.** If sending an email now, review and send; if scheduling future outreach, save the task. → *Expect:* the CRM shows either sent outreach or a pending follow-up.

## Decision points

- If the buyer requested a specific time → use a calendar invite instead of a generic task.
- If consent is missing → do not schedule marketing outreach; use an allowed operational or internal task instead.
- If the account has an owner → assign the follow-up to that owner unless routing rules say otherwise.

## Failure modes & recovery

- **F1 No reminder created:** detect the follow-up only exists in personal notes → create a CRM task with due date.
- **F2 Wrong channel:** detect a requested call scheduled as email or vice versa → update the task type and notes.
- **F3 Noncompliant outreach:** detect missing opt-in, opt-out, or lawful basis → cancel the outreach task and ask the owner to verify permission.

## Verification

The CRM record shows a pending or sent follow-up with owner, due date, channel, and clear action detail.

## Variations

- Calendar-based follow-up: include attendees, timezone, agenda, and conferencing details.
- Sequence-based follow-up: enroll only if the contact meets consent and segmentation rules.
- Customer follow-up: coordinate with customer success before scheduling commercial outreach.

## Safety & privacy

Medium risk when external outreach is sent or scheduled. Follow CAN-SPAM, GDPR, opt-out, consent, frequency, and company communication rules before contacting anyone.
