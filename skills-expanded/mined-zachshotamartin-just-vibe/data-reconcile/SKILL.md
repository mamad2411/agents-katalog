---
name: data-reconcile
description: "Compare source and destination records and explain discrepancies. Use to compare corresponding datasets; db-integrity checks database invariants."
---

# data-reconcile

Compare source and destination records and explain discrepancies.

## Choose this workflow

Use to compare corresponding datasets; db-integrity checks database invariants.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Data engineering methods](../../references/packs/data.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; source/destination snapshots, keys, transformations, tolerances, and comparison budget.

**Pack prerequisites:** Data source/version, schema/semantics, transformation code, permitted sampling scope, and storage/compute budget. Prefer aggregates and redacted samples; never upload datasets to external services implicitly. Record time zones and snapshot identity for reproducibility.

- **Infer from evidence:** Inspect schema, source snapshot, transformation code, grain, time zones and permitted sample scope.
- **Reasonable default:** Use bounded synthetic or supplied samples when full data is unavailable; keep unknown values distinct from zero.
- **Ask only when needed:** Resolve ambiguous entity/grain/time semantics before reconciliation or backfill; obtain missing data/compute limits only for the dependent scan or execution.

Declared evidence requirements: `data.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Missing, duplicated, changed, or aggregated discrepancies; no automatic repair.

No source changes in inspect/plan. Save only requested planning artifacts. data-pipeline or fix applies an accepted change.

## Execute

1. Align snapshots or time windows and key grain.
2. Compare membership before values, normalizing only explicitly documented transformations.
3. Sample discrepancies safely and explain likely causes.

## Technical method

- **Inspect:** Align source/destination snapshots, key grain, time window, lag, normalization and delete semantics.
- **Method:** Compare key membership then per-field values with explicit tolerances; isolate legitimate lag from corruption.
- **Avoid misdiagnosis:** Equal counts or totals can hide missing and duplicated rows that cancel out.
- **Check the result:** Use a fixture with equal totals but different membership and verify the report locates discrepancies without exposing sensitive values.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Data engineering worked example](../../references/examples/data.md).


## Decision branches

- **When counts match but keys or values differ:** Quantify each mismatch class and retain redacted examples rather than declaring parity.

## Deliver and verify

- Reconciliation report for the snapshot pair with keyed mismatch categories, denominators, evidence, repair candidates and evidence limits.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Equal row counts do not hide different records; allowed rounding/timing differences are distinguished from loss.

## Stop and recover

- Misaligned snapshots prevent a definitive mismatch claim. No row-level data exposure beyond necessary authorized evidence.

## Example requests

- **Normal (inspect):** Compare these aligned snapshots by key, not just row counts.
- **Edge (inspect):** Reconcile exports with equal row counts but missing and duplicated IDs.
- **Blocked (inspect):** Compare misaligned snapshots without calling timing differences data loss.
