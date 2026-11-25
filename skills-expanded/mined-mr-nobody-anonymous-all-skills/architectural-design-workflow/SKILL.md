---
name: architectural-design-workflow
description: "Develop an architectural design: brief and constraints, site analysis, concept massing, drawing sets at each stage, code compliance checks and consultant coordination."
type: procedural
category: architecture
domain: architecture
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - architectural concept design process
  - site analysis architecture
  - architecture drawing set stages
  - building code compliance check
  - massing study
keywords:
  - architecture
  - design
  - site-analysis
  - massing
  - drawings
  - code
mcp_servers:
  - ifc
source: custom
enabled: true
---

# Architectural Design Workflow

## Purpose

Develop an architectural design: brief and constraints, site analysis, concept massing, drawing sets at each stage, code compliance checks and consultant coordination.

## When to Use

- A building project must move from brief to coordinated documentation.
- A site's constraints must be analysed before massing.
- A design must be checked against zoning and egress requirements.

## When NOT to Use

- The task is interior fit-out only, with no building envelope work.
- The deliverable is a structural calculation (engineering, not architecture).
- The work is a rendering exercise with no code or constructability review.

## Capabilities

- Turn a brief into measurable area and adjacency requirements.
- Analyse site constraints (orientation, access, setbacks, topography).
- Test massing options against daylight, area and circulation criteria.
- Prepare stage-appropriate drawings and coordinate consultant inputs.

## Inputs

- The brief: programme, budget, site, and client priorities.
- The site survey, zoning envelope and applicable building codes.
- Project stage (concept, schematic, design development, construction documents).

## Workflow

1. Write the brief as measurable requirements and confirm priorities with the client.
2. Model the site constraints and the allowable envelope before massing.
3. Test options quickly in massing and compare against area/daylight targets.
4. Develop the chosen scheme into plans, sections and elevations at stage-appropriate detail.
5. Run code checks (egress, accessibility, fire) and log consultant coordination items.

## Tools

- CAD/BIM (Revit, ArchiCAD, Rhino)
- site analysis in QGIS for context data
- code reference sets

## Examples

- `allskills route "test massing options for a site"`
- `allskills explain architecture/architectural-design-workflow --query "zoning envelope"`
- `allskills mcp list --category cad`

## Safety

- Zoning and code requirements are jurisdiction-specific; verify with the authority, never assume.
- Skipping the site survey invalidates massing and later drawing work.
- Unlogged consultant changes cause clashes later in the project.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `ifc` | stdio | full | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/architecture/architectural-design-workflow`). First-party skill, maintained in this repository.

## Notes

- Area schedules are the fastest way to test a brief against a scheme.
- Record assumptions; they become change orders when forgotten.
- Pairs with: `cad/bim-ifc-coordination`, `architecture/interior-space-planning`.
