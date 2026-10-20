---
tags: [design, figma, token, tailwind, theme]
name: figma-token-to-tailwind-theme
description: Pipeline from Figma Token Studio JSON exports through Style Dictionary v5 to Tailwind v4 @theme CSS custom properties, with dark/light/contrast mode support and breaking change detection
category: design
trigger: When setting up a design token pipeline from Figma to code, or migrating to Tailwind v4 @theme format
version: 1.1.0
source_project: lucida-ui
linked_knowledge:
  - dual-design-token-pipeline-arch
---

# Figma Token → Tailwind @theme Pipeline

## Context
Design tokens authored in Figma Token Studio need to flow into code as CSS custom properties consumable by Tailwind v4's `@theme` directive, supporting dark/light/contrast mode switching via `[data-theme]` selectors.

## Steps

1. **Export tokens from Figma Token Studio** as DTCG multi-file JSON:
   - `tokens/core.json` — primitive values (colors, spacing, sizing)
   - `tokens/semantic/brand/*.json` — brand-specific aliases
   - `tokens/semantic/theme/{light,dark,contrast}.json` — per-mode overrides
   - `tokens/semantic/size.json` — component sizing
   - `tokens/$themes.json` — theme permutation metadata

2. **Configure Style Dictionary v5** build script (`scripts/build-tokens.mjs`):
   - Register `@tokens-studio/sd-transforms` with hex color modifier format
   - Use `permutateThemes()` to find Light/Dark/Contrast keys for the target brand
   - Custom `name/custom-css` transform maps token paths to CSS variable names via rule-based matching
   - Transform chain: `ts/resolveMath`, `ts/size/px`, `ts/opacity`, `ts/typography/fontWeight`, `ts/color/modifiers`, `ts/color/css/hexrgba`, `shadow/css/shorthand`, `border/css/shorthand`, `name/custom-css`

3. **Token naming convention** — Rule-based path-to-variable mapping:
   - `color.*` → `--color-*`, `brand.*` → `--color-brand-*`
   - `sizing.*` → `--sizing-*`, `spacing.*` → `--spacing-*`
   - `borderRadius.*` → `--radius-*`, `boxShadow.*` → `--shadow-*`
   - `brand-fontSize.*` → `--text-*` (with `--line-height` and `--letter-spacing` companions)
   - Theme semantic categories (background, layer, text, etc.) → `--color-{category}-{token}`

4. **Section-ordered output** — Tokens grouped into readable sections:
   - Spacing Base → Core Colors → Core Sizing → Brand Colors → Typography → Component Size → Theme categories
   - Typography composed as triplets: `--text-{role}`, `--text-{role}--line-height`, `--text-{role}--letter-spacing`

5. **Dark/Contrast override diffing** — Only variables that differ from light are emitted:
   - Light: full `@theme {}` block
   - Dark: `[data-theme="dark"] { /* changed vars only */ }`
   - Contrast: `[data-theme="contrast"] { /* changed vars only */ }`

6. **Breaking change detection** — Compares old and new `@theme {}` to find removed tokens:
   - Reports removed/added token count
   - Prints grep command to find affected source files

7. **Consume in Tailwind v4**:
   - `@import './tokens.css'` in your main CSS entry
   - Variables available as `bg-[--color-background-primary]` or via Tailwind config mapping
   - Manual portal tokens in separate `portal.css` for values not yet in Figma

## Key decisions
- Light mode defines all base vars; dark/contrast only override differing vars (smaller bundle)
- Token naming: rule-based path mapping, not simple kebab-case, for semantic CSS variable names
- Legacy theme constants (`THEME_LIGHT`, `THEME_DARK`) coexist for non-Tailwind consumers

## See also
- `content.md` for full SD v5 configuration, naming rules, and diffing implementation
