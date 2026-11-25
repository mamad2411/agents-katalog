---
name: ui-part-lists
description: "Lists of items: list, table or cards, the row's anatomy and measures, dividers or spacing, clickable rows, selection and bulk actions, sorting and grouping, listbox and grid keyboard patterns, drag to reorder, empty, loading and error states, and very long lists. Read before building or reworking a list of records, files, messages or people."
---

# Lists

The generated version: every row a card with a shadow, a divider and an
avatar circle; a green "Active" pill on each; three buttons at the end of
every row; the whole row a `div` with an `onClick`. A list is for scanning:
consistent rows with the most important field first, secondary details
quieter, and the one action where the eye ends. The principles are in the
`ui` skill, the measures in `ui-layout`, tables in `ui-part-tables`, cards
in `ui-part-cards`.

## 1. List, table or cards

| The items | Use |
|---|---|
| are compared on three or more fields (amounts, dates, statuses) | a table (`ui-part-tables`) |
| are recognised by their picture (products, places, photographs) | cards in a grid (`ui-part-cards`) |
| have a name and a line of detail (messages, clients, files, tasks) | a list |
| are pairs of label and value about one record | a description list, `dl` |
| have a rank or a sequence | an ordered list, `ol` |

- A list reflows at every width without effort, so on a phone it often
  replaces a table (`ui-part-tables`, narrow screens).
- Markup: `ul` or `ol` with `li`. With `list-style: none`, add
  `role="list"`: Safari drops the list semantics otherwise, and a screen
  reader stops saying "list, 24 items", which is how a listener learns the
  size.

## 2. The row

- Four slots: an optional leading visual, the title, one line of meta, and
  a trailing value or action.
- **Leading visual** only when it tells rows apart: a person's avatar in a
  list of people (32 to 40px, `ui-part-avatars`), a file type icon (20 to
  24px), a product thumbnail (40 to 48px, 1:1). Never the same icon on
  every row.
- **Title**: the identifying field (a name, a subject, an invoice number),
  14 to 16px, weight 500 to 600, one line, truncated with an ellipsis
  (`min-width: 0` on its container) and the full text reachable in the
  detail or a `title`.
- **Meta**: one line, 13 to 14px, in the muted colour: the one to three
  facts that help decide (a date, an amount, an exception), joined by a
  middle dot.
- **Trailing**: a value right-aligned in `tabular-nums`, or one quiet
  action, or a labelled menu (`ui-part-menus`); a chevron only where the
  row opens a page on a phone.
- **Height**: 48px for one line, 56 to 64px for two, 64 to 72px with an
  avatar; 36 to 40px with 14px text in a dense tool. 12 to 16px of side
  padding, 12px between the visual and the text.
- **Separation**: hairline dividers (1px `--border`, inset to the text when
  rows have a leading visual) or 8 to 12px of space between rows, not both
  heavy. Never dividers and cards and shadows on every row at once.
- Every row the same structure, the same field always in the same place.

## 3. States

- **Hover**: a surface step (`--surface-2`), only on clickable rows, under
  `@media (hover: hover)`.
- **Focus-visible**: the ring around the whole row while its link has focus.
- **Selected**: the checkbox checked and a tinted background, never colour
  alone.
- **Current** (its detail is open beside the list): `aria-current="true"`
  and a 2 to 3px bar at the start or a surface step.
- **Unread or new**: weight 600 on the title and a dot with visually hidden
  text ("Unread").
- **Unavailable**: muted, with the reason in the meta ("Archived 3 Oct").
- **Loading**: skeleton rows at the real row height, as many as usually
  arrive; never twenty grey bars for a list that holds three
  (`ui-part-loading`).
- **Empty**: in the list's place, why it is empty and the action that
  fills it (`ui-part-empty-states`).
- **Error**: in the list's place, what failed and a Retry button; rows
  already shown stay.
- **Loading more**: a "Show more" button or a spinner row at the end
  (`ui-part-pagination`).

## 4. Behaviour and keyboard

- **Clickable rows**: one real link on the title, stretched over the row by
  a pseudo-element; the row's other controls sit above it
  (`position: relative; z-index: 1`). Never an `li` or `div` with an
  `onClick`, never a link or a button nested inside a link.
- **Selection**: a checkbox at the start of each row (a 44px hit area on
  touch); "Select all" in the list's header, indeterminate for a partial
  selection; Shift+click selects a range. Once rows are selected, a bulk
  bar takes the toolbar's place: "3 selected", the bulk actions, "Clear
  selection" (`ui-layout`, section 4), the count announced with
  `role="status"`.
- **Sorting and grouping**: a Sort menu in the toolbar (Newest, Name,
  Amount). Groups under headings ("Today", "Earlier this week", or by
  status), each group a `section` with its heading and its own list; on
  long lists the group heading sticks below the top bar with a solid
  background.
- **Plain lists of links** need no ARIA and no arrow keys: Tab moves through
  the links.
- **Lists people choose from** (a select that stays open): the listbox
  pattern, `role="listbox"` and `option` with `aria-selected`, one Tab
  stop, arrow keys, Home and End, typeahead. **Rows holding several
  controls** that should move with arrow keys (a mail client): the grid
  pattern. Build both with React Aria's `ListBox` and `GridList` rather
  than by hand.
- **Drag to reorder**: a visible handle (a grip icon, a 44px target on
  touch, named "Reorder" plus the item) and a keyboard way: dnd-kit's
  `KeyboardSensor` with `sortableKeyboardCoordinates` and its screen reader
  announcements, or Move up and Move down in the row's menu. Pragmatic drag
  and drop or SortableJS outside React. The order saves at once and can be
  undone.
- **Swipe actions** on phones only as a shortcut to actions that are also in
  the row's menu.

## 5. Very long lists

- Paginate on the server first (`ui-part-pagination`). More than a few
  hundred rows on screen at once are virtualised: TanStack Virtual
  (`useVirtualizer` with `count`, `getScrollElement`, `estimateSize` and
  `overscan`; `measureElement` when heights vary).
- Virtualised rows are missing from find in page and from the screen
  reader's count: set `aria-setsize` and `aria-posinset` on each item, and
  offer search or filters.
- Scroll restoration: back to the list lands on the same row. Keep the
  loaded pages in the query cache and the offset per URL (the virtualiser's
  `initialOffset`), never a jump to the top.
- For a few hundred rows, `content-visibility: auto` with
  `contain-intrinsic-size: auto 56px` on each row skips rendering what is
  off screen and keeps find in page working.

## 6. Content

- The identifying field first, then what decides; secondary details
  quieter.
- Meta states the exception, not the norm: no "Active" on every row;
  "Overdue · 2 days" where it applies, in words as well as colour.
- Recent dates relative ("2 hours ago") with the exact time in a
  `<time datetime>` (`ui-part-dates`); amounts with their currency.
- No label repeated on every row ("Email: …"): the value says what it is.
- Real rows, or the empty state; never "John Doe" and "Acme Inc" left in.

## 7. Phones, themes and motion

- Rows stay rows: the trailing value moves under the title, row actions
  fold into the menu, targets reach 44px, nothing appears on hover only.
- Themes: hover, selected and current are surface steps from tokens,
  visible in both themes (`ui-themes`).
- Motion: an added item fades in while its height opens, a removed one
  fades and closes, a reorder moves with FLIP (`motion-interface`, section
  9). No staggered entrance on every load, no per-row animation on long
  lists.

## 8. A sketch (React)

```tsx
<ul role="list" className="rows">
  {clients.map((client) => (
    <li key={client.id} className="row">
      <Avatar person={client} size={40} />
      <div className="row-text">
        <a className="row-link" href={`/clients/${client.id}`}>{client.name}</a>
        <p className="row-meta">{client.summary}</p>
      </div>
      <span className="row-value">{formatMoney(client.balance)}</span>
      <RowMenu label={`Actions for ${client.name}`} client={client} />
    </li>
  ))}
</ul>
```

```css
.row {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-height: 56px;
  padding: var(--space-2) var(--space-4);
}
.row + .row { border-top: 1px solid var(--border); }
.row-text { flex: 1; min-width: 0; }
.row-link, .row-meta { display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.row-link { font-weight: 600; color: var(--text); text-decoration: none; }
.row-link::after { content: ""; position: absolute; inset: 0; } /* the row opens the record */
.row-link:focus-visible { outline: none; }
.row:has(.row-link:focus-visible) { outline: 2px solid var(--focus); outline-offset: -2px; }
.row-meta { color: var(--text-muted); font-size: var(--font-sm); }
.row-value { font-variant-numeric: tabular-nums; white-space: nowrap; }
.row :is(button, input) { position: relative; z-index: 1; }
@media (hover: hover) { .row:hover { background: var(--surface-2); } }
```

## Check it

- Keyboard: Tab reaches each row once (its link), then its menu; a listbox
  or grid is one Tab stop driven by the arrows; Space toggles a focused
  checkbox.
- A screen reader says "list, N items", and each row's name once: the
  link's name is the title, not the whole row read out.
- Try 0, 1, 3 and 500 items, an 80-character name and a throttled network:
  the empty state, an ellipsis rather than an overflow, skeleton rows
  replaced without a jump (`preview` with `motion: true` reports layout
  shift).
- `preview` at 360px: no overflow, row menus named, targets at 44px.
  `ui_check` flags "John Doe" and "Acme Inc" rows left in.

## Avoid

Dividers and cards and shadows on every row at once; an avatar or icon
that is the same on every row; the same badge on every row; three buttons
repeated on every row; clickable `div`s; links nested in links; rows of
different heights for the same content; truncation with no way to read the
rest; twenty skeleton bars for a list of three; drag to reorder with no
keyboard way; a long list that loses its place on back.
