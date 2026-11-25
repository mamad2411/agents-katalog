---
name: spec-to-task-plan
description: convert an approved specification into an sdd task plan with waves, task sizes, task categories, required agents, acceptance checks, validation steps and review gates. use when a spec is ready for implementation planning but should not be coded directly yet.
---

# Spec to Task Plan

Use this skill to transform an approved specification into executable waves and tasks.

## Input

Use an approved or mostly stable specification.

## Process

1. Read the spec and identify goals, scope and constraints.
2. Split the work into waves when needed.
3. Split each wave into small tasks.
4. Estimate task size.
5. Assign task category.
6. Identify required agents or specialists.
7. Define acceptance checks and validation steps.
8. Define review gates.
9. Identify dependencies and risks.

## Task size

- `XS`: very small and local.
- `S`: small change in one area.
- `M`: moderate change across more than one concern.
- `L`: large change requiring decomposition.
- `XL`: too large for direct execution; split first.

## Task category

- `standard`
- `XS-doc-only`
- `XS-safe-change`

Use lightweight categories only when risk is clearly low.

## Output format

```md
# Task Plan: <spec title>

## Summary

## Waves

### Wave 1: <name>

#### Task 1.1: <title>

- Size:
- Category:
- Objective:
- Expected result:
- Suggested branch:
- Files or areas:
- Required agents:
- Acceptance checks:
- Validation:
- Gates:
  - review:
  - tests:
  - acceptance:
  - security:
- Risks:
- Dependencies:

## Execution order

## Human review checklist
```

## Rules

- Do not create large vague tasks.
- Do not skip gates.
- Do not plan implementation before scope is clear.
- Mark unknowns explicitly.
