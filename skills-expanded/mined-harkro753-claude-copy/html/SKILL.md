---
name: html
description: >
  Clone a captured website into pixel-verified static HTML — a capture session
  (pages.json plus one folder per page holding ref.png, source.html,
  computed.json, meta.json) becomes one page.html per route, sharing a shell, a
  stylesheet, a glyph set and a token scale, where every route's `check` exits 0
  against its own reference screenshot. Use whenever the user points at a
  capture session, a pages.json, or one or more page folders and wants them
  copied, replicated, rebuilt or cloned — "clone this dashboard", "copy this
  landing page", "1:1", "pixel perfect", "rebuild this UI" — even if they name
  only one folder inside a session and even if they never say "pixel perfect".
  Prefer the react skill instead when the deliverable is a real component tree
  with behaviour (hover, focus, keyboard nav) rather than a static page.
---

# clone:html — capture session → verified static routes

**In:** a session folder — `pages.json` + one folder per page holding `ref.png`,
`source.html`, `computed.json`, `meta.json`.
**Out:** `<slug>/page.html` per route, sharing `shared/*.css` and one glyph set,
where every route's `check` exits 0 against its own `ref.png`.

Work **in place** in the session folder (copy it under `apps/<name>/` first if
it isn't already there). Everything the loop needs lives on disk, so any phase
can be re-run and any cycle handed to a fresh subagent.

**Read [`references/pipeline.md`](../../references/pipeline.md) first** — the
CLI, the phases, the loop discipline and the four hard nevers are there and are
not repeated here. This file is only what differs for static HTML.

```
clone prep <session> --target html
clone extract | resolve | cluster | check
```

## Why static HTML, and when not to

A route is a file. No toolchain, no server, no build — the loop is edit and
recheck with nothing in between, and the output is something anyone can open.
That is the whole appeal, and for a landing page or a marketing site it is the
right answer.

It is the wrong answer when the thing you are cloning has **behaviour**. A
screenshot is the resting frame of components that do things: a command palette
cloned as HTML is a `div` with a fake list. Hover, focus rings, disabled states
and keyboard nav are real parts of the original and none of them are in
`ref.png`. When the deliverable needs those, use `clone:react`.

## Authoring

One `page.html` per route, plus `shared/shell.css` (and `shared/components.css`
if it earns its own file), linked relatively — **`base.css` first, always**:

```html
<link rel="stylesheet" href="../shared/base.css">
<link rel="stylesheet" href="../shared/shell.css">
```

- **Author in CSS px.** Every number in `layout.md` is CSS px and goes straight
  into the HTML. `check` renders at the capture's device pixel ratio and scales
  for you — never double numbers for a retina reference.
- **`margin:0`, exact canvas size, no responsive units.** One width, one page.
- **Flow layout, not absolute coordinates.** `layout.md` gives you
  `display:flex`, `gap`, `padding`, `align-items` — the page was built that way
  and reproducing it that way is what makes the output worth keeping. Reach for
  `position:absolute` only where the capture says so.
- **A repeated recipe becomes a class.** Same six properties on thirty rows is
  one `.row` class; inline `style=` is for the single value that differs per
  instance. This is what lets a fix subagent change one thing in one place.
- **Icons are `<img>`, never inline SVG.**
  `<img class="ico" src="../shared/icons/ready/search-444342.svg">` — `resolve`
  has already produced that file at that colour. An `<img>` renders identically
  to inline SVG (measured: same ink, same bounding box) and keeps a route free of
  SVG source, which is most of a page's bulk: on the Tailscale clone it took two
  routes from 59 KB to 35 KB. Every one of those bytes is context an author and a
  fix subagent would otherwise carry for markup they never edit.
  - **Size icons in whole pixels.** An `<img>` rasterises at its device size, so
    `1.25em` (17.5px) rounds up where an inline SVG drew 17.
  - The colour is baked in, so `color:` no longer reaches an icon — pick the file
    whose suffix matches the colour `layout.md` shows for that box.
  - Author from `shared/icons.md` rather than swapping icons in afterwards.
- **Hover/active go in `shell.css`, on the class.** Where `layout.md` shows
  `hover{background-color:#f7f7f8}` those are the source's own rules, read out of
  its stylesheets. Only changed properties are listed, so each one is a real
  difference. `check` screenshots the resting state and drives each hover
  separately — copy what is listed and invent nothing beyond it.
- **Fonts local or not at all.** If `shared/fonts.json` lists files,
  `@font-face` them with a relative `url()` — a CDN `<link>` silently no-ops in
  headless Chromium and every text run drifts 7–30% wide, so `check` refuses to
  run when the declared family didn't load. A system stack needs nothing.
- **Nothing is a slice of `ref.png`.** Charts are SVG, banners are HTML/CSS,
  gradients are CSS. A photograph you cannot rebuild becomes a neutral
  placeholder block in a palette colour. If the render is only right because it
  contains the reference, the clone is worth nothing.

Author routes in parallel with one subagent each **only after** the shell and
shared CSS exist — separate files make parallel writes safe; the shared
stylesheet is not, and edits to it serialize.

## Accept

Every route at `0 failing`. Then the link pass: for each `<a>` whose target
matches another route's URL, point it at `../<slug>/page.html`; uncaptured
targets get `href="#"`. Re-run `check` afterwards — hrefs paint no pixels, so it
is a free regression gate. Report the per-route match and the crops that
mattered.

A route whose only remaining failures are "Not asserted" boxes — photographs,
swapped brand art, anything animated at capture time — is **done**. Say so with
the reason; do not keep grinding on a box that cannot converge.
