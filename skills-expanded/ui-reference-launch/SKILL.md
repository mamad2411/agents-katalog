---
name: ui-reference-launch
description: "A worked reference, measured from a hand-designed launch page: a product before or at launch (early access, a waitlist, a developer tool) on one page. Its skeleton, wireframes, measures and component anatomy, and what to take from it. Read before building a launch, waitlist or single-product page."
---

# Reference: a launch page

Measured from a hand-designed page (enowx.ai, an AI coding tool in early
access). Take its structure and its decisions; its words, name, colours,
logo and background belong to it. Its concept is its own: find yours from
your product (the `ui` skill, section 1).

**Its concept**: the page reads like the product's own report. The hero's
visual is a real example of what the product produces, and every section
after it is set as plainly as a document: a label, a heading, a sentence,
then a ruled grid of facts.

## Skeleton

1. Header, sticky, 77px.
2. Hero, about one screen: the claim, the sign-up, and the product's real
   output beside them.
3. "What is inside": six capabilities.
4. "Who does the work": three roles.
5. "How it works": four steps.
6. The sign-up again, with what happens after it.
7. Footer.

Sections 3 to 6 share one composition (below), which is what makes the page
calm: the reader learns the pattern once.

## Wireframes (wide screen)

```
┌───────────────────────────────────────────────────────────────────────┐
│ ✕ WORDMARK / early access    ( Link  Link  Link  Link )   (Sign up)  │ 77px, sticky
├───────────────────────────────────────────────────────────────────────┤
│ [◷ status chip]                                                       │
│ The claim, in one line,                     ┌──────────────────────┐ │
│ its consequence in the muted colour.        │ ● ● ●  example output│ │
│ One paragraph, about 60 characters wide,    │ LABEL   value        │ │
│ saying what it is and what it does.         │ LABEL   value        │ │
│ ┌──────────────────────────┬───────────┐    │ LABEL   value        │ │
│ │ email field              │ [ Button ]│    └──────────────────────┘ │
│ └──────────────────────────┴───────────┘                             │
│ small note: what the address is used for                              │
│ [ community button ]   link to the first section                      │
├───────────────────────────────────────────────────────────────────────┤
│ SECTION LABEL                                                         │
│ Heading of the section.              One sentence that explains it,  │
│                                      set against the heading's base. │
│ ───────────────────────────────────────────────────────────────────── │
│ ┌───────────────────────┬───────────────────────┬───────────────────┐ │
│ │ area/name             │ area/name             │ area/name         │ │
│ │ [▢] Title             │ [▢] Title             │ [▢] Title         │ │
│ │ Two or three lines.   │ Two or three lines.   │ Two or three      │ │
│ ├───────────────────────┼───────────────────────┼───────────────────┤ │
│ │ ...                   │ ...                   │ ...               │ │
│ └───────────────────────┴───────────────────────┴───────────────────┘ │
└───────────────────────────────────────────────────────────────────────┘
```

On a phone: the header keeps the brand and the button; the hero stacks
(text, form, then the output panel); the form's field and button stack, the
button full width; every ruled grid becomes one column.

## Measures

- Container 1240px, centred. Hero columns 633 and 551px, gap 56px (about 7
  and 5 of 12). Section intro columns 588 and 588px, gap 64px.
- Ruled grid: 3 columns of 412px (4 of 309px for steps) with a 1px gap over
  a line-coloured background, so the gaps draw the lines; cells padded 24 to
  32px; no shadows, no radius beyond a few pixels.
- Type: one family (IBM Plex Sans) for everything, a monospace for the
  output panel and the small tags. H1 56px, weight 400, tracking -1.9px; H2
  36px, weight 400; H3 16px, weight 500; labels 14px uppercase, 2px
  tracking; body 16px.
- Colour: near-black background (about 4% lightness), off-white text, one
  muted grey for second lines and notes, the button inverted (light on
  dark). No accent colour beyond that.

## Anatomy worth taking

- **Header**: brand at the left with a small status label beside it (early
  access, beta); the in-page links centred in one pill; the one action at
  the right as an outline pill. The links point at sections that exist.
- **Two-tone headline**: the claim in the text colour, its consequence on
  the second line in the muted one. One sentence, two weights of meaning.
- **Sign-up as one control**: the field and the button joined in a single
  bordered box; the note on what happens to the address directly under it,
  not in a footer.
- **The product's real output as the hero image**: a bordered panel with a
  title bar holding label and value rows the product actually produces. Not
  a mock-up of a dashboard, not an illustration.
- **Section intro as a pair**: label and heading on the left, the
  explanation on the right, aligned to the heading's baseline, a hairline
  under both. Instead of a centred heading and subtitle over three cards.
- **Ruled grid of facts**: cells divided by hairlines, each with a small
  monospace tag naming its area, a small icon in a square, a title and two
  or three lines. Steps use the same grid with short lines instead of
  paragraphs; the closing section numbers its cells 01, 02, 03.
- **Footer**: the logo, one line on what it is, the year; the same section
  links at the right.

## When it fits, and when not

For one product with one action (join, try, install), especially before
launch. Its dark, monospace-tagged look suits a developer tool; for a
bakery, a clinic or a school, keep the skeleton (claim, evidence, pair
intros, ruled facts, one form) and take the look from that product's own
concept.
