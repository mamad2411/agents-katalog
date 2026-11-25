---
name: openscad-programmatic-cad
description: "Design parts in OpenSCAD: parametric modules, CSG operations, libraries, preview versus render, and export for printing or machining."
type: procedural
category: cad
domain: cad
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - openscad parametric script
  - openscad module library
  - openscad render vs preview
  - openscad stl export
  - programmatic cad design
keywords:
  - openscad
  - csg
  - parametric
  - scad
  - stl
  - 3d-printing
mcp_servers:
  - openscad
source: custom
enabled: true
---

# OpenSCAD Programmatic CAD

## Purpose

Design parts in OpenSCAD: parametric modules, CSG operations, libraries, preview versus render, and export for printing or machining.

## When to Use

- A part's shape is naturally described by parameters and repetition.
- The model must live in version control and be diffable.
- Variants are generated programmatically (sizes, grids, enclosures).

## When NOT to Use

- Complex organic surfaces are required; a mesh modeller is better.
- The deliverable needs assembly constraints and a drawing sheet.
- The team cannot read code to review the design.

## Capabilities

- Structure parameters, modules and includes so variants are one-line changes.
- Use CSG correctly (union, difference, intersection) with predictable origins.
- Distinguish fast preview from full CGAL render before export.
- Export printable STL/3MF with correct units and manifold geometry.

## Inputs

- The dimensional constraints and what the part must fit.
- Manufacturing process and its limits (overhang, minimum wall, tolerance).
- The parameter set that defines each variant.

## Workflow

1. Put every dimension in a top-level parameter block with comments and units.
2. Build primitive modules, then compose; keep the origin at a meaningful datum.
3. Preview (`F5`) while iterating, then render (`F6`) before exporting.
4. Check manifoldness and wall thickness in a slicer before printing.
5. Export STL/3MF per variant from a script so the artifacts are reproducible.

## Tools

- OpenSCAD CLI (`openscad -o out.stl in.scad`)
- openscad-mcp connector
- a slicer for print checks

## Examples

- `openscad -o bracket.stl -D 'width=40' bracket.scad`
- `openscad -o preview.png --camera=0,0,0,55,0,25,120 --imgsize=1200,900 part.scad`
- `allskills mcp install --harness claude --servers openscad`

## Safety

- `$fn` set globally on large models explodes render time and memory.
- Preview can show geometry that full render rejects as non-manifold.
- Non-manifold or zero-thickness walls fail in the slicer or the machine.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `openscad` | stdio | full | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/cad/openscad-programmatic-cad`). First-party skill, maintained in this repository.

## Notes

- `-D` overrides parameters from the CLI, which makes variant generation trivial.
- Keep modules small and named; a 500-line single module is unreviewable.
- Pairs with: `cad/freecad-parametric-modeling`, `3d/mesh-repair-printing`.
