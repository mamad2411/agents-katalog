---
name: blueprint-supabase-scaffold
description: "Lay out a Vue app on the local Supabase stack, served as static files by wrangler, with tests that run against the local stack."
---

# App skeleton

One folder, one `package.json`, TypeScript throughout, `yarn`. The later checks rely on this layout exactly:

```
supabase/config.toml    yarn supabase init; project_id is the app's name
supabase/migrations/    the schema, one timestamped .sql per change (yarn supabase migration new <name>)
supabase/seed.sql       rows for trying the app locally; the security check needs one in every table
index.html              the Vue entry (<div id="app">)
src/client/             Vue 3 + Vite; src/client/supabase.ts creates the one Supabase client
vite.config.ts          writes _headers into the build (see below)
wrangler.jsonc          serves the build as static files; there is no Worker code
scripts/local-env.mjs   writes .env.development.local from the running local stack
test/                   vitest against the local stack; one file per area: data, ui, auth
```

- Dev dependencies: `supabase`, `@supabase/supabase-js`, `vite`, `@vitejs/plugin-vue`, `vue`, `typescript@^6` (not 7:
  a later check reads test files through TypeScript's compiler API, which TypeScript 7 does not ship), `vitest`,
  `wrangler`.
- The browser gets two values and no others: `VITE_SUPABASE_URL` and `VITE_SUPABASE_PUBLISHABLE_KEY` (the
  publishable key, `sb_publishable_…`). The secret key never goes into `src/` or any `VITE_` variable.
- `scripts/local-env.mjs` runs `yarn -s supabase status -o json` and writes `API_URL` and `PUBLISHABLE_KEY` to
  `.env.development.local` as those two variables.
- `vite.config.ts`: on `vite build` only, read `VITE_SUPABASE_URL` with `loadEnv` (throw if it is missing) and emit a
  `_headers` asset for every path: `Content-Security-Policy: default-src 'self'; connect-src 'self' <that URL>;
  frame-ancestors 'none'; object-src 'none'; base-uri 'self'`, `X-Content-Type-Options: nosniff`,
  `Referrer-Policy: same-origin`. The CSP has to name the Supabase URL of the build it is in, or the browser blocks
  every call; a fixed `public/_headers` cannot, because the local and the production URL differ.
- `wrangler.jsonc`: `name`, `compatibility_date` (a date the installed wrangler supports — about a month before
  today), `"assets": { "directory": "./dist", "not_found_handling": "single-page-application" }`. No `main`.
- Scripts:
  - `db:start`: `supabase start -x studio,imgproxy,logflare,vector,edge-runtime,realtime,mailpit,supavisor,postgres-meta && node scripts/local-env.mjs`
    (leave out `mailpit` from `-x` if the spec signs people in by email link)
  - `build`: `vite build --mode development` — the local build, talking to the local stack
  - `start`: `yarn -s db:start >/dev/null && yarn -s build && wrangler dev --local --ip 127.0.0.1`. The checks run
    `yarn start --port <n>`, so extra arguments must reach `wrangler dev`.
  - `test`: `vitest run`
  - `deploy`: `vite build --mode production && wrangler deploy`
- `.gitignore`: `node_modules`, `dist`, `.wrangler`, `*.local`.
- `test/local-stack.ts`: reads `yarn -s supabase status -o json`; exports an admin client made with `SECRET_KEY`
  (tests only, never the app), a signed-out client made with `PUBLISHABLE_KEY`, and `signedIn()`, which creates a
  fresh user with `auth.admin.createUser({ email, password, email_confirm: true })` and returns a client signed in as
  them. Tests never reach a hosted project.
- Add one trivial passing test in `test/` that reaches the local stack, so the harness is proven.

The checks start the local stack themselves and reset its database to the migrations and the seed before testing, so
a test may not rely on rows another test left behind.

Done when the check passes: the layout exists, `yarn db:start` starts the stack, `yarn build` and `yarn test` succeed.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
