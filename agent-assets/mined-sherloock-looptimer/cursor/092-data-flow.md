---
description: Data flow, auth/validation boundaries, React Query and custom events (TIMER).
globs: "app/api/**/*.ts, actions/**/*.ts, hooks/**/*.ts, lib/constants/*.ts"
alwaysApply: false
---

## High-level flow

1. **UI** (`components/`, `app/`) calls **hooks**
2. **Hooks** (`hooks/use-timers.ts`) call **API routes** (`app/api/timers/*`)
3. **API routes** call **server actions** (`actions/timers/*`)
4. **Server actions** enforce auth + ownership and call **Prisma** (`prisma/`)

## Auth boundary

- Client is never trusted.
- Server actions: call `checkAuth()` before reading/mutating data.
- API routes: keep thin, use actions, return consistent status codes.

## Validation boundary

- Validate client inputs with Zod at boundaries: API route body parsing, server action inputs (where relevant), forms when implemented.

## Caching and invalidation

- React Query keys: `lib/constants/query-keys.ts`.
- Mutations invalidate: `QUERY_KEYS.TIMERS`, `QUERY_KEYS.TEMPLATES`, `QUERY_KEYS.SHARED_TIMERS` as appropriate.

## Custom events

- Timer running state: broadcast via `CUSTOM_EVENTS.TIMER_STATE_CHANGE` (`lib/constants/custom-events.ts`).
