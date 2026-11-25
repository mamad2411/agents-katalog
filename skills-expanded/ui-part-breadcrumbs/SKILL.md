---
name: ui-part-breadcrumbs
description: "Breadcrumbs: when a hierarchy needs them and when it does not, the nav and list markup with the current page, separators screen readers skip, placement and type, labels, long trails, the phone version, building them from routes, and structured data. Read before adding breadcrumbs to a page or screen."
---

# Breadcrumbs

The generated version: "Home / Page" on a site two levels deep, a trail
that repeats the navigation right above it, separators read aloud as
"slash", the current page as a link to itself, and a trail that runs off a
phone's edge. Breadcrumbs answer one question, where am I in this
hierarchy and how do I go up, and only deep structures ask it. One part of
an interface: the principles (direction, spacing, type, colour, icons,
states, accessibility) are in the `ui` skill, the measures in `ui-layout`,
their place above the title in `ui-part-page-header`.

## 1. When to use them

- For hierarchies more than two levels deep: documentation, a catalogue
  (Furniture, Tables, a table), a file tree, nested records in an
  application (Clients, a client, Projects, a project).
- Not for a flat site or a hierarchy of two levels, where the header's
  navigation already says where you are.
- Not for steps in order (checkout, onboarding): that is a step indicator
  with done, current and next.
- Location, not history: the trail shows where the page sits, whatever
  route the user took to reach it. For "back to my search results", a
  back link that keeps the query.
- Not on the top level itself.

## 2. Markup

- A `nav` with `aria-label="Breadcrumb"` around an ordered list, one `li`
  per level, each ancestor a link to its page.
- The current page last and not a link: a `span` with
  `aria-current="page"`. Some design systems leave it out because the
  `h1` sits right below; keep it when the trail wraps or truncates, so the
  end of the path is never in doubt.
- Separators drawn by CSS or an `aria-hidden` icon, never typed into the
  text: a screen reader hears "Clients, link. Projects, link", not
  "slash".
- No keyboard handling of its own: the links are in the Tab order, and
  that is all.

## 3. Anatomy and measures

- Above the page title, 8 to 12px over it, its left edge on the content's
  line.
- 13 to 14px, one step below body; ancestors in the muted colour at 4.5:1,
  the current page in the text colour.
- Links underlined quietly (a 1px underline in the border colour that
  turns to the text colour on hover), so they are told apart from the
  current page by more than colour.
- Separators in the muted colour: a chevron (12 to 16px) or a slash, with
  4 to 8px either side, the same one everywhere.
- The first crumb is the first level that means something: "Docs",
  "Clients". A "Home" crumb only on a public site with a deep tree; a house
  icon alone needs `aria-label="Home"`.
- A focus ring on each link (2px `--focus`, 2px offset); the target is at
  least 24px tall, 44px on touch.

## 4. Labels

- Each label is the title of the page it links to (its `h1`), shortened
  when long: "Invoice INV-0042" can be "INV-0042".
- Record names come from the data. While they load, a short skeleton in
  the crumb; never "undefined", a bare id, or a jump when the name arrives.
- A label longer than about 24 characters truncates with an ellipsis at a
  maximum width, the full name in `title`; the current page truncates last.
- Labels go through i18n like any text (`i18n`). In right-to-left
  languages the list runs right to left by itself; a chevron is mirrored
  (`scale: -1 1` under `[dir="rtl"]`), a slash needs nothing.

## 5. Long trails and phones

- More than 4 or 5 levels: keep the first and the last two, and collapse
  the middle into a "…" button (`aria-label="Show hidden levels"`,
  `aria-haspopup="menu"`, `aria-expanded`) that opens a menu of them
  (`ui-part-menus`).
- On a phone the trail becomes one link to the parent, "‹ Orders" or "Back
  to Orders", above the title. It links to the parent's URL, not
  `history.back()`, so it never leaves the site or lands on a search page.
- Or, on a docs site, the whole trail on one line that scrolls sideways in
  its own container, scrolled to its end. Never three wrapped lines above
  the title, never past the edge.

## 6. Building them from routes

- From the route tree, not by hand on each page. React Router: a
  `handle.crumb` on each route, collected with `useMatches()`. Next.js App
  Router: `useSelectedLayoutSegments()` with a label per segment, record
  names fetched in the layout.
- Library parts carry the markup above: shadcn's Breadcrumb (with its
  ellipsis), React Aria `Breadcrumbs`.

## 7. Structured data

- On public sites, a `BreadcrumbList` in JSON-LD with the same trail as
  the page: each `ListItem` with `position`, `name` and `item` (its URL);
  the last may leave `item` out.
- Only the trail that is on the page. Validate it with Google's Rich
  Results Test.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Furniture", "item": "https://example.com/furniture" },
    { "@type": "ListItem", "position": 2, "name": "Tables", "item": "https://example.com/furniture/tables" },
    { "@type": "ListItem", "position": 3, "name": "[Product name]" }
  ]
}
</script>
```

## 8. Themes and motion

- The muted colour passes 4.5:1 in both themes; chevrons are icons in
  `currentColor` (`ui-themes`).
- No motion: a trail does not slide or fade in (`motion-interface`).

## 9. A sketch

```html
<nav aria-label="Breadcrumb" class="crumbs">
  <ol>
    <li><a href="/clients">Clients</a></li>
    <li><a href="/clients/42">[Client name]</a></li>
    <li><a href="/clients/42/projects">Projects</a></li>
    <li><span aria-current="page">[Project name]</span></li>
  </ol>
</nav>
```

```css
.crumbs ol {
  display: flex; flex-wrap: wrap; align-items: center; gap: 4px 8px;
  margin: 0; padding: 0; list-style: none;
  font-size: 14px; color: var(--text-muted);
}
.crumbs li { display: inline-flex; align-items: center; gap: 8px; min-inline-size: 0; }
/* The second value is the alt text: empty, so the separator is not read. */
.crumbs li + li::before { content: "/"; content: "/" / ""; }
.crumbs a {
  color: inherit; text-decoration-line: underline;
  text-decoration-thickness: 1px; text-underline-offset: 0.2em;
  text-decoration-color: var(--border-strong);
}
.crumbs a:hover { text-decoration-color: currentColor; }
.crumbs a:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.crumbs [aria-current="page"] { color: var(--text); }
@media (max-width: 640px) {
  .crumbs li:not(:nth-last-child(2)) { display: none; }
  .crumbs li:nth-last-child(2)::before { content: "‹"; content: "‹" / ""; }
  .crumbs a { display: inline-flex; align-items: center; min-block-size: 44px; min-inline-size: 44px; }
}
```

## Check it

- `preview` at 360px: the trail neither wraps into a block nor pushes the
  page wider; its link is not in "touch targets under 44px"; at 1440px it
  starts on the title's left edge.
- A screen reader announces the "Breadcrumb" landmark, skips the
  separators, and reads the last item as the current page.
- Follow every crumb: each label matches the `h1` of the page it opens.
- On a public site the Rich Results Test reads the `BreadcrumbList`
  without errors, with the names of the visible trail.

## Avoid

Breadcrumbs on a flat site; "Home / Page" alone; a trail that repeats the
navigation; the current page as a link to itself; separators read aloud;
a history trail instead of a location; crumbs named differently from the
pages they open; "undefined" or an id while a name loads; a trail wrapping
onto three lines or running off a phone; breadcrumbs in place of a step
indicator; large, bold or coloured crumbs competing with the title.
