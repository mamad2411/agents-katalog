---
name: data-pipelines
description: Builds batch and streaming data pipelines that are idempotent, re-runnable and safe to backfill, with incremental loads, late-data handling, schema contracts and data quality gates. Use when writing ETL or ELT jobs, Airflow, Dagster or Prefect DAGs, dbt models, Kafka, Spark or Flink jobs, planning a backfill, or debugging duplicate, missing or stale rows in a warehouse. Not for OLTP schema changes (see database-migrations).
license: MIT
---

# Data Pipelines

Every pipeline task must be safe to re-run: the same inputs produce the same output, with no duplicates and no partial results visible to consumers. Design for the rerun and the backfill from day one, and stop bad data before it is published, not after a dashboard shows it.

## When to use

- Writing ETL/ELT jobs, orchestrator DAGs (Airflow, Dagster, Prefect), dbt models, or streaming jobs (Kafka consumers, Spark Structured Streaming, Flink).
- Planning a backfill or a full refresh.
- Duplicate, missing, late or stale rows in a warehouse or lake.
- An upstream schema change broke a pipeline.

Not for: OLTP schema changes (database-migrations), service-to-service events (event-driven-architecture), or model training workflows (ml-experiments).

## Batch or streaming?

| Freshness needed | Choose |
| --- | --- |
| Hours to daily (reporting, finance, most analytics) | Scheduled batch over time partitions |
| Minutes | Incremental batch or micro-batch |
| Seconds, or reacting to each event | Streaming |

Default to batch. Streaming adds state management, late-data handling and harder reprocessing; pay that cost only when the latency requirement is real.

## Workflow

1. **Define the output contract**: grain ("one row per order per day"), keys, columns and meanings, freshness SLA, consumers, owner, retention.
2. **Define the inputs**: each source, how changes are detected (full snapshot, `updated_at` watermark, change data capture), and how deletes arrive.
3. **Design each task to be idempotent**, parameterized by a partition or time interval (techniques below).
4. **Add quality gates** with write-audit-publish.
5. **Orchestrate**: dependencies, retries, timeouts, concurrency limits, alerts, SLAs.
6. **Test** with fixtures, run the task twice to prove idempotency, and backfill a small range in a non-production environment.
7. **Document lineage and ownership**, and monitor freshness and volume after launch.

## Idempotency techniques

| Technique | How | Notes |
| --- | --- | --- |
| Partition overwrite | The task for date D replaces partition D completely (`INSERT OVERWRITE`, or delete + insert in one transaction, or an atomic partition swap) | Simplest and most robust; needs a partitioned target |
| MERGE / upsert on a key | `MERGE INTO target USING staging ON target.id = staging.id WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT ...` | Supported by most warehouses and PostgreSQL 15+. Deduplicate the staging data first; duplicate source keys cause errors or wrong results |
| Stage and swap | Write to a temporary table or path, validate it, then rename or swap atomically | Consumers never see partial data |
| Dedupe by event ID | Keep the latest row per event ID with `ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY ingested_at DESC) = 1` | Needed for at-least-once sources; use `QUALIFY` where the warehouse supports it, otherwise a subquery |

Rules:

- **Parameterize by the logical interval**, never by the wall clock. Use the orchestrator's interval (for example Airflow's `data_interval_start` / `data_interval_end`, or a Dagster partition key) instead of `now()` or `CURRENT_DATE` inside the logic. Otherwise reruns and backfills compute different results.
- **Plain append is not idempotent.** An `INSERT` without a dedupe key duplicates data on every retry.
- **Be deterministic**: stable tie-breakers in ranking and deduplication, seeded sampling, no dependence on row order.
- **Keep side effects out of transformations.** Emails, API calls and notifications belong in separate tasks guarded by idempotency keys.

## Incremental loads and watermarks

- With an `updated_at` watermark, read `updated_at > last_watermark - overlap` and merge on the key. The overlap covers clock skew and transactions that commit late.
- `updated_at` watermarks miss hard deletes. Use change data capture from the database log (for example Debezium) or a periodic full reconciliation.
- Advance the stored watermark only after the publish step succeeds.
- dbt incremental models: filter with `is_incremental()` and set `unique_key` so reruns merge instead of duplicating. A `--full-refresh` rewrites the whole table; treat it as a backfill and confirm first.

## Late and out-of-order data

- Separate event time (when it happened) from processing time (when it arrived). Partition analytics tables by event time.
- Batch: reprocess a trailing lookback window (the last N partitions) on every run, with N chosen from the lateness you actually observe.
- Streaming: use event-time watermarks and allowed lateness (Flink, Spark Structured Streaming). Send events that arrive too late to a side output or a late-data table instead of dropping them silently.
- "Exactly once" is an end-to-end property. With at-least-once delivery, make the sink idempotent (upsert on event ID) rather than trusting the transport.

## Backfills

- A backfill is the normal idempotent task run for historical partitions. If a backfill needs special code, the task is not idempotent yet.
- Estimate cost and runtime first. Run one partition, validate it against expectations, then run the range with limited concurrency so the source and warehouse are not overloaded.
- Check downstream effects: dependent models that recompute, caches, exports, notifications.
- Backfills and full refreshes overwrite production data. Stop and get explicit confirmation, stating which tables, which partitions and the expected cost.
- Orchestrator backfill commands differ by tool and version (Airflow 2 and Airflow 3 differ, for example). Check the docs for the installed version.

## Schema evolution and contracts

- Agree a contract with each producer: schema, field meanings, SLAs, owner, and how changes are announced.
- For event streams, use a schema registry (Avro, Protobuf or JSON Schema) with a compatibility mode, typically backward compatible.
- Safe changes: adding optional (nullable) fields. Breaking: renames, type changes, removals, and changes in meaning, which are the most dangerous because nothing fails.
- On unexpected schema, fail loudly at ingestion or quarantine the batch. Never silently drop or coerce columns.
- Select explicit columns in transformations instead of `SELECT *`, so new upstream columns don't change outputs or leak sensitive fields.

## Data quality gates (write-audit-publish)

1. **Write** the new data to a staging table or partition.
2. **Audit** it with checks.
3. **Publish** (swap or merge) only if blocking checks pass. Otherwise alert the owner and keep serving the previous version.

| Check | Example |
| --- | --- |
| Volume | Row count within an expected range compared with recent runs |
| Completeness | Required columns are not null |
| Uniqueness | The grain key has no duplicates |
| Validity | Accepted values, ranges, formats |
| Referential integrity | Foreign keys exist in dimension tables |
| Freshness | Newest event time is within the SLA |
| Reconciliation | Totals match the source system |

Mark each check as blocking or warning. Implement with dbt tests (`unique`, `not_null`, `accepted_values`, `relationships`), a data quality tool (for example Great Expectations or Soda), or plain SQL assertions.

Read [references/data-quality-checklist.md](references/data-quality-checklist.md) when adding checks; it has SQL for each check type and guidance on thresholds and alerts.

## Orchestration

- Small tasks with clear inputs and outputs, each retryable on its own.
- Retries with backoff for transient failures only, a bounded retry count, and a timeout on every task.
- Alerts on failure and SLA miss go to the owning team and include a runbook link.
- Limit concurrency against source systems (read replicas, API rate limits).
- In Airflow, keep DAG files light: no database queries or heavy imports at the top level, because the scheduler parses them often.
- Asset- or model-oriented definitions (Dagster assets, dbt models) make lineage explicit; prefer them to opaque scripts.

## PII and governance

- Ingest only the columns you need. Hash or tokenize identifiers when they are used only for joins.
- Tag PII columns and apply column- or row-level access controls in the warehouse.
- Retention and deletion requests must reach derived tables too. Know which tables hold copies.
- Don't copy production PII into development or test environments without approval; use masked or synthetic data.

## Cost and performance

- Prefer incremental processing to full refreshes.
- Filter on partition columns so the engine prunes partitions; cluster or sort on common filter columns.
- Select only needed columns (columnar storage charges by data scanned in many warehouses).
- Compact small files in data lakes.
- Track cost per pipeline and alert on spikes.

## Testing

- Unit-test transformations on small fixture inputs with expected outputs (dbt unit tests in dbt 1.8+, pytest with DataFrames, or SQL run against DuckDB).
- Cover edge cases: empty input, duplicate keys, nulls, late rows, schema drift, and DST or month-end boundaries.
- Idempotency test: run the same partition twice and assert identical results.
- Run against sampled data in a staging environment before the first production run.

## Anti-patterns

- **`now()` inside transformation logic**, so reruns give different answers.
- **Append-only loads without deduplication.**
- **Publishing before validating**, so consumers read bad data.
- **Watermarks without overlap**, silently missing late-committed rows.
- **Ignoring deletes** from sources.
- **`SELECT *` from upstream tables.**
- **Silent schema coercion** instead of failing or quarantining.
- **Unbounded retries**, or retries on logic errors.
- **Backfilling production without a cost estimate or confirmation.**
- **One giant task** that cannot be retried partially.

## Done when

- The output contract (grain, keys, SLA, owner) is written down.
- Each task is parameterized by its interval, and running it twice gives identical results.
- Blocking quality checks gate publishing, and failures alert the owner.
- Late data and deletes are handled explicitly.
- A backfill of a sample range succeeded in a non-production environment.
- Freshness, volume and cost are monitored.

## References

- [references/data-quality-checklist.md](references/data-quality-checklist.md) — read when designing quality checks, thresholds and alerts.
