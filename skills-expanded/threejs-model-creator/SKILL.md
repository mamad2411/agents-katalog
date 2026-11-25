---
name: threejs-model-creator
description: Create, import, refine, and optimize 3D models for Three.js labs. Use for procedural geometry, GLB/GLTF asset loading, model composition, materials, textures, labels, articulated parts, educational apparatus, lab benches, robots, instruments, and visual polish for web 3D.
---

# Three.js Model Creator

Build models that explain the lab. Default to procedural geometry when it is enough; use GLB only when shape fidelity matters.

When using generated references, prefer object turnaround sheets: front/side/top/cutaway on a plain background. Ignore decorative backgrounds and model only the shapes, materials, labels, and functional parts needed for the lab.

## Decision

- Primitive/parametric: best for school lab equipment, levers, blocks, tanks, wires, fields, meters, charts, molecule kits, and physics apparatus.
- GLB/GLTF: use for recognizable complex objects, robots, room assets, hands/tools, or product-like props.
- R3F/drei abstractions: use only in a scene already using R3F.
- Babylon assets: use only in Babylon scenes; do not mix render engines in one viewport.

## Model Standard

Each model needs:

- Semantic object/group names.
- Correct scale relative to the lab unit.
- Contact with table/floor unless intentionally floating.
- Materials chosen for function: metal, plastic, rubber, liquid, glass, emissive, field line.
- Distinct visual hierarchy: hero object, active mechanism, supporting apparatus, labels.
- Label/readout strategy: CSS2D/HTML overlay, CanvasTexture, or DOM panel.
- Disposal path for generated geometries/materials/textures.

## Articulation

For moving parts, group by physical linkage:

- Pivoting: parent group origin at hinge/pivot.
- Sliding: group axis aligned to movement direction.
- Rotating: named shaft/rotor group with visible axis or bearing.
- Multi-part apparatus: one root group, child groups per moving subsystem.

## References

Read `references/model-standards.md` for concrete modeling, material, GLB, and optimization rules.
