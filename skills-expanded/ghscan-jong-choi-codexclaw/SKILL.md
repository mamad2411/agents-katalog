---
name: time_context
description: Manage Telegram chat timezone and check current time during conversations.
metadata:
  { "openclaw": { "emoji": "🕒" } }
---

# time_context

Use these tools when the user asks about current time, timezone, reminders, or local-time scheduling.

## Tools

`current_time_get`
- Optional `timezone` (IANA) to inspect time in a specific zone.
- Without `timezone`, uses this chat's configured timezone if available.

`timezone_get`
- Returns current chat timezone status and current local/UTC time.

`timezone_set`
- `timezone` (required, IANA): set timezone for this Telegram chat.
- Example values: `Asia/Seoul`, `Europe/London`, `America/New_York`.

## Working rules

- If user asks a local-time operation and timezone is not configured, ask once and call `timezone_set`.
- Prefer explicit timezone confirmation before absolute-time reminders.
- For relative delays ("in 3 minutes"), timezone is not required.
