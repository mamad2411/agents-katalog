---
name: autocad-drafting
description: "Draft in AutoCAD with production discipline: layers and standards, model versus paper space, annotative scaling, xrefs, sheet sets and plotting to PDF."
type: procedural
category: cad
domain: cad
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - autocad layer standards
  - paper space viewport scale
  - autocad xref management
  - autocad plot to pdf
  - autocad drawing template
keywords:
  - autocad
  - dwg
  - layers
  - xref
  - viewport
  - plot
  - annotative
mcp_servers:
  - autocad
source: custom
enabled: true
---

# AutoCAD Drafting

## Purpose

Draft in AutoCAD with production discipline: layers and standards, model versus paper space, annotative scaling, xrefs, sheet sets and plotting to PDF.

## When to Use

- Construction or fabrication drawings must be issued from AutoCAD.
- A drawing set must be consistent across sheets and revisions.
- A consultant's drawing needs review against a layer standard.

## When NOT to Use

- The output is a 3D model for printing; use a mesh/CAD modeller.
- Open formats are mandatory — issue DXF or PDF instead.
- The work is pure GIS mapping.

## Capabilities

- Apply a layer standard (name, colour, linetype, lineweight) consistently.
- Set model space geometry and paper space sheets with correct viewport scales.
- Manage xrefs and bind them for issue.
- Plot reproducible PDFs with correct scale, lineweights and fonts.

## Inputs

- The office CAD standard or client layer/drawing standard.
- Sheet sizes, titleblock and revision conventions.
- The deliverable: DWG, DXF and/or plotted PDF set.

## Workflow

1. Start from the approved template, not a blank drawing.
2. Draw at 1:1 in model space with units set explicitly.
3. Create sheets in paper space; set viewport scale and lock it.
4. Annotate with annotative styles so text reads correctly at each scale.
5. Audit and purge, then plot the full set and check scale bars and lineweights.

## Tools

- AutoCAD (LAYER, XREF, PAGESETUP, PUBLISH)
- autocad-mcp connector for automation
- PDF comparison tools for revisions

## Examples

- `allskills mcp install --harness claude --servers autocad`
- `allskills explain cad.autocad-drafting --query "set viewport scale"`
- `allskills route "issue a drawing set as pdf"`

## Safety

- Never edit geometry through a locked viewport or with the wrong layer current.
- Unbound xrefs sent to a client arrive as missing references.
- Plot scale errors are silent — always verify with a dimensioned check.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `autocad` | stdio | full | high | `AUTOCAD_BACKEND_URL` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/cad/autocad-drafting`). First-party skill, maintained in this repository.

## Notes

- `AUDIT` and `PURGE` before issue prevent bloated, corrupt files.
- Sheet set manager keeps revision numbering consistent across a project.
- Pairs with: `cad/dxf-dwg-interchange`, `cad/technical-drawing-gdt`.
