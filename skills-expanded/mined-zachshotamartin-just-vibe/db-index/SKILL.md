---
name: db-index
description: "Recommend indexes based on queries, write costs, and measurements. Use for workload-specific index design; db-schema handles broader constraints and data shape."
---

# db-index

Recommend indexes based on queries, write costs, and measurements.

## Choose this workflow

Use for workload-specific index design; db-schema handles broader constraints and data shape.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Databases methods](../../references/packs/database.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; actual queries/plans, schema/indexes, write workload, engine, and storage constraints.

**Pack prerequisites:** Actual engine/version, schema/migrations, query workload, and explicitly identified environment. Prefer supplied plans, metadata, and isolated fixtures. Even a SELECT can lock, call mutating functions, or overload a database; inspect semantics before execution. Executing an analyzed query is distinct from reading its plan.

- **Infer from evidence:** Read engine/version, ORM/runner, schema and migration history from project artifacts before choosing SQL.
- **Reasonable default:** Prepare local SQL and isolated fixtures without assuming production size, locks or recovery guarantees.
- **Ask only when needed:** Ask for environment, downtime or recovery constraints before live/destructive execution when missing; unavailable production access does not block migration files.

Declared evidence requirements: `database.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Evidence-based index design, redundancy, and rollout; no automatic production DDL.

No source changes in inspect/plan. Save only requested planning artifacts. db-migrate applies an accepted index change.

## Execute

1. Match equality, range and order predicates and their selectivity to existing indexes.
2. Estimate write and storage cost from evidence, and design the before/after measurement on the exact workload and an online-creation strategy where supported.

## Technical method

- **Inspect:** Inspect real predicates, ordering, selectivity, existing index definitions and write volume.
- **Method:** Choose key order, covering/partial options and rollout method using supported engine behavior and measured plans.
- **Avoid misdiagnosis:** More indexes increase write/storage cost; an index on a low-selectivity column may not improve the actual workload.
- **Check the result:** Compare read plans/latency and representative write cost; verify validity after online/concurrent creation before declaring completion.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Databases worked example](../../references/examples/database.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).

## Decision branches

- **When an existing index shares the proposed name:** Inspect definition and validity before reuse; an IF NOT EXISTS notice is not a compatibility check.

## Deliver and verify

- Candidate index definition with the workload it supports, redundant overlap, a measured validation plan and a rollout proposal for db-migrate.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Target query improves under comparable conditions; added write cost and redundant indexes are considered.

## Stop and recover

- Do not recommend indexes from column names alone. Unsupported online operations or lock risks must be addressed before execution.

## Example requests

- **Normal (plan):** Recommend indexes from these query plans, including write and storage costs.
- **Edge (plan):** Design an index for a tenant-filtered timeline with a stable secondary sort key.
- **Blocked (inspect):** Assess indexing from schema without plans or workload counts; label performance estimates unknown.
