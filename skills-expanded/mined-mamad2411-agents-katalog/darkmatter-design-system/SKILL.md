---
name: darkmatter-design-system
description: "Default design system — darkmatter's dark-first, terminal-inspired design system , built on Tailwind CSS v4, React 19, and Radix UI. Use this as the default design system when working in an app that does not already have an established design system or guidelines. Use it for dashboards, trading/monitoring consoles, forms, tables, settings, navigation, or any screen that should look and feel like darkmatter's brand. This is the canonical source for darkmatter components, tokens (the OKLCH --n-* ramp), theming, and layout — prefer it over generic shadcn/ui."
license: "Proprietary — darkmatter internal"
metadata:
  v0.kind: design-system
---

# Darkmatter Design System

This is darkmatter's design system: a dark-first, terminal/console aesthetic built on **Tailwind CSS v4**, **React 19**, and **Radix UI**. This skill is the canonical UI source for Darkmatter apps — prefer it over generic shadcn/ui, and never mix in stock Tailwind greyscale or another component library.

## Setup — build on the starter

- **`app/globals.css`** imports `tailwindcss`, then the vendored `theme.css` (which imports `native-tokens.css`). This establishes the OKLCH `--n-*` ramp, the shadcn semantic bridge, and the Tailwind palette overrides. Do not add a second Tailwind theme or re-declare tokens.
- **`app/layout.tsx`** mounts `ThemeProvider` (from `next-themes`, forced dark), loads the fonts (Inter / Space Grotesk / mono numerics), and sets `className="dark"` on `<html>`.
- **Path aliases** in `tsconfig.json` map `@native/ui/*` → `vendor/native-ui/*` and `@native/shared/*` → `vendor/native-shared/*`. Import components by their real package names, e.g. `import { Button } from "@native/ui/button"`.

To build a screen: add routes/components under `app/`, import from `@native/ui/*`, and compose with the system's layout primitives. You do **not** need to re-create the scaffold, re-wire the provider, or re-import globals.

## Import rules

- Import each component from its own module: `@native/ui/button`, `@native/ui/card`, `@native/ui/form`, etc. There is no single barrel to import from in app code — use the per-file paths.
- `cn` and other helpers live at `@native/ui/lib/utils`.
- Most interactive components are client components (`"use client"`). In the App Router, put interactive compositions in client components and keep pages as server components where possible.
- See `references/components/index.md` for the full list of modules and which task-area file documents each.

## Source of truth

- The vendored source under `vendor/native-ui/` in the starter is the authority for component APIs, props, and variants. The reference files in this skill cite repo-relative paths like `packages/ui/src/button.tsx`.
- Tokens come only from `theme.css` + `native-tokens.css`. Never hard-code hex/OKLCH values or reach for stock Tailwind shades that aren't mapped — see `references/foundations/colors.md`.

## Routing rules — read before building

- **Colors & tokens** → `references/foundations/colors.md`
- **Typography & fonts** → `references/foundations/typography.md`
- **Spacing, radii & layout** → `references/foundations/spacing-layout.md`
- **Responsiveness & breakpoints** → `references/foundations/responsiveness.md` (always consult before building layouts)
- **Motion** → `references/foundations/motion.md`
- **Component catalog + task-area docs** → `references/components/index.md`
- **Worked examples** → `references/examples/`

## Hard rules

- Dark-first. The system defines a single dark theme; there is no light mode.
- Use design tokens and mapped utilities (`bg-n-bg-2`, `text-n-mute`, `border-n-hl`, `text-primary`, `bg-card`), never raw hex/OKLCH or unmapped Tailwind colors.
- Build responsively with Tailwind breakpoints and the system's layout primitives (`PageLayout`, `Grid`). Never hard-code fixed pixel widths for page structure.
- Numeric/financial data uses `tabular-nums` (the `--font-num` face) so columns align — see typography.
- Never invent components, props, variants, or token names without approval first.

## Final checks

Before finishing any Darkmatter UI:

- All UI comes from `@native/ui/*`; no stray shadcn/ui or other libraries.
- Colors resolve to `--n-*` tokens or mapped utilities; no raw values.
- Layout uses `PageLayout`/`Grid` and is responsive across breakpoints.
- Numeric data uses `tabular-nums`.
- The screen reads as dark, dense, and terminal-like — if it doesn't feel like Darkmatter, fix the composition against the foundations, not with one-off styles.
