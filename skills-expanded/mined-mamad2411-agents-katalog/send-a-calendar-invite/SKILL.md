---
name: send-a-calendar-invite
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

Create and send a calendar invite with the correct attendees, time, location, and meeting context.

## Preconditions

- You know the meeting title, date, start time, end time, and attendee list.
- You have access to a calendar account.
- You know whether the meeting is virtual, in person, or hybrid.

## Steps

1. **Open a new event.** Start a calendar event on the intended calendar, not a personal or test calendar. → *Expect:* a blank event editor is open.
2. **Enter the title.** Use a specific title that identifies the topic or decision. → *Expect:* the event is recognizable on a busy calendar.
3. **Set date and time.** Enter the confirmed start, end, and time zone. → *Expect:* the event duration matches the planned meeting.
4. **Add attendees.** Add required participants and mark optional attendees if the tool supports it. → *Expect:* the invitee list contains the intended people only.
5. **Add location or link.** [BRANCH: virtual | in-person | hybrid] add video link, room, or both as appropriate. → *Expect:* attendees know where to join.
6. **Write the description.** Include the agenda, preparation links, and owner for follow-up. → *Expect:* attendees understand why they are invited.
7. **Check notifications.** Confirm default reminders are suitable and avoid noisy extra reminders. → *Expect:* reminders are present but not excessive.
8. **Send the invite.** ⚠️ *Irreversible:* before sending, confirm attendees, time zone, and external recipients because invitations may notify everyone immediately. → *Expect:* the calendar event shows as sent or saved with guests.

## Decision points

- If attendee availability is unknown → check free/busy or ask before sending.
- If the invite includes external guests → verify the description has no internal-only notes.
- If the event is tentative → put "HOLD" in the title and explain the confirmation condition.

## Failure modes & recovery

- **F1 Wrong attendee:** detect an unintended person on the guest list → remove them and send a corrected update.
- **F2 Missing join details:** detect no link or room in the invite → add the location and update guests.
- **F3 Time-zone error:** detect attendee confusion or shifted time → correct the time zone and resend the update.

## Verification

The event appears on the intended calendar with the correct attendees, time, location or join link, and description.

## Variations

- Executive meeting: keep the title and description concise and attach pre-read links.
- Interview: include candidate-friendly joining instructions and interviewer roles.
- Webinar hold: mark attendees optional if the event is informational.

## Safety & privacy

Low risk. Do not include confidential notes, private customer data, or sensitive personnel context in an invite visible to guests.
