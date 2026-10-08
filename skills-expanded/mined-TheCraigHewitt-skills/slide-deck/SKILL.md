---
name: slide-deck
description: "Generate a polished, presentation-ready HTML slide deck from a topic, document, or set of notes. Use this whenever the user says 'make a slide deck,' 'build a presentation,' 'turn this into slides,' 'create a deck for,' 'pitch deck,' 'investor deck,' 'training deck,' or asks for slides on any topic. Outputs a single self-contained HTML file with scroll-snap navigation and a clean visual system. The deck should look like a designer made it, not a default template."
---

# Slide Deck

You generate a single-file HTML slide deck that the user can present in a browser, share as a link, or export to PDF. Output should look professional out of the box — not a default Reveal.js template, not corporate clipart.

## Before you start

Get just enough context to make the deck specific:

1. **Topic** — what's the deck about, in one sentence?
2. **Audience** — who's it for? (Internal team, customers, investors, conference, students)
3. **Length** — rough number of slides (default 12–15 if unspecified)
4. **Source material** — point to any docs, notes, or transcripts in the working folder, or paste raw input
5. **Tone** — formal, casual, punchy, dry?
6. **Brand** — any colors, fonts, or visual references? Check for a `BRAND.md` or `brand-guidelines.md` in the folder first.

If the user said something like "make a deck on X" with no further detail, infer aggressively and just produce a draft — they'll redirect if it's off.

## Structural template

For most decks, this 5-act structure works:

1. **Title** — one slide, big idea + presenter
2. **The hook** — 1–2 slides setting up why this matters now
3. **The argument** — 6–10 slides making the case in beats
4. **The pivot / payoff** — 1–2 slides on the takeaway, reframe, or ask
5. **Close** — 1 slide: contact, next step, CTA

For specific deck types, adapt:

- **Pitch deck** — problem / solution / market / traction / model / team / ask
- **Training deck** — outcome / context / method (multiple slides) / examples / practice / next steps
- **Conference talk** — story open / problem / journey / framework / examples / call to action
- **Internal update** — TL;DR / metrics / what shipped / what's next / decisions needed

## Visual system

Default style if no brand reference is provided:

- **Layout** — generous whitespace, max 1 idea per slide. No walls of text.
- **Type** — one sans-serif for headings (Inter, IBM Plex Sans, or similar), one for body. Headings large (60-90px), body comfortable (24-32px).
- **Color** — light background (off-white or near-white), one strong accent color (default: a confident teal or muted blue), neutral text. Use the accent sparingly — for one number, one word, one underline per slide max.
- **Imagery** — prefer simple geometric shapes, charts, and typographic emphasis over stock photos. If you do use imagery, keep it consistent in style.
- **Slide numbers** — small, bottom-corner, unobtrusive.
- **Transitions** — none, or a clean fade. No swooshes.

If the user provides brand colors / fonts, use them. If they provide a reference deck or website, mirror its visual language.

## Technical implementation

Single self-contained `.html` file. Save as `slides-[topic-slug].html` in the working folder.

Required features:

- **Scroll-snap navigation** — each slide is a full viewport, scrolls cleanly between
- **Keyboard navigation** — arrow keys + spacebar to advance, Esc for overview
- **Slide counter** — small "3 / 15" indicator
- **Print/PDF stylesheet** — ensure each slide prints to one page, no awkward overflow. The user will export to PDF often; this needs to work.
- **Responsive** — readable on a laptop, projector, and big external display. Don't over-optimize for mobile.

Use vanilla HTML/CSS/JS. No external dependencies, no CDN fonts that might not load offline. Embed any custom fonts as base64 if needed, or use system font stacks.

## Content rules

1. **One idea per slide.** If a slide has two competing ideas, split it. The discipline of one-idea-per-slide is what separates good decks from "wall of bullets."
2. **Headings do the work.** A slide's heading should communicate the takeaway on its own. Body content supports it. Don't make the audience read body copy to figure out what the slide is saying.
3. **Numbers get their own slide.** A big number ("$1.5M ARR" or "62% retention") deserves a full slide. Don't bury it in a bullet.
4. **No bullet lists longer than 3 items.** If you need 5 bullets, split into two slides or rethink the structure.
5. **Charts over tables.** If you're showing data, use a chart. If you must use a table, keep it to 4 rows max.
6. **Speaker notes (optional).** If the user asks, add `<aside class="notes">` blocks with what to say off-slide. Keep notes shorter than the slide content — they're prompts, not scripts.

## After generating

Tell the user:

1. The path to the file
2. How to open it (just double-click or `open slides-x.html`)
3. How to navigate (arrow keys / scroll)
4. How to export to PDF (print to PDF in their browser)
5. What to ask for if they want changes — common ones: tighter copy, different visual style, add/remove slides, change tone

## Customizing later

If the user comes back saying "make these more [X]," adjust holistically — re-render the whole deck rather than patching one slide. Decks should feel cohesive.

## Why this is built this way

Slide tools (PowerPoint, Keynote, Slides) make it easy to overload slides with text and hard to look professional without a template. Generating a deck as HTML lets us enforce one-idea-per-slide by design and produces something that actually looks designed. The user can always export to PDF for sharing.
