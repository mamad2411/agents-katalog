---
name: design-instagram-post
description: Generate an Instagram post artifact — pixel-exact HTML canvas at 1080×1350 (portrait, default — Instagram's max-real-estate format) with opt-in 1080×1080 (square) and 1080×1920 (story / reel cover) modes. Reads ./design/<brand-slug>/DESIGN.md, tokens.css, and components.html. Triggers include "instagram post about X", "ig post", "ig story", "instagram artifact", "/instagram-post".
---

# Skill: instagram-post

Produces a pixel-exact HTML canvas for Instagram. Three canvas modes:

- **`portrait`** (default, 1080×1350) — feed post in 4:5 ratio, the maximum vertical real estate Instagram allows
- **`square`** (1080×1080) — classic feed square, useful for grid coherence
- **`story`** (1080×1920) — vertical 9:16 for Stories and Reels covers

Plus an optional caption suggestion (2200-char limit; first 125 chars visible before "more").

## When to use

- User wants a visual asset for Instagram (feed post, carousel cover, story, reel cover)
- A `DESIGN.md` exists for the brand

## Inputs

- **Required:** brand slug, post topic / title (1 line)
- **Optional:** mode (`portrait` | `square` | `story`, default `portrait`), supporting line, attribution, caption style, hashtag set

## Output

`./design/<brand-slug>/artifacts/instagram-<mode>-YYYY-MM-DD-<slug>.html`

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

### 2. Pick mode

Default `portrait` (1080×1350) — gets the most feed space and converts best.
Use `square` if user explicitly asks for grid coherence with existing square posts.
Use `story` for Stories or Reel covers.

### 3. Gather the brief

Ask in one message:

```
1. Headline — the dominant text on the canvas (max 8 words for portrait/square, max 6 for story)
2. Optional supporting line (max 12 words)
3. Attribution — name + handle, or leave blank
4. Caption style: insight | story | announcement | carousel-intro | reel-cover | none
5. Hashtag set: any specific tags, or leave blank for none
```

### 4. Pick variation — ARCHITECTURE FIRST

Pick ONE archetype before any other axis. Portrait dimensions invite vertical type stacking and number-led layouts that horizontal formats don't — use them.

- **Architecture archetype** (pick FIRST):
  - `chrome-led` — eyebrow + headline + footer band. **Last resort.** AI-editorial default.
  - `type-only` — pure type, no chrome.
  - `number-led` — one oversized number dominates; rest is short caption. Portrait format suits this beautifully.
  - `object-of-content` — looks like the thing being communicated (a list, a transcript fragment, a printed page, a journal entry).
  - `pattern-led` — typographic repetition or grid fills canvas; one element breaks it.
  - `inverse-text` — headline carved from a block of body copy; or massive headline with body wrapping negative space.
  - `vertical-stack` — words stacked one per line in display weight, leveraging portrait height. Each line is its own statement.

After archetype, pick from:
- **Layout**: `centered-poster | top-anchored | bottom-anchored | split-vertical | corner-stamp`
- **Type pressure**: `display-dominant | mixed-weight | mono-led`
- **Color usage**: `monochrome | single-accent-block | inverted | duotone-split-vertical`
- **Composition focus**: `headline-led | quote-led | data-led | mark-led`

**Cross-artifact rule:** different archetype than the most recent artifact in this brand. Read variation comments in `./design/<brand-slug>/artifacts/`.

### 5. Crop safety (Instagram-specific)

Instagram crops portrait posts to a square in the explore feed and to ~1:1 thumbnails on profile grids. Keep critical content (headline + brand mark) within the **center 1080×1080 of a portrait canvas**, with safe margins of `var(--space-2xl)` from the top and bottom edges. The top/bottom 135px regions can carry secondary content (eyebrow, footer) but should remain readable when cropped out.

For Story mode (1080×1920), Instagram's interface chrome covers the top 250px and bottom 220px. Keep critical content within `y: 250–1700`.

### 6. Generate the canvas HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><Brand> — Instagram <mode> — <topic></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<families>&display=swap">
<style>
/* Embed tokens.css verbatim */
<contents of tokens.css>

html, body { margin: 0; padding: 0; background: #2a2a2a; min-height: 100vh; display: grid; place-items: center; font-family: var(--type-body-md-family); }

.canvas {
  /* Per mode:
     portrait: 1080x1350
     square:   1080x1080
     story:    1080x1920 */
  width: 1080px;
  height: <1350 | 1080 | 1920>px;
  background: var(--color-surface);
  color: var(--color-ink);
  position: relative;
  overflow: hidden;
  padding: var(--space-3xl);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

/* Story mode — content respects IG's interface chrome */
.canvas--story {
  padding: 270px var(--space-3xl) 240px;
}

/* Portrait/square — the safe-crop center ring (visual aid for design, removed in export) */
.canvas--portrait::after {
  /* Uncomment during design to visualize crop safety
  content: ""; position: absolute; left: 0; right: 0; top: 135px; bottom: 135px;
  border: 1px dashed var(--color-rule);
  pointer-events: none;
  */
}

.eyebrow {
  font: var(--type-label-caps-weight) var(--type-label-caps-size)/var(--type-label-caps-leading) var(--type-label-caps-family);
  letter-spacing: var(--type-label-caps-tracking);
  text-transform: uppercase;
  color: var(--color-ink-soft);
}

.headline {
  font-family: var(--type-display-xl-family);
  font-weight: var(--type-display-xl-weight);
  letter-spacing: var(--type-display-xl-tracking);
  font-size: clamp(72px, 9vw, 132px);
  line-height: 1.04;
  margin: var(--space-md) 0 0;
}

.support {
  font-family: var(--type-body-lg-family);
  font-size: var(--type-body-lg-size);
  font-size: clamp(20px, 2.4vw, 32px);
  line-height: 1.45;
  color: var(--color-ink-soft);
  max-width: 80%;
  margin: var(--space-lg) 0 0;
}

.footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-top: 1px solid var(--color-rule);
  padding-top: var(--space-md);
  font: var(--type-label-caps-weight) var(--type-label-caps-size)/var(--type-label-caps-leading) var(--type-label-caps-family);
  letter-spacing: var(--type-label-caps-tracking);
  text-transform: uppercase;
  color: var(--color-ink-soft);
}

@page { size: 1080px <height>px; margin: 0; }
</style>
</head>
<body>
<!--
Mode: <portrait | square | story>
Variation choices:
  layout: <picked>
  type-pressure: <picked>
  color: <picked>
  composition: <picked>
-->
<article class="canvas canvas--<mode>">
  <header>
    <span class="eyebrow"><eyebrow text></span>
    <h1 class="headline"><headline></h1>
    <!-- optional supporting line -->
  </header>
  <footer class="footer">
    <span><Brand mark or @handle></span>
    <span><YYYY.MM.DD></span>
    <span><optional CTA or topic tag></span>
  </footer>
</article>
</body>
</html>
```

### 7. Generate caption suggestion

Instagram caption rules:
- 2200 char limit total
- First ~125 chars visible before "more" — front-load the value
- Hashtags work better in first comment than in caption itself (cleaner aesthetic)
- Style by user choice:
  - **insight**: claim → reasoning → question to invite comments
  - **story**: scene → tension → takeaway
  - **announcement**: what's new → why it matters → where to find it
  - **carousel-intro**: hook + "(swipe →)" pointing to subsequent slides
  - **reel-cover**: 1-line hook for the cover frame; full caption goes elsewhere

Append in HTML comment:
```html
<!--
CAPTION (<count>/2200 chars):

<line 1 hook>

<paragraph 2>

<paragraph 3>

<final line — invitation or question>

[Hashtags in first comment, not caption — cleaner look:]
<hashtag set>
-->
```

### 8. Verify and report

- [ ] Canvas matches exact mode dimensions
- [ ] Architecture archetype documented AND differs from the most recent artifact in this brand
- [ ] **Read `../../design-anti-patterns.md` and verify the artifact violates none of its rules.** Pay special attention to sections 2 (no italics-emphasis OR single-word color emphasis), 4 (architecture must reach inner blocks; vary footer treatment; no top-metadata-row disguised as eyebrow), 5 (no editorial-cosplay markers), and 7 (cross-artifact rules)
- [ ] Critical content within crop-safe zone for chosen mode (Instagram-specific)
- [ ] No emojis unless `DESIGN-PLAN.md` allows them (Instagram is emoji-heavy by default; if the brand stance is "no emojis", hold the line)

> Instagram artifact (`<mode>` mode) at `./design/<brand-slug>/artifacts/instagram-<mode>-YYYY-MM-DD-<slug>.html`.
>
> Variation: `<layout>` × `<type-pressure>` × `<color>` × `<composition>`.
>
> Export as PNG: open in browser → DevTools → device toolbar → 1080×<height> → screenshot. Or `Cmd+P` → save as PDF.
>
> Caption suggestion is in an HTML comment at the end of the file.

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

- **Pixel exactness.** No rounding.
- **Crop safety.** Critical content stays inside the safe-crop region for the chosen mode. The safe-crop guide is commented out in the template — uncomment during design, recomment before export.
- **Token-pure.** Every visual value via `var(--*)`.
- **Story mode respects IG chrome.** Top 270px / bottom 240px reserved padding.
- **Caption first comment, not in body.** Hashtags belong in the first comment for cleaner caption aesthetics.
- **Default mode is portrait.** Don't quietly downgrade to square unless the user asks for it.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list. If you find a new tell in the output, add it there.
