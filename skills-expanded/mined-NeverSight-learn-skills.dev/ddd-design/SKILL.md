---
name: ddd-design
description: Derive aggregate, consistency, transaction, and integration boundaries from event-storming output. Use when shaping domain-driven design before code structure decisions.
---

# ddd-design

## What it does

`ddd-design` narrows `/event-storming` output into aggregates, boundaries, consistency, transaction, and integration decisions.

It does not choose packages, modules, persistence, or framework wiring; those choices belong to `codebase-design`.

## Inputs

- Product Spec
- `CONTEXT.md`
- related ADRs
- event-storming output

## Process

1. Read the Product Spec and domain guidance.
2. Review the event-storming result: actors, commands, events, policies, and external systems.
3. Group the flow into aggregate candidates and boundary candidates.
4. Decide consistency, transaction, and integration boundaries only as far as the design needs them.
5. Ask one question at a time if a stakeholder perspective is still missing.
6. Hand off structure-level decisions to `codebase-design`.

## Connection

- `event-storming` exposes the business flow and domain shape.
- `ddd-design` turns that flow into DDD boundaries and invariants.
- `codebase-design` turns the DDD shape into module and seam decisions.

## Output shape

- Aggregate boundaries are described through entity identity relationships.
- Domain behavior is expressed as domain methods or domain services.
- Policies remain design facts that later become unit-testable behavior.

## Completion

- The design is concrete enough to implement.
- The established vocabulary is not destabilized.
- Remaining structural questions are deferred to `codebase-design`.
