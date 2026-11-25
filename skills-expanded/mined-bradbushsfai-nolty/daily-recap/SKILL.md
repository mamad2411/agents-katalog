---
name: daily-recap
description: Daily 9pm wrap-up — task reconciliation, sent emails, Zoom transcripts, Obsidian summary, Telegram report. EXAMPLE — adapt to your own setup.
---

# Daily Recap (example)

> **EXAMPLE — adapt to your own setup.**

You are Nolty running the Daily Recap.

If you see `[cron model:X effort:Y]` suffix, spawn a Task sub-agent with that model + effort.

## Procedure

### STEP 1 — What got sent today (email)

```bash
/opt/homebrew/bin/gog gmail search "in:sent newer_than:1d" --limit 20 --account YOUR_EMAIL@example.com --json
```

Note the count + a one-line summary of each thread you initiated or replied to. Anything significant (proposal sent, contract signed, hard-thing-said) gets a line in the recap.

### STEP 2 — Today's calendar (what actually happened)

```bash
/opt/homebrew/bin/gog calendar list --today --account YOUR_EMAIL@example.com --json
```

Filter to events that ended (now > event end time). For each, note: title + attendees. Flag anything cancelled or moved.

### STEP 3 — Zoom transcripts (if available)

If you use Zoom and have transcript access:

```
# TODO: plug in your transcript source
# Options:
#   - mcp__zapier__zoom_get_meeting_summary
#   - Local download of .vtt transcripts
#   - Skip if not applicable
```

For each transcribed meeting, write a 3-bullet summary to YOUR_OBSIDIAN_VAULT/MeetingNotes/YYYYMMDD-{title}.md.

### STEP 4 — Tasks reconciliation

```
# TODO: plug in your task source
# Pull tasks completed today + tasks deferred to tomorrow + still-open count.
```

### STEP 5 — Compose

Markdown Telegram message (under 1500 chars):

```
🌙 *Daily Recap — {weekday} {date}*

*Sent:* {N} emails
{1-line summary of significant ones}

*Meetings completed:* {N}
{1-line summary of each significant one}

*Tasks:* {completed_count} done, {deferred_count} deferred to tomorrow, {open_count} still open

*Tomorrow:*
First meeting at {time} — {title}
{N} more events scheduled

Notes saved: YOUR_OBSIDIAN_VAULT/MeetingNotes/
```

### STEP 6 — Send

`reply` MCP tool with `chat_id` from `USER.md`. End with `RECAP_OK <timestamp>` (success) or `RECAP_PARTIAL <timestamp>: <missing>` (degraded).

### STEP 7 — Log to memory

Append a one-line entry to `memory/YYYY-MM-DD.md`: `21:00 — Daily recap sent. {summary}`.

## Failure handling

Send a best-effort recap via `reply` with gaps flagged. Don't exit silently — user expects a 9pm message.
