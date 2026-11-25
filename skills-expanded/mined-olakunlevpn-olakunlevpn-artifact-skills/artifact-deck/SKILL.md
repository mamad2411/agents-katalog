---
name: artifact-deck
description: OUTPUT IS ALWAYS A SINGLE `.html` FILE (never `.md`, never separate per-slide files) containing multiple slides navigated by arrow keys. Use this skill whenever the user asks for a slide deck, presentation, talk, "Friday demo", "share-out slides", "exec readout", "kickoff deck", "lightning talk", arrow-key deck, keynote-style outline, or any artifact whose primary shape is "a sequence of slides you advance through". Pair with `artifact-css` for the underlying design system. Do NOT use for single-page reports — those are `artifact-report`.
---

# artifact-deck

> ## OUTPUT CONTRACT
>
> **Produces ONE `.html` file.** A slide deck is multi-slide by definition; all slides live inside the same file and are switched by JavaScript (arrow keys, click on the chrome, hash routing). NEVER one file per slide. NEVER a `.md` outline.
>
> File extension is `.html`. File name typically `<topic>-deck.html`.

---

A single-file slide deck. Navigate with arrow keys, click the dots, or drag the URL hash. The reader can jump straight to slide N via `#/N`. The deck is presentation-mode by default — chrome stays minimal, content sits center-screen.

Read `artifact-css/SKILL.md` first for the full OUTPUT CONTRACT, design tokens, and class vocabulary. This skill uses **no jQuery** — slide nav is ~30 lines of vanilla JS.

## When to reach for this skill

- User says "make me a deck for X", "Friday demo slides", "kickoff deck", "exec readout", "lightning talk".
- User has 5-15 short ideas they want to walk a viewer through in order.
- User wants something they can present in a meeting without firing up Keynote / Google Slides.

If they want a one-page summary, use `artifact-report`. If they want a clickable mockup with hotspots, use `artifact-flow`. If they want a long narrative, use `artifact-explainer`.

## Anatomy of a deck

Built from four element types. Use them in order.

1. **Header bar** — fixed-position chrome at top with: deck title, current slide number / total, optional progress bar. Stays visible across all slides.
2. **Slide container** — a `<section class="slide" id="s-N">` per slide. Only the active slide is visible. Each slide is its own flexbox-centered viewport (`100vh - header`).
3. **Slide content** — one of these shapes per slide:
   - **Title slide** — eyebrow + h1 + lead. The cover.
   - **Statement slide** — one giant headline. No subhead. Used when the slide is a single point.
   - **Two-column slide** — `.grid-2` with image/code/list on each side.
   - **Stat slide** — `.stats` grid for 2-4 big numbers.
   - **Timeline slide** — small `.timeline` showing progression.
   - **Code slide** — `.code-block` with one focused snippet, mono large.
   - **Closing slide** — eyebrow + h2 + call-to-action.
4. **Footer chrome** — fixed-position bottom-right: prev / next buttons, slide counter, "Press → to advance" hint.

Five to fifteen slides is the right zone. Fewer = no point of a deck. More = it's an article.

## Voice and density rules

1. **One idea per slide.** If a slide needs more than one h2, split it.
2. **Big type.** Body text below 18px shouldn't appear on a deck slide. The reader is 6 feet from a screen.
3. **No paragraphs.** A slide with three sentences of prose is a slide that should have been a stat or a bullet list.
4. **No bullet soup.** Three to five bullets max per slide. Beyond that, split.
5. **Numbers, names, and verbs.** A slide that says "We made progress on infrastructure" is a slide that should have been deleted. Replace with "Cut p99 latency 38% across 3 services."

## Navigation contract

- **→ / Space / PageDown** — next slide.
- **← / PageUp** — previous slide.
- **Home / End** — first / last slide.
- **Click anywhere on the slide chrome (not on a link or button)** — next slide.
- **Hash routing** — `#/3` jumps to slide 3. Updates as you navigate so the URL is shareable.
- **F or `?`** — toggle a help overlay listing the shortcuts.

The JS that wires this is ~30 lines, included in the template.

## Fallback contract

With JS disabled:
- All slides render stacked top-to-bottom (one after another).
- Each slide has its own scroll target.
- The header / footer chrome still renders but the prev/next buttons are dead.

Reader still gets the content. Just no presentation polish.

## Common mistakes

- **Slide deck as long-form article.** If your slides are paragraphs, you wanted `artifact-explainer`.
- **Two ideas per slide.** Reader can't track. Split.
- **Tiny screenshots.** A 240×180 PNG on a 1920×1080 deck is unreadable. Either it fills 60%+ of the slide or it doesn't belong.
- **No closing slide.** Decks need a "what now" slide — next steps, links, contact. Otherwise the deck just stops.
- **Auto-advance.** Don't add timed advance. Presenter controls the pace.

## After the artifact

Offer the plain-text outline alongside: one line per slide, prefixed with the slide number. Useful for speaker notes or for pasting into a thread that won't render the HTML.
