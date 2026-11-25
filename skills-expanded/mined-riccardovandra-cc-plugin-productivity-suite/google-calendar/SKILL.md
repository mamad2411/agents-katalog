---
name: google-calendar
description: Read and create Google Calendar events. View today's schedule, upcoming events, and create new events. Use when user asks about calendar, schedule, meetings, or availability.
---

# Google Calendar Skill

Read and manage Google Calendar events.

## Quick Start

```bash
# View today's events
uv run scripts/today.py

# View this week
uv run scripts/today.py --week

# Create an event
uv run scripts/create.py --title "Meeting with client" --start "2025-12-21 14:00" --duration 60

# Update an event's time
uv run scripts/update.py --id EVENT_ID --start "2025-12-21 15:00"

# Update an event's description
uv run scripts/update.py --id EVENT_ID --description "New meeting notes"
```

## Available Operations

| Operation | Script | Description |
|-----------|--------|-------------|
| Today | `today.py` | View today's/tomorrow's/week's events |
| Create | `create.py` | Create a new calendar event |
| Update | `update.py` | Update event time or description |

## First-Time Setup

This skill uses the shared Google OAuth integration.

```bash
# Add calendar scope to existing OAuth
cd .claude/integrations/google/scripts
python oauth_setup.py --add-scope calendar.events
```

See [SETUP.md](modules/SETUP.md) for detailed instructions.

## Activation Triggers

- "what's on my calendar", "my schedule today"
- "what meetings do I have"
- "create a calendar event", "schedule a meeting"
- "block time for...", "add to calendar"
- "update meeting time", "reschedule event", "change event time"
- "update event description", "modify calendar event"
- Any mention of "calendar", "schedule", "meeting"

## Output

Events are displayed in a simple format:
```
Today's Events (3):
--------------------------------------------------
  09:00  Team standup
  14:00  Client call
         @ Zoom
  16:30  Focus time - writing
```

## Dependencies

- `google-api-python-client`
- `google-auth-oauthlib`
- `python-dateutil` (for flexible date parsing)
