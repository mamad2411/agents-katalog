---
name: technical-drawing-gdt
description: "Produce and read manufacturing drawings: projection views, dimensioning and tolerancing, GD&T symbols and datums, surface finish and title-block standards."
type: procedural
category: cad
domain: cad
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - gd&t symbols meaning
  - datum reference frame
  - technical drawing tolerances
  - surface finish callout
  - asme y14.5 drawing
keywords:
  - gd&t
  - tolerance
  - datum
  - drawing
  - asme
  - iso-2768
  - surface-finish
source: custom
enabled: true
---

# Technical Drawing and GD&T

## Purpose

Produce and read manufacturing drawings: projection views, dimensioning and tolerancing, GD&T symbols and datums, surface finish and title-block standards.

## When to Use

- A part must be manufactured and inspected against a drawing.
- A tolerance stack needs to be justified rather than guessed.
- A supplier's drawing must be interpreted correctly.

## When NOT to Use

- The part is 3D printed for fit-check only; a model may suffice.
- The geometry is architectural rather than manufactured.
- The drawing is being replaced entirely by a model-based definition.

## Capabilities

- Choose views and sections that show every critical feature.
- Apply GD&T controls with datums that match function.
- Calculate tolerance stacks for fits and assemblies.
- Specify surface finish and material callouts that a shop can meet.

## Inputs

- The functional requirements (what mates, what moves, what seals).
- The manufacturing process and its achievable tolerances.
- The applicable standard (ASME Y14.5 or ISO GPS).

## Workflow

1. Identify functional datums from how the part is used and fixtured.
2. Dimension from datums, not from whichever edge is convenient.
3. Apply the loosest tolerance that satisfies function; tighten only where needed.
4. Run a tolerance stack for every critical interface.
5. Review with manufacturing before release — if it cannot be inspected, it cannot be made.

## Tools

- CAD drawing environment
- tolerance stack spreadsheet
- GD&T reference (ASME Y14.5 / ISO 1101)

## Examples

- `allskills explain cad.technical-drawing-gdt --query "choose datums"`
- `allskills route "add gd&t to this bracket drawing"`
- `allskills mcp list --category cad`

## Safety

- Tolerances tighter than the process can hold raise cost with no functional gain.
- Missing datum references make a control unmeasurable.
- Never release a drawing without checking it against the model.

## Source

All-Skills canonical library (`skills/cad/technical-drawing-gdt`). First-party skill, maintained in this repository.

## Notes

- Position tolerance with MMC can save cost versus a tight ± dimension.
- Every drawing needs units, scale, projection method and revision block.
- Pairs with: `cad/fusion360-solid-modeling`, `cad/autocad-drafting`.
