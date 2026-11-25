---
name: polish-ui-components
description: Design and refine polished UI components that feel premium, tactile, and production-ready. Use when Codex is building or upgrading component-heavy frontend work and needs stronger motion, design tokens, layered shadows, tactile press states, drag physics, snap behavior, reveal animations, accessibility-aware motion, prompt scaffolding, or Figma-to-code handoff discipline.
---

# Polish UI Components

## Apply the Skill

- Read `references/rules.md` before changing the component.
- Start from the visual seam the user named: motion, depth, drag feel, reveal behavior, loading state, or Figma parity.
- Keep the repo's existing design system, framework, and component APIs intact unless the user asked for a broader redesign.

## Work in This Order

1. Define the state model before styling details.
   - List the real states first: idle, hover, pressed, focused, open, loading, disabled, success, error, dragging, snapped, or whatever the component actually needs.
2. Establish tokens before adding one-off values.
   - Add or reuse motion, radius, duration, color, and shadow tokens up front.
3. Tune feel before adding decoration.
   - Fix easing, timings, drag resistance, and press response before layering on glow, blur, or flourish.
4. Use deliberate depth and entrances.
   - Prefer layered shadow stacks, hairline rings, blur-plus-rise entrances, and tactile hover or press feedback.
5. Finish with accessibility and performance checks.
   - Honor reduced motion and avoid expensive animations across large surfaces or long lists.

## Decision Rules

- Prefer exact numbers over vague adjectives when prompting or implementing motion.
- Prefer a shared token block over one-off values.
- Treat polish as state design, not just static styling.
- When iterating, change one variable at a time so motion and depth tuning stay legible.
- If a Figma selection exists, explicitly enumerate the properties to copy instead of assuming a handoff tool inferred them correctly.

## Reference Map

- Read `references/rules.md` for the motion presets, drag and snap heuristics, shadow recipes, reveal patterns, prompt templates, and Figma handoff checklist.
