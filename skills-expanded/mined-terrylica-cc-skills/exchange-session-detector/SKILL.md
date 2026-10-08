---
name: exchange-session-detector
description: "DST-aware exchange session detection using exchange_calendars. Holiday & lunch break handling. TRIGGERS - exchange session, trading hours"
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Exchange Session Detector

Production-grade pattern for detecting exchange trading sessions with full DST, holiday, and lunch break support. Validated in `exness-data-preprocess` across 10 global exchanges.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use

- Adding session flags (is_nyse_session, is_lse_session, etc.) to time-series DataFrames
- Detecting whether a timestamp falls within trading hours for any major exchange
- Checking for holidays (NYSE, LSE, or "major" when both are closed)
- Handling lunch breaks for Asian exchanges (Tokyo, Hong Kong, Singapore)
- Upgrading from simplified hour-range checks to production accuracy
- Building ClickHouse materialized columns for session classification

## Architecture Overview

```
ExchangeConfig registry (exchanges.py)     SessionDetector (session_detector.py)
┌──────────────────────────────────┐      ┌──────────────────────────────────────┐
│ 10 frozen dataclasses            │      │ Wraps exchange_calendars library     │
│ ISO 10383 MIC codes              │─────▶│ Pre-computes trading minutes (sets)  │
│ IANA timezones for DST           │      │ Vectorized .isin() lookup (2.2x)    │
│ Local open/close hours           │      │ Holiday detection (NYSE + LSE)       │
└──────────────────────────────────┘      └──────────────────────────────────────┘
```

## Quick Start

```python
import exchange_calendars as xcals
import pandas as pd

# Single-exchange check
cal = xcals.get_calendar("XNYS")  # NYSE via ISO 10383 MIC
cal.is_open_on_minute(pd.Timestamp("2024-07-04 14:30", tz="UTC"))  # False (July 4th)
cal.is_open_on_minute(pd.Timestamp("2024-07-05 14:30", tz="UTC"))  # True

# Full session detection across 10 exchanges
from session_detector import SessionDetector
detector = SessionDetector()
df = detector.detect_sessions_and_holidays(dates_df)
# Adds: is_us_holiday, is_uk_holiday, is_major_holiday, is_{exchange}_session
```

## The Two Tiers of Session Detection

### Tier 1: Simple Hour-Range (What Most Projects Start With)

```python
# Pattern from opendeviationbar-py/ouroboros.py
EXCHANGE_SESSION_HOURS = {
    "sydney":  {"tz": "Australia/Sydney",   "start": 10, "end": 16},
    "tokyo":   {"tz": "Asia/Tokyo",         "start":  9, "end": 15},
    "london":  {"tz": "Europe/London",      "start":  8, "end": 17},
    "newyork": {"tz": "America/New_York",   "start": 10, "end": 16},
}

def is_in_session(session_name, timestamp_utc):
    info = EXCHANGE_SESSION_HOURS[session_name]
    tz = zoneinfo.ZoneInfo(info["tz"])
    local_time = timestamp_utc.astimezone(tz)
    if local_time.weekday() >= 5:
        return False
    return info["start"] <= local_time.hour < info["end"]
```

**What this gets right**: DST conversion via `zoneinfo`, weekend exclusion.

**What this misses**:

- Holidays (Christmas, Thanksgiving, bank holidays)
- Lunch breaks (Tokyo 11:30-12:30, HK 12:00-13:00, SGX 12:00-13:00)
- Half-day / early close sessions
- Sub-hour precision (NYSE opens 9:30, not 10:00; LSE closes 16:30, not 17:00)
- Exchange schedule changes (Tokyo extended to 15:30 on Nov 5, 2024)

### Tier 2: exchange_calendars (Production-Grade)

The `exchange_calendars` library (maintained, pip-installable, 50+ exchanges) handles all of the above automatically via `is_open_on_minute()`. The library uses IANA timezone data internally, so DST transitions are handled correctly without any manual logic.

Read `references/exchange-registry.md` for the full 10-exchange registry with MIC codes, timezones, and open/close hours.

Read `references/session-detector-pattern.md` for the complete SessionDetector implementation pattern with pre-computed trading minutes and vectorized lookup.

## Exchange Registry

10 exchanges are supported via ISO 10383 MIC codes:

| Exchange | MIC Code | Timezone         | Hours (local) | Lunch Break       |
| -------- | -------- | ---------------- | ------------- | ----------------- |
| NYSE     | XNYS     | America/New_York | 09:30 - 16:00 | -                 |
| LSE      | XLON     | Europe/London    | 08:00 - 16:30 | -                 |
| SIX      | XSWX     | Europe/Zurich    | 09:00 - 17:30 | -                 |
| FWB      | XFRA     | Europe/Berlin    | 09:00 - 17:30 | -                 |
| TSX      | XTSE     | America/Toronto  | 09:30 - 16:00 | -                 |
| NZX      | XNZE     | Pacific/Auckland | 10:00 - 16:45 | -                 |
| JPX      | XTKS     | Asia/Tokyo       | 09:00 - 15:00 | 11:30 - 12:30 JST |
| ASX      | XASX     | Australia/Sydney | 10:00 - 16:00 | -                 |
| HKEX     | XHKG     | Asia/Hong_Kong   | 09:30 - 16:00 | 12:00 - 13:00 HKT |
| SGX      | XSES     | Asia/Singapore   | 09:00 - 17:00 | 12:00 - 13:00 SGT |

Adding a new exchange requires only one change: add an `ExchangeConfig` entry to the registry dict. The SessionDetector, schema generation, and column naming all propagate automatically.

## Performance: Pre-Computed Trading Minutes

The naive approach calls `calendar.is_open_on_minute()` per timestamp per exchange — O(N \* E) with high constant factor. The validated pattern pre-computes all trading minutes into sets for O(1) lookup:

```python
# Pre-compute once (startup cost, amortized over millions of lookups)
trading_minutes = detector._precompute_trading_minutes(start_date, end_date)
# Returns: {"nyse": {ts1, ts2, ...}, "lse": {ts1, ts2, ...}, ...}

# Vectorized lookup via pandas .isin() — 2.2x faster than per-row .apply()
df["is_nyse_session"] = df["ts"].isin(trading_minutes["nyse"]).astype(int)
```

The pre-computation itself uses `is_open_on_minute()` internally, so lunch breaks, holidays, and schedule changes are all respected.

## Holiday Detection

```python
# NYSE holidays (excludes weekends — only official closures)
nyse_holidays = {
    pd.to_datetime(h).date()
    for h in calendar.regular_holidays.holidays(start=start, end=end, return_name=False)
}

# Major holiday = both NYSE AND LSE closed
df["is_major_holiday"] = ((df["is_us_holiday"] == 1) & (df["is_uk_holiday"] == 1)).astype(int)
```

## ClickHouse Integration

For server-side session detection (e.g., materialized columns), ClickHouse's `toTimezone()` handles DST automatically when given IANA timezone names:

```sql
-- DST-aware hour extraction (matches Python zoneinfo behavior)
ALTER TABLE my_table
UPDATE is_nyse_session = if(
    toHour(toTimezone(toDateTime(intDiv(close_time_ms, 1000)), 'America/New_York')) >= 9
    AND toHour(toTimezone(toDateTime(intDiv(close_time_ms, 1000)), 'America/New_York')) < 16
    AND toDayOfWeek(toTimezone(toDateTime(intDiv(close_time_ms, 1000)), 'America/New_York')) <= 5,
    1, 0
) WHERE 1 = 1
```

**Limitation**: ClickHouse `toTimezone()` handles DST but not holidays or lunch breaks. For those, compute in Python and write the flags back, or maintain a holiday calendar table in ClickHouse.

## Upgrade Path: Hour-Range to exchange_calendars

1. `pip install exchange_calendars` (or add to `pyproject.toml`)
2. Replace fixed-hour dicts with `ExchangeConfig` registry (see `references/exchange-registry.md`)
3. Replace `zoneinfo` hour checks with `SessionDetector.detect_sessions_and_holidays()`
4. Update tests to cover: holidays, lunch breaks, DST transitions, early closes

The `exchange_calendars` library is ~10MB installed and has no heavy dependencies beyond pandas and numpy. Calendar data is bundled (no network calls at runtime).

## References

| File                                                                    | Content                                                    |
| ----------------------------------------------------------------------- | ---------------------------------------------------------- |
| [exchange-registry.md](./references/exchange-registry.md)               | Full ExchangeConfig registry with frozen dataclass pattern |
| [session-detector-pattern.md](./references/session-detector-pattern.md) | Complete SessionDetector class with pre-computed minutes   |
| [clickhouse-session-sql.md](./references/clickhouse-session-sql.md)     | ClickHouse SQL patterns for server-side session detection  |

## Source

Validated implementation: `~/eon/exness-data-preprocess/src/exness_data_preprocess/session_detector.py` + `exchanges.py`

Simplified predecessor: `~/eon/opendeviationbar-py/python/opendeviationbar/ouroboros.py` (Tier 1 only)

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
