---
name: nextjs-public-env-vars
description: NEXT_PUBLIC_* are inlined into the bundle at build time — never use for secrets or per-environment values.
---

# Next.js NEXT_PUBLIC_* env vars

Inlined into bundles at `next build` by textual substitution on `process.env.NEXT_PUBLIC_FOO`. Not runtime config.

## Never `NEXT_PUBLIC_` a secret

A `NEXT_PUBLIC_`-prefixed secret is permanently baked into shipped client JS — anyone can read it from the browser; rotation is the only fix.

Reject the name if it matches `(SECRET|TOKEN|PRIVATE|SERVICE_ROLE|PASSWORD|ADMIN)`, or the value looks like `sk_*`, `eyJ` (JWT), `postgres://`, `mongodb://`, `-----BEGIN`. Use an unprefixed name instead and read it server-side. Sentry DSN is intentionally public (OK); Sentry source-map auth token is not. Internal hostnames (`*.svc.cluster.local`) leak infra topology.

This is a deterministic, safety-critical check — enforce it with a lint/CI gate (e.g. grep `NEXT_PUBLIC_` assignments against the patterns above), not prose alone.

## Access must be the literal token

Destructure, alias, computed key, and spread all silently become `undefined` in the browser:

```ts
const { NEXT_PUBLIC_FOO } = process.env;    // BAD
const k = 'NEXT_PUBLIC_X'; process.env[k];  // BAD
const e = process.env; e.NEXT_PUBLIC_FOO;   // BAD
```

T3 Env: spell out each var in `runtimeEnv` — never `runtimeEnv: process.env`.

## Cannot be injected at runtime

k8s ConfigMaps, Secrets, Helm values, and post-build Docker `ENV` are all no-ops on the browser bundle. Pass via Docker `ARG` + `ENV` in the same stage as `next build`; re-declare `ARG` in every stage that needs it.

## Different value per environment → don't use NEXT_PUBLIC_

One image cannot serve staging and prod. For per-env values (API URLs, DSNs, env names, flags), use one of:

1. Server Component reads unprefixed env, passes as prop (canonical).
2. `/api/config` route handler the client fetches once.
3. `window.__ENV` injection via `<Script strategy="beforeInteractive">` in the root layout.

## Other gotchas

- Unprefixed `process.env.X` in `'use client'` → `""` (empty string, not undefined). Falsy checks silently pass.
- `typeof window` guards do NOT prevent inlining. Use `import 'server-only'` / `'client-only'`.
- Edge runtime and middleware behave like a client bundle: unprefixed env is `undefined`.
- `publicRuntimeConfig` / `serverRuntimeConfig` — removed in Next.js v16. Never suggest.
- Tests don't auto-load `.env.local`; use `.env.test` or `loadEnvConfig` from `@next/env`.

## Examples

```ts
// BAD — secret exposed in bundle; dynamic key silently becomes undefined
const NEXT_PUBLIC_STRIPE_SECRET = process.env.NEXT_PUBLIC_STRIPE_SECRET_KEY  // exposed!
const { NEXT_PUBLIC_API_URL } = process.env  // undefined in browser

// BAD — per-environment API URL baked into the build
// .env.production: NEXT_PUBLIC_API_URL=https://api.prod.example.com
// One image cannot serve both staging and prod

// GOOD — public non-secret accessed as literal token
const apiKey = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY  // OK: intentionally public

// GOOD — per-env URL via Server Component prop (canonical pattern)
// app/layout.tsx (Server Component)
export default function Layout({ children }) {
  return <ClientShell apiUrl={process.env.API_URL}>{children}</ClientShell>
}
```
