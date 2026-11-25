---
name: design-governance
description: Use when creating or maintaining docs/DESIGN.md as the implementation-facing source of truth for UI, layout, component, accessibility, and interaction rules.
---

# Design Governance

Use this skill when a repository needs design-system guidance for implementation.

## Goal

Maintain `docs/DESIGN.md` as the source of truth for how UI should be built.

Use this skill only when the repository or request includes UI, frontend, desktop, mobile, component, visual asset, or design-system work. For script, CLI, automation, library, or docs-only repositories, do not create `docs/DESIGN.md` unless the user request or repository evidence introduces UI or visual design.

Use Clarification Gate output when available. If the audience, platform, density, layout, accessibility, or visual direction is still unclear, clarify those material gaps before writing.

## Fixed Clarification Flow

If the user has not clearly specified design direction, follow this flow before writing:

1. Discover existing signals: app screens, CSS/theme files, component libraries, screenshots, assets, design docs, and product copy.
2. Extract confirmed patterns, gaps, contradictions, and risky assumptions.
3. Ask focused questions for material gaps such as audience, density, layout, typography, accessibility, and platform constraints.
4. Draft concrete implementation rules, not abstract taste statements.
5. Cross-check with `docs/PRD.md`, `docs/BRAND.md`, and `docs/assets/*`.
6. Confirm unresolved design decisions with the user.
7. Create or patch `docs/DESIGN.md`.

## DESIGN.md Owns

- Project/profile and platform-specific rules
- Evidence and source notes
- Spacing
- Typography
- Tokens
- Layouts
- Interaction rules
- Responsive behavior
- Animation rules
- Accessibility
- Component standards
- Component reuse rules
- Component pattern registry
- Prohibited implementation patterns

## Component Pattern Governance

When UI work introduces or changes a component, enforce this flow:

1. Check `docs/DESIGN.md` and the existing component directory before creating a new component.
2. Reuse or extend an existing component when it covers roughly 70-80% of the needed behavior.
3. Create a new component only when reuse would make the existing component unclear, brittle, or over-generalized.
4. If the new component is reusable across screens, update the `Component Patterns` section in `docs/DESIGN.md` during the same change.
5. If the new component is intentionally one-off, record why in the related spec or plan instead of adding it to `docs/DESIGN.md`.

`Component Patterns` entries should be concrete enough for future agents to reuse without reading the component implementation first:

- Use when
- Do not use when
- Reuse path
- Variants
- Accessibility or interaction notes

Do not add every component to `docs/DESIGN.md`. Only document stable reusable patterns or important prohibitions.

## Boundary

Do not merge `docs/DESIGN.md` with `docs/BRAND.md`.

`DESIGN.md` governs UI implementation, engineering constraints, component systems, layout rules, and interaction behavior.

`BRAND.md` governs identity, storytelling, naming, tone, and communication style.

Cross-reference them when useful, but keep the source-of-truth boundary clear.

## Rules

- Detect an existing design system before writing defaults.
- Patch existing design docs instead of replacing them.
- Prefer concrete implementation rules over abstract taste statements.
- Tailor the design guide to the detected platform; do not put web-specific design-system rules into iOS, desktop, CLI, library, or docs-only projects.
- Reference `docs/assets/` when visuals, screenshots, or brand assets are needed.
- Do not invent a visual system when repository evidence and user intent are insufficient.
- Before adding UI components, search for reusable local components and documented patterns.
- Keep `docs/DESIGN.md` aligned when a reusable component pattern becomes part of the system.
