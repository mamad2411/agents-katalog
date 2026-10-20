---
name: ops-restore
description: "Prepare or validate backup restoration in an appropriate environment. Use for a scoped backup recovery plan or rehearsal; db-migrate changes schema/data intentionally."
---

# ops-restore

Prepare or validate backup restoration in an appropriate environment.

## Choose this workflow

Use for a scoped backup recovery plan or rehearsal; db-migrate changes schema/data intentionally.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Operations methods](../../references/packs/operations.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; backup identity, source system, isolated destination, recovery objectives, and encryption/access prerequisites. A requested rehearsal uses apply mode and writes only to the named isolated destination.

**Pack prerequisites:** Exact service/environment, time window, revision/configuration identity, authorized logs/metrics, and operational constraints. Prefer observation before intervention; live restarts, traffic changes, restores, and notifications require the requested target/action. Redact sensitive telemetry.

- **Infer from evidence:** Read service/environment, time window, revision, available telemetry and existing incident or recovery procedure.
- **Reasonable default:** Start from supplied logs and read-only observation; rank hypotheses without presenting an unexecuted intervention as recovery.
- **Ask only when needed:** Resolve the precise target and missing authority before restart, restore, notification or traffic changes; continue evidence analysis while waiting.

Declared evidence requirements: `project.read`, `database.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Validate restoration and readiness; production replacement requires exact explicit authorization.

Inspect/plan: plan the restore; save requested artifacts only. Apply: restore only into the named isolated destination and run integrity and application checks against it; never overwrite the source system or a shared database. Production replacement requires its exact explicit authorization.

## Execute

1. Verify backup identity, provenance, completeness and keys, and plan destination isolation.
2. Restore into the isolated destination in apply mode.
3. Reconcile schema, counts, integrity and application behavior, and record recovery duration and the data-loss window.

## Technical method

- **Inspect:** Resolve backup identity, encryption access, retention, destination isolation and recovery objectives.
- **Method:** Restore into a verified separate target and validate schema, membership, constraints and application behavior.
- **Avoid misdiagnosis:** A readable archive or backup job success does not prove restoration; testing on production can overwrite current data.
- **Check the result:** Measure restored data cutoff and elapsed recovery, verify integrity and application checks, and retain the failed-step recovery plan.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Operations worked example](../../references/examples/operations.md).
- Restoring a database: consistency, point-in-time recovery and integrity checks: [Database methods](../../references/packs/database.md).

## Decision branches

- **When backup reads successfully but application checks fail:** Treat recovery as incomplete and preserve the isolated target for diagnosis; do not overwrite the live source.

## Deliver and verify

- Restore procedure or exercise report with source/target identities, recovery timing and data-loss window, integrity and application results, and limitations.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Restore succeeds into the intended isolated destination; a readable backup alone does not count as demonstrated recoverability.

## Stop and recover

- Never overwrite live data implicitly. Missing keys, integrity checks, or target identity stops execution before destructive steps.

## Example requests

- **Normal (plan):** Plan restoring the specified backup into an isolated target, not production.
- **Edge (apply):** Rehearse restore into an isolated database with missing recent transactions.
- **Blocked (inspect):** Plan restore with missing decryption keys or an ambiguous destination; do not execute.
