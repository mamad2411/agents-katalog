---
name: plan-before-code
description: Use when a task requires meaningful implementation. Research the repo, inspect docs/specs, and create a concrete plan before editing code.
---

# Plan Before Code

## Workflow

1. Read `AGENTS.md`.
2. Inspect relevant files, docs, and specs.
3. Identify ownership boundaries and validation requirements.
4. Write `plans/PLAN_<NAME>.md`.
5. Include implementation details:
   - files to change
   - APIs or function signatures
   - data models
   - tests
   - docs/spec updates
   - rollout or migration notes
6. Include a Mermaid diagram when it clarifies flow, ownership, or state.
7. Implement only after the plan is clear.
8. Reconcile the plan if live code contradicts assumptions.

## Output

Return the plan path, key assumptions, validation strategy, and any open questions.
