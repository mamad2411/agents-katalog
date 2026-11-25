---
name: persian-dates
description: Converts and calculates dates in the Persian (Jalali, Solar Hijri, Shamsi) calendar. Use whenever the user mentions a Jalali, Shamsi or Persian date, month names like فروردین or آبان, years like 1404 or ۱۴۰۵, wants to convert to or from Gregorian, add or subtract days, find the weekday, count days between dates, print a month calendar, or fix a table that mixes calendars, even if they only say "what is this date in the Iranian calendar". Verified against known Nowruz dates.
---

# persian-dates

Convert between Gregorian and Jalali dates reliably, with Persian digits accepted on input and available on output. Standard library only.

```
persian-dates/
├── SKILL.md
├── scripts/
│   └── jalali.py          today, to-jalali, to-gregorian, add, diff, month; importable functions
└── references/
    └── calendar.md        months, weekdays, leap rule, checked reference dates, data advice
```

## When to use

- Converting a date either way between the two calendars
- Adding days, finding the weekday or the distance between dates
- Showing a month calendar
- Cleaning a column that mixes Jalali and Gregorian dates
- Choosing how to store Persian dates in a database

## Workflow

1. **Identify the calendar** of every date. Years around 1300 to 1500 are Jalali, around 1900 to 2100 are Gregorian. If a value is ambiguous, ask.
2. **Convert with the script** instead of mental arithmetic:
   `python3 scripts/jalali.py to-jalali 2026-11-02 --names` gives `دوشنبه 11 آبان 1405`
   `python3 scripts/jalali.py to-gregorian ۱۴۰۵/۰۸/۱۱` gives `2026-11-02`
3. **Calculate** with `add` and `diff`:
   `python3 scripts/jalali.py add 1405-08-11 --days 30`
   `python3 scripts/jalali.py diff 1405-01-01 1405-08-11`
4. **Validate**: the script rejects impossible days such as 31 Mehr or 30 Esfand in a non-leap year (exit code 2).
5. **For bulk data**, import the functions rather than calling the CLI per row:
   ```python
   from jalali import gregorian_to_jalali, jalali_to_gregorian
   gregorian_to_jalali(2026, 11, 2)    # (1405, 8, 11)
   ```
6. **Report** both calendars side by side so the user can check.

## Rules

- Never convert by adding a fixed number to the year; the calendars shift every year
- Store ISO Gregorian dates in data and convert for display; if Jalali must be stored, zero pad and use Western digits
- Say which calendar a date is in whenever you write one
- State the limit: the 33-year rule matches the official calendar for years in everyday use; for legal deadlines near a leap boundary, advise checking an official calendar
- Remember Iran's weekend is Friday, and the week starts on Saturday
- Keep time zones separate: this skill converts dates, not timestamps (Iran is UTC+3:30, with changing daylight saving rules)

## What to report back

| Field | Content |
|-------|---------|
| Input | the date as given, with its calendar |
| Result | both calendars, weekday name |
| Method | script and rule used, plus the limitation if relevant |
| Warnings | ambiguous input, invalid days, leap year edge cases |

## Related skills

- `persian-text-processing`: normalize digits and letters before parsing
- `csv-profiling`: detect mixed date formats in a data file
- `document-conversion`: Persian reports with correct layout
