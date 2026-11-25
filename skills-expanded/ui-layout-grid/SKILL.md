---
name: ui-layout-grid
description: "The mechanics of CSS Grid and Flexbox: which one to reach for, how to write grid-template-columns and rows, gap, grid-template-areas, repeat, minmax and auto-fit, and every flex property (direction, justify, align, wrap, grow, shrink, basis). The named layouts (holy grail, sidebar, card grid, centred, split) as copy-ready code. Read when a layout needs columns and rows that line up, or a row of items that space and wrap on their own, and `ui-layout` set the numbers."
---

# CSS Grid and Flexbox, as mechanics

`ui-layout` fixes the numbers: one container width, the spacing scale, where
each thing goes. This skill is how you actually place them, the two engines
every modern layout is built from. A generated layout reaches for neither:
it nests `div`s, pushes them with margins, floats, absolute positioning and
magic percentages, and the columns do not line up, the gaps drift, and one
long word tears it sideways. Grid and Flexbox remove all of that. Pick the
right one, write the template once, and the browser does the arithmetic.

## 1. Grid or Flexbox

Decide by the shape of the content, not by habit.

- **Flexbox: one axis.** A row or a column of items that share out the space
  along a single line. A toolbar, a button group, a nav bar, a card's inner
  stack, a centred thing. The item sizes lead; the container distributes what
  is left.
- **Grid: two axes.** Rows *and* columns that must line up with each other.
  A page shell (sidebar plus content), a card grid, a form of label/field
  pairs, a dashboard, an image gallery, any "these line up in both
  directions". The container defines the tracks; the items drop into them.

The quick test: if you find yourself nesting a row of columns inside a column
of rows to force alignment, you wanted Grid. If one `gap` and letting items
size themselves does it, you wanted Flexbox. They nest freely: a grid cell
whose contents are a flex row is the common, correct case.

Both use the same `gap` property, so spacing is one value in either, taken
from the `--space-*` scale in `ui-layout`, never a margin on each child.

## 2. Grid: the template

A grid is defined on the container. Everything else follows from the track
lists.

### Columns and rows

```css
.grid {
  display: grid;
  grid-template-columns: 240px 1fr;   /* two columns: fixed, then the rest */
  grid-template-rows: auto 1fr auto;  /* header, body that grows, footer */
  gap: var(--space-5);                 /* 24px between every track */
}
```

- `1fr` is "one share of the leftover space". Two `1fr` columns are equal;
  `2fr 1fr` is two-thirds and one-third. `fr` is the unit that makes columns
  line up without percentages that forget the gap.
- `auto` sizes a track to its content. `auto 1fr auto` is the universal
  "top and bottom hug their content, the middle fills" (a page column, a
  card, a dialog).
- A fixed track (`240px`, `16rem`) for a thing with a set width (a sidebar,
  an icon rail); `1fr` beside it for the part that should take the rest.
- `gap` replaces every margin between children. Set it once on the
  container; never space grid children with their own margins.

### repeat, minmax, auto-fit: the responsive card grid

The pattern the generators exist for. A grid of cards that fits as many
columns as the width allows and reflows on its own, with no media query:

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-5);
}
```

- `repeat(N, ...)` writes a track N times. `repeat(3, 1fr)` is three equal
  columns.
- `minmax(260px, 1fr)` is a track that is never narrower than 260px and
  grows to a share of the rest. This is what keeps a card from being
  crushed.
- `auto-fill` makes as many 260px-plus columns as fit, then stretches them to
  `1fr`. Use `auto-fit` instead when you want a single remaining card to
  stretch across the whole row rather than leave empty tracks; `auto-fill`
  keeps the empty tracks, so cards stay their natural width. Prefer
  `auto-fill` for a catalogue, `auto-fit` when the row should always be full.
- Pick the `minmax` floor from the content: a product card 240 to 280px, a
  stat tile 160 to 200px, a wide feature 320px.

### Spanning and placing

```css
.featured { grid-column: span 2; }      /* this card takes two columns */
.full     { grid-column: 1 / -1; }      /* from the first line to the last: full width */
```

- `span 2` makes an item cover two tracks: the one large tile in an uneven
  grid (`ui-layout`, section 7).
- `1 / -1` is "start at the first grid line, end at the last", the clean way
  to make one item full width inside a grid without leaving it.
- Lines are numbered from 1; negative numbers count from the end, so `-1` is
  always the far edge however many columns there are.

### grid-template-areas: the named layout

For a shell you will read again in a month, name the regions instead of
counting lines. The ASCII drawing *is* the layout:

```css
.app {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "sidebar header"
    "sidebar main"
    "sidebar footer";
  min-height: 100dvh;
}
.app > .sidebar { grid-area: sidebar; }
.app > .header  { grid-area: header; }
.app > .main    { grid-area: main; }
.app > .footer  { grid-area: footer; }
```

- Each quoted string is a row; each word is a cell. Repeating a name across
  cells makes that region span them (here `sidebar` spans all three rows).
- A `.` (a lone dot) is an empty cell.
- Rearranging on a phone is rewriting the drawing in a media query, nothing
  else moves:

```css
@media (max-width: 1023px) {
  .app {
    grid-template-columns: 1fr;
    grid-template-areas: "header" "main" "footer";  /* sidebar becomes a drawer */
  }
  .app > .sidebar { display: none; }
}
```

This is the holy-grail layout (header, sidebar, main, footer) in full, and
the sidebar-plus-content shell from `ui-layout` section 5. Use areas when
there are three or more regions; use a plain two-track template when there
are two.

### Aligning inside the grid

- `align-items` / `justify-items`: how every item sits in its cell on the
  block and inline axis. Default `stretch` fills the cell, which is what
  makes a row of cards share one height (`ui-layout`). `start`, `center`,
  `end` for the rest.
- `align-content` / `justify-content`: how the whole set of tracks sits when
  it is smaller than the container.
- One item overriding its cell: `align-self` / `justify-self` on that item.

## 3. Flexbox: the one-axis row or column

Flex is defined on the container; the children then flex.

```css
.row {
  display: flex;
  flex-direction: row;          /* or column */
  gap: var(--space-3);          /* 12px between items */
  justify-content: space-between;
  align-items: center;
}
```

### The container properties

- **`flex-direction`**: `row` (the main axis runs across) or `column` (down).
  Switching to `column` is how a row stacks on a phone.
- **`justify-content`** (along the main axis): `flex-start`, `center`,
  `flex-end`, `space-between` (first and last to the edges, equal space
  between), `space-around`, `space-evenly`.
- **`align-items`** (across the main axis): `stretch` (default, equal
  heights), `center` (the common one for a toolbar), `flex-start`,
  `flex-end`, `baseline` (text baselines line up).
- **`flex-wrap`**: `nowrap` (default, items shrink or overflow) or `wrap`
  (items that do not fit move to the next line). A wrapping flex row with a
  `gap` is the simple responsive tag list or button bar.
- **`gap`**: the space between items, both axes when wrapping. Same scale as
  grid.

### The child properties

`flex` is shorthand for three values on each child: `flex: grow shrink basis`.

- **`flex-grow`** (default 0): how greedily an item takes free space. `1` on
  one child makes it absorb the rest (the search box in a toolbar, the title
  beside fixed action buttons).
- **`flex-shrink`** (default 1): how readily an item gives space up. `0`
  stops a thing from being squashed (an icon, a button, an avatar). The
  combination `flex: 0 0 auto` means "stay your natural size".
- **`flex-basis`** (default `auto`): the item's size before growing or
  shrinking. `flex: 1 1 0` makes equal columns regardless of content;
  `flex: 1 1 240px` makes columns that are at least 240px then share the
  rest (a flex alternative to the grid card row when you want wrapping).
- **`margin-left: auto`** (or `margin-top: auto` in a column) pushes one item
  and everything after it to the far end: the way to send the last button to
  the right of a toolbar, or a card's action to the bottom of a `column`
  card so a row of cards still lines up (`ui-layout`).

### Two flex idioms worth memorising

Centre one thing, both axes:

```css
.centre { display: flex; align-items: center; justify-content: center; min-height: 100dvh; }
```

Title left, actions right, on one line, vertically centred:

```css
.bar { display: flex; align-items: center; gap: var(--space-3); }
.bar .title { flex: 1 1 auto; min-width: 0; }   /* takes the space, can shrink */
.bar .actions { flex: 0 0 auto; }                /* stays its size */
```

`min-width: 0` on the growing child is what lets a long title truncate
instead of pushing the buttons off the edge (`ui-layout`, section 8).

## 4. The named layouts, copy-ready

- **Centred column (a page's content)**: a block, not a flex or grid job.
  `max-width` plus `margin-inline: auto` (`ui-layout`'s `.container`).
- **Sidebar + content**: grid, `grid-template-columns: 240px minmax(0, 1fr)`.
  The `minmax(0, 1fr)` (not plain `1fr`) lets a wide table scroll inside the
  content instead of stretching the page (`ui-layout`, section 5).
- **Holy grail (header, sidebar, main, footer)**: grid with
  `grid-template-areas`, section 2 above.
- **Responsive card grid**: grid,
  `repeat(auto-fill, minmax(260px, 1fr))`, section 2.
- **Split (text beside media)**: grid, `grid-template-columns: 7fr 5fr` (or
  `1fr 1fr`), `align-items: center` or `start`. Stacks to one column under
  768px.
- **Toolbar (search grows, filters, view toggle)**: flex, `align-items:
  center`, the search `flex: 1 1 auto`, the rest `flex: 0 0 auto`.
- **Tag / button row that wraps**: flex, `flex-wrap: wrap`, a `gap`.
- **Form of label/field pairs that line up**: grid,
  `grid-template-columns: max-content 1fr` so every label column is as wide
  as the longest label and every field lines up. One column on a phone.
- **Media object (avatar beside text)**: flex, `align-items: flex-start`,
  the avatar `flex: 0 0 auto`, the text `flex: 1 1 auto; min-width: 0`.

## 5. With Tailwind

Every property above is a utility; the mechanics are identical.

- `grid grid-cols-[240px_minmax(0,1fr)]`, `grid-cols-3`, `gap-6`,
  `grid-rows-[auto_1fr_auto]`.
- The card grid: `grid grid-cols-[repeat(auto-fill,minmax(260px,1fr))] gap-6`.
- Spanning: `col-span-2`, `col-span-full`.
- Flex: `flex items-center justify-between gap-3`, `flex-col`, `flex-wrap`,
  `flex-1` (grow and shrink), `flex-none` (`flex: 0 0 auto`), `shrink-0`,
  `grow`, `ml-auto`, `mt-auto`, `min-w-0`.
- Named areas are uncommon in Tailwind; for a three-region shell write the
  grid in the component's CSS (or a `grid-template` arbitrary value) and keep
  the regions readable. The two-track shell is just `grid-cols-[...]`.
- The gaps and track sizes come from the theme tokens that hold `ui-layout`'s
  scale, not arbitrary pixels, except the deliberate fixed tracks
  (`ui-stack-tailwind`).

## 6. Common failures and the fix

- **Columns that do not line up**: margins and percentages instead of a
  grid. Replace with `grid-template-columns` in `fr`; delete the margins and
  use `gap`.
- **A card row with uneven heights**: let the grid or flex row stretch
  (`align-items: stretch`, the default) and make each card a `column` flex so
  its content fills and the action sits at the bottom with `margin-top:
  auto`.
- **One long word or a wide table tears the layout sideways**: the flex or
  grid child needs `min-width: 0` (Tailwind `min-w-0`); a `1fr` content track
  should be `minmax(0, 1fr)`.
- **Items crammed instead of wrapping**: a flex row needs `flex-wrap: wrap`,
  or the card grid wants `auto-fill` with a `minmax` floor.
- **Space distributed wrongly**: reaching for `justify-content: space-between`
  when one child should grow. Put `flex: 1` on that child instead, so the
  others keep their size.
- **A gap only on some sides**: spacing children with individual margins.
  Remove them; one `gap` on the container spaces all of them evenly.
- **Nested flex rows and columns to force a two-axis layout**: that is a
  grid. Flatten it to one `display: grid` with a template.

## 7. Check it

- Every column lines up with the ones in the sections above and below: one
  grid, one set of tracks, one `gap` (`ui-layout`, section 3).
- No child pushes past the container at 360px: `min-w-0` on text and table
  children, `minmax(0, 1fr)` on the content track (`ui-layout`, section 8).
- A row of cards shares one height and the actions line up along the bottom.
- The card grid reflows with the width and needs no media query.
- Spacing between items is the `gap`, from the scale, not per-child margins.
- The layout rearranges on a phone by changing the template or the
  direction, not by squeezing the wide-screen one (`ui-layout`, section 9).
