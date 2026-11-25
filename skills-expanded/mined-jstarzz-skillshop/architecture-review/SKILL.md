---
name: architecture-review
description: "Challenge architecture for unnecessary complexity, coupling, failure modes, ownership ambiguity and operational burden. Use when architecture proposal, system design review, new services or queues."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "architecture"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Architecture Review

Challenge architecture for unnecessary complexity, coupling, failure modes, ownership ambiguity and operational burden.

## Activate when

- architecture proposal
- system design review
- new services or queues

## Focus

- Primary mission: Challenge architecture for unnecessary complexity, coupling, failure modes, ownership ambiguity and operational burden.
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
- A result that directly satisfies: Challenge architecture for unnecessary complexity, coupling, failure modes, ownership ambiguity and operational burden.

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
