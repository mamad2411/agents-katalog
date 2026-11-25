---
name: data-backfill
description: "Plan or run resumable historical-data backfills. Use for bounded historical reprocessing; data-pipeline creates normal transformation behavior, and a backfill that is a phase of a schema change belongs to db-migrate."
---

# data-backfill

Plan or run resumable historical-data backfills.

## Choose this workflow

Use for bounded historical reprocessing; data-pipeline creates normal transformation behavior, and a backfill that is a phase of a schema change belongs to db-migrate.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Data engineering methods](../../references/packs/data.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan the backfill; apply for requested backfill code or an explicitly scoped data run.

**Pack prerequisites:** Data source/version, schema/semantics, transformation code, permitted sampling scope, and storage/compute budget. Prefer aggregates and redacted samples; never upload datasets to external services implicitly. Record time zones and snapshot identity for reproducibility.

- **Infer from evidence:** Inspect schema, source snapshot, transformation code, grain, time zones and permitted sample scope.
- **Reasonable default:** Use bounded synthetic or supplied samples when full data is unavailable; keep unknown values distinct from zero.
- **Ask only when needed:** Resolve ambiguous entity/grain/time semantics before reconciliation or backfill; obtain missing data/compute limits only for the dependent scan or execution.

Declared evidence requirements: `data.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Resumable historical recomputation; execution requires the specified data/environment authorization.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Estimate volume and partition a fixed source snapshot.
2. Define idempotent writes and checkpoints, and account for concurrent incremental writers.
3. Measure and validate a small permitted batch, reconcile its output, then resume within limits.

## Technical method

- **Inspect:** Define bounded historical range, target revision, batch key, live-writer policy and resource limits.
- **Method:** Make chunks resumable and idempotent; prevent old backfill data from overwriting newer live values.
- **Avoid misdiagnosis:** A successful batch counter does not prove all rows were covered, and retrying non-idempotent transforms can corrupt values.
- **Check the result:** Stop and resume midway while a live update occurs, then reconcile coverage and values at the agreed snapshot boundary.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Data engineering worked example](../../references/examples/data.md).


## Decision branches

- **When a batch fails or load exceeds the cap:** Pause with its partition identity and reconciliation state so resume cannot duplicate or overwrite good output.
- **When the request is for local preparation or implementation:** Implement restartable batches, progress and reconciliation using a local fixture; resolve live target, limits and recovery before modifying existing data.

## Deliver and verify

- Backfill plan or script, or a run record, with partitions, caps, checkpoints, reconciled counts, discrepancies and resume/recovery instructions.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Restart skips or safely replays completed batches; live incremental processing does not race into inconsistent output.

## Stop and recover

- Pause on load/error thresholds. Never launch an unbounded production scan or overwrite historical data without explicit scope.

## Example requests

- **Normal (plan):** Plan a resumable one-year backfill with explicit batch and load limits.
- **Edge (plan):** Plan resuming a backfill while the live pipeline updates the same historical records.
- **Blocked (inspect):** Plan a backfill without production scan permission or known source volume.
