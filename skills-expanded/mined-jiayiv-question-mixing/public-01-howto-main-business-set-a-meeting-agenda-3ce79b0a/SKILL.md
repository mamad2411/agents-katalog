---
name: set-a-meeting-agenda
domain: business
locale: [generic]
interface: mixed
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Create a focused meeting agenda that makes the purpose, topics, owners, and desired outcomes clear.

## Preconditions

- You know why the meeting is needed.
- You know who should attend and what decision or output is expected.
- You can edit the invite or a shared agenda document.

## Steps

1. **Define the outcome.** Write the decision, alignment, review, or handoff the meeting must produce. → *Expect:* the meeting has a clear end state.
2. **List topics.** Add only topics that need discussion with this group. → *Expect:* the agenda excludes items that can be handled asynchronously.
3. **Assign topic owners.** Name the person leading each topic or decision. → *Expect:* no agenda item is ownerless.
4. **Estimate timing.** Allocate minutes to each topic and leave time for wrap-up. → *Expect:* the agenda fits the meeting length.
5. **Add preparation links.** Include pre-reads, documents, dashboards, or decisions needed before the meeting. → *Expect:* attendees know what to review.
6. **Place the agenda where attendees will see it.** Add it to the calendar invite or link a shared document. → *Expect:* the agenda is visible before the meeting starts.
7. **Confirm with key owners.** Ask topic owners to verify their item and timing. → *Expect:* owners are prepared to lead their sections.

## Decision points

- If there is no clear outcome → cancel or convert to async status sharing.
- If the agenda exceeds the meeting length → cut topics or extend only with attendee agreement.
- If a decision owner cannot attend → reschedule or change the goal to preparation only.

## Failure modes & recovery

- **F1 Agenda too broad:** detect too many topics for the time → move lower-priority items to follow-up.
- **F2 No decision maker:** detect the approver is absent → defer the decision and use the meeting for recommendation building.
- **F3 Missing pre-read:** detect attendees lack context → send the material and delay the decision if needed.

## Verification

The invite or shared document contains the outcome, agenda items, owners, timing, and preparation links before the meeting.

## Variations

- One-on-one: use priorities, blockers, feedback, and decisions instead of a formal agenda.
- Workshop: include exercises, materials, breaks, and facilitation roles.
- Board or executive meeting: circulate the agenda and pre-read farther in advance.

## Safety & privacy

Low risk. Keep sensitive topics and links restricted to attendees with a legitimate need to know.
