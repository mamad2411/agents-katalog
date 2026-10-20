---
name: webapp-testing-pro
description: Professional web application testing with real browser workflows, Playwright-style checks, accessibility smoke tests, responsive screenshots, API mocks, regression coverage, and QA matrices. Use for browser validation, E2E tests, UI regression checks, and release-readiness testing.
---

# Webapp Testing Pro

## Purpose

Prove that important user workflows work in a real browser.

Use with `qa-pro` for release sweeps and `frontend-design-pro` for UI state coverage.

## Workflow

1. Identify critical user path, business risk, and affected routes.
2. Choose test level: unit, component, browser workflow, visual, or release QA.
3. Prefer browser tests for integrated UI behavior.
4. Use stable selectors based on roles, labels, and visible text.
5. Control network dependencies with fixtures or mocks when appropriate.
6. Verify desktop and mobile viewports for layout-sensitive changes.
7. Capture screenshots/traces only when useful for diagnosis or regression.

## Coverage Matrix

- Navigation and auth-gated routes.
- Forms, validation, submit, retry, dirty state, and disabled state.
- Tables, filters, pagination, sorting, and empty states.
- API failures: 401, 403, 404, 409, 422, 429, 5xx.
- Accessibility smoke: keyboard path, focus, role/name queries.
- Responsive layout and text fit.
- Loading, refreshing, stale, saving, and optimistic update states.

## Rules

- Avoid arbitrary sleeps; wait on visible UI state, network state, or framework signals.
- Prefer role and label selectors over brittle CSS selectors.
- Keep E2E focused on workflows; test pure logic closer to the code.
- Make failure artifacts available when debugging UI failures.

## Output

State tested path, command, result, browser/viewport, API mock strategy, and remaining gaps.
