---
name: morning-brief
description: Produces a short morning briefing from the user's calendar, inbox, and messaging apps — today's schedule, the emails that actually need attention, the top three priorities for the day. Use when the user asks for a morning brief, daily summary, start-of-day briefing, or variations. Best run as a scheduled task weekday mornings.
---

# Morning Brief

Turn calendar + inbox + messaging chaos into one readable page the user can scan while drinking coffee.

## Before starting

Read these in order. Skip any that don't exist.

1. `context/about-me.md` — who the user is
2. `context/preferences.md` — how they want reports formatted
3. `context/voice.md` — only if the brief includes any drafted messages

If none of those exist, tell the user this skill works better with context files set up, and offer to help create them. Then proceed with sensible defaults.

## What to produce

A single markdown file, saved to `/output/morning-brief-{YYYY-MM-DD}.md`, with four sections:

1. **Today at a glance** — the day's calendar, one line per event. Highlight the first event and any back-to-backs.
2. **Inbox that matters** — emails received since the last brief (or the last 18 hours if no prior brief exists) that meet at least one of: (a) from a named priority contact, (b) explicit question directed at the user, (c) deadline in the next 48 hours, (d) reply from an active thread the user started. Summarize each in one line. Skip everything else.
3. **Messages worth seeing** — same filter applied to Slack, Teams, or whichever messaging connector is wired up. Only DMs and @mentions, never channel noise.
4. **Top three priorities** — your best read of what the user should focus on today, based on the calendar, the inbox, and anything flagged in prior briefs. One line each, with a one-line "why."

## What not to do

- Do not include every email. If the list is longer than 8 items, you've set the bar too low — raise it.
- Do not draft replies. This is a brief, not an action.
- Do not include marketing emails, newsletters, automated notifications, or CC-ed threads where the user isn't the primary recipient.
- Do not speculate on priorities without evidence. If you can't justify a priority from the data, leave it out.

## Inputs (usually connectors)

- Google Calendar or equivalent (required)
- Gmail or equivalent (required)
- Slack / Teams / other messaging (optional but valuable)
- Prior morning briefs in `/output/` (optional — use to track continuity)

## How it works

1. Pull today's calendar events (user's local time zone from `preferences.md`, or ask)
2. Pull unread + recently-read emails in the window (default: since last brief, else 18 hours)
3. Apply the "inbox that matters" filter
4. Pull messages (if connector available) — DMs and @mentions only
5. Read the prior brief if one exists, note any "to follow up on tomorrow" items
6. Assemble the four-section brief, save to `/output/morning-brief-{YYYY-MM-DD}.md`
7. Tell the user the file is ready and give a one-sentence top-line ("Big day — three external calls, two flagged emails, one decision due.")

## Example output structure

```markdown
# Morning Brief — 2026-04-18

**TL;DR:** Three external calls, two flagged emails, one decision due by 3pm.

## Today at a glance
- 09:00–09:30 — 1:1 with Morgan *(first event)*
- 10:00–11:00 — Board prep (internal)
- 13:00–14:00 — Acme discovery call *(external — confirm deck is final)*
- 15:00–15:30 — Back-to-back starts: Q2 planning
- 15:30–16:00 — Back-to-back continues: ops review

## Inbox that matters (3)
- **Sarah Chen (Northwind)** — asking for contract redline by EOD Friday
- **Morgan** — sent Q2 priorities doc for review ahead of 9am 1:1
- **Legal (thread reply)** — answered the question about indemnification; needs your sign-off to proceed

## Messages worth seeing (2)
- Slack DM from Taylor: "Need your call on the vendor switch by 3pm"
- Slack @mention in #ops: question about the weekly report format

## Top three priorities
1. **Decision on vendor switch by 3pm** — Taylor is blocked. (from Slack DM)
2. **Read Morgan's Q2 priorities doc before 9am** — better prep for the 1:1. (from inbox)
3. **Redline Northwind contract today or tomorrow** — Friday EOD is the real deadline. (from inbox)
```

## Customization notes

- If the user works outside a standard 9–5, ask them what window to pull the inbox over.
- If they use a non-Google / non-Microsoft calendar, you'll need a compatible connector or an iCal export workflow.
- If the "inbox that matters" filter is too aggressive or too loose, tell them to save feedback to `memory.md` and this skill will tune over time.
