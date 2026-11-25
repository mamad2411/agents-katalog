---
name: remove-duplicate-shapes
description: "Find and safely remove confirmed duplicate overlapping shapes on selected PowerPoint slides after repeated generation. Use only for duplicate cleanup, not general overlap repair. 重複生成された同一図形の検出・削除に使用。"
license: MIT
---

# Remove Duplicate Shapes

## Scope

Default to the current or selected slide. Expand to the whole deck only when
explicitly requested. Overlap alone is never evidence of duplication.

## Procedure

1. Establish a recoverable original or use the application's undo/version
   history. Inspect available tools before choosing a supported editing method.
2. Inventory candidate shapes by slide and shape ID. Exact name, position,
   dimensions, and text can identify candidates, but cannot prove equivalence.
3. Compare actual content and appearance: shape type/geometry, fill, line,
   text runs and formatting, rotation, transparency, effects, crop, links,
   alt text, and stacking context. Where accessible, compare image bytes and
   relationships, not just filenames or relationship IDs.
4. Exclude placeholders, groups, connectors, tables, charts, media, and objects
   referenced by animations or actions from automatic deletion. These may carry
   distinct data or dependencies. If a necessary property cannot be inspected,
   flag the pair for manual review; do not assume equality or silently skip errors.
5. Use exact comparisons, not fuzzy position or text thresholds. Two empty
   shapes with the same bounds but different colors are not duplicates.
6. Present candidate pairs, reasons, slides, IDs, and intended survivors.
   Obtain confirmation before deleting, unless the user has already approved
   this exact preview. A request to find duplicates is not deletion approval.
7. Delete only confirmed redundant copies. Normally keep the first/lower copy;
   change that choice if it would alter layering, interactions, or accessibility.
   Do not rewrite the deck with a library that cannot preserve its features.
8. Inspect each changed slide and verify that no intended content, links, or
   animations were lost. Report deleted IDs, survivors, counts, exclusions, and
   unresolved candidates. If comparison is inconclusive, make no deletion.

## Acceptance examples

- Same coordinates and text, different fill: keep both.
- Identical-looking table with different cell values: keep both.
- Identical rectangle used by an animation: manual review, not automatic deletion.
- Two fully equivalent ordinary shapes, preview approved: remove only the
  redundant copy and verify the resulting stacking order.
