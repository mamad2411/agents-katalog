---
name: json-server
description: json-server standards — db.json, routes.json, custom middleware, and CI usage. Load when working with json-server.
user-invocable: false
stack: mocking/json-server
paths:
  - "**/db.json"
  - "**/routes.json"
  - "**/json-server/**"
  - "**/__mocks__/**"
---

Full standards in [json-server.md](json-server.md). Always-on summary:

> **Scope — applies only if this project uses json-server.** This layer shares `**/__mocks__/**` with `mirage` in `layers/mocking/`, so more than one may load at once and their rules conflict. If the project is not using json-server, ignore this layer.
> See `docs/adr/0001-layer-glob-collision-and-dispatcher-routing-policy.md`.

**db.json:**
- Each top-level key becomes a REST resource: `GET /users`, `POST /users`, `DELETE /users/:id`
- Always include an `id` field — json-server uses it for relationship resolution and updates
- Seed data should be realistic and cover edge cases (empty lists, long strings, boundary values)

**routes.json:**
- Use `routes.json` to rewrite paths: `{ "/api/*": "/$1" }` strips the `/api` prefix
- Keep rewrites minimal — complex logic belongs in custom middleware, not route rewrites

**Custom middleware:**
- Add delays: `json-server --middlewares delay.js` with `res.header('X-Response-Time', ...)`
- Simulate auth: check `req.headers.authorization` in middleware; return 401 if missing
- Add custom endpoints that db.json cannot express (aggregations, computed fields)

**CI usage:**
- Start json-server before tests: `json-server --watch db.json --port 3001 &`
- Use `--delay 300` to catch loading states; use `--delay 0` for speed in unit tests
- Reset db.json between test suites — copy from a fixture file, not in-place mutation

**Never:**
- Use json-server as a production backend — it is a dev/test tool only
- Commit a mutated db.json — the file is rewritten on POST/PUT/DELETE; gitignore or restore in CI
- Put sensitive data in db.json — it is served as plain JSON with no auth by default

**Related skills:** `mocking/mirage` (in-process alternative), `mocking/msw` (service-worker mocking), `testing/playwright`
