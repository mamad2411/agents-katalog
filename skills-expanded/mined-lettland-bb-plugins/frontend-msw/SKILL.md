---
name: frontend-msw
description: Use when mocking APIs with MSW (Mock Service Worker) — REST + GraphQL handlers, node vs browser, CI integration, request matching, response composition.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [react, typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related:
    [
      react,
      typescript,
      ts-vitest,
      ts-zod,
      frontend-tanstack-query,
      frontend-feature-sliced-design,
      frontend-pwa-workbox,
      graphql-essentials,
    ]
---

# MSW (Mock Service Worker)

**Iron Law: mock at the network boundary, never at the client API. If you stub `fetch`, `axios`, or your custom `api.ts` directly, you're testing your wrapper — not what the browser sends. MSW intercepts at the SW/HTTP layer so every code path (TanStack Query retries, deduped requests, abort signals) runs unmodified.**

**Versions:** Current `MSW 2.6` — _2.x is the only supported line; v1 reached EOL early 2024. Handler API changed entirely in 2.0 (`rest.get` → `http.get`, `req/res/ctx` → `({ request }) => HttpResponse.json(...)`). Tutorials older than 2024 are wrong — verify the syntax._

## Two runtimes, one handler set

| Runtime                        | Use                                 | Setup file                                         |
| ------------------------------ | ----------------------------------- | -------------------------------------------------- |
| **Browser** (Service Worker)   | dev, Storybook, manual QA           | `src/mocks/browser.ts` → `worker.start()`          |
| **Node** (request interceptor) | Vitest, Jest, Playwright unit-style | `src/mocks/server.ts` → `server.listen()` in setup |

Handlers (`src/mocks/handlers.ts`) are shared. Both runtimes call into the same array.

```ts
// src/mocks/handlers.ts
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/reports", () => HttpResponse.json([{ id: "1", title: "Q1 inspection" }])),
  http.post("/api/reports", async ({ request }) => {
    const body = (await request.json()) as { title: string };
    return HttpResponse.json({ id: "2", ...body }, { status: 201 });
  }),
];
```

## Browser setup (dev / Storybook)

```ts
// src/mocks/browser.ts
import { setupWorker } from "msw/browser";
import { handlers } from "./handlers";
export const worker = setupWorker(...handlers);

// src/main.tsx — gate on env so prod doesn't ship the SW
async function enableMocks() {
  if (import.meta.env.MODE !== "development" || !import.meta.env.VITE_MOCK) return;
  const { worker } = await import("./mocks/browser");
  await worker.start({ onUnhandledRequest: "bypass" });
}
enableMocks().then(() => ReactDOM.createRoot(...).render(<App />));
```

Run `npx msw init public/ --save` once to copy `mockServiceWorker.js` into `public/`. Commit it. If the app already registers a Workbox SW (`Skill(frontend-pwa-workbox)`), MSW can't run in browser mode — only one SW per scope. Use node mode for tests; bypass MSW in dev when PWA mode is on.

## Node setup (Vitest)

```ts
// src/mocks/server.ts
import { setupServer } from "msw/node";
import { handlers } from "./handlers";
export const server = setupServer(...handlers);
```

```ts
// vitest.setup.ts — register in vite.config.ts `test.setupFiles`
import { afterAll, afterEach, beforeAll } from "vitest";
import { server } from "./src/mocks/server";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers()); // critical — drops per-test overrides
afterAll(() => server.close());
```

`onUnhandledRequest: "error"` makes CI fail when test code hits a URL with no handler. That's a feature — it catches accidental real-network calls.

## REST handlers

```ts
http.get("/api/reports/:id", ({ params }) => HttpResponse.json({ id: params.id })),

http.get("/api/reports", ({ request }) => {
  const status = new URL(request.url).searchParams.get("status");
  return HttpResponse.json(status === "draft" ? [] : [{ id: "1" }]);
}),

http.post("/api/reports", async ({ request }) => {
  const body = (await request.json()) as { title?: string };
  if (typeof body.title !== "string")
    return HttpResponse.json({ error: "title required" }, { status: 400 });
  return HttpResponse.json({ id: "new", ...body }, { status: 201 });
}),

http.delete("/api/reports/:id", () => new HttpResponse(null, { status: 204 })),
```

Verbs: `http.get | post | put | patch | delete | options | head | all`.

## GraphQL handlers

```ts
import { graphql, HttpResponse } from "msw";

export const gqlHandlers = [
  graphql.query("GetReports", () => HttpResponse.json({ data: { reports: [{ id: "1", title: "Q1" }] } })),
  graphql.mutation("CreateReport", ({ variables }) =>
    HttpResponse.json({ data: { createReport: { id: "2", ...variables.input } } }),
  ),
];
```

Match by operation **name**, not URL — MSW reads the operation from the body. For multiple endpoints, scope with `graphql.link("/graphql").query(...)`.

## Request matching

| Match by                    | How                                                                          |
| --------------------------- | ---------------------------------------------------------------------------- |
| URL path                    | `http.get("/api/x")` — exact path; query string ignored unless you parse it  |
| Path params                 | `http.get("/api/x/:id", ({ params }) => params.id)`                          |
| Query string                | parse from `new URL(request.url).searchParams` inside the handler            |
| Body                        | `await request.json()` / `await request.text()` / `await request.formData()` |
| Header                      | `request.headers.get("authorization")`                                       |
| Cross-origin / absolute URL | `http.get("https://api.example.com/x", ...)`                                 |

**No built-in body matcher.** Read the body inside the handler and branch. If you need pattern matching, return one response for a match and call `passthrough()` for everything else.

## Response composition

```ts
import { delay } from "msw";

HttpResponse.json(data, { status: 200, headers: { "x-trace": "abc" } });
HttpResponse.error(); // network-level error (fetch rejects)
http.get("/api/slow", async () => {
  await delay(500);
  return HttpResponse.json({});
});
```

| Goal                          | Handler shape                                                              |
| ----------------------------- | -------------------------------------------------------------------------- |
| Loading spinner               | `await delay(500)` then respond                                            |
| Error toast                   | `HttpResponse.json({ error: "..." }, { status: 500 })`                     |
| Network error (fetch rejects) | `HttpResponse.error()`                                                     |
| 401 re-auth flow              | `HttpResponse.json(..., { status: 401 })`                                  |
| Rate limit                    | `HttpResponse.json(..., { status: 429, headers: { "retry-after": "5" } })` |

## Per-test overrides

```ts
it("shows empty state", async () => {
  server.use(http.get("/api/reports", () => HttpResponse.json([])));
  render(<ReportList />);
  expect(await screen.findByText(/no reports yet/i)).toBeInTheDocument();
});

it("shows error toast on 500", async () => {
  server.use(http.get("/api/reports", () =>
    HttpResponse.json({ error: "boom" }, { status: 500 })));
  render(<ReportList />);
  expect(await screen.findByRole("alert")).toBeInTheDocument();
});
```

`server.use(...)` prepends handlers; `afterEach(() => server.resetHandlers())` drops them. Without the reset, override leaks into the next test and you debug for an hour.

## Handler organization (FSD-friendly)

```
src/mocks/
├── handlers.ts                  # combines all
├── handlers/
│   ├── reports.ts               # one file per resource
│   ├── users.ts
│   └── auth.ts
├── browser.ts
└── server.ts
```

In FSD repos (`Skill(frontend-feature-sliced-design)`), `src/mocks/` sits under `shared/api/` and handlers can pull factory functions from `entities/<x>/lib/factories.ts` to keep fixtures consistent with real types.

## Anti-patterns

- **Mocking `fetch` / `axios` / the wrapper directly.** You test your wrapper, not your app behavior. MSW intercepts the network — everything above is real.
- **Forgetting `afterEach(server.resetHandlers())`.** Per-test `server.use()` leaks. Tests start flaking weeks later.
- **`onUnhandledRequest: "bypass"` in CI.** Tests silently make real network calls and pass/fail nondeterministically. Use `"error"`.
- **Hand-writing JSON fixtures in every test.** Build factory functions in one place; share types with the real API via zod schemas (`Skill(ts-zod)`).
- **Running MSW browser mode alongside Workbox.** Single SW scope. They fight. Use node mode for tests when PWA is on.
- **Inline imports in the wrong order** — `setupServer` must be imported before any module that fires a request at top level. Vitest's `setupFiles` runs before test modules; keep network calls inside test bodies.
- **Mocking auth by URL pattern instead of header.** Brittle. Inspect `request.headers.get("authorization")`. Returning a mock shape that diverges from the real API is the same trap — generate response types from one OpenAPI/GraphQL schema both sides consume.
- **Shipping auth flows that were only tested against MSW handlers.** Mock handlers bypass real token validation, JWKS rotation, PKCE exchange, and claim-based authz — every auth code path needs a smoke test against the real OIDC provider before merge. Use MSW for UI shape; use a staging Keycloak for the actual flow.

## Red flags

| Thought                                                      | Reality                                                                               |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| "I'll just stub `axios.get`"                                 | You're testing axios. Mock the network — test your code.                              |
| "I'll set up MSW only when I need it"                        | Day one. Adding it later means rewriting every fetch-stub-based test.                 |
| "Why is this test passing in isolation but failing in suite" | `server.use` leak. Add `afterEach(server.resetHandlers())`.                           |
| "Handlers don't match — let me add `/*` to be safe"          | You just shadowed every other handler. Specific paths only.                           |
| "MSW doesn't work in my browser SW build"                    | PWA already owns the SW scope. Use node mode for tests; disable PWA in mock-dev mode. |

## Hand-off

For React Testing Library queries + user-event around MSW-mocked components: `Skill(react)`. For Vitest setup + `vitest.setup.ts` wiring: `Skill(ts-vitest)`. For shared response schemas between mocks and production: `Skill(ts-zod)`. For TanStack Query retry/abort behavior interacting with MSW responses: `Skill(frontend-tanstack-query)`. For GraphQL response shapes: `Skill(graphql-essentials)`. For mock placement in FSD repos: `Skill(frontend-feature-sliced-design)`.
