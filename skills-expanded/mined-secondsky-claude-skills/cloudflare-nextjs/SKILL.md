---
name: cloudflare-nextjs
description: "Deploy Next.js to Cloudflare Workers via the OpenNext adapter (@opennextjs/cloudflare). Use for SSR/ISR/SSG/App or Pages Router, getCloudflareContext, bindings (D1/R2/KV/AI/Hyperdrive), caching tiers, skew protection, multi-worker, custom worker, env vars, or worker size/runtime/keep_names/FinalizationRegistry/connection-scoping errors."
license: MIT
metadata:
  version: 2.0.0
  last_verified: 2026-08-05
  package_versions:
    "@opennextjs/cloudflare": "^1.18.1"
    "next": "^14.2.0 || ^15.0.0 || ^16.0.0"
    "wrangler": "^4.81.0"
  compatibility_requirements:
    compatibility_date: "2025-05-05"
    compatibility_flags: ["nodejs_compat", "global_fetch_strictly_public"]
    min_wrangler: "3.99.0"
  token_savings: "~60%"
  errors_prevented: 18+
  sources:
    overview: "https://opennext.js.org/cloudflare"
    get_started: "https://opennext.js.org/cloudflare/get-started"
    cli: "https://opennext.js.org/cloudflare/cli"
    bindings: "https://opennext.js.org/cloudflare/bindings"
    caching: "https://opennext.js.org/cloudflare/caching"
    howto_stripe: "https://opennext.js.org/cloudflare/howtos/stripeAPI"
    howto_db: "https://opennext.js.org/cloudflare/howtos/db"
    howto_dev_deploy: "https://opennext.js.org/cloudflare/howtos/dev-deploy"
    howto_env_vars: "https://opennext.js.org/cloudflare/howtos/env-vars"
    howto_image: "https://opennext.js.org/cloudflare/howtos/image"
    howto_custom_worker: "https://opennext.js.org/cloudflare/howtos/custom-worker"
    howto_keep_names: "https://opennext.js.org/cloudflare/howtos/keep_names"
    howto_workerd: "https://opennext.js.org/cloudflare/howtos/workerd"
    howto_skew: "https://opennext.js.org/cloudflare/howtos/skew"
    howto_assets: "https://opennext.js.org/cloudflare/howtos/assets"
    howto_multi_worker: "https://opennext.js.org/cloudflare/howtos/multi-worker"
    performance: "https://opennext.js.org/cloudflare/perf"
    known_issues: "https://opennext.js.org/cloudflare/known-issues"
    troubleshooting: "https://opennext.js.org/cloudflare/troubleshooting"
    migration_06_to_1: "https://opennext.js.org/cloudflare/migrate-from-0.6-to-1.0.0-beta"
    open_issues: "https://github.com/opennextjs/opennextjs-cloudflare/issues"
  keywords:
    - OpenNext Cloudflare
    - "@opennextjs/cloudflare"
    - opennextjs-cloudflare cli
    - Next.js on Workers
    - Next.js App Router Cloudflare
    - Next.js Pages Router Cloudflare
    - Next.js SSR Cloudflare
    - Next.js ISR Workers
    - server components cloudflare
    - server actions workers
    - Next.js middleware workers
    - getCloudflareContext
    - nodejs_compat
    - global_fetch_strictly_public
    - workerd runtime
    - worker size limit
    - next.js runtime compatibility
    - database connection scoping
    - R2 incremental cache
    - Durable Objects queue
    - skew protection
    - multi-worker
    - custom worker
    - keep_names
    - FinalizationRegistry
---

# OpenNext Cloudflare Adapter — Next.js on Workers

Deploy Next.js applications to **Cloudflare Workers** using the OpenNext adapter (`@opennextjs/cloudflare`). The adapter takes a standard Next.js build, runs `package.json` build script, then transforms the output to run on the Workers runtime using the Node.js compatibility layer (`nodejs_compat`) — **not** the Edge runtime.

## Critical Requirements (get these wrong and the build/runtime fails)

| Requirement | Value | Why |
|---|---|---|
| Runtime | **Node.js** (default). Remove every `export const runtime = "edge";` | Edge runtime is unsupported; OpenNext uses `nodejs_compat`. |
| `compatibility_flags` | `["nodejs_compat", "global_fetch_strictly_public"]` | Node APIs + allow `fetch()` in app code. |
| `compatibility_date` | **≥ `2024-09-23`**; **≥ `2025-05-05`** recommended (FinalizationRegistry) | Older dates break `FinalizationRegistry`, DOs, and more. |
| Wrangler | **≥ `3.99.0`** to deploy; **≥ `4.13.0`** for `keep_names`; **≥ `4.36.0`** for stable remote bindings | Feature gates in the docs. |
| Next.js | v16 all minors/patches supported; latest minors of v14 and v15; **v14 dropped Q1 2026** | Stated on the overview page. |
| Worker size (gzip) | **3 MiB Free / 10 MiB Paid** (compressed only) | Hard Cloudflare limits. |

**Windows:** not fully guaranteed (Next.js tooling issues). Use WSL, a Linux VM, or Linux/macOS CI. See known issue #1305.

## Disambiguation: this skill vs `nextjs`

- **`nextjs` skill** → framework/App Router/Server Components/Cache Components patterns, **any platform** (Vercel, self-hosted, ...). Use for `async params`, `proxy.ts` migration, `"use cache"`.
- **THIS skill (`cloudflare-nextjs`)** → deploying Next.js to **Workers** via the OpenNext adapter: `wrangler.jsonc`, `open-next.config.ts`, `getCloudflareContext`, caching tiers, bindings, skew protection, multi-worker, the Workers-specific errors.

> **proxy.ts caveat (Next 16):** Next 16 renamed `middleware.ts` → `proxy.ts`, but `@opennextjs/cloudflare` does **not** recognize `proxy.ts` yet (issue #1277) — on Cloudflare, keep using `middleware.ts`. This is the one place the `nextjs` skill's guidance does NOT apply here.

## Quick Start

### New project (recommended)

```bash
npm create cloudflare@latest -- my-next-app --framework=next --platform=workers
```

C3 scaffolds a Next.js app, installs `@opennextjs/cloudflare`, creates `wrangler.jsonc` + `open-next.config.ts` + `.dev.vars`, wires `package.json` scripts, and (if R2 is enabled) creates an R2 bucket for caching.

### Existing Next.js project (one command)

```bash
npx @opennextjs/cloudflare migrate
```

`migrate` automates: install adapter + wrangler, create `wrangler.jsonc`/`open-next.config.ts`/`.dev.vars`, update scripts, add `public/_headers`, add `.open-next` to `.gitignore`, wire `initOpenNextCloudflareForDev()` into `next.config.ts`, and create+configure an R2 cache bucket (only if R2 is enabled on the account).

<details><summary>Manual install (if you prefer not to run migrate)</summary>

```bash
npm install @opennextjs/cloudflare@latest
npm install --save-dev wrangler@latest
```

Then create the three files (see `references/wrangler.jsonc`, `references/open-next.config.ts`, `references/package.json`) and add the `dev`/`preview`/`deploy`/`upload`/`cf-typegen` scripts. **Pin adapter versions and audit before upgrading** — see the `dependency-upgrade` skill.

</details>

### The four scripts

```jsonc
// package.json
{
  "dev":     "next dev",                                                       // fast HMR via Next dev server
  "preview": "opennextjs-cloudflare build && opennextjs-cloudflare preview",   // build + run in workerd locally
  "deploy":  "opennextjs-cloudflare build && opennextjs-cloudflare deploy",    // build + serve immediately
  "upload":  "opennextjs-cloudflare build && opennextjs-cloudflare upload",    // build + upload a version (gradual rollout)
  "cf-typegen": "wrangler types --env-interface CloudflareEnv cloudflare-env.d.ts"
}
```

- `dev` — fastest feedback loop; add `initOpenNextCloudflareForDev()` to `next.config.ts` so `getCloudflareContext()` works locally with simulated/remote bindings.
- `preview` — runs in the **actual Workers runtime** (not Node). Always run before `deploy` to catch runtime-only issues.
- `deploy` — populates the **remote** cache, then `wrangler deploy`. App serves immediately.
- `upload` — populates remote cache, then `wrangler versions upload`. Does NOT serve automatically; for gradual deployments.

`build`, `preview`, `deploy`, `upload` all implicitly call `populateCache` — you do not need to run it manually.

### Dev `next.config.ts`

```ts
import type { NextConfig } from "next";
const nextConfig: NextConfig = { /* ... */ };
export default nextConfig;

import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare";
initOpenNextCloudflareForDev();
```

## Accessing Cloudflare Bindings — `getCloudflareContext()`

**Do NOT use `process.env` for bindings.** The official API is `getCloudflareContext()` from `@opennextjs/cloudflare`.

```ts
import { getCloudflareContext } from "@opennextjs/cloudflare";

export async function GET() {
  const { env, cf, ctx } = getCloudflareContext();
  await env.MY_KV.put("foo", "bar");
  return new Response(await env.MY_KV.get("foo"));
}
```

**Static routes (ISR/SSG) MUST use async mode** — and be careful: secrets/local values are used during static generation.

```ts
const { env } = await getCloudflareContext({ async: true });
```

**TypeScript types:** `npm run cf-typegen` generates `cloudflare-env.d.ts` (re-run after any binding change).

**Remote bindings (local dev → real resources):** stabilized in **Wrangler 4.36.0**. On older wrangler, enable via `initOpenNextCloudflareForDev({ experimental: { remoteBindings: true } })` and use the `experimental_remote` (not `remote`) key on binding options. Note: remote bindings are also used **during build**.

Full patterns (D1/R2/KV/AI/Hyperdrive, Drizzle, Prisma, Stripe) → `references/bindings-and-services.md`.

## Caching — three components, three tiers

OpenNext's cache has three parts: **Incremental Cache** (storage), **Queue** (dedupe/revalidate), **Tag Cache** (on-demand `revalidateTag`/`revalidatePath`).

| Site profile | Incremental | Queue | Tag Cache | When |
|---|---|---|---|---|
| **SSG only** (no revalidation) | `staticAssetsIncrementalCache` + `enableCacheInterception: true` | none | none | Fastest option; read-only |
| **Small site** (ISR/on-demand) | `r2IncrementalCache` | `doQueue` | `d1NextTagCache` | Low traffic; D1 tag cache |
| **Large/high-traffic site** | `withRegionalCache(r2IncrementalCache, { mode: "long-lived" })` | `doQueue` | `doShardedTagCache({ baseShardSize: 12 })` + `purgeCache({ type: "direct" })` | DO-sharded; add cache purge if using on-demand |

**Reserved binding names** (do not reuse): `ASSETS`, `WORKER_SELF_REFERENCE`, `NEXT_INC_CACHE_R2_BUCKET`, `NEXT_CACHE_DO_QUEUE`, `NEXT_TAG_CACHE_D1`, `NEXT_TAG_CACHE_DO_SHARDED`, `NEXT_CACHE_DO_PURGE`, `IMAGES`.

- **Avoid Workers KV** for incremental cache — eventually consistent, can persist stale data indefinitely.
- **Cache interception + PPR**: incompatible today; cache interception is NOT enabled by default and does not work with PPR.
- **On-demand revalidation** requires both a Tag Cache **and** the Cache Purge component (cache purge only works on a zone/custom domain; needs `CACHE_PURGE_API_TOKEN` + `CACHE_PURGE_ZONE_ID` secrets).
- **Pages Router** `res.revalidate` requires a self-reference service binding named `WORKER_SELF_REFERENCE`.
- **Headers caveat**: the Worker does not run in front of static assets, so `next.config.ts` `headers()` for `public/` and immutable build files do not apply. Use `public/_headers`.

Deep dive (all options, env vars, regional modes, migration from 0.6) → `references/caching.md` and `references/known-issues.md`.

## Common Integrations (condensed — full patterns in references)

- **Drizzle + D1/Hyperdrive/PG**, **Prisma + D1/PG/Hyperdrive** — request-scoped clients via `cache()` from `react`; `maxUses: 1` on PG pools; `getCloudflareContext({ async: true })` for ISR/SSG; Prisma needs `previewFeatures = ["driverAdapters"]`, no output dir in `schema.prisma`, and `serverExternalPackages: ["@prisma/client", ".prisma/client"]`. → `references/bindings-and-services.md`
- **Stripe** — Workers have no `node:https`; pass `httpClient: Stripe.createFetchHttpClient()`. → `references/bindings-and-services.md`
- **Image optimization** — `images.binding: "IMAGES"` in `wrangler.jsonc`, **or** a custom loader (`/cdn-cgi/image/...`) for zones. `minimumCacheTTL` and `dangerouslyAllowLocalIP` are not supported; custom loader bypasses middleware and ignores `remotePatterns`. → `references/advanced.md`
- **Env vars** — use Next.js `.env` files (not just `.dev.vars`); `NEXTJS_ENV` in `.dev.vars` selects the env; `--keep-vars` on deploy; secrets are write-only. → `references/dev-deploy-and-env.md`
- **Custom worker** (add `scheduled`, Durable Object exports) — point `main` at your worker that re-exports the generated fetch handler. → `references/advanced.md`
- **Multi-worker** (split middleware from server) — reduces per-worker memory + cold starts; **incompatible** with preview URLs, skew protection, and `@opennextjs/cloudflare deploy`. → `references/advanced.md`
- **Skew protection** (preview-URL-based version matching) — `cloudflare.skewProtection.enabled`, `run_worker_first: true`, `getDeploymentId()`, env vars `CF_WORKER_NAME`/`CF_PREVIEW_DOMAIN`/`CF_WORKERS_SCRIPTS_API_TOKEN`/`CF_ACCOUNT_ID`. **Disabled for Workers with a Durable Object** (move DOs to a separate worker). → `references/advanced.md`

## Top Errors (full catalog → `references/error-catalog-extended.md`)

### 1. Worker size limit exceeded
`"Your Worker exceeded the size limit of 3 MiB"` (Free) / `"10 MiB"` (Paid). Only **gzip** size counts. Free → upgrade to Paid. Paid → analyze bundle: `npx @opennextjs/cloudflare build`, then inspect `.open-next/server-functions/default/handler.mjs.meta.json` (visualize with ESBuild Bundle Analyzer); remove unused deps, use dynamic imports.

### 2. Cannot perform I/O on behalf of a different request
Global DB client (e.g. `postgres`, `pg` Pool) reused across requests. Create the client **inside** the request handler (or use `cache()` from `react`), and `maxUses: 1` for PG pools.

### 3. NPM package import / "Could not resolve \<package\>"
Enable `nodejs_compat`, ensure `compatibility_date ≥ 2024-09-23`. Some packages ship a `workerd` export — add them to `serverExternalPackages` in `next.config.ts` (e.g. `@prisma/client`, `.prisma/client`, `postgres`, `jose`, `react-textarea-autosize`, `@libsql/isomorphic-ws`). Or set `.env`: `WRANGLER_BUILD_CONDITIONS=""` + `WRANGLER_BUILD_PLATFORM="node"`.

### 4. SSRF (CVE-2025-6087) — versions < 1.3.0
`/_next/image` SSRF. Upgrade immediately: `@opennextjs/cloudflare@^1.3.0` (current: `^1.18.1`).

### 5. Failed to load chunk `server/chunks/ssr/<name>.js`
Outdated adapter with Turbopack builds. Upgrade `@opennextjs/cloudflare` to latest, or switch to webpack (`next build` without `--turbo`).

### 6. `ReferenceError: FinalizationRegistry is not defined`
`compatibility_date` too old. Set `"compatibility_date": "2025-05-05"` (or later) in `wrangler.jsonc`.

### 7. `Uncaught ReferenceError: __name is not defined`
Wrangler's esbuild `keep-names` injects `__name` into generated script strings that some libs (e.g. `next-themes`) eval at runtime. Set `"keep_names": false` in `wrangler.jsonc` (requires **Wrangler ≥ 4.13.0**). You lose original function names in debugging.

### 8. "Failed to send request to R2 worker" / 403 during `populateCache remote`
Account protected by Cloudflare Access blocks the `open-next-cache-populate` helper worker. Do **not** create a separate Access app for it; add a Service Auth policy (Include = Any Access Service Token) to the existing app covering `*.<account>.workers.dev`, create a service token, and export `CLOUDFLARE_ACCESS_CLIENT_ID` / `CLOUDFLARE_ACCESS_CLIENT_SECRET`.

## Known Open Bugs (live tracker)

Always check the issue tracker — these are recurring at the time of writing:

| # | Bug | Workaround |
|---|---|---|
| [#1171](https://github.com/opennextjs/opennextjs-cloudflare/issues/1171) | **v1.18.0 breaks R2 cache population** (pinned) | Pin to 1.17.x or upgrade past the fix |
| [#1277](https://github.com/opennextjs/opennextjs-cloudflare/issues/1277) | **`proxy.js` not supported** — Next 16 `proxy.ts` rename breaks routing | Keep `middleware.ts` on Cloudflare |
| [#1130](https://github.com/opennextjs/opennextjs-cloudflare/issues/1130) / [#1225](https://github.com/opennextjs/opennextjs-cloudflare/issues/1225) | `cacheComponents: true` crashes (`Unexpected identifier '$'` / `Connection closed`) | Disable `cacheComponents` |
| [#1321](https://github.com/opennextjs/opennextjs-cloudflare/issues/1321) | Intermittent React hydration mismatch (~9% of loads) | — |
| [#1322](https://github.com/opennextjs/opennextjs-cloudflare/issues/1322) / [#1214](https://github.com/opennextjs/opennextjs-cloudflare/issues/1214) | Hyperdrive + `pg` / `@prisma/adapter-pg` bundling failure | — |
| [#1315](https://github.com/opennextjs/opennextjs-cloudflare/issues/1315) | Time-based fetch-cache revalidation silently no-ops on Next 16 (deployed) | — |
| [#1305](https://github.com/opennextjs/opennextjs-cloudflare/issues/1305) | Windows + Turbopack routes 500 | Use Linux/macOS or webpack |
| [#1317](https://github.com/opennextjs/opennextjs-cloudflare/issues/1317) | `@cf-wasm/photon` Turbopack build fails (raw `.wasm`) | Use webpack |
| [#1326](https://github.com/opennextjs/opennextjs-cloudflare/issues/1326) | Webpack chunk inlining misses named chunks → `Unknown chunk N` | — |
| [#617](https://github.com/opennextjs/opennextjs-cloudflare/issues/617) | Node middleware (Next 15.2+) unsupported (feature request) | Use standard middleware |

Full tracker: https://github.com/opennextjs/opennextjs-cloudflare/issues

## Feature Support

| Feature | Status | Notes |
|---|---|---|
| App Router, Pages Router, Route Handlers, Dynamic routes | ✅ | Full |
| React Server Components, Server Actions | ✅ | Full |
| SSG, SSR, ISR | ✅ | Full |
| Middleware | ✅ | **Except** Node middleware (Next 15.2+, issue #617) |
| Image optimization | ✅ | Via Cloudflare Images (binding or custom loader) |
| Partial Prerendering (PPR) | ✅ | But cache interception + PPR incompatible today |
| Composable Caching (`'use cache'`), `after` | ✅ | |
| Turbopack | ✅ | But see #1305, #1317, #1326 — webpack is safer |
| Edge Runtime | ❌ | Node runtime only; remove `runtime = "edge"` |
| Node Middleware (15.2+) | ❌ | #617 |

## Related Skills

| Skill | Use for |
|---|---|
| `nextjs` | Next.js framework/App Router patterns on any platform (the `proxy.ts`/cache/Server Components reference) |
| `cloudflare-workers` | Generic Workers patterns; framework decision tree (Hono vs OpenNext) |
| `drizzle-orm-d1` | Drizzle + D1 deep dive (note: OpenNext must not bundle Wrangler — see its error catalog) |
| `cloudflare-r2` / `cloudflare-kv` / `cloudflare-d1` | Service-specific deep dives |
| `dependency-upgrade` | Pinning/auditing `@opennextjs/cloudflare` (production traffic) |

## When to Load References

| File | Load when |
|---|---|
| `references/caching.md` | Choosing/configuring incremental/queue/tag cache, regional cache, cache purge |
| `references/bindings-and-services.md` | Integrating D1/R2/KV/AI/Hyperdrive, Drizzle/Prisma request-scoped clients, Stripe |
| `references/dev-deploy-and-env.md` | Setting up dev/preview/deploy, Workers Builds CI, env vars/secrets |
| `references/advanced.md` | Custom worker, multi-worker, skew protection, static assets, keep_names, workerd packages, image optimization |
| `references/known-issues.md` | DO build warnings, migrating 0.6 → 1.0.0-beta |
| `references/error-catalog-extended.md` | Any error beyond the top 8 above |
| `references/troubleshooting.md` | Step-by-step debugging + profiling/minification |
| `references/feature-support.md` | Detailed feature compatibility matrix |
| `references/wrangler.jsonc` | Small-site and large-site wrangler templates (all reserved bindings) |
| `references/open-next.config.ts` | The three caching tiers as runnable configs |
| `references/database-client-example.ts` | Request-scoped DB client patterns |
| `references/package.json` | Reference scripts + versions |

## Sources

- Overview — https://opennext.js.org/cloudflare
- Get started — https://opennext.js.org/cloudflare/get-started
- CLI — https://opennext.js.org/cloudflare/cli
- Bindings — https://opennext.js.org/cloudflare/bindings
- Caching — https://opennext.js.org/cloudflare/caching
- How-to: Stripe — https://opennext.js.org/cloudflare/howtos/stripeAPI
- How-to: DB — https://opennext.js.org/cloudflare/howtos/db
- How-to: Dev/deploy — https://opennext.js.org/cloudflare/howtos/dev-deploy
- How-to: Env vars — https://opennext.js.org/cloudflare/howtos/env-vars
- How-to: Image — https://opennext.js.org/cloudflare/howtos/image
- How-to: Custom worker — https://opennext.js.org/cloudflare/howtos/custom-worker
- How-to: keep_names — https://opennext.js.org/cloudflare/howtos/keep_names
- How-to: workerd — https://opennext.js.org/cloudflare/howtos/workerd
- How-to: Skew protection — https://opennext.js.org/cloudflare/howtos/skew
- How-to: Assets — https://opennext.js.org/cloudflare/howtos/assets
- How-to: Multi-worker — https://opennext.js.org/cloudflare/howtos/multi-worker
- Performance — https://opennext.js.org/cloudflare/perf
- Known issues — https://opennext.js.org/cloudflare/known-issues
- Troubleshooting — https://opennext.js.org/cloudflare/troubleshooting
- Migration 0.6 → 1.0.0-beta — https://opennext.js.org/cloudflare/migrate-from-0.6-to-1.0.0-beta
- Open issues — https://github.com/opennextjs/opennextjs-cloudflare/issues

---
**Version**: `@opennextjs/cloudflare ^1.18.1` · Next.js 14/15/16 · Wrangler ≥ 3.99.0 · `compatibility_date ≥ 2025-05-05`
**Last Verified**: 2026-08-05
