---
name: calendar-assistant
description: Plan and modify calendar events with timezone checks, conflict detection, and confirmation.
category: productivity
aliases:
- event
- google-calendar
- outlook
triggers:
- Schedule this meeting
- Add to my calendar
- What's on my calendar
- Find a time for
- Check for conflicts
keywords:
- calendar
- schedule
- meeting
- event
- time
- timezone
dependencies:
- optional:calendar-access
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- calendar-assistant
- productivity
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- assistant
- calendar
- event
- meeting
- productivity
- schedule
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Calendar Assistant

## Purpose
Plan, modify, and query calendar events with proper timezone handling, conflict
detection, and explicit user confirmation for all changes. The skill helps users
manage their time effectively without overbooking or scheduling conflicts.

## When to Use
- Scheduling a new meeting or event
- Checking availability before committing
- Finding time slots for a proposed meeting
- Querying upcoming events

## When NOT to Use
- Real-time calendar monitoring (use notifications)
- Automatic scheduling without user approval
- Accessing shared calendars without authorization

## Capabilities
- List upcoming events (today, this week, custom range)
- Create events with title, time, duration, location, attendees
- Update event details
- Cancel or delete events
- Find available time slots
- Conflict detection and alerts
- Timezone conversion and display
- Recurring event support

## Inputs
- `action` (required) — one of: list, create, update, delete, find-time
- `event_details` (required for create/update) — title, time, duration, etc.
- `range` (optional for list) — today, this-week, custom dates
- `attendees` (optional) — list of participant emails

## Workflow
1. **Query** — Fetch current calendar state
2. **Check** — Detect conflicts, show availability
3. **Draft** — Prepare event details for user review
4. **Confirm** — Wait for explicit approval
5. **Execute** — Create/update/delete event
6. **Notify** — Confirm action taken

## Tools
- Calendar API (Google Calendar, Outlook, or CalDAV)
- Timezone library

## Examples
**User:** "Find time for a 1-hour meeting with alice@example.com tomorrow"
**Response:**
```
Available slots tomorrow (Feb 10):
- 10:00-11:00 AM âœ“ (Alice available)
- 2:00-3:00 PM âš ï¸ (You have 'Lunch' 1-2pm)
- 4:00-5:00 PM âœ“

Select a slot or I'll propose 10:00 AM.
```

## Safety
- ALWAYS require confirmation before creating/modifying events
- Never auto-schedule meetings
- Verify attendee availability before booking
- Warn about double-booking
- Respect calendar access permissions
- Include timezone information in all responses

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical productivity category.
