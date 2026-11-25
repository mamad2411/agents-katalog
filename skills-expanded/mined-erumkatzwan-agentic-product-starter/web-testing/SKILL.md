---
name: web-testing
description: Use when writing or fixing unit tests (Vitest) or end-to-end tests (Playwright) in the Web app, or when one of its checks is red.
---

# Web testing

| Layer | Where | Runs against | Command |
|---|---|---|---|
| Unit | `src/**/*.test.ts(x)` | A fake API (`src/test/fakeApi.ts`) | `npm run test:coverage` |
| End-to-end | `e2e/*.spec.ts` | The real backend in SYST + the built app | `npm run e2e` |

## Rules

- Test behaviour the user sees: find elements by role and label (`getByRole`, `getByLabelText`), not CSS classes.
- Unit tests render `<App api={fakeApi(...)} />` and override only the calls the test needs.
- End-to-end tests use the seeded accounts or create their own data with unique emails, and clean up after themselves.
- Coverage must stay at or above 70% of lines.

## When a check is red

- Lint or types: run `npm run lint` and `npm run typecheck`.
- Unit tests: run `npm test`.
- End-to-end: run `npm run e2e` locally; in CI, download the Playwright report artifact.
