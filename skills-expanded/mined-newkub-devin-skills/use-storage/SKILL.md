---
name: follow-service-cloudflare-use-storage
description: Use Cloudflare KV and R2 — namespaces, caching patterns, object storage, presigned uploads
argument-hint: "[binding]"
related:
  - follow-service-cloudflare
  - run-test
  - resolve-errors
---

## Goal

Use KV and R2 for the right case — KV = small, read-heavy key-value (global cache); R2 = object storage (files/media/large payloads)

## Scope

The storage layer of Workers — pick correctly: KV (~64KB-25MB values, eventual consistency ~60s), R2 (objects, S3-compatible), Cache API (per-colo HTTP cache); bindings → `config-bindings`, details in `references/bindings.md`

## Execute

### 1. Provision And Bind

```bash
wrangler kv namespace create CACHE
wrangler r2 bucket create my-bucket
```

`wrangler.jsonc`: `kv_namespaces: [{ binding: "CACHE", id }]`, `r2_buckets: [{ binding: "BUCKET", bucket_name }]` → `wrangler types`

### 2. KV Patterns

> Goal: Use KV per its strengths/weaknesses

```ts
await env.CACHE.put('key', value, { expirationTtl: 3600 })
const cached = await env.CACHE.get('key', { type: 'json' })   // 'text'|'json'|'arrayBuffer'|'stream'
await env.CACHE.delete('key')
await env.CACHE.list({ prefix: 'user:' })
```

- Good for: config, sessions, feature flags, cache — not good for: data needing immediate consistency (eventual ~60s), high-write data
- metadata: `put(key, val, { metadata })` + `getWithMetadata` — e.g. content-type/tags

### 3. R2 Patterns

> Goal: object storage operations

```ts
await env.BUCKET.put(key, body, { httpMetadata: { contentType }, customMetadata })
const obj = await env.BUCKET.get(key)          // obj.body stream, obj.writeHttpMetadata(headers)
for await (const chunk of obj.body) { /* stream */ }
await env.BUCKET.delete(key)
await env.BUCKET.list({ prefix, limit, cursor })
```

- Multipart upload for large files (`createMultipartUpload`)
- Range reads: `get(key, { range })` — partial content
- Serving files: return `new Response(obj.body, { headers })` + `writeHttpMetadata`

### 4. Cache API (optional)

- `caches.default` — per-colo HTTP cache for Response objects; good for hot paths that don't need global consistency

### 5. Verify

1. `wrangler dev` with a real put/get/delete round trip (local = miniflare-backed)
2. `/run-test`; fail → `/resolve-errors`

## Rules

- Never use KV as the source of truth — cache/derived data only
- Design R2 keys as paths (`users/{id}/avatar.png`) so `list` by prefix works
- Use separate bindings per env (staging/production)
- Use ETag/conditional requests on R2 GET to save bandwidth

## Expected Outcome

- KV/R2 bound and round-trips working both locally and remotely
- Storage choice matches the use case + consistency requirements
