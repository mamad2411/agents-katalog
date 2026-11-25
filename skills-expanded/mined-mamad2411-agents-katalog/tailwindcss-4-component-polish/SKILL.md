---
name: tailwindcss-4-component-polish
description: Improves Tailwind CSS 4 component presentation without changing business logic. Use for visual polish, spacing and typography consistency, layout refinement, accessible focus/error/success states, and responsive UI improvements.
license: MIT
---

# Tailwind CSS 4 Component Polish Skill

Use this skill when the task is to improve UI quality without changing product behavior or business logic.

## When to Use

- The user asks for UI polish, cleanup, design consistency, or a more professional look.
- A component needs better spacing, typography, layout, responsive behavior, or visual hierarchy.
- Error, success, disabled, selected, loading, or focus states need accessible styling.
- A Tailwind class block is hard to read or repeats across related UI.
- A component should align with existing design tokens or shared UI primitives.

## Boundaries

- Do not change data flow, validation rules, API behavior, routing, persistence, authorization, or feature logic.
- Do not introduce a component library, class sorting tool, or design-token system unless the project already uses it or the user explicitly asks.
- Prefer small, reviewable UI-only changes.
- Preserve existing framework and component conventions.

## Workflows

- `workflows/component-polish-workflow.md`: use for UI polish that must not change logic.
- `workflows/design-consistency-review-workflow.md`: use for spacing, typography, alignment, rhythm, and layout consistency review.
- `workflows/accessible-state-styles-workflow.md`: use when styling focus, error, success, warning, selected, disabled, or loading states.

## Resources

- `resources/component-polish-checklist.md`: practical checklist for UI polish reviews.
- `resources/state-style-patterns.md`: accessible state styling patterns.

## Examples

- `examples/component-polish-before-after.md`: safe component polish example.
- `examples/accessible-state-styles.example.md`: accessible validation and focus-state example.

## Operating Guidance

1. Inspect existing components and tokens before editing.
2. Identify whether the change is visual-only or logic-affecting.
3. Use existing primitives and tokens when available.
4. Improve class readability while preserving behavior.
5. Verify responsive, keyboard, and state behavior.
6. Summarize exactly what changed visually and what logic was intentionally left untouched.
