---
name: xunit-v2-v3-migration
description: Use when upgrading xUnit test assets from v2 to v3 requires deterministic compatibility checks, migration sequencing, and risk-controlled rollout decisions.
---

# xUnit v2 to v3 Migration

## Specialization

Use this skill to plan and validate risk-controlled migration from xUnit v2 to v3 across repositories.

This skill is specialized for migration planning and compatibility evidence.

## Objective

Produce one deterministic migration contract with compatibility checks, phased rollout sequencing, and explicit go/no-go criteria.

## Trigger Conditions

- Repository still uses xUnit v2 and needs modernization.
- Mixed v2/v3 assumptions cause tooling or runner confusion.
- Teams need cross-project migration consistency and rollback posture.

## Scope Boundaries

In scope:

- Dependency and tooling compatibility mapping.
- Breaking-change risk assessment and sequencing.
- Phased migration and rollback checkpoints.
- Migration evidence and gate criteria.

Out of scope:

- Full code implementation of migration changes.
- Non-xUnit framework migration.
- CI provider infrastructure redesign.

## Inputs

- Current package versions and runner adapters.
- Target runtime and SDK constraints.
- Test suite scale and risk classification.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Compatibility and blocker matrix.
- Phased migration sequence with checkpoints.
- Rollback and contingency plan.
- Migration gate criteria and final recommendation.

## Deterministic Workflow

1. Inventory current xUnit packages, adapters, and runner integrations.
2. Build compatibility matrix against target v3 posture.
3. Identify breaking-change risks and categorize by severity.
4. Define phased rollout with measurable checkpoints.
5. Define rollback triggers and owner responsibilities.
6. Publish migration recommendation with unresolved blockers.

## Decision Rules

- No migration phase starts without compatibility evidence for that phase.
- Rollback plan must be executable without in-flight context.
- Fail closed when critical blockers remain unresolved.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Expert migration planning | Deterministic Workflow |
| Deterministic compatibility gating | Decision Rules + Required Outputs |
| Risk-controlled rollout | Required Outputs |
| Cross-project portability | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Most migration failures come from hidden compatibility dependencies.
- Phased rollout reduces blast radius and improves confidence.

Trade-offs:

- Conservative phased rollout lowers risk but increases elapsed migration time.
- Fast cutover reduces time but increases rollback pressure.

Open blockers:

- Unknown plugin/adapter dependencies may block full v3 adoption.
- Incomplete test telemetry can hide regression signals.

Recommendation:

- Use a phased, evidence-first migration with explicit rollback criteria at every checkpoint.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Migration planning checklist is provided in [migration-checklist.md](./references/migration-checklist.md).

## Pragmatic Stop Rule

Stop when compatibility blockers are mapped, phased gates are explicit, and rollback posture is validated.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Migration and rollback decisions are explicit.
- Source catalog is current for this evaluation cycle.
