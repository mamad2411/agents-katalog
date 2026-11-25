---
name: cnc-machining-fabrication
description: "Go from a solid model to machined parts: DFM review, toolpath strategy, workholding, feeds and speeds, and a G-code sanity check."
type: procedural
category: cad
domain: cad
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: high
level: advanced
triggers:
  - cnc toolpath setup
  - feeds and speeds aluminium
  - gcode verification
  - fixture and workholding plan
  - design for machining
aliases:
  - cnc
  - milling
keywords:
  - cnc
  - machining
  - gcode
  - toolpath
  - feeds-speeds
  - fixture
  - dfm
mcp_servers:
  - freecad
  - openscad
source: custom
enabled: true
---

# CNC Machining and Fabrication

## Purpose

Go from a solid model to machined parts: DFM review, toolpath strategy, workholding, feeds and speeds, and a G-code sanity check.

## When to Use

- A CAD model must become a machined part on a real machine.
- A toolpath needs verification before it can break a tool or a workpiece.
- A design must be revised for manufacturability.

## When NOT to Use

- The part will be printed; additive rules differ.
- Only a drawing is needed, with no machining intent.
- The machine and controller are unknown — post-processor choice is not guessable.

## Capabilities

- Review geometry for machinability: radii, depths, setups and tolerances.
- Choose roughing and finishing strategies per feature.
- Calculate feeds and speeds from material, tool and rigidity.
- Verify G-code offline and dry-run safely.

## Inputs

- The solid model and the material stock size.
- The machine envelope, spindle power and controller/post-processor.
- Available tooling, and the tolerances that actually matter.

## Workflow

1. Check the model: minimum internal radius ≥ tool radius, depth-to-diameter within reach.
2. Plan setups and workholding before generating paths; every re-fixture is an error source.
3. Rough with adaptive clearing, then semi-finish, then finish — do not skip stages.
4. Compute feeds and speeds from surface speed and chip load, then derate for rigidity.
5. Simulate the toolpath, check for gouges, collisions and rapid moves through stock.
6. Dry-run with the spindle off and Z offset raised before the first cut.

## Tools

- freecad
- fusion360
- linuxcnc
- camotics
- openscad

## Examples

- `A 6 mm end mill cannot produce a 2 mm internal corner — either accept a larger radius or plan a second operation.`
- `A first cut on scrap material is cheaper than a broken tool and a scrapped workpiece.`

## Safety

- Always dry-run; never trust a first-run path on a loaded machine.
- Confirm units (mm vs inch) in both CAM and the post-processor.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `freecad` | stdio | full | medium | — |
| `openscad` | stdio | full | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/cad/cnc-machining-fabrication`). First-party skill, maintained in this repository.

## Notes

- Chip load matters more than spindle speed for tool life.
- Record the post-processor version; a silent post update changes output.
- Pairs with: `freecad-parametric-modeling`, `technical-drawing-gdt`.
