---
name: follow-lib-mswjs
description: Set up and use MSW (Mock Service Worker) for API mocking in dev and test
argument-hint: "[scope]"
related:
  - run-test
  - implement-to-production
  - deep-review-codebase
  - report

---

## Goal

Set up and use MSW to mock network requests at the real network layer — covering dev (browser worker) and test (Node server) without patching fetch/axios

## Scope

- Use when a frontend or Node app needs mocked API responses in dev, unit tests, or integration tests
- Covers REST and GraphQL handlers, `setupWorker` (browser) and `setupServer` (Node/Vitest)
- Do not use this skill for E2E tests against a real backend → use `/follow-tool-playwright` against the real API instead
- Works with `/implement-to-production` when mocks must later become production code

- Latest stable: `msw@2.15.0` (verified 2026-09-13) — `msw@3.0.3` just released (ESM-only, requires Node 22+/TS 5.9+, `onUnhandledRequest` → `onUnhandledFrame`, GraphQL split into `msw/graphql`, no `msw/native`) — too new to pin; live-check via `/deep-research` before using v3
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### Workflows

> Goal: dispatch to the workflow matching the topic

| Topic | Workflow |
|-------|----------|
| setup | `workflows/setup-msw/SKILL.md` — install, worker/server setup, basic handlers |
| config | `workflows/config-handlers/SKILL.md` — handler organization, error simulation, passthrough |

1. If the argument matches a topic → read and follow `workflows/<name>/SKILL.md` instead of the steps below
2. Otherwise → follow the steps below as usual

### 1. Review Tech Stack

> Goal: know the stack and test runner before installing

1. Do `/deep-review-codebase`
2. Identify the environment: browser dev, Node tests, or both
3. Identify the HTTP client in use (`fetch`, `axios`, `graphql-request`) — MSW intercepts everything at the network layer

### 2. Install And Scaffold

> Goal: MSW installed and initialized correctly

1. Install `bun add -D msw` (dev dependency)
2. If using the browser → `bunx msw init public/ --save` to create `mockServiceWorker.js`
3. Create `src/mocks/handlers.ts` for request handlers
4. Create `src/mocks/browser.ts` (`setupWorker`) and `src/mocks/node.ts` (`setupServer`)

### 3. Write Handlers

> Goal: handlers cover the endpoints that need mocking

1. Use `http.get('/api/users', () => HttpResponse.json([...]))` for REST
2. Use `graphql.query('GetUser', ...)` for GraphQL
3. Write happy path, errors (4xx/5xx), network error (`HttpResponse.error()`), and delay (`await delay()`)
4. Split handlers by domain when many: `src/mocks/handlers/<domain>.ts`

### 4. Wire Dev Mode

> Goal: mocks work in browser dev

1. In the entry (`src/main.ts`): start the worker only under `import.meta.env.DEV` and an enabling flag
2. `await worker.start({ onUnhandledRequest: 'bypass' })` before rendering the app
3. Make it opt-in via env, e.g. `VITE_MSW=1` — don't force every developer onto mocks

### 5. Wire Test Mode

> Goal: mocks work in the test suite

1. In the test setup file: `beforeAll(() => server.listen())`, `afterEach(() => server.resetHandlers())`, `afterAll(() => server.close())`
2. Point the setup file in `vitest.config.ts` → `test.setupFiles`
3. For tests needing specific responses → `server.use(http.get(...))` overrides
4. Run `/run-test` to confirm tests pass with the mock layer

### 6. Report

> Goal: summarize what was set up

1. Run `/report` with columns: `No.`, `Endpoint`, `Method`, `Handler File`, `Covered Cases`
2. List endpoints still unhandled (`onUnhandledRequest: 'warn'` helps find them)

## Rules

- Never mock by patching `fetch`/`axios` — use MSW interception at the network only
- Handlers must reflect the real API contract — update handlers when the API changes
- Use `onUnhandledRequest: 'warn'` in dev to find unmocked endpoints
- Separate test overrides with `server.use()` — never edit base handlers for one test
- Don't commit a generated `mockServiceWorker.js` outside the `public/` convention

- Use /implement-to-production if needed
- Use /deep-test api if needed
- Use /report if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- MSW works in both browser dev and test environments
- Handlers cover the main endpoints with success/error cases
- Tests don't depend on the real network and are deterministic
