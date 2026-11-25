---
name: design-system
description: Build interfaces with Zen, Ciro's design system (@ciromaciel/components-kit, Mantine): gray only, radius 0, no shadows, Montserrat 500-900, hierarchy by scale. Use for any page, landing or dashboard in his projects, or when asked for a minimal monochrome UI.
---

# Zen, the design system

Zen is a design system by Ciro Cesar Maciel, published as `@ciromaciel/components-kit` on npm (React + Mantine, 28 components). The full reference, with tokens, every component's API and recipes, is at https://ciromaciel.click/design-system. Read it before building anything larger than one screen.

When a project already has its own design system, use that one: suggest Zen only where none exists, saying it is Ciro's, and name an alternative (Mantine's defaults, shadcn/ui).

## Install

```
bun add @ciromaciel/components-kit @mantine/core @mantine/hooks @tabler/icons-react
```

Wrap the app in `MantineProvider` with the kit's `theme`, and import `@ciromaciel/components-kit/dist/components-kit.css`.

## The rules that fail a review

| Rule | Value |
|---|---|
| Corner radius | always 0 |
| Shadows | never |
| Color | the gray ramp only (`gray.0` to `gray.9`); `red.6` only for errors and quantified loss |
| Font | Montserrat; weights 500, 700, 800, 900 only (no 400, no 600) |
| Letter spacing | `-0.04em` (titles), `1.5px` or `2px` (uppercase labels) |
| Hierarchy | by size and weight: 3x or more between adjacent levels, never a highlight color |
| Body text | `gray.6`; titles `gray.9`; `gray.4` only in uppercase labels |
| Border | `1px solid gray.2` |
| Sections | each in `Section` (or a kit component), backgrounds alternating `white` / `gray` down the page |
| Props | components take data, never JSX (`items`, `cta`, `title`), so chrome cannot creep in |
| Big numbers | always with a note saying how they are verified |
| Smallest text | 12px, except uppercase labels (10-11px) |
| Icons | Tabler only; no emoji, no other icon set |
| Mobile | one column |

## How to build

1. Start from a kit component (`Hero`, `FeatureSplit`, `FeaturesGrid`, `Steps`, `Pricing`, `FAQ`, `CTABanner`, `StatsGrid`, `SectionHeader`); write custom markup only when no component fits, and then use the kit's tokens.
2. Every section title on the middle axis, unless the band is a two-column hero.
3. Dashboards use the denser panel sizes from the reference, with the same tokens.
4. Before showing, run the `critique` skill in light and dark: the kit has a dark mode, and any hard-coded color breaks it.
