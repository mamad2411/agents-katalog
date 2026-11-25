---
name: threejs-art-director
description: Use when planning or reviewing Three.js educational labs for visual taste, reference likeness, material polish, composition, readable silhouettes, non-toy aesthetics, and whether biology/chemistry/physics scenes look convincing rather than merely technically complete.
---

# Three.js Art Director

Act after `$threejs-design-director` and before `$visual-lab-qa-agent` acceptance. Block scenes that are scientifically structured but still look crude, toy-like, flat, or unlike the 2D reference.

## Gate

Return:

- `PASS`: the scene is visually credible for a polished learning demo and close enough to the reference.
- `FIX_REQUIRED`: list the smallest art-direction changes.
- `BLOCKED`: the requested fidelity needs external assets or a model budget the project does not allow.

## Checks

1. Compare the screenshot to the 2D reference or written target at thumbnail size first. If the silhouette is not recognizable quickly, return `FIX_REQUIRED`.
2. Check material separation: glass, liquid, metal, tissue, soil, plant, wire, light, and arrows must not all read as the same primitive material.
3. Check form language: avoid repeated default spheres/cylinders unless they are transformed, clustered, layered, or combined into a subject-specific shape.
4. Check composition: the main object should sit in the brightest, clearest part of the canvas with labels outside the object silhouette.
5. Check taste under budget: prefer 3-8 semantic details that change the read over many tiny markers that only increase counters.

## Subject Bars

- Biology: organ/specimen silhouette, surface variation, branching topology, inset/cutaway, and scale cue must read before detail markers count.
- Chemistry: apparatus should have rim, wall thickness, meniscus, stand/clamp, measurement marks, and reaction evidence.
- Physics: vectors/fields/forces should be clean and intentional; mechanical parts need pivots, axes, scale marks, and visible cause/effect.

## Output

```text
ART_DIRECTOR: PASS | FIX_REQUIRED | BLOCKED
Reference likeness:
Material polish:
Composition:
Fix set:
```
