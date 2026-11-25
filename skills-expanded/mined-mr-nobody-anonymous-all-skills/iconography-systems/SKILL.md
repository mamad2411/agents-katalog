---
name: iconography-systems
description: "Build an icon system: consistent optical grid, stroke and corner radii, naming, SVG sprite delivery and accessibility."
type: procedural
category: design
domain: design
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - design icon set
  - svg sprite icons
  - icon grid and stroke width
  - icon accessibility aria
  - icon naming convention
aliases:
  - icons
keywords:
  - icons
  - iconography
  - sprite
  - svg
  - stroke
  - pixel-grid
mcp_servers:
  - figma
  - inkscape
source: custom
enabled: true
---

# Iconography Systems

## Purpose

Build an icon system: consistent optical grid, stroke and corner radii, naming, SVG sprite delivery and accessibility.

## When to Use

- A product needs a coherent icon family instead of mixed sources.
- Icons render blurry, at inconsistent weight or misaligned with text.
- An icon set must ship as one accessible, cacheable asset.

## When NOT to Use

- A single decorative glyph is needed — use a licensed brand icon.
- The symbol is really an illustration with gradients and detail.
- The task is a logo; brand marks follow different rules.

## Capabilities

- Define an optical grid with consistent keyline shapes and stroke weight.
- Normalise corners, joins, caps and terminal angles across the set.
- Build an SVG sprite with `<symbol>` and currentColor theming.
- Ship accessible icons with labels or `aria-hidden` as appropriate.

## Inputs

- The list of concepts the product must express, with usage frequency.
- Sizes actually used (16, 20, 24 px) and the display density.
- The existing type metrics so icons sit optically with text.

## Workflow

1. Draw keyline shapes on a 24 px grid with a 2 px stroke and 20 px live area.
2. Redraw at the smallest real size first; check legibility at 16 px.
3. Align to pixels with the strokes snapped to half-pixels on a 1x grid.
4. Name icons by concept (`arrow-left`, not `icon-3`), and store the source file per icon.
5. Assemble one sprite and reference with `<use>`; document the mapping.
6. Review the whole set side by side for weight and optical balance.

## Tools

- inkscape
- svgo
- figma
- svg-sprite

## Examples

- `A 24 px grid with 1.5 px strokes lands cleanly on 1x and 2x but not on 1.5x — choose the grid by the dominant DPR.`
- ``currentColor` on sprite symbols lets one asset serve every theme without duplication.`

## Safety

- Do not use colour alone to convey icon state.
- Keep icon-only buttons labelled for screen readers.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `figma` | http | full | medium | — |
| `inkscape` | stdio | full | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/design/iconography-systems`). First-party skill, maintained in this repository.

## Notes

- Optical size beats mathematical consistency: a circle needs to be slightly larger than a square to look equal.
- Audit for orphan icons with no counterpart in the set's metaphor.
- Pairs with: `vector-illustration-svg`, `ui-ux`.
