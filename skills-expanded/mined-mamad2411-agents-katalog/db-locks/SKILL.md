---
name: db-locks
description: "Investigate blocking, deadlocks, long transactions, and contention. Use for transaction blocking/deadlock diagnosis; backend-concurrency designs application consistency, and db-migrate designs a lock-safe rollout."
---

# db-locks

Investigate blocking, deadlocks, long transactions, and contention.

## Choose this workflow

Use for transaction blocking/deadlock diagnosis; backend-concurrency designs application consistency, and db-migrate designs a lock-safe rollout.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Databases methods](../../references/packs/database.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; engine, time window, affected workload, and lock/session metadata.

**Pack prerequisites:** Actual engine/version, schema/migrations, query workload, and explicitly identified environment. Prefer supplied plans, metadata, and isolated fixtures. Even a SELECT can lock, call mutating functions, or overload a database; inspect semantics before execution. Executing an analyzed query is distinct from reading its plan.

- **Infer from evidence:** Read engine/version, ORM/runner, schema and migration history from project artifacts before choosing SQL.
- **Reasonable default:** Prepare local SQL and isolated fixtures without assuming production size, locks or recovery guarantees.
- **Ask only when needed:** Ask for environment, downtime or recovery constraints before live/destructive execution when missing; unavailable production access does not block migration files.

Declared evidence requirements: `database.context`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Blocking chains, deadlocks, transaction duration, and contention causes.

No source changes in inspect/plan. Save only requested planning artifacts. fix applies an accepted code repair; operational changes need their own exact request.

## Execute

1. Correlate wait and blocker snapshots with transaction age, query identity and application transaction boundaries.
2. Follow the root blocker rather than the noisiest victim, distinguish transient waits from persistent contention, and propose targeted remedies.

## Technical method

- **Inspect:** Inspect blocking chain, lock modes, transaction age, statements and isolation on the exact database.
- **Method:** Find the root blocker and conflicting access order; consider shorter transactions, consistent ordering or bounded retries against the invariant.
- **Avoid misdiagnosis:** The busiest blocked query may be a victim; terminating a session is an operational mutation with rollback consequences.
- **Check the result:** Reproduce the interleaving with separate isolated connections and verify bounded recovery, not merely lower observed lock counts.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Databases worked example](../../references/examples/database.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).

## Decision branches

- **When the reported deadlock already resolved:** Separate historical deadlock analysis from current blocking and avoid terminating unrelated live sessions.

## Deliver and verify

- Blocking chain or timeline with snapshot time, transaction boundary, likely cause and safe operational or code remedies.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- The root blocker is distinguished from downstream victims; a completed deadlock is not confused with current blocking.

## Stop and recover

- No session termination, transaction cancellation, or timeout changes implicitly. Redact sensitive query parameters and acknowledge snapshot limitations.

## Example requests

- **Normal (inspect):** Explain the blocking chain from these session and lock snapshots.
- **Edge (inspect):** Diagnose an idle transaction blocking several otherwise fast updates.
- **Blocked (inspect):** Analyze a saved lock snapshot without cancelling sessions or changing timeouts.
