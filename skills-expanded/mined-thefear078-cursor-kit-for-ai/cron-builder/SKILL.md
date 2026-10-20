---
name: cron-builder
description: Explain, generate, validate cron expressions and compute next run times. Use when configuring schedulers, debugging missed jobs, converting natural language schedules, or comparing cron dialects.
---

# Cron Builder

Explain, generate, validate cron expressions and compute next execution times. **Always confirm timezone and cron dialect** — standard 5-field, systemd 6-field, and Quartz 6-7 field crons differ.

## When to Use This Skill

| Trigger | Example request |
|---------|-----------------|
| Explain expression | "What does `0 9 * * 1-5` mean?" |
| Generate from text | "Every weekday at 9 AM" |
| Validate syntax | "Is `60 * * * *` valid?" |
| Next run times | "When does this cron fire next?" |
| Dialect comparison | "Convert to systemd timer" |
| Debug missed jobs | "Why didn't this run on Sunday?" |

## Phase Checklist

```
[ ] 1. Identify cron dialect (standard 5-field, systemd, Quartz, AWS)
[ ] 2. Confirm timezone (UTC vs local — never assume)
[ ] 3. Validate field ranges and special characters
[ ] 4. Explain in plain language
[ ] 5. Compute next N execution times
[ ] 6. Flag ambiguous or dangerous schedules (every minute, Feb 31)
```

---

## Standard 5-Field Cron

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-7, 0 and 7 = Sunday)
│ │ │ │ │
* * * * *
```

### Field Reference

| Field | Range | Special chars |
|-------|-------|---------------|
| Minute | 0-59 | `, - * /` |
| Hour | 0-23 | `, - * /` |
| Day of month | 1-31 | `, - * / ?` |
| Month | 1-12 | `, - * /` |
| Day of week | 0-7 (0=Sun) | `, - * /` |

### Special Characters

| Char | Meaning | Example |
|------|---------|---------|
| `*` | Every value | `* * * * *` = every minute |
| `,` | List | `0 9,17 * * *` = 9 AM and 5 PM |
| `-` | Range | `0 9 * * 1-5` = Mon-Fri at 9 AM |
| `/` | Step | `*/15 * * * *` = every 15 minutes |
| `?` | No specific (Quartz DOM/DOW) | `0 0 ? * MON` |

---

## Explain Expression

```python
# Using croniter (pip install croniter)
from croniter import croniter
from datetime import datetime
import pytz

def explain_cron(expr: str, tz_name: str = "UTC") -> dict:
    tz = pytz.timezone(tz_name)
    now = datetime.now(tz)
    try:
        cron = croniter(expr, now)
    except (ValueError, KeyError) as e:
        return {"valid": False, "error": str(e)}

    next_runs = [cron.get_next(datetime) for _ in range(5)]
    return {
        "valid": True,
        "expression": expr,
        "timezone": tz_name,
        "next_runs": [t.strftime("%Y-%m-%d %H:%M:%S %Z") for t in next_runs],
    }

result = explain_cron("0 9 * * 1-5", "Europe/Kyiv")
print(result)
```

### Plain Language Templates

| Expression | Explanation |
|------------|-------------|
| `0 9 * * *` | Every day at 9:00 AM |
| `0 9 * * 1-5` | Every weekday (Mon-Fri) at 9:00 AM |
| `*/15 * * * *` | Every 15 minutes |
| `0 0 1 * *` | First day of every month at midnight |
| `0 0 * * 0` | Every Sunday at midnight |
| `0 22 * * 1-5` | Weekdays at 10:00 PM |
| `0 9,17 * * *` | Every day at 9:00 AM and 5:00 PM |
| `0 0 1 1 *` | January 1st at midnight (yearly) |
| `@hourly` | Every hour at minute 0 |
| `@daily` | Every day at midnight |
| `@weekly` | Every Sunday at midnight |
| `@monthly` | First of month at midnight |
| `@yearly` | January 1 at midnight |

---

## Generate from Natural Language

### Generation Rubric

| Phrase | Cron | Notes |
|--------|------|-------|
| "every minute" | `* * * * *` | Warn: high frequency |
| "every hour" | `0 * * * *` | Top of hour |
| "every day at 3 AM" | `0 3 * * *` | Confirm timezone |
| "every Monday" | `0 0 * * 1` | Midnight Monday |
| "every 30 minutes" | `*/30 * * * *` | Step syntax |
| "first of month" | `0 0 1 * *` | DOM = 1 |
| "weekdays at noon" | `0 12 * * 1-5` | Mon-Fri |
| "every quarter hour" | `*/15 * * * *` | :00, :15, :30, :45 |

```python
def generate_cron(description: str) -> str:
    """Map common phrases — confirm with user for ambiguous input."""
    mapping = {
        "every minute": "* * * * *",
        "hourly": "0 * * * *",
        "daily at midnight": "0 0 * * *",
        "daily at 9am": "0 9 * * *",
        "weekdays at 9am": "0 9 * * 1-5",
        "weekly on sunday": "0 0 * * 0",
        "monthly on 1st": "0 0 1 * *",
        "every 15 minutes": "*/15 * * * *",
        "every 30 minutes": "*/30 * * * *",
    }
    key = description.lower().strip()
    return mapping.get(key, f"AMBIGUOUS: {description} — please clarify")
```

**Always confirm** generated expression with user before deploying.

---

## Validate Expression

```python
from croniter import croniter
from datetime import datetime

def validate_cron(expr: str) -> dict:
    errors = []

    parts = expr.strip().split()
    if len(parts) != 5:
        errors.append(f"Expected 5 fields, got {len(parts)}")

    # Field range checks (basic)
    ranges = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 7)]
    names = ["minute", "hour", "day-of-month", "month", "day-of-week"]

    for i, (part, (lo, hi), name) in enumerate(zip(parts, ranges, names)):
        if part in ("*", "?"):
            continue
        if part.startswith("*/"):
            try:
                step = int(part[2:])
                if step < 1:
                    errors.append(f"{name}: step must be >= 1")
            except ValueError:
                errors.append(f"{name}: invalid step '{part}'")
            continue
        for val in part.split(","):
            if "-" in val:
                try:
                    a, b = val.split("-", 1)
                    if not (lo <= int(a) <= hi and lo <= int(b) <= hi):
                        errors.append(f"{name}: range {val} out of bounds ({lo}-{hi})")
                except ValueError:
                    errors.append(f"{name}: invalid range '{val}'")
            else:
                try:
                    if not (lo <= int(val) <= hi):
                        errors.append(f"{name}: value {val} out of bounds ({lo}-{hi})")
                except ValueError:
                    pass  # croniter handles names like JAN, MON

    try:
        croniter(expr, datetime.now())
        parseable = True
    except (ValueError, KeyError) as e:
        parseable = False
        errors.append(f"Parse error: {e}")

    return {"valid": len(errors) == 0 and parseable, "errors": errors}

for expr in ["0 9 * * 1-5", "60 * * * *", "0 25 * * *"]:
    result = validate_cron(expr)
    print(f"{expr}: {'✓' if result['valid'] else '✗'} {result.get('errors', [])}")
```

### Common Invalid Expressions

| Expression | Error |
|------------|-------|
| `60 * * * *` | Minute 60 out of range |
| `0 25 * * *` | Hour 25 out of range |
| `0 0 32 * *` | Day 32 invalid (most months) |
| `0 0 31 2 *` | Feb 31 never fires |
| `* * * *` | Only 4 fields (missing one) |

---

## Next Run Times

```python
from croniter import croniter
from datetime import datetime
import pytz

def next_runs(expr: str, count: int = 10, tz_name: str = "UTC", start: datetime = None) -> list[str]:
    tz = pytz.timezone(tz_name)
    base = start or datetime.now(tz)
    if base.tzinfo is None:
        base = tz.localize(base)
    cron = croniter(expr, base)
    return [cron.get_next(datetime).strftime("%Y-%m-%d %H:%M:%S %Z") for _ in range(count)]

print(next_runs("0 9 * * 1-5", count=5, tz_name="Europe/Kyiv"))
```

```bash
# crontab.guru (reference — explain only, don't depend on network)
# Manual verification: compare computed times with user's scheduler
```

---

## Cron Dialects

### Standard (Vixie cron) — 5 fields

```
min hour dom month dow
0 9 * * 1-5
```

### systemd — 6 fields (includes seconds)

```
sec min hour dom month dow
0 0 9 * * 1-5
# OnCalendar syntax alternative:
# Mon..Fri *-*-* 09:00:00
```

### Quartz (Java) — 6-7 fields

```
sec min hour dom month dow [year]
0 0 9 ? * MON-FRI *
# ? = no specific value (DOM or DOW, not both)
# Day names: MON, TUE, ... or 1-7
```

### AWS EventBridge — 6 fields

```
min hour dom month dow year
0 9 ? * MON-FRI *
# Does not support: year field ranges, some special chars
```

### Conversion Notes

| From | To | Change |
|------|-----|--------|
| Standard → systemd | Prepend `0` for seconds field |
| Standard → Quartz | Prepend `0`; use `?` for DOM or DOW |
| `@daily` → standard | `0 0 * * *` |
| Day 0 vs 7 | Both Sunday in standard cron |

---

## Day-of-Week Reference

| Value | Day | Quartz |
|-------|-----|--------|
| 0 | Sunday | SUN |
| 1 | Monday | MON |
| 2 | Tuesday | TUE |
| 3 | Wednesday | WED |
| 4 | Thursday | THU |
| 5 | Friday | FRI |
| 6 | Saturday | SAT |
| 7 | Sunday | SUN |

**Note:** Some systems use 1=Monday (ISO). Standard cron uses 0=Sunday.

---

## Worked Examples

### Example 1: Explain weekday schedule

```
Expression: 0 9 * * 1-5
Timezone:   Europe/Kyiv (UTC+2 / UTC+3 DST)
Meaning:    9:00 AM Monday through Friday
Next runs:  2024-06-17 09:00 EEST (Mon)
            2024-06-18 09:00 EEST (Tue)
            ...
```

### Example 2: Dangerous every-minute cron

```
Expression: * * * * *
Warning:    Runs 1,440 times/day — confirm intentional
Use case:   Monitoring/heartbeat only
Alternative: */5 * * * * for every 5 minutes
```

### Example 3: DOM + DOW interaction

```
Expression: 0 0 15 * 1
Behavior:   Runs on EVERY Monday AND on the 15th of every month
            (both conditions apply — not "15th if Monday")
Note:       Quartz uses ? to avoid this ambiguity
```

---

## Output Template

```markdown
## Cron: {expression}

| Property | Value |
|----------|-------|
| Dialect | Standard 5-field |
| Timezone | UTC |
| Valid | ✓ |

### Plain Language
Every weekday (Monday–Friday) at 9:00 AM.

### Field Breakdown
| Field | Value | Meaning |
|-------|-------|---------|
| Minute | 0 | At minute 0 |
| Hour | 9 | At 9 AM |
| DOM | * | Every day of month |
| Month | * | Every month |
| DOW | 1-5 | Monday through Friday |

### Next 5 Runs (UTC)
1. 2024-06-17 09:00:00 UTC
2. 2024-06-18 09:00:00 UTC
3. 2024-06-19 09:00:00 UTC
4. 2024-06-20 09:00:00 UTC
5. 2024-06-21 09:00:00 UTC
```

---

## Anti-Patterns

- Explaining cron without stating timezone
- Assuming 5-field when user uses Quartz or systemd
- Using both DOM and DOW without explaining interaction
- Deploying `* * * * *` without frequency warning
- Confusing 0 and 7 for Sunday vs Monday-start systems
- Ignoring DST transitions when computing next runs
- Hardcoding UTC when scheduler uses local time

---

## Cross-References

| Related need | Skill |
|--------------|-------|
| Cron in SQL scheduled jobs | `sql-format` |
| Cron in JSON/YAML config files | `format-convert` |
| Server timezone / NTP issues | `network-utils` |
| Encode cron in URL params | `encode-decode` |
| Schedule documentation diff | `text-utils` |
| systemd timer file formatting | `format-convert` |
