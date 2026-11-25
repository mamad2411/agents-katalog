---
name: design-quote-card
description: |
  Generate a pull-quote / insight card — TWO pixel-exact HTML canvases in one file: 1080×1080 (square, default) AND 1080×1920 (story variant). Text-dominant, Fraunces-led, no chrome. The quote IS the artifact. Reads ./design/<brand-slug>/DESIGN.md, tokens.css, and components.html. Triggers include "quote card for X", "pull quote", "insight card", "/quote-card".
---

# Skill: quote-card

Produces a single self-contained HTML file containing TWO pixel-exact canvases:

1. **Square** (1080×1080) — Instagram feed / LinkedIn / generic social
2. **Story** (1080×1920) — Instagram Story / Reel cover / vertical share

Both render the same quote at proportional scale for their format. Screenshot each separately for the appropriate platform.

This is the artifact format most prone to AI-default tells: large opening quotation mark glyph (❝), centered alignment as default, color-gradient backgrounds behind text. **All three are explicitly banned in this skill.** The quote IS the artifact — typography carries everything.

## When to use

- User wants to share a single insight, claim, or pull-quote as a standalone card
- A `DESIGN.md` exists for the brand

## Inputs

- **Required:** brand slug, the quote text (1 sentence, sentence-case ending in period per brand voice; max ~25 words)
- **Optional:** attribution (e.g. "Shane Logsdon, 2026" — usually omitted if the brand IS the speaker)
- **Optional:** source — link to the longer piece the quote is from
- **Optional:** type-accent — one word in the quote to set in `--color-accent`

## Output

`./design/<brand-slug>/artifacts/quote-card-YYYY-MM-DD-<slug>.html`

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

### 2. Gather the brief

Ask in one message:

```
1. Quote text — 1 sentence, sentence-case ending in period (max ~25 words; push back if longer)
2. Optional attribution — name + date, OR omit if the brand IS the speaker
3. Optional source — URL to the longer piece this quote is from
4. Optional type-accent word — one word from the quote to set in the brand's accent color (used as a SUBJECT marker, not generic emphasis)
```

If the user provides 26+ words, push back: "Quote cards work at 25 words or fewer. Cut the support — keep the claim. What's the line that lands?" Don't proceed until they agree.

### 3. Pick variation — ARCHITECTURE FIRST

Pick ONE archetype — quote cards reward severe restraint:

- `type-only` — the quote at MAX scale, asymmetric anchor (top-left or bottom-right), no chrome. Strongest for short claims.
- `inverse-text` — full canvas dark inversion (canonical v2 feature treatment). The quote in cream on ink. Reads with conviction.
- `pattern-led` — repeating text fragments as background; the quote breaks through as the punctum. Risky — only use if the quote concept invites the device.
- `inverted-text` — quote carved out of a body-text wall (the body is the negative, quote is the positive). Editorial-architectural.

Then pick:
- **Layout**: `top-anchored | bottom-anchored | off-grid | center-anchored` (center-anchored only if the quote is a single short line — center as default is the AI tell to avoid)
- **Color usage**: `monochrome | single-accent | inverted` (inversion often strongest for quotes)

**Cross-artifact rule:** if a recent quote card for this brand used the same archetype, vary it. Two quote cards in a row with the same treatment dilutes both.

### 4. Generate the HTML

Template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><Brand> — Quote card — <topic></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<families>&display=swap">
<style>
/* Embed tokens.css verbatim */
<contents of tokens.css>

html, body { margin: 0; padding: 0; background: #2a2a2a; min-height: 100vh; font-family: var(--type-display-family); }
body { display: flex; flex-direction: column; align-items: center; gap: 32px; padding: 32px 0; }

.canvas-label { font-family: var(--type-mono-family); font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,0.7); align-self: center; }

/* Square canvas — 1080×1080 */
.canvas-square {
  width: 1080px;
  height: 1080px;
  background: var(--color-surface);   /* or --color-ink for inversion */
  color: var(--color-ink);
  position: relative; overflow: hidden;
  padding: 96px;
  box-sizing: border-box;
  display: grid;
  /* Justify per layout choice — NOT centered by default */
  align-items: end;          /* bottom-anchored default; switch per variation */
}

/* The quote — Fraunces serif at scale */
.quote {
  font-family: var(--type-display-family);
  font-weight: 400;
  font-size: clamp(56px, 7.5vw, 88px);
  line-height: 1.08;
  letter-spacing: -0.018em;
  margin: 0;
  color: var(--color-ink);
  /* NO opening/closing quote glyph — typography is the quote, not the marks */
}
.quote .accent { color: var(--color-accent); }

/* Optional attribution — small, asymmetric, NOT centered */
.attribution {
  align-self: end;
  margin-top: 32px;
  font-family: var(--type-mono-family);
  font-size: 14px; letter-spacing: 0.06em;
  color: var(--color-ink-3);
}
.attribution::before { content: '— '; color: var(--color-ink-3); }

/* Story canvas — 1080×1920 */
.canvas-story {
  width: 1080px;
  height: 1920px;
  background: var(--color-surface);
  color: var(--color-ink);
  position: relative; overflow: hidden;
  padding: 270px 96px 240px;     /* IG Story chrome — top + bottom safe zones */
  box-sizing: border-box;
  display: grid;
  align-items: end;
}
.canvas-story .quote {
  font-size: clamp(72px, 8vw, 104px);
  line-height: 1.06;
}

/* Inverted variant — applies to either canvas */
.canvas--inverted {
  background: var(--color-ink);
  color: var(--color-surface);
}
.canvas--inverted .quote { color: var(--color-surface); }
.canvas--inverted .attribution { color: rgba(251, 250, 249, 0.55); }
.canvas--inverted .attribution::before { color: rgba(251, 250, 249, 0.55); }

@page { size: 1080px 1080px; margin: 0; }
</style>
</head>
<body>
<!--
Variation choices:
  archetype: <picked>
  layout:    <picked>
  color:     <picked>
-->

<span class="canvas-label">→ Square · 1080×1080 · screenshot for IG feed / LinkedIn</span>
<article class="canvas canvas-square">
  <p class="quote">[the quote, with optional <span class="accent">[one accent word]</span>]</p>
  <!-- optional attribution — omit if brand IS the speaker -->
</article>

<span class="canvas-label">→ Story · 1080×1920 · screenshot for IG Story / Reel cover</span>
<article class="canvas canvas-story">
  <p class="quote">[same quote, scaled up for vertical format]</p>
</article>

</body>
</html>
```

### 5. Verify

- [ ] Both canvases at exact dimensions (1080×1080 + 1080×1920)
- [ ] Quote is at most 25 words; ends in period per brand voice
- [ ] **No quotation mark glyphs around the quote** (❝ ❞ " " — banned as decorative)
- [ ] Layout is NOT center-anchored (unless the quote is a single short line and center is genuinely the right anchor)
- [ ] Architecture archetype documented AND differs from the most recent quote card for this brand
- [ ] **Read `../../design-anti-patterns.md` and verify the artifact violates none of its rules.** Pay special attention to sections 1 (no gradients behind text — text on solid surface only), 2 (no italics-emphasis OR single-word color emphasis as decoration), 4 (architecture must reach inner blocks), and 5 (no editorial-cosplay markers)
- [ ] Type-accent (if used) is on the SUBJECT word of the quote, not a generic adjective
- [ ] No attribution if the brand IS the speaker (avoid the "— Shane Logsdon" cliché on Shane's own quotes)
- [ ] Story canvas respects IG chrome (top 270px / bottom 240px reserved padding for app UI)

> Quote card at `./design/<brand-slug>/artifacts/quote-card-YYYY-MM-DD-<slug>.html`.
>
> Variation: `<archetype>` × `<layout>` × `<color>`.
>
> Export square: open in browser → DevTools → 1080×1080 viewport → screenshot the `.canvas-square` element.
> Export story: 1080×1920 viewport → screenshot `.canvas-story`.

## Anti-Slop Rules

Governed by three shared canonical references — read them, do not restate them:

- **`../../design-anti-patterns.md`** — the hard floor. Wins every conflict.
- **`../../design-principles.md`** — the craft floor (typographic hierarchy, spatial rhythm, color theory, layout logic, visual tension).
- **`../../design-variation-sop.md`** — the named-aesthetic roster + the procedure for varying every invocation.

**Forbidden (fast scan — the references hold the full list):**

- Indigo/violet/purple as default accent or primary — the `hsl(230–280)` family on a near-white surface. The single loudest AI tell.
- Purple→blue / "aurora" / gradient-mesh backgrounds; gradient-fill text.
- Glassmorphism without an explicit AA-contrast scrim; floating gradient "blobs" as atmosphere.
- The three-up icon-card feature grid; the "hero → 3 cards → CTA" median skeleton.
- One global border-radius on every element; timid evenly-weighted low-contrast palette.
- Inter / Roboto / Arial / Open Sans / Lato / Helvetica / system as the primary family (Space Grotesk = yellow flag). Use a category-matched stack from the variation roster.
- Value-free CTAs ("Get Started", "Learn More", "Sign Up"); the two-CTA hero. Name the real action and its value.

**Required variation (every invocation):**

- Make at least **two** intentional decisions that differ from the safe defaults (palette, layout structure, typographic voice, or spatial density) AND from the most recent artifact in this brand.
- Never default to "clean / minimal / modern" — that is the absence of a direction (variation-sop Rule 1).
- Sketch **three distinct directions**, offer them as a one-line menu, generate the best-fit by default, all three only if asked (variation-sop Rule 3).

**Authenticity:** prefer specific over generic everywhere — real datelines (not "today"), the brand's actual voice (not "build the future" filler), concrete CTAs over placeholders.

## Rules

- **No quotation mark glyphs.** The decorative ❝/❞ around a pull quote is the format's most-overused tell. Typography carries the weight; the glyphs add nothing.
- **No gradient backgrounds.** Quote on a solid surface — cream OR inverted ink. No purple-to-cyan, no anything-to-anything.
- **Centered layout requires justification.** Default to top-anchored, bottom-anchored, or off-grid. Centered is fine for one-line quotes where it's the right answer — never as a default reach.
- **Word count: 25 max.** Push back on the user if longer. Quote cards land at the speed of a single read.
- **Pixel exactness on both canvases.**
- **Token-pure.** Every visual value via `var(--*)` from tokens.css.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list.
