---
name: ui-page-landing
description: "How to build a landing page for one product or service from its own story: the hero with the claim, the audience and one action, proof beside the claim, how it works as the real steps, features shown as evidence, pricing and social proof only when real, a real FAQ, the closing action, varied sections, the waitlist variant, search basics and a fast first screen. Read before building or reworking a landing page."
---

# Landing page for one product or service

The generated landing page is one template for every product: a gradient
hero with a slogan, a row of logos nobody agreed to, three icon cards
(Fast, Secure, Scalable), invented numbers, three stock-photo testimonials,
three price tiers with "Most popular" in the middle, a generic FAQ and a
"Get started" band. None of it says what this product does, for whom, or
why anyone should believe it. This skill starts from the product's story,
lets it choose the sections, and fills each with evidence. Write the
blueprint first (`ui-structure` has the landing page's regions in order and
the skeleton in numbers) and build each control to `ui-anatomy`.

One kind of page. The measures are in `ui-layout`, section compositions in
`ui-part-sections`, the concept in the `ui` skill (section 1), the words in
`writing`. Two worked examples: `ui-reference-launch` and
`ui-reference-saas`.

## 1. The story chooses the sections

Answer each question in one line, from what you were given (the README,
the product, the brief), never from invention:

1. Who is it for, in their own words?
2. What do they do today, and what goes wrong?
3. What does the product change? (the claim)
4. How does it work, as the steps a user really takes?
5. What can be shown to make it believable?
6. What does it cost, and what is the one next step?
7. What do people ask before they commit?

An answer with content becomes a section; an answer without content is
cut, not padded. The order follows the reader's doubts, not a template.

| The product | Sections, in order |
|---|---|
| Software whose screens sell it | Hero with the product in use, the workflow step by step on real screens, the two or three things only it does, proof, pricing, questions, closing action |
| A tool replacing a chore | Hero with the claim, the old way beside the new, how it works, proof, how to start |
| A service (a studio, a course, a programme) | Hero with the offer and who it is for, what you get, how it runs (dates, sessions, deliverables), who runs it, price and terms, questions, booking |
| Before launch | Claim and real output, what is inside, how it works, sign-up (section 9) |

## 2. The skeleton

1. Header: the name left, three to five links, one action right; it
   sticks (`ui-part-header`).
2. Opening: the headline and one line of support on the left (7 of 12
   columns), a real image or screenshot on the right (5 of 12); on a phone,
   text then image. Or text alone, left-aligned, when there is no real
   image.
3. The problem or the use: one section in prose or a short list, showing
   the product in the context it is used.
4. How it works or what you get, shaped by the content: steps if there are
   steps (as many as there are), a comparison if it replaces something, a
   screenshot with callouts if it is software.
5. Proof, only if real: a quote with a name, a figure with a source.
6. Price or how to start, if there is one.
7. Closing action: one line and the primary action again.
8. Footer: contact and the links that exist.

```
│ ◉ Name      How it works  Pricing  Docs  FAQ        [ Primary action ] │ sticky
│ The claim in the display face, twelve words     ┌────────────────────┐ │
│ or fewer, its consequence in the muted colour.  │ the product in     │ │
│ One line: for whom, and what changes.           │ use, a real        │ │
│ [ Primary action ]   How it works →             │ screenshot         │ │
│ "A real quote, in their words." Name, role      └────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ LABEL  A heading that says the point      One sentence on what it      │
│                                           means for the reader.        │
│ ────────────────────────────────────────────────────────────────────── │
│ 1 Import          │ 2 Check            │ 3 Send                        │
│ [real screen]     │ [real screen]      │ [real screen]                 │
├────────────────────────────────────────────────────────────────────────┤
│ The lead feature, larger, with       │ Other features, as a list:      │
│ a piece of the real interface        │ name · one line · link          │
```

## 3. The hero

- What it is, for whom, and the one action (`ui-part-hero`). The claim in
  twelve words or fewer, passing the competitor test: with a rival's name
  in it, it no longer holds.
- The supporting line names the audience and the result, at body size or
  one step up.
- One filled button that says what happens: "Download for macOS", "Book a
  20-minute call", "Start a free trial" only when there is one. A
  secondary text link to the proof or how it works. Never two primaries.
- The proof in the same screen: the product in use, its real output, a
  real quote, a dated figure.
- As tall as its content (320 to 560px), never `100vh`: on a 1440 by 900
  laptop the next section starts in view.

## 4. Proof near the claim

- The strongest evidence beside, or directly under, the claim it supports;
  each later claim carries its own evidence in its section.
- Kinds: a screenshot cropped to the part that matters at a readable size
  (not a whole dashboard shrunk to a blur); a short scripted demo of the
  real interface (`motion-demo`); a real command and its real output for a
  developer tool; before and after for a service; a customer's result with
  their name and permission; a number with its source and its date ("as of
  May 2026").
- With none of these, say precisely what the product does and let the
  product itself be the picture. No placeholder statistics.

## 5. How it works, features

- The real steps, as many as there are (two or five, not three by habit):
  what the person does, what they get back, the real screen or artefact
  beside each. Numbered only when order matters.
- When it replaces something, a comparison beats steps: the old way and
  the new in two columns, row by row.
- Features as evidence: the one or two that decide a purchase, each larger,
  shown with a piece of the real interface or output and a heading that
  states the point ("Reminders go out on day 7, by WhatsApp"); the rest as
  a compact list (name, one line, a link). No icon cards, no feature
  without something to show or a concrete detail (`ui-part-cards`).

## 6. Pricing, proof from others, questions, the close

- Pricing only when it is public (`ui-part-pricing`): the real plans in
  the local currency with the period and the tax note, what the button
  does next; `[Price]` placeholders when not given. A monthly and yearly
  switch only when both exist, with the real saving.
- Social proof real or none (`ui-part-social-proof`): a quote with the
  person's name, role and company and their permission; logos of customers
  who agreed; ratings only with their source (an app store, a review site)
  linked.
- An FAQ only with the questions people actually ask (from sales calls,
  support, reviews), answered in two to four sentences with a link onward,
  as `details` and `summary` (`ui-part-faq`). Invented questions are worse
  than none.
- The closing action once: one line on why now and the same verb as the
  hero's button (`ui-part-cta`). The footer: contact, the links that exist,
  the privacy policy when the page collects an email (`ui-part-footer`).

## 7. Rhythm

- Vary the sections: alternate a text-led section with a visual-led one,
  contained with full-bleed, left-weighted with right-weighted.
- Introduce a section with a pair: a small label and the heading on one
  side, the sentence that explains it on the other, over a hairline.
- Space between sections 96 to 128px on wide screens, 64 to 80px on
  phones; a full-bleed band of colour once or twice, not every other
  section; one filled button per view.
- Motion at dial 2 or 3 (`motion`): content arriving as it scrolls only
  where the arrival says something (`motion-reveal`); the first screen
  never waits for a script.

## 8. On a phone

- The claim at 31 to 39px, the action in the first screen under the
  supporting line, the image after the text.
- The sticky header keeps the name and a short action ("Start trial");
  the links fold behind a labelled "Menu".
- Steps and features in one column; comparisons scroll in their container
  or become stacked pairs; price plans stacked, or scrolling sideways with
  the next one peeking.
- The page runs well past three screens, so it has a back-to-top control
  (`ui-part-back-to-top`).

## 9. Before launch: the waitlist variant

- `ui-reference-launch` is the worked example: the claim, the real output
  or a real preview, what is inside, how it works, the sign-up.
- The sign-up as one control: an email field (`type="email"
  autocomplete="email"`) joined to a button that says what it does ("Join
  the waitlist"), and under it what the address is for and how often you
  will write.
- Success shown in place ("You are on the list. We will email you once,
  when early access opens."); a confirmation email where the law asks for
  double opt-in.
- The form stores the address somewhere real, with a honeypot and a rate
  limit. No "Join 10,000 others" unless counted, no launch date unless
  set, no countdown.

## 10. Search engines and the first screen's speed

- The page in the served HTML (static or server-rendered); the claim is
  the `h1` as text, never in an image.
- A title of 50 to 60 characters (what it is and the name), a description
  of 120 to 160, a canonical URL, an Open Graph image of 1200 by 630 that
  shows the product, and JSON-LD (`Organization`, `SoftwareApplication` or
  `Product`) with real facts only (`frontend-seo`).
- The first screen within budget on a mid-range phone: LCP under 2.5s, CLS
  under 0.1 (`frontend-performance`). The hero image in AVIF or WebP with
  `srcset` and `sizes`, its width and height set, `fetchpriority="high"`,
  never lazy; everything below it lazy.
- One or two `woff2` fonts preloaded with `font-display: swap` and fallback
  metrics (`size-adjust`), so the headline does not jump when they arrive.
- A hero video only with a poster, muted, and a pause control; chat
  widgets and analytics after the page has loaded; script for a content
  page under about 150 kB compressed.

## Check it

- Put a competitor's name in place of the product's: every section that
  still holds is generic, and is rewritten or cut.
- `ui_check`: buzzwords, "Get started" and "Learn more", invented figures,
  default gradients, emoji; fix the high and medium findings.
- `preview` at 360, 768 and 1440px: overflow, contrast, dead links (every
  nav link reaches a section that exists), the sticky header, back to top;
  with `motion: true` when anything moves.
- Lighthouse on mobile for LCP and CLS; the page source shows the claim and
  every section as text.
- Send the form: the address arrives where it should, the success state
  shows, and a failure says what to do.
- List every placeholder left (prices, quotes, figures, images) in the
  report.

## Avoid

The template order whatever the product; logos of companies that are not
customers; three icon cards; invented statistics, testimonials and
ratings; "Most popular" with no reason; questions nobody asked; "Get
started" and "Learn more"; gradient headline text; a `100vh` hero with a
scroll-down arrow; a carousel in the hero; sound that plays by itself; a
pop-up on arrival; a countdown to nothing; one section composition repeated
down the page; a call-to-action band after every section.
