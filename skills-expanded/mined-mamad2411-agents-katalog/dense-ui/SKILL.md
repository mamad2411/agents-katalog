---
name: dense-ui
description: "Use when designing tables and dashboards: column alignment, tabular numerals, row density, sticky headers, bulk actions, and information per screen."
---


# Tables and Dashboards

A dense surface exists so someone can compare values, not read them. Every default here follows from that: the eye travels *down* a column, so a column must be internally consistent before a row is pretty. Default to the tightest density the pointer allows, put every quantity on the right in tabular figures, and cut columns before you cut rows — a column you keep taxes every future scan, a row you keep costs only pixels. When the data and the grid disagree, the data wins; a table is not a place to express a layout idea.

The boundary with the siblings that look like this one: **rows and cells are here; axes and marks are `charts`.** The query input, facets, and result ranking above a grid belong to `search-filter` — this skill starts once the rows have arrived. Empty, loading, and error specs belong to `ui-states`, which owns the threshold ladder; do not restate it here.

**Work inside the table layer the project already has.** Check for a headless table library (TanStack Table, AG Grid, an existing `<DataTable>`) and a virtualizer before writing markup, and express density, alignment, and sticky behavior through what it exposes. Row padding and text sizes come from the project's spacing and type scales — `spacing` owns the scale — never from pixel values invented for one table.

## Quick Reference

| Open it when | File |
| --- | --- |
| You are specifying real columns and need the alignment, number format, width behavior, truncation, and empty-value rule for a given column type | [table-spec.md](references/table-spec.md) |

## Decision: how dense?

Ship at most three modes — `comfortable`, `default`, `compact` — and change exactly two things between them: vertical row padding and text size. Column widths, alignment, radii, and icon sizes stay fixed, or switching reflows the table and the user loses their place mid-scan.

Row height is derived, never typed: `row height = line-height + 2 × one step of the project's spacing scale`. Dense text may drop to `14px` for cells and `13px` for captions, almost never below `12px` — `typography` owns those floors. Under `@media (pointer: coarse)`, drop `compact`; its rows fall under the hit-target floor `touch-input` owns.

## Core Principles

1. **Right-align every quantity, always with tabular figures.** Comparison happens on the digit columns, and proportional figures draw a narrow `1` and a wide `4`, so the column reads as chaos. Set `text-align: right` and `font-variant-numeric: tabular-nums`. *Exception:* a numeric identifier (order `#4021`, a ZIP code) is a label, not a quantity — left-align it, never sum it.

2. **Align the header with its own cells.** A left-aligned header over a right-aligned column leaves a visible dogleg at the top of the table, and the sort affordance ends up furthest from the values it sorts. Put the sort indicator on the column's *inside* edge, next to the numbers. *Exception:* an icon-only header control (select-all checkbox) centers with its cells.

3. **Fix the fraction digits before trusting `tabular-nums`.** Tabular figures equalize digit *width*, not decimal *position* — `1.5` and `1.25` still misalign. Format to a fixed fraction count per column, then right-align. *Exception:* a column spanning orders of magnitude (bytes, multi-currency) uses a unit-scaled format like `1.2 GB` and aligns on the unit boundary.

4. **Put the unit in the header, not in every cell.** Repeating `ms` two hundred times adds two hundred glyphs of noise and shortens the digits actually being compared. Write `Latency (ms)`. *Exception:* a genuinely mixed-unit column keeps per-cell units, and then aligns per principle 3.

5. **Fix alignment before adding zebra stripes.** Right-aligned tabular numbers do the work striping was compensating for; stripes on a correctly aligned table add noise and a second background color to maintain in both themes. *Exception:* a table wide enough to scroll horizontally, where a row must be tracked across a scroll boundary — and even then, freezing the identifier column beats striping.

6. **Hover and selection must not share a channel.** If hover tints the row and selection also tints the row, a hovered unselected row and a selected row are indistinguishable. Hover keeps the tint; selection adds a persistent second signal — a checked box plus a leading accent bar. Gate the hover tint behind `@media (hover: hover)`; `touch-input` owns why. *Exception:* a single-select picker that navigates away on click, where nothing persists.

7. **Freeze the header and at most one column.** Two frozen columns on a narrow viewport leave nothing to scroll. Put `position: sticky` on the `<th>` elements rather than on `<thead>` or `<tr>` — sticky on table sections and rows has patchy engine support — and cap sticky chrome with `max-height` in `dvh`: an 80px header on a 667px landscape viewport leaves almost no room for content. The frozen column's shadow appears only once `scrollLeft > 0`; a permanent one reads as a seam. *Exception:* an identifier that is genuinely two columns (name + version).

8. **The row is not a link.** Wrapping a row in an anchor kills text selection, breaks copying values out of the table, and makes a screen reader announce the whole row as one link. Give the row one explicit target — the identifier cell — and layer row-click on top as a convenience. *Exception:* a chooser dialog whose only purpose is picking one row.

9. **Bulk actions state their exact scope.** "Select all" is ambiguous the moment the result set exceeds the page, and users discover the ambiguity by deleting the wrong thing. Show the count and both scopes: `3 selected`, then `Select all 50 on this page` / `Select all 1,284 matching`. Never seat a destructive bulk action adjacent to a benign one. *Exception:* when page size equals the match count, offer one scope.

10. **A dashboard tile carries one number and its comparison.** A bare number is not information — value, delta, and the period the delta covers are. A tile holding three numbers is a table pretending to be a tile. *Exception:* a status roll-up (`4 healthy · 1 degraded`) is a partition of one total, not three metrics.

11. **Tile values share a baseline.** Different digit counts and label lengths shift each number's position, and a row of tiles stops reading as one instrument. Fix the label row height, fix the value's type size, and use `tabular-nums`. *Exception:* one deliberate hero tile at a larger size, sitting outside the row.

12. **Cut columns before rows.** The real column count is what fits at the narrowest supported width without horizontal scroll; everything past that goes to a detail view or behind a column picker whose state persists per user. *Exception:* an export or audit view whose purpose is completeness — it scrolls, and it says so.

## Smell / Fix

| Smell | Fix |
| --- | --- |
| Numbers left-aligned, or right-aligned without `tabular-nums` | `text-align: right` + `font-variant-numeric: tabular-nums` |
| Decimals ragged despite tabular figures | Fixed fraction count per column |
| `ms` / `%` / `$` repeated in every cell | Unit moves to the header |
| Zebra stripes over a misaligned table | Fix alignment first; delete the stripes |
| Selected row looks identical to a hovered row | Selection gets a second, persistent channel |
| Sticky header transparent, content sliding under it | Opaque background; hairline only once scrolled |
| Blank cell where a value is genuinely absent | `—` for no value, `0` for a real zero |
| "Select all" with no scope, next to Delete | Name both scopes; separate the destructive action |
| Tile shows a number with nothing to compare it to | Add delta + period, or delete the tile |
| Scroll goes choppy past a few hundred rows | Virtualize — `perf` owns the threshold |
| Rows animate in on every data refresh | No entrance animation on data being read (`motion`) |

## Output: the column contract

Before writing a table, emit the contract and get it agreed — one row per column, no prose.

```
| Column       | Type       | Align | Format                       | Width | Empty |
| Name         | identifier | start | truncate 1 line, title attr  | flex  | —     |
| Latency (ms) | quantity   | right | 0 decimals, tabular          | 96px  | —     |
| Updated      | timestamp  | right | relative < 7d, else ISO date | 120px | Never |
```

Then state density mode, sticky columns, selection model, and bulk actions beneath it.

## Checklist

- [ ] Every quantity right-aligned with `tabular-nums` and a fixed fraction count
- [ ] Headers aligned to their cells; sort indicator on the inside edge
- [ ] Units live in headers, not cells; no stripes standing in for alignment
- [ ] Hover and selection use different channels; hover gated to hover-capable pointers
- [ ] One frozen column maximum; sticky applied to `<th>`; sticky chrome capped in `dvh`
- [ ] Row is not an anchor; one explicit navigation target per row
- [ ] Bulk selection names its scope and its count exactly
- [ ] Every dashboard tile shows value + delta + period, on a shared baseline
- [ ] Column count fits the narrowest supported width; the rest is behind a picker
- [ ] Empty, loading, and error states taken from `ui-states`, not improvised here
