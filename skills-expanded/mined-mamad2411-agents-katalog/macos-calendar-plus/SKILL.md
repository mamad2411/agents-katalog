---
name: macos-calendar-plus
description: Create, list, update, and manage macOS Calendar events with location and URL support via AppleScript. Use when the user asks to add a reminder, schedule an event, create a calendar entry, set a deadline, list upcoming events, update an existing event, or anything involving Apple Calendar on macOS. Triggers on requests like "remind me in 3 days", "add to my calendar", "schedule a meeting next Monday at 2pm", "create a recurring weekly event", "add event at [place/address]", "show my events this week", "update the meeting URL", "add these events to calendar". Supports batch creation, multi-day all-day events, event URLs, and location (street address format — look up addresses from place names before creating). macOS only.
license: MIT
compatibility: Requires macOS with Calendar.app. Uses osascript (AppleScript) and python3 for JSON parsing.
metadata:
  author: axot
  version: "2.0.0"
  based_on: lucaperret/agent-skills@macos-calendar v1.2.0
  openclaw:
    os: macos
    emoji: "\U0001F4C5"
    requires:
      bins:
        - osascript
        - python3
---

# macOS Calendar Plus

Manage Apple Calendar events via `$SKILL_DIR/scripts/calendar.sh`. All date handling uses relative math (`current date + N * days`) or `iso_date` to avoid locale issues.

## Confirmation workflow (MANDATORY)

Before executing ANY calendar command(s), present the user with a summary of planned actions and **wait for explicit confirmation**.

**Single event:**
> Adding to **Family** calendar:
> - 📅 Team sync — 2026-05-01 14:00 (60 min) @ 4-2-8, Shibakoen, Minato, Tokyo
>
> Proceed?

**Multiple events (batch):**
> Adding 5 events to **Work** calendar:
> 1. Sprint planning — 2026-05-04 (all day)
> 2. Design review — 2026-05-05 (all day)
> 3. Team standup — 2026-05-06 10:00 (15 min)
> 4. Demo day — 2026-05-07 15:00 (60 min)
> 5. Retro — 2026-05-08 16:00 (45 min)
>
> Proceed?

**Update:**
> Updating on **Work** calendar:
> - Sprint planning (2026-05-04) → set URL
>
> Proceed?

Only execute after the user confirms ("yes", "go ahead", "proceed", "do it", "y", etc.).

## Quick start

### List calendars

Always list calendars first to find the correct calendar name:

```bash
"$SKILL_DIR/scripts/calendar.sh" list-calendars
```

### List events

```bash
echo '{"calendar":"Work","from_date":"2026-05-04","to_date":"2026-05-08"}' | "$SKILL_DIR/scripts/calendar.sh" list-events
```

JSON fields:

| Field | Required | Description |
|---|---|---|
| `calendar` | no | Calendar name (all calendars if omitted) |
| `from_date` | yes | Start of range `YYYY-MM-DD` |
| `to_date` | yes | End of range `YYYY-MM-DD` |

### Create an event

```bash
echo '<json>' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

JSON fields:

| Field | Required | Default | Description |
|---|---|---|---|
| `summary` | yes | - | Event title |
| `calendar` | no | first calendar | Calendar name (from list-calendars) |
| `description` | no | "" | Event notes |
| `location` | no | "" | Event location — **street address only** (see "Location rules") |
| `url` | no | "" | Event URL (ticket link, meeting link, etc.) |
| `offset_days` | no | 0 | Days from today (0=today, 1=tomorrow, 7=next week) |
| `iso_date` | no | - | Absolute date `YYYY-MM-DD` (overrides offset_days) |
| `iso_end_date` | no | - | End date for multi-day all-day events `YYYY-MM-DD` (requires `all_day: true`) |
| `hour` | no | 9 | Start hour (0-23) |
| `minute` | no | 0 | Start minute (0-59) |
| `duration_minutes` | no | 30 | Duration |
| `alarm_minutes` | no | 0 | Alert N minutes before (0=no alarm) |
| `all_day` | no | false | All-day event |
| `recurrence` | no | - | iCal RRULE string. See [references/recurrence.md](references/recurrence.md) |

### Batch create

Create multiple events in one call. Input is a JSON **array** of event objects (same fields as create-event):

```bash
echo '[{"summary":"Morning standup","iso_date":"2026-05-04","all_day":true,"calendar":"Work"},{"summary":"Sprint review","iso_date":"2026-05-08","all_day":true,"calendar":"Work"}]' | "$SKILL_DIR/scripts/calendar.sh" batch-create
```

### Update an event

Find an existing event by summary + date and update its fields:

```bash
echo '<json>' | "$SKILL_DIR/scripts/calendar.sh" update-event
```

JSON fields:

| Field | Required | Description |
|---|---|---|
| `find_summary` | yes | Summary of the event to find |
| `find_date` | yes | Date of the event `YYYY-MM-DD` |
| `calendar` | no | Calendar name (searches all calendars if omitted) |
| `new_summary` | no | New title (omit to keep unchanged) |
| `description` | no | New description (omit to keep unchanged) |
| `url` | no | New URL (omit to keep unchanged) |
| `location` | no | New location (omit to keep unchanged) |

## Interpreting natural language

Map user requests to JSON fields:

| User says | JSON |
|---|---|
| "tomorrow at 2pm" | `offset_days: 1, hour: 14` |
| "in 3 days" | `offset_days: 3` |
| "next Monday at 10am" | Calculate offset_days from today to next Monday, `hour: 10` |
| "February 25 at 3:30pm" | `iso_date: "2026-02-25", hour: 15, minute: 30` |
| "every weekday at 9am" | `hour: 9, recurrence: "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"` |
| "remind me 1 hour before" | `alarm_minutes: 60` |
| "all day event on March 1" | `iso_date: "2026-03-01", all_day: true` |
| "summer break Jul 20 – Aug 31" | `iso_date: "2026-07-20", iso_end_date: "2026-08-31", all_day: true` |
| "meeting at Starbucks Shibuya" | Search web for address → `location: "21-6, Udagawacho, Shibuya, Tokyo, Japan"` |
| "dentist at 1-2-3 Nishi-Shinjuku" | Use address directly → `location: "1-2-3, Nishi-Shinjuku, Shinjuku, Tokyo, Japan"` |
| "add this ticket link" | `url: "https://..."` |

For "next Monday", "next Friday" etc: compute the day offset using the current date. Use `date` command if needed:

```bash
target=1; today=$(date +%u); offset=$(( (target - today + 7) % 7 )); [ "$offset" -eq 0 ] && offset=7; echo $offset
```

## Example prompts

**"Remind me to call the dentist in 2 days"**
```bash
"$SKILL_DIR/scripts/calendar.sh" list-calendars
```
Then:
```bash
echo '{"calendar":"Personal","summary":"Call dentist","offset_days":2,"hour":9,"duration_minutes":15,"alarm_minutes":30}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**"Schedule a team sync every Tuesday at 2pm at Tokyo Tower"**
```bash
echo '{"calendar":"Personal","summary":"Team sync","hour":14,"duration_minutes":60,"recurrence":"FREQ=WEEKLY;BYDAY=TU","alarm_minutes":10,"location":"4-2-8, Shibakoen, Minato, Tokyo, Japan"}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**"Block summer vacation Jul 20 – Aug 31"**
```bash
echo '{"calendar":"Personal","summary":"Summer vacation","iso_date":"2026-07-20","iso_end_date":"2026-08-31","all_day":true}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**"Add airport shuttle with this link"**
```bash
echo '{"calendar":"Personal","summary":"Airport shuttle","iso_date":"2026-06-15","hour":14,"minute":30,"duration_minutes":60,"url":"https://example.com/ticket/abc123","location":"1-9-1, Marunouchi, Chiyoda, Tokyo, Japan"}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**"Add all these conference events to Work calendar"** (batch)
```bash
echo '[{"calendar":"Work","summary":"Keynote","iso_date":"2026-06-10","all_day":true},{"calendar":"Work","summary":"Workshop A","iso_date":"2026-06-11","all_day":true},{"calendar":"Work","summary":"Closing party","iso_date":"2026-06-12","hour":18,"duration_minutes":120}]' | "$SKILL_DIR/scripts/calendar.sh" batch-create
```

**"Add the meeting URL to tomorrow's sync event"**
```bash
echo '{"calendar":"Personal","find_summary":"Team sync","find_date":"2026-05-01","url":"https://meet.google.com/abc-def-ghi"}' | "$SKILL_DIR/scripts/calendar.sh" update-event
```

**"What's on my calendar next week?"**
```bash
echo '{"from_date":"2026-05-04","to_date":"2026-05-10"}' | "$SKILL_DIR/scripts/calendar.sh" list-events
```

## Critical rules

1. **Always show confirmation** before executing any command — see "Confirmation workflow" section
2. **Always list calendars first** if the user hasn't specified one — calendars marked `[read-only]` cannot be used for event creation
3. **Never use hardcoded date strings** in AppleScript — always use `offset_days` or `iso_date`
4. **Confirm the calendar name** with the user if multiple personal calendars exist
5. **Never target a `[read-only]` calendar** — the script will reject it with an error
6. **For recurring events**, consult [references/recurrence.md](references/recurrence.md) for RRULE syntax
7. **Pass JSON via stdin** — never as a CLI argument (avoids leaking data in process list)
8. **All fields are validated** by the script (type coercion, range checks, format validation) — invalid input is rejected with an error message
9. **All actions are logged** to `logs/calendar.log` with timestamp, command, calendar, and summary
10. **Location format is strict** — see "Location rules" section below
11. **Use batch-create** for 2+ events — faster and cleaner than individual create-event calls
12. **iso_end_date requires all_day: true** — multi-day ranges are only for all-day events

## Location rules

The `location` field must be a **street address only**, formatted as:

```
{street/block number}, {area}, {city}, {prefecture}, Japan
```

**Example:** `1-1, Maihama, Urayasu, Chiba, Japan`

**What to strip:**
- Postal codes (e.g. 123-4567)
- Place/brand/venue names (Hilton, Starbucks, etc.)
- Building/floor names (Mori Tower 52F, QFRONT 2F, etc.)

**When the user gives only a place name** (e.g. "Starbucks Shibuya", "Hilton Shinjuku"), search the web — the venue's official site or maps — to find the actual street address before creating the event. Never use a place name as the location value.
