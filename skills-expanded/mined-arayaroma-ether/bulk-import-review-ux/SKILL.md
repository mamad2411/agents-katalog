---
name: bulk-import-review-ux
description: Use when designing or reviewing a "review before commit" UI for bulk data import (CSV/xlsx upload, spreadsheet paste, API sync preview) — before building a multi-pane or wizard layout for row-level validation/fix-up. Triggers on "import review", "CSV upload UX", "preview before commit", "data validation table", "bulk fix errors UI".
metadata:
  origin: dar-money-mind reconciliation-import session, 2026-08-27
  sources: Flatfile, OneSchema, CSVBox, Airtable CSV import
allowed-tools: Read, Edit, Grep, Glob
---

# Bulk import review UX

For small-to-medium imports (roughly 10–200 rows) reviewed by one person before commit — bank
statement imports, contact list uploads, transaction CSVs, anything with a preview → fix → commit
flow.

## The anti-pattern: two-pane pending/confirmed split

First instinct is often "pending rows on the left, confirmed rows on the right, move them across
as they're fixed" — a kanban-style split. **Don't.** Rows physically relocating as you edit them
is disorienting: you lose your place, scan order breaks, and a row you were about to fix next has
already jumped away by the time you look back. None of the mature import tools (Flatfile,
OneSchema, Airtable's CSV import) do this. It also doubles table width, which forces horizontal
scrolling on any table with more than ~4 columns — a second, compounding usability failure.

## The pattern: one table, error-grouping banner, cell-level tinting, sticky progress footer

Single spreadsheet-like table for every row. Status is a **row/cell attribute**, never a spatial
partition.

1. **One table, problem rows sorted first** (or an explicit "show only rows with issues" toggle).
   Never split into two containers for the same row set.
2. **Error-grouping banner above the table**, computed from the current rows: "12 rows missing
   category", "2 need an account", "1 invalid date" as clickable filter chips. This is the
   single highest-leverage change — it turns "scroll through 30 red rows" into "click a chip, fix
   that group, move to the next."
3. **Cell-level tinting, not row-level.** Only the offending cell gets the warning/error color
   (e.g. a category `<select>` left empty) — unrelated cells in the same row (date, description,
   amount) stay neutral. Tinting the whole row for a single bad cell is noisy and makes genuinely
   broken rows (multiple bad cells) look no worse than rows with one missing dropdown.
4. **Distinguish soft-pending from hard-error color.** A field that's merely unfilled-but-fixable
   (pick a category from a dropdown) reads as amber/warning. A field that's structurally wrong
   (unparseable date, an amount that isn't a number, a payment method matching no known account)
   reads as red/error. Same "blocks commit" behavior, different visual urgency — don't flatten
   both to red.
5. **Bulk-fix actions scoped to the active filter.** "Apply to all" is dangerous once a filter
   chip is active — scope the bulk action to the currently visible/filtered rows and say so in
   the button label ("Apply to these 12 rows" vs "Apply to all 30"), so the action's blast radius
   is never a surprise.
6. **Sticky footer with live progress**, not a bottom-of-page action bar. "23 of 30 ready" plus
   Cancel/Confirm, pinned to the viewport bottom, so the user always sees how close they are
   without scrolling past a long table. Confirm stays disabled until zero blocking rows remain.

## Checklist before shipping an import-review UI

- [ ] Is there ever a moment a row moves to a different container/section as a *side effect* of
      editing it? If yes, that's the anti-pattern — collapse to one table.
- [ ] Does a single bad cell tint the entire row, or just that cell?
- [ ] Can the user filter to "just the broken ones" instead of scrolling past clean rows?
- [ ] Does a bulk-fix button's label say what it's about to touch?
- [ ] Is the confirm/commit action visible without scrolling, with a live ready-count?
