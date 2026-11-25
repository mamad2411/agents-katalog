---
name: api-boundary-review
description: "Check service and module boundaries for coherent ownership, stable contracts and avoidable chatty coupling. Use when service split, module boundary, chatty internal API."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "architecture"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Api Boundary Review

Check service and module boundaries for coherent ownership, stable contracts and avoidable chatty coupling.

## Activate when

- service split
- module boundary
- chatty internal API

## Focus

- Primary mission: Check service and module boundaries for coherent ownership, stable contracts and avoidable chatty coupling.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Restate the required capabilities and quality attributes independently of the proposed implementation.
2. Map components, ownership, data flow, synchronous/asynchronous boundaries, and major operational dependencies.
3. Challenge each moving part against a simpler alternative and require a concrete reason for retained complexity.
4. Walk failure, migration, deployment, and maintenance scenarios—not only the happy-path diagram.
5. Identify coupling, irreversible decisions, hidden shared state, and boundaries that will be expensive to move later.
6. Balance present simplicity against credible future change; reject fantasy scale and premature generalization.
7. Return a recommendation with explicit tradeoffs, rejected options, and revisit triggers.

## Deliverables

- Recommended design or critique
- Tradeoffs and rejected alternatives
- Complexity/failure/migration notes
- A result that directly satisfies: Check service and module boundaries for coherent ownership, stable contracts and avoidable chatty coupling.

## Common failure modes

- Architecture astronautics and future-scale theater
- Adding services, queues, caches or frameworks without a concrete requirement
- Big-bang rewrites when an incremental boundary move works
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
