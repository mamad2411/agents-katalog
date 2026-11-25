---
name: design-blog-hero
description: |
  Generate a blog post hero artifact — TWO pixel-exact HTML canvases in a single file: an Open Graph card (1200×630) for social meta tags AND an in-page hero (1440×600) for the article header. Both canvases share the same content + brand tokens; only the proportions differ. Reads ./design/<brand-slug>/DESIGN.md, tokens.css, and components.html. Triggers include "blog hero for X", "OG card for X", "open graph image", "in-page hero", "/blog-hero".
---

# Skill: blog-hero

Produces a single self-contained HTML file containing TWO pixel-exact canvases:

1. **OG card** (1200×630) — Open Graph / Twitter card dimensions for social link unfurls
2. **In-page hero** (1440×600) — wide format for the article's header section on the site

The same headline + meta render in both canvases at appropriate proportions. Screenshot each canvas separately for its respective use.

## When to use

- Publishing a blog post / field note that needs both an OG meta image and a page header asset
- A `DESIGN.md` exists for the brand

## Inputs

- **Required:** brand slug, post title / hero headline (1 sentence, ending in period per brand voice)
- **Optional:** dek (1 supporting sentence), category label, dateline, optional type-accent word (one word in the headline to set in `--color-accent`)

## Output

`./design/<brand-slug>/artifacts/blog-hero-YYYY-MM-DD-<slug>.html` — single file, two canvases stacked vertically with a labeled header above each so it's clear which to screenshot for which use.

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

If missing, stop and tell the user to run `/design-system <brand-slug>` first.

### 2. Gather the brief

Ask in one message:

```
1. Hero headline — the post's title, sentence-case ending in period (max ~12 words for legibility at OG thumbnail size)
2. Optional dek — 1 supporting sentence (max ~18 words)
3. Category label — short string (e.g. "field notes", "strategic insights")
4. Dateline — YYYY.MM.DD
5. Optional type-accent word — one word from the headline to set in the brand's accent color
```

### 3. Pick variation — ARCHITECTURE FIRST

Pick ONE archetype that applies to BOTH canvases (consistency between OG and in-page hero is important for brand recognition):

- `chrome-led` — eyebrow + headline + dateline + category. Use cautiously — it's the AI-editorial default.
- `type-only` — headline only at maximum scale; nothing else. Strongest for short titles.
- `inverse-text` — body copy fills surface; headline carved out of the type wall.
- `object-of-content` — looks like a fragment of the actual article (excerpt, pull-quote pattern, transcript line).
- `pattern-led` — typographic pattern fills surface; headline is the punctum.

Then pick from:
- **Layout**: `symmetric | asymmetric | off-grid | full-bleed | split`
- **Color usage**: `monochrome | single-accent | inverted` (full dark inversion is the canonical v2 feature treatment for hero contexts)
- **Type pressure**: `display-dominant | mixed-weight | mono-led`

**Cross-artifact rule:** if a recent artifact for this brand used the same archetype, pick differently. Read `./design/<brand-slug>/artifacts/*.html` variation comments before deciding.

### 4. Generate the canvas HTML

Template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><Brand> — Blog hero — <topic></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<families from DESIGN.md>&display=swap">
<style>
/* Embed tokens.css verbatim */
<contents of tokens.css>

html, body { margin: 0; padding: 0; background: #2a2a2a; min-height: 100vh; font-family: var(--type-sans-family); }
body { display: flex; flex-direction: column; align-items: center; gap: 32px; padding: 32px 0; }

/* Section labels (above each canvas — for the screenshotter, NOT part of the artifact) */
.canvas-label {
  font-family: var(--type-mono-family);
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.7);
  align-self: center;
}

/* OG canvas — exact 1200×627 (LinkedIn/Twitter/Facebook OG spec) */
.canvas-og {
  width: 1200px;
  height: 630px;
  background: var(--color-surface);   /* or --color-ink for inversion */
  color: var(--color-ink);
  /* ... layout per variation ... */
}

/* In-page hero — wider format for article header */
.canvas-hero {
  width: 1440px;
  height: 600px;
  background: var(--color-surface);
  color: var(--color-ink);
  /* ... layout per variation ... */
}

@page { size: 1200px 630px; margin: 0; }   /* default page size for browser print export */
</style>
</head>
<body>
<!--
Variation choices:
  archetype:  <picked>
  layout:     <picked>
  color:      <picked>
  type-press: <picked>
-->

<span class="canvas-label">→ OG card · 1200×630 · screenshot this for og:image meta tag</span>
<article class="canvas canvas-og">
  <!-- hero content -->
</article>

<span class="canvas-label">→ In-page hero · 1440×600 · screenshot this for the article header</span>
<article class="canvas canvas-hero">
  <!-- same content, different proportions — vary headline scale and meta placement to suit -->
</article>
</body>
</html>
```

Adapt the inner content per archetype. For example:
- **`chrome-led`**: dateline + category at top, headline center, dek + author at bottom
- **`type-only`**: headline fills the canvas at max scale
- **`inverse-text`**: full canvas dark inversion (`background: var(--color-ink); color: var(--color-surface);`); headline in cream
- **`object-of-content`**: looks like a fragment of the article — excerpt, pull-quote, dateline strip mimicking the in-article layout

### 5. Verify and report

- [ ] Both canvases at exact dimensions (1200×630 + 1440×600)
- [ ] Architecture archetype documented AND differs from the most recent artifact in this brand
- [ ] **Read `../../design-anti-patterns.md` and verify the artifact violates none of its rules.** Pay special attention to sections 2 (no italics OR single-word color emphasis), 4 (architecture must reach inner blocks; vary footer; no top-metadata-row disguised as eyebrow), 5 (no editorial-cosplay markers unless brand-earned), and 7 (cross-artifact rules)
- [ ] Headline legible at OG thumbnail size (~600px wide on Twitter feed)
- [ ] Companion meta data (slug, OG description) noted at end of file

> Blog hero artifact at `./design/<brand-slug>/artifacts/blog-hero-YYYY-MM-DD-<slug>.html`.
>
> Variation: `<archetype>` × `<layout>` × `<color>` × `<type-press>`.
>
> Export OG: open in browser → DevTools → device toolbar → set viewport to 1200×630 → screenshot the `.canvas-og` element.
> Export in-page hero: same flow at 1440×600 on `.canvas-hero`.

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

- **Pixel exactness on both canvases.** No rounding, no responsive scaling beyond `clamp()` for headline overflow.
- **Token-pure.** Every visual value via `var(--*)` from tokens.css. The only literal pixel values allowed are `1px` for hairlines and the canvas pixel dimensions.
- **Both canvases share archetype + content.** They're variations on the same hero, not different concepts.
- **One file per artifact.** If the user wants alternate hero treatments, make multiple files.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list. If you find a new tell in the output, add it there.
