---
name: morning-brief
description: Daily 6:30am Morning Brief — calendar, tasks, email triage, meeting prep, weather. Sends via Telegram. EXAMPLE — adapt to your own setup.
---

# Morning Brief (example)

> **EXAMPLE — adapt to your own setup.** Replace placeholders with real values. This skill demonstrates the multi-source aggregator pattern: pull from calendar + email + task source + weather, synthesize, send as a single rich Telegram message.

You are Nolty running the Morning Brief.

If you see a `[cron model:X effort:Y]` suffix, you were fired by `cron-runner.py`. Spawn a Task sub-agent with the specified model + effort. The sub-agent has access to your `reply` MCP tool.

## Procedure

### STEP 1 — Get today's calendar

```bash
/opt/homebrew/bin/gog calendar list --today --account YOUR_EMAIL@example.com --json
```

Parse out events. Skip all-day events for the brief unless they're significant (out-of-office, conference). For each remaining event, note: time, title, attendees, and whether you have a prep doc (next step).

Also pull tomorrow's "at a glance":

```bash
/opt/homebrew/bin/gog calendar list --days 2 --account YOUR_EMAIL@example.com
```

### STEP 2 — Get unread / important email

```bash
/opt/homebrew/bin/gog gmail search "is:unread newer_than:1d" --limit 20 --account YOUR_EMAIL@example.com
```

Same triage rules as heartbeat: client replies, time-sensitive items, anything from a frequent contact. Skip newsletters, automated notifications, LinkedIn InMail.

### STEP 3 — Meeting prep (for each meeting that needs it)

For each meeting in the next 4 hours with a contact you have history with:

Use the `Task` tool (subagent_type: "general-purpose") to spawn a meeting-prep sub-agent. Prompt:

> "Run the meeting-prep skill at `examples/meeting-prep/SKILL.md` (or `skills/meeting-prep/SKILL.md` if you've copied it into core) for [Contact] at [Company], meeting at [Time]. Save prep doc to YOUR_OBSIDIAN_VAULT/MeetingPreps/[date]-[contact].md. Return only the file path + 1-line summary."

Don't inline the meeting-prep logic in the morning-brief sub-agent — keeps context small. The nested sub-agent gets fresh context.

The meeting-prep skill itself ships in `examples/meeting-prep/SKILL.md`. If you haven't enabled it, either skip this step or set up a stub (write a one-line prep doc per meeting that just says "prep manually").

### STEP 4 — Tasks for today

```
# TODO: plug in your task source here
#
# Options:
#   - Apple Reminders via osascript
#   - Todoist via mcp__zapier__todoist_*
#   - Linear via API
#   - Plain text file at ~/today.md that you maintain manually
#   - Skip this step entirely
#
# Example (Todoist):
#   mcp__zapier__todoist_make_api_get_request URL: "https://api.todoist.com/rest/v2/tasks?filter=today"
```

### STEP 5 — Weather

```bash
curl -s "wttr.in/${YOUR_CITY}?format=3"
# Example output: "Dallas: 🌦 +72°F"
```

Or use a Perplexity / Web search call for a more detailed forecast.

### STEP 6 — Compose

Markdown-formatted Telegram message:

```
☀️ *Morning Brief — {weekday} {date}*

*Weather:* {weather one-liner}

*Today's calendar:*
• 09:00 — {title} — {attendees} — [prep: [[YYYYMMDD-name]]]
• 11:30 — {title} — {attendees}
• 14:00 — {title}

*Tomorrow at a glance:*
• {first event}, {second event}

*Urgent email:*
• {sender}: {subject}
• {sender}: {subject}

*Today's tasks:*
• {task 1}
• {task 2}
```

### STEP 7 — Send

Use the `reply` MCP tool with `chat_id` from `USER.md`. End the sub-agent with `BRIEF_OK <timestamp>` on success, `BRIEF_PARTIAL <timestamp>: <what was missing>` on partial failure.

### STEP 8 — Log to memory

Append a one-line entry to `memory/YYYY-MM-DD.md`: `06:30 — Morning brief sent. {N} meetings, {N} urgent emails flagged.`

## Failure handling

If any step errors (gmail auth, calendar unavailable, etc.), continue with what you have. Flag gaps at the bottom: "⚠️ Calendar unavailable this morning." Never exit silently — the user expects a 6:30am message.
