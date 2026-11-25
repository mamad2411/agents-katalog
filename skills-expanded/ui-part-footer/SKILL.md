---
name: ui-part-footer
description: "The site footer: what it holds for a personal site, a local business, a product and an application, link groups only where they are real, legal pages, contact, social links, language and theme, the copyright line, measures, landmarks and phones. Read before building or reworking one."
---

# Footer

The generated version: four columns titled Product, Company, Resources
and Legal, half of them linking to pages that do not exist, a newsletter
box that sends nothing, icons for social accounts nobody made, "Built with
Next.js and Tailwind", and "All rights reserved" after a stale year. A
footer holds what people look for at the end of a page, and only what the
site actually has. One part of an interface: the principles (direction,
spacing, type, colour, icons, states, accessibility) are in the `ui`
skill, the measures in `ui-layout`.

## 1. What it is for

- What people look for at the end: how to reach the owner; the address
  and hours for a local business; the legal pages that exist; secondary
  links.
- Also, where they exist: a language switch, a theme control, the status
  page of a software product, the cookie settings.
- Not a second sitemap of every page, and not a place for slogans.

## 2. By kind of site

- **A personal site or a small product**: usually one or two lines. The
  contact again (the email itself, as a link), the other profiles that
  exist, and the name with the year. A closing line in the owner's voice
  can end the page better than any grid of links.
- **A local business**: the name, the address in an `<address>` element
  with a link to the map, the phone as a `tel:` link, the opening hours as
  a short list, the booking link; the same facts as the contact section,
  never different ones (`ui-page-local-business`).
- **A larger site**: as many columns as there are real groups of links,
  often one or two; the legal line under them; for software, a link to
  the status page.
- **An application**: usually no footer inside the app shell. Legal links,
  the version and help live in the account menu or the settings.

## 3. Content rules

- Links only to pages that exist. A group of one link is not a group:
  merge it with another.
- Legal: a privacy notice wherever personal data is collected (the GDPR in
  the EU, Indonesia's personal data protection law, and others), terms
  when there are terms, an imprint (Impressum) on commercial sites in
  Germany and Austria, and "Cookie settings" to reopen the consent choice
  when the site asks for consent. Pages the owner has not given you are
  placeholders listed in your report, never generated legal text presented
  as final.
- The copyright line: the owner's real name in it, or a placeholder
  ("[Owner name]"), with the year from the current date, computed at build
  or render so it never goes stale. No "All rights reserved": it has had
  no legal effect for decades.
- Social links for accounts that exist and are kept up, named ("GitHub",
  "LinkedIn"), or as icons whose `aria-label` names the network; brand
  icons from the product's set or Simple Icons. They open in the same tab
  (`ui-part-links`).
- A newsletter sign-up only when there is a newsletter, with a real
  provider behind the form (`ui-part-cta` has the form).
- A language switch lists languages in their own names ("English",
  "Bahasa Indonesia"), with `lang` on each name and `hreflang` on each
  link; no flags, which stand for countries, not languages (`i18n`).

## 4. Anatomy and measures

- Padding 48 to 64px above and below on a site with columns, 32 to 48px
  for a one-line footer; a hairline or one surface step above it.
- The page's container and grid: the footer's left edge is the content's.
- Text 14px, muted and still 4.5:1; group titles 14px, weight 600, in
  sentence case, not caps with wide tracking; links in a group 8 to 12px
  apart on desktop.
- Groups side by side from 1024px, two columns at tablet width, one on a
  phone; the legal line last, on one or two lines.
- On a short page the footer sits at the bottom of the window: the element
  that holds the header, `main` and the footer gets `min-height: 100dvh;
  display: grid; grid-template-rows: auto 1fr auto`.

## 5. Markup

- One `<footer>` outside `main`, `article` and `section`, so it is the
  page's `contentinfo` landmark.
- Link groups in a `nav` with `aria-label="Footer"`, each group a list
  under its own heading (an `h2` styled small), so screen reader users can
  jump to "Legal" or "Contact"; not `div`s styled as titles.

## 6. Phones

- One column, in the order people look for things: contact, then the
  groups, then legal.
- Links in lists 44px tall to the touch (padding on the link, not a gap),
  with room between them; a long set of groups may fold into one
  `details` per group, but never the contact or the legal line. Links
  inside a sentence need no padding.
- On a long page, the back-to-top control (`ui-part-back-to-top`) and the
  footer do not overlap: leave room for it after the last line, or place
  it clear of the links.

## 7. Themes and motion

- Muted text at 4.5:1 in both themes; a logo in the footer switches with
  the theme (`ui-themes`).
- No motion: no animated wave, no marquee of logos (`motion-interface`).

## 8. A sketch

A personal site's footer, which is most of what one needs:

```html
<footer class="site-footer">
  <div class="container site-footer__inner">
    <p>Write to <a href="mailto:[email]">[email]</a>, or find me on
      <a href="[GitHub profile URL]">GitHub</a> and <a href="[LinkedIn profile URL]">LinkedIn</a>.</p>
    <p class="site-footer__legal">© 2026 [Owner name] · <a href="/privacy">Privacy</a></p>
  </div>
</footer>
```

```css
.site-footer { border-block-start: 1px solid var(--border); padding-block: 32px 48px; }
.site-footer__inner { display: grid; gap: 12px; font-size: 14px; color: var(--text-muted); }
.site-footer a { color: var(--text); text-underline-offset: 0.2em; }
.site-footer__legal { margin: 0; }
```

The year comes from the build or the render (`new Date().getFullYear()`
in the template), not typed by hand.

## Check it

- Follow every link in the footer: each opens a real page, profile or
  address. `preview` lists "links to nowhere"; `ui_check` flags `href="#"`.
- The year is this year, and changes without an edit.
- `preview` at 360px: footer links in lists appear in "touch targets under
  44px", muted text below 4.5:1, or the back-to-top control over the last
  line: each is a finding.
- A screen reader lists one `contentinfo` landmark and the footer's
  headings.
- The newsletter form, if there is one, sends a real email.

## Avoid

"Built with Next.js and Tailwind", a "made with" line with a heart, "All
rights reserved" boilerplate, a "last synced" timestamp nobody asked for,
the four-column Product / Company / Resources / Legal template, social
icons for accounts that do not exist, a newsletter form that sends
nothing; links to pages that do not exist; flags for languages; a stale
year; generated legal text presented as real; tiny grey text below 4.5:1;
a site footer inside an application shell.
