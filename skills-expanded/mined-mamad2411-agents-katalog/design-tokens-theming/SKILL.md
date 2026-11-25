---
name: design-tokens-theming
description: When the agent needs to define design tokens, a theming system, CSS variables, color scales, spacing scales, or dark mode support — token architecture that keeps an entire product visually consistent.
department: Design
source: helm
---

# Design Tokens & Theming

You architect token systems like the teams behind Radix, Tailwind, and Material 3: a small set of decisions encoded once, consumed everywhere, themable without rewrites.

## Operating principles

1. **Three tiers, strictly.** Primitive tokens (raw values: `blue-600`, `space-4`) → semantic tokens (meaning: `color-accent`, `surface-raised`) → component tokens (scoped: `button-bg`) only when a component genuinely diverges. Components consume SEMANTIC tokens — never primitives directly. Theming = swapping the semantic layer only.
2. **Scales, not values.** Color: 10–12 steps per hue generated in a perceptual space (OKLCH), not eyeballed hex. Spacing: geometric-ish 4/8-base scale (4, 8, 12, 16, 24, 32, 48, 64, 96). Type: 1.2–1.25 ratio scale. Radii: 3 sizes + full. One-off values are bugs.
3. **Dark mode is a semantic remap, not an inversion.** Dark surfaces are layered by ELEVATION (darker base, lighter raised — e.g. #0a0a0b → #131316 → #1c1c21); shadows weaken, borders strengthen (white at 6–10% alpha); accent usually needs one step lighter to hold contrast.
4. **Name by role, not appearance.** `text-muted`, not `gray-500` — the whole point is that the value can change.

## Workflow

1. Inventory the UI (or planned UI): every color/space/type decision currently made ad hoc.
2. Define primitives: hue ramps in OKLCH with fixed lightness stops so cross-hue steps match perceptually.
3. Define the semantic layer — minimum viable set: `bg`, `surface`, `surface-raised`, `border`, `border-strong`, `text`, `text-muted`, `accent`, `accent-hover`, `accent-fg`, `danger`, `success`, `warning`, `focus-ring`. Map light + dark values side by side in one table.
4. Encode as CSS custom properties on `:root` and `[data-theme="dark"]` (or `@media (prefers-color-scheme)` with an override attribute). Show the exact CSS block.
5. Contrast-audit the pairs that matter: text/bg ≥ 4.5:1, text-muted/bg ≥ 4.5:1 (not 3:1 — muted text is still text), accent-fg/accent ≥ 4.5:1, focus-ring vs adjacent ≥ 3:1.
6. Document consumption rules: which tokens a new component may use, and the escalation path when none fits (add semantic token > add component token > never inline a hex).

## Output contract

Deliver: the full token table (primitive ramps + semantic map, light/dark columns) · the CSS custom-property block ready to paste · contrast audit results for the critical pairs · naming convention note · 3 worked examples (button, card, input) consuming only semantic tokens.

## Quality bar

- A theme swap touches ONE layer and zero components.
- No component in the examples references a primitive or raw hex.
- Every scale has ≤ 12 steps; if a 13th "special" value appears, the scale is wrong — fix the scale.
