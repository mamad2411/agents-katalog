---
name: design-system
description: Generate a brand-agnostic DESIGN.md (Google design.md spec format) plus tokens.css and showcase.html for any branding project. Reads ./design/<brand-slug>/DESIGN-PLAN.md if present, otherwise asks for an inline brief. Use AFTER design-plan and BEFORE design-ui-components. Triggers include "design system for [brand]", "build a DESIGN.md", "generate design tokens", "/design-system".
---

# Skill: design-system

Generates three artifacts that together define a brand's visual system:

1. **`DESIGN.md`** — portable spec following the [Google design.md format](https://github.com/google-labs-code/design.md). YAML frontmatter (machine-readable tokens) + 8 markdown sections (human rationale).
2. **`tokens.css`** — CSS custom properties exported from the YAML, consumed by `design-ui-components` and every platform skill.
3. **`showcase.html`** — single self-contained HTML page that renders every token in context. The visual proof that the system holds together.

## When to use

- After `/design-plan` has produced `DESIGN-PLAN.md`
- Before any platform artifact skill (LinkedIn, Twitter, YouTube, etc.) — they all read `DESIGN.md` and `tokens.css`
- When iterating on brand: re-run to regenerate downstream files when the plan changes

## Inputs

- **Required:** brand slug (e.g. `shane-personal`)
- **Preferred:** existing `./design/<brand-slug>/DESIGN-PLAN.md` (read with Read tool)
- **Fallback:** if no plan exists, ask the user for a 3-question inline brief (visual direction, voice adjectives, hard NOs)

## Outputs

```
./design/<brand-slug>/
  DESIGN.md          # Google spec format
  tokens.css         # CSS custom properties
  showcase.html      # visual proof
```

## Steps

### 1. Locate and read the plan

```bash
test -f ./design/<brand-slug>/DESIGN-PLAN.md
```

If present, read it. If absent, ask the user 3 quick questions (visual direction, voice adjectives, hard NOs) and proceed with those answers as the de-facto plan.

### 2. Derive concrete tokens from the plan

Translate the plan's strategic decisions into specific token values. Use these heuristics by visual direction:

**editorial** → display serif (Fraunces, Playfair Display, Crimson Pro, Newsreader), restrained sans body (Söhne, Public Sans, IBM Plex Sans), mono accents (JetBrains Mono, Berkeley Mono); warm neutral surface (#fbfaf9-ish, not pure white); single ink color near-black; one accent used sparingly; generous letter-spacing on small uppercase labels (0.18em+); hairline rules over heavy borders; small radius (0–4px).

**technical** → mono-dominant or sans-only (IBM Plex, Source Sans 3, JetBrains Mono); cool neutrals or high-contrast; small radius (0–2px); compact density; single signal accent (often a saturated green or amber); grid-paper texture allowed; eyebrow labels mandatory.

**bold** → heavy display sans (Clash Display, Cabinet Grotesk, Satoshi, Söhne Breit, Roobert) at 800–900 against 100–200 body, high-saturation palette, sharp contrast, large radius (8–16px) or zero radius (no middle), unapologetic 4×+ scale jumps.

**minimal** → single humanist sans family (Söhne, Public Sans, IBM Plex Sans), 2–3 weights max, mostly grayscale with one quiet accent, large whitespace, no decorative elements, larger radius (8px+) for softness. Valid only when chosen deliberately against the alternatives — never as the default (see `../../design-variation-sop.md` Rule 1).

> **Never** derive Inter, Roboto, Arial, Open Sans, Lato, Helvetica, or system stack as the primary family — that is the AI-default monoculture (anti-patterns §2). The fuller named-aesthetic roster (Swiss, brutalist, warm minimal, code/terminal, solarpunk, distinctive display, archival, etc.), each defined in concrete type/color/radius/density/layout terms, lives in `../../design-variation-sop.md`. These four directions are the common cases; the roster is the full menu — pick from it deliberately, biased away from recent brands and away from minimal-by-default.

**mixed** → resolve based on the two directions chosen and how they were described.

For each token category, pick one option from the **variation axes** below to avoid output collapse:

- **Surface tone**: warm-cream | cool-paper | true-white | near-black | warm-charcoal
- **Accent role**: single-color | dual-accent | mono-with-signal | no-accent (grayscale only)
- **Type pairing**: serif-display + sans-body | sans-display + sans-body | sans-display + mono-body | mono-only | serif-only
- **Radius scale**: zero (0px) | hairline (2px) | small (4px) | medium (8px) | soft (12–16px)
- **Spacing scale**: 4px-base (compact) | 6px-base (balanced) | 8px-base (spacious)

State which option you picked from each axis at the top of `DESIGN.md` as a comment so the choice is reproducible.

When deriving the actual token *values*, apply `../../design-principles.md`:

- **Typographic extremes** (§1): the type scale uses weight extremes (100/200 vs 800/900, not 400 vs 600) and 3×+ size jumps. Display weights should reach 700–900 or drop to 100–300 — do not cluster every level at 500–600. Pick one distinctive family and use it decisively; max 2 families.
- **Dominant + sharp accent** (§3): one color owns the large surfaces, one saturated accent is used rarely. Reject any palette where you can't name the single dominant and the single accent. Draw the palette from a real reference (IDE theme, material, subject) — never the neutral SaaS center.
- Before committing the system, sketch **three distinct directions** per `../../design-variation-sop.md` Rule 3 and offer them as a one-line menu; generate the best-fit by default, all three only if asked.

### 3. Write DESIGN.md (Google spec format)

Use this structure exactly. Sections appear in this order. YAML frontmatter is mandatory.

```markdown
---
version: alpha
name: <Brand Name>
description: <One-line summary of the visual identity>
colors:
  primary: "#XXXXXX"
  secondary: "#XXXXXX"
  accent: "#XXXXXX"
  surface: "#XXXXXX"
  surface-muted: "#XXXXXX"
  ink: "#XXXXXX"
  ink-soft: "#XXXXXX"
  rule: "#XXXXXX"
  success: "#XXXXXX"
  warning: "#XXXXXX"
  danger: "#XXXXXX"
typography:
  display-xl:
    fontFamily: <Family>
    fontSize: 64px
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: -0.02em
  display-lg:
    fontFamily: <Family>
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: -0.018em
  headline-md:
    fontFamily: <Family>
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: <Family>
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: -0.01em
  body-lg:
    fontFamily: <Family>
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.55
  body-md:
    fontFamily: <Family>
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: <Family>
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
  label-caps:
    fontFamily: <Mono Family>
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.18em
  code:
    fontFamily: <Mono Family>
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
spacing:
  base: 16px
  3xs: 2px
  2xs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  4xl: 96px
rounded:
  none: 0
  sm: 2px
  md: 4px
  lg: 8px
  full: 9999px
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
    padding: 12px 20px
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: 12px 20px
---

<!--
Variation choices:
  surface: <picked>
  accent: <picked>
  type-pairing: <picked>
  radius: <picked>
  spacing: <picked>
-->

# <Brand Name> — Design System

## Overview

<3–5 sentences capturing brand personality, target emotional response, and how the look feels in one paragraph. Reference the visual direction from DESIGN-PLAN.md without restating it verbatim.>

## Colors

<Prose: explain the role of each palette entry — primary as ink/permanence, accent as the only attention-pull, surface as foundation. 3–6 sentences total.>

## Typography

<Prose: explain the type pairing logic, where each level is used, why these families. Mention specific feature settings if any (e.g. "ss01" for Inter alternates, "cv11" for single-story g).>

## Layout

<Spacing scale rationale, grid approach (8pt baseline grid is the default unless the plan said compact/spacious), max widths for content, gutter strategy.>

## Elevation & Depth

<Flat vs. layered. If flat, explain how hierarchy is conveyed (rules, color contrast, scale). If layered, define shadow/border tokens.>

## Shapes

<Radius philosophy. Editorial systems often go zero-radius for an architectural feel; technical systems often hairline (2px); minimal systems lean soft (8px+).>

## Components

<Brief notes on button hierarchy, input states, card structure. Defer detail to design-ui-components — this section is just the rationale.>

## Do's and Don'ts

- Do <use the accent color only for the single most important action per surface>
- Do <maintain WCAG AA contrast: 4.5:1 for body, 3:1 for large text>
- Don't <mix more than 2 type families and 3 weights on a single surface>
- Don't <introduce off-palette colors when an existing token solves the problem>
- <pull every Hard NO from DESIGN-PLAN.md verbatim into this list>
```

### 4. Generate tokens.css

Convert the YAML frontmatter into CSS custom properties. Mapping rules:

- `colors.<name>` → `--color-<name>`
- `typography.<name>.<prop>` → `--type-<name>-<prop-short>` where prop-short = `family | size | weight | leading | tracking`
- `spacing.<name>` → `--space-<name>`
- `rounded.<name>` → `--radius-<name>`

Write to `./design/<brand-slug>/tokens.css`:

```css
/* Auto-generated from DESIGN.md — do not edit by hand. Re-run /design-system to regenerate. */
:root {
  /* Colors */
  --color-primary: <value>;
  --color-secondary: <value>;
  /* …all colors… */

  /* Typography */
  --type-display-xl-family: <value>;
  --type-display-xl-size: 64px;
  --type-display-xl-weight: 600;
  --type-display-xl-leading: 1.05;
  --type-display-xl-tracking: -0.02em;
  /* …all type levels… */

  /* Spacing */
  --space-base: 16px;
  --space-xs: 8px;
  /* …all spacing… */

  /* Radii */
  --radius-sm: 2px;
  /* …all radii… */
}

/* Convenience utility classes — optional but useful for design-ui-components */
.t-display-xl { font: var(--type-display-xl-weight) var(--type-display-xl-size)/var(--type-display-xl-leading) var(--type-display-xl-family); letter-spacing: var(--type-display-xl-tracking); }
.t-display-lg { font: var(--type-display-lg-weight) var(--type-display-lg-size)/var(--type-display-lg-leading) var(--type-display-lg-family); letter-spacing: var(--type-display-lg-tracking); }
/* …one utility per type level… */

.t-eyebrow {
  font: var(--type-label-caps-weight) var(--type-label-caps-size)/var(--type-label-caps-leading) var(--type-label-caps-family);
  letter-spacing: var(--type-label-caps-tracking);
  text-transform: uppercase;
  color: var(--color-ink-soft);
}
```

### 5. Generate showcase.html

A single self-contained HTML page proving every token in context. Structure:

1. **Header** — brand name in `display-xl`, tagline in `body-lg`, eyebrow label "DESIGN SYSTEM v1"
2. **Color palette** — every color token as a 120×120 swatch with the token name and hex
3. **Type scale** — every type level rendered with sample text ("The quick brown fox jumps over the lazy dog — 0123456789")
4. **Spacing scale** — every spacing token as a labeled bar (4px tall, width = the token value)
5. **Radii** — every radius token as a 64×64 filled square showing the corner shape
6. **Component preview** — primary button, secondary button, card, badge, hairline divider, eyebrow label

The showcase MUST embed `tokens.css` via inline `<style>` so the file is portable.

Keep markup semantic and minimal. Use only the tokens — no magic numbers, no off-palette colors. The showcase is a litmus test: if it looks coherent here, the system holds.

### 6. Verify and hand off

After writing all three files, do one self-check:

- [ ] Did I pick one option from each variation axis and document it?
- [ ] Does every color in `tokens.css` appear in `DESIGN.md`'s YAML?
- [ ] Are the Hard NOs from `DESIGN-PLAN.md` reflected in the Do's/Don'ts?
- [ ] Is `showcase.html` self-contained (no external CSS, no external fonts unless via Google Fonts `<link>`)?

Then tell the user:

> System generated for `<brand-slug>`:
> - `./design/<brand-slug>/DESIGN.md` — Google spec format
> - `./design/<brand-slug>/tokens.css` — CSS custom properties
> - `./design/<brand-slug>/showcase.html` — visual proof
>
> Open `showcase.html` in a browser to verify. Next: run `/design-ui-components <brand-slug>` to generate the component library.

## Rules

- **Brand-agnostic.** Never hardcode Shane's brand values. Every value derives from the plan or the variation matrix.
- **Self-contained outputs.** `showcase.html` and downstream artifact files should work offline (Google Fonts `<link>` is the only allowed external).
- **Spec-compliant.** YAML frontmatter must validate as the Google design.md schema (colors, typography, rounded, spacing, components groups; token references via `{path.to.token}`).
- **Reproducible.** The variation choices comment block at the top of `DESIGN.md` must list the picked option per axis. Re-running with the same plan + same picks should produce equivalent output.
- **Anti-pattern compliance.** Read the three shared canonical references before generating tokens: `../../design-anti-patterns.md` (hard floor — wins all conflicts), `../../design-principles.md` (craft floor — typographic/spatial/color/layout/tension requirements), and `../../design-variation-sop.md` (direction roster + offer-3 procedure). The Do's and Don'ts section of `DESIGN.md` should pull in any brand-specific Hard NOs from `DESIGN-PLAN.md`, but the universals (no purple-cyan gradients, no indigo/violet default, no drop shadows on text, no more than 2 type families, no Inter/Roboto/system primary, no accent-as-partner-to-primary) come from the shared references and don't need to be restated.
