---
name: ui-reference-saas
description: "A worked reference, measured from a hand-designed product site: a professional tool with several features, proof, a team, pricing and a sign-up (a SaaS for lawyers). Its skeleton, wireframes, measures and component anatomy, and what to take from it. Read before building a product or SaaS marketing site with pricing."
---

# Reference: a product site with pricing

Measured from a hand-designed site (jagahukum.com, a legal research tool for
Indonesian lawyers). Take its structure and its decisions; its words, name,
imagery and colours belong to it. Its concept is its own: find yours from
your product (the `ui` skill, section 1).

**Its concept**: a serious professional tool that belongs to its country.
The hero is a painting of a landmark the audience knows; the pages
alternate a warm paper background with deep navy bands, like a legal
document and its binding; an italic serif marks the words that matter.

## Skeleton

1. A thin announcement bar: one line of real news and a link, dismissable.
2. Navigation over the hero: brand, seven links (two with menus), sign-in
   and the one filled "Try free".
3. Hero, one screen: a full-bleed image of a place, a three-line claim, one
   sentence, two buttons.
4. The problem: one large, sourced number beside a statement.
5. "See it work": the product itself, large, in a framed window.
6. Four features as a 2 by 2, each shown by a small real piece of the
   interface, not an icon.
7. Membership (dark band): what one account gives, as numbered rows, beside
   an object that makes the product tangible (an ID card on a lanyard).
8. Numbers strip: four figures, dated ("as of May 2026").
9. Team: who it was built with, as a list with large initials.
10. One testimonial at a time, large, with its source.
11. Pricing: a monthly and yearly toggle, the tiers in a row.
12. How it works: four steps.
13. A closing band with the hero image again, then a full footer.

Light and dark bands alternate for a reason: the product is shown on light,
membership, testimonials and pricing sit on the navy.

## Wireframes (wide screen)

```
│ one line of news · link                                          ✕ │ thin bar
│ ◉ Brand   Product▾ Solutions▾ Research Security Company Pricing    │
│                                          ◐  (Log in)  [Try free]   │ over the hero
│░░░░░░░░░░░░░░░░░ full-bleed painting of a known place ░░░░░░░░░░░░│
│               Claim in large type,                                 │
│               over two lines, and one                              │
│               Last word in italic serif.                           │
│          One sentence of what it does, ending in italics.          │
│               [ Start free ]  ( Watch the demo → )                 │
├────────────────────────────────────────────────────────────────────┤
│ ▏[figure]K+                    THE PROBLEM                         │
│ ▏LABEL UNDER THE NUMBER        A statement in large type whose     │
│                                second half turns italic.           │
│                                ──                                  │
├────────────────────────────────────────────────────────────────────┤
│  ┌─ real UI snippet ────────┐   ┌─ real UI snippet ────────┐       │
│  │ a chat with its steps    │   │ a file table             │       │
│  └──────────────────────────┘   └──────────────────────────┘       │
│  Feature title (serif)          Feature title (serif)              │
│  Two lines on what it does.     Two lines on what it does.         │
├────────────────────────────────────────────────────────────────────┤
│ Italic serif heading.                                AS OF DATE    │
│ ····································································│
│  [figure] K+   │ [figure] M+  │ <[figure] ms  │ [figure] %         │
│  LABEL         │  LABEL       │  LABEL        │  LABEL             │
└────────────────────────────────────────────────────────────────────┘
```

On a phone: the navigation folds behind a menu; the hero keeps its image,
its claim at 40 to 48px; the 2 by 2 becomes one column (snippet, title,
text); the numbers go two by two; pricing cards scroll sideways with the
next one peeking.

## Measures

- Content 960 to 1100px wide, centred; section padding 96 to 128px on wide
  screens.
- Problem row: 442 and 598px, gap 96px. Features: 552 and 552px, gap 32px.
  Team: 468 and 572px, gap 96px. Steps: 4 columns of 263px, gap 28px. Stats:
  4 equal columns divided by 1px vertical rules.
- Type, three families, each with one job: a geometric sans (Geist) for
  headings and interface (H1 96px, weight 600; H2 48px, weight 400); a serif
  (Fraunces) in italic for the emphasised words and for feature titles (21px,
  weight 500); a monospace (JetBrains Mono) for labels, dates and units
  (11 to 12px, uppercase, 2 to 3px tracking).
- Colour: warm paper (about 94% lightness) and a deep navy (about 12%), ink
  near-black on paper, off-white on navy, one muted blue for the italics on
  paper and a gold on navy. Nothing else.
- Framed product window: 16px radius, deep soft shadow, bracket marks at two
  corners; UI snippets in a pale inset frame with a 12px radius.

## Anatomy worth taking

- **Evidence as the images**: the product's real screens and pieces of its
  interface stand where icons and stock photos usually go.
- **One big number with its label and a vertical accent line**, beside the
  problem it measures. Numbers only when real, with the date they were true.
- **Italic serif for the turn in a sentence**: the last word of the claim,
  or the second half of a statement, set in the italic serif and the accent
  colour. One word or phrase per heading, the one that carries the meaning;
  never whole paragraphs.
- **Numbered rows as a list of what you get**: bordered rows with a small
  number (01 to 04) and one line each, the first highlighted.
- **Team as a list**: a large italic initial, the area of practice, one line;
  hairlines between rows. No stock headshots.
- **Testimonials one at a time**: a large italic quote, the person's name and
  role under a hairline, a counter ("03 / 04") and previous and next buttons.
- **Pricing card**: the name and the price on one line, who it is for, the
  price in the local currency under it, one outline button, a "What is
  included" divider, then a check list. One chip on the tier that deserves
  it, sitting on the card's border.
- **Footer with a disclaimer**: the brand, one line on what the product is
  and is not, contact, then columns of the links that exist.

## When it fits, and when not

For a product with several features, a team to show and paid plans, sold to
professionals. The landmark painting, the paper and navy, and the italics
come from its audience; a product for designers or for gamers takes the
skeleton (proof, product in a window, real snippets, dated numbers, list
team, one quote at a time, honest pricing) with a look of its own.
