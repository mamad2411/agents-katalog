---
name: follow-lib-nitro-config-storage
description: Configure Nitro storage — unstorage useStorage, drivers, route rules cache, prerender
argument-hint: "[driver]"
related:
  - follow-lib-nitro
  - run-test
  - resolve-errors
---

## Goal

Configure the Nitro storage layer — `useStorage` (unstorage) KV abstraction, drivers per deployment, `routeRules` caching, prerender

## Scope

server-side caching/storage — unstorage mounts, route rules (`cache`, `swr`, `prerender`), per-preset drivers

## Execute

### 1. useStorage Basics

```ts
const storage = useStorage()                    // default mount
await storage.setItem('key', value)
const v = await storage.getItem('key')
await storage.removeItem('key')
await storage.getKeys('prefix:')
```

- Mounts: `useStorage('cache')` / `useStorage('data')` — separate namespaces per driver

### 2. Mounts And Drivers

```ts
// nitro.config.ts
export default defineNitroConfig({
  storage: {
    cache: { driver: 'redis', url: '...' },          // or cloudflare-kv-binding
    data: { driver: 'fs', base: './.data' },
  },
})
```

- Drivers: `memory`, `fs`, `redis`, `cloudflare-kv-binding`, `vercel-kv`, `mongodb`, etc. — choose per preset/infra
- Dev default = memory/fs; production mounts follow the provider (preset `cloudflare-module` → `cloudflare-kv-binding` binds the KV namespace)

### 3. Route Rules Caching

```ts
routeRules: {
  '/api/heavy': { cache: { maxAge: 300 } },              // response cache
  '/api/live':  { swr: 60 },                             // stale-while-revalidate
  '/blog/**':   { prerender: true },                     // build-time static
}
```

- `prerender` → output lands in `.output/public/` (serve static, no worker hit)
- `isr`/`swr` keys depend on preset support (vercel/netlify/cloudflare support different ones — check the docs)

### 4. Verify

1. Cache hit: the second request is fast/doesn't enter the handler (compare with a log inside the handler)
2. `/run-test`; fail → `/resolve-errors` max 3 rounds

## Rules

- The mount name must match `useStorage('name')` — typo = silent default mount
- Use `routeRules` instead of in-handler cache whenever possible — more deterministic
- Driver selection must match the preset — the fs driver doesn't persist on serverless/edge
- Set `cache.maxAge`/`swr` according to the data's real freshness needs

## Expected Outcome

- Storage mounts + drivers match the deployment target
- Route rules caching/prerender work
