---
name: broker-schedule
description: Repricing schedule management. Sets the interval for automatic price research and repricing, and registers the system-level scheduler (launchd on macOS, cron on Linux). Use when user wants to set or change the repricing interval, or invoke /broker-schedule to view/manage existing schedules. Default interval: 7 days.
---

# broker-schedule: Repricing Interval & Scheduler

Sets the repricing cycle and registers the system timer that drives automatic price adjustments.

## Workflow

1. Ask user for interval in days (default: 7)
2. Write interval to the listing's state via state_manager
3. Register (or update) the system-level daily check job:
   - macOS: LaunchAgent plist at `~/Library/LaunchAgents/com.skillhub.broker-repricing.plist`
   - Linux: crontab entry

## What the Daily Check Does

1. Scans all active listings
2. For listings whose `next_repricing_date` ≤ today:
   - Search platform prices using stored sessions
   - Calculate new recommended price
   - **Floor validation (MANDATORY GATE)**: If new price < floor → BLOCKED. Repricing paused, user notified, event logged to audit trail.
   - If new price ≥ floor: auto-adjust, log repricing to audit trail.
3. Also checks each listing's status on platform:
   - If found as "sold" on any platform → auto-trigger broker-delist on all others
4. **All decisions logged**: Every repricing, floor block, and delist event is recorded in `~/.broker/audit.jsonl`

## Script

```bash
python3 scripts/schedule.py --item-id <id> --interval 7    # Set interval
python3 scripts/schedule.py --item-id <id> --status         # Check schedule
python3 -m broker_core.scheduler register                   # Register cron/launchd
```
