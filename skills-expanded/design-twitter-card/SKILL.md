---
name: design-twitter-card
description: Generate a Twitter/X card artifact — pixel-exact HTML canvas at 1600×900 (in-feed image) by default, with 1200×630 (Open Graph link card) opt-in. Reads ./design/<brand-slug>/DESIGN.md, tokens.css, and components.html. Triggers include "twitter card for X", "x card for X", "twitter post about X", "OG card", "/twitter-card", "/x-card".
---

# Skill: twitter-card

Produces a pixel-exact HTML canvas for Twitter/X. Two canvas modes:

- **`feed`** (default, 1600×900) — in-timeline post image at the recommended max-quality 16:9 ratio
- **`og`** (1200×630) — Open Graph link card for shared URLs from your site

Plus an optional companion tweet (280-char limit) or thread starter.

## When to use

- User wants a visual asset for a tweet, an X thread cover, or an Open Graph card on their site
- A `DESIGN.md` exists for the brand

## Inputs

- **Required:** brand slug, post headline / title (1 line)
- **Optional:** mode (`feed` | `og`, default `feed`), supporting line, attribution, companion tweet style

## Output

`./design/<brand-slug>/artifacts/twitter-<mode>-YYYY-MM-DD-<slug>.html`

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

If missing, stop and instruct the user to build the design system first.

### 2. Pick the canvas mode

If user said "OG card" or "link card", use `og` (1200×630).
Otherwise default to `feed` (1600×900) — sharper, larger, displays better in-timeline.

### 3. Gather the brief

Ask in one message:

```
1. Headline — the dominant text on the canvas (max 10 words for feed mode, max 6 for OG)
2. Optional supporting line
3. Attribution — name + role, or leave blank
4. Companion tweet style: claim | thread-starter | quote | question | none
```

### 4. Pick variation — ARCHITECTURE FIRST

Pick ONE architecture archetype before any other axis. The single biggest cause of AI-editorial output is reaching for `chrome-led` by default.

- **Architecture archetype** (pick FIRST):
  - `chrome-led` — eyebrow + headline + footer band. **Last resort.** AI-editorial default; structural sameness across artifacts.
  - `type-only` — type only, no chrome.
  - `number-led` — single oversized number/stat dominates the canvas; rest is caption.
  - `object-of-content` — the artifact IS the thing being said (transcript, list, fake printed page, receipt).
  - `pattern-led` — typographic repetition fills the canvas; one element breaks the pattern.
  - `inverse-text` — text becomes surface (carved-out headline, body wrapping negative space).

After archetype, pick ONE per axis:
- **Layout**: `symmetric | asymmetric | off-grid | full-bleed | split`
- **Type pressure**: `display-dominant | body-dominant | mono-led | mixed-weight`
- **Color usage**: `monochrome | single-accent | duotone | inverted`
- **Composition focus**: `headline-led | quote-led | mark-led | data-led`

**Cross-artifact rule:** read variation comments in the most recent 2–3 artifacts under `./design/<brand-slug>/artifacts/`. Different archetype than recent. Different axis combos.

### 5. Generate the canvas HTML

Template (swap dimensions based on mode):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><Brand> — Twitter — <topic></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<families>&display=swap">
<style>
/* Embed tokens.css verbatim */
<contents of tokens.css>

html, body { margin: 0; padding: 0; background: #2a2a2a; min-height: 100vh; display: grid; place-items: center; font-family: var(--type-body-md-family); }

/* Canvas — switch dimensions by mode */
.canvas {
  /* feed mode: 1600x900   |   og mode: 1200x630 */
  width: <1600 | 1200>px;
  height: <900 | 630>px;
  background: var(--color-surface);
  color: var(--color-ink);
  position: relative;
  overflow: hidden;
  padding: var(--space-3xl);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: <by variation>;
}

.eyebrow {
  font: var(--type-label-caps-weight) var(--type-label-caps-size)/var(--type-label-caps-leading) var(--type-label-caps-family);
  letter-spacing: var(--type-label-caps-tracking);
  text-transform: uppercase;
  color: var(--color-ink-soft);
}

.headline {
  font: var(--type-display-xl-weight) var(--type-display-xl-size)/var(--type-display-xl-leading) var(--type-display-xl-family);
  letter-spacing: var(--type-display-xl-tracking);
  margin: var(--space-md) 0 0;
  /* feed mode allows larger; OG mode caps lower for safety */
  font-size: clamp(48px, 6vw, 96px);
}

.footer {
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

@page { size: <1600 | 1200>px <900 | 630>px; margin: 0; }
</style>
</head>
<body>
<!--
Mode: <feed | og>
Variation choices:
  layout: <picked>
  type-pressure: <picked>
  color: <picked>
  composition: <picked>
-->
<article class="canvas">
  <header>
    <span class="eyebrow"><eyebrow text></span>
    <h1 class="headline"><headline></h1>
  </header>
  <footer class="footer">
    <span><Brand mark or @handle></span>
    <span><YYYY.MM.DD></span>
    <span><optional URL or topic tag></span>
  </footer>
</article>
</body>
</html>
```

Layout adaptations (same options as `linkedin-post`):
- **off-grid**: anchor headline at the optical center (slightly above geometric center), shift left ~12% of canvas width
- **split**: divide vertically into two unequal panels (e.g. 60/40), headline in larger, supporting in smaller
- **full-bleed**: extend background color or single-accent block beyond default padding to canvas edge on one side
- **mark-led**: oversized typographic brand mark dominates upper region, headline reads as caption beneath

### 6. Generate companion tweet

Twitter/X rules:
- 280 character limit (count carefully; URL counts as 23)
- First 70 chars are the preview when quote-tweeted — front-load the claim
- Style by user choice:
  - **claim**: declarative single-line punchline
  - **thread-starter**: hook + "🧵 below" or "(1/X)" — but since no emojis by default, use "→" or numbering
  - **quote**: pull quote from the artifact + attribution
  - **question**: provocative ask + context

Append in an HTML comment at end of file:
```html
<!--
COMPANION TWEET (<count>/280 chars):

<tweet text>

(Optional thread continuation in additional posts.)
-->
```

### 7. Verify and report

- [ ] Canvas is exactly the chosen mode's pixel dimensions
- [ ] Architecture archetype documented AND differs from the most recent artifact in this brand
- [ ] **Read `../../design-anti-patterns.md` and verify the artifact violates none of its rules.** Pay special attention to sections 2 (no italics-emphasis OR single-word color emphasis), 4 (architecture must reach inner blocks; vary footer; no top-metadata-row disguised as eyebrow), 5 (no editorial-cosplay markers), and 7 (cross-artifact rules)
- [ ] Headline legible at preview thumbnail (~500px) for feed; ~400px for OG
- [ ] Companion tweet under 280 chars

> Twitter artifact (`<mode>` mode) at `./design/<brand-slug>/artifacts/twitter-<mode>-YYYY-MM-DD-<slug>.html`.
>
> Variation: `<layout>` × `<type-pressure>` × `<color>` × `<composition>`.
>
> Export as PNG: open in browser, DevTools → device toolbar → match canvas dims → screenshot. Or `Cmd+P` → save as PDF.
>
> Companion tweet at the end of the file in an HTML comment.

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

- **Pixel exactness.** No rounding, no scaling.
- **Token-pure.** No literal hex codes or font sizes outside `clamp()` calls.
- **No center-aligned safe layout** unless the brand's plan explicitly calls for symmetry.
- **Mode default is `feed`** (1600×900), not OG. Most users want in-timeline posts.
- **Aliases**: this skill answers to both `twitter-card` and `x-card`. Trigger phrases work either way.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list. If you find a new tell in the output, add it there.
