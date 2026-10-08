---
name: google-calendar-tool
description: >-
  A Google Calendar integration tool. It retrieves and creates event lists via the Calendar API using OAuth2.
  Use when: Use when: checking schedules, creating new events, modifying schedules, or needing calendar synchronization.
tags: [calendar, google, schedule, external]
---


# Google Calendar Tool

An external tool that directly operates Google Calendar events via OAuth2.

## How to Invoke

**Bash**: Run with `animaworks-tool google_calendar <サブコマンド> [引数]`

## List of Actions

### list — Retrieve Event List
```bash
animaworks-tool google_calendar list [-n 20] [-d 7] [--calendar-id primary]
```

| Parameter | Type | Default | Description |
|-----------|-----|-----------|------|
| max_results | integer | 20 | Maximum number of results to retrieve |
| days | integer | 7 | How many days ahead to retrieve |
| calendar_id | string | "primary" | Calendar ID |

### add — Add Event
```bash
animaworks-tool google_calendar add "会議" --start 2026-03-04T10:00:00+09:00 --end 2026-03-04T11:00:00+09:00
```

| Parameter | Type | Required | Description |
|-----------|-----|------|------|
| summary | string | Yes | Event title |
| start | string | Yes | Start time (ISO8601 or YYYY-MM-DD) |
| end | string | Yes | End time (ISO8601 or YYYY-MM-DD) |
| description | string | No | Detailed description |
| location | string | No | Location |
| calendar_id | string | No | Calendar ID (default: primary) |
| attendees | array | No | List of attendee email addresses |

## CLI Usage

```bash
animaworks-tool google_calendar list [-n 20] [-d 7] [--calendar-id primary]
animaworks-tool google_calendar add "会議" --start 2026-03-04T10:00:00+09:00 --end 2026-03-04T11:00:00+09:00
```

## Notes

- OAuth2 authentication flow is required on first use
- Place credentials.json in ~/.animaworks/credentials/google_calendar/
- For all-day events, specify start/end in YYYY-MM-DD format
