---
name: tech-task-generator
description: Expand Sprint Story (+ Tech Story when present) into task files — traceability, regression, no invented scope
model: sonnet-4-6
token_budget: {input: 4000, output: 3000}
---

> **Standards:** [templates/AUTHORING_STANDARDS.md](../../../templates/AUTHORING_STANDARDS.md)

# Tech Task Generator (Atomic)

## Input

- **Sprint Story** (required)
- **Tech Story** (recommended when the sprint slice has architectural / multi-module impact)
- PRD section ids (from parent stories)
- Optional: stack, capacity

## Rules

1. **Traceability:** Each task fills **🔗 Traceability** on `task-template.md`: Sprint Story, Master Story, PRD ids; **Tech Story** when the task maps to technical spec.
2. **No invention:** If the Sprint/Tech story does not name files, APIs, or tests, use `USER_INPUT_REQUIRED`—do not guess.
3. **Regression:** Every engineering task names **regression** coverage (suite, command, or explicit N/A with reason)—aligned with Tech Story **🛡️ Non-regression** when present.
4. **Copy/strings:** Do **not** invent user-visible text; pull from Sprint/Master **📎** sections or PRD.

## Output

One file per atomic task using **`templates/story-templates/task-template.md`**.

## See also

- [templates/AUTHORING_STANDARDS.md](../../../templates/AUTHORING_STANDARDS.md)
- **Sprint:** `skills/shared/sprint-story-generator/`
- **Master:** `skills/shared/story-generator/`
- **Tech story:** `skills/shared/tech-story-generator/`
