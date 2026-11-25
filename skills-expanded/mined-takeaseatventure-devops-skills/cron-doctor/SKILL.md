---
name: cron-doctor
description: "Diagnose and validate cron expressions before they ship. Catches the five silent death-traps: impossible dates that never fire, OR-semantics that fire too often, midnight spikes, uneven step drift, and leap-year February 29."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-06-26"
author: takeaseat
tags: [cron, crontab, scheduling, devops, debugging, kubernetes, validation]
tools: [claude, cursor, codex, gemini, opencode]
license: "MIT"
---

# cron-doctor

## When to use this skill

Use this skill whenever a cron expression is involved:
- A user is writing or editing a crontab, Kubernetes `CronJob`, GitHub Actions schedule, Airflow DAG, or any scheduled task.
- A user is debugging a job that "didn't fire" or "fired at the wrong time."
- A user asks "what does this cron expression mean?" or "when will this run next?"
- A CI/CD pipeline includes a scheduled trigger that needs validation.

Cron is deceptively error-prone. The failure mode is **silent** — a syntactically valid
expression that simply never fires, or fires far more often than intended. This skill
catches those before they reach production.

## The five cron death-traps

These are the bugs that pass `crontab -l` validation but break in prod:

### 1. Impossible dates — the "never fires" bug
```
0 0 30 2 *
```
**Valid syntax. Never fires.** February has no 30th. This schedule is a dead job that
will silently sit there forever. The same applies to `0 0 31 4 *`, `0 0 31 6 *`,
`0 0 31 9 *`, `0 0 31 11 *` — any day 31 in a 30-day month.

**Fix:** use `0 0 28-31 * *` and check for end-of-month in the script, or use `L`
(last day) syntax if supported.

### 2. OR-semantics — the "fires too often" bug
```
0 0 1,15 * 1
```
**Does NOT mean** "midnight on the 1st and 15th if it's Monday."
**Does mean** "midnight on the 1st, the 15th, **OR** every Monday." That's ~6 fires/month
instead of ~2.

This is the single most misunderstood cron rule. When both day-of-month AND day-of-week
are restricted (not `*`), cron uses OR logic, not AND.

**Fix:** if you need "1st and 15th only if Monday," run daily and check in the script:
```bash
0 0 * * 1 [ $(date +%d) = "01" -o $(date +%d) = "15" ] && your-command
```

### 3. Midnight spike — the "everything at once" bug
```
0 0 * * *
```
Every job scheduled at `0 0` competes for resources at exactly 00:00. Database backups,
log rotations, cert renewals, report generation — all fire simultaneously. This causes
load spikes, connection pool exhaustion, and cascading timeouts.

**Fix:** stagger your jobs across the hour. Use `17 2 * * *` or `43 3 * * *` instead.
Jitter is your friend.

### 4. Uneven steps — the "drift" bug
```
*/7 * * * *
```
**Does NOT mean** "every 7 minutes evenly." It means "every 7 minutes starting at 0,
then resets at 60." So: 0, 7, 14, 21, 28, 35, 42, 49, 56 — then 0 again (3-minute gap).
The intervals drift: 7, 7, 7, 7, 7, 7, 7, 7, **4**.

**Fix:** 60 is not divisible by 7. Use step values that divide 60 evenly: `*/5`, `*/10`,
`*/15`, `*/20`, `*/30`. If you truly need every-7-minutes, use a loop with `sleep 420`.

### 5. Leap-year February 29 — the "annual surprise"
```
0 0 29 2 *
```
Fires only on leap years — February 29, 2024 / 2028 / 2032... If someone writes this
expecting "end of February," they'll be confused for 3 out of every 4 years.

**Fix:** use `0 0 28 2 *` and handle the 29th case in the script if needed.

## How to diagnose a cron expression

When a user provides a cron expression to check:

1. **Parse it.** Split on whitespace into 5 fields: minute, hour, day-of-month, month,
   day-of-week. Validate ranges: minute 0-59, hour 0-23, dom 1-31, month 1-12, dow 0-7
   (0 and 7 both = Sunday).

2. **Describe it in plain English.** What the user *thinks* it does vs. what it
   *actually* does. Be explicit about OR-vs-AND semantics.

3. **Run the trap checklist** above. Flag any of the five death-traps.

4. **Calculate next runs.** Compute the next 5 fire times as concrete dates so the user
   can verify the schedule behaves as expected.

5. **Estimate annual fire count.** A schedule that fires 365 times/year vs. 12 times/year
   is a 30x cost difference. Make this visible.

## Using the validation script

This skill includes a zero-dependency validation engine at
`scripts/cron-engine.js` (638 lines, 69 tests). You can use it programmatically:

```javascript
// Node.js — no install needed, zero dependencies
const { parse, describe, validate, nextRuns } = require('./scripts/cron-engine.js');

// Parse + describe
console.log(describe('0 0 30 2 *'));
// → "At 00:00 on day-of-month 30 in February"

// Deep validation — catches the traps
const result = validate('0 0 30 2 *');
// → { valid: true, warnings: ["February 30 never occurs — this schedule never fires"],
//     observations: [...], runsPerYear: 0 }

// Next 5 fire times
console.log(nextRuns('0 9 * * 1-5', 5, new Date()));
// → [Date, Date, Date, Date, Date]
```

You can also run it from the command line:
```bash
node scripts/cron-engine.js validate "0 0 30 2 *"
node scripts/cron-engine.js describe "*/5 * * * *"
node scripts/cron-engine.js next "0 9 * * 1-5" 5
```

## Common cron presets

| Expression | Description | Use case |
|-----------|-------------|----------|
| `*/5 * * * *` | Every 5 minutes | Health checks, polling |
| `0 * * * *` | Every hour | Hourly aggregation |
| `0 */2 * * *` | Every 2 hours | Semi-frequent sync |
| `0 9 * * 1-5` | 9am Mon-Fri | Business hours task |
| `0 2 * * *` | 2am daily | Off-peak batch (avoid midnight) |
| `0 0 * * 0` | Midnight Sunday | Weekly maintenance |
| `0 0 1 * *` | Midnight 1st of month | Monthly report |
| `0 0 1 1 *` | Midnight Jan 1st | Annual task |

## Always verify

When you help a user with cron, **always** provide the plain-English description AND run
the trap checklist. Don't just say "looks good" — cron's whole danger is that invalid
schedules look valid.
