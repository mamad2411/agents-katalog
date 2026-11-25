---
name: design-system
description: Generate a unique, production-grade brand design system from a short brief. Use when starting a new site or product, defining or extending design tokens (color, type, spacing, radii, shadows, motion), producing a token file plus Tailwind config plus a brand rules doc plus a storybook, or giving a project a distinct visual identity. Encodes a house DNA and forces per-brand variation so no two systems look alike.
license: MIT
---

# Design System

A factory for brand identities. Given a short brief, it produces a complete, unique design system in the house DNA: a token file, a Tailwind config, a brand rules doc the agent obeys, a storybook, and a human spec. The opposite of a template: the DNA (method and quality bar) stays constant, the output (palette, type, shape, mood) is different every time.

It is the piece that kills the generic look at the source. The `fluid` skill handles motion, the detector catches slop after the fact, this gives each project an identity from line one.

Built from four hand-made systems: MVP "Liquid Glass" (the structural template), LeCoffre (the delivery format), PLR @plr/ui, and Vigie.

## When to use

- Starting a new client site or product and you need its visual identity defined.
- Producing or extending design tokens (color, type, spacing, radii, shadows, motion).
- You want a `tokens.css` + Tailwind config + brand `CLAUDE.md` + storybook for a project.
- An existing UI feels generic and needs a committed identity.

## The two halves

A system here is DNA (constant) plus brand (variable). Get both right.

- The DNA is the house method and quality bar. It never changes. See `reference/dna.md`.
- The brand is what makes this system unlike any other: palette, type, shape, surface, mood. Derived per project from the brief. This is where you must NOT converge.

## init: the workflow

1. Gather the brief (ask only what is missing):
   - Brand name and sector/positioning.
   - Personality, pick an extreme: institutional/refined, editorial, luxury, playful/energetic, techy/precise, brutalist/raw, organic/warm. Half-measures read as generic.
   - Light, dark, or both (auto).
   - Surface treatment: flat, soft (subtle shadow/relief), or glass (liquid, translucent).
   - One anchor or constraint: an existing logo color, a reference you admire, a competitor you must NOT resemble.

2. Derive the brand variables (commit, do not hedge):
   - Start from the database: pick a palette from `data/palettes.md` (100+ committed palettes), a type pairing from `data/type-pairings.md` (50+ distinctive pairings), a style direction from `data/styles.md`, and a layout archetype from `data/layouts.md` that fit the brief. Adapt the exact values; never improvise a generic default, and never default to the split-hero-plus-three-cards skeleton. Two clients in the same sector get different picks, including a different page shape. For motion reach into `data/motion-presets.md`, for any data display into `data/chart-types.md`, and for the build pick a stack from `data/tech-stacks.md`.
   - Color: one dominant brand hue + one sharp accent + semantic (success/warn/danger) + tuned neutrals. Never pure black. See `reference/color.md`.
   - Type: a distinctive display font paired with a refined body font, self-hosted. Never Inter/Roboto/Arial as the primary. See `reference/typography.md`.
   - Shape: a radii scale (sharp 4 to 8, rounded 12 to 22, or pill) chosen to match the personality.
   - Surface/relief: flat, soft-shadow, or glass tokens.
   - Motion: the house easings, already in the template (`--ease-out`, `--spring`, `--ease-in-out`), shared with `fluid`.

3. Map to light/dark tokens: decide which tokens invert (bg, surface, text, glass, tints, on-tint) and which hold (brand hues, accent). See `reference/color.md`.

4. Emit the files from `templates/` (fill the `{{placeholders}}`):
   - `tokens.css`: the source of truth (CSS variables + base classes).
   - `tailwind.config.js`: same tokens for Tailwind/TanStack sites (omit for CSS-pur projects).
   - `CLAUDE.md`: the brand rules the agent obeys on every UI task.
   - `storybook.html`: a live showcase of every token and base component.
   - `DESIGN_SYSTEM.md`: the human-readable spec.
   Put them in a `<project>/design-system/` folder (the LeCoffre pattern).

5. Wire it: load the fonts, import `tokens.css` (or extend Tailwind), and from then on every color/space/radius is `var(--token)`, never a raw value.

## Stack note (light/dark strategy)

- App with auto theme (like MVP): light by default, dark via `@media (prefers-color-scheme: dark)`. CSS pur, no Tailwind needed.
- Vitrine site with a theme toggle (like LeCoffre, TanStack/Tailwind): dark via `:root[data-theme="dark"]` / `.dark`, plus the `tailwind.config.js`.

The template carries both, keep the one you use.

## Anti-generic rules (non negotiable)

- Commit to ONE dominant color and ONE sharp accent. Timid, evenly spread palettes read as generic. Ration the brand: a thin accent beats a full wash.
- Never the purple-on-white gradient. Never Inter/Roboto/Arial as the primary font. Never pure black, use a tuned near-black.
- Every color, space, radius, shadow goes through a token. No raw hex on text or surface.
- Bespoke SVG over stock icons, zero decorative emoji. (MVP runs a 3-tier icon system: glossy 3D for large elements, duotone gradient-sheen inline, bespoke SVG art for brand marks.)
- Keyboard accessibility is part of premium: a global `:focus-visible` ring, defined with `:where()` so components can override.
- Vary every system. Two projects must never share a palette or a type pairing. Do not default to the same fonts each time.
- Distinctive does not mean loud. Refined minimal and bold maximal both work; intentionality is the bar.

## Output checklist

- [ ] One dominant + one accent, committed, not a timid spread.
- [ ] Distinctive type pairing, self-hosted, no generic primary.
- [ ] Full token set: color (light + dark), type scale, base-8 spacing, radii, shadows, motion.
- [ ] Light and dark both resolve through tokens, both tested.
- [ ] No raw hex on text/surface, no #000, no emoji.
- [ ] Global `:focus-visible`, and a reduced-motion path (CSS and JS).
- [ ] `tokens.css` + (`tailwind.config.js`) + `CLAUDE.md` + `storybook.html` + `DESIGN_SYSTEM.md` emitted.
- [ ] Distinct from the last system produced (different palette and type).
- [ ] Run the `fluid` detector on the result.

## Database (pick from these first)

- `data/palettes.md`: 100+ committed palettes by sector and mood (dominant + accent + neutrals).
- `data/type-pairings.md`: 50+ distinctive display + body + mono pairings, never Inter primary.
- `data/styles.md`: 53 aesthetic directions with their token tendencies.
- `data/layouts.md`: 14 page-shape archetypes (bento, centered editorial, index, full-bleed, single column, broken grid, maximalist type, lineup, sidebar, poster, and more). Pick one per page, vary across pages so two never share a silhouette.
- `data/motion-presets.md`: ready-to-use motion recipes in the house easings (reveals, hovers, press, overlays, ambient).
- `data/chart-types.md`: 32 chart and data-viz types, which one answers which question, with house data-viz defaults.
- `data/tech-stacks.md`: 10 curated build stacks by project type, each wired back to the house tokens and motion.

## Reference

- `reference/rules.md`: the hard rules (locks, hero discipline, layout honesty, bans). Read before shipping.
- `reference/dna.md`: the constant house DNA.
- `reference/typography.md`: choosing a distinctive type pairing.
- `reference/color.md`: building a committed palette and the light/dark token map.
- `reference/glass.md`: liquid-glass and surface recipes (the actual CSS, plus the shimmer button and card).
- `reference/icons.md`: the 3-tier bespoke icon system, with code.
- `templates/`: `tokens.css`, `tailwind.config.js`, `CLAUDE.md`, `storybook.html`.
