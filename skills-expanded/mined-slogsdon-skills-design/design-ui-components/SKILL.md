---
name: design-ui-components
description: Generate components.html — a brand-agnostic component library that pulls from a project's DESIGN.md tokens. Includes buttons, cards, badges, eyebrows, hairlines, code blocks, callouts, hero blocks, stat callouts, list items, avatar frames, pull quotes, footer blocks. Use AFTER design-system and BEFORE platform artifact skills. Triggers include "components for [brand]", "component library", "generate UI components", "/ui-components".
---

# Skill: ui-components

Produces `./design/<brand-slug>/components/components.html` — a single self-contained HTML library where every reusable atom is rendered using the brand's `tokens.css`. Platform skills (linkedin-post, twitter-card, youtube-thumbnail, stream-overlay, instagram-post) read this library to compose artifacts without re-deriving primitive markup.

## When to use

- After `/design-system <brand-slug>` has produced `DESIGN.md` + `tokens.css`
- Before any platform artifact skill — they reference component snippets from this file
- When you've added a new component category (e.g. data viz callouts) that platform skills need

## Inputs

- `./design/<brand-slug>/DESIGN.md` (read for component prose guidance)
- `./design/<brand-slug>/tokens.css` (embedded via `<style>` block in the output)

## Output

`./design/<brand-slug>/components/components.html` — single file, no external CSS dependencies (Google Fonts `<link>` is allowed for the type families declared in `DESIGN.md`).

## Steps

### 1. Read inputs

```bash
test -f ./design/<brand-slug>/tokens.css && test -f ./design/<brand-slug>/DESIGN.md
```

If either is missing, stop and tell the user to run `/design-system <brand-slug>` first.

### 2. Pick component variations

For each component category below, pick ONE primary variation that fits the brand's visual direction. Show the alternates in the library too, but mark the primary explicitly so platform skills know which to default to.

### 3. Generate components.html

Use this structure. Each component section follows: heading → rendered preview → expandable HTML snippet.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><Brand Name> — Component Library</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=<Display+Family>&family=<Body+Family>&family=<Mono+Family>&display=swap">
<style>
/* Embed tokens.css verbatim */
<contents of tokens.css>

/* Page chrome — neutral wrapper, intentionally muted so components stand out */
body { background: var(--color-surface-muted); color: var(--color-ink); margin: 0; padding: var(--space-2xl); font-family: var(--type-body-md-family); }
.library { max-width: 960px; margin: 0 auto; }
.lib-section { margin-bottom: var(--space-3xl); }
.lib-section h2 { font: var(--type-headline-md-weight) var(--type-headline-md-size)/var(--type-headline-md-leading) var(--type-headline-md-family); letter-spacing: var(--type-headline-md-tracking); margin: 0 0 var(--space-md); }
.lib-section .preview { background: var(--color-surface); padding: var(--space-xl); margin-bottom: var(--space-md); border: 1px solid var(--color-rule); }
.lib-section details { font-family: var(--type-code-family); font-size: var(--type-code-size); }
.lib-section summary { cursor: pointer; padding: var(--space-xs) 0; color: var(--color-ink-soft); }
.lib-section pre { background: var(--color-ink); color: var(--color-surface); padding: var(--space-md); overflow-x: auto; margin: var(--space-xs) 0 0; }
</style>
</head>
<body>
<main class="library">
  <header style="margin-bottom: var(--space-3xl);">
    <span class="t-eyebrow">COMPONENT LIBRARY · v1</span>
    <h1 class="t-display-lg" style="margin: var(--space-sm) 0 var(--space-xs);"><Brand Name></h1>
    <p class="t-body-lg" style="color: var(--color-ink-soft); margin: 0;">Reusable atoms for platform artifacts. Every component is composed from tokens.css — no magic numbers.</p>
  </header>

  <!-- Sections below: one per component category -->
</main>
</body>
</html>
```

### 4. Component inventory (build each as a `.lib-section`)

Order matters — group by atomic level (smallest first).

#### a. Eyebrows
Mono uppercase tracked label. Variations: with hairline beside, with index number ("01 / "), with date prefix.

**Critical:** eyebrows are a tell when overused. They appear by default on a lot of AI-generated layouts and that's exactly the problem. Mark this category in the library as `OPTIONAL — apply only when the artifact genuinely needs category/section anchoring`. Never include the eyebrow in default scaffolds for platform skills; let the platform skill decide whether to invoke it per-artifact.

#### b. Hairlines
1px full-width rules. Variations: full-width, indented, with center label ("§").

#### c. Type scale samples
Render each type level from `DESIGN.md` once with the same string ("Build something obvious."). Useful as a quick reference for platform skills.

#### d. Buttons
- Primary (filled, ink-on-surface or surface-on-ink depending on direction)
- Secondary (outline)
- Tertiary (text-only with arrow suffix)
- Ghost (icon-only square)

Each in 3 sizes (sm, md, lg). Show hover state via `:hover` rules.

#### e. Badges / tags
Small inline labels. Variations: solid, outline, dot-prefixed, with count ("New · 3").

#### f. Cards
- Plain card (padding + surface + border)
- Stat card (big number in `display-xl`, label in eyebrow)
- Linked card (entire surface clickable, arrow appears on hover)

#### g. Code blocks
- Inline `<code>` with subtle background
- Multi-line `<pre>` with optional filename header bar

#### h. Callouts
- Note (neutral)
- Warning (uses `--color-warning`)
- Success (uses `--color-success`)

Use a thin left rule, NOT a colored background fill (that's a cliché). Icon optional, must be a single character or simple SVG, never an emoji.

#### i. Hero blocks
- Headline-led: massive `display-xl` headline + body-lg subhead, no image
- Quote-led: pull quote in `display-lg` italic + attribution in eyebrow
- Stat-led: oversized number + supporting context

#### j. Stat callouts
Big number (`display-xl` or larger via `clamp()`) + small label. The unit (%, ×, etc.) sits at half the number's size for visual hierarchy.

#### k. List items
- Numbered (with eyebrow-styled index)
- Bulleted (with custom marker — never a generic disc, use `—` or `›` or a hairline)
- Definition list (term in eyebrow, def in body)

#### l. Pull quotes
Display serif italic, large size, with indent rule on the left. Attribution sits below in eyebrow style with em-dash prefix.

#### m. Avatar / headshot frame
Square or circle (matches `--radius-*` philosophy). With optional 1px ring + name plate beneath in eyebrow + role.

#### n. Footer block
Eyebrow-style row: brand mark + URL + date + version. Used as the consistent signature on every platform artifact.

#### o. Brand mark placeholder
A typographic logotype using the display family. Provide 2–3 variations: the wordmark plain, the wordmark with a hairline rule above or below, the wordmark with a single-character accent (a period in accent color, an em-dash, etc.).

**Forbidden by default:** the `/Brand` slash-prefix mark. It became a Vercel/Linear-era cliché around 2023; using it now reads as "AI mimicking a SaaS startup." Only include this variant if the brand's `DESIGN-PLAN.md` explicitly requests it.

### 5. Mark the primary variant for each category

At the top of each section, add a one-line note: `<!-- PRIMARY: <variant-name> -->` so platform skills know which to default to.

### 6. Hand off

After writing the file:

> Component library generated at `./design/<brand-slug>/components/components.html`.
> Open in a browser to verify visual consistency. Every platform skill (linkedin-post, twitter-card, youtube-thumbnail, stream-overlay, instagram-post) will pull from this library.
>
> Next: run a platform skill, e.g. `/linkedin-post "Your post topic" --brand <brand-slug>`.

## Rules

- **Token-pure.** Every color, font, spacing, and radius value must come from `var(--*)`. No literal hex codes or px values in component CSS except `1px` for borders.
- **Self-contained.** The file works opened directly in a browser — no build step, no JS framework, no external CSS beyond Google Fonts.
- **No JS for visuals.** Components are pure HTML+CSS. JS is allowed only for the `<details>` snippets being expandable (which is native HTML, no JS needed).
- **Variation discipline.** For each category, pick ONE primary that fits the brand's visual direction. Showing 4 button styles is fine; designating none as primary leaves platform skills guessing.
- **Anti-pattern compliance.** Read the three shared canonical references before building the library: `../../design-anti-patterns.md` (hard floor — wins all conflicts), `../../design-principles.md` (craft floor), `../../design-variation-sop.md` (direction roster). Components must violate none of the anti-pattern rules. Especially: no center-aligned hero template, no drop shadows on text, no filled-background callouts (left rule + color hint instead), no emoji icons, no `/Brand` slash mark, **no single global border-radius on every atom** (radius is role-specific — a button, card, image, and input do not share one corner; principles §1/§4), no indigo/violet default accent, no Inter/Roboto/system primary family.
