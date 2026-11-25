---
name: drawing-diagrams-with-typst
description: Use when creating, revising, or debugging diagrams in Typst for slides, books, or papers, especially when arrows, feedback loops, scaling, whitespace, overlap, or visibility issues make the layout fragile.
---

# Drawing Diagrams with Typst

## Overview

Build Typst diagrams that survive reuse across slides, books, and papers. Prefer `cetz` for anything with blocks, arrows, feedback loops, or geometry that will need iteration.

## Workflow

1. Model semantics first: blocks, routes, labels, and feedback destinations.
2. Encode geometry so AI can edit it: named sizes, gaps, anchors, loop heights, and return points.
3. Render the diagram standalone before embedding it anywhere.
4. Verify in this order:
   - low-res preview first with `scripts/make_preview.py`
   - AI visual review of the low-res preview image
   - diagnostics with `scripts/diagnose_diagram.py`
   - Typst source edits
   - rerender and re-review the low-res preview image
   - high-res image review only when the diagram contains small objects, thin lines, arrowheads, or small text
   - only then embedded checks in the final target context
5. If whitespace dominates an SVG, create a tight copy with `scripts/tighten_svg_viewbox.py`. Do not mistake scaling for a geometry fix.

## Non-Negotiables

- Treat slides, books, and papers as equal targets.
- Connect arrows to box edges with explicit gaps. Do not rely on center-to-center routing.
- Return feedback loops to the intended block, not the nearest node.
- Keep text readable in low-res preview. Tiny labels that only work after zooming are a failure.
- Diagnostics are advisory only. AI must inspect the preview image directly before sign-off.
- For slide-targeted figures, final sign-off is the whole-slide preview, not the standalone diagram.
- Default exported SVGs to zero outer whitespace. Add padding only when there is an explicit reason.
- Avoid projector-hostile bright greens and yellows. Prefer darker, mixed colors.
- Let AI fix Typst source geometry and colors. Use scripts for diagnosis and safe `viewBox` trimming only.

## References

- Layout and parameterization: `references/layout.md`
- Connections and arrow routing: `references/arrows-and-connections.md`
- Color and visibility: `references/color-and-visibility.md`
- Verification sequence: `references/verification.md`

## Common Failure Modes

- Absolute coordinates scattered through the file make small routing edits touch unrelated numbers.
- A standalone SVG looks acceptable, but overlap appears after slide embedding or scaling.
- A figure passes standalone checks but still reads as too small once inserted into a text-heavy slide.
- Extra SVG padding survives every embed and makes a diagram look smaller for no semantic reason.
- Diagnostics stay quiet because the failure is a crushed arrowhead, thin stroke, or other small object that only visual review catches.
- Tightening `viewBox` hides a geometry problem instead of fixing it.
- Feedback loops return to a node edge when the semantics require re-entering a block.

## Quick Start

- Run `scripts/make_preview.py path/to/diagram.typ`
- Run `scripts/diagnose_diagram.py path/to/diagram.typ`
- Fix Typst source, not the PNG
- Rerender low-res until layout, gaps, text size, and colors are stable
