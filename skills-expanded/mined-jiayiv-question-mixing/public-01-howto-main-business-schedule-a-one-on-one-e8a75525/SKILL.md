---
name: schedule-a-one-on-one
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Schedule a one-on-one meeting with the right participant, cadence, agenda space, and calendar details.

## Preconditions

- You know who should attend the one-on-one.
- You have access to both calendars or a scheduling tool.
- The desired cadence and meeting length are known.

## Steps

1. **Check availability.** Compare calendars for both participants and select a workable time. → *Expect:* an open time slot is identified.
2. **Create the event.** Add the participant, title, date, time, duration, and recurrence if needed. → *Expect:* the calendar invite draft has the correct basics.
3. **Add location or link.** Include a room, video link, phone number, or office location. → *Expect:* attendees know how to join.
4. **Add agenda space.** Include a shared agenda document or brief description of topics to maintain. → *Expect:* both participants have a place to add topics.
5. **Set visibility.** Use appropriate privacy settings if the meeting may include personnel, performance, or health topics. → *Expect:* calendar details are visible only as intended.
6. **Send the invite.** Send the calendar invitation to the participant. → *Expect:* the invite appears on both calendars or awaits response.
7. **Confirm acceptance.** Check the attendee response or follow up if needed. → *Expect:* attendance is accepted, tentative, or clearly pending.

## Decision points

- If the meeting may cover sensitive HR topics → make the event private and avoid detailed calendar descriptions.
- If schedules do not overlap → offer two or three alternatives or use a scheduling link.
- If the one-on-one is recurring → choose an interval that matches the relationship and workload.

## Failure modes & recovery

- **F1 No meeting link:** detect a remote meeting with blank location → add a valid link and notify the attendee.
- **F2 Wrong recurrence:** detect too many or too few events → update the series and confirm the next occurrence.
- **F3 Sensitive title:** detect confidential details in the visible title → rename to a neutral title and set private visibility.

## Verification

The calendar shows the one-on-one with correct participant, time, recurrence if needed, join details, and appropriate visibility.

## Variations

- US: avoid calendar details that reveal medical, leave, or protected HR topics.
- Other countries: calendar privacy, working time, and employee monitoring norms may differ.
- Manager one-on-one: include a shared agenda and recurring cadence.

## Safety & privacy

Low risk, but one-on-ones may involve personnel information. Keep sensitive topics out of public calendar fields and apply scheduling norms consistently.
