---
name: ui-part-tables
description: "How to build and place tables: when a table beats a list or cards, one surface with its toolbar and footer, choosing and ordering columns, widths, density and alignment, statuses that show the exception, row actions and selection, sorting, filtering and pagination, sticky headers, the data table library, loading and empty states, accessibility, and how a table fits a narrow screen. Read before building or reworking one."
---

# Tables

Generated tables look the same whatever the data: Name, Status, Date and
Actions; a green "Active" badge on every row; a filled primary button and a
three-dot menu repeated on every line; inputs and steppers in every cell; a
filter card floating above a table card; product codes wrapping onto two
lines; the whole page scrolling sideways on a phone. A table is a tool for
comparing records on the same fields and acting on the few that need it.
The principles (direction, spacing, type, colour, icons, states,
accessibility) are in the `ui` skill; where a table and its toolbar sit, in
`ui-layout` section 4; the page around it in `ui-page-list-detail`.

## 1. When a table

- A table: records compared on the same fields (orders, customers, stock,
  invoices, logs), where people scan a column, sort, or pick out the ones
  that need action.
- A list (`ui-part-lists`): items read one at a time with one or two facts
  each (notifications, messages, activity).
- Cards (`ui-part-cards`): visual items where an image decides (products,
  portfolios).
- A description list: one record's fields (the detail view).

## 2. One surface

The toolbar, the header row, the rows and the footer are one surface: one
border or one background, no gaps between them.

```
┌──────────────────────────────────────────────────────────────────────┐
│ [⌕ Search orders ............]  [Status ▾] [Date ▾]      [Columns ▾] │  toolbar
├──────────────────────────────────────────────────────────────────────┤
│ ☐  Order ↓     Customer          Status          Total     Due       │  header
│ ☐  #10482      Rina Pratama      Overdue · 2 d   1.250.000 12 Mar  ⋯ │
│ ☐  #10481      Budi Santoso                        480.000 14 Mar  ⋯ │
├──────────────────────────────────────────────────────────────────────┤
│ 1 to 25 of 214                                    ‹  1  2  3 …  9  › │  footer
└──────────────────────────────────────────────────────────────────────┘
```

- Toolbar: search first (the widest control), then filters, then view
  options at the right (columns, density, export); no heading or card of its
  own. When rows are selected, the bulk actions replace the toolbar in the
  same place ("3 selected · Mark paid · Export · Clear").
- Footer: the count and range at the left, pagination at the right
  (`ui-part-pagination`); the page size selector beside it for large tables.
- No title repeated inside the surface: the page header names it
  (`ui-part-page-header`).

## 3. Columns

- Chosen from the decision the user makes on this screen: the identifying
  field first (name, number), then the deciding ones (status, stock, amount,
  due date), then context (owner, created, tags). Five to eight columns on a
  laptop; more only in tools built for it, with a column chooser.
- Widths fixed so they do not jump between rows or pages: `table-layout:
  fixed` with widths on the columns that need them, or the library's sizing;
  the identifying column takes the rest.
- Headers are short nouns in sentence case with units ("Total (IDR)",
  "Weight, kg"), not repeated in every cell.
- Hidden, reordered and resized columns are saved per user when the table
  is used daily.

## 4. Density and alignment

- Rows 40 to 48px (32 to 36px in a compact mode people can choose), 14px
  text, 12 to 16px cell padding, the header in a quieter weight and colour,
  a hairline between rows rather than a box around each.
- Text left; numbers and money right with `font-variant-numeric:
  tabular-nums`; dates in one format (`ui-part-dates`); each header aligned
  like its cells.
- Short values (codes, prices, dates, badges) never wrap
  (`white-space: nowrap`); long names wrap to two lines or truncate with the
  full text in a `title` and on focus.
- Zebra stripes only for very wide tables; a hover tint on rows that open
  something.

## 5. Statuses and values

- A status says the exception, not the norm: no badge when a product is
  simply active; "Inactive", "Low stock · 3 left", "Overdue · 2 days" where
  they apply, with the text as well as the colour (`ui-part-badges`).
- Empty values show a dash with an accessible "None", not "N/A" or "null".
- Relative values where they matter ("in 2 days"), exact ones on hover.
- Links in cells go to the record; the identifying cell is the main link.

## 6. Cells show values, not controls

- No steppers, inputs or selects in every row. A quick change (stock,
  status) opens a small popover or the record's panel.
- Inline editing only in a spreadsheet-like tool, one cell at a time, when
  the brief asks for it: Enter to edit, Escape to cancel, Enter or Tab to
  save, a visible saving and error state per cell.

## 7. Row actions and selection

- The row (or its name) opens the record: a side panel for quick detail
  (`ui-part-drawers`) or its own page; the URL follows.
- One or two actions people use daily as quiet ghost buttons or links at
  the row's end; the rest in a labelled menu ("Actions for order #10482",
  `ui-part-menus`). Never the page's filled primary button repeated on every
  row; a three-dot menu only with real items in it.
- Destructive actions confirm or offer undo, and never sit beside the
  harmless one without space.
- Selection: a checkbox column with a header checkbox (indeterminate when
  some are selected), Shift+click for ranges, "Select all 214" offered after
  selecting a page; selection survives paging only when the bulk action
  works on all.

## 8. Sorting, filtering, paging

- Sortable headers are buttons with the current direction shown and
  `aria-sort` on the column; one sort at a time unless the tool needs more;
  the default sort is the one that answers the page's question (overdue
  first, newest first).
- Filters in the toolbar (`ui-part-search` for the search field); active
  filters as chips with "Clear all"; the state in the URL
  (`frontend-state`).
- Sorting, filtering and paging on the server for more than a few hundred
  rows; the count comes from the server.
- Virtualise very long tables (TanStack Virtual) instead of rendering
  thousands of rows; keep the header aligned.

## 9. Sticky parts

- On long tables a sticky header, set below the top bar (`top` equal to its
  height), with a solid background.
- When the table scrolls sideways, the first column sticky with a shadow or
  line at its edge while scrolled.
- A sticky bulk bar or footer only when it is used while scrolling.

## 10. The data table library

- The component library's data table (TanStack Table underneath, as in
  shadcn/ui, Mantine React Table, AG Grid for heavy grids) rather than a
  hand-built `<table>` once it sorts, filters or pages.
- Still a real `<table>` with `<thead>`, `<th scope="col">`, `<tbody>` and a
  `<caption>` (visible or visually hidden) for screen readers; `role="grid"`
  only when cells are navigable with arrow keys.
- Column definitions typed; cell renderers small; formatting through
  `Intl` with the active locale.

## 11. States

- Loading: skeleton rows the height of real ones on first load; later
  loads keep the rows with a quiet indicator in the toolbar.
- Empty: an empty state in the table's place, with the action that fills it
  ("No invoices yet. Create invoice"); filtered to nothing: say so and offer
  "Clear filters" (`ui-part-empty-states`).
- Error: in the surface, with Retry, the toolbar still usable.

## 12. On narrow screens

- Columns hide by priority as the width drops (`hidden md:table-cell` on
  the context columns first), keeping the identifying and deciding ones.
- Below about 640px, either a scroll container with a visible edge and the
  first column sticky, or one compact card per record: the identifying
  field as the heading, a meta line, the status, and the daily action on
  the status line, without every column's label repeated on every card.
- Never cut off: the table's container, not the page, scrolls sideways
  (`min-width: 0` on its flex or grid parents).
- Filters open in a sheet from one "Filters" button showing how many are
  active; bulk actions in a bar at the bottom.

## 13. Themes and motion

Row hover and selection as surface steps that hold in both themes
(`ui-themes`); no row animations beyond a short highlight on a changed or
new row (`motion-interface`).

## Check it

- `preview` at 360, 768 and 1440px: no page overflow, the first column and
  actions reachable, touch targets 44px on phones.
- Tab through: sortable headers, row links and the actions menu reachable
  in order; a screen reader announces the caption, headers and sort state.
- Sort, filter and page, reload: the same view returns from the URL.
- 0 rows, 1 row, 1,000 rows, a very long name, a missing value.

## Avoid

Name / Status / Date / Actions whatever the data is; a green "Active" badge
on every row; steppers or inputs in every row; two buttons on every row
where a menu would do; a three-dot menu with nothing real in it; product
codes breaking over two lines; a filter card, a gap and a table card; a
table where a list would do; the page scrolling sideways; client-side
sorting of a table that is paged on the server.
