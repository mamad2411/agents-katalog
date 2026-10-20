---
description: Test layers, commands, and conventions (TIMER).
globs: "**/*.test.{ts,tsx}", "**/*.spec.ts", "jest.config.*", "playwright.config.*"
alwaysApply: false
---

## Test layers

- **Unit (pure)**: `lib/`, `utils/` — no DOM, no network.
- **Integration**: Prisma + DB, API routes with mocked auth.
- **Component**: React components + user interactions (React Testing Library + jsdom).
- **E2E**: Playwright, full browser flows.

## Setup

- Jest (`jest.config.js`) for unit/integration. DB tests in `prisma/__tests__/`.
- Playwright for E2E.

## Commands

- `npm test` — Jest
- `npm run test:watch` — watch
- `npm run test:coverage` — coverage
- `npm run test:e2e:install` — install Playwright browsers
- `npm run test:e2e` — Playwright
- `npm run lint` — must be clean before merge
- `npm run build` — production build check

## Recommended targets

- Unit: `utils/compute-total-time.ts`, `lib/timer-utils.ts`
- Component: timers-list (loading/empty/error), timer-display (interval types), running-timer-view (keyboard, mute, fullscreen)
- Integration: `app/api/timers/route.ts`, `app/api/timers/[id]/route.ts`; server action ownership checks
- E2E: timer list → create → start → pause/resume → stop

## Conventions

- Do not swallow errors; assert on message and status codes.
- Use constants: `QUERY_KEYS.*` (`lib/constants/query-keys.ts`), `CUSTOM_EVENTS.*` (`lib/constants/custom-events.ts`).
