---
name: ui-page-dashboard
description: "How to build a dashboard or an application's overview: the shell, the overview's grid and blocks, responsive behaviour, and loading it fast (independent blocks, pagination, caching, virtualised lists). Read before building or reworking one."
---

# Dashboard or application overview

One kind of page. Write its blueprint first (`ui-structure`: the regions
in order, the skeleton in numbers, the components and their states), and
build each control to its contract in `ui-anatomy`. The measures
(container, grid, spacing, type) are in `ui-layout`; each part it uses (sidebar, header, tables, charts, cards,
pagination, loading) has its own `ui-part-*` skill. Build it from the
component library (the `ui` skill), themed with the tokens.

## 1. Start from the questions

Name the two or three decisions a user makes on this screen ("what is
overdue", "who owes money", "what failed overnight"). Every block answers
one of them; a block that answers none is cut. The order of the blocks is
the order of those questions.

## 2. The shell

- **Sidebar** 240 to 256px, full window height and sticky, with its own
  scroll; the product name at the top, the daily places next (icon and
  label each, the current one marked), settings and the account at the
  bottom. It collapses to icons (with tooltips) below about 1280px if
  space is tight, and becomes a drawer below 1024px (`ui-part-sidebar`).
- **Top bar** 56 to 64px inside the content column: the page title or
  breadcrumbs on the left; search, notifications that exist and the account
  on the right. Sticky.
- **Content** anchored beside the sidebar, padded 24 to 32px (16px on
  phones), fluid up to about 1600px with any extra width left on the right,
  never a centred column floating between empty bands (`ui-layout` section
  2b); a grid of 12 columns with 16 to 24px gutters.

## 2a. What sticks

Stick what the user needs while scrolling through the work, and nothing
else:

- the sidebar (full height, its own scroll) and the top bar;
- a long table's header row, and its first column when the table scrolls
  sideways;
- the filter and search bar above a long list;
- the bulk-action bar that appears when rows are selected;
- the Save and Cancel bar of a long form or settings page.

Figures, charts and a short page header scroll away. The sticky layers
together stay under about 120px on a wide screen and about 64px on a phone
(on a phone, only the top bar, or the filter bar in its place), each
stacked below the one above (`top` set to the height above it) with a
solid background.

## 3. The overview, row by row

A composition that works for most overviews; cut the rows the questions do
not need.

1. **Page header**: the title, the scope (a date range or a filter the whole
   page follows, as one control, its value in the URL), the one primary
   action. One row, 24 to 32px below the top bar.
2. **Figures**: three or four stat cards across (3 columns each of 12),
   equal height. Each card: a label in the quiet colour (14px), the value
   large (28 to 32px, tabular numbers) with its unit, and one line of
   context: the comparison with a named period ("+12 vs last month"), or
   what it means ("4 due today"). A small sparkline only when the trend is
   the point. The whole card links to the list behind the figure.
3. **The work**: the table or list the user acts on, 8 of 12 columns, with
   its own header (title, count, a "View all" link, filters when they
   matter). Beside it, 4 of 12: what needs attention next (due soon,
   alerts), as a short list with one action each.
4. **Trends**: one chart that answers a question in its title, 8 of 12;
   a breakdown (top items, a split by category as a bar list, not a donut)
   in 4 of 12.
5. Anything else below, only when it answers a question.

Cards in a row share their height (`align-items: stretch`); each card has
the same padding (16 to 24px), the same header (title left, one action
right, 12px above the content) and no heading repeated inside it. Space
between rows 24px; inside a card 12 to 16px.

## 4. Responsive

- 1280px and wider: the rows above.
- 768 to 1279px: figures in two columns; the work and its side list stack,
  the work first; the chart full width.
- Under 768px: one column in the order of the questions; figures two
  across in a compact form (label and value only); a table becomes one card
  per row with the deciding fields, or scrolls inside a container with a
  visible edge; filters open in a sheet from one "Filters" button; the
  sidebar is a drawer behind a labelled "Menu" button.
- Nothing overflows at 360px, and touch targets stay at 44px.

## 5. Loading it fast

- **The shell first.** The sidebar, the top bar and every block's frame
  render at once; each block loads its own data and shows a skeleton the
  shape of its content. One slow query never blanks the page, and an error
  sits on the block that failed, with a retry.
- **Fetch with a cache**: TanStack Query or SWR (or the framework's loader
  with its cache). Figures and charts can be 30 to 60 seconds stale and
  refetch on focus; a list keeps the previous page on screen while the next
  loads. Mutations update the cache or invalidate the right keys, so the
  figure changes when a row does.
- **Paginate on the server** once a list can pass a couple of hundred rows:
  page, sort and filter in the query, never by loading everything and
  slicing in the browser (`ui-part-pagination`). Cursor pagination for long
  or growing lists, page numbers where position matters. More than a few
  hundred rows on screen at once are virtualised (TanStack Virtual).
- **Aggregate where the data lives**: figures and chart series come from
  the database (a grouped query, a materialised view, a cached summary),
  not from fetching rows to count them in the browser.
- **State in the URL**: filters, sort, page and date range in the query
  string, so a view can be shared, reloaded and gone back to.
- **Search** debounced 250 to 300ms, with the request cancelled when a new
  one starts.
- **Load heavy parts late**: the chart library and panels below the fold
  are imported when needed (`import()`, `next/dynamic`, `lazy`).
- **HTTP caching** for data that changes slowly: `Cache-Control` and an
  `ETag`, so a reload costs a 304.

## 6. States

- First run with no data: the one step that fills it ("Add your first
  book"), not a page of zeroes.
- A block with no rows says so in its own place ("Nothing is overdue").
- Loading keeps the layout; numbers do not jump when they arrive.

## Avoid

The default admin shell (four stat cards with invented numbers and green
deltas, a line chart titled "Overview", an activity feed of made-up people,
a table of Name / Status / Date / Actions); numbered section headings
("01 Perlu tindakan"); a sentence under every heading explaining it; a
heading alone inside a card; the accent colour on every button and badge;
the page's filled primary button repeated on every row; a greeting
("Welcome back, John!") taking the top of the screen; gradients on cards; a
donut for two values.
