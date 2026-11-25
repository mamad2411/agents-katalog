---
name: taste-direction
description: Design decision engine of the Tastemaker suite. Chooses style, palette, typography, layout, navigation, density, motion and chart types from the product archetype and audience, with a one-line reason for each, and runs UX-law and accessibility checks before any code. Use when starting or restyling any UI, choosing colors or fonts, picking a dashboard layout or chart, or when output "looks generic". Extends ui-ux-pro-max style and palette lookups with a reasoned, slop-free decision.
---

# Taste Direction: decide before you draw

Taste is a chain of reasons. Output a **Design Decision** before code. Every line needs a "why" tied to the product, the audience or the data. Trend is never a reason.

## Procedure

1. Read archetype, users, top-3 questions and risk from `BUILD_MANIFEST.md` (or infer them in 3 lines).
2. **Style**: one primary + at most one modifier (`references/styles.md`).
3. **Palette**: domain recipe, one accent, semantic status set; verify contrast (`references/palettes.md`, `../taste-tokens/scripts/contrast.mjs`).
4. **Type**: pairing + scale + numeric style (`references/typography.md`).
5. **Layout + nav + density**: from the user's top questions, not from a template (`references/layout-patterns.md`).
6. **Interaction**: forms, tables, feedback, destructive flows (`references/interaction.md`).
7. **Motion level**: none / subtle / expressive with durations (`references/motion.md`).
8. **Charts**: one chart per question (`references/dataviz.md`).
9. **Pre-flight**: UX laws + accessibility floor (`references/ux-laws.md`). Name the top risk for this audience.

## Output (8 lines, shown to the user on new builds so they can redirect cheaply)

```
Style:    <primary> + <modifier>            | why: <audience/product reason>
Palette:  <recipe>, primary <token>, accent <token or none>, neutral <family> | why:
Type:     <heading> / <body> / <mono>, base <14|16>, scale <ratio> | why:
Layout:   <pattern>, nav <pattern>, density <compact|comfortable|spacious> | why: answers "<top question>"
Motion:   <none|subtle|expressive>, <durations> | Theme: <light|dark|both>
Charts:   <metric -> chart>; <metric -> chart>
Avoid:    <3 slop IDs most likely for this archetype, e.g. V01 V15 C01>
Risk:     <what could fail for this audience and how the design prevents it>
```

## Anti-default rules

- Do not reach for indigo/violet as primary unless the brand says so. Pick hue from the domain recipe.
- Do not default to "hero + 3 feature cards + testimonials + CTA" for marketing, or "4 KPI cards + area chart + table" for dashboards. Derive sections from the top questions (V15, V17).
- Inter is acceptable when density and neutrality are the point; say so. Otherwise choose a pairing with character from the table.
- Restraint scales: a dense ops tool earns less decoration than a consumer onboarding flow, never more.
- Interop: if the `ui-ux-pro-max` skill is installed, you may query its search script for extra style or palette candidates; this skill still makes the final, reasoned choice and the guard still gates it.
