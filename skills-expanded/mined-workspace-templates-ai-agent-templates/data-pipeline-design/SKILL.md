---
name: data-pipeline-design
description: Designs idempotent, testable batch pipelines with safe backfills and data quality checks. Use it when planning or reviewing a scheduled data job.
---

# Data pipeline design

Design for the rerun. Assume every job will fail midway and be started again.

## Steps

1. Define the contract: source, destination, schedule, the grain of the output, and who consumes it. Write the output schema with types and a unique key.
2. Partition by processing window (usually a date). Each run takes the window as a parameter and never reads "now" or "latest" implicitly.
3. Make writes idempotent: overwrite the partition, or `MERGE`/upsert on the key. Write to a staging location, validate, then swap or publish atomically. Never append blindly.
4. Separate stages: extract (raw, immutable copy), transform (pure functions of raw data), load. Keep transform code free of I/O so it can be unit tested with a tiny fixture.
5. Add quality checks between stages: row count against the source within a tolerance, non-null keys, unique keys, value ranges, and freshness. A failed check stops the run and alerts; it does not warn and continue.
6. Plan late and changed data: reprocess a trailing window (for example 3 days) or key on event time with a watermark.
7. Document the backfill: the command, the date range parameters, the expected runtime, and how to verify afterwards.

## Rules

- No hidden state: no files in local temp directories, no global counters.
- Secrets come from the environment, never from the repo.
- Prefer boring tools already in the stack over a new orchestrator.

## Report

A stage diagram in text, the key and partition choices, the checks with thresholds, the failure modes considered, and the backfill steps.
