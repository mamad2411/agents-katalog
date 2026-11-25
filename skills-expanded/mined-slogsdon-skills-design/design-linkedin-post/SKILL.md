---
name: design-linkedin-post
description: Generate a LinkedIn post artifact — a 1200×627 image canvas (LinkedIn's recommended share image dimension) plus a companion text suggestion (1300-char limit, hook-first structure). Reads ./design/<brand-slug>/DESIGN.md, tokens.css, and components.html. Triggers include "linkedin post about X", "linkedin artifact", "generate a linkedin image", "/linkedin-post".
---

# Skill: linkedin-post

Produces a pixel-exact 1200×627 HTML canvas suitable for screenshotting and uploading to LinkedIn as a post image, plus a markdown block with the recommended companion text. Reads from a brand's `DESIGN.md` system — never hardcodes brand values.

## When to use

- User wants a visual asset for a LinkedIn post (announcement, milestone, opinion piece, takeaway from a project)
- A `DESIGN.md` exists for the brand. If it doesn't, stop and tell the user to run `/design-plan` → `/design-system` first.

## Inputs

- **Required:** brand slug, post topic / headline (1 line)
- **Optional:** key claim or supporting line, CTA text, attribution (author name + role), variation hints

## Output

`./design/<brand-slug>/artifacts/linkedin-YYYY-MM-DD-<topic-slug>.html`

## Steps

### 1. Verify brand exists

```bash
test -f ./design/<brand-slug>/tokens.css
```

If missing, stop and instruct the user to build the design system first.

### 2. Gather the brief

Ask in one message:

```
1. Headline — the single sentence on the image (max 8 words for legibility at feed scale)
2. Optional supporting line (max 14 words)
3. Optional CTA text (e.g. "Read more →") — leave blank to omit
4. Attribution — your name + role, or leave blank for a clean unsigned look
5. Companion text style: insight | story | announcement | question
```

### 3. Pick variation — ARCHITECTURE FIRST

Before anything else, pick ONE architecture archetype. This is the structural skeleton; everything else is decoration. The single biggest cause of AI-editorial output is reaching for `chrome-led` by default.

- **Architecture archetype** (most-important choice — pick FIRST):
  - `chrome-led` — eyebrow + headline + signature-row footer. **Treat as the LAST resort.** This is the AI-editorial default; using it more than once per brand creates structural sameness.
  - `type-only` — nothing but the type. No eyebrow, no footer, no rules. The headline IS the artifact.
  - `number-led` — one oversized number/stat dominates ~60%+ of canvas; the rest is short caption. Everything bows to the figure.
  - `object-of-content` — the artifact IS the thing being communicated. Looks like a fragment of the product (a transcript, a printed page, a list of entries, a receipt). The "post" frame disappears.
  - `pattern-led` — typographic pattern or repetition fills the canvas; one element breaks the pattern as the punctum.
  - `inverse-text` — text becomes surface. Massive headline with body text wrapping the negative space; or a block of body type with the headline carved out as a void.

After the archetype, pick ONE from each remaining axis:
- **Layout**: `symmetric | asymmetric | off-grid | full-bleed | split`
- **Type pressure**: `display-dominant | body-dominant | mono-led | mixed-weight`
- **Color usage**: `monochrome | single-accent | duotone | inverted` (inverted = surface-as-ink)
- **Composition focus**: `headline-led | quote-led | mark-led | data-led`

**Cross-artifact rule (mandatory):** before picking, list `./design/<brand-slug>/artifacts/` and read the variation comments of the most recent 2–3 artifacts. If your archetype matches any recent one, pick a DIFFERENT archetype. Same with secondary axes — don't repeat combos within a brand.

### 4. Generate the canvas HTML

Template (canvas dimensions are NOT negotiable — exact 1200×627):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><Brand> — LinkedIn — <topic></title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<families from DESIGN.md>&display=swap">
<style>
/* Embed tokens.css verbatim */
<contents of tokens.css>

/* Page-level — center the canvas in the viewport for preview */
html, body { margin: 0; padding: 0; background: #2a2a2a; min-height: 100vh; display: grid; place-items: center; font-family: var(--type-body-md-family); }

/* THE CANVAS — exact LinkedIn dimensions */
.canvas {
  width: 1200px;
  height: 627px;
  background: var(--color-surface);
  color: var(--color-ink);
  position: relative;
  overflow: hidden;
  /* Set padding using a token, NOT a magic number */
  padding: var(--space-3xl);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  /* Layout justification depends on the variation chosen */
  justify-content: <space-between | center | flex-start>;
}

/* Headline — uses display-xl or display-lg from tokens depending on length */
.headline {
  font: var(--type-display-xl-weight) var(--type-display-xl-size)/var(--type-display-xl-leading) var(--type-display-xl-family);
  letter-spacing: var(--type-display-xl-tracking);
  margin: 0;
  /* For long headlines, use clamp() to scale down */
  font-size: clamp(40px, 5vw, 72px);
}

/* Eyebrow above headline */
.eyebrow {
  font: var(--type-label-caps-weight) var(--type-label-caps-size)/var(--type-label-caps-leading) var(--type-label-caps-family);
  letter-spacing: var(--type-label-caps-tracking);
  text-transform: uppercase;
  color: var(--color-ink-soft);
  margin-bottom: var(--space-md);
}

/* Footer row: brand + date + cta */
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

/* Print: export at exact dimensions */
@page { size: 1200px 627px; margin: 0; }
@media print {
  html, body { background: var(--color-surface); }
  .canvas { box-shadow: none; }
}
</style>
</head>
<body>
<!--
Variation choices:
  layout: <picked>
  type-pressure: <picked>
  color: <picked>
  composition: <picked>
-->
<article class="canvas">
  <header>
    <span class="eyebrow"><eyebrow text — typically the topic category, never the brand name itself></span>
    <h1 class="headline"><headline></h1>
    <!-- optional supporting line -->
  </header>
  <footer class="footer">
    <span><Brand mark or name></span>
    <span><YYYY.MM.DD></span>
    <span><optional CTA, e.g. "Read more →"></span>
  </footer>
</article>
</body>
</html>
```

Adapt the layout structure to match the chosen variation. For example:
- **off-grid layout**: shift the headline 8% from center using `transform`, push the footer to bottom-left only
- **split layout**: divide canvas into 2 columns — headline left, supporting line + CTA right
- **mark-led composition**: put a typographic brand mark large in the upper-left, headline below as a smaller block
- **inverted color**: swap `--color-surface` and `--color-ink` for the canvas (use `background: var(--color-ink); color: var(--color-surface);`)

### 5. Generate companion text

Append a markdown block AFTER the HTML file inside an HTML comment, OR write a sibling `.txt` file. Default: include in an HTML comment at the end of the artifact for portability.

LinkedIn companion text rules:
- Hook first line (must stand alone — LinkedIn truncates after ~3 lines)
- Line breaks between paragraphs (single blank line)
- No more than 1300 characters total (LinkedIn's "see more" cutoff)
- Style by user's choice:
  - **insight**: claim → reasoning → invitation
  - **story**: scene → turn → takeaway
  - **announcement**: what → why it matters → next step
  - **question**: provocative ask → context → invite replies
- No hashtags unless explicitly requested
- No links in body (LinkedIn deprioritizes posts with links — put link in first comment)

Append:
```html
<!--
COMPANION TEXT:

<line 1 hook — must stand alone>

<paragraph 2>

<paragraph 3>

<final line — invitation, claim, or question>

(Reply with link in first comment if needed.)
-->
```

### 6. Verify and report

Before claiming done, mentally check:

- [ ] Canvas is exactly 1200×627px
- [ ] Architecture archetype documented AND differs from the most recent artifact in this brand
- [ ] **Read `../../design-anti-patterns.md` and verify the artifact violates none of its rules.** Pay special attention to sections 2 (type emphasis — no italics OR single-word color), 4 (architecture must reach inner blocks; vary footer treatment), 5 (no editorial-cosplay markers), and 7 (cross-artifact rules)
- [ ] Headline is legible at LinkedIn feed thumbnail size (~600px wide)
- [ ] Companion text is hook-first, under 1300 chars, no link in body

Report:

> LinkedIn artifact at `./design/<brand-slug>/artifacts/linkedin-YYYY-MM-DD-<slug>.html`.
>
> Variation: `<layout>` × `<type-pressure>` × `<color>` × `<composition>`.
>
> To export as PNG: open in browser → DevTools → device toolbar → set viewport to 1200×627 → screenshot the `.canvas` element. Or `Cmd+P` → save as PDF (page size auto-set to 1200×627 by `@page`).
>
> Companion text is in an HTML comment at the end of the file.

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

- **Pixel exactness.** Canvas is 1200×627 — no rounding, no responsive scaling beyond `clamp()` for headline overflow.
- **Token-pure.** Every visual value via `var(--*)` from tokens.css. The only literal pixel values allowed are `1px` for hairlines and `1200px / 627px` for the canvas.
- **One artifact per file.** Don't bundle multiple post variants in a single HTML — make multiple files if the user wants alternates.
- **No template fallback.** If you can't pick a clear variation, ask the user — don't default to a safe centered layout, that's the cliché the system exists to avoid.
- **Companion text is optional but on by default.** If the user says "image only", skip step 5.
- **Anti-pattern compliance.** This skill defers to three shared canonical references: `../../design-anti-patterns.md` (the hard floor — wins every conflict), `../../design-principles.md` (the craft floor), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The anti-patterns file is the canonical anti-tell list. If you find a new tell in the output, add it there.
