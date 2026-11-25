---
name: notify
description: Send macOS system notifications. Use for pipeline completion alerts, scheduler callbacks, or quick reminders. Use when user asks to notify, send notification, alert, or /notify.
---

# Notify Skill (/notify)

Send macOS system notifications. Useful for pipeline/scheduler completion alerts.

## Quick Start

```bash
python3 _scripts/notify.py "Done" "Daily curation complete"
python3 _scripts/notify.py "Reminder" "Call dentist at 3pm" --no-sound
```

## Options

- `title` — Notification title (required)
- `message` — Body text (optional)
- `--no-sound` — Silent notification

## Use with Scheduler

```bash
python3 _scripts/scheduler.py run --notify
python3 _scripts/scheduler.py wake --notify
```

## Requirements

macOS only (uses osascript).
