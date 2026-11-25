---
name: google-calendar-automation
description: "Automate Google Calendar: OAuth scopes, event creation with time zones and recurrence, free/busy queries, and safe updates across attendees."
type: procedural
category: productivity
domain: productivity
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - google calendar api event
  - calendar freebusy query
  - recurring event rrule
  - calendar oauth scope
  - schedule meeting automation
keywords:
  - google-calendar
  - oauth
  - rrule
  - timezone
  - freebusy
  - scheduling
source: custom
enabled: true
---

# Google Calendar Automation

## Purpose

Automate Google Calendar: OAuth scopes, event creation with time zones and recurrence, free/busy queries, and safe updates across attendees.

## When to Use

- Events must be created or read programmatically for a workflow.
- Scheduling decisions need free/busy data rather than guesses.
- Recurring events and time zone handling must be correct.

## When NOT to Use

- A simple calendar link or ICS file is sufficient.
- The user's calendar data cannot leave their control for policy reasons.
- You only need to display availability already published elsewhere.

## Capabilities

- Request the narrowest scope that satisfies the workflow.
- Create events with explicit time zones and RRULE recurrence.
- Query free/busy across attendees before proposing slots.
- Update or cancel events without notifying attendees unnecessarily.

## Inputs

- The calendar id (`primary` or a shared calendar) and the account context.
- The time window, attendees and desired duration.
- The time zone policy: organiser's zone or attendee-local.

## Workflow

1. Confirm the target calendar and the account that will own the event.
2. Query `freebusy` for the proposed window before creating anything.
3. Create the event with explicit `timeZone`; avoid naive local datetimes.
4. Use RRULE for recurrence; never create N separate events by hand.
5. Verify by reading the event back and checking attendee responses.

## Tools

- Google Calendar API v3
- OAuth consent flow
- a calendar MCP connector

## Examples

- `allskills mcp install --harness cursor --servers google-calendar`
- `curl -s -H "Authorization: Bearer $TOKEN" "https://www.googleapis.com/calendar/v3/freeBusy" -d @window.json`
- `allskills route "schedule a recurring standup"`

## Safety

- `calendar` scope grants full read/write; prefer `calendar.events` where possible.
- Sending invites emails real people — never test against live attendee lists.
- Recurring event updates can move history; scope changes with `singleEvents` carefully.

## Source

All-Skills canonical library (`skills/productivity/google-calendar-automation`). First-party skill, maintained in this repository.

## Notes

- Store the organiser's time zone explicitly; DST shifts otherwise move meetings.
- `sendUpdates=none` is required for silent bulk changes.
- Pairs with: `productivity/calendar-assistant`, `productivity/google-sheets-automation`.
