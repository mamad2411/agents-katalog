---
name: html-deck-building
description: Use when building or editing a medical presentation as an HTML deck (single offline file, motion graphics, presenter laser/pen tools), after the plan is approved and claims and figures exist, or when an HTML deck renders with overflow, stutters, or needs a template applied.
---

# HTML deck building

## Before you start

This skill is stage 6 of grand-rounds:medical-deck. Work only inside a talk folder whose
`STATUS.md` marks the Plan as `done, approved` and which has `evidence/claims.json`. If
either is missing, stop and call the Skill tool with grand-rounds:medical-deck instead: it
runs the interview, the plan and the evidence first. This holds for a new deck from a
one-line request too.

## Overview

Start from `assets/deck-engine.html`: a 1920 × 1080 stage that scales to any screen. It has
fragments, speaker notes, a cross-fade between slides, presenter tools (laser, circle,
pen, undo, erase), keyboard and clicker control, and a `window.deck` API for the render
checker. You write slides and theme. You do not rewrite the engine.

## Procedure

1. Write the slides in `<talk>/build/slides.html`, deck-specific CSS (theme variables
   first) in `deck.css`, and chart code in `deck.js`. Then assemble the source from the
   engine, so engine fixes reach every deck:

   ```bash
   python scripts/compose_deck.py --slides <talk>/build/slides.html --css <talk>/build/deck.css \
     --js <talk>/build/deck.js --title "<talk> · <presenter>" --lang vi --cite "<footer citation>" \
     -o <talk>/build/index.src.html
   ```
2. **Theme.** Start `deck.css` with a `:root{…}` block holding the `theme/theme.json` values
   (it overrides the engine defaults). If there is a
   template, rebuild its chrome (header band, footer, logo, title layout) in CSS from the
   measured geometry. Keep the logo as a file and reference it; the build inlines it.
3. **Slides.** One `<section class="slide" data-name="…">` per row of `plan.md`, in order:
   - the plan's assertion as the title (`h2.t`, or the template's title element);
   - the visual from `figures/` via `<!--include: ../figures/s05-km.svg-->` or `<img>`;
   - only numbers from `claims.json`, written as in the source and formatted for the
     deck's language (`0,58` in Vietnamese, `0.58` in English);
   - `<aside class="notes">` with what the presenter says, including cues such as
     "[click] 24-month landmark". **Cues never go on the slide.**
   - a per-slide `data-cite="…"` when the slide's source differs from the deck's.
4. **Motion.** Use the engine's classes: `.a-in` with `style="--d:.3s"` for staged entry;
   `.draw` with `pathLength="1"` for connectors; `.pop` for arrowheads; `data-frag="n"`
   for click-revealed overlays; `data-scene="n"` for a mechanism stepped by clicks. A
   looping motion graphic (a mechanism that plays like a video) carries its own CSS loop
   and `data-poster`. For large figures, use the `.km` wipe structure. Follow
   `medical-figures` → `motion.md`: transforms and opacity only.
5. **Build** one offline file:

   ```bash
   python scripts/build_deck.py <talk>/build/index.src.html <talk>/out/<name>.html
   ```

6. **Check** with a real browser:

   ```bash
   python scripts/check_render.py <talk>/out/<name>.html --out <talk>/build/render --smooth <slide with the main animation>
   ```

   It needs Playwright for Python (`pip install playwright`). It uses an installed Edge or
   Chrome, so `playwright install` is needed only on a machine with neither. If you cannot
   install it, open the deck in a browser tool and screenshot every slide instead, and say in
   the delivery report that the automatic check did not run. Never skip the check silently.

   Fix every `off-stage` and `clipped-or-overflowing` finding by cutting words, splitting
   the slide, or re-laying out. Never fix overflow by shrinking text below 18 px (body 24 px).
   Then open `contact.html` and look at every slide yourself. The script cannot see
   collisions, bad wrapping (a number split from its unit) or a figure that is too small.
7. Hand `render/dom.html` to the slop audit. It contains text that JavaScript adds at run
   time, which the source file does not show.

## Type and layout floor (1920 × 1080)

| Element | Minimum |
|---------|---------|
| Title | 48 px (template may set larger) |
| Body text | 24 px |
| Figure labels, tables | 18 px |
| Footer / source credit | 16 px |
| Margins | 80 px left/right |

## Common mistakes

| Mistake | Fix |
|---------|-----|
| A presenter hint in the footer ("▸ click for HR by period") | Speaker notes only |
| Content vanishes before the slide fades out | Engine handles it; don't remove `.play` yourself |
| Animating a big SVG with `setAttribute` in `requestAnimationFrame` | Wipe reveal with transforms |
| Fonts from a CDN | Inline them (`@font-face` with a local file, inlined at build) or use the template's system fonts |
| Same title + three-cards layout on every slide | Pick visuals per `deck-planning` → `visual-grammar.md` |
