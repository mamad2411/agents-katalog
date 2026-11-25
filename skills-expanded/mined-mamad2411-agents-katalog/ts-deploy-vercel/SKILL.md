---
name: ts-deploy-vercel
description: >
  Vercel deployment for a Next.js app — project config via vercel.json, environment
  variables scoped to Development/Preview/Production, automatic preview deployments
  per PR, and the Edge vs Node.js runtime choice per route. Covers the Turborepo
  monorepo case where only the affected app should rebuild, and the secret-leak risk
  of committing env files even to a private repo.
license: Apache-2.0
metadata:
  author: ts-agent-skills
  last-updated: '2026-08-08'
  keywords:
    - Vercel
    - deployment
    - preview deployment
    - Edge runtime
    - Node.js runtime
    - environment variables
    - vercel.json
    - serverless functions
    - Turborepo
    - monorepo deploy
    - root directory
    - runtime config
    - route handler
---

## When to Use This Skill

Use when you need to:
- Configure `vercel.json` (redirects, headers, per-route function settings)
- Decide which environment an env var belongs in, or why a preview build can't see a
  production secret
- Set up preview deployments for PR review, including inside a Turborepo monorepo
- Choose Edge runtime vs Node.js runtime for a route handler or middleware

**Trigger keywords:** vercel.json, Vercel deployment, preview deployment, Edge runtime,
`export const runtime`, environment variables, Vercel env, serverless function, Vercel
monorepo, root directory, ignoreCommand, Turborepo remote cache.

**Freshness rule:** Vercel's Edge runtime API surface and `functions` config schema
change across platform releases — recheck the current Vercel docs before relying on a
specific limit (memory, duration, supported Node APIs).

---

## Recommendation First

**Node.js runtime by default. Opt into Edge only for routes that are pure request/response
logic with no Node-only dependency** — auth checks, redirects, simple API proxying,
personalization at the edge.

Why: Edge has a real, permanent API gap (no `fs`, no raw TCP, no most native Node
addons), so most database drivers (`pg`, `mysql2`, Prisma's default engine) and anything
doing heavier compute simply don't run there. Edge's win — faster cold start, runs in a
region close to the user — doesn't matter for a route that's going to block on a
database round-trip anyway.

Don't reach for Edge speculatively. Default to Node.js runtime and move a route to Edge
only when you've confirmed it doesn't need a Node-only API and the latency actually
matters.

---

## Environment Variables — Three Environments, One `.env.local`

Vercel has three environments: **Development**, **Preview**, **Production**. Each Vercel
env var is scoped to one or more of these in the dashboard (Project Settings →
Environment Variables) or via `vercel env add`.

Locally, `vercel env pull .env.local` pulls the **Development**-scoped values down into
`.env.local` — this is the file `next dev` reads, and it's the dev-machine equivalent of
whichever values are marked Development in the dashboard.

```bash
# pull dev-scoped vars into .env.local
vercel env pull .env.local

# add a var scoped to Preview + Production, not Development
vercel env add DATABASE_URL preview production
```

**Never commit a real secret, even to a private repo.** A private repo still has
collaborators, CI logs that may echo env values, and a git history that outlives any
access-list change — revoking access later doesn't erase what was already committed.
`.env.local` is git-ignored by the default Next.js `.gitignore`; keep it that way and
only commit `.env.example` with placeholder keys:

```bash
# .env.example — committed, no real values
DATABASE_URL=
STRIPE_SECRET_KEY=
```

---

## Edge vs Node.js Runtime

| | Edge | Node.js (default) |
|---|---|---|
| Cold start | Faster (V8 isolate, no container boot) | Slower (full Node process) |
| Location | Runs in the region closest to the request | Runs in your configured function region(s) |
| Node APIs | No `fs`, no raw TCP sockets, no most native addons | Full Node API surface |
| Database drivers | Only HTTP-based drivers (Neon serverless driver, PlanetScale HTTP, Prisma Accelerate) | Any driver, including raw TCP ones (`pg`, `mysql2`) |
| Max compute | Lower CPU/memory ceiling | Higher, configurable via `functions` in `vercel.json` |
| Use for | Auth/redirect middleware, geolocation personalization, simple proxying | DB queries, file access, heavy compute, most third-party SDKs |

Declaring the runtime in a route handler:

```ts
// app/api/geo/route.ts — Edge: no DB call, just reads request geo, wants low latency
export const runtime = "edge";

export function GET(request: Request) {
  const country = request.headers.get("x-vercel-ip-country") ?? "unknown";
  return Response.json({ country });
}
```

```ts
// app/api/orders/route.ts — Node.js (default, no directive needed): uses `pg`
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export async function GET() {
  const { rows } = await pool.query("SELECT * FROM orders LIMIT 50");
  return Response.json(rows);
}
```

`middleware.ts` always runs on Edge — there is no Node.js option for middleware, which is
why middleware can't use `pg` or `fs` directly; do the DB-dependent work in a route
handler it calls out to instead.

---

## `vercel.json` Essentials

```jsonc
{
  "redirects": [
    { "source": "/old-path", "destination": "/new-path", "permanent": true }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ],
  "functions": {
    "app/api/reports/route.ts": {
      "runtime": "nodejs22.x",
      "memory": 1024,
      "maxDuration": 60
    }
  }
}
```

`functions` config is per-route-file glob, not global — a heavy report-generation route
gets more memory/duration than the default without bumping every function's cost.
`runtime` here is the Node.js *version*, separate from the Edge/Node.js runtime choice
made via `export const runtime` in the route file itself.

---

## Preview Deployments and Turborepo Monorepos

Every PR gets a unique preview URL automatically — comment it on the PR, click through,
QA the actual change before merge instead of trusting the diff. No extra config needed
for a single-app repo.

In a Turborepo monorepo with multiple apps (`apps/web`, `apps/docs`, `apps/admin`), each
app is its own separate Vercel Project pointed at the same git repo, scoped with:

- **Root Directory** (Project Settings → General): set to `apps/web` for the web
  project, `apps/docs` for the docs project, etc. — this is what makes each project
  build only its own app.
- **Ignored Build Step**, using Turborepo's own change-detection so a commit that only
  touches `apps/docs` doesn't trigger a rebuild of `apps/web`:

```bash
# Project Settings → Git → Ignored Build Step, for the apps/web project
npx turbo-ignore
```

`turbo-ignore` walks the Turborepo dependency graph from the changed files and exits
0 (skip build) when nothing relevant to this project changed. Combined with Turborepo's
remote cache (see `ts-ci-github-actions`), a PR that touches one app produces one preview
deployment, not three.

---

## Common Anti-Patterns

- **Edge runtime on a route that needs a Node-only DB driver** — `export const runtime =
  "edge"` on a route importing `pg` or Prisma's default engine fails at build or throws
  at request time (`Error: The edge runtime does not support Node.js 'net' module`).
  Default to Node.js; only opt into Edge after confirming every dependency is Edge-safe.
- **Committing `.env` with real secrets** — even in a private repo. Keep secrets in
  Vercel's env var store, `.env.local` git-ignored, and only `.env.example` with empty
  placeholders committed.
- **No Root Directory set in a monorepo** — Vercel tries to build from the repo root,
  picks up the wrong `package.json`, or builds every app on every commit. Set Root
  Directory per Vercel Project to the specific `apps/*` path.
- **Skipping `turbo-ignore`** — without it, every commit to the monorepo triggers a
  rebuild of every app's Vercel Project regardless of what changed, burning build
  minutes and slowing down PR feedback.
- **Assuming Preview-scoped env vars match Production** — a Preview deployment pointed
  at a shared staging DB with different values than Production and no one noticed the
  scoping in the dashboard; check each var's environment scope explicitly, don't assume.

---

## Related Skills

- `ts-project-foundation` — the Turborepo/pnpm workspace layout this deploy config sits
  on top of
- `ts-nextjs-app-router` — the app whose routes get Edge/Node runtime and env vars
  configured here
- `ts-ci-github-actions` — Turborepo remote caching and CI checks that run before a
  deploy
- `ts-expert` — routing and build order for the full skill set

---

## Changelog

| Date | Change |
|---|---|
| 2026-08-08 | Initial version. |
