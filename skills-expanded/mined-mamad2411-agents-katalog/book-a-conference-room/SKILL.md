---
name: book-a-conference-room
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

Reserve an appropriate conference room for an in-person or hybrid meeting.

## Preconditions

- You know the meeting time, expected headcount, and equipment needs.
- You have access to the room booking system or calendar resources.
- You know any office visitor or room-use rules.

## Steps

1. **Confirm headcount.** Count required in-room attendees and likely visitors. → *Expect:* a minimum room capacity is known.
2. **List room needs.** Note video, screen, whiteboard, phone, privacy, accessibility, or catering needs. → *Expect:* room filters match the meeting requirements.
3. **Search available rooms.** Open the room calendar or booking tool for the meeting time. → *Expect:* available rooms appear for the correct date and duration.
4. **Choose the best fit.** Select a room with enough capacity and required equipment without overbooking a much larger room. → *Expect:* the room matches the meeting size and purpose.
5. **Add the room to the invite.** Reserve the room resource or complete the booking form. → *Expect:* the room shows as accepted, reserved, or pending.
6. **Include access details.** Add floor, building, visitor instructions, or hybrid equipment notes to the invite. → *Expect:* attendees know where to go and what to expect.
7. **Check confirmation.** Verify the room did not decline because of a conflict or approval rule. → *Expect:* the booking status is confirmed or a clear next action is shown.

## Decision points

- If no room fits → shorten the meeting, move time, split attendance, or switch to virtual.
- If room approval is pending → notify attendees that location is not final.
- If external visitors attend → confirm reception, building access, and host responsibilities.

## Failure modes & recovery

- **F1 Room declined:** detect declined resource status → choose another room or time.
- **F2 Capacity mismatch:** detect headcount exceeds seats → rebook a larger room or make some attendees remote.
- **F3 Missing equipment:** detect the room lacks video or display → reserve equipment or change rooms.

## Verification

The room booking is confirmed for the correct time, capacity, location, and equipment needs.

## Variations

- Hybrid meeting: test video equipment or book a room known to support conferencing.
- Confidential meeting: choose a room with doors, sound privacy, and limited visibility.
- Multi-office meeting: reserve rooms in each office and include all locations on the invite.

## Safety & privacy

Low risk. Avoid putting confidential meeting topics on public room displays if the office shows event titles outside rooms.
