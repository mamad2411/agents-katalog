---
name: threejs-design-director
description: Use when planning or reviewing a Three.js educational lab scene for coherent 3D object design, morphology, composition, reference interpretation, element necessity, camera framing, and avoiding visually wrong or literal-but-illogical model choices.
---

# Three.js Design Director

Act before implementation and again before visual QA. Block 3D that is decorative, copied blindly from a reference, or unclear as a model.

## Gate

Return:

- `PASS`: every visible 3D element has a role and the model reads correctly.
- `FIX_REQUIRED`: list the smallest shape/composition changes.
- `BLOCKED`: reference is missing, contradictory, or cannot be built within budget.

## Checks

1. Name the primary object/system and 4-8 morphology anchors from the reference.
2. Decide what is a real 3D object versus an annotation. Do not model labels, guide rays, or sketch arrows as physical objects unless they teach a variable.
3. Check silhouette from the learner camera: front/side/top/cutaway references must map to visible geometry.
4. Check necessity: delete any object that does not teach the phenomenon, show state, provide scale, or support interaction.
5. Check implementation path: primitive, curve/tube, instanced mesh, or GLB. Use the smallest path that preserves morphology.

## Biology Rules

- Heart: chambers, valves, vessel branching, and flow path must read before particles are added.
- Lung: trachea, branching bronchi, lung lobes, diaphragm, and alveoli inset must read before gas markers are added.
- Ecosystem: terrarium boundary, soil layers, roots, organism groups, decomposers, and one clear energy-flow arrow must read before population markers are counted.

## Output

```text
DESIGN_DIRECTOR: PASS | FIX_REQUIRED | BLOCKED
Primary object:
Morphology anchors:
Real objects:
Annotations:
Fix set:
```
