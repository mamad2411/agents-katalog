---
name: blueprint-local-scaffold
description: "Create the app skeleton: Express API, SQLite through node:sqlite, a Vue screen, and the test harness, following the layout the later checks rely on."
---

# App skeleton

One folder, one `package.json`, TypeScript throughout, `yarn`. The later checks rely on this layout exactly:

```
server/index.ts      Express app; listens on PORT (default 3000) and HOST (default 127.0.0.1)
server/db.ts         opens data/app.db with node:sqlite (DatabaseSync); runs migrations on start
server/migrations/   numbered .sql files, applied in order, recorded in a schema_migrations table
client/              Vite + Vue 3 app (index.html has <div id="app">)
test/                vitest; one file per area: data.test.ts, api.test.ts, ui.test.ts, auth.test.ts
data/                the database file lives here; data/*.db is in .gitignore
```

- `typescript@^6`, not 7: a later check reads the test files through TypeScript's compiler API, which TypeScript 7
  does not ship.
- Scripts: `dev` (server + vite together), `build` (vite build to dist/client and the server with tsc or tsup to
  dist/server), `start` (runs the BUILT server: `node dist/server/index.js`), `test` (`vitest run`).
- Under `yarn dev`, Vite forwards `/api` to the server. Write the proxy as an object with `changeOrigin: false`
  (`"/api": { target: "http://127.0.0.1:3000", changeOrigin: false }`), never as a plain string: a string makes Vite
  rewrite the `Host` to the server's port, and the API, which refuses a change whose `Origin` is not its own `Host`,
  then refuses every change made in development. The check loads the Vite config and says so.
- `GET /api/health` answers `{ "ok": true }`. In production the server serves `dist/client` and falls back to
  `index.html` for screen routes.
- The server exports a function that builds the app for a given database path, so tests run against a
  temporary database, never `data/app.db`.
- Add one trivial passing test in `test/` so the harness is proven.

Done when the check passes: the layout exists, `yarn build` and `yarn test` succeed.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
