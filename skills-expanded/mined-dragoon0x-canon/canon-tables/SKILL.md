---
name: canon-tables
description: Use when designing, auditing, or refactoring data tables, grids, lists of tabular data, sortable columns, or any structured-data display. Covers the table vs card decision, density, row height, alignment, sorting, pagination, sticky headers, zebra striping, responsive behavior, and empty states. Trigger when the user mentions table, data grid, rows, columns, spreadsheet, list view, or data table.
---

# CANON · Tables

Tables are for comparing values across rows. If users aren't comparing, they don't need a table.

## Table vs cards vs list

| Pattern | Use when |
|---|---|
| **Table** | Users scan multiple columns, compare rows, sort by column |
| **Cards** | Each item has rich content (image, description, multiple actions) |
| **List** | Simple one-item-per-row with 1–2 pieces of info |

Tables shine with 4+ columns of structured data. Two columns? That's a list.

## Use `<table>` semantics

```html
<table>
  <caption class="sr-only">Sales by region, Q4 2025</caption>
  <thead>
    <tr>
      <th scope="col">Region</th>
      <th scope="col">Revenue</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">North America</th>
      <td>$2.4M</td>
      <td>+12%</td>
    </tr>
  </tbody>
</table>
```

- `<table>` — never a grid of `<div>`s. Screen readers need semantics.
- `<caption>` — describes the table; visually hide if the context makes it redundant.
- `<th scope="col">` on column headers, `<th scope="row">` on row headers.
- For complex tables (merged cells), use `id` + `headers` instead of scope.

## Density — pick one, apply consistently

| Density | Row height | Use |
|---|---|---|
| Compact | 32px | Power-user tools, dense dashboards |
| **Default** | 48px | Most apps |
| Comfortable | 56px | Content-heavy rows with secondary text |

Let users toggle density if power-user context. Default to 48px.

## Alignment

| Data type | Alignment |
|---|---|
| Text (names, descriptions) | Left |
| Numbers | **Right** |
| Currency, percentages | Right |
| Dates | Left |
| Status pills, boolean | Center or left |
| Actions column | Right |

Numbers right-aligned compare at a glance. Left-aligned numbers force the eye to scan.

Use `font-variant-numeric: tabular-nums` on numeric columns — digits align vertically.

## Sticky headers

For tables taller than one viewport:

- Column header: `position: sticky; top: 0`
- Optional: first column sticky-left for wide tables (`position: sticky; left: 0`)
- Background color must be opaque — or scrolled content bleeds through

## Zebra striping — usually unnecessary

Zebra striping is a band-aid for poor row separation. A 1px subtle border between rows works better and looks cleaner.

Use zebra only when:
- Very wide tables where the eye loses the row across columns
- Extremely dense (32px) rows where borders clutter

When striping, use a **very light** alternate: 2–4% difference from base. Heavy stripes dominate the content.

## Sorting

- Every sortable column has a visible indicator when active (up/down arrow).
- Hover on sortable column shows a muted preview arrow.
- Click toggles ascending → descending → (optionally) unsorted.
- `aria-sort="ascending" | "descending" | "none"` on the `<th>`.
- Default sort is the most meaningful column, not the first (usually not "ID").

## Pagination vs infinite scroll vs virtualization

| Pattern | Use when |
|---|---|
| Pagination | ≤ 1000 rows, users often jump to specific pages |
| Infinite scroll | Feeds where "what's new" matters, not "where am I" |
| Virtualization (windowed render) | 10,000+ rows, keeping table semantics |

For large data, **virtualization wins** over infinite scroll for tabular contexts. Keyboard and screen-reader users need predictable jumps.

Show total count always: "Showing 1–50 of 1,247."

## Row actions

| Pattern | Use |
|---|---|
| Trailing actions column | Frequent row actions (Edit, Delete) |
| Kebab menu (⋯) per row | Many actions (4+) |
| Row click → detail page | Rich detail needed |
| Inline checkbox + bulk action bar | Bulk operations |

Don't hide the primary action in a hover-only menu — breaks on touch.

## Empty state

Every table needs an empty state with an action path.

```
No projects yet.
[+ Create project]
```

Three types of empty:
- **Initial**: "You haven't created any X yet. [action]"
- **Filtered**: "No X match your filters. [Clear filters]"
- **Error**: "Couldn't load X. [Retry]"

## Loading state

First load: skeleton rows matching the final row count (3–8 rows), shimmer 1000–1500ms.

Subsequent loads (sort/filter): overlay with 60% opacity + spinner, keep existing rows visible so users don't lose context.

## Responsive — tables on mobile

Tables are hard on mobile. Three strategies:

1. **Horizontal scroll** — table keeps structure, container scrolls. Works for wide data tables. Cue with shadow on scroll edge.
2. **Collapse to cards** — each row becomes a card with label: value pairs. Works for < 6 columns of meaningful data.
3. **Hide columns** — show 2–3 critical columns on mobile, hide the rest, reveal via expand or detail page.

Don't crush text to fit — unreadable beats scrollable.

## Column widths

- Let content drive where possible.
- Fixed widths only for: action column (right-aligned, often 40–80px), status column, date column.
- Text columns use `min-width` not hard `width`, allow truncation with tooltip on hover/focus.

## Truncation

```css
.cell-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 240px;
}
```

Truncated text must show the full value on hover (tooltip) and keyboard focus. Users shouldn't need to widen the window to read data.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Using `<div>` grid for tabular data | Screen reader fail, no semantic sort/filter |
| Numbers left-aligned | Hard to compare |
| Zebra striping on short tables | Clutter, no purpose |
| Hover-only row actions | Broken on touch, hidden from screen readers |
| No loading state | Users see empty table, think it's broken |
| No empty state action | Dead-end UX |
| Default sort by "ID" | Users almost never care about ID |
| Pagination without total count | Users can't judge scale |
| Sticky header with transparent background | Content bleeds through, unreadable |
| Shrinking text to fit mobile | Illegible |
| Row heights mixed in one table | Visual instability |

## Decision tree

```
Are users comparing values across rows?
  ├─ No → Use cards or list
  └─ Yes → Table

How many rows?
  ├─ < 50 → Render all
  ├─ 50–1000 → Paginate
  └─ 1000+ → Virtualize

Mobile?
  ├─ < 6 columns → Collapse to cards
  └─ 6+ columns with comparable data → Horizontal scroll

Row actions?
  ├─ 1–3, frequent → Trailing column buttons
  ├─ 4+ → Kebab menu
  └─ Bulk → Checkbox + action bar
```

## Audit checklist

- [ ] Uses `<table>` / `<thead>` / `<tbody>` / `<th>`
- [ ] `scope` attributes on `<th>`
- [ ] `<caption>` present (visually hidden OK)
- [ ] Numbers right-aligned with tabular-nums
- [ ] Sticky headers opaque, visible
- [ ] Sorted column shows indicator + `aria-sort`
- [ ] Empty state has action path
- [ ] Loading state shown on first and subsequent loads
- [ ] Row actions visible without hover on touch
- [ ] Truncation reveals full value on hover/focus
- [ ] Pagination shows total count
- [ ] Mobile strategy chosen (scroll / cards / hidden columns)
- [ ] Row heights consistent

## Sources

- WCAG 2.2 · 1.3.1 Info and Relationships, 1.3.2 Meaningful Sequence
- WAI-ARIA · aria-sort, table roles
- Material Design 3 · Data tables
- Apple HIG · Tables, Lists
- Refactoring UI · "Align text to improve legibility", "Use tabular numbers"
