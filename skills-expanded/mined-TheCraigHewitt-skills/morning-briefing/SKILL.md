---
name: morning-briefing
description: "Generate a daily briefing dashboard that pulls calendar, email, and news into one interactive HTML page. Use this whenever the user says 'morning briefing,' 'daily briefing,' 'what's on today,' 'start my day,' 'good morning,' 'daily report,' 'today's agenda,' or asks for a summary of their day, schedule, or inbox first thing in the morning. Also use when the user wants to set up a recurring daily report or scheduled task that runs each morning. Trigger even when the user doesn't explicitly say 'briefing' — any 'what should I focus on today' question qualifies."
---

# Morning Briefing

You generate the user's daily briefing: one interactive HTML dashboard plus a short Slack-ready summary. The point is to replace 30 minutes of inbox-skimming, calendar-checking, and news-scanning with a 2-minute scan of a single page.

## What you produce

Two artifacts:

1. **`briefing-YYYY-MM-DD.html`** — an interactive dashboard saved to the current working folder
2. **A short Slack-ready summary** — printed in chat so it can be copied or sent via a Slack connector

## Before you start

Check for a `BUSINESS_CONTEXT.md` or `briefing-config.md` in the working folder. If it exists, read it — it should tell you which connectors to use, what news sources matter, what counts as urgent, and which sections to include or skip.

If neither exists, ask the user once:

- Which connectors do you have? (Gmail, Google Calendar, Slack, Notion, etc.)
- Any news topics you want tracked? (AI, fintech, your industry, specific companies)
- What counts as urgent in your inbox? (clients, investors, specific senders)

Save the answers as `briefing-config.md` for future runs. Don't ask again on subsequent days.

## Gather the data

Pull the following, in parallel where possible:

- **Today's calendar** — all events, with attendees, location/link, and meeting type
- **Unread + flagged email** — count, top 5 most important by recency + sender importance
- **Pending Slack DMs and @mentions** — count + top 3
- **News headlines** — 3–5 items relevant to the user's tracked topics, from the last 24 hours
- **Yesterday's loose ends** — any sent emails awaiting reply, any tasks marked for today

If a connector isn't available, skip that section rather than guessing. Note the gap at the bottom of the dashboard.

## Dashboard structure

Build a single-file HTML page, mobile-friendly, with these sections in order:

1. **Hero strip** — today's date, weather (if connector available), a one-sentence "shape of the day" written by you ("4 meetings, 2 deep-work blocks, one decision needed")
2. **Schedule timeline** — visual timeline of today's meetings, color-coded by meeting type. Click an event for prep notes if available.
3. **Inbox snapshot** — unread count, top 5 emails with sender, subject, one-line summary, and a suggested action (reply / archive / flag / defer)
4. **Slack pulse** — open DMs and @mentions worth responding to
5. **News** — 3–5 cards with headline, source, one-sentence "why it matters to you"
6. **Loose ends** — sent emails over 48 hours old without a reply, prior-day tasks not yet done
7. **Today's one thing** — your read on the single most important thing the user should do today, given everything above

Style: clean, dense, scannable. Light theme by default. Use a small accent color for callouts. No animations beyond hover states.

## Slack summary format

Plain text, under 600 characters, structured like:

```
☀️ Morning briefing — [Date]

📅 [N] meetings today. First: [time + name]. Watch: [the one to be sharp for]
📥 [N] unread, [N] flagged. Urgent: [sender / topic]
💬 [N] Slack DMs waiting
📰 Notable: [one headline + one-line why it matters]
🎯 Today's one thing: [your call]

Full dashboard: [filename]
```

## Why this matters

The user opens this once at the start of the day and decides what to do. If the dashboard is cluttered, generic, or full of stuff they already knew, it has failed — they'll go back to manually checking everything. Optimize for the moment they scan it: every section should either tell them something they didn't already know, or surface something they were about to forget.

## Running on a schedule

After the user runs this manually once and likes the output, suggest scheduling it:

"Want me to run this every weekday morning at 7am? I can turn this into a scheduled task that delivers the dashboard and pings you on Slack."

If yes, set up a recurring scheduled task with the appropriate cron schedule. The scheduled version should write the dashboard to a `briefings/` subfolder, named by date, so the user builds up a history they can search later.

## Rules

1. **Specificity beats completeness.** Three sharp insights > a comprehensive but generic dump. If you're padding to fill a section, cut the section.
2. **Don't summarize what they wrote.** If the user's own sent email is in the inbox, don't summarize it back at them.
3. **Your read matters.** The "Today's one thing" line is the only place you get to play strategist. Use it. Make a real call.
4. **Be useful when connectors fail.** If Gmail is down, still produce the dashboard with the sections you can fill. Note what's missing at the bottom, not at the top.
5. **Don't include sensitive content in the Slack summary.** Subjects and senders are fine; body content is not.
