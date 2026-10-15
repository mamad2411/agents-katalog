---
name: gsp-implementation-plan
description: "Use when turning an approved game brief into verifiable implementation tasks matched to the chosen build mode."
---

# Game Implementation Plan

Turn the approved build brief into an execution plan.
Use `../../shared/templates/task-plan.md`.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present implementation plan in conversation.
- **minimal** or **full**: write `docs/game-studio/plan.md`.

## Spec-driven compatibility
When `gsp-spec-driven-planning` is active:
- write the implementation plan to `changes/<change-id>/tasks.md`
- keep each task traceable to the requirement or design area it implements

## Key rule
Do not use one default task size for all situations.
Use the chosen development mode.

## Planning bias
- In **yolo-super**, larger end-to-end tasks are allowed and often preferred.
- In **guided-build**, keep the plan comprehensible but still fast.
- In **refactor-open**, plan migrations and replacements explicitly.
- In **surgical-live**, keep tasks tight and rollbackable.

## Execution bias
Unless the user explicitly wants a cheap or minimal pass, assume the plan should support:
- a **builder** stage
- a **reviewer** stage
- a **verifier** stage

For benchmark, showcase, or polished-prototype work, plan with this loop in mind instead of assuming one pass from build to done.

## Important
Do not produce fake progress tasks like “set up scaffolding” unless that scaffold immediately enables real implementation.
Prefer tasks that end in a stronger running build.
