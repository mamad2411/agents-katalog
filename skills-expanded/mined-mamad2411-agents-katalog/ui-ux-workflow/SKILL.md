---
name: ui-ux-workflow
description: "Deliver UI/UX flows with explicit states, accessibility, responsiveness, and tests."
---

# UI/UX Workflow

Use this as the process skill for frontend UI work before loading framework-specific skills such as `svelte-implementation` or `svelte-review`.

## Process

1. Inspect the existing app first: similar views, base components, tokens, layout primitives, forms, tables, error states, tests, and Storybook or visual examples.
2. Clarify the user goal, roles, permissions, required data, optional data, actions, destructive paths, mobile/tablet/desktop expectations, and async states.
3. Route to focused UI skills for touched areas: design system, component architecture, view states/forms, responsiveness/media, Tailwind/tokens, accessibility/motion, performance/stability, tests/QA, and UI code review.
4. For functional work, include UI/UX requirements in the Business Plan and exact UI implementation/review skills in the Technical Plan.
5. During implementation, start from semantic HTML and existing components, then add accessibility, states, responsive layout, tokens, tests, and visual verification.
6. Before PR, self-review the UI for consistency, UX states, keyboard support, long text, responsive behavior, layout stability, performance, tests, and security-sensitive rendering.
7. For review, use `ui-code-review`; for large frontend PRs, delegate subagents by area instead of doing one broad inline pass.

## Routing Map

- UI process, planning questions, and minimum standard: `ui-ux-workflow`.
- Design tokens, base components, variants, consistency: `ui-design-system`.
- Component decomposition, container/presentational split, UI refactor: `ui-component-architecture`.
- View hierarchy, loading/empty/error, forms, tables/lists, API/cache states, optimistic UI: `ui-view-states-forms`.
- Mobile/tablet/desktop layouts, breakpoints, images, media: `ui-responsive-media`.
- Tailwind theme, tokens, variants, arbitrary values, `@apply`: `ui-tailwind-tokens`.
- Semantic HTML, keyboard, ARIA, focus, reduced motion and motion design: `ui-accessibility-motion`.
- Core Web Vitals, layout shift, expensive rendering, images, large lists: `ui-performance-stability`.
- Component/E2E/a11y/visual tests, manual QA matrix, edge cases: `ui-frontend-testing-qa`.
- UI pull request review and final verdict: `ui-code-review`.

## Before Implementation

Confirm:

- primary user goal and first thing the user should see;
- roles, permissions, readonly and permission-denied behavior;
- required, optional, partial, stale and deleted data;
- first load, background refetch, empty, validation error, server error, network error, rate limit and offline states;
- main action, destructive action, undo/confirmation, toast/inline message/redirect/cache update;
- existing matching component or pattern;
- mobile/tablet/desktop/wide desktop behavior;
- animation, skeleton, lazy loading, media and layout-stability needs.

Ask only questions that cannot be answered from existing code or patterns.

## During Implementation

- Start with semantic HTML and accessible structure.
- Reuse existing base components and tokens before adding new style.
- Add labels, accessible names, keyboard behavior, visible focus and error associations.
- Handle all data states without assuming perfect mock data.
- Reserve space for async content, images, skeletons, toasts and validation errors.
- Test long text, empty strings, many records, localization, zoom and slow API.
- Add tests for user-visible behavior, not internal component details.

## Minimum Standard For New Views

A new view should not be considered ready when it lacks:

- loading, error and empty states where data can be missing;
- mobile behavior and no-unwanted-horizontal-scroll check;
- keyboard path for primary action;
- labels and visible field errors for forms;
- stable image/skeleton dimensions;
- design tokens instead of one-off colors and spacing;
- security review for untrusted HTML or dangerous links;
- tests for the primary user behavior;
- justification for a new UI pattern.

## Developer Self-Review

Check before PR:

- existing components and tokens are used;
- long text, missing optional data and partial data do not break layout;
- main action, destructive action and feedback are clear;
- mobile, tablet, desktop and wide layouts work;
- keyboard, focus, labels and reduced motion work;
- images, fonts, skeletons and API refetch do not shift layout;
- large lists and heavy imports are controlled;
- tests cover the main behavior, errors and permission states.
