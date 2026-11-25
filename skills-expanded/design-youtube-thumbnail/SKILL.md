---
name: design-youtube-thumbnail
description: Generate a YouTube thumbnail artifact — a 1280×720 HTML canvas optimized for legibility at small sizes (mobile feed, sidebar suggestions, search results). Reads ./design/<brand-slug>/DESIGN.md, tokens.css, and components.html. Triggers include "youtube thumbnail for X", "thumbnail for [video title]", "yt thumb", "/youtube-thumbnail".
---

# Skill: youtube-thumbnail

Produces a pixel-exact 1280×720 HTML canvas. The defining constraint: it must read clearly at 240×135px (typical mobile feed thumbnail) — not just at full size. Bias toward fewer words, larger type, higher contrast than other platform skills.

## When to use

- User has (or is about to publish) a YouTube video and wants a thumbnail asset
- A `DESIGN.md` exists for the brand

## Inputs

- **Required:** brand slug, video title (the ACTUAL video title, not the on-thumbnail text)
- **Required:** thumbnail text — the 2–4 words that go ON the image (this is NOT the video title; it's the visual hook)
- **Optional:** episode/series number, supporting micro-text (max 6 words)

## Output

`./design/<brand-slug>/artifacts/youtube-YYYY-MM-DD-<slug>.html`

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

### 2. Gather the brief

Ask in one message:

```
1. Video title (full title that goes in YouTube's title field)
2. Thumbnail text — 2–4 words MAX that appear ON the image. This is your visual hook, not your title.
   Examples: "Built it wrong" / "Faster than you'd think" / "Why I quit Vim" / "Day 47"
3. Optional episode/series marker (e.g. "EP. 12" or "PART 3 / 5")
4. Optional supporting micro-text under the hook (max 6 words)
```

If the user gives you 8+ words for thumbnail text, push back: "That's too many for legibility at mobile size. Pick the 3–4 words that carry the hook." Don't proceed until they agree.

### 3. Pick variation — ARCHITECTURE FIRST

Pick ONE archetype before any other axis. YouTube thumbnails have specific archetypes that work at small sizes; pick from these.

- **Architecture archetype** (pick FIRST):
  - `text-only` — the hook is the entire artifact. No marker, no mark, no rules. Default for maximum legibility.
  - `single-word` — one massive word fills 70%+ of canvas; everything else absent.
  - `number-led` — a number/stat dominates (e.g. "47", "0.3s", "$11M"); hook becomes caption.
  - `object-of-content` — looks like a screenshot/quote from the video itself (transcript line, terminal output, code fragment).
  - `pattern-led` — repetition or grid fills canvas; one element breaks it.
  - `chrome-led` — marker + hook + corner mark. **Last resort.** Use only if the brand requires consistent chrome AND no other archetype suits.

After archetype, pick from these YouTube-specific axes:
- **Layout**: `centered-bold | left-anchored | split-diagonal | corner-stamp | full-text-takeover`
- **Type pressure**: `monolithic-display` (one huge word) | `stacked-words` (words on own lines) | `display-with-mono-caption`
- **Color usage**: `single-accent-block` | `inverted-canvas` | `monochrome` | `duotone-split`

Avoid: faces, arrows pointing at things, red circles around things, "MIND BLOWN" energy. Type-led restraint is the differentiator.

**Cross-artifact rule:** different archetype than the brand's most recent artifact (check `./design/<brand-slug>/artifacts/`).

### 4. Generate the canvas HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><Brand> — YouTube — <video title></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<families>&display=swap">
<style>
/* Embed tokens.css verbatim */
<contents of tokens.css>

html, body { margin: 0; padding: 0; background: #2a2a2a; min-height: 100vh; display: grid; place-items: center; font-family: var(--type-body-md-family); }

.canvas {
  width: 1280px;
  height: 720px;
  background: var(--color-surface);
  color: var(--color-ink);
  position: relative;
  overflow: hidden;
  padding: var(--space-2xl);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  /* Justification per layout choice */
}

/* The hook text — MUST be massive. Use clamp() with high min/max */
.hook {
  font-family: var(--type-display-xl-family);
  font-weight: 700; /* even if display-xl is 600, push to 700 here for thumbnail weight */
  letter-spacing: -0.025em;
  line-height: 0.95;
  margin: 0;
  font-size: clamp(140px, 15vw, 220px);
}

/* Stacked variant: each word on its own line */
.hook--stacked .word { display: block; }

/* Episode marker */
.marker {
  font: var(--type-label-caps-weight) var(--type-label-caps-size)/var(--type-label-caps-leading) var(--type-label-caps-family);
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--color-ink-soft);
  font-size: 18px;
}

/* Brand mark in corner — small, never dominates */
.mark {
  position: absolute;
  bottom: var(--space-xl);
  right: var(--space-xl);
  font: var(--type-label-caps-weight) var(--type-label-caps-size)/var(--type-label-caps-leading) var(--type-label-caps-family);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-ink-soft);
}

/* Inverted canvas variant */
.canvas--inverted { background: var(--color-ink); color: var(--color-surface); }
.canvas--inverted .marker, .canvas--inverted .mark { color: var(--color-surface); opacity: 0.7; }

/* Single-accent-block variant — one colored region */
.canvas--accent::before {
  content: "";
  position: absolute;
  background: var(--color-accent);
  /* Position varies by layout — e.g. left third, top quarter, diagonal */
  width: 30%; height: 100%;
  top: 0; left: 0;
  z-index: 0;
}
.canvas--accent > * { position: relative; z-index: 1; }

@page { size: 1280px 720px; margin: 0; }
</style>
</head>
<body>
<!--
Variation choices:
  layout: <picked>
  type-pressure: <picked>
  color: <picked>
  composition: <picked>

Video title (for YouTube field, NOT on canvas): "<title>"
Thumbnail text (on canvas): "<hook>"
-->
<article class="canvas <modifier classes>">
  <span class="marker"><episode marker, e.g. "EP. 12 — TITLE"></span>
  <h1 class="hook"><hook text — split into words for stacked variant></h1>
  <span class="mark"><Brand mark></span>
</article>
</body>
</html>
```

### 5. Test legibility (mental check)

Imagine the canvas scaled to 240×135px (a YouTube mobile feed thumbnail). At that size:
- Can you read the hook text in under 1 second?
- Is the contrast strong enough to pop against a busy feed?
- Does the brand mark survive (or is it OK if it disappears at small size)?

If "no" to the first two, the hook is too small or contrast too low. Bump font-size up or switch to inverted canvas.

### 6. Verify and report

- [ ] Canvas is exactly 1280×720
- [ ] Architecture archetype documented AND differs from the most recent artifact in this brand
- [ ] **Read `../../design-anti-patterns.md` and verify the artifact violates none of its rules.** Pay special attention to sections 2 (type emphasis), 4 (no top-metadata-row disguised as eyebrow; vary mark placement), 5 (no `EP. 01` cosplay), and 8 (no animations).
- [ ] Hook text is at minimum 140px (typical: 160–280px); no more than 4 words in the hook
- [ ] No face, no arrow, no red circle, no thumbnail-clickbait clichés (YouTube-specific)
- [ ] Brand mark, if present, is unobtrusive (corner, eyebrow style, opacity ~0.7) — or absent entirely

> YouTube thumbnail at `./design/<brand-slug>/artifacts/youtube-YYYY-MM-DD-<slug>.html`.
>
> Variation: `<layout>` × `<type-pressure>` × `<color>` × `<composition>`.
>
> Export as PNG at exact 1280×720: open in browser → DevTools → device toolbar → 1280×720 → screenshot.
>
> Quick legibility check: zoom out in your browser to 20% — if the hook still reads instantly, you're good.

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

- **Hook word count is hard-capped at 4.** Push back on the user if they want more. The whole skill is built around small-size legibility.
- **No clickbait clichés** (YouTube-specific). No faces, no arrows pointing at things, no red circles, no "MIND BLOWN" energy. Type-led restraint is the brand differentiator.
- **Pixel exact.** 1280×720, no flex.
- **Token-pure.** Every value via `var(--*)` except `1px` borders and the canvas pixel dimensions.
- **Brand mark stays small or absent.** If present, max 18px font-size, corner placement.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list. If you find a new tell in the output, add it there.
