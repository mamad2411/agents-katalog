---
name: taste-tokens
description: Builds the design-token system every Tastemaker skill consumes - primitive, semantic and component layers in design-tokens.json, light/dark/high-contrast themes, density modes, and generated tokens.css, Tailwind v4 @theme, Tailwind v3 config and shadcn/ui variables, with automatic reference and WCAG contrast validation. Use for "design system", "tokens", "theme", "dark mode", "brand colors in Tailwind", "component specs", or before any UI build that lacks tokens.
---

# Taste Tokens: one source of truth

Every color, space, radius, font, shadow, duration and z-index in the product comes from `design-tokens.json`. Components never see a raw value (V08).

## Modes

- **Minimal** (default before UI work): copy `templates/design-tokens.json`, set primary/neutral from taste-direction or brand, build, done.
- **Full** (explicit design-system request): all layers, component specs, docs page, governance.

## Procedure

1. Start from `templates/design-tokens.json` (valid, contrast-checked). Replace primitives with the brand or taste palette; keep the semantic names.
2. Three layers (`references/token-architecture.md`): **primitive** (raw) -> **semantic** (role, the only layer components use) -> **component** (targeted overrides). Themes remap semantic only.
3. Every semantic color has a `light` and `dark` value; add `contrast` pairs for every text/background combination you use.
4. Build and validate:
   ```bash
   node <skill-dir>/scripts/build-tokens.mjs design-tokens.json --out src/styles
   ```
   Writes `tokens.css` (CSS variables + shadcn aliases, light/dark/reduced-motion), `tailwind.v4.css` (`@theme inline`), `tailwind.v3.cjs` (`theme.extend` fragment). Fails on unresolved references, missing dark values, component-to-primitive references and contrast failures. Fix and rebuild until clean.
5. Wire by detected Tailwind major (tastemaker/references/stacks.md): v4 imports `tailwind.v4.css` after `@import "tailwindcss"`; v3 spreads `tailwind.v3.cjs` into `theme.extend`.
6. Full mode: write component specs (`references/component-spec.md`) and a `design-system.html` showing swatches, type, spacing, radius, elevation and every component state in both themes.

No Node available (chat platforms): emit `tokens.css` by hand from the same structure and list the contrast pairs you checked with their ratios.

## Rules

- Names: `{category}.{role}.{variant}.{state}` in JSON, `--color-bg-surface` in CSS. Lowercase, no brand names in semantic tokens.
- Dark mode is a remap, not an inversion. Elevation in dark = lighter surface, not shadow.
- Density via `data-density="compact|comfortable"` overriding component space/size tokens.
- Theme switch: class `.dark` (or `data-theme`) on `<html>`, respect `prefers-color-scheme` on first visit, persist with try/catch storage, set before paint to avoid flash.
- Versioning: semver. Add = minor, rename/remove = major (keep a deprecated alias for one minor), value tweak = patch.

## Quality gate

- [ ] Build script exits 0 (references, dark coverage, layer rules, contrast).
- [ ] shadcn variable set complete (`--background` ... `--ring`, `--radius`, `--chart-1..5`).
- [ ] No raw values in components (`tastemaker scan` V08 clean).
- [ ] Specs exist for every shipped component (Full mode).
