---
name: fxview-parquet-consumer
description: Consume FXView tick data from Parquet files. Schema, file layout, DuckDB queries, Python/Rust examples.
allowed-tools: Read, Bash, Grep, Glob
---

# FXView Tick Parquet Consumer

Read FXView tick data from Parquet files produced by the MT5 tick collection system.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- Reading or querying FXView tick Parquet files
- Building adapters or pipelines for FXView tick data
- Writing DuckDB queries against tick data
- Integrating tick data into Python or Rust pipelines
- Checking tick data schema or file layout

## Authoritative Source

<https://github.com/terrylica/mql5/blob/05f7c82/docs/tick_research/SCHEMA_VERIFIED.md>

This skill summarizes the verified schema. For full verification details, flags distributions, and row group internals, see the source document.

## Schema

All 6 columns are non-nullable. Schema is identical between EURUSD and XAUUSD files.

| Column   | Arrow Type | DuckDB Type | Nullable | Notes                                         |
| -------- | ---------- | ----------- | -------- | --------------------------------------------- |
| time_msc | Int64      | BIGINT      | NO       | Unix epoch milliseconds                       |
| bid      | Float64    | DOUBLE      | NO       | Bid price                                     |
| ask      | Float64    | DOUBLE      | NO       | Ask price                                     |
| last     | Float64    | DOUBLE      | NO       | Always 0.0 for FXView forex -- IGNORE         |
| volume   | Int64      | BIGINT      | NO       | Always 0 for FXView forex -- IGNORE           |
| flags    | UInt8      | UTINYINT    | NO       | MqlTick flags bitmask (3 values: 4, 130, 134) |

## Parquet Footer Metadata

Key-value pairs embedded in every file footer:

| Key        | Example Value                    | Purpose                               |
| ---------- | -------------------------------- | ------------------------------------- |
| symbol     | EURUSD                           | Bare symbol name (no FXVIEW\_ prefix) |
| digits     | 5 (EURUSD) / 2 (XAUUSD)          | Price decimal digits                  |
| broker     | FXView                           | Broker name                           |
| created_at | 2026-03-24T10:32:35.101090+00:00 | File creation timestamp (RFC3339 UTC) |

## File Layout

**Directory pattern:** `{base_path}/FXVIEW_{SYMBOL}/{YYYY}/{SYMBOL}_{YYYYMMDD}.parquet`

**Example:** `~/.cache/opendeviationbar/ticks/FXVIEW_EURUSD/2026/EURUSD_20260323.parquet`

**IMPORTANT asymmetry:** The directory uses the `FXVIEW_` prefix (broker-qualified), but the filename and metadata use the bare symbol name. Do not mix these up.

**Crash recovery files:** `{SYMBOL}_{YYYYMMDD}_1.parquet`, `_2.parquet`, etc. Created when the EA restarts and finds an existing file for today. All segments are valid, complete Parquet files with footers.

## XAUUSD Differences

| Property          | EURUSD                        | XAUUSD                        |
| ----------------- | ----------------------------- | ----------------------------- |
| digits            | 5                             | 2                             |
| Price scale       | ~1.15                         | ~4400                         |
| Ticks/day         | ~416K                         | ~929K                         |
| last/volume       | Always 0                      | Always 0                      |
| Flag distribution | 53% bid+ask, 24% bid, 23% ask | 98% bid+ask, ~1% each bid/ask |

XAUUSD has ~2.2x higher tick density than EURUSD.

## DuckDB Consumption Examples

### Read a single day

```sql
SELECT * FROM read_parquet('~/.cache/opendeviationbar/ticks/FXVIEW_EURUSD/2026/EURUSD_20260323.parquet');
```

### Read all files for a symbol (glob)

```sql
SELECT * FROM read_parquet('~/.cache/opendeviationbar/ticks/FXVIEW_EURUSD/**/*.parquet');
```

### Convert timestamp to human-readable

```sql
SELECT make_timestamp(time_msc * 1000) AS ts, bid, ask, ask - bid AS spread
FROM read_parquet('~/.cache/opendeviationbar/ticks/FXVIEW_EURUSD/2026/EURUSD_20260323.parquet');
```

### Spread statistics

```sql
SELECT avg(ask - bid) AS avg_spread, max(ask - bid) AS max_spread
FROM read_parquet('~/.cache/opendeviationbar/ticks/FXVIEW_EURUSD/2026/EURUSD_20260323.parquet');
```

### Flags distribution

```sql
SELECT flags, count(*) AS cnt, round(count(*) * 100.0 / sum(count(*)) OVER (), 2) AS pct
FROM read_parquet('...')
GROUP BY flags
ORDER BY cnt DESC;
```

## Anti-Patterns

- Do NOT use `last` or `volume` columns for FXView forex (always zero)
- Do NOT assume `FXVIEW_` prefix in filenames -- it is ONLY in the directory name
- Do NOT use f64 for prices in Rust production code (use i64 fixed-point via digits metadata)
- Do NOT expect time_msc in seconds -- it is MILLIseconds
- Do NOT hardcode machine paths -- use pattern `{base_path}/FXVIEW_{SYMBOL}/{YYYY}/{SYMBOL}_{YYYYMMDD}.parquet`

## Parquet Internals

- **Compression:** ZSTD level 3
- **time_msc encoding:** DELTA_BINARY_PACKED (optimal for monotonic timestamps, dictionary disabled)
- **flags encoding:** Dictionary encoding (low cardinality -- 3 distinct values)
- **bid, ask, last, volume:** Default (PLAIN + ZSTD)
- **Row groups:** ~65,536 rows each (last group has remainder)
- **File size:** ~1.35 MB for ~416K EURUSD ticks/day

## Flags Bitmask Reference

| Value | Meaning                                       |
| ----- | --------------------------------------------- |
| 4     | Ask price changed (TICK_FLAG_ASK)             |
| 130   | Bid changed + first tick marker (2+128)       |
| 134   | Bid+ask changed + first tick marker (2+4+128) |

## Troubleshooting

| Issue                    | Cause                       | Solution                                                      |
| ------------------------ | --------------------------- | ------------------------------------------------------------- |
| No files found           | Wrong base path or symbol   | Check directory pattern with FXVIEW\_ prefix                  |
| All last/volume are zero | Normal for FXView forex     | Ignore these columns for forex pairs                          |
| Timestamp looks wrong    | Using seconds not ms        | time_msc is milliseconds -- multiply by 1000 for microseconds |
| Schema mismatch          | Different broker or version | Verify against SCHEMA_VERIFIED.md permalink                   |
| Multiple files same day  | Crash recovery segments     | All \_N suffixed files are valid, union them                  |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
