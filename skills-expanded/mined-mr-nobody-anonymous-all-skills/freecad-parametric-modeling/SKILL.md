---
name: freecad-parametric-modeling
description: "Model parametrically in FreeCAD: sketches and constraints, Part Design bodies, spreadsheets and expressions, TechDraw drawing sheets and headless scripting."
type: procedural
category: cad
domain: cad
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - freecad parametric model
  - freecad sketch constraints
  - freecad spreadsheet driven dimensions
  - freecad techdraw
  - freecad python script
aliases:
  - freecad
keywords:
  - freecad
  - cad
  - parametric
  - sketch
  - part-design
  - techdraw
  - step
mcp_servers:
  - freecad
source: custom
enabled: true
---

# FreeCAD Parametric Modeling

## Purpose

Model parametrically in FreeCAD: sketches and constraints, Part Design bodies, spreadsheets and expressions, TechDraw drawing sheets and headless scripting.

## When to Use

- A mechanical part must be driven by parameters and revised safely.
- An open-source CAD workflow is required for licensing or cost reasons.
- The model must be scripted or generated in CI.

## When NOT to Use

- The deliverable requires a proprietary format contract with a supplier.
- A one-off mesh is enough; parametric CAD adds overhead.
- The geometry is architectural at building scale — use BIM tooling.

## Capabilities

- Build fully constrained sketches that survive dimension changes.
- Drive dimensions from a spreadsheet so variants are data, not re-modelling.
- Export STEP/IGES/STL with the correct units and tolerance.
- Generate TechDraw sheets with views, sections and dimensions.

## Inputs

- Nominal dimensions, tolerances and the interfaces the part mates with.
- The target manufacturing process (3D print, CNC, sheet metal).
- Output format required by the supplier or downstream tool.

## Workflow

1. Create a spreadsheet of driving parameters and name every constraint dimension.
2. Model with Part Design features in a deliberate order (pad, pocket, fillet last).
3. Fully constrain sketches; check the solver reports zero degrees of freedom.
4. Derive drawing sheets and verify dimensions match the parameter table.
5. Export STEP for CAD interchange and STL/mesh only for printing.

## Tools

- FreeCAD (Part Design, Spreadsheet, TechDraw)
- FreeCAD Python console / `freecadcmd`
- freecad-mcp connector

## Examples

- `freecadcmd -c "import FreeCAD; FreeCAD.openDocument('bracket.FCStd')"`
- `allskills mcp install --harness cursor --servers freecad`
- `allskills route "model a parametric bracket"`

## Safety

- Fillets applied before later features often break the model; add them last.
- Unit mismatch (mm vs inch) in imported STEP silently scales parts.
- Never trust a model without a drawing or measurement check against the spec.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `freecad` | stdio | full | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/cad/freecad-parametric-modeling`). First-party skill, maintained in this repository.

## Notes

- Fully constrained sketches are the difference between a model and a sketch that breaks.
- Keep a parameter spreadsheet versioned next to the model.
- Pairs with: `cad/openscad-programmatic-cad`, `cad/technical-drawing-gdt`.
