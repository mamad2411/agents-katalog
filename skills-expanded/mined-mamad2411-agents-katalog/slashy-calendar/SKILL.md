---
name: slashy-calendar
description: Check calendar availability, find and compare meeting times, create or update events and invitations, and schedule from email through Slashy MCP. Use for free/busy questions, proposed slots, event details, RSVP or invite work, timezone-aware scheduling, and drafting email that offers calendar availability.
---

# Slashy calendar

Use the connected Slashy calendar tools for live availability and events.
Discover exact tool names and schemas before the first call.

## Availability and proposed times

1. Resolve relative dates to concrete dates and state the timezone used.
2. Gather duration, attendees, working-hour constraints, and conferencing needs
   from the request; infer only low-risk defaults and state them.
3. Check live availability across every relevant calendar.
4. Return a small ranked set of slots with date, local time, timezone, and
   duration. A proposal is read-only until the user asks to book it.

## Create or change an event

- Create, reschedule, cancel, invite, or RSVP only when explicitly requested.
- Before a write, verify the date, start time, timezone, duration, organizer
  calendar, attendee addresses, and recurrence when applicable.
- Distinguish a private or tentative hold from an attendee event. "Put it on my
  calendar" authorizes a hold, but does not by itself authorize sending an
  invitation to someone else.
- Avoid double-booking: re-check availability immediately before creation when
  the proposed slot came from an earlier turn.
- After the tool succeeds, report the final title, date/time/timezone,
  attendees, calendar, conferencing details, and any attendee failures.
- Calendar events do not have Slashy deep links. Do not fabricate one.

## Schedule from an email

1. Use `slashy-email` to read the relevant thread and extract participants,
   constraints, and requested duration.
2. Check availability and choose or propose the requested number of slots.
3. Draft a reply offering those slots unless the user explicitly asked to send.
4. Create an event only when the user explicitly asked to book it; offering a
   time in a draft does not authorize event creation. If the request authorizes
   a calendar hold but not an invitation, create a private or tentative hold.

When multiple inboxes or calendars are connected, keep the sending identity,
organizer calendar, and timezone explicit so the wrong account is not used.
