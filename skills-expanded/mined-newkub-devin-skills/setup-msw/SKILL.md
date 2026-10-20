---
name: follow-lib-mswjs-setup-msw
description: Install MSW with worker (browser) and server (node) setup plus basic handlers
argument-hint: "[scope]"
related:
  - follow-lib-mswjs
  - follow-tool-vitest
  - run-test
  - deep-review-codebase
---

## Goal

First-time MSW setup so network requests can be mocked in both browser dev and Node tests — worker, server, and basic handlers

## Scope

- first-time MSW setup in a frontend or Node project
- covers: install, `msw init`, `setupWorker`/`setupServer`, entry wiring, smoke test
- does not cover: advanced handler organization (`workflows/config-handlers`)

## Execute

### 1. Check Prerequisites

> Goal: know the stack and environments that need mocking

1. run `/deep-review-codebase` — identify the HTTP client (`fetch`, `axios`, `graphql-request`) — MSW can intercept all of them at the network layer
2. identify the environments: browser dev, Node tests (Vitest/Jest), or both
3. identify the dev server's public dir (`public/` for Vite, etc.)
4. check `package.json` — if `msw` is already there (idempotent check) → skip install

### 2. Install And Init

> Goal: install MSW and scaffold the worker file

1. install with `bun add -D msw` (dev dependency)
2. if using the browser → run `bunx msw init public/ --save` — generates `mockServiceWorker.js` and records the dir in `package.json` (`msw.workerDirectory`)

### 3. Create Handlers And Entry Points

> Goal: create the handlers + worker/server entries

1. create `src/mocks/handlers.ts` — export the `handlers` array
2. write basic handlers: `http.get('/api/users', () => HttpResponse.json([...]))` for REST, `graphql.query('GetUser', ...)` for GraphQL
3. create `src/mocks/browser.ts` — `export const worker = setupWorker(...handlers)`
4. create `src/mocks/node.ts` — `export const server = setupServer(...handlers)`

### 4. Wire Browser Dev

> Goal: mocks work in the dev server (opt-in)

1. in the entry (`src/main.ts`): start the worker only in dev + with a flag such as `import.meta.env.DEV && import.meta.env.VITE_MSW`
2. `await worker.start({ onUnhandledRequest: 'bypass' })` before rendering the app — makes the bootstrap async
3. use `'warn'` instead of `'bypass'` early on to find endpoints that aren't mocked yet

### 5. Wire Node Tests

> Goal: mocks work in the test suite

1. create a test setup file: `beforeAll(() => server.listen())`, `afterEach(() => server.resetHandlers())`, `afterAll(() => server.close())`
2. point the setup file in `vitest.config.ts` → `test.setupFiles` (or the runner's equivalent)
3. run `/run-test` — tests that hit the API must pass against the mock layer

### 6. Verify

> Goal: smoke check both environments

1. dev: open the app with the flag → requests get intercepted (see the console "[MSW] Mocking enabled")
2. tests: a spec hitting a mocked endpoint passes without touching the real network
3. if verify fails → run `/resolve-errors` max 3 rounds then stop and report

## Rules

- never patch `fetch`/`axios` — use MSW interception at the network layer only
- the worker is opt-in via an env flag — never force every dev user onto mocks
- `mockServiceWorker.js` is a generated file — don't edit it by hand (refresh it by re-running `msw init`)
- `afterEach(() => server.resetHandlers())` is mandatory — tests must not leak handlers into each other
- no secrets/real tokens in handlers — mock data only

## Expected Outcome

- MSW works in both browser dev (opt-in) and Node tests
- `handlers.ts`, `browser.ts`, `node.ts` live under `src/mocks/`
- the test suite runs without depending on the real network
