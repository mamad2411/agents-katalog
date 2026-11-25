---
name: thunderbird-calendar
description: Read-only access to Thunderbird/Betterbird calendar data (cached CalDAV). Query upcoming events, search by title/location, find free time slots, and generate .ics files for import. Use when the user asks about their schedule, calendar, availability, events, or appointments.
---

# Thunderbird Calendar Skill

Read-only access to the user's calendar via Thunderbird/Betterbird's local SQLite cache. No API keys, no network access needed -- everything is read from local files.

## When to Use This Skill

Invoke this skill when the user:

- Asks about their **schedule**: "what's on my calendar", "do I have anything today", "what's my week look like"
- Asks about **availability**: "am I free on Monday", "find me a free slot", "when can I schedule a meeting"
- **Searches** for events: "when was my last dentist appointment", "find meetings with X"
- Wants to **create** an event: generate an .ics file they can import into Thunderbird or Google Calendar
- Asks about **upcoming** travel, meetings, appointments, etc.

## Configuration

Config is stored in `pass` (the standard unix password manager) under `thunderbird_calendar/config`.

The entry contains key=value pairs:

```
db=~/.thunderbird/PROFILE/calendar-data/cache.sqlite
calendar_id=CALENDAR_UUID
timezone=Europe/London
```

### Setup (one-time)

```bash
# 1. Find the Thunderbird profile
ls ~/.thunderbird/*/calendar-data/cache.sqlite

# 2. Identify the right calendar ID
cal.py list-calendars

# 3. Store in pass
pass insert -m thunderbird_calendar/config
# Paste the 3 lines above with correct values, then Ctrl+D
```

Environment variable overrides (for testing): `THUNDERBIRD_CALENDAR_DB`, `THUNDERBIRD_CALENDAR_ID`, `THUNDERBIRD_CALENDAR_TZ`.

## Available Commands

The script is at the skill's base directory: `cal.py`

### View events

```bash
# Today's events
cal.py today

# Tomorrow's events
cal.py tomorrow

# This week (Mon-Sun)
cal.py week

# Next N days (default 7)
cal.py upcoming
cal.py upcoming --days 14

# Specific date range
cal.py range --from 2026-03-01 --to 2026-03-15
```

### Search events

```bash
# Search by title, location, or description
cal.py search "dentist"
cal.py search "London"
cal.py search "meeting"
```

### Find free slots

```bash
# Free slots on a specific day (default 09:00-18:00)
cal.py free --date 2026-03-01

# Custom work hours
cal.py free --date 2026-03-01 --start 08:00 --end 20:00
```

### Generate .ics for import

```bash
# Create an .ics file (written to ~/Desktop/ by default)
cal.py ics "Team standup" --start "2026-03-01 10:00" --end "2026-03-01 10:30"

# With location and description
cal.py ics "Dinner" --start "2026-03-01 19:00" --end "2026-03-01 21:00" \
  --location "Le Petit Bistrot" --description "Reservation for 4"

# Custom output path
cal.py ics "Meeting" --start "2026-03-01 14:00" --end "2026-03-01 15:00" \
  --output ~/Desktop/meeting.ics
```

### Setup helper

```bash
# List all calendars in the database (works without config)
cal.py list-calendars

# Specify database path explicitly
cal.py list-calendars --db ~/.thunderbird/PROFILE/calendar-data/cache.sqlite
```

## Important Notes

- **Read-only**: The script never writes to Thunderbird's database. It copies the SQLite file to /tmp before reading to avoid lock conflicts with a running Thunderbird/Betterbird instance.
- **Creating events**: Use the `ics` subcommand to generate standard .ics files. The user can then import these into Thunderbird (File > Import) or Google Calendar.
- **Timestamps**: Thunderbird stores timestamps as microseconds since Unix epoch. The script handles conversion and timezone display automatically.
- **All-day events**: Detected by `floating` timezone and duration being a multiple of 24 hours.

## Dependencies

- Python 3.9+ (uses `zoneinfo` from stdlib)
- `pass` (the standard unix password manager) for configuration
- No external Python packages required -- stdlib only
