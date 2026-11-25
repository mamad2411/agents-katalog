---
name: pa-daily-digest
version: 1.0.0
description: Produce a concise personal daily digest — calendar, tasks, weather, and the emails that need attention.
author: matrixx0070
tags: [digest, daily, calendar, briefing, personal-assistant]
capabilities: []
---

## When to use

Use this when the owner wants a single morning (or evening-prep) briefing that pulls the day together: what is scheduled, what must get done, the weather, and the few messages that actually need them. Good as a standing 7am start-the-day summary.

**Not for:** deep inbox triage (hand that to a triage skill), long-form planning, or acting on the items — the digest informs; the owner decides and acts.

## Method

1. Set the window (today by default) and gather sources: calendar events, task/reminder list, weather for the owner's location, and flagged/important emails.
2. Order the calendar chronologically; mark the first commitment and any hard deadlines today.
3. Decision point — more than ~5 tasks? Show the top 3 by priority and collapse the rest into a count, so the digest stays skimmable.
4. Summarize weather as a one-liner plus any actionable note (umbrella, cold snap, commute impact).
5. Pull only emails that need the owner today (a reply, a decision, a deadline) — not the full inbox; give sender + one-line ask each.
6. Decision point — anything time-critical in the next 2 hours (early meeting, thing due at noon)? Surface it as a top "HEADS UP" line.
7. Deliver it tight — a full digest should read in under 30 seconds. Confirm before sending any reply or acting on a digest item.

## Example

Output:
HEADS UP: 9am dentist — leave by 8:30.
CALENDAR: 9:00 dentist, 11:00 team call, 6:00 dinner w/ Alex.
TOP TASKS: 1) submit tax form (due today) 2) call bank 3) gym.
WEATHER: 12C, rain from 3pm — take an umbrella.
NEEDS YOU: Landlord — confirm renewal; Mom — call back re: weekend.

## Pitfalls

- Dumping the whole inbox/task list — the point is a filtered brief, not a data dump.
- Burying the time-critical item mid-list; lead with HEADS UP.
- Vague weather ("nice out") with no action. Say what to do about it.
- Acting on digest items unprompted. The digest reports; sending or scheduling needs the owner's OK.

## Output format

```
DAILY DIGEST — [day, date] — [location]

HEADS UP: [most time-critical thing, or "clear morning"]
CALENDAR
- [HH:MM] [event]
TOP TASKS (of [N])
1. [task] (due/priority)  2. ...
WEATHER: [temp/conditions] — [action note]
NEEDS YOU
- [sender] — [one-line ask]

Next: say the word to reply/act on any item — nothing sent automatically.
```
