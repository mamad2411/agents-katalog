---
name: spec-to-plan
description: Use when converting a product spec, use case, or PRD into a concrete implementation plan before code changes.
---

# Spec To Plan

## Workflow

1. Read `AGENTS.md` and the relevant spec.
2. Inspect current code, docs, examples, and tests that the spec would affect.
3. Identify ownership boundaries, data shapes, API signatures, UI states, permission rules, and validation needs.
4. Create `plans/PLAN_<NAME>.md`.
5. Include concrete implementation details, not only task steps.
6. Include a Mermaid diagram for flow, state, ownership, or rollout when useful.
7. Do not edit implementation files until the plan is accepted or clearly ready to execute.

## Plan Must Include

- goal and non-goals
- files to change
- data models or schemas
- APIs or function signatures
- error handling and permission enforcement
- test strategy
- docs/spec updates
- rollout and backout notes

## Output

Return the plan path, assumptions, unresolved questions, and validation strategy.
