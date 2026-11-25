---
name: ui-part-header
description: "The header (top bar), sticky by default: what goes left, centre and right on a personal site, a product site, docs, a shop, a local business and an app, heights, the name, links and one action, the sticky rules (a solid background, a hairline once scrolled, scroll-padding-top, nothing that stops it sticking), transparent over a hero, hiding on scroll only when asked, announcement bars, the phone header with its Menu button, search and account placement, the skip link, stacking with drawers and dialogs, and the preview check. Read before building or reworking one."
---

# Header (top bar)

The generated header: a glass bar with a glow, seven links to pages that
do not exist, "Log in" beside a gradient "Get started" pill, a "Beta"
badge beside a name with a coloured full stop, and a bar that scrolls away
on a long page, or sticks with nothing behind it so text runs over text.
This is the bar that says whose site it is and keeps the few places people
need one reach away, on every screen. One part of an interface: the
principles (direction, spacing, type, colour, icons, states,
accessibility) are in the `ui` skill, the measures in `ui-layout`, the
links inside it in `ui-part-navigation`.

## 1. What it holds, by kind of site

Use it for saying whose site or product this is, and reaching the three or
four places people go most. Not for everything the site has: the rest goes
in the footer (`ui-part-footer`). It is read on every screen, so it is the
quietest thing on the page that still does that job.

| Kind | Left | Centre | Right | Height |
|---|---|---|---|---|
| Personal site | the name | nothing | three links and the contact link, on one baseline | 56 to 64px |
| Product or marketing site | the name or logo | three to five links | "Sign in" as a text link, the one action | 64 to 72px |
| Docs | the name to the docs home, the sections | search, drawn as a field with its shortcut | version (only with versions), theme, repository | 56 to 64px |
| Shop | the logo | the search field, 320 to 560px | Account, Cart with its count | 64 to 72px |
| Local business | the name | nothing, or two links | Call, and the booking action | 56 to 64px |
| App without a sidebar | product or workspace switcher | search, or the command palette's trigger | help, notifications, the account menu | 56 to 64px |
| Checkout, sign-up, onboarding | the logo | nothing | one way back ("Back to cart") or out ("Save and exit") | 56px |

An app with a sidebar has no site header: under 1024px a 56px top bar holds
a labelled Menu button, the screen's title and its primary action
(`ui-layout` section 5, `ui-part-sidebar`); the screen's own title and
actions are its page header (`ui-part-page-header`).

## 2. The name, the links, the action

- The name as it is written, linking home: the text face at 16 to 18px,
  weight 600, or the real logo when there is one (an SVG 24 to 32px tall,
  its `alt` the name, not "logo"). No full stop, underscore, bracket or
  blinking cursor after it, and no generated monogram.
- Three or four links at most, named with the nouns the page uses
  ("Projects", "Writing", "Contact"), at body size in the text colour, 24
  to 32px apart. The current one is marked by weight or an underline with
  `aria-current`, not by a pill. Dropdowns: `ui-part-navigation` section 3.
- One action only when the product has one (Book, Download, Sign in), as a
  real button at the default size (`ui-part-buttons`). A link to a profile
  (GitHub, LinkedIn) is a text link, or an icon with a label, not an
  outlined button beside the navigation.
- A theme toggle only when both themes are built and checked: one icon
  button (sun or moon), no visible text, whose `aria-label` says what it
  switches to (`ui-themes`).
- The name's left edge and the last link's right edge line up with the
  content's container, so the header and the page share one grid: the
  bar's inner row is the page's container, its background full width.
- For a personal site the whole header can be one line of text on one
  baseline: the name, the links, the contact link, with no boxes at all.
- Links follow the name, or sit at the right before the action; centred
  only on a product site with three to five (`grid-template-columns: 1fr
  auto 1fr` keeps them on the page's centre line).

## 3. Sticky, by default

- 56 to 72px tall on wide screens, 56px on a phone. A solid background,
  from the surface token: content scrolls under it, and a transparent bar
  lays text over text. A border or a shadow only once the page has scrolled
  under it: a 1px hairline in the line colour, fading in over 160ms.
- Sticky by default, on a phone too: `position: sticky; top: 0`, with a
  `z-index` above the content and below menus and dialogs (section 8), so
  the navigation and the primary action are always one reach away.
  `sticky`, not `fixed`: it keeps its place in the flow, so nothing needs a
  padding-top to clear it.
- `scroll-padding-top` on `html`, its height plus 8px, so a link to a
  section does not land under the bar and a control reached by Tab is not
  hidden behind it (WCAG 2.4.11). Docs with large headings use 16px.
- Nothing around it has `overflow` other than `visible` or `clip`: a
  wrapper with `overflow: hidden`, or `overflow-x: hidden` on both `html`
  and `body`, silently stops it sticking. Fix a horizontal overflow at its
  cause instead.
- Its parent runs the page's full height: a sticky element sticks only
  inside its parent, so a header wrapped in a `div` of its own height
  scrolls away. Put it directly in `body`, or in the layout's root.
- Only the bar with the navigation sticks: an announcement strip above it
  scrolls away, and a header taller than 72px shrinks to its bar once the
  page scrolls (a negative `top` the height of the part above the bar).
- The phone menu opens under the bar and scrolls inside itself:
  `max-height: calc(100dvh - <bar height>)`.
- `transform`, `filter` or `backdrop-filter` on the header traps anything
  `position: fixed` inside it: a menu panel in a blurred bar is cut to the
  bar. Open the panel as a `dialog` with `showModal()`, or outside it.
- Not sticky: a page that fits one screen (sign-in, a short form), and an
  app shell whose content area scrolls on its own, where the bar stays put
  by the layout.

## 4. Over a hero, and hiding on scroll

- Transparent over the hero only when the hero is a full-bleed photograph
  that is itself the content (a place, a room), and only at the very top:
  the bar turns solid, with its hairline, the moment the page scrolls (the
  same observer), before anything passes under it. The hero pulls up under
  the bar (`margin-block-start: calc(-1 * var(--header-h))`). Its words
  keep 4.5:1 against the lightest part of the photograph, on a scrim at the
  image's top; `preview` measures text against the nearest background
  colour, not a photograph, so check that yourself.
- Hiding on scroll down only when the brief asks for it, for a reading page
  on a phone; never on a desktop app bar, nor when the bar holds the page's
  action. Hide with `transform: translateY(-100%)` after 8 to 10px down;
  show on any upward scroll, at the top, while focus is inside
  (`:focus-within`) and while its menu is open; no transition under reduced
  motion. `preview` reports it as scrolling away: say the brief asked for it.

## 5. Announcement bars

- One line of real news and one link ("Version 3 is out: what changed")
  above the header, scrolling away with the page: 36 to 40px tall, 44px on
  phones so its close button is a full target, wrapping rather than cut.
- One at a time: never an announcement, a cookie notice and a promotion
  stacked over the header. A state of the page or the account (offline, a
  failed payment) is a banner below the header (`ui-part-notifications`).
- Dismissible ("Dismiss announcement"), the dismissal kept per announcement
  id (`localStorage`, or the account) and applied before the first paint
  (an inline script in `head`, or a cookie the server reads), so it does
  not flash in and push the page down on every visit. No countdown.

## 6. On a phone

- 56px, sticky, the same solid surface. At the left the name (the logomark
  alone only when the product has one, its `alt` the name); at the right
  the one action, shortened ("Book", "Start trial"), then the Menu button.
- On a phone the links collapse into a button labelled "Menu", not an
  unlabelled icon: the icon and the word, `aria-expanded`, a 44px target;
  the panel keeps focus inside, closes on Escape and after a link is
  chosen, and locks the page behind it (`ui-part-navigation` section 4,
  `ui-part-drawers`). The links fold where they no longer fit on one line
  (look at 768px); above that, no hamburger.
- Search becomes a named icon button opening a full-screen search; the
  account menu moves into the panel. Side padding 16 to 20px, plus
  `env(safe-area-inset-left)` and `-right` in landscape.

## 7. Search and account

- Search in the bar only when it is a main way in (docs, a shop, a large
  blog) and searches something real: a field-shaped button showing `⌘K` or
  `Ctrl K` on docs, a real field on a shop (`ui-part-search`). A site of
  ten pages needs none.
- Signed out: "Sign in" as a text link; one filled button only when signing
  up is the page's goal. Signed in: the avatar or name as a menu button at
  the far end, named "Account menu", with Sign out last
  (`ui-part-navigation` section 7, `ui-part-menus`); on the marketing site,
  "Open app" where "Sign in" was. Counts go in names: "Notifications, 3
  unread", "Cart, 2 items".

## 8. Keyboard, screen readers, stacking

- A "Skip to content" link as the first thing a keyboard reaches, shown on
  focus, pointing at `<main id="main" tabindex="-1">` (`ui-part-links`).
- `<header>` directly in `body`, so it is the banner landmark; `<nav
  aria-label="Main">` around the links; the name is a link, not the `h1`.
- The current page marked with `aria-current="page"` and more than colour
  (weight or an underline). Tab order follows the visual order: skip link,
  name, links, search, action, account menu.
- One stacking order as tokens, so a dialog never opens under the bar:
  `--z-to-top: 20` (back to top), `--z-header: 30`, `--z-drawer: 40`
  (drawers, the phone menu), `--z-dialog: 50`, `--z-toast: 60`. A `dialog`
  opened with `showModal()` and a `popover` sit in the top layer above all
  of them with no z-index; a dropdown inside the header rises with it.

## 9. Themes and motion

The bar is the surface token in both themes, its hairline the line token;
the logo is inline SVG in `currentColor`, or one file per theme
(`ui-themes`). The hairline fades over 160ms; the height never animates; no
blur; the phone panel moves as in `ui-part-navigation` section 8.

## 10. A sketch

```css
/* Markup: skip link, header.site-header > .bar (name, nav, action), main#main */
:root { --header-h: 64px; }
@media (max-width: 767px) { :root { --header-h: 56px; } }
html { scroll-padding-top: calc(var(--header-h) + 8px); }
.site-header {
  position: sticky; top: 0; z-index: var(--z-header);
  background: var(--surface);
  border-block-end: 1px solid transparent;
  transition: border-color 160ms ease-out;
}
.site-header[data-scrolled] { border-block-end-color: var(--line); }
.bar {
  display: flex; align-items: center; gap: 24px; min-block-size: var(--header-h);
  max-width: 1200px; margin-inline: auto; padding-inline: clamp(16px, 5vw, 48px);
}
.bar nav { margin-inline-start: auto; }
```

```js
// The hairline once the page has scrolled: a 1px marker at the top of the page.
const header = document.querySelector(".site-header");
const marker = document.createElement("div");
marker.style.cssText = "position:absolute;top:0;width:1px;height:1px;pointer-events:none";
document.body.prepend(marker);
new IntersectionObserver(([entry]) => {
  header.toggleAttribute("data-scrolled", !entry.isIntersecting);
}).observe(marker);
```

## Check it

- `preview` at 360, 768 and 1440px: on a page longer than a screen and a
  half it scrolls halfway down, finds the first `header`, `[role=banner]`
  or `nav` at the top, and when that has left the screen reports "the top
  bar scrolls away on a page N screens long: make it sticky
  (ui-part-header)". It scrolls rather than reading the CSS, so a wrapper's
  `overflow` that stops the sticking is caught.
- In the same report: "controls without a name" (an icon-only Menu),
  "touch targets under 44px", "links to nowhere"; in the 768px screenshot,
  links wrapping onto a second line.
- Follow every in-page link: its heading lands below the bar. Tab from the
  address bar: the skip link first, then the name and links in order.
- Open the phone menu, a dialog and a drawer: each covers the bar. Dismiss
  the announcement and reload: it stays gone, with no flash.
- When it will not stick, search the global styles and the layout's
  wrappers for `overflow` (`overflow-hidden` in Tailwind).

## Avoid

A glass header with a glow, seven links to pages that do not exist, "Log
in" beside a gradient "Get started" pill, a "Beta" badge next to the logo;
a name with a coloured full stop or a cursor; a GitHub button with its icon
in a bordered box; a search shortcut that searches nothing; a bar that
scrolls away on a long page, one that sticks with a transparent background,
section links that land under it; a hamburger on a wide screen where the
links fit, or an icon with no word on a phone; announcement, cookie and
promotion bars stacked over it; a bar that hides on scroll without being
asked, or on a desktop app; a menu panel cut off inside a blurred bar;
`z-index: 9999`.
