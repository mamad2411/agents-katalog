---
name: ui-part-navigation
description: "Site and app navigation: choosing and naming the places, the top links and the current page, dropdowns as disclosures, mega menus, the phone menu, a bottom tab bar, in-page tables of contents, search and account placement, the skip link, and no dead links. Read before building or reworking the navigation of a site or an app."
---

# Navigation

The generated version: Solutions, Platform, Resources, Company, Pricing,
Blog and Contact, half of them pointing at `#`; dropdowns that open on
hover and vanish on the way to them; a hamburger on a 1440px screen; a
phone menu that lets the page scroll behind it and stays open after a tap.
Navigation is the map of what exists: few places, named in the visitor's
words, the current one marked, reached the same way on every screen. The
principles are in the `ui` skill, the measures in `ui-layout`; the bar it
sits in is `ui-part-header`, an app's sidebar `ui-part-sidebar`.

## 1. What goes in it

- Use it for three to seven destinations, named with the nouns users
  already use ("Invoices", "Clients", not "Solutions"). The words come from
  what people search for and ask about (support mail, search logs, the
  business's own customers).
- Order by how often each place is used, not by the org chart.
- Every item leads somewhere that exists: no "Features" pointing to a
  missing section, no "Blog" with no posts, no `href="#"`. A place not
  built yet is left out.

| Navigation | Where | Read |
|---|---|---|
| A site's main places | the header | this skill, `ui-part-header` |
| An app's places | a sidebar; a drawer or a bottom bar on phones | `ui-part-sidebar`, section 5 below |
| Views of one object | tabs as links | `ui-part-tabs` |
| Where a page sits in a hierarchy | breadcrumbs | `ui-part-breadcrumbs` |
| Sections of a long page | a table of contents | section 6 below |
| Everything else the site links to | the footer | `ui-part-footer` |

## 2. The top links (a website)

- On a website it lives in the header, which sticks (`ui-part-header`), so
  it is in reach anywhere on the page.
- `<nav aria-label="Main">` around a `ul` of links. Other `nav` elements get
  their own labels ("Footer", "On this page"); the word "navigation" stays
  out of the label, the screen reader already says it.
- Links at body size (15 to 16px) in the text colour, 24 to 32px apart, or
  8 to 12px of padding each; at least 44px tall on touch.
- The current page: `aria-current="page"` with weight or an underline, not
  colour alone and not a pill. A section parent (the page sits under
  "Guides") takes `aria-current="true"` and the same mark.
- One action at the end when the product has one ("Book", "Sign in"); search
  in the bar when it is a main way in, as on docs and shops
  (`ui-part-search`); the account menu at the far end once signed in.
- A skip link ("Skip to content") before it all, the first thing the
  keyboard reaches (`ui-part-links`).

## 3. Dropdowns and mega menus

- Dropdowns only for real groups. They open on click, tap and Enter, close
  on Escape and on a click outside, and never exist only on hover. Hover
  may open them too, after 100 to 150ms, with about 300ms of grace on the
  way out.
- A dropdown is a disclosure (the APG disclosure navigation pattern): a
  `button` with `aria-expanded` and `aria-controls`, showing a list of
  links. Not `role="menu"`, which is for application actions and changes
  what the keys do. Tab moves through the links; Escape closes and returns
  focus to the button; focus leaving the group closes it.
- When the group's parent is also a page ("Services"), put it first inside
  ("All services"), or pair a link with a small toggle button that has its
  own name ("Show Services pages").
- Mega menus only for large sites (hundreds of pages in several groups: a
  university, a retailer): columns under headings, still a disclosure,
  still keyboard-driven, scrolling inside when taller than the window. Not
  for a site with ten pages.

## 4. The phone menu

- Where the links no longer fit on one line (check at 768px; set by the
  content, not a device width), they fold behind a button labelled "Menu"
  (the icon and the word) with `aria-expanded` and `aria-controls`. Above
  that width, no hamburger: hiding links that fit hides the map for nothing.
- The panel: full width under the bar (`max-height: calc(100dvh - <bar
  height>)`, scrolling inside), or a full-screen sheet or drawer; 44 to
  48px rows; groups as expandable sections; the primary action kept in the
  bar or first in the panel.
- It behaves as a modal dialog: focus moves in and stays inside while it is
  open (`dialog` with `showModal()`, or `inert` on the rest of the page); a
  labelled close button ("Close menu"); Escape closes it; focus returns to
  the Menu button; the page behind it is locked from scrolling
  (`html:has(dialog[open]) { overflow: hidden; }`).
- It closes after a link is chosen, including an in-page anchor and a route
  change in a single-page app, where no page load closes it for you.

## 5. A bottom tab bar (apps)

- An app with three to five main places, used daily on a phone, can use a
  bottom tab bar: an icon and a label on every tab (12px or more), the
  current one marked (`aria-current="page"`, the filled icon and the accent,
  not colour alone), and the content padded so the bar never covers it.
- 56 to 64px tall plus `env(safe-area-inset-bottom)`, fixed to the bottom, a
  solid surface with a hairline on top; the content's `padding-bottom`
  matches it; toasts, back-to-top and sticky buttons sit above it.
- Not on marketing sites. On wider screens the same places move to the
  sidebar or the header. A "More" tab only when there really are more than
  five places.

## 6. In-page navigation

- A table of contents for a long document or article (`ui-page-docs`):
  sticky in a side column on wide screens (`top` equal to the header's
  height plus 24px), an "On this page" disclosure above the content on
  phones.
- The section on screen marked as the reader scrolls
  (`aria-current="location"`, the observer band in `motion-reveal`, section
  10); anchors land below the sticky header (`scroll-padding-top`), and
  every anchor's id exists.

## 7. Account and sign-in

- Signed out: "Sign in" as a text link, and one filled button only when
  signing up is the page's goal.
- Signed in: the avatar or the name as a menu button at the end of the
  header (at the foot of an app's sidebar), named for what it opens
  ("Account menu"), holding the name and email, Settings, Billing where it
  exists, and Sign out last (`ui-part-menus`).

## 8. Themes and motion

- The bar and the phone panel are solid surfaces in both themes, the
  current mark at 3:1 (`ui-themes`).
- A dropdown fades and scales from its button in 160 to 240ms; the phone
  drawer slides in over 320ms and out in 200ms; the section marker slides.
  Under reduced motion they fade or simply appear (`motion-interface`,
  sections 2 and 5).

## 9. A sketch (a disclosure dropdown in plain HTML and JavaScript)

```html
<nav aria-label="Main">
  <ul class="nav">
    <li><a href="/work" aria-current="page">Work</a></li>
    <li class="nav-group">
      <button type="button" aria-expanded="false" aria-controls="nav-services">Services</button>
      <ul id="nav-services" hidden>
        <li><a href="/services">All services</a></li>
        <li><a href="/services/audits">Audits</a></li>
      </ul>
    </li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>
```

```js
for (const button of document.querySelectorAll(".nav-group > button")) {
  const group = button.parentElement;
  const panel = document.getElementById(button.getAttribute("aria-controls"));
  const set = (open) => {
    button.setAttribute("aria-expanded", String(open));
    panel.hidden = !open;
  };
  button.addEventListener("click", () => set(panel.hidden));
  group.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !panel.hidden) { set(false); button.focus(); }
  });
  group.addEventListener("focusout", (event) => {
    if (event.relatedTarget && !group.contains(event.relatedTarget)) set(false);
  });
  document.addEventListener("click", (event) => {
    if (!group.contains(event.target)) set(false);
  });
}
```

## Check it

- `preview` at 360, 768 and 1440px: "links to nowhere" (`#`, empty hrefs,
  anchors with no target), "controls without a name" (an icon-only Menu
  button), "touch targets under 44px" in the phone menu and the tab bar, a
  nav that wraps or overflows at 768px, and a top bar that scrolls away.
- Keyboard: the skip link first; links and buttons in visual order; a
  dropdown opens with Enter and closes with Escape back on its button; the
  phone menu keeps focus inside, closes on Escape and after a link is
  chosen, and hands focus back to "Menu".
- Follow every link in the navigation; `grep -n 'href="#'` for leftovers.
- On a phone: the page behind the open menu does not scroll; the tab bar
  never covers the last line of content.

## Avoid

Mega-menus for a site with ten pages; icons without labels; a hamburger on
wide screens where the links fit; "Solutions", "Resources" and "Platform"
on a small site; dropdowns on hover only; `role="menu"` on site links;
items that go to `#` or to sections that do not exist; the current page
marked by colour alone or by a pill; a phone menu that lets focus escape,
lets the page scroll or stays open after a tap; a bottom bar on a
marketing site, or one that covers the content.
