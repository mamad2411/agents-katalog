---
name: design-layout-and-grid
description: "Repair visual composition, whitespace, alignment, grouping and responsive layout grids using Gestalt proximity, consistent spacing, CSS Grid and content-driven breakpoints."
---

# Layout and grid

## Scope

Use this specialist when the actual task involves layout issues. Check documented brand/system decisions before prescribing changes. Do not conflate taste with accessibility standards or make assumptions from screenshots alone.

Affecting category: **layout**. Related governing principles: balance, proportion. Route from `design-diagnose` or `design-review` when observations match this category, or load directly during a focused implementation.

## Procedure

- **crowded-groups**: Use proximity: tighten within a group, increase gaps between groups and align major edges. Verify: At mobile and desktop widths, related elements are identifiable without outlines.
- **broken-responsive-grid**: Use CSS grid minmax(), min(), auto-fit or container queries; allow content-driven stacking. Verify: No lost content, overlap or horizontal scroll at narrow viewports and zoom/reflow.
- **uneven-alignment**: Set shared grid tracks and layout tokens; allow variable content while aligning semantically similar landmarks. Verify: Across content variants, rows/columns remain visually stable without truncating text.

Read `references/playbook.md` for exact discriminating checks, implementation examples, tradeoffs and acceptance tests. Keep the fix within the existing component architecture. Report original observation, selected recipe and evidence. For usability, engage `ux-*`; for normative accessibility, engage `wcag-*`.
