---
name: frontend
description: Build and modify frontend pages, components, state logic, styling, forms, client-side interactions, and UI behavior in React, Vue, Svelte, vanilla HTML/CSS/JS, or similar frameworks. Use for frontend implementation and frontend bug fixes.
---

# Frontend

## Workflow

1. Read existing component, styling, routing, state, and test patterns.
2. Implement the smallest change that fits the local design system.
3. Handle loading, empty, error, retry, disabled, and permission-limited states when data or actions are involved.
4. Verify responsive behavior and text fit for likely viewport sizes.
5. Add focused tests for user-visible behavior when risk justifies it.

## Required Checks

- Use semantic HTML first; add ARIA only when native semantics are insufficient.
- Ensure keyboard reachability and visible focus for interactive controls.
- Keep state ownership clear and avoid unnecessary global state.
- Avoid hardcoded date, number, currency, and user-facing locale formatting.
- Avoid unrelated refactors, broad formatting churn, and mixing UI changes with infrastructure changes.

## React Guidance

- Follow existing project conventions for hooks and state.
- Do not add `useMemo` or `useCallback` by default.
- Keep effects for synchronization, not derived rendering state.

## Verification

Prefer existing commands: unit tests, component tests, lint, typecheck, build, and browser screenshot checks when layout matters.
