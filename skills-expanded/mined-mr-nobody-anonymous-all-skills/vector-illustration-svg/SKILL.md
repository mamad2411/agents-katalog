---
name: vector-illustration-svg
description: "Author clean, editable vector artwork and SVG: paths and boolean operations, stroke-to-outline, Inkscape CLI automation, and web-safe SVG export."
type: procedural
category: design
domain: design
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - clean up svg file
  - inkscape command line export
  - convert logo to vector
  - svg too large optimize
  - trace bitmap to vector
aliases:
  - inkscape
  - svg-art
keywords:
  - svg
  - vector
  - inkscape
  - illustration
  - path
  - bezier
  - trace
mcp_servers:
  - inkscape
source: custom
enabled: true
---

# Vector Illustration and SVG

## Purpose

Author clean, editable vector artwork and SVG: paths and boolean operations, stroke-to-outline, Inkscape CLI automation, and web-safe SVG export.

## When to Use

- A raster logo or scan must become a scalable vector asset.
- An SVG from a design tool is bloated, has broken paths or renders differently per browser.
- Artwork must be exported at exact dimensions for print or UI.

## When NOT to Use

- The deliverable is a bitmap photo edit; use a raster workflow.
- The artwork is generated procedurally at runtime; that belongs in the frontend skill.
- The task is a full brand system rather than a single asset.

## Capabilities

- Repair and simplify path geometry, nodes and fill rules.
- Convert strokes to outlines and flatten transparency before delivery.
- Automate batch conversion, resizing and export with the Inkscape CLI.
- Produce optimised SVG that keeps accessibility and print fidelity.

## Inputs

- The source file (SVG, AI, EPS, PDF) or a raster image to trace.
- The target medium and its constraints: print at 300 dpi, screen at 1x/2x, single colour.
- The brand palette and whether spot colours or CMYK are required.

## Workflow

1. Open the artwork and inspect the object tree: groups, clipped masks, embedded rasters.
2. Trace or redraw with the fewest nodes that preserve the shape; delete stray points.
3. Unify fill rules and stroke widths, then outline strokes that must not scale.
4. Set the document to the exact artboard size in millimetres or pixels, with no bleed unless print.
5. Export with Inkscape CLI (`inkscape --export-type=svg,png --export-dpi=300`) and visually diff against the source.
6. Run an SVG optimiser only after the geometry is correct, then re-check rendering.

## Tools

- inkscape
- svgo
- vips
- imagemagick
- potrace

## Examples

- ``inkscape art.svg --export-type=png --export-dpi=300 --export-filename=art-300.png` produces the print proof at the correct physical size.`
- `A traced bitmap with 4,000 nodes becomes a 300-node path after simplify-and-rebuild, and its SVG drops below 40 KB.`

## Safety

- Keep the untouched original; vector repair is destructive by nature.
- Do not convert text to outlines before the copy is signed off — it becomes uneditable.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `inkscape` | stdio | full | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/design/vector-illustration-svg`). First-party skill, maintained in this repository.

## Notes

- Check the SVG in a browser and a print preview; some filters only fail in one of them.
- Embedded rasters inside an SVG are a delivery smell — flatten or link them deliberately.
- Pairs with: `print-production-prepress`, `iconography-systems`.
