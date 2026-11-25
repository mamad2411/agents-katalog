---
name: rhino-grasshopper
description: "Parametric design in Rhino and Grasshopper: NURBS modelling, definition structure, data trees, scripting with Python/C# and baking to Rhino geometry."
type: procedural
category: cad
domain: cad
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - grasshopper data tree
  - rhino nurbs modeling
  - grasshopper python component
  - parametric facade design
  - bake grasshopper geometry
keywords:
  - rhino
  - grasshopper
  - nurbs
  - parametric-design
  - datatree
  - computational-design
mcp_servers:
  - grasshopper
source: custom
enabled: true
---

# Rhino and Grasshopper

## Purpose

Parametric design in Rhino and Grasshopper: NURBS modelling, definition structure, data trees, scripting with Python/C# and baking to Rhino geometry.

## When to Use

- A design must be driven by rule-based variation (facades, structures, patterns).
- Geometry generation needs to be scripted and iterated.
- Complex freeform surfaces must be modelled accurately.

## When NOT to Use

- The geometry is simple prismatic CAD better done in a solid modeller.
- The deliverable must be a native BIM model rather than geometry.
- The team cannot maintain a computational definition long-term.

## Capabilities

- Model with NURBS curves/surfaces and maintain continuity.
- Structure Grasshopper definitions so data trees stay predictable.
- Script components in Python or C# for logic GH cannot express.
- Bake results with attributes (layers, materials) for downstream use.

## Inputs

- The generative rules and their parameter ranges.
- Constraints: fabrication limits, panel sizes, structural grid.
- Downstream consumer: Rhino layers, Revit, or a mesh for rendering.

## Workflow

1. Define inputs and outputs of the definition before wiring components.
2. Keep one definition per concern; group and label sections.
3. Handle data trees explicitly (graft, flatten) and verify counts at each step.
4. Test parameter extremes, not just the nominal case.
5. Bake to named layers and export what the next tool needs.

## Tools

- Rhino + Grasshopper
- grasshopper-mcp connector for automation
- RhinoPython / GhPython

## Examples

- `allskills mcp install --harness cursor --servers grasshopper`
- `allskills explain cad.rhino-grasshopper --query "data tree flatten"`
- `allskills route "generate a parametric facade"`

## Safety

- Flattening data trees silently destroys intended pairings.
- NURBS surfaces with poor continuity fail fabrication and rendering.
- Unbounded parametric ranges generate geometry no process can build.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `grasshopper` | stdio | full | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/cad/rhino-grasshopper`). First-party skill, maintained in this repository.

## Notes

- Name every input and output group; anonymous definitions become unmaintainable.
- Test extremes of each slider range before sharing the definition.
- Pairs with: `cad/freecad-parametric-modeling`, `3d/blender-geometry-nodes`.
