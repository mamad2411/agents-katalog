---
name: design-carousel-slide
description: Generate a LinkedIn / Instagram multi-slide carousel — single HTML file with N square 1080×1080 .canvas divs, each representing one slide. Default N=5 (cover + 3 content + closing CTA). Cover and closing always use the brand's most distinctive treatments; middle slides are content-led. Reads ./design/<brand-slug>/DESIGN.md, tokens.css, and components.html. Triggers include "carousel for X", "linkedin carousel", "instagram carousel", "carousel slides", "/carousel-slide".
---

# Skill: carousel-slide

Produces a single self-contained HTML file containing N pixel-exact 1080×1080 canvas divs. Each canvas is an individual carousel slide; screenshot each separately at native dimensions to upload as a multi-slide post on LinkedIn or Instagram.

The carousel format is high-leverage for editorial brands — it lets the brand's longer-form thinking land in a feed that otherwise rewards single posts. The discipline: cover and closing slides do the visual work; middle slides do the content work.

## When to use

- User wants a multi-slide carousel post (LinkedIn or Instagram)
- A `DESIGN.md` exists for the brand

## Inputs

- **Required:** brand slug, post topic / thesis
- **Optional:** number of slides (default 5: cover + 3 content + closing), CTA text for closing slide
- **Optional:** content for each middle slide (or leave for the agent to draft from the topic)

## Output

`./design/<brand-slug>/artifacts/carousel-YYYY-MM-DD-<slug>.html`

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

### 2. Gather the brief

Ask in one message:

```
1. Topic / thesis — the carousel's argument in one sentence (sentence-case ending in period per brand voice)
2. Number of slides — default 5 (1 cover + N content + 1 closing CTA); valid range 3–9 (carousel max)
3. Per-slide content — optional. If omitted, the agent drafts from the topic.
4. Closing CTA — the action you want readers to take (e.g. "read the full piece at shane.logsdon.io")
```

### 3. Pick variations — DIFFERENT archetypes for cover, content, closing

Carousel formats reward visual variation between cover and content. The discipline:

**Cover slide** (slide 1) — picks from the most distinctive archetypes:
- `single-word` — one massive Fraunces serif word
- `inverse-text` — full canvas dark inversion with the carousel's claim as the headline
- `number-led` — the topic's defining stat dominates the cover
- `type-only` — the topic statement at maximum scale, no chrome

**Content slides** (slides 2 through N-1) — picks from CONSISTENT archetypes (slides should feel like a series, not a deck of mismatched cards):
- `chrome-led` — running head + numbered headline + brief body
- `object-of-content` — looks like a fragment from the brand's actual writing
- `pattern-led` — typographic pattern with a punctum

**Closing slide** (slide N) — picks from action-oriented archetypes:
- `chrome-led` with explicit CTA
- `inverse-text` with the CTA as the carved headline
- `single-word` ("more.") with URL beneath

**Color treatment** must hold across all slides for series coherence: `cream-page` | `inverted-feature-on-cover` (cover dark, body cream, closing dark to bookend) | `full-cream`.

**Cross-artifact rule:** if a recent carousel for this brand used a particular cover archetype, vary it.

### 4. Generate the HTML

Template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><Brand> — Carousel — <topic></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<families>&display=swap">
<style>
/* Embed tokens.css verbatim */
<contents of tokens.css>

html, body { margin: 0; padding: 0; background: #2a2a2a; min-height: 100vh; font-family: var(--type-sans-family); }
body { display: flex; flex-direction: column; align-items: center; gap: 32px; padding: 32px 0; }

.slide-label { font-family: var(--type-mono-family); font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,0.7); align-self: center; }

/* All slides at exact 1080×1080 */
.canvas {
  width: 1080px; height: 1080px;
  background: var(--color-surface);
  color: var(--color-ink);
  position: relative; overflow: hidden;
  padding: 80px;
  box-sizing: border-box;
  display: grid;
}

/* Cover slide — strongest treatment */
.canvas--cover { /* style per cover archetype: single-word / inverse-text / etc. */ }

/* Content slide — consistent archetype across slides 2..N-1 */
.canvas--content {
  grid-template-rows: auto 1fr auto;
  gap: 32px;
}

/* Closing slide — action-oriented */
.canvas--closing { /* style per closing archetype */ }

/* Slide-position folio (same as page numbers in a magazine) */
.slide-folio {
  position: absolute; bottom: 64px; right: 64px;
  font-family: var(--type-mono-family); font-size: 14px; letter-spacing: 0.06em;
  color: var(--color-ink-3);
}
.slide-folio .pos { color: var(--color-ink); }

@page { size: 1080px 1080px; margin: 0; }
</style>
</head>
<body>
<!--
Variation choices:
  cover-archetype:   <picked>
  content-archetype: <picked>
  closing-archetype: <picked>
  color:             <picked>
-->

<span class="slide-label">→ Slide 1 / N · COVER · 1080×1080</span>
<article class="canvas canvas--cover">
  <!-- cover content per chosen archetype -->
  <span class="slide-folio"><span class="pos">01</span> / 05</span>
</article>

<span class="slide-label">→ Slide 2 / N · CONTENT</span>
<article class="canvas canvas--content">
  <!-- content slide -->
  <span class="slide-folio"><span class="pos">02</span> / 05</span>
</article>

<!-- ... repeat for content slides 3, 4 ... -->

<span class="slide-label">→ Slide N / N · CLOSING</span>
<article class="canvas canvas--closing">
  <!-- closing CTA per archetype -->
  <span class="slide-folio"><span class="pos">05</span> / 05</span>
</article>
</body>
</html>
```

### 5. Per-slide content guidance

- **Cover (slide 1)**: the carousel's claim or topic, set at maximum scale per chosen archetype. NO chrome (no eyebrow, no body text). The cover IS the hook.
- **Content slides (slides 2..N-1)**: each carries ONE point. Format: small running head + headline (24–48px) + brief body (1–3 sentences). Numbered ordinal in marginalia. Slides build on each other.
- **Closing (slide N)**: the action — read the full piece, subscribe, follow, etc. Either chrome-led with explicit CTA OR inverse-text with the CTA carved as the dominant element.

### 6. Verify

- [ ] All N canvases at exact 1080×1080
- [ ] Cover archetype documented AND distinct from content archetype
- [ ] Content slides consistent in archetype (so they read as a series)
- [ ] Closing slide has clear action / next step
- [ ] Slide folios (01/05, 02/05, etc.) on every slide for orientation
- [ ] **Read `../../design-anti-patterns.md` and verify the artifact violates none of its rules.** Pay special attention to sections 2 (no italics-emphasis OR single-word color emphasis), 4 (architecture must reach inner blocks; no top-metadata-row eyebrow disguise), 5 (no editorial-cosplay markers unless brand-earned), and 7 (cross-artifact rules)
- [ ] Type-accent (one word in `--color-accent`) appears AT MOST once across the whole carousel — typically on the cover or closing
- [ ] Companion text drafted (LinkedIn post or IG caption) accompanies the file in an HTML comment

> Carousel artifact at `./design/<brand-slug>/artifacts/carousel-YYYY-MM-DD-<slug>.html`.
>
> Variations: cover `<arch>` · content `<arch>` · closing `<arch>` · color `<picked>`.
>
> Export: open in browser → DevTools → device toolbar → 1080×1080 viewport → screenshot each `.canvas` separately. Upload as multi-slide post in LinkedIn or Instagram in slide-folio order.

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

- **Pixel exactness on every slide.** 1080×1080, no flex.
- **Cover and closing get the most distinctive treatments.** Middle slides serve content; bookends serve attention.
- **Slide folios mandatory.** Each slide gets its position marker (01/05, 02/05) — readers need orientation in carousel UIs.
- **Companion text included.** LinkedIn or IG caption drafted for the post body.
- **Token-pure.** Every visual value via `var(--*)` from tokens.css.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list.
