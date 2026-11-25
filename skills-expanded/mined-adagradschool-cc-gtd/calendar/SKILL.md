---
name: calendar
description: Pull Google Calendar context into the GTD system — read events, surface fixed commitments and open blocks, and (only when asked) create/move time-block events. Use when planning the day or week, checking the schedule, syncing calendar.md, or time-blocking a task. Invoked by /daily and /weekly.
allowed-tools: mcp__claude_ai_Google_Calendar__list_events, mcp__claude_ai_Google_Calendar__list_calendars, mcp__claude_ai_Google_Calendar__create_event, mcp__claude_ai_Google_Calendar__update_event, mcp__claude_ai_Google_Calendar__delete_event
---

# /calendar

Pull Google Calendar context into the GTD system using the Google Calendar MCP tools.

Uses the connected Google Calendar MCP server (tools named `mcp__*_Google_Calendar__*`).

## Process

### 1. Read the Calendar
- Use `list_events` on the primary calendar for the relevant window:
  - `/daily` → today (00:00 → 24:00 local)
  - `/weekly` → the upcoming 7 days
- Use `list_calendars` first if you need a non-primary calendar.

### 2. Surface Context for Planning
- Summarize fixed commitments (meetings, appointments) with start/end times
- Identify open blocks of time available for focus work and task time-blocking
- Flag conflicts, back-to-back stretches, and travel/buffer needs

### 3. Create / Update Events (only when asked)
- Time-block a task: `create_event` with `summary`, `startTime`, `endTime` (full ISO 8601), optional `timeZone`
- Reschedule or adjust: `update_event`
- Never create, move, or delete events automatically — only when I explicitly ask.

### 4. Keep calendar.md in Sync
- `calendar.md` mirrors the recurring daily skeleton and dated commitments for the GTD side.
- When the recurring blocks change in Google Calendar, re-sync the skeleton table in
  `calendar.md` and update the "Last synced" date.

## Notes
- Times are interpreted in my primary calendar's time zone unless I specify otherwise.
- This skill provides calendar **context** for `/daily` and `/weekly`; task content lives in Todoist via the `/todoist` skill.
