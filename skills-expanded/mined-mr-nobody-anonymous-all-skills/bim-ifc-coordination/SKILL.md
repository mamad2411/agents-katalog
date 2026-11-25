---
name: bim-ifc-coordination
description: "Coordinate building models: IFC schema and exports, Revit/ArchiCAD workflows, clash detection, LOD/LOI expectations and model federation."
type: procedural
category: cad
domain: cad
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - ifc export coordination
  - clash detection bim
  - revit model federation
  - lod loi bim
  - ifc schema validation
keywords:
  - bim
  - ifc
  - revit
  - archicad
  - clash-detection
  - lod
  - federation
mcp_servers:
  - ifc
  - revit
source: custom
enabled: true
---

# BIM and IFC Coordination

## Purpose

Coordinate building models: IFC schema and exports, Revit/ArchiCAD workflows, clash detection, LOD/LOI expectations and model federation.

## When to Use

- Multiple disciplines must be coordinated in one federated model.
- An IFC deliverable must be checked before handover.
- Clashes must be found and tracked to resolution.

## When NOT to Use

- The task is single-discipline drafting with no coordination need.
- The client requires a native format you cannot export.
- The model is a conceptual mass with no construction intent.

## Capabilities

- Produce IFC exports with the right schema version and view.
- Federate models and run clash detection with tolerance control.
- Interpret LOD/LOI requirements and check compliance.
- Track issues to resolution with owner and status.

## Inputs

- The BIM execution plan: schema version, LOD/LOI, classification system.
- The discipline models and their coordinate origin agreement.
- Clash tolerance and the matrix of which disciplines to test.

## Workflow

1. Agree the shared coordinate system and project base point before modelling.
2. Export IFC with the correct schema (IFC4 vs IFC2x3) and validation settings.
3. Validate the IFC (schema, entity counts, property sets) before federation.
4. Run clash detection with a defined tolerance and filter hard vs soft clashes.
5. Assign, track and re-test clashes after each model update.

## Tools

- Revit / ArchiCAD / Tekla
- IFC validator and `ifcopenshell`
- clash detection (Navisworks, Solibri, or open tools)

## Examples

- `python -c "import ifcopenshell; m=ifcopenshell.open('model.ifc'); print(m.schema, len(m.by_type('IfcWall')))"`
- `allskills mcp install --harness claude --servers ifc`
- `allskills route "coordinate the architectural and structural models"`

## Safety

- Mismatched project base points create thousands of false clashes.
- An IFC export that looks right can lose property sets the client needs.
- Never close a clash without a re-test after the model update.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `ifc` | stdio | full | low | — |
| `revit` | stdio | full | high | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/cad/bim-ifc-coordination`). First-party skill, maintained in this repository.

## Notes

- IFC is an exchange format, not a modelling format — round trips lose data.
- Classify elements consistently or quantity take-offs fail silently.
- Pairs with: `cad/autocad-drafting`, `cad/technical-drawing-gdt`.
