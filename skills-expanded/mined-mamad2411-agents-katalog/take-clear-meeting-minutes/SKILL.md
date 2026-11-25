---
name: take-clear-meeting-minutes
domain: communication
locale: [generic]
interface: mixed
difficulty: basic
est_time: 30min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Capture meeting minutes that preserve decisions, action items, owners, and useful context without becoming a transcript.

## Preconditions

- A scheduled meeting with agenda, attendees, or topic.
- Permission to take notes and clarity on whether notes are public, internal, or confidential.
- A shared document, ticket, or email thread for distributing minutes.

## Steps

1. **Create the note structure.** Set headings for attendees, decisions, action items, open questions, and context links. → *Expect:* notes are ready before discussion starts.
2. **Record attendance.** List who attended, who was absent, and who represented each function if relevant. → *Expect:* readers know whose input was present.
3. **Capture decisions as decisions.** Write "Decision: We will do X because Y; owner is Z." → *Expect:* decisions are not buried in discussion notes.
4. **Track actions live.** For each action, write owner, deliverable, due date, and dependency. → *Expect:* follow-up work is assignable.
5. **Summarize discussion selectively.** Include key tradeoffs, objections, and evidence, not every sentence. → *Expect:* absent stakeholders understand the reasoning.
6. **Clarify ambiguous items.** Ask "Can I capture that as an action for Pat by Thursday?" when ownership is unclear. → *Expect:* the group confirms wording in real time.
7. **Send minutes promptly.** [BRANCH: small team | formal meeting] send informal minutes in the team channel; send formal minutes by email or approved repository. → *Expect:* participants can correct mistakes while memory is fresh.
8. **Update the source of truth.** Copy decisions and action items into the project tracker or decision log. → *Expect:* minutes drive execution beyond the meeting.

## Decision points

- If the meeting is confidential → label the notes and limit distribution.
- If no decisions were made → state "No decisions; follow-up needed on X."
- If the meeting is recorded → still capture decisions and actions because recordings are hard to scan.
- If people dispute the notes → ask the decision owner to confirm final wording.

## Failure modes & recovery

- **F1 Notes become a transcript:** detect long chronological paragraphs → rewrite into decisions, actions, open questions, and context.
- **F2 Owner missing:** detect action items with "we" or "team" → assign one named owner or mark owner needed.
- **F3 Sensitive detail shared too widely:** detect private personnel, legal, or customer data in broad notes → remove or restrict before sending.

## Verification

The minutes identify attendees, decisions, action items with owners and dates, open questions, and a distribution location visible to the intended audience.

## Variations

- Board or governance meeting: follow the required formal minute format.
- Technical design meeting: add links to design docs, tickets, and rejected alternatives.
- Customer meeting: separate internal follow-up notes from customer-facing recap.

## Safety & privacy

Low to medium risk depending on content. Do not include private HR, legal, customer, medical, or financial details unless the audience is authorized.
