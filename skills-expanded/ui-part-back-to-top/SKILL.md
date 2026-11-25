---
name: ui-part-back-to-top
description: "The back-to-top control every long page has: when it appears (after the first screen, on pages over about three screens on a phone), a real link to #top that works without a script, its name and icon, its size and place above bottom bars, chat buttons and the safe area, showing and hiding, smooth scrolling only without reduced motion, focus and the keyboard, app shells that scroll a container, alternatives such as a footer link or a sticky table of contents, and the preview check. Read before building a page longer than about three screens (count them on a phone)."
---

# Back to top

The generated version: a glowing gradient circle with a bouncing arrow on
every page whatever its length, a `div` that calls `scrollTo` and leaves
the keyboard's focus at the bottom, parked over the footer's last link or
the chat button. This is a small real link that takes a reader from far
down a long page back to its start, works before any script loads, and
keeps clear of everything else fixed to the screen. One part of an
interface: the principles (direction, spacing, type, colour, icons,
states, accessibility) are in the `ui` skill, the measures in `ui-layout`.

## 1. When a page has one

- Use it for: getting back to the navigation from far down a long page.
  Every page longer than about three screens has one. Count the screens on
  a phone, where a page runs three to four times as tall as on a laptop, so
  nearly every landing page, article, portfolio and long list has one. A
  page of one or two screens does not.
- The sticky header already keeps the links in reach (`ui-part-header`);
  this takes the reader back to the start: the claim, the article's title,
  the filters above a long list.
- It shows after the first screen, never at the top, where there is
  nowhere to go back to (section 4).

## 2. The link and its name

- A link, not a script: `<a href="#top">`, with `id="top"` on `<body>` or
  on the first element of the page, never on the sticky header, which
  never leaves the screen and so is never scrolled back to. The link works
  without JavaScript, and it moves the keyboard's starting point to the
  top, so the next Tab reaches the skip link and the navigation.
- A plain `<a>`, not the router's link component, which may treat the hash
  as a route. Following it adds `#top` to the address, and the browser's
  Back button returns the reader to where they were.
- A name: an up arrow from the product's icon set with
  `aria-label="Back to top"`, or the words, in the page's language
  ("Kembali ke atas").
- The arrow: arrow-up or chevron-up from the one set, 20 to 24px, in
  `currentColor`, `aria-hidden="true"`; the word beside it ("Top") when the
  page's other buttons carry words. Never an emoji, never capitals.

## 3. Size and place

- Fixed at the bottom right, 16 to 24px from the edges plus the safe area,
  44 to 48px square, on the surface colour with a 1px line and the same
  radius as the other buttons; above the content, below menus and dialogs
  (`--z-to-top: 20` in the stacking order of `ui-part-header` section 8).
- Clear of everything else fixed at the bottom: a bottom tab bar, a chat
  button, a cookie notice, a sticky "Book" button on a phone. Stack above
  them or take the other side; never cover a control or the footer's last
  line.
- In numbers: 12 to 16px above a bottom tab bar (56 to 64px plus the safe
  area, `ui-part-navigation` section 5) or a phone's sticky action bar;
  above a chat button by its height plus 12px, or on the bottom left when
  the chat owns the right; above a cookie notice until it is answered.
- Keep that offset in one custom property (`--fixed-bottom`), set where the
  bars are (`body:has(.tab-bar)`, or by the script that shows them) and
  added to the sketch's `bottom`, so the control and the toasts share it.
- In a right-to-left page it takes the bottom left: `inset-inline-end`
  rather than `right`.
- In the markup after the main content (the end of `body`, or just before
  the footer), so the keyboard reaches it last, not first. Hidden in print:
  `@media print { .to-top { display: none; } }`.

## 4. Showing and hiding

- Hidden at the top, shown after the first screen: a passive scroll
  listener sets `hidden` while `scrollY < innerHeight`, and runs once on
  load. Without JavaScript it simply stays visible.
- Or with no scroll listener: an IntersectionObserver on a marker that
  covers the first screen, hiding the control while the marker is in view
  (the second script in section 8).
- It appears at once, or fades in over 150 to 200ms; no bounce, no pulse,
  no spin; under reduced motion it simply appears (`motion-interface`).
- Past the first screen it stays: it does not hide on scroll down and come
  back on scroll up, which moves it under the reader's thumb.

## 5. Scrolling, focus and the keyboard

- Smooth scrolling only for those who have not asked for less motion: the
  CSS in the sketch; in script, `behavior: prefersReducedMotion() ? "auto"
  : "smooth"` (`motion-reveal` section 11).
- Following the link moves the keyboard's starting point and a screen
  reader's reading position to the top: the next Tab reaches the skip link,
  then the navigation.
- Where a button must scroll by script, it then moves focus to the page's
  `h1` (given `tabindex="-1"`) with `focus({ preventScroll: true })`;
  otherwise the keyboard stays at the bottom of the page.
- Reached by Tab while shown, followed with Enter, with the same focus ring
  as every other control (2px, offset 2px).

## 6. In an app shell

- In an app shell whose content area scrolls on its own, the control sits
  in that area and returns it to the top (`main.scrollTo({ top: 0 })`),
  then moves focus to the area's heading.
- It listens to the area, not the window (`main.scrollTop <
  main.clientHeight`), and sits at the area's bottom corner, clear of a
  side panel.
- Or with no script: a link to the area's heading (an `id` and
  `tabindex="-1"` on its `h1`); following it scrolls the area and focuses
  the heading.

## 7. Alternatives, and together

- A "Back to top" link at the end of the footer is a good addition, never
  the only one: it is out of reach from halfway down, and `preview` says so.
- On a wide screen, the sticky table of contents of a long article or docs
  page, with "Back to top" at its end, can stand in for the floating
  control (`ui-page-blog`, `ui-page-docs`); on a phone, where the table
  folds away, the floating control stays.
- A feed that loads more as it scrolls needs it most: its footer may never
  come. A paged list already returns the reader to its top on each page
  (`ui-part-pagination`).

## 8. A sketch in plain HTML, CSS and JavaScript

```html
<body id="top">
  …
  <a class="to-top" href="#top" aria-label="Back to top">
    <svg aria-hidden="true" …>…</svg>
  </a>
</body>
```

```css
@media (prefers-reduced-motion: no-preference) {
  html { scroll-behavior: smooth; }
}
.to-top {
  position: fixed;
  right: calc(var(--space-4) + env(safe-area-inset-right));
  bottom: calc(var(--space-4) + env(safe-area-inset-bottom));
  z-index: 20;
  display: grid;
  place-items: center;
  inline-size: 48px;
  block-size: 48px;
  color: var(--ink);
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius);
}
/* `display: grid` would override the attribute's own display: none. */
.to-top[hidden] { display: none; }
```

```js
const toTop = document.querySelector(".to-top");
const place = () => { toTop.hidden = scrollY < innerHeight; };
addEventListener("scroll", place, { passive: true });
place();
```

Or, in place of the listener, a marker over the first screen:

```js
const marker = document.createElement("div");
marker.style.cssText = "position:absolute;top:0;width:1px;height:100svh;pointer-events:none";
document.body.prepend(marker);
new IntersectionObserver(([entry]) => { toTop.hidden = entry.isIntersecting; })
  .observe(marker);
```

In React, Vue or Svelte: the same link as a small component, the listener
added on mount and removed on unmount.

## Check it

- `preview` at 360, 768 and 1440px: on a page more than three screens long
  it scrolls halfway down, waits a moment, and looks within the screen for
  a link to `#top`, a link to an element at the top of the page (not inside
  the header), or a control named like "Back to top", "Top" or "Kembali ke
  atas"; finding none it reports "N screens long, and halfway down there is
  no way back to the top: add a back-to-top control (ui-part-back-to-top)".
  A control still under 10% opacity counts as hidden; `href="#top"` is
  found in any language.
- In the same report: `href="#"` under "links to nowhere", an arrow with no
  label under "controls without a name", a control under 44px at 360px.
- With `motion: true`: the reduced-motion pass says "smooth scrolling is
  still on" if it is; the scroll listener shows in its list, passive.
- By hand at 360px, with the cookie notice, the chat button and any bottom
  bar showing: nothing overlaps the control or the footer's last line.
  Follow it, then press Tab: the skip link appears.

## Avoid

A glowing gradient circle with a bouncing arrow; `href="#"`, which reads as
a link to nowhere; a button that calls `scrollTo` and leaves the keyboard's
focus at the bottom of the page; one on a page of two screens; one that
covers the footer's links or a cookie banner's buttons; "SCROLL TO TOP" in
capitals; one showing at the very top; `id="top"` on the sticky header; a
footer link as the only way back; smooth scrolling for someone who asked
for less motion.
