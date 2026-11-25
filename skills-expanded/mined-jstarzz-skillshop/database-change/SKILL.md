---
name: database-change
description: "Design schema changes and deployment order to preserve data, compatibility and availability. Use when schema migration, add column index, database change."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "backend"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Database Change

Design schema changes and deployment order to preserve data, compatibility and availability.

## Activate when

- schema migration
- add column index
- database change

## Focus

- Primary mission: Design schema changes and deployment order to preserve data, compatibility and availability.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Write the domain invariant, contract, or data ownership rule that the backend behavior must preserve.
2. Trace the operation through request validation, authorization, business logic, persistence, external side effects, and asynchronous work.
3. Review transaction, concurrency, idempotency, retry, compatibility, and migration implications where applicable.
4. Prefer database constraints and explicit state models for hard invariants instead of relying only on convention.
5. Exercise failure between meaningful stages and consider ambiguous outcomes such as timeout-after-commit.
6. Measure query/IO behavior when performance is relevant instead of masking pathological access with infrastructure.
7. Return contract/data changes, rollout order, tests, and recovery implications explicitly.

## Deliverables

- Contract/invariant findings
- Data/transaction/concurrency implications
- Tests and rollout/recovery requirements
- A result that directly satisfies: Design schema changes and deployment order to preserve data, compatibility and availability.

## Common failure modes

- External network calls inside long database transactions without justification
- Read-modify-write flows with no concurrency semantics
- Breaking schema/API compatibility without rollout planning
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
