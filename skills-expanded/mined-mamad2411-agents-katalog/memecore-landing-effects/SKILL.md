---
name: memecore-landing-effects
description: Visual-effect primitives for the Claude-demo / Maverick landing page in MemeCore vibe-marketing register. Catalogs 9 CSS+SVG-filter effects from Artur Bień (expensive.toys / 98.css / Whop design system) — blur vignette, ambilight, RGB anaglyph, heat-map, masks, fancy reveals, ASCII canvas — each with source URL, register guidance, and integration notes. Used by the landing-page-generator skill creator to compose forensic-investigation-tone marketing pages.
tier: POWERFUL
category: Product Team
domain: Marketing / Visual Design / CSS-SVG-Filters
register: memecore (forensic-investigation tone — wallet-hashes-as-entities, timeline tables, DECF per-finding pills, third-person reportorial)
attribution_required: true
upstream_author: Artur Bień (github.com/arturbien · expensive.toys)
---

# MemeCore Landing Effects

A primitive library of 9 visual effects for the Claude demo / Maverick Industries landing-page skill creator. Every effect originates from Artur Bień's blog at **expensive.toys** and his retro/glassmorphic design work (he authored the Whop app design system and the React95 / 98.css libraries). The skill creator stitches these primitives into landing-page sections in the **MemeCore vibe-marketing** register.

## Why these specific effects

The MemeCore register (per `project_memecore_temp_variance_dialect.md`) is **forensic-investigation tone for marketing**. The reader feels like they're reading a leaked DEA dossier on why-this-product-matters. Visual register has to match: heat maps (thermal imaging vibes), RGB anaglyph glitch (surveillance feed), ambilight (CCTV edge glow), blur vignette (focus on a target), CSS masks (redaction / cutout reveal), ASCII canvas (terminal-output-as-art).

Artur's effect library was *designed* for this register without being labeled that way. Pulling it in is a register match, not a style import.

## Attribution discipline

Every section that uses an Artur effect ships with attribution in the page footer:
> Visual primitives by [Artur Bień](https://expensive.toys/) · used with credit, MIT-spirit
Failing to attribute breaks the trust register. Forensic-investigation tone requires sources.

---

## The 9 primitives

### 1. Blur Vignette · Hero focal-point
- **Source:** https://expensive.toys/blog/blur-vignette
- **Date:** June 2023 · **Tech:** pure CSS · **Engagement:** 18,620
- **Effect:** soft-blurred outer ring, sharp center — drives eye to the focal point.
- **Use for:** hero section. Center the headline + Otto avatar; let everything else feather out.
- **Register cue:** "the file in the center is the only one that matters."
- **Key primitive:** `backdrop-filter: blur(...)` masked by a radial gradient.

### 2. Ambilight · Section edge-glow
- **Source:** https://expensive.toys/blog/ambilight
- **Date:** April 2023 · **Tech:** CSS + SVG filter · **Engagement:** 4,575
- **Effect:** TV-style edge bloom — content emits its own dominant-color halo into the surrounding space.
- **Use for:** product screenshots, demo videos, before/after splits.
- **Register cue:** "evidence pack rendered as evidence — it glows because it's hot."

### 3. RGB Split / 3D Anaglyph Glitch · Surveillance feed
- **Source:** https://expensive.toys/blog/rgb-split-glitch-effect
- **Date:** April 2023 · **Tech:** CSS + SVG filter · **Engagement:** 2,731
- **Effect:** RGB channels offset on hover/scroll — chromatic aberration, anaglyph 3D feel.
- **Use for:** the "what could go wrong" section. Probabilistic-AI-without-governance visualized as drift.
- **Register cue:** "this is what your pipeline looks like when the gate is down."

### 4. CSS Heat Map (color grading) · Cohort visualization
- **Source:** https://expensive.toys/blog/css-heat-map
- **Date:** January 2023 · **Tech:** CSS · **Engagement:** 3,557
- **Effect:** numeric data → color-graded heat map purely in CSS, no chart lib.
- **Use for:** "user CI scores across the cohort" visualization. PI archetype distributions. Drift-tolerance bands.
- **Register cue:** "cohort heat-map: every Smart Touch Point is a pixel."

### 5. CSS Heat Map / Thermal Vision (SVG filters) · Activity surveillance
- **Source:** https://expensive.toys/blog/heat-map-thermal-vision-svg-filter
- **Date:** February 2023 · **Tech:** CSS + Data-viz + SVG filter · **Engagement:** 3,684
- **Effect:** thermal-camera vision applied to any DOM node — humanlike content glows.
- **Use for:** the "where the system is hot" panel — live truth-config gate firing rates, drift alerts, runtime telemetry.
- **Register cue:** "thermal feed of the substrate — glow = drift."
- **Differs from #4:** #4 is data→heat-color; this is DOM→thermal-imaging-overlay. They compose.

### 6. Fancy Reveal Animations (CSS masks + @property) · Drop sequencing
- **Source:** https://expensive.toys/blog/fancy-reveal-animations-with-css-masks-and-property
- **Date:** April 2023 · **Tech:** CSS · **Engagement:** 9,926
- **Effect:** scroll/hover reveals using animated CSS masks via the @property API.
- **Use for:** the doctrine drops — "Governance is a file" reveals from behind a redaction mask. Smart Touch Points list reveals one by one.
- **Register cue:** "declassified, line by line."

### 7. HTML Elements as CSS Masks · Knockout / cutout
- **Source:** https://expensive.toys/blog/html-elements-as-css-masks
- **Date:** April 2023 · **Tech:** CSS + SVG filter · **Engagement:** 7,268
- **Effect:** use any HTML element (text, image, SVG) as a mask — knockout reveals through the shape.
- **Use for:** Otto-shaped cutouts revealing the hero image; logo-shape masks over screenshots.
- **Register cue:** "the silhouette is the story — fill it with what's underneath."

### 8. Animated Blur Overlay · Modal / focus state
- **Source:** https://expensive.toys/blog/animated-blur-overlay
- **Date:** September 2023 · **Tech:** CSS · **Engagement:** 1,927
- **Effect:** cross-browser overlay with smoothly animated backdrop filter blur.
- **Use for:** modal opens (sign-up, demo-request, archetype-probe screen). The Method-2 onboarding probe overlay.
- **Register cue:** "the rest of the page recedes — only this question remains."

### 9. Dynamic Canvas ASCII Art · Terminal aesthetic
- **Source:** Zac-prompted addition (2026-04-26) — pattern: live `<canvas>` rendering text at terminal density, color-graded by source-image luminance.
- **Tech:** Canvas 2D API + characterset density mapping (`@%#*+=-:. `).
- **Effect:** any image or live video → ASCII text rendering, frame-by-frame.
- **Use for:** "Otto on the terminal" — Otto avatar rendered as live ASCII; webcam → ASCII for the demo's "see yourself in the system" moment.
- **Register cue:** "the substrate looks at you. You look back. It writes you in characters."
- **Note:** not from Artur's blog directly — bundled here because the register match is identical (forensic / terminal aesthetic).

---

## How the skill creator uses this

The `landing-page-generator` skill, when invoked with `register=memecore`, calls this skill as a primitive library. Workflow:

1. **Section planning** — for each landing-page section (hero / problem / how-it-works / proof / pricing / CTA), pick one or two of the 9 effects whose register cue matches the section's job.
2. **Fetch implementation** — pull the actual CSS/SVG-filter code from the source URL (or local cache if mirrored). Do NOT hand-write Artur's code from memory; cite the source.
3. **Register-tune the copy** — pair the visual effect with MemeCore-register copy. Forensic tone, third-person reportorial, named entities, sources inline.
4. **Compose** — drop the effect + copy block into the page TSX/HTML.
5. **Attribution footer** — append the Artur Bień credit line.

## Pairing rules

- Don't stack RGB Split + Ambilight on the same element — they fight for the chromatic budget.
- Heat Map (#4) data + Thermal (#5) overlay COMPOSE — use both for the live-substrate visualization panel.
- Fancy Reveal (#6) is the doctrine-drop primitive — reserve it for the load-bearing message moments (3-5 per page max, more dilutes).
- Blur Vignette (#1) and Animated Blur Overlay (#8) are the two "focus" primitives — pick one per page-state, never both at once.
- ASCII Canvas (#9) is a high-cost moment — one per page, ideally above-the-fold or as the demo CTA.

## Output contract

When the skill creator emits a landing page using these primitives, every effect block in the source must include a comment header:

```html
<!-- effect: blur-vignette · src: https://expensive.toys/blog/blur-vignette · author: Artur Bień -->
```

This makes the page auditable post-generation — anyone reading the source can trace each effect to its origin.

## Open questions (do not silently answer)

- Whether to mirror Artur's source CSS into this repo (with explicit license / consent) vs. fetch-at-build-time. Fetch is safer; mirror is faster. Decide per page.
- Whether the ASCII Canvas (#9) deserves its own standalone skill — it's the only non-Artur one in this bundle, and it might grow legs.
- How effects degrade on touch surfaces (per Patent #4 dynamic-layer reframe — onboarding is touch-first). Hover-triggered effects need touch-equivalent triggers (long-press, force-touch).

## Discipline

- **Attribution is non-negotiable.** Every page emits the footer credit. Forensic register loses credibility without sources.
- **Don't fabricate Artur's code.** Fetch from source; if unreachable, fall back gracefully and note the gap. Hand-rolling CSS in his style without his code is misattribution.
- **MemeCore register is not "edgy."** It's *reportorial* — calm, named-entity, third-person, evidence-cited. The visual heat / glitch / thermal effects work BECAUSE the copy stays cool. If the copy gets hot, the visuals tip into noise.
- **One register at a time.** Don't mix MemeCore with corporate-deck or playboy register on the same page. Pick the lane and hold it.
