---
name: blueprint-cloudflare-scaffold
description: "Lay out a Worker with D1 and static Vue assets, with tests that run inside the Workers runtime."
---

# App skeleton

One folder, one `package.json`, TypeScript throughout, `yarn`. The later checks rely on this layout exactly:

```
wrangler.jsonc          the Worker: main, compatibility_date, assets, the D1 binding "DB"
src/worker/index.ts     the Worker's fetch handler; /api/* is the API, everything else is the Vue app
migrations/             D1 migrations: numbered .sql files, applied by wrangler
index.html              the Vue entry (<div id="app">)
src/client/             Vue 3 + Vite
public/_headers         the security headers for the static files (they do not go through the Worker)
vitest.config.ts        @cloudflare/vitest-pool-workers: tests run in workerd with D1, migrations applied first
test/                   one file per area: data.test.ts, api.test.ts, ui.test.ts, auth.test.ts
```

- Dev dependencies: `wrangler`, `vite`, `@vitejs/plugin-vue`, `vue`, `typescript`, `@cloudflare/workers-types`,
  `@cloudflare/vitest-pool-workers`, and the `vitest` major that it asks for as a peer (check `yarn why` and the
  install warnings: a newer vitest than it supports fails to start).
- `typescript@^6`, not 7: a later check reads the test files through TypeScript's compiler API, which TypeScript 7
  does not ship.
- `wrangler.jsonc`:
  - `assets`: `{ "directory": "./dist/client", "not_found_handling": "single-page-application", "run_worker_first": ["/api/*"] }`
  - `d1_databases`: one entry with `"binding": "DB"`, `"migrations_dir": "migrations"`. The `database_id` is a
    placeholder until the publish step creates the real database.
  - `compatibility_date`: a date the installed wrangler's runtime supports — about a month before today. A date
    newer than the runtime refuses to start ("requires compatibility date … newest supported is …").
- Scripts:
  - `build`: `vite build` into `dist/client`
  - `start`: `wrangler d1 migrations apply DB --local && wrangler dev --local --ip 127.0.0.1`. The checks run
    `yarn start --port <n>`, so extra arguments must reach `wrangler dev`.
  - `test`: `vitest run`
  - `deploy`: `wrangler deploy`
- `GET /api/health` answers `{ "ok": true }`.
- The tests read the migrations with `readD1Migrations` and apply them in a setup file with `applyD1Migrations`, so
  every test starts from the same schema. Call the Worker through `SELF.fetch` from `cloudflare:test`.
- Add one trivial passing test in `test/` so the harness is proven.

Done when the check passes: the layout exists, `yarn build` and `yarn test` succeed.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
