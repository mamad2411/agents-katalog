---
name: remind-me
description: Turns the open loops from the current conversation into reminders. It proposes the platform (Google Tasks, Google Calendar, email to self, or a T3 scheduled task), the time and the text, then creates them once Magnus confirms. Use when Magnus says "remind me", "$remind-me", "/remind-me", "minn meg på", or "så jeg ikke glemmer det". Also use it unprompted when a task ends with open loops (waiting on a reply, a deadline, a long-running agent or CI job), and offer the proposal instead of creating anything.
---

# Remind me

Magnus should only have to say yes or correct you. You do the thinking: what needs a reminder, where it goes, when it fires and what it says. Nothing gets created until he confirms.

## 1. Harvest the open loops

Read back through the whole conversation and list every **open loop**:

- waiting on someone (a reply, an approval, a delivery)
- a deadline or appointment that was agreed
- something Magnus has to do himself later (file an expense claim, call someone, review a PR)
- an agent job, CI run, deploy or build that is still running
- a decision that was postponed

Done means every loop is either proposed as a reminder or listed as skipped, with the reason. Before proposing, check that the reminder does not already exist. Update an existing task or event instead of creating a duplicate.

## 2. Choose platform and time

| Platform | Choose when | Tool |
|---|---|---|
| **Google Tasks** (default) | Something Magnus has to do, tied to a date but not a time | `gws tasks tasks insert`, TODO list |
| **Google Calendar** | Tied to a time: an appointment, a call within business hours, a block of work | `gws calendar events insert` |
| **Email to self** | The context is too big for a task note: commands, links, a summary of agent work, a handoff to a later session. It is sent now and lands in the inbox as the reminder | `gws gmail +send --to magnus.rodseth@gmail.com` |
| **T3 scheduled task** | An agent can check the follow-up itself, such as a reply arriving in Gmail, CI going green or a job finishing. It runs a prompt later and posts the result to the thread | `mcp__t3-code__schedule_task` |

Two platforms for one loop is fine when each does its own job, for example a calendar event for the appointment and a task for the expense claim afterwards. Never use more than two.

Default timing:

- **Waiting on a reply:** 2 working days after it was sent.
- **Deadline:** with enough margin to act. A hard end date, such as a last working day, wins over everything else.
- **Agent or CI job:** the expected finish time plus margin.
- **A call:** within the recipient's opening hours, if they appeared in the conversation.

For time-bound proposals, check the calendar for conflicts. Use the Europe/Oslo timezone.

## 3. Propose

Show a table and wait:

| # | Reminder | Platform | When | Text (title + note) |
|---|---|---|---|---|

The title must make sense on its own on a phone screen. The note holds the why, the links, the phone numbers and what "done" looks like. Write in the language of the conversation. Then ask whether he wants to confirm or change anything.

## 4. Create and verify

Create only what he confirmed, with the changes he asked for. Read every item back afterwards (`get` or `list`) and report what was created. Include the ID or link and the time.

## Reference

- **Google Tasks:** the TODO list ID is `MDA2MzI2Mjc0MDE1MDgxNzM0ODY6MDow`. If it fails, find the list by its title "TODO" with `gws tasks tasklists list`. `due` keeps the date only, and the API drops the time. When the time matters, use Calendar.
  `gws tasks tasks insert --params '{"tasklist":"<id>"}' --json '{"title":"...","notes":"...","due":"YYYY-MM-DDT00:00:00.000Z"}'`
- **Google Calendar:** use `primary` by default. If Lotte is involved as well, use the shared calendar `family17231499499363123738@group.calendar.google.com`, and do not invite her to a primary-calendar event. A meeting with other people gets a title like `Magnus x Ola: Topic`.
  `gws calendar events insert --params '{"calendarId":"primary"}' --json '{"summary":"...","start":{"dateTime":"...","timeZone":"Europe/Oslo"},"end":{...},"description":"..."}'`
  Search by date with `events list` before you `patch`. A `q` search can match the wrong event.
- **Email to self:** the subject starts with `[Påminnelse]` or `[Reminder]`. The body must stand on its own without this conversation. Gmail has no scheduled send through gws, so for email at a later time, use a T3 scheduled task whose prompt sends it.
- **T3 scheduled task:** `schedule` only supports recurring triggers (`fixed_time`, `interval`). For a one-off reminder, the prompt must end by calling `schedule_task` with its own `scheduledTaskId` and `enabled:false`. Write the prompt so a fresh agent can act on it: what to check, how, and what counts as done. Report the next run time that comes back. Only works when the session runs in T3.
