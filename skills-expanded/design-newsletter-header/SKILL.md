---
name: design-newsletter-header
description: Generate a newsletter email header banner — pixel-exact 600×200 HTML canvas (the standard email-client safe-zone width). Self-contained, INLINE styles only (no external <style> blocks beyond <head>) for email-client compat. Intended to be screenshot to PNG and embedded as <img> in email — the rendered image is what readers see, regardless of their email client. Reads ./design/<brand-slug>/DESIGN.md and tokens.css. Triggers include "newsletter header", "email header for X", "email banner", "/newsletter-header".
---

# Skill: newsletter-header

Produces a 600×200 pixel-exact HTML canvas for use as a newsletter email header. The canvas is small — typography choices must be ruthless. Display sizes top out around 36–48px; meta around 11–14px. The artifact is meant to be screenshot to PNG and embedded as `<img>` in the email — the email client never sees raw HTML, so font and CSS quirks don't matter for delivery.

## When to use

- User publishes a newsletter and needs a branded header banner image
- A `DESIGN.md` exists for the brand

## Inputs

- **Required:** brand slug, newsletter title or issue identifier (e.g. "Working notes — May 2026")
- **Optional:** issue number, dateline, tagline (max 6 words)

## Output

`./design/<brand-slug>/artifacts/newsletter-header-YYYY-MM-DD-<slug>.html`

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

If missing, stop and tell the user to run `/design-system <brand-slug>` first.

### 2. Gather the brief

Ask in one message:

```
1. Header text — the masthead string (max 6 words)
2. Optional issue number / dateline (e.g. "Issue 003 · 2026.05.02")
3. Optional tagline / subtitle (max 6 words)
```

If the user gives 8+ words, push back: "600×200 won't hold that legibly. Cut to the masthead + meta." Don't proceed until they agree.

### 3. Pick variation — ARCHITECTURE FIRST

Pick ONE. Newsletter headers favor restraint — pick the simplest archetype that carries the brand register:

- `chrome-led` — masthead title + meta strip (issue / date). The classic newsletter header pattern; brand-earned for editorial titles.
- `type-only` — title alone at maximum scale; no meta at all.
- `inverse-text` — full canvas dark inversion (canonical v2 feature treatment) — masthead in cream on ink.
- `object-of-content` — looks like a printed masthead from a magazine/quarterly cover.

Then pick:
- **Layout**: `symmetric | asymmetric | full-bleed | split`
- **Color usage**: `monochrome | single-accent | inverted`

**Cross-artifact rule:** vary from the brand's most recent header (issue 002 vs issue 003 should not be visually identical).

### 4. Generate the canvas HTML

Template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><Brand> — Newsletter header — <issue></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<families>&display=swap">
<style>
/* Inline tokens (no external CSS — though Google Fonts <link> is allowed since it's a font, not CSS) */
<minimal subset of tokens.css needed for this artifact>

html, body { margin: 0; padding: 0; background: #2a2a2a; min-height: 100vh; display: grid; place-items: center; font-family: var(--type-sans-family); }

.canvas {
  width: 600px;
  height: 200px;
  background: var(--color-surface);   /* or --color-ink for inversion */
  color: var(--color-ink);
  position: relative;
  overflow: hidden;
  padding: 24px 32px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  /* Layout per variation */
}

@page { size: 600px 200px; margin: 0; }
</style>
</head>
<body>
<!--
Variation choices:
  archetype: <picked>
  layout:    <picked>
  color:     <picked>
-->
<article class="canvas">
  <!-- masthead content per archetype -->
</article>
</body>
</html>
```

For the masthead itself:
- **`chrome-led`**: small mono dateline at top, masthead in display serif (~36-44px), tagline in small caps below
- **`type-only`**: the masthead title alone, scaled to fill the canvas (clamp 44-72px depending on word count)
- **`inverse-text`**: full canvas dark; same masthead pattern but inverted text colors

### 5. Verify and report

- [ ] Canvas is exactly 600×200px
- [ ] Architecture archetype documented AND differs from the most recent artifact in this brand
- [ ] **Read `../../design-anti-patterns.md` and verify the artifact violates none of its rules.** Pay special attention to sections 2 (type emphasis) and 5 (no editorial-cosplay markers unless brand-earned)
- [ ] Header text is at most 6 words; tagline is at most 6 words
- [ ] Display type doesn't exceed ~48px (smaller canvas, smaller scale ceiling)

> Newsletter header at `./design/<brand-slug>/artifacts/newsletter-header-YYYY-MM-DD-<slug>.html`.
>
> Variation: `<archetype>` × `<layout>` × `<color>`.
>
> Export PNG: open in browser → DevTools → set viewport to 600×200 → screenshot the `.canvas` element. Embed the PNG as `<img>` in your email at full resolution (the email client renders the image directly, no font/CSS dependencies).

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

- **Pixel exactness.** Canvas is 600×200 — the email-safe width. No rounding.
- **Display scale ceiling.** ~48px max. The canvas is small; oversized type breaks the proportions.
- **Word count discipline.** 6 words max for the masthead, 6 max for the tagline. Push back on the user if they exceed it.
- **Token-pure.** Every visual value via `var(--*)` from the embedded tokens. Only literal pixel values allowed: `1px` for hairlines and the canvas dimensions.
- **One masthead per file.** If the user wants alternates, make multiple files.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list. If you find a new tell in the output, add it there.
