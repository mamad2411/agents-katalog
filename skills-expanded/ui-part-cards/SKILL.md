---
name: ui-part-cards
description: "Cards and feature lists: when a card is the right unit and when a list, a table or nothing is, anatomy and measures, the whole-card link, grids and equal heights, hover, selected, loading, empty and error states, and the phone layout. Read before building cards, a card grid or a feature list."
---

# Feature lists and cards

The generated version: three identical cards, each an icon in a coloured
circle over "Lightning fast", "Secure" and "Scalable"; a card around every
paragraph; cards that scale and tilt under the cursor; a whole card
wrapped in a link with a button inside it. A card is a unit with its own
action, or the summary of one record. This is how to tell when that is
true, and how to build one that reads, links and aligns. One part of an
interface: the principles (direction, spacing, type, colour, icons,
states, accessibility) are in the `ui` skill, the measures in `ui-layout`.

## 1. Card, list, table or nothing

- Cards for parallel, self-contained items a user compares or picks from,
  above all with an image: products, projects, templates, places, people.
- A list with a short line each is usually clearer: for items scanned by
  name, and for features (`ui-part-lists`).
- A table when items are compared on the same fields (`ui-part-tables`).
- Nothing when the content is a section of a page: a heading, text and a
  hairline, not a box (`ui-part-sections`). A card around every paragraph
  is noise, not structure; a card inside a card means one is not needed.

## 2. Features are not cards

- Emphasis follows importance: the main feature larger, or shown with a
  real screenshot or its output, and the rest listed as rows (a name and
  one line each) or in a split beside it.
- An icon only when it helps recognition, from the product's one set, at
  the size of the text beside it, with no coloured circle behind it.
- Each feature says the concrete thing ("Imports bank statements in CSV
  and OFX"), not an adjective ("Lightning fast", "Secure", "Scalable").

## 3. Anatomy and measures

- In reading order: media (optional), title, meta, a short text, actions.
- Media at a fixed ratio with `aspect-ratio` and `object-fit: cover`: 16/9
  for screenshots, 4/3 or 1/1 for products, 3/2 for photographs; real
  images only (`ui-part-images`).
- Title 16 to 20px, weight 600, two lines at most; meta 13 to 14px in the
  muted colour; the text 14 to 16px, clamped at two or three lines.
- Padding 16 to 24px (16px on phones), radius from the token set (8 to
  12px), a 1px border or one surface step from the page, not a heavy border
  and a large shadow together. A shadow only on a card that floats: being
  dragged, or over other content.
- Actions at the bottom, pushed down (`margin-block-start: auto` in a flex
  column) so they line up across a row; the record's other actions in a
  menu at the top right (`ui-part-menus`).
- The title is a heading at the section's next level (an `h3` under an
  `h2`), so screen reader users can jump from card to card. It comes first
  in the markup even when the image shows above it (`order: -1` on the
  media).

## 4. The whole card as a link

- A card that is a link is one link: the title's link, stretched over the
  card with a pseudo-element, and `position: relative` on the card. The
  link's name is the title: short and clear.
- Never the whole card wrapped in `<a>` (the link reads as everything in
  it, and nothing inside may be a button), never a button nested inside a
  link, never a `div` with a click handler that pushes a route (no middle
  click, no new tab, no keyboard).
- Other controls inside (a menu, a tag link, a favourite button) sit above
  the overlay with `position: relative; z-index: 1` and have their own
  names. Two targets besides the card itself are the limit.
- The focus ring draws on the overlay, round the whole card.
- Text under the overlay cannot be selected; when copying matters (an
  address, a code), link only the title.

## 5. Grids and heights

- `grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr))`
  with 16 to 24px gaps: 2 to 4 columns on wide screens, one on a phone.
  `auto-fill` keeps a lone last card as wide as the others; `auto-fit`
  would stretch it across the row.
- Equal heights come from the grid, content aligned to the top: items
  stretch to the tallest in their row by default. `align-self: start` on a
  card that should keep its own height.
- Titles, prices and buttons on one line across cards: each card spans the
  rows it holds and sets `grid-template-rows: subgrid`.
- Never pad a grid with invented items to fill the last row.
- One size for the cards of a grid: the width comes from the grid's tracks
  (never a `width` on the card), and every card has the same padding,
  radius, border and media box (`aspect-ratio: 16 / 9` or `4 / 3` on the
  image wrapper, `object-fit: cover` on the image), so a tall photo or a
  long title never makes one card a different shape.
- The card is a flex column (`display: flex; flex-direction: column; gap:
  8px`); its action or price sits at the bottom with `margin-top: auto`, so
  they line up across the row whatever the text above them.
- The gap between cards is the grid's `gap`, 16px or 24px, the same both
  ways; never margins on the cards.

## 6. States

- Hover only when the card is clickable: the border to `--border-strong`
  or one surface step, at most a 2px lift. A card that is not a link does
  not react. No scale, no tilt, no glow.
- Focus-visible: a 2px ring round the card, from the overlay.
- Selected (picking a plan, a template): the card is the label of a radio
  or a checkbox, with a 2px accent border and a check icon when chosen,
  not colour alone (`ui-part-choices`).
- Unavailable: says why on the card ("Sold out, back on 12 October"), not
  only greyed out.
- Loading: skeletons the size of the card (the media box at its ratio, two
  lines of text), after about 200ms, replaced without a jump
  (`ui-part-loading`).
- Empty: the grid's place holds one line on why, and the action that fills
  it: "No projects yet. Create one to see it here."
- Error: a failed image leaves a surface with the item's initial, not a
  broken-image icon; failed data shows the error and a retry in the grid's
  place.

## 7. Phones, themes, motion

- One column at 360px with 16px gaps; or, for a secondary shelf, a row that
  scrolls sideways (`scroll-snap-type: x mandatory`) with cards at 80 to
  85% of the width so the next one shows. Never a carousel that advances
  by itself.
- The whole card is the target, so it is large; controls inside it still
  get 44px.
- Themes: on dark a card is one surface step lighter with a hairline,
  since shadows barely show (`ui-themes`).
- Motion: hover and press as in `motion-interface`; cards on an
  application screen do not fade up one by one.

## 8. A sketch

```html
<ul class="cards" role="list">
  <li class="card">
    <h3 class="card__title"><a class="card__link" href="/work/[slug]">[Project name]</a></h3>
    <img class="card__media" src="/work/[slug].webp" alt="" width="640" height="360">
    <p class="card__meta">[Client] · [Year]</p>
    <p class="card__text">[One or two sentences on what it is and did]</p>
  </li>
</ul>
```

```css
.cards {
  display: grid; gap: 24px; margin: 0; padding: 0; list-style: none;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
}
.card {
  position: relative; display: flex; flex-direction: column; gap: 8px;
  padding: 16px; background: var(--surface);
  border: 1px solid var(--border); border-radius: var(--radius);
}
.card__media {
  order: -1; inline-size: 100%; block-size: auto; aspect-ratio: 16 / 9;
  object-fit: cover; border-radius: calc(var(--radius) - 4px);
}
.card__link { color: inherit; text-decoration: none; }
.card__link::after { content: ""; position: absolute; inset: 0; border-radius: var(--radius); }
.card__link:focus-visible { outline: none; }
.card__link:focus-visible::after { outline: 2px solid var(--focus); outline-offset: 2px; }
@media (hover: hover) {
  .card:has(.card__link:hover) { border-color: var(--border-strong); }
}
.card__text {
  display: -webkit-box; -webkit-box-orient: vertical;
  -webkit-line-clamp: 3; overflow: hidden;
}
```

The image is `alt=""` because the title names the item; describe it only
when it shows something the text does not.

## Check it

- `preview` at 360, 768 and 1440px: one column on a phone, nothing wider
  than the screen, text on cards at 4.5:1 in both themes. It reports the
  same tall block stacked four or more times: expected in a catalogue's
  grid on a phone, a template when the blocks are the page's features or
  sections (`ui-part-sections`).
- `ui_check`: the generic feature icons (sparkles, rocket, lightning),
  heavy shadows everywhere, glow, and invented figures on cards.
- Keyboard: Tab reaches each card once, the ring surrounds the whole card,
  inner controls are separate stops; Enter opens the item.
- A screen reader lists the cards by their headings and reads each link as
  the title alone.
- Middle-click a card: it opens in a new tab.

## Avoid

Three identical cards with an icon in a coloured circle each; a card
around every paragraph; "Lightning fast / Secure / Scalable"; cards that
scale, tilt or glow on hover; a hover effect on cards that are not links;
a whole card wrapped in a link with buttons inside; a `div` with a click
handler for navigation; ragged action rows; skeletons shaped unlike the
card; invented items filling a grid; cards inside cards.
