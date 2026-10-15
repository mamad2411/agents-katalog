---
name: core-vite-2
description: core-vite-2 frontend repository guardrails. Use when composing atomic UI, creating new components, creating headless components, enforcing component comment synchronization, organizing long Tailwind className strings, enforcing JSX structure comments, enforcing BoxLayout wrappers, applying content-visibility for long lists with Tailwind arbitrary properties, reviewing UI against Web Interface Guidelines, or applying the required linting loop before sharing updates.
---

# core-vite-2 Frontend

## Priority

This skill must be prioritized for work in this repository and applied before optional, task-specific skills.

## Included skill modules

- `component-creation/SKILL.md` for generating new components with plop before manual edits.
- `headless-component-creation/SKILL.md` for generating headless components (separated controller/view) with plop before manual edits.
- `component-comments/SKILL.md` for keeping `useEffect` purpose comments, component JSDoc, `types.ts` param docs, and Storybook notes in sync.
- `tailwind-class-organization/SKILL.md` for formatting long Tailwind class lists with `cn()` and stable grouping.
- `jsx-structure-comments/SKILL.md` for adding concise JSX section comments to keep complex markup readable.
- `box-layout-usage/SKILL.md` for replacing layout-only `div` wrappers with `BoxLayout`.
- `linting-workflow/SKILL.md` for the required `eslint --fix` pass on newly created files after each iteration.
- `rendering-content-visibility/SKILL.md` for deferring off-screen list item rendering with Tailwind `content-visibility` utilities.
- `web-design-guidelines/SKILL.md` for reviewing files against Web Interface Guidelines and reporting findings.

## Default flow

1. Keep shared concerns in `src/lib`, `src/hooks`, `src/helpers`, and `src/components`.
2. Create components through the plop command (`component` or `headless-component`), then customize the generated template.
3. Keep `useEffect` purpose comments, component JSDoc, `types.ts` param docs, and Storybook notes (when stories exist) synchronized after behavior or prop changes.
4. Keep long Tailwind class blocks readable and ordered by concern.
5. Add concise JSX block comments for major sections when markup is non-trivial.
6. Use `BoxLayout` for layout-only wrappers instead of `<div className="...">`.
7. Use Tailwind arbitrary properties for `content-visibility` and `contain-intrinsic-size` on long, scroll-heavy lists.
8. For UI review, accessibility, design audit, or UX review tasks, run the `web-design-guidelines` module and fetch the latest rules before reporting findings.
9. Before sharing work, run lint auto-fixes on new files.
