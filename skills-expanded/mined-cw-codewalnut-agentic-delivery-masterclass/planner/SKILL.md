---
name: planner
description: Use when approved intent and ready design need a build plan.
version: 1.0.0
---
# Plan a traceable implementation

## Purpose and boundary
Create a dependency-ordered technical plan. Do not implement, change product policy, or claim feasibility without inspection.

## Inputs
Exact approved PRD, ready design, affected repository/service boundaries, current contracts, engineering standards, deployment constraints, and owners.

## Steps
1. Validate matching input revisions and make a requirement-to-design index.
2. Locate state owners and interface boundaries relevant to the change. Record assumptions instead of broad architecture archaeology.
3. Define invariants: authorization, allowed state transitions, idempotency identity, expected-version behaviour, side effects, and failure atomicity.
4. Select a consistency boundary and explain where it holds. For distributed work, specify durable uniqueness, transaction scope, event publication, crash recovery, and reconciliation.
5. Split the work into dependency-ordered increments. Each task names changed surfaces, requirement IDs, proof command, rollback, and owner.
6. Plan negative, retry, race, migration, compatibility, and observability checks.
7. Review risks and return unresolved product/design questions to their owners.

## Outputs
Impact map, invariants, task sequence, test strategy, risk/migration/rollout/rollback notes, traceability matrix, and `ready_for_build` or `blocked`.

## Stop gates
Stop for stale inputs, unknown state ownership, contradictory interfaces, unbounded migration, no rollback, undefined atomicity, or tasks without observable proof.

## Example
For cancellation, one atomic operation checks request-key reuse, loads the order, verifies owner/version/status, updates status, records the idempotency result, and appends an event. The teaching plan permits one-process locking; the production note requires a database transaction, unique request-key constraint, and transactional outbox.

## Quality check
Every task links backward to intent and forward to a check; race and failure boundaries are explicit; illustrative shortcuts are labelled rather than generalized.
