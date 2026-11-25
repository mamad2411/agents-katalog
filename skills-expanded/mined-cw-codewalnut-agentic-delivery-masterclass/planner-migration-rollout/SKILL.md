---
name: planner-migration-rollout
description: Use when a plan changes data, interfaces, configuration, deployment order, or rollback behaviour.
---

# Plan migration, rollout, and rollback

## Inputs
Impact map, delivery slices, consumers, data/interface changes, operational constraints, and existing deployment practices.

## Procedure
1. Classify each change as backward-compatible, coordinated, destructive, or no migration.
2. Define expand/migrate/contract order, mixed-version compatibility, and the coexistence window.
3. Specify backfill identity, batching, restartability, validation, failure handling, and reconciliation.
4. Define rollout controls, health signals, abort thresholds, and operator ownership.
5. Separate code rollback from data/state reversal; name irreversible effects and compensating actions.
6. Record prerequisites and executable proof for every transition.

## Output
A migration, compatibility, rollout, and rollback plan, or an explicit `not_applicable` record with rationale.

## Stop condition
Stop for unknown consumers, non-restartable backfill, destructive work without recovery, missing abort signals, or a rollback that would violate accepted business state.
