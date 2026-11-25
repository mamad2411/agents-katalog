---
name: schedule
description: Creates scheduled or recurring tasks that fire automatically on a cadence or on-demand. Make sure to use this skill whenever the user says schedule [task], set this to run [daily/weekly/monthly], remind me to [thing] on [date], create a recurring task, automate [thing] every [interval], cron-style schedule, set a daily/weekly/monthly job, or describes wanting any task to fire on a time-based trigger rather than on user prompt. Useful for security automation (scheduled scans, weekly compliance evidence collection, quarterly cert rotation reminders, vendor renewal alerts), recurring operational checks, and personal-cadence reminders. Do NOT use for: complex incident response procedures (use runbook), one-off task tracking (use productivity:task-management), full daily briefings (use personal-assistant which has briefing scheduled built in), or scheduling calendar events with people (use calendar tools directly). Defining characteristic: "the task fires on a time trigger, not a user prompt."
---

# Schedule

Creates scheduled or recurring tasks that fire on time triggers.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| You want a task to fire automatically on a schedule | Documenting a procedure to be run by a human → `runbook` |
| The trigger is time-based, not prompt-based | Tracking a single task to do once → `productivity:task-management` |
| Output is a scheduled/recurring job specification | You want a daily morning brief → `personal-assistant` (has built-in briefing) |
| Cron-like or human-readable cadence | Scheduling a meeting with a person → calendar tool directly |

## Schedule patterns this skill handles

### Security automation schedules

Common cadences for cybersec/dev founder use:

| Task | Cadence | Notes |
|---|---|---|
| Vulnerability scan triage | Weekly (Mon AM) | Pull last week's findings, group by severity, draft response |
| Access review | Quarterly | Pull IdP user list, flag for managers to confirm |
| Cert/key rotation reminder | 30 days before expiration | Surface from cert inventory |
| Vendor renewal alerts | 90 days before contract expiration | Cross-reference legal:vendor-check data |
| Backup restoration test | Monthly | Trigger DR drill runbook |
| MFA enforcement audit | Monthly | Pull anyone without MFA, draft reminder |
| Compliance evidence sweep | Monthly (last week) | Collect evidence per ongoing controls |
| Sub-processor refresh check | Quarterly | Verify list still accurate |
| Pen test scheduling | Annually | Surface ~120 days before due |
| SOC 2 fieldwork prep | Twice (90d + 30d before) | Trigger preparation runbook |

### Operational schedules

| Task | Cadence | Notes |
|---|---|---|
| Weekly metrics review | Mondays | Pull last week's KPIs |
| Monthly board prep | Last week of month | Draft board update |
| Quarterly roadmap review | Quarter start | Trigger roadmap-update skill |
| Annual compliance program review | January | Full program audit |

### Personal/founder schedules

| Task | Cadence | Notes |
|---|---|---|
| Daily morning brief | 7 AM weekdays | Already covered by personal-assistant |
| End-of-day recap | 8 PM weekdays | Already covered by personal-assistant |
| Weekly priority review | Friday PM | What got done, what carries over |
| Monthly retrospective | Last weekday | Reflection prompt |

## Schedule specification format

Every scheduled task this skill produces includes:

```yaml
name: descriptive-task-name
trigger:
  type: cron | interval | event
  expression: "0 9 * * MON"   # cron syntax for "9 AM every Monday"
  timezone: America/Puerto_Rico
action:
  description: "What runs when the trigger fires"
  skill_to_invoke: <skill-name> (optional)
  inputs: { ... }
output:
  destination: email | dashboard | slack | log
  format: brief | full | structured
failure_handling:
  on_missed_run: catch-up | skip | alert
  on_action_failure: retry-3x | alert | quiet-fail
notification:
  who: [list of recipients]
  when: [success | failure | both]
```

## Cron syntax cheat sheet

```
* * * * *
| | | | |
| | | | +--- Day of week (0-7, Sunday is 0 or 7)
| | | +----- Month (1-12)
| | +------- Day of month (1-31)
| +--------- Hour (0-23)
+----------- Minute (0-59)
```

Common patterns:
- `0 7 * * 1-5` — 7 AM weekdays
- `0 0 1 * *` — midnight on the 1st of every month
- `0 0 * * 0` — midnight every Sunday
- `*/15 * * * *` — every 15 minutes
- `0 9 1,15 * *` — 9 AM on the 1st and 15th of every month
- `0 9 * * 1#1` — 9 AM on the first Monday of every month (extension, not POSIX)

## Anti-patterns

- **Scheduling without an owner** — scheduled tasks rot; assign a human reviewer
- **Catch-up storms** — if a system was down for a week, do you really want all missed runs to fire at once?
- **Silent failures** — set up failure alerting, not just success
- **Drift over time** — review schedules quarterly; outdated tasks waste compute and attention
- **Time-zone bugs** — always specify TZ explicitly; never rely on server TZ
- **Conflicting schedules** — two tasks both trying to update the same resource at 9 AM Monday will collide

## Output

Produces:
1. The schedule specification in YAML
2. Equivalent cron expression
3. Recommended owner + review cadence
4. Failure handling strategy
5. Notification strategy
6. Suggested follow-up: "schedule this monitoring runbook to verify the schedule itself runs reliably" (meta but useful)
