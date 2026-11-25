---
name: ui-part-links
description: "Links that look and act like links: link or button, underlines and colour, hover, focus and visited states, link text that makes sense alone, new tabs, downloads, email and phone links, anchors under a sticky header, the skip link, and router links. Read before building or restyling links, in running text or in navigation."
---

# Links

The generated version: body links with the underline removed and only a
slightly different grey to tell them apart, "Learn more" under every card,
`href="#"` on half the navigation, every outside link opening a new tab,
and a `div` with an `onClick` doing a link's job. People rely on a link's
conventions: it looks like a link, says where it goes, goes there, and
works however they open it (a click, a middle click, a long press, a
keyboard). The principles are in the `ui` skill, the measures in
`ui-layout`, buttons in `ui-part-buttons`.

## 1. Link or button

- Links navigate, buttons act. A link goes to a URL (a page, a section, a
  file, an email address) and can be opened in a new tab, bookmarked and
  copied. A button does something here: submits, saves, opens a dialog or
  a menu, toggles, deletes.
- The look can cross over, the element cannot. "Book a table" that goes to
  `/book` is an `<a>` styled as a button; "Show 3 more" that expands in
  place is a `<button>` that may look like a text link. Avoid buttons
  styled as links for navigation, and links styled as buttons that perform
  actions.
- Never a JavaScript-only link: an `<a>` without `href` or a clickable
  `div` cannot be reached with the keyboard, and neither they nor
  `href="#"` and `javascript:void(0)` can be opened in a new tab,
  bookmarked or shared. In a single-page app use the router's link, which
  renders a real `<a href>`:
  `next/link`, React Router's `Link`, `RouterLink` or `NuxtLink`, a plain
  `<a>` in SvelteKit and Astro.

## 2. Kinds, and how each looks

- **In running text**: underlined, always, or distinct by more than
  colour. `text-decoration-thickness: 1px`, `text-underline-offset: 0.2em`,
  in the link colour at 4.5:1 against the background. A design that will
  not underline needs a link colour 3:1 apart from the surrounding text
  and an underline on hover and focus (WCAG technique G183); colour alone
  below that fails.
- **Standalone** (navigation, a footer, a list of documents, "All
  invoices" under a list): the position already says "link", so the
  underline can wait for hover; they keep the link colour or weight, a
  focus ring, and a 44px target on phones.
- **Styled as a button**: a link to the page's main task ("Book a table"),
  sized and coloured as in `ui-part-buttons`, still an `<a>`.
- **Card links**: the whole card opens through one real link on its title,
  stretched with a pseudo-element; nothing interactive nested inside
  (`ui-part-cards`).
- **With an icon**: an arrow after an outside link, a file icon before a
  download, from the product's icon set, at the text's size,
  `aria-hidden="true"`.

## 3. States

| State | What it looks like |
|---|---|
| Default | the link colour (`--link`), underlined in text |
| Hover | the underline thickens to 2px or the colour deepens a step, under `@media (hover: hover)` |
| Focus-visible | a 2px ring in `--focus` with a 2px offset on every link; never `outline: none` without a replacement |
| Active | a step darker while pressed |
| Visited | a distinct colour (`--link-visited`) on content sites: docs, articles, search results, archives; not in an app's navigation |
| Current | in navigation, `aria-current="page"` and weight or an underline (`ui-part-navigation`) |
| Unavailable | a link has no disabled state: remove it, or show plain text with the reason ("Available from 1 Nov") |

`:visited` accepts only colour properties (browsers ignore the rest there
for privacy), so the visited difference is a colour, subtle but real.

## 4. Words

- Link text says where it goes and makes sense alone: screen reader users
  often list a page's links. "Read the refund policy", not "Click here";
  "Pricing", not "Learn more".
- A "Read more" under every card: make the card's title the link instead,
  or add visually hidden text so each is unique:
  `Read more<span class="visually-hidden"> about the spring timetable</span>`.
- The accessible name contains the visible words (WCAG 2.5.3): an
  `aria-label` that says something else breaks voice control ("click
  Pricing").
- One destination, one wording, everywhere; two links with the same words
  go to the same place.
- A URL as the text only when the URL is the content (a domain people will
  type). Long URLs wrap with `overflow-wrap: anywhere`, or they push a
  phone's page sideways.
- `mailto:` and `tel:` links show the address or the number as their text,
  so it can be read and copied on a desktop where `tel:` does nothing; the
  href holds the full international number (`tel:+62…`).

## 5. New tabs, downloads, anchors

- A new tab only when leaving mid-task would lose work (a link inside a
  form, a checkout, a playing video), or for a reference read beside the
  app. Otherwise the same tab: people open new tabs themselves.
- When a link does open one: `target="_blank"` with `rel="noopener"`
  (current browsers imply it; keep it for older ones), and a hint that it
  opens a new tab: the icon plus visually hidden "(opens in a new tab)".
- `rel="noreferrer"` when the destination should not learn where the
  visitor came from; `rel="nofollow ugc"` on links in user content,
  `rel="sponsored"` on paid ones.
- Downloads say the type and size: "Annual report (PDF, 2.4 MB)". The
  `download` attribute (same-origin files only) saves instead of opening.
- In-page anchors land below the sticky header: `scroll-padding-top` on
  `html`, the header's height plus 8px (`ui-part-header`), or
  `scroll-margin-top` on the targets. Every anchor's id exists.
- The skip link comes first: "Skip to content", pointing at `<main
  id="main">`, hidden until it has focus.

## 6. Phones and touch

- Links inside a paragraph are exempt from the target size, since the line
  of text sets their height (the `preview` tool skips them).
- Standalone links (navigation, footer, lists) get at least 44px of height
  through `padding-block`, and 8px between neighbours.
- There is no hover on touch: the resting state has to say "link" on its
  own.

## 7. Themes and motion

- `--link`, `--link-visited` and `--focus` have a value per theme: links at
  4.5:1 and the ring at 3:1 in both (`ui-themes`).
- A colour change of 160ms (`--m-fast`) at most; no underline sweeping in
  on every link in running text (`motion-interface`, section 1).

## 8. A sketch

```css
.prose a {
  color: var(--link);
  text-decoration-line: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 0.2em;
}
.prose a:visited { color: var(--link-visited); }
@media (hover: hover) {
  .prose a:hover { text-decoration-thickness: 2px; }
}
a:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
  border-radius: 2px;
}
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}
.skip-link {
  position: absolute;
  inset-block-start: var(--space-3);
  inset-inline-start: var(--space-3);
  z-index: 100;
  padding: var(--space-3) var(--space-4);
  background: var(--surface);
  transform: translateY(-200%);
}
.skip-link:focus { transform: none; }
```

```html
<a class="skip-link" href="#main">Skip to content</a>

<a href="https://docs.example.org/setup" target="_blank" rel="noopener">
  Setup guide<span class="visually-hidden"> (opens in a new tab)</span>
  <svg class="icon" aria-hidden="true">…</svg>
</a>

<a href="/files/price-list.pdf" download>Price list (PDF, 240 KB)</a>
```

## Check it

- `preview`: "links to nowhere" lists `href="#"`, empty hrefs and anchors
  whose id does not exist; "controls without a name" lists icon-only
  links; "touch targets under 44px" lists standalone links on phones (it
  skips links inside running text); contrast covers link text.
- `ui_check`: `dead-link` (`href="#"`, `javascript:void(0)`),
  `generic-action` ("Learn more", "Click here"), `focus-removed`.
- `grep -n 'target="_blank"'`: each has a reason and says it opens a new
  tab. Search for `<div` with `onClick` and `<a` without `href`.
- Keyboard from the address bar: the skip link appears first and jumps to
  the content; every link shows its ring; an anchor lands with its heading
  clear of the sticky header.

## Avoid

Body links without an underline in a slightly different grey; "Click
here", "Read more" and "Learn more" as the whole link; buttons styled as
links for navigation, links styled as buttons that perform actions;
`href="#"` placeholders; every outside link in a new tab, or a new tab
without a word about it; an `aria-label` that differs from the visible
words; `outline: none`; downloads with no type or size; anchors that land
under the header; long URLs pushing the page sideways.
