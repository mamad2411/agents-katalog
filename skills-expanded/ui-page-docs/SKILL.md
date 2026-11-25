---
name: ui-page-docs
description: "How to build documentation and long articles: the three-column layout with a navigation tree, text at 65 to 75ch and an on-this-page list, search with a keyboard shortcut, versions, code blocks with copy buttons and tabs, callouts, API reference pages, heading anchors, edit and last-updated links, the phone drawer, both themes, and the four kinds of docs. Read before building or reworking a docs site, a docs page or an article."
---

# Documentation or article

A generated docs site is a landing page that lost its way: a gradient hero
on the docs home, a flat alphabetical sidebar, text across a wide screen, a
search box that searches nothing, code blocks that copy the `$` with the
command, a callout on every paragraph, a dark code theme glaring on a light
page, pages half tutorial, half reference. Readers arrive from a search or
mid-task, want one answer and leave; this skill is the layout that serves them.

One kind of page. The measures are in `ui-layout`, its parts (header,
search, tabs, drawers, breadcrumbs, back to top) in their `ui-part-*`
skills, what to write and how to split it in the `docs` skill.

## 1. Four kinds of page

Each page is one kind (the Diátaxis split, `docs`), and the kind sets its
shape. A page that mixes them serves nobody.

| Kind | The reader asks | Its shape |
|---|---|---|
| Tutorial | "Teach me" | One path, numbered steps, each ending in a visible result |
| How-to guide | "How do I rotate a key?" | Title as the task, prerequisites, steps, variations |
| Reference | "What does this option take?" | Tables and signatures, the same layout for every entry |
| Explanation | "Why does it work like this?" | Prose and diagrams, no steps |

The navigation groups pages by kind, or by topic with the kinds inside.
The docs home routes by task: one line on what the product is, Install and
Quick start first, each section with one line, no marketing.

## 2. The skeleton

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ◉ Docs   Guides  Reference  API  Changelog   [⌕ Search docs  ⌘K]  v3▾ ◐ │ sticky
├───────────────┬──────────────────────────────────────────┬──────────────┤
│ Get started   │ Guides / Deploy                          │ On this page │
│   Install     │ Deploy to a server                       │ Requirements │
│   Quick start │ One line on what this page gets you to.  │ ▌Build       │
│ Guides        │                                          │ Configure    │
│ ▌ Deploy      │ Requirements                           # │ Run          │
│   Environment │ Text at 65 to 75ch, 16 to 18px.          │              │
│ Reference     │ ┌ npm │ pnpm │ yarn ─────────── Copy ┐   │ Edit page    │
│   CLI         │ │ npm install product-cli            │   │              │
│   Config      │ └────────────────────────────────────┘   │              │
│               │ ▍Note: one sentence, where it matters.   │              │
│               │ ← Install                  Environment → │              │
│               │ Edit this page · Updated 12 Sep 2026     │              │
└───────────────┴──────────────────────────────────────────┴──────────────┘
```

- Header 56 to 64px: the name to the docs home, the sections, search, the
  version switcher (only with versions), the theme toggle, the repository.
- Three columns on wide screens: navigation 240 to 280px on the left, the
  text at 65ch (65 to 75) in the middle, the "on this page" list (200 to
  240px) on the right, hidden below 1200px. Code blocks full width of the
  text column.
- The header sticks, and both side columns stick under it (`position:
  sticky` with `top` set to the header's height), each scrolling on its own
  when it is taller than the screen; `scroll-padding-top` keeps a heading
  reached by its anchor clear of the header.

```css
html { scroll-padding-top: calc(var(--header-h) + 16px); }
.docs { display: grid; gap: 48px; padding-inline: 24px;
  grid-template-columns: 260px minmax(0, 1fr) 220px; }
.docs-nav, .docs-toc {
  position: sticky; top: var(--header-h);
  align-self: start; /* a stretched grid item has no room to stick */
  max-height: calc(100dvh - var(--header-h));
  overflow-y: auto; overscroll-behavior: contain;
}
.docs-article { max-width: 70ch; }
@media (max-width: 1199px) {
  .docs { grid-template-columns: 240px minmax(0, 1fr); }
  .docs-toc { display: none; } /* a collapsible list in the article instead */
}
@media (max-width: 1023px) {
  .docs { grid-template-columns: minmax(0, 1fr); }
  .docs-nav { display: none; } /* the same tree, as a drawer */
}
```

## 3. The navigation tree

- Groups under short headings (not links), two levels, three at most, in
  the reader's order (install, then the first task), not the alphabet;
  labels are the pages' titles, with no icon on every item. Several areas:
  the areas in the header, the sidebar holding the current one's tree.
- The current page marked by weight and a bar, with `aria-current="page"`;
  its group open; collapsible groups are buttons with `aria-expanded`. On
  load the current item scrolls into view inside the nav
  (`scrollIntoView({ block: "nearest" })`), not the page.

## 4. The page

- Breadcrumbs, the `h1` (the nav label's words), then one line on what the
  page gets the reader to (it doubles as the meta description). Text 16 to
  18px at a line height of 1.6 to 1.7; ordered lists for steps, tables for
  options.
- `h2` and `h3` (an `h4` rarely), each with a stable `id` and an anchor
  link shown on hover and focus (always, on touch), named "Link to this
  section". Renaming a heading breaks links to it: keep the old id on an
  empty element when the page is widely linked.
- "On this page" lists the `h2` and `h3` and marks the section being read
  (one IntersectionObserver, `aria-current="true"`).
- At the end: previous and next as two blocks (the direction and the
  title), "Edit this page" to the source file in the repository, "Updated
  12 Sep 2026" from the file's last commit at build time in a `<time>`, and
  "Was this helpful?" only when someone reads the answers.

## 5. Search

- In the header on every page: a button drawn as a field ("Search docs"
  and the shortcut, `⌘K` on Apple, `Ctrl K` elsewhere) opening a dialog
  with the combobox pattern: arrows move, Enter opens, Escape closes and
  returns focus. `Ctrl+K` or `Cmd+K` open it, and `/` when focus is not in
  a text field; never take a key the reader is typing into an input.
- Results: page title, heading and a snippet with the match marked, linking
  to the anchor; when empty, the query and what to try. With versions,
  search the reader's version only.
- **Pagefind** for static sites: indexes the built HTML (`npx pagefind
  --site dist`), loads its index in chunks, needs no server, is built into
  Starlight; `data-pagefind-body` on the content, `data-pagefind-ignore` on
  repeated parts. **Algolia DocSearch**: free for public technical docs, a
  crawler plus `@docsearch/js`, its search-only key public by design.

## 6. Code blocks

- Highlighted at build time (Shiki, or Expressive Code in Starlight), a
  theme per mode (`github-light`, `github-dark`) switching with the page
  (`ui-themes`); comments at 4.5:1, which many themes miss.
- The language or the file name as the block's title; a Copy button at the
  top right, visible on hover, on focus and always on touch, turning to
  "Copied" through `aria-live="polite"`.
- The copied text is what runs: no `$` prompt (leave it out, or draw it
  with CSS), no line numbers, one command per line, output in its own block
  labelled Output.
- Tabs per package manager (npm, pnpm, yarn, bun) or language (curl,
  TypeScript, Python), synced across the page and remembered in
  `localStorage` (`ui-part-tabs`).
- Highlight the lines the text discusses (`{2-4}`, added and removed);
  line numbers only when the text cites them.
- Long lines scroll inside the block (`overflow-x: auto`, and `tabindex="0"`
  with a name on a scrolling `pre`). Examples run as written: real values,
  or placeholders that say so (`<your-api-key>`), never a real secret.

## 7. Callouts

- Note, tip, warning (danger for what cannot be undone), one or two per
  screen at most: a page of boxes has no emphasis. A warning that belongs
  to a step goes in the step.
- The kind in words ("Warning") first, a left rule or tinted surface from
  the status tokens, an icon optional; a `div` with `role="note"` rather
  than an `aside` per callout, which some screen readers list as landmarks.

## 8. API reference

```
│ POST /v1/orders                        │ ┌ curl │ TypeScript │ Python ┐ │
│ Creates an order. Scope: orders:write  │ │ curl -X POST .../v1/orders │ │
│ Body                                   │ └────────────────────────────┘ │
│ items      array    required  ...      │ ┌ 201 │ 400 │ 409 ───────────┐ │
│ note       string   optional  ...      │ │ { "id": "ord_...", ... }   │ │
```

- Parameters on the left; examples on the right, sticky on wide screens,
  after the parameters below 1200px. The method as text (not colour alone),
  the path in monospace, one line on what it does, auth and scopes.
- Parameters grouped by where they go (path, query, header, body): name,
  type, required in words, default, allowed values; nested objects expand.
- Examples in curl first, then the languages users use, with realistic
  values; every response status with its body; errors, pagination and rate
  limits explained once and linked.
- Generated from the OpenAPI document (Scalar, Redoc, Stoplight Elements)
  so it cannot drift, with written guides around it (`docs`).

## 9. Versions

Only when readers run old versions (libraries, self-hosted software); a
hosted product with one live version has no switcher. The switcher sits in
the header or atop the nav and keeps the reader on the same page when it
exists. The latest lives at `/docs/...`, older ones at `/docs/v2/...` with
a banner ("These docs are for v2. The current version is v3.") linking to
the same page; old versions are `noindex` or canonical to the latest.

## 10. On a phone

- Under 1024px the tree is a drawer from the left behind a labelled "Menu"
  button in the sticky header, opening at the current page and closing when
  a link is chosen (`ui-part-drawers`). Under 1200px "On this page" is a
  collapsed `details` under the title; search is a named icon button.
- Text 16 to 17px, side padding 16 to 20px; code and tables scroll in their
  own containers; tabs scroll or become a select; previous and next stack
  full width; a back-to-top control (`ui-part-back-to-top`).

## 11. Themes, speed and search engines

- Both themes, following the system, with a toggle: code, callouts,
  diagrams (drawn from tokens) and screenshots checked in each
  (`ui-themes`). Static HTML that reads without JavaScript; search, tab
  syncing and copy are enhancements; the index loads when search opens.
- Titles "Page title · Product docs" within 60 characters, the one-line
  summary as the description, canonical URLs, a sitemap, `BreadcrumbList`
  data, readable paths (`/docs/guides/deploy`), a 301 for every page that
  moves (`frontend-seo`). Starlight gives most of this (`ui-stack-astro`).

## 12. An article

No tree: one column of 60 to 75ch, body 17 to 20px at a line height of
1.6, the title large; a byline with the author and the published and
updated dates; a sticky table of contents on the right for long pieces;
figures wider than the text, with captions; footnotes; related pieces; a
feed. A long article has a back-to-top control (`ui-part-back-to-top`).

## Check it

- `preview` at 360, 768 and 1440px: nothing overflows from code or tables,
  the drawer works, the right column shows only from 1200px, the header and
  columns stick, long pages have a way back to the top.
- Follow three anchors (each lands below the header); search a term from a
  deep page; press `/` in a text field and see it typed; paste a copied
  block into a terminal and see it run; switch the theme.
- Keyboard: skip link, tree, tabs with arrow keys, search dialog, copy.
- View the source (the text is in the HTML); run a link checker (lychee, or
  the generator's own) and `ui_check`.

## Avoid

A hero, testimonials or pop-ups on docs pages; a flat alphabetical sidebar;
text across the full width; a search that finds nothing; `$` and line
numbers in copied code; highlighting that flashes in after load; one dark
code theme for both modes; a callout on every paragraph; a tutorial that
turns into a reference table halfway; a version switcher with one version;
old versions indexed; screenshots older than the interface; a wrapper with
`overflow: hidden` that stops the columns sticking.
