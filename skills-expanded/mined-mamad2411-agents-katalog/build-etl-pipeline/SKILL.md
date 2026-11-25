---
name: build-etl-pipeline
description: Designs and implements ETL/ELT pipelines — extract from sources, transform/normalize, load to a warehouse — with idempotency, incremental loads, scheduling, and orchestration patterns.
when_to_use: When the user wants to build or refactor a data pipeline that moves data between systems — ingest from API/DB/files, transform and load into a warehouse, set up incremental/CDC loads, or structure an Airflow/dbt-style orchestration. Distinct from one-off tabular wrangling: use this for scheduled, multi-source, repeatable pipelines.
---

## When to Use

Use when the work is a **repeatable, scheduled flow** that moves data from one or more sources into a sink/warehouse — not a one-off transform of a single file. Signals: "ingest from the API every hour", "incremental load", "CDC", "backfill", "dedup on load", "Airflow DAG", "dbt models", "the nightly job".

If it's a single ad-hoc clean/reshape of one dataset with no schedule, that's tabular wrangling, not this skill.

## Steps

1. **Pin the contract before writing code.** Lock down per source: format (JSON/CSV/Parquet/DB rows), grain (one row = ?), natural/business key, and the timestamp you'll use for incrementality (`updated_at`? event time? ingestion time?). Lock down per sink: target table, primary/unique key, partition column, and SLA (freshness target + max runtime). Write these as a short table — every later decision hangs off it.

2. **Choose extraction mode per source — don't default to full reload.**
   - **Full snapshot**: small/dimension tables, no reliable change marker. Reload whole table each run.
   - **Incremental (watermark)**: source has a monotonic `updated_at`/`id`. Store last successful high-watermark in a state table/file; next run pulls `WHERE updated_at > :watermark`. Advance the watermark **only after the load commits**, never at extract time.
   - **CDC**: high-volume mutable tables where you need deletes/updates. Consume a log (Debezium/WAL/binlog) or a change-tracking table; map `op = c/u/d` to upsert/delete.
   - Always pull with **overlap** (`>=` watermark minus a small lag window, e.g. 5–15 min) to catch rows committed out of clock order, then rely on idempotent load to dedup.

3. **Make extract resumable and bounded.** Paginate/chunk by key range or time window, not `OFFSET` (offset drifts under concurrent writes). Cap page size. Persist a per-window cursor so a crash resumes mid-source instead of restarting from zero. Land raw extracts to a staging/bronze layer first (immutable, partitioned by load date) before any transform — this is your replay buffer.

4. **Transform in a staging layer with explicit schema mapping.** Normalize types and timezones (store UTC). Apply: dedup (keep latest by key + version/`updated_at`), surrogate keys (hash of natural key — stable across reloads, e.g. `md5(coalesce(cols))`), and schema mapping source→target column by column (no `SELECT *` into the warehouse). Handle **late-arriving data**: dimensions arriving after facts → either staging buffer + retry, or an "unknown" placeholder key you backfill later. Keep transforms deterministic so the same input always yields the same output (required for idempotency).

5. **Load idempotently — every run must be safe to re-run.**
   - Prefer `MERGE`/upsert keyed on the business/surrogate key, or **partition-overwrite** (delete-then-insert the affected partition in one transaction). Never bare `INSERT` from an at-least-once source — it duplicates on retry.
   - Wrap delete+insert per partition in a transaction so a failure leaves the partition fully old, never half-loaded.
   - For append-only event sinks, dedup by a unique event id (`INSERT ... ON CONFLICT DO NOTHING`).
   - **Backfill = the same load path with a date-range param**, not a separate script. Backfill one partition/day at a time so reruns and forward jobs share idempotency guarantees.

6. **Orchestrate with idempotent tasks and explicit deps.** Model as a DAG: `extract → stage → transform → load → validate`. Each task must be retry-safe in isolation. Set bounded retries with exponential backoff + jitter. Make tasks **parameterized by execution window** (the run's logical date), so a backfill of an old date hits exactly that partition. In Airflow, key off `execution_date`/`data_interval`, not `now()`. In dbt, use incremental models with a unique_key and `is_incremental()` filter. Set `max_active_runs` per DAG to avoid two runs racing the same watermark.

7. **Isolate failures and observe.** Route bad rows to a **dead-letter / quarantine** table (with raw payload + error reason) instead of failing the whole batch — but fail loudly if the dead-letter rate crosses a threshold. Emit per-run metrics: rows in/out, rejected count, watermark advanced from→to, runtime. Add freshness + row-count + null-key assertions as a post-load `validate` task that fails the run (e.g. dbt tests, Great Expectations, or plain `SELECT` checks).

## Common Errors

- **Watermark advanced before load committed** → on crash you skip rows permanently. Advance watermark only in the success path, after the load transaction commits.
- **Non-idempotent reload (bare INSERT) on an at-least-once source** → duplicates on every retry. Use MERGE/upsert or partition-overwrite; key on business/surrogate key.
- **Half-loaded partition** → reader sees old+new mixed, sums wrong. Delete+insert the partition inside one transaction; don't insert then separately delete.
- **`OFFSET`-based pagination under concurrent writes** → rows skipped or doubled as the table shifts. Paginate by key/time range with a stored cursor.
- **No overlap window on incremental pull** → rows committed slightly out of order (clock skew, long transactions) are missed forever. Re-pull a small lag window each run; idempotent load absorbs the overlap.
- **Schema drift breaks the load silently** → new/renamed/dropped source column. Validate the incoming schema against expected and fail (or quarantine) on mismatch; never `SELECT *` into the warehouse.
- **Orchestrator uses `now()` instead of the run's logical date** → backfills land in the wrong partition and reruns aren't reproducible. Parameterize every task by execution window.
- **Late-arriving dimensions create orphan facts** → fact rows point to a key the dim doesn't have yet. Use placeholder/unknown keys + a backfill pass, or buffer-and-retry.
- **One bad row kills the whole batch** → no progress until manual fix. Dead-letter the row, continue, alert on rate.

## Verify

Run these checks before declaring done — show output, don't assert "it works":

1. **Idempotency**: run the same window twice; row counts and key aggregates are identical the second time (no growth, no dups). `SELECT key, count(*) FROM target GROUP BY key HAVING count(*) > 1` returns zero rows.
2. **Incrementality**: confirm watermark/state advances only on success — kill the job mid-load, rerun, verify no rows lost and none duplicated.
3. **Backfill = forward path**: backfill one historical partition and confirm it produces the same shape as a live run for that date.
4. **Failure isolation**: inject a malformed row; verify it lands in dead-letter and the run still completes (or fails only if over threshold).
5. **Validation gate**: confirm the post-load assertions (freshness, row count, null-key) actually fail the run when violated — break one deliberately and watch it red.
6. **Schema drift**: add/rename a source column in a fixture; confirm the pipeline fails or quarantines instead of loading garbage.
