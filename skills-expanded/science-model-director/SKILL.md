---
name: science-model-director
description: Use when planning or reviewing science, KHTN8, biology, chemistry, physics, or simulation labs for conceptual correctness, causal logic, variable-to-visual mapping, simplification risk, and whether each 3D element is necessary for the lesson.
---

# Science Model Director

Review the science story before polish. A good-looking scene fails if learners cannot see the cause, effect, and measured result.

## Gate

Return:

- `PASS`: variables, visuals, and outputs form a correct lesson loop.
- `FIX_REQUIRED`: list the minimum model/visual changes.
- `BLOCKED`: the science model is wrong or missing measurable outputs.

## Checks

1. State the lesson claim in one sentence.
2. Map each control to a visible 3D change and a measured output.
3. Check causal direction: cause -> visual state -> formula/result -> reset.
4. Separate object geometry from explanatory annotation. An arrow is acceptable only when it represents flow, force, direction, transfer, or causality.
5. State the school-level simplification and the upgrade path if the real system is more complex.

## Subject Bars

- Chemistry: apparatus, reagent state, reaction evidence, measurement, and safety/scale cue.
- Biology: recognizable morphology first, detail markers second, flow or population dynamics third.
- Physics: units, vectors/fields/forces, calibration constants, and edge cases.

## Output

```text
SCIENCE_MODEL: PASS | FIX_REQUIRED | BLOCKED
Lesson claim:
Control -> visual -> output:
Simplification:
Fix set:
```
