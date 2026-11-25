---
name: follow-lib-mswjs-config-handlers
description: Organize MSW handlers — error simulation, passthrough, overrides and organization
argument-hint: "[scope]"
related:
  - follow-lib-mswjs
  - update-config
  - run-test
  - report
---

## Goal

Organize and extend MSW handlers to stay maintainable — domain-based organization, error/network failure simulation, passthrough patterns, per-test overrides

## Scope

- tune existing MSW handlers after setup (setup → `workflows/setup-msw`)
- covers: file organization, success/error/delay responses, `passthrough()`, `server.use()` overrides, `onUnhandledRequest` strategies
- does not cover: first-time install/scaffold

## Execute

### 1. Audit Current Handlers

> Goal: know the coverage and gaps of the existing handlers

1. read `src/mocks/handlers.ts` (or what exists) — list the already-mocked endpoints
2. compare against the real API surface — run `/report` with columns `No.`, `Endpoint`, `Method`, `Handler File`, `Covered Cases`
3. use `onUnhandledRequest: 'warn'` to find endpoints the app fires that have no handler yet

### 2. Organize By Domain

> Goal: a handler structure that can scale

1. split handlers by domain when there are many: `src/mocks/handlers/users.ts`, `orders.ts`, etc.
2. `handlers.ts` combines into a single export: `export const handlers = [...userHandlers, ...orderHandlers]`
3. move mock data/fixtures into `src/mocks/data/` — handlers shouldn't inline lots of data
4. name handler exports after the domain — `userHandlers`, not `handlers2`

### 3. Cover Response Cases

> Goal: cover success, error, delay, network failure

1. happy path: `HttpResponse.json(data)` with the status matching the contract (200/201)
2. error responses: `HttpResponse.json({ message }, { status: 400/404/500 })` — cover the statuses the app really handles
3. network failure: `HttpResponse.error()` — simulates a connection drop, not an HTTP error
4. latency: `await delay(200)` or `delay('infinite')` for pending states
5. dynamic responses: read `request`, `params`, `cookies` in the resolver — make the mock answer based on the input

### 4. Passthrough And Selective Mocking

> Goal: mock only what you want, let the rest pass through

1. use `passthrough()` from `msw` inside a resolver — intercept, then forward the real request (e.g. conditional on a header)
2. set `onUnhandledRequest` per context: `'warn'` (dev, find gaps), `'error'` (strict tests), `'bypass'` (silently pass), or a function for whitelists like analytics/sentry hosts
3. don't use `http.all('*')` as a catch-all instead of passthrough — it doesn't return a real response

### 5. Per-Test Overrides

> Goal: test-specific responses without editing base handlers

1. in a test needing special behavior → `server.use(http.get('/api/x', ...))` for a temporary override
2. `server.resetHandlers()` in `afterEach` (from setup) clears overrides automatically
3. never edit the base handlers for one test — always use `server.use()`
4. run `/deep-test api` or `/run-test` to confirm the suite passes

## Rules

- handlers must reflect the real API contract — when the API changes, update the handlers immediately
- base handlers are the happy path — do error cases via `server.use()` or dedicated error handlers
- `passthrough()` is used only inside a resolver — it doesn't create a new request
- `onUnhandledRequest: 'error'` in tests catches unmocked calls — but whitelist the real ones first
- don't inline large mock data in resolvers — keep `data/` fixtures separate

## Expected Outcome

- handlers grouped by domain with fixtures separated
- success/error/delay/network-failure cases covered
- per-test overrides via `server.use()` — base handlers stay clean
- unhandled requests are managed per context (warn/error/bypass)
