---
name: ui-frontend-testing-qa
description: "Plan UI component, integration, E2E, accessibility, visual, and responsive tests."
---

# UI Frontend Testing QA

Test user-visible behavior, not private implementation details.

## Process

1. Choose the smallest test level that proves the behavior: pure unit, component, integration, E2E, accessibility, visual, performance or manual QA.
2. Test interactions, validation, error messages, loading/disabled states, submit success/error, permission states, optimistic rollback, routing and focus behavior.
3. Avoid testing private functions, Tailwind class names, framework internals, cache implementation details or mock behavior that does not resemble the real API.
4. For E2E, cover critical user flows and use selectors based on roles, labels and text when stable; use `data-testid` only when no stable user-facing selector exists.
5. For visual regression, stabilize data, disable animations, freeze time/randomness, and review snapshot updates as UI changes.
6. For manual QA, cover data volume, empty/partial data, slow network, permissions, keyboard, touch, zoom, mobile/desktop and edge cases.

## Test Pyramid

Use:

- unit tests for pure functions, mappers, validators and formatting;
- component tests for base and domain components;
- integration tests for forms, cache, routing and API mocks;
- E2E tests for main user paths;
- accessibility tests for key components and views;
- visual tests for base components and high-risk screens;
- performance tests for large-data screens;
- manual QA for UX, responsiveness and hard-to-automate edge cases.

## What To Automate

- default render;
- user interactions;
- form validation;
- error messages;
- disabled/loading state;
- submit success and error;
- optimistic update and rollback;
- permission-dependent visibility;
- routing and deep links;
- modal/menu/dropdown focus management;
- visual regressions in base components.

## What Not To Test

- private functions when behavior can be tested;
- Tailwind class names unless testing visual variants;
- internal hook/store order;
- UI library implementation details;
- cache internals instead of UI effect;
- unrealistic mocks.

## E2E Rules

- Cover main flows, not every UI variant.
- Prefer selectors by role, label and text.
- Avoid random timeouts.
- Wait for user-visible state.
- Create isolated data or seed.
- Do not depend on test order.
- Treat flakiness as a test or app bug.

## Manual QA Matrix

Cover:

- desktop browsers relevant to users;
- iOS Safari and Android Chrome when mobile matters;
- viewports around 360, 390, 768, 1024, 1280 and 1440+;
- mouse, keyboard and touch;
- zoom 100, 125 and 200 percent;
- fast, slow and offline network;
- light/dark theme when present;
- longest supported locale;
- user, admin, readonly and forbidden permissions.

## Edge Cases

Use data with long text, short text, missing text, long IDs/emails/URLs, many records, zero records, one record, partial data, deleted-in-background data, expired session, double submit, rapid filter changes, browser back after mutation, refresh mid-flow, slow API, failed optimistic update and offline state.
