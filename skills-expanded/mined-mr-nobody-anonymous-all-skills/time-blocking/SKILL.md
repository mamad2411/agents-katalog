---
name: time-blocking
description: Build realistic deep-work time blocks around energy, priorities, breaks, and constraints.
category: productivity
aliases:
- calendar-block
triggers:
- Schedule deep work
- Block time for
- When should I do this
- I keep getting interrupted
- Help me plan my week
keywords:
- time
- block
- schedule
- deep
- work
- calendar
- pomodoro
- focus
- planning
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- time-blocking
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
- block
- blocking
- deep
- productivity
- schedule
- time
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

# Time Blocking

## Purpose
Place a piece of work on the calendar with enough context (intent, duration, recovery,
friction-reducers) that the block actually gets used instead of being quietly cancelled
by a meeting invite or a "quick check" of email.

## When to Use
- The user has identified a chunk of work that needs uninterrupted time
- The user reports losing their day to small tasks and meetings
- A planning conversation has just produced a list of chunks (see `adhd-task-breakdown`)

## When NOT to Use
- The work is itself a small action (just do it)
- The user's calendar is fully owned by others (route to `focus-guard` or a meeting audit)

## Capabilities
- Convert a work item into a calendar event with the right duration
- Add a 10-minute ramp-up and 10-minute ramp-down around the block
- Pair the block with a friction-reducer (tabs closed, phone in another room, focus music)
- Suggest recovery gaps between deep-work blocks
- Honor realistic energy levels (morning vs. afternoon)
- Re-time blocks when a conflict is detected

## Inputs
- The work item (one sentence)
- A target duration or energy level
- Existing calendar (optional; can be inferred)

## Workflow
1. **Restate the work item** as a verb phrase ("Write the API spec", not "Spec").
2. **Pick a duration** — minimum 25 min, maximum 90 min before a break.
3. **Wrap it**: add 5 min before for setup, 5 min after for shutdown notes.
4. **Add a friction-reducer** to the event description (one concrete action).
5. **Check for collisions** with existing meetings; if any, propose a new time.
6. **Write the event** with the verb phrase as the title and the friction-reducer in the body.

## Tools
- Calendar API (Google Calendar, Outlook, or iCal via `ical` / `gcalcli` / `outlook-cli`).
- Optional: notification suppression via `focus-guard` (Do Not Disturb mode).

## Examples
**User:** "Block 2 hours for the auth refactor tomorrow."
**Response:**

> Tomorrow, 09:30 â€“ 11:30. Title: "Auth refactor — split user/session tables".
> Body: "Before: close Slack, open branch, run migrations locally. After: write 3-line shutdown note."

**User:** "I want to write a blog post this week."
**Response:**

> 3 blocks, 60 min each, on Tue / Wed / Thu morning. Tue: outline. Wed: first draft.
> Thu: edit. Each block wrapped with 5-min setup and 5-min shutdown.

## Safety
- Do not schedule through sleep hours
- Do not pack more than 4 deep-work blocks into a single day
- Honor stated energy and accessibility constraints

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical productivity category.
