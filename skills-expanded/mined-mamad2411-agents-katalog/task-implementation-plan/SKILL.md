---
name: task-implementation-plan
description: "Create a low-level implementation design from the architect's and UX designer's specifications."
---

# Implementation Plan Task

## Input
- `docs/designs/{feature-name}.md` (Architect's technical design)
- `docs/ui_spec.md` (UX Designer's interaction and layout design, if applicable)

## Output
- **Implementation Sequence** (ordered by dependency).
- **Granular logic updates** (files and functions).
- **Test Design Strategies** (Unit / Manual).
- **Trade-off Disclosure (MANDATORY)**: Following `project-conventions/resources/templates.md`, you must explicitly document downsides, constraints, or side effects of the implementation.

## Steps
1. Break down the high-level designs into concrete coding tasks.
2. Order the tasks based on module dependencies.
3. Determine the testing strategy for each subtask.
4. **Define Red Teaming Scenarios**: Following `project-conventions/resources/templates.md`, include failure scenarios ("How could this feature break?") in the verification plan.

## MANDATORY GATE: Approval & Questions
- Strictly follow the **"Universal Integrity Gates"** in `project-conventions/SKILL.md`.
- If the plan contains "Open Questions," you must end your turn immediately and wait for user feedback.
