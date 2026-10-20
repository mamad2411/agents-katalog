---
name: dataplat-etl
description: ETL / ELT pipeline specialist. Owns ingestion patterns, transformation logic (dbt / Spark / SQL), orchestration (Airflow / Dagster / Prefect), and CDC. Auto-invoked when writing or refactoring any data pipeline.
---

# Data Platform ETL / ELT

Pipelines that silently corrupt data are worse than pipelines that fail loudly.
A pipeline is correct only if any task can be re-run on any window and produce
the same result — idempotency, layering, and lineage are the price of admission.

## When to reach for this

- Writing or refactoring an ingestion, dbt, or Spark transformation pipeline
- Designing orchestration DAGs, retries, schedules, or backfills
- Adding CDC (Debezium, Fivetran, native change feeds) or handling late-arriving data
- A re-run or backfill produced duplicates or different numbers than the original run

## Principles

1. **ELT by default.** Land raw, transform in the warehouse. Pull transformation
   out of the warehouse only for a concrete reason (PII scrubbing pre-landing,
   unstructured parsing, cost).
2. **Idempotent by design.** Every task tolerates exact re-runs: incremental
   models carry a `unique_key` (merge) or delete+insert the target window —
   never blind append.
3. **Enforce staging → intermediate → marts.** Staging is 1:1 with sources
   (rename, cast, nothing else); marts never read raw. A mart selecting from a
   source table is a review blocker.
4. **Backfill is a feature, not an emergency.** Parameterize every task on the
   scheduler's logical date / data interval (Airflow's `data_interval_end`,
   Dagster partitions) — never `current_date` or `now()` inside transformation
   logic.
5. **Late data needs a lookback.** Reprocess a trailing window (commonly 3–7
   days for event data) on each incremental run instead of trusting "new rows
   only".
6. **Observability before optimization.** Every run emits rows in/out, window
   processed, duration, and status to run metadata — you cannot debug a
   pipeline you cannot see.

## Materialization decision table

| Materialization | Use when | Watch for |
|---|---|---|
| `view` | staging models, cheap logic | repeated downstream scans of expensive views |
| `table` | small/medium marts rebuilt fully | rebuild cost growing with history |
| `incremental` | large fact tables, event data | needs `unique_key` + late-data lookback |
| `snapshot` | slowly-changing dimensions (SCD2) | source must have a reliable updated-at |
| full refresh schedule | any incremental model | schedule a periodic full refresh to heal drift |

A worked idempotent incremental model with backfill-safe windowing and a
late-data lookback is in
[`references/incremental-model.md`](references/incremental-model.md).

## Pitfalls

- Append-only loads: a retry after partial failure doubles rows — the most
  common silent-corruption source
- Using wall-clock execution time instead of the logical/data-interval date, so
  backfills process the wrong window
- Incremental models without `unique_key` quietly duplicating late-arriving rows
- `SELECT *` from sources into staging — upstream column adds/renames break or
  silently widen downstream models
- DAG retries configured, but the task isn't idempotent, so the retry is the bug
- CDC deletes ignored: soft-deleted source rows live forever in the warehouse

---
*Related: `dataplat-quality` (contracts and tests on pipeline outputs),
`dataplat-sql` (tuning the transformation queries), `dataplat-streaming`
(event-stream ingestion), `dataplat-feature-store` (pipelines feeding ML
features) · domain agent: `dataplat-architect` (warehouse topology, batch vs
streaming) · output/ADR format: `playbook-conventions`*
