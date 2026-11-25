---
name: fusion360-solid-modeling
description: "Model production parts in Fusion 360 or SolidWorks: feature-based history, design intent, assemblies and joints, sheet metal and manufacturing exports."
type: procedural
category: cad
domain: cad
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - fusion 360 design intent
  - solidworks assembly mates
  - fusion sheet metal rules
  - cad design intent modeling
  - step export manufacturing
keywords:
  - fusion360
  - solidworks
  - solid-modeling
  - assemblies
  - sheet-metal
  - step
source: custom
enabled: true
---

# Fusion 360 Solid Modeling

## Purpose

Model production parts in Fusion 360 or SolidWorks: feature-based history, design intent, assemblies and joints, sheet metal and manufacturing exports.

## When to Use

- A part or assembly must be modelled for manufacture.
- Design intent must survive later dimension changes.
- A supplier needs STEP plus a drawing.

## When NOT to Use

- The part is purely decorative and a mesh suffices.
- The job is architectural/BIM scale.
- You lack a licence for the required native format; use STEP interchange.

## Capabilities

- Build feature trees with clear intent (symmetry, patterns, reference geometry).
- Define assembly joints/mates that reflect real degrees of freedom.
- Model sheet metal with bend rules and a flat pattern.
- Export STEP/IGES plus drawings with tolerances.

## Inputs

- The mating interfaces and the critical dimensions with tolerances.
- Manufacturing process and its constraints (bend radius, draft, tool access).
- Supplier's required format and revision convention.

## Workflow

1. Define the datum and the design intent before the first sketch.
2. Model primary form, then secondary features, then fillets and chamfers last.
3. Build the assembly and apply joints; test motion through the full range.
4. Check manufacturability: wall thickness, draft, bend relief, tool access.
5. Export STEP and a drawing; re-import STEP to confirm the export is intact.

## Tools

- Fusion 360 / SolidWorks
- a slicer or CAM tool for process checks
- STEP validator / re-import

## Examples

- `allskills explain cad.fusion360-solid-modeling --query "design intent"`
- `allskills route "model this assembly with joints"`
- `allskills mcp list --category cad`

## Safety

- Fillets early in the tree break when dimensions change; keep them last.
- Exporting without checking units produces parts off by 25.4x.
- Never assume a joint range without measuring the real mechanism.

## Source

All-Skills canonical library (`skills/cad/fusion360-solid-modeling`). First-party skill, maintained in this repository.

## Notes

- Design intent is about which dimensions are independent, not about feature count.
- Always round-trip a STEP export before sending it out.
- Pairs with: `cad/technical-drawing-gdt`, `cad/freecad-parametric-modeling`.
