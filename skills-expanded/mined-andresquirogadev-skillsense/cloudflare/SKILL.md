# Cloudflare Skill

You are working with Cloudflare Workers / Pages. Apply these conventions.

## Workers

- Workers run in the V8 isolate environment — no Node.js built-ins by default; use the compatibility flag `nodejs_compat` for Node.js API support.
- Export a default object with a `fetch` handler:
  ```ts
  export default {
    async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
      return new Response('Hello');
    },
  };
  ```
- Define the `Env` interface from `wrangler.toml` bindings — never use `process.env` in Workers.

## wrangler.toml

- Define KV namespaces, R2 buckets, D1 databases, and Durable Objects as bindings in `wrangler.toml`.
- Use `[vars]` for non-secret env vars; use `wrangler secret put` for secrets.
- Use `compatibility_date` to pin the runtime behavior; update periodically.

## Cloudflare KV

- KV is eventually consistent and best for read-heavy, infrequently written data.
- Use `env.KV.put(key, value, { expirationTtl: 3600 })` for TTL-based expiry.
- Use `env.KV.getWithMetadata(key)` to retrieve value and metadata in one call.

## Cloudflare D1 (SQLite)

- Run migrations with `wrangler d1 migrations apply DB_NAME`.
- Use the D1 client: `await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(id).first()`.
- Use `.all()` for multiple rows, `.first()` for a single row, `.run()` for mutations (INSERT/UPDATE/DELETE).

## Cloudflare R2

- R2 is S3-compatible object storage with no egress fees.
- Upload: `await env.BUCKET.put(key, body, { httpMetadata: { contentType: 'image/png' } })`.
- Generate pre-signed URLs with `createPresignedUrl()` from the S3-compatible API.

## Pages

- Cloudflare Pages Functions live in `functions/` — they map to URL routes.
- Use `export const onRequestGet: PagesFunction<Env> = async (ctx) => { … }`.
- Share `Env` types between Workers and Pages Functions via a shared `bindings.d.ts`.

## Security

- Always validate `cf-connecting-ip` / `CF-Ray` headers carefully — they can be spoofed if Workers are called directly.
- Use Cloudflare Access for protecting internal routes instead of custom auth.
