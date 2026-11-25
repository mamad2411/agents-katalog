---
name: design-build
description: "Implement or refine frontend visual design, CSS, layout, typography, color tokens, and component states. Use when creating or styling an interface."
---

# Build coherent, aesthetic, accessible frontend design

## Scope

Implement visual design decisions within the existing product requirements and design system. Use specialist guidance for the specific composition problem.

## Procedure

1. **Read before styling:** existing brand/semantic tokens, component library, themes, accessibility target, user workflows, supported locales and responsive breakpoints. Do not invent a new visual identity if one exists.
2. Choose the screen's purpose and focal point. Sketch content hierarchy and source/DOM order first. Select grouping, grid, whitespace and type roles **before** decoration.
3. Read only the specialist playbooks matching the design problem. Use `../design-diagnose/references/remediation_recipes.json` for relevant repairs; avoid loading all ten specialists. Map visual primitives to semantic roles and existing components. Prefer scoped variables, `minmax`, `clamp`, flexible measures and maintained theme tokens over hardcoded one-off values.
4. Implement complete visual states: default, hover, focus-visible, active, disabled, loading, empty, error and success, plus dark theme if supported. Color is not the only indicator; focus rings and meaningful contrast must remain clear.
5. Verify screenshot comparisons at representative content lengths, mobile/tablet/desktop, zoom, themes and loading states. Check actual task behavior with `ux-build` and accessibility with `wcag-build`. Design tokens are not a shortcut around interactive or WCAG tests.
6. Deliver a narrow component/style diff, explicit rules for reuse, and a short verification record. Avoid a giant custom design-system framework for one simple page.

## Defaults are hypotheses, not mandates

A modest modular type scale, restrained palette, consistent spacing tokens, one main accent and intentional negative space are good starting points. **Do not** enforce 60/30/10 color area, a golden ratio, one hero or two fonts as immutable constraints. Dense dashboards, localized interfaces and critical operations may demand different treatments.

Use `references/implementation-contracts.md` for CSS/token examples and state/viewport acceptance checks.
