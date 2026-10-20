---
name: db-integrity
description: "Find orphaned records, invalid relationships, and missing constraints. Use to check declared invariants in existing data; db-access checks permission policy, db-migrate rolls out an accepted constraint and data-backfill runs a bounded repair."
---

# db-integrity

Find orphaned records, invalid relationships, and missing constraints.

## Choose this workflow

Use to check declared invariants in existing data; db-access checks permission policy, db-migrate rolls out an accepted constraint and data-backfill runs a bounded repair.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Databases methods](../../references/packs/database.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; invariants, schema, data scope, and bounded read permission.

**Pack prerequisites:** Actual engine/version, schema/migrations, query workload, and explicitly identified environment. Prefer supplied plans, metadata, and isolated fixtures. Even a SELECT can lock, call mutating functions, or overload a database; inspect semantics before execution. Executing an analyzed query is distinct from reading its plan.

- **Infer from evidence:** Read engine/version, ORM/runner, schema and migration history from project artifacts before choosing SQL.
- **Reasonable default:** Prepare local SQL and isolated fixtures without assuming production size, locks or recovery guarantees.
- **Ask only when needed:** Ask for environment, downtime or recovery constraints before live/destructive execution when missing; unavailable production access does not block migration files.

Declared evidence requirements: `database.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Orphans, duplicates, invalid relationships, and constraint gaps; no automatic deletion or repair.

No source changes in inspect/plan. Save only requested planning artifacts. db-migrate applies an accepted constraint and data-backfill runs a bounded repair.

## Execute

1. Translate each explicit business invariant into its row, relationship and transaction boundary. Distinguish nullability and historical exceptions from actual corruption; ambiguous policy remains a question, not a deletion rule.
2. Choose bounded counts and redacted examples against an identified snapshot. Assess scan/lock impact before live queries; use supplied artifacts when they are sufficient and do not infer current production state from stale samples.
3. For prevention, propose input validation separately from shared storage constraints and atomic multi-row checks. Cover type/range, ownership, uniqueness, referential rules and overflow where relevant to the invariant.
4. Propose repair with a selection predicate, expected count, restart behavior and recovery boundary; db-migrate or data-backfill applies an accepted change. Detection does not authorize a live cleanup or schema change.

## Technical method

- **Inspect:** Identify claimed invariants, enforcing constraints, existing violation counts and repair ownership.
- **Method:** Use bounded aggregate queries and redacted synthetic examples; separate diagnosis, business reconciliation and constraint rollout.
- **Avoid misdiagnosis:** Automatically deleting orphans can erase legitimate records awaiting asynchronous completion.
- **Check the result:** Verify each invariant with both valid and invalid fixtures and show unresolved real-data policy decisions before any live repair.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Databases worked example](../../references/examples/database.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).

## Decision branches

- **When data violates an ambiguous business rule:** Report the evidence and policy question before proposing deletion or repair.

## Deliver and verify

- Invariant and snapshot, bounded check/count/example evidence, prevention or scoped repair proposal, and uncertainty from missing policy or live data.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Checks detect an actual violating example and accept legitimate null/historical cases. Proposed preventive changes cannot leave partial multi-row state on interruption; repair claims name the snapshot and rows actually verified.

## Stop and recover

- Ambiguous business rules prevent destructive recommendations. Large scans need a budget and appropriate execution environment.

## Example requests

- **Normal (inspect):** Audit orphaned invoice records with bounded read-only checks.
- **Edge (inspect):** Check duplicate business keys while retaining legitimate archived duplicates.
- **Blocked (inspect):** Plan integrity checks on a large table without scan authorization or production row dumps.
