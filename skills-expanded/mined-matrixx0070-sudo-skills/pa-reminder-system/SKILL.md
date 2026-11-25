---
name: pa-reminder-system
version: 1.0.0
description: Set up a reliable reminder and follow-up system for the owner's commitments and deadlines.
author: matrixx0070
tags: [reminders, follow-up, deadlines, commitments, personal-assistant]
capabilities: []
---

## When to use

Use this when the owner has commitments, deadlines, or open loops that keep slipping and wants a structured system that surfaces the right nudge at the right time. Good for "things I keep forgetting," follow-ups awaiting someone else's reply, and recurring obligations.

**Not for:** full project management with dependencies and assignees, real-time alarms you cannot actually fire, or nagging other people directly — you remind the owner, who then acts.

## Method

1. Capture every commitment: what, who it involves, the hard deadline, and whether it is one-off or recurring.
2. Classify each as **DEADLINE** (fixed date), **FOLLOW-UP** (waiting on someone — track the wait), or **RECURRING** (repeats on a cadence).
3. Decision point — is there a true deadline or just "soon"? If vague, propose a concrete date and confirm it, because undated items never fire.
4. Set a lead time per item: high-stakes or prep-heavy → remind 3-7 days ahead plus day-of; trivial → day-of only.
5. For FOLLOW-UPs, set a "check back" date; if no reply by then, surface a nudge draft for the owner to send.
6. Decision point — does the reminder engine exist (calendar, task app, scheduled message)? Use the available channel; if none, deliver as a dated checklist the owner can paste in.
7. Confirm the schedule. Confirm before sending any follow-up message to a person.

## Example

Input: "Renew passport (expires in 3 months), waiting on quote from plumber, water the plants weekly."
System: DEADLINE passport — remind at 8/6/4 weeks + day-of. FOLLOW-UP plumber — check back in 3 days; if silent, nudge draft ready. RECURRING plants — every Sunday. Owner gets one weekly digest plus dated alerts.

## Pitfalls

- Undated reminders. "Later" never triggers; force a real date or it is not tracked.
- One lead time for everything. A passport needs weeks of runway; a call needs an hour.
- Silent follow-ups that never close. Every FOLLOW-UP needs a check-back date and an escalation.
- Auto-sending the nudge to the third party. Surface the draft and confirm before messaging anyone.

## Output format

```
REMINDER SYSTEM — [owner] — [date set]

DEADLINES
- [item] — due [date] — remind: [lead schedule]
FOLLOW-UPS
- [item] — waiting on [who] since [date] — check back [date] — nudge draft: "[text]"
RECURRING
- [item] — every [cadence] — next [date]

Delivery: [channel / weekly digest]
Next: reply YES to schedule these; follow-up messages sent only on your OK.
```
