---
name: meeting-scheduler
description: Schedule a meeting with someone using M365 Copilot Chat. Use when the user wants to set up a meeting — Copilot handles name resolution, availability checking, and booking. Requires browser automation via Playwright.
---

# Meeting Scheduler

Schedule a meeting using M365 Copilot Chat via Playwright browser automation. Copilot resolves names, checks attendee availability, and creates the calendar event.

## Workflow

1. Navigate to `https://m365.cloud.microsoft/chat/?auth=2&home=1` and wait 5 seconds for Copilot Chat to load
2. Take a `browser_snapshot` — confirm the chat compose box is visible. If you see a login page, STOP and report that the session has expired.
3. Type a scheduling prompt into the compose box using `browser_type`:
   "Schedule a [duration] meeting with [attendee names] about [subject]. Find a time that works for everyone [this week / next week / specific date range]."
   Then press Enter to submit.
4. **WAIT PATIENTLY** — Copilot takes 15-30 seconds to check availability. Use `browser_wait_for` with `time: 20` seconds, then take a `browser_snapshot` to check progress.
5. If Copilot is still working (shows a loading indicator or "Searching" text), wait another 15 seconds and snapshot again. Repeat up to 3 times (total ~60 seconds max).
6. Once Copilot responds with time slot options:
   - Take a `browser_snapshot` to read ALL proposed time slots
   - Note each option: day, time range, and any conflict warnings
7. **MANDATORY CONFIRMATION** — call `ask_user`:
   "Schedule meeting:
    Subject: [meeting subject]
    Attendees: [list of resolved names]

    Copilot suggests these times:
    1. [Day, Time range]
    2. [Day, Time range]
    3. [Day, Time range]

    Which option? Reply with the number, or 'cancel' to abort."
8. WAIT for user response. If 'cancel' or no response → abort immediately.
9. Click the user's chosen time slot option in the Copilot UI
10. Wait 5 seconds, then take a `browser_snapshot` to check for a confirmation card or "Send" button
11. If Copilot shows a final confirmation card with a "Send" or "Book" button, click it
12. Wait 3 seconds, take a final `browser_snapshot` to confirm the meeting was created
13. Report the result: meeting title, time, and attendees

## Handling Copilot Responses

Copilot may respond in several ways:

- **Time slot cards**: Interactive cards showing available times. Read all options from the snapshot.
- **Conflict warning**: "X has a conflict at that time." Report this to the user in the confirmation step.
- **Name ambiguity**: "Did you mean X or Y?" Take a snapshot, read the options, and include them in the ask_user confirmation.
- **No availability**: "No common free time found." Report this to the user and suggest they provide alternative dates.
- **Error / timeout**: If Copilot doesn't respond after 60 seconds total waiting, report the failure and suggest the user try manually.

## Rules

- NEVER book a meeting without calling `ask_user` first and receiving a selection.
- NEVER guess meeting times — always let Copilot check availability first.
- If Copilot asks a clarifying question, read it from the snapshot and relay it to the user via `ask_user`.
- If Copilot shows a login page or error, STOP and report the issue.
- Default duration is 30 minutes unless the user specifies otherwise.
- Default time range is "this week" unless the user specifies otherwise.
- Keep the scheduling prompt simple and direct — Copilot works best with natural language.
- If Copilot's UI changes or the expected elements aren't found, STOP and report what you see rather than guessing.
