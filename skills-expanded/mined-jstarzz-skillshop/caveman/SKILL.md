---
name: caveman
description: "Solve the real problem with the fewest moving parts, dependencies and abstractions that satisfy current requirements. Use when overbuilt architecture, dependency for later, simplify system."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "architecture"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Caveman

Solve the real problem with the fewest moving parts, dependencies and abstractions that satisfy current requirements.

## Activate when

- overbuilt architecture
- dependency for later
- simplify system

## Focus

- Primary mission: Solve the real problem with the fewest moving parts, dependencies and abstractions that satisfy current requirements.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Restate the actual required behavior, scale, availability and security constraints.
2. Inventory every runtime service, queue, cache, datastore, framework, abstraction layer and custom subsystem involved.
3. For each moving part, ask: what concrete requirement or observed failure does this solve today?
4. Try substitutions aggressively: service→module, queue→synchronous call, cache→query, framework→library, class→function, distributed→local, dynamic→static, custom→platform primitive.
5. Keep complexity only when removing it violates a current requirement or creates clearly higher migration cost than the maintenance burden it avoids.
6. Compare operational burden before and after: deployables, failure modes, secrets, networking, monitoring, on-call knowledge and cost.
7. Return the simplest design that still satisfies correctness, security, reliability and credible near-term constraints.
8. Name anything intentionally deferred so future engineers do not mistake omission for ignorance.

## Deliverables

- Recommended design or critique
- Tradeoffs and rejected alternatives
- Complexity/failure/migration notes
- A result that directly satisfies: Solve the real problem with the fewest moving parts, dependencies and abstractions that satisfy current requirements.

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
