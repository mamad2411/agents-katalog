---
name: schedule-a-meeting-across-time-zones
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

Find and propose a meeting time that works for participants in different time zones.

## Preconditions

- You know the required attendees and their locations or time zones.
- You have access to a calendar or scheduling tool.
- You know the meeting length and latest acceptable meeting date.

## Steps

1. **List participant zones.** Record each attendee's city or time zone and normal working hours. → *Expect:* every required attendee has a time zone and availability window.
2. **Set the meeting length.** Choose the shortest duration that can achieve the meeting purpose. → *Expect:* the calendar search uses a specific duration.
3. **Compare overlapping hours.** Use a calendar availability view or world-clock planner to find times inside shared working hours. → *Expect:* at least one candidate slot is visible, or the conflict is clear.
4. **Check calendar conflicts.** Review required attendees' free/busy calendars for the candidate slots. → *Expect:* the best slot has no required-attendee conflicts.
5. **Prefer fair inconvenience.** If no slot fits everyone cleanly, rotate the burden away from the same person or region. → *Expect:* the chosen slot is defensible and not repeatedly unfair.
6. **Send the proposed time with zones.** Include the time in your zone plus the main attendee zones or use the calendar tool's timezone conversion. → *Expect:* attendees can see the meeting time in their local calendar.
7. **Hold alternatives briefly.** If approval is needed, mention one backup option and set a response deadline. → *Expect:* people know when the time will be finalized.

## Decision points

- If a required attendee has no overlapping work hours → ask whether async input can replace attendance.
- If the meeting is urgent → choose the least-bad shared slot and explain the constraint.
- If attendees are external customers → prioritize their business hours unless internal coverage is impossible.

## Failure modes & recovery

- **F1 Wrong time zone:** detect an attendee says the time is outside their stated zone → correct the invite and resend.
- **F2 Daylight-saving mismatch:** detect conflicting converted times → use named cities instead of manual offsets.
- **F3 No common slot:** detect every required attendee is busy → reduce required attendees or switch to async review.

## Verification

The selected slot appears on required attendees' calendars at the intended local time and does not conflict with known required-attendee events.

## Variations

- Large group: use a poll and select the slot with required attendees plus the strongest optional attendance.
- Recurring meeting: verify the time works for future daylight-saving changes.
- Customer meeting: include the customer's local time explicitly in the message.

## Safety & privacy

Low risk. Do not expose private calendar details when summarizing conflicts; share only availability, not event names.
