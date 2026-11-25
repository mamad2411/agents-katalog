---
name: construction-documents-specifications
description: "Produce construction documents: drawing set structure, sheet numbering, dimensioning, schedules, specifications and revision control."
type: procedural
category: architecture
domain: architecture
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: high
level: advanced
triggers:
  - construction drawing set
  - sheet numbering convention
  - specification section writing
  - revision control drawings
  - door and window schedule
aliases:
  - construction-docs
keywords:
  - construction-documents
  - specifications
  - drawings
  - schedules
  - revisions
  - tender
mcp_servers:
  - ifc
  - revit
source: custom
enabled: true
---

# Construction Documents and Specifications

## Purpose

Produce construction documents: drawing set structure, sheet numbering, dimensioning, schedules, specifications and revision control.

## When to Use

- A design must be issued for tender, permit or construction.
- Contractors need unambiguous drawings, schedules and specs.
- A revision must be traceable across the whole set.

## When NOT to Use

- The deliverable is a concept design or visualisation.
- The jurisdiction requires a licensed architect's stamp and you are drafting support only.
- No coordinated model or survey exists yet.

## Capabilities

- Structure a drawing set with a defensible sheet numbering scheme.
- Dimension to reference points, not to finished surfaces only.
- Build schedules that match the drawings element for element.
- Write specification sections that reference the drawn scope.
- Control revisions and issue sets with a transmittal.

## Inputs

- The coordinated model and the consultant drawings (structure, MEP).
- The applicable code, standards and the client's brief.
- The issue purpose: tender, permit, construction, as-built.

## Workflow

1. Fix the sheet set order: general, plans, elevations, sections, details, schedules, specs.
2. Number sheets by discipline and series, and keep the index current.
3. Dimension from a single datum per view and cross-check against the model.
4. Derive schedules from the model where possible, then verify by count.
5. Cross-reference details and specs so nothing is documented twice in conflicting ways.
6. Issue as a dated, revision-marked set with a transmittal and a change log.

## Tools

- revit
- archicad
- ifc
- bluebeam

## Examples

- `Sheet A-201 is architecture, series 2, sheet 01 — the numbering itself tells a reader where to look.`
- `A door schedule with 40 doors must reconcile with 40 door tags on plan; count both.`

## Safety

- Never issue an unchecked set: a wrong dimension becomes a built defect.
- Confirm local licensing requirements before signing or sealing anything.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `ifc` | stdio | full | low | — |
| `revit` | stdio | full | high | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/architecture/construction-documents-specifications`). First-party skill, maintained in this repository.

## Notes

- Clashes between consultants are cheaper to fix in the model than on site.
- Revision clouds plus a delta and a change log are the audit trail.
- Pairs with: `architectural-design-workflow`, `bim-ifc-coordination`.
