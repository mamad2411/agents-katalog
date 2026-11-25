---
name: frontend-design-engineering
description: Use for frontend, UI, web app, dashboard, landing page, component, responsive, accessibility, visual polish, or design-system work.
---

# Frontend Design Engineering

Build UI with empathy, existing systems, and rendered verification.

## Before Edits

1. Inspect the current stack and styling approach.
2. Locate tokens: CSS variables, Tailwind config, theme files, radius, shadow, duration, easing, primitives.
3. Reuse tokens before adding new ones.
4. Identify states: idle, hover, pressed, focus-visible, loading, disabled, error, success, empty/skeleton, reduced motion.
5. Check mobile and desktop paths, including separate mobile components.

## Design Brief

Name:

- Product type and audience.
- Density level.
- Visual direction.
- Anti-patterns to avoid.
- Primary workflow on the first screen.

## Interaction Rules

- No inaccessible clickable divs.
- Every keyboard control has `focus-visible`.
- Every clickable control has tactile pressed feedback.
- No `transition-all`.
- No default/generic easing.
- Reduced-motion behavior exists for every animation.
- Prefer transform/opacity over layout animation.
- Numbers in tables/metrics use tabular numerals.
- Loading state is designed, not just a generic spinner by default.

## Responsive Verification

Check at least:

- mobile width around 375px
- tablet around 768px
- desktop around 1024px+
- long content
- empty/error/loading states when relevant

Rendered UI is the verification target. Build success is not visual verification.

