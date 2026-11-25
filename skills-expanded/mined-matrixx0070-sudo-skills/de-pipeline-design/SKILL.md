---
name: de-pipeline-design
version: 1.0.0
description: Design an ETL/ELT data pipeline end to end — sources, transforms, load pattern, SLAs, and idempotency.
author: matrixx0070
tags: [data-engineering, pipeline, etl, elt, ingestion]
capabilities: []
---

# de-pipeline-design

## When to use

Use this when you must move data from one or more sources into a warehouse or lake and decide how: extract cadence, transform placement, load strategy, and the reliability guarantees around them. This is the blueprint you write before any code.

**Not for:** modeling the destination schema (use de-data-modeling), writing the transform SQL (use de-dbt-transform), scheduling the run graph (use de-orchestration), or defining validation checks (use de-data-quality).

## Method

1. **Inventory each source.** For every source record: system, format, volume/day, change rate, and how you detect change (CDC log, updated_at, full snapshot, event stream). Decision point: no reliable change key means you extract full snapshots, not incrementals.
2. **Choose ETL vs ELT.** If the warehouse is powerful (Snowflake/BigQuery/Redshift) and raw data is cheap to land, prefer ELT — load raw, transform in-warehouse. Choose ETL only when you must mask/PII-strip before landing or the target cannot scale transforms.
3. **Pick the load pattern per table:** full refresh (small/dimension), incremental append (immutable events), or incremental merge/upsert (mutable records with a key). State the merge key and the watermark column.
4. **Make it idempotent.** Every run must produce the same result if re-run for the same window. Use deterministic partition overwrite or MERGE keyed on a natural/surrogate key — never blind INSERT.
5. **Define SLAs.** Freshness (data no older than X), completeness (all partitions present), and latency budget. Decision point: sub-minute freshness pushes you to streaming; hourly/daily stays batch.
6. **Design failure handling:** retries, dead-letter for bad records, and a documented backfill procedure keyed on the same watermark.

## Example

Source: an orders Postgres table, ~2M rows/day, mutable, `updated_at` present.

```
Pattern:   ELT, incremental MERGE
Extract:   WHERE updated_at > {last_watermark}  (overlap 1h for late writes)
Land:      raw.orders_staging (append, partitioned by extract_date)
Load:      MERGE into warehouse.orders ON order_id
           WHEN MATCHED THEN UPDATE  WHEN NOT MATCHED THEN INSERT
Watermark: max(updated_at) persisted only after successful MERGE
SLA:       freshness < 2h, run hourly
```

Re-running yesterday's window re-MERGEs the same keys with no duplicates — idempotent.

## Pitfalls

- Blind INSERT with no key, so a retried run doubles rows.
- Advancing the watermark before the load commits, silently dropping a window on failure.
- One giant transform coupling all sources, so one bad source blocks every table.
- Extracting with a hard `>` boundary and no overlap window, missing late-arriving updates.

## Output format

```
Pipeline:   <name>  | Pattern: ETL|ELT  | Cadence: <freq>
Sources:    <system → format → volume → change-detection>
Load:       <table → full|append|merge → key → watermark col>
Idempotency:<how re-runs stay safe>
SLA:        freshness <X> | completeness <rule> | latency <budget>
Failure:    retries <n> | dead-letter <where> | backfill <command/window>
```
