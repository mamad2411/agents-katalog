---
name: data-incremental
description: "Implement checkpoints, deduplication, and incremental processing. Use for replay-safe CDC or watermark processing; data-backfill handles bounded historical ranges."
---

# data-incremental

Implement checkpoints, deduplication, and incremental processing.

## Choose this workflow

Use for replay-safe CDC or watermark processing; data-backfill handles bounded historical ranges.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Data engineering methods](../../references/packs/data.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; source change mechanism, stable keys, watermark/checkpoint, late-data policy, and destination semantics.

**Pack prerequisites:** Data source/version, schema/semantics, transformation code, permitted sampling scope, and storage/compute budget. Prefer aggregates and redacted samples; never upload datasets to external services implicitly. Record time zones and snapshot identity for reproducibility.

- **Infer from evidence:** Inspect schema, source snapshot, transformation code, grain, time zones and permitted sample scope.
- **Reasonable default:** Use bounded synthetic or supplied samples when full data is unavailable; keep unknown values distinct from zero.
- **Ask only when needed:** Resolve ambiguous entity/grain/time semantics before reconciliation or backfill; obtain missing data/compute limits only for the dependent scan or execution.

Declared evidence requirements: `data.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Incremental updates, deduplication, deletes, and resume behavior.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Define event versus arrival order, stable keys, deletions, overlap and late-arrival handling.
2. Define the checkpoint transaction and persist checkpoints only after durable effects so replay is safe.
3. Test crashes on both sides of the write/checkpoint boundary.

## Technical method

- **Inspect:** Identify ordering key, watermark meaning, late arrival bound, change/delete events and deduplication identity.
- **Method:** Use a stable tie-breaker and explicit overlap/reconciliation window; preserve progress only after durable output.
- **Avoid misdiagnosis:** A maximum event timestamp alone skips equal-timestamp rows and late arrivals; updates and tombstones need semantics.
- **Check the result:** Test tied timestamps, late corrections, deletes, duplicate deliveries and restart at a batch boundary without missing or duplicating results.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Data engineering worked example](../../references/examples/data.md).


## Decision branches

- **When late updates fall behind the current watermark:** Use an explicit overlap/reconciliation policy rather than silently skipping them.

## Deliver and verify

- Incremental processor with its watermark/key protocol and state format, and replay, late-update, deletion and crash tests.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Replaying a completed window does not duplicate effects; late updates and deletions follow documented rules.

## Stop and recover

- Do not advance checkpoints before durable output. Missing stable identity or change semantics requires a design decision before implementation.

## Example requests

- **Normal (apply):** Implement checkpointed updates that handle late records and deletion events.
- **Edge (apply):** Process late corrections while safely replaying the previous hour.
- **Blocked (inspect):** Review incremental design without stable source identity; identify the blocking semantic gap.
