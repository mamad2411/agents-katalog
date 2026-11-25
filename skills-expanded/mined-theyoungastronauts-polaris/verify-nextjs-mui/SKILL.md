---
name: verify-nextjs-mui
description: "MUI-specific Next.js verification checklist — sx/Emotion SSR setup, Grid size prop."
disable-model-invocation: true
---

# Skill: Verify Next.js (MUI)

## Purpose
MUI-specific checklist for a Next.js + Material UI project. Run alongside `verify-nextjs.md` (general Next.js/React concerns) — this file only covers what MUI adds. MUI projects use Emotion, **not** Tailwind, so skip the Tailwind section of `verify-nextjs.md`.

## Verification Process

Flag each as PASS, WARN, or FAIL.

### 1. Styling (sx + Emotion)
- [ ] Component styling uses the `sx` prop (or `styled()`), not inline `style={{}}`
- [ ] No Tailwind — no `tailwind.config`, `postcss.config`, or `globals.css` utility layer (MUI owns styling via Emotion)
- [ ] Colors and spacing come from the theme (`primary.main`, `text.secondary`, spacing units), not hardcoded hex/px
- [ ] Emotion is the only styling engine — `styled-components` is not mixed in

### 2. SSR + Theme Setup (layout.tsx)
- [ ] `AppRouterCacheProvider` wraps the app with `options={{ enableCssLayer: true }}` so Emotion styles are injected correctly during SSR (no style flash / hydration mismatch)
- [ ] `InitColorSchemeScript` is rendered (matching the theme's `attribute`) to prevent a light/dark flash on load
- [ ] `ThemeProvider` + `CssBaseline` live in `layout.tsx`, not re-declared in nested providers

### 3. Components
- [ ] MUI `Grid` uses the v6+ `size` prop (`<Grid size={{ xs: 12, sm: 6 }}>`), not the deprecated `item` + `xs`/`sm`/`md` props

## Output
Produce a `verification-report.md` (same format as verify-django), adding a "MUI" section.
