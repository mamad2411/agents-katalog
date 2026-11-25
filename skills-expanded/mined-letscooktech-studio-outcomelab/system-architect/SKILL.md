---
name: system-architect
description: Design or review software system architectures with explicit requirements, trade-offs, failure modes, and validation plans. Use for new systems, major integrations, scaling plans, architecture decision records, and technical design reviews.
---

# System Architect

Apply the shared [OutcomeLab skill standard](../../docs/SKILL-STANDARD.md) for evidence, verification, risk, benchmarking, and improvement.

Produce an architecture a team can implement, operate, and reverse when assumptions change.

## Workflow

1. Extract functional requirements, quality attributes, constraints, growth assumptions, and non-goals.
2. Model components, data flows, trust boundaries, dependencies, and ownership. Trace critical paths end-to-end.
3. Compare at least two viable designs where the choice is material; quantify latency, reliability, consistency, cost, and delivery trade-offs.
4. Design failure handling, observability, capacity limits, rollout/rollback, and data migration before selecting a path.
5. Record decisions as reversible or hard-to-reverse, with triggers for revisiting them.

## Output contract

Return a context diagram, component/data-flow design, interface contracts, ADR table, SLOs, capacity assumptions, threat considerations, delivery phases, and validation plan. Label estimates and unknowns.

## Quality gates

- No component exists without an owner, failure behavior, and operational signal.
- No synchronous dependency is added without timeout, retry, idempotency, and fallback reasoning.
- Include a rollback path for every stateful release.
