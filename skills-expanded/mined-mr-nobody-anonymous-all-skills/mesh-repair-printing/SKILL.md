---
name: mesh-repair-printing
description: "Prepare meshes for manufacturing: manifold repair, normals, wall thickness, overhangs and supports, slicer profiles and dimensional tolerance for 3D printing and CNC."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - mesh not manifold 3d print
  - repair stl holes
  - 3d print supports overhang
  - slicer profile settings
  - print tolerance fit
keywords:
  - 3d-printing
  - mesh
  - manifold
  - slicer
  - supports
  - tolerance
  - fdm
source: custom
enabled: true
---

# Mesh Repair and 3D Printing

## Purpose

Prepare meshes for manufacturing: manifold repair, normals, wall thickness, overhangs and supports, slicer profiles and dimensional tolerance for 3D printing and CNC.

## When to Use

- A model fails to slice or prints with defects.
- Printed parts must fit together predictably.
- A design must respect process limits before manufacture.

## When NOT to Use

- The output is visual only and never manufactured.
- The part needs machined tolerance beyond the process capability.
- The geometry is 2D and belongs to laser cutting.

## Capabilities

- Detect and repair non-manifold edges, flipped normals and holes.
- Check minimum wall thickness and detail against nozzle/process limits.
- Orient parts and generate supports that respect overhang rules.
- Set tolerances for press/slip fits measured in test prints.

## Inputs

- The printing process (FDM, resin, SLS) and machine constraints.
- Material and its shrink/creep behaviour.
- The fit requirement (clearance, interference, surface finish).

## Workflow

1. Inspect the mesh for holes, non-manifold edges and zero-area faces.
2. Repair in the mesh tool, then re-check before slicing.
3. Orient for strength and minimal support, then preview the sliced layers.
4. Print a tolerance test coupon for any critical fit.
5. Record the slicer profile with the part so it is reproducible.

## Tools

- Blender 3D-Print toolbox / MeshLab
- PrusaSlicer / OrcaSlicer / Cura
- calipers for verification

## Examples

- `blender -b part.blend -P repair.py`
- `prusa-slicer --export-gcode --load profile.ini part.stl`
- `allskills route "fix this stl so it prints"`

## Safety

- A non-manifold shell produces hollow or missing walls that fail structurally.
- Printing without a fit coupon almost always misses the intended clearance.
- Resin printing requires drainage holes and safe handling of uncured resin.

## Source

All-Skills canonical library (`skills/3d/mesh-repair-printing`). First-party skill, maintained in this repository.

## Notes

- Design clearance differs by process: FDM typically needs more than resin.
- Keep supports off visible or functional surfaces when possible.
- Pairs with: `3d/blender-modeling-topology`, `cad/openscad-programmatic-cad`.
