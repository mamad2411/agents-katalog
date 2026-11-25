---
name: factory-retrospective
description: Use after incidents, regressions, repeated review findings, or completed features to convert lessons into durable factory improvements.
---

# Factory Retrospective

## Workflow

1. Identify what happened and what artifact should have caught it.
2. Classify the lesson as product behavior, implementation strategy, current-state knowledge, repeated workflow, or validation gap.
3. Update the right durable surface:
   - product behavior: `specs/`
   - implementation strategy: `plans/`
   - current-state knowledge: `docs/`
   - repeated workflow: `.agents/skills/`
   - validation gap: tests, CI, or checklists
4. Keep the update scoped and copyable.
5. Run `make validate-factory` after artifact changes.

## Output

Return the lesson, updated artifact paths, validation run, and any remaining risk.
