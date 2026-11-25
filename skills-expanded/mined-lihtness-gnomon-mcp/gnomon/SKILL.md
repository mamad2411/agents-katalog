---
name: gnomon
description: Use the gnomon MCP server's deterministic tools whenever a request depends on the current date/time, involves arithmetic past trivial mental math, mixes timezones, parses natural-language dates, counts business days, or needs unit conversion. Stop next-token-guessing math and time.
---

# gnomon

gnomon-mcp exposes four MCP tools so the model computes deterministically instead of guessing.

## Reach for gnomon whenever the answer involves

- **The current date or time.** Your training cutoff is not today. Call `now`.
- **Elapsed time / time-until / time-since.** Call `calendar` with `diff`, `until`, or `since`.
- **Date arithmetic** (adding days/weeks/months/years, weekday lookups, business days, formatting). Call `calendar`.
- **Natural-language dates** ("next thursday", "in 3 hours", "last friday"). Call `calendar` with `parse`.
- **Arithmetic that matters** — anything past trivial mental math: decimals, percentages, sums over many items, averages, statistics. Call `calc`.
- **Unit conversion** — metric/imperial, temperature, bytes, time durations. Call `calc_convert`. Never eyeball.

## The four tools

### `now(tz?)` — current moment, rich dict

One call returns ISO, date, time, weekday, day_of_year, week_of_year (ISO), quarter, fiscal year (US gov), is_weekend, and more. Optional IANA timezone (defaults to UTC).

```
now()                          → UTC snapshot
now("America/Los_Angeles")     → in a specific tz
```

### `calendar(ops)` — batch date operations

Pass a list of `{"op": NAME, ...args}` dicts, get a list back in order. Use this for table-row workloads — one tool call covers a whole column.

```python
calendar([
  {"op": "until", "target": "2026-12-31", "unit": "days"},
  {"op": "since", "source": "2026-01-01", "unit": "days"},
  {"op": "diff",  "start": "2026-01-01", "end": "2026-12-31", "unit": "days"},
  {"op": "add",   "date": "2026-05-25", "n": 1, "unit": "months"},
  {"op": "weekday", "date": "2026-05-25"},
  {"op": "business_days", "start": "2026-05-01", "end": "2026-06-01"},
  {"op": "parse", "natural": "next thursday", "tz": "America/Los_Angeles"},
  {"op": "format", "date": "2026-05-25", "fmt": "%A, %B %d %Y"},
])
```

Units for `diff`/`until`/`since`: `seconds`, `minutes`, `hours`, `days`, `weeks`.
Units for `add`: above plus `months`, `years` (calendar-aware via `relativedelta`).
`business_days` counts Mon-Fri (`start` inclusive, `end` exclusive); doesn't yet know holidays.

### `calc(expressions)` — batch Python expressions

Pre-loaded: `math` (sqrt, sin, log, pi, e, …), `statistics` (mean, median, stdev, variance), and useful builtins (abs, round, min, max, sum, range, sorted, …).

```python
calc(["sqrt(16)", "mean([1,2,3,4])", "sum(range(101))", "0.075 * 12000"])
```

### `calc_convert(value, from_unit, to_unit)` — Pint unit conversion

```python
calc_convert(100, "meter", "foot")     → 328.08...
calc_convert(0, "degC", "degF")        → 32.0
calc_convert(1, "GiB", "MiB")          → 1024.0
```

## Patterns

- **Batch always.** If you're about to make N similar tool calls, build a list and call once. Both `calendar` and `calc` are list-in, list-out by design.
- **Trust the snapshot.** `now()` returns 18 fields in one call; don't call it three times for ISO + weekday + week-of-year separately.
- **No mental shortcuts.** If you would otherwise "estimate" or "approximately" a date or a number, route it through gnomon instead.

## When NOT to call gnomon

- Counting items in a small list you can see (`len()` in your head is fine for 5 things).
- Quoting a date that's already in the user's message (no math needed).
- One-digit arithmetic (`2 + 2`).

Otherwise — default to gnomon. The cost of one tool call is trivial; the cost of a confidently-wrong number is not.
