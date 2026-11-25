---
name: interior-space-planning
description: "Plan interior spaces: programme and adjacencies, circulation and clearances, furniture layouts, lighting and finishes, and code requirements for egress and accessibility."
type: procedural
category: architecture
domain: architecture
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - interior space planning layout
  - furniture clearance dimensions
  - lighting plan interior
  - accessibility clearances interior
  - adjacency diagram space plan
keywords:
  - interior-design
  - space-planning
  - clearances
  - lighting
  - finishes
  - accessibility
mcp_servers:
  - ifc
source: custom
enabled: true
---

# Interior Space Planning

## Purpose

Plan interior spaces: programme and adjacencies, circulation and clearances, furniture layouts, lighting and finishes, and code requirements for egress and accessibility.

## When to Use

- A floor plan must be laid out for a specific use and occupancy.
- Furniture and circulation need dimensioned clearances.
- Finishes and lighting must be specified coherently.

## When NOT to Use

- Structural or MEP design decisions are required (engineer).
- The task is exterior architecture.
- Only a mood board is requested with no plan implications.

## Capabilities

- Build an adjacency and bubble diagram from the programme.
- Apply dimensional standards for circulation and accessibility.
- Lay out furniture with real dimensions and service clearances.
- Coordinate lighting layers and finish schedules.

## Inputs

- The programme: rooms, occupancy, equipment and storage needs.
- The base plan with structural and MEP constraints.
- Applicable accessibility standards and local code.

## Workflow

1. List the programme with areas and required adjacencies.
2. Draw circulation first, then place furniture against real dimensions.
3. Check door swings, turning circles and accessible routes.
4. Layer lighting (ambient, task, accent) and specify fixtures with output data.
5. Produce a finish schedule and verify transitions at thresholds.

## Tools

- CAD/interior design software (SketchUp, Revit, Rhino)
- furniture specs
- lighting calculation tools

## Examples

- `allskills route "space plan a 200 m2 office"`
- `allskills explain architecture/interior-space-planning --query "accessible clearances"`
- `allskills mcp list --category cad`

## Safety

- Furniture placed without service clearances looks fine and fails in use.
- Accessibility routes must be verified against the local standard, not memory.
- Finish choices drive maintenance cost; confirm with the operator.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `ifc` | stdio | full | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/architecture/interior-space-planning`). First-party skill, maintained in this repository.

## Notes

- Circulation first prevents the classic too-narrow corridor.
- Specify fixtures by photometric data, not marketing descriptions.
- Pairs with: `architecture/architectural-design-workflow`, `cad/bim-ifc-coordination`.
