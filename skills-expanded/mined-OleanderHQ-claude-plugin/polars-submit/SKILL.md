---
name: polars-submit
description: >-
  Runs Polars queries or scripts on oleander via the CLI, in local or
  distributed mode, and saves results to the lake catalog. Use when
  writing Polars jobs, choosing query vs script mode, using --save /
  --distributed, or wiring scan()/params/result contracts.
---

# Polars Submit

Use this skill when running Polars on oleander from the CLI, choosing between query and script mode, or deciding whether to use distributed compute.

For shared catalog conventions such as naming and namespaces, also use `lake-catalog`.

## CLI query mode

Use query mode for quick SQL-style exploration:

```bash
oleander polars "select * from events limit 10" \
  --table events=my_namespace.events
```

In query mode, pass each source table with `--table`. Use `alias=namespace.table` when the SQL should refer to a short name like `events`.

## CLI script mode

Use script mode for idiomatic Polars logic:

```bash
oleander polars --script ./job.py \
  --param table=my_namespace.events \
  --param limit=100
```

Script mode is the default choice when the work is easier to express with the Polars DataFrame API than with SQL.

## Script contract

oleander injects the runtime pieces for you. In script mode, these are already available:

- `pl`
- `catalog`
- `scan(table)`
- `params`

Your script must assign `result` to a Polars `LazyFrame` or `DataFrame`.

Good:

```python
table = params.get("table", "default.my_table")

result = (
    scan(table)
    .filter(pl.col("value") > 0)
    .group_by("category")
    .agg(pl.len().alias("rows"))
)
```

Avoid:

- calling `.collect()` yourself
- calling `.remote()` yourself
- handling credentials in the script

## Table identifiers

For oleander Polars examples, pass table identifiers as `namespace.table` strings such as `default.sf_311` or `analytics.daily_metrics`.

- In `scan(table)`, use `namespace.table`
- In `--table alias=...`, use `namespace.table`
- In `--save`, use `namespace.table`

The catalog is selected separately with `--catalog` and defaults to `oleander`.

## Saving results

Use `--save` when the result should be written to the lake catalog:

```bash
oleander polars --script ./job.py \
  --param table=default.sf_311 \
  --save analytics.top_rows \
  --save-mode overwrite
```

Use `overwrite` when replacing the full result. Use `append` for incremental writes.

## Distributed mode

Use distributed mode only for large workloads:

```bash
oleander polars --script ./job.py \
  --param table=default.sf_311 \
  --distributed \
  --save analytics.large_result \
  --save-mode overwrite
```

Distributed runs write results to the lake catalog and are better for large jobs where startup cost is worth it.

## Quick guidance

- Prefer query mode for simple SQL-style reads, joins, and filters.
- Prefer script mode for reusable Polars transformations.
