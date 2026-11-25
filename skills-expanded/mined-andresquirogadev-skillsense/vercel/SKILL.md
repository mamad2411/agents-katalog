# Vercel Skill

You are deploying to Vercel. Apply these conventions.

## Deployment

- Connect the GitHub repo to Vercel — every push to `main` deploys to production; every PR creates a preview deployment.
- Use `vercel.json` only for rewrites, redirects, headers, and cron jobs — avoid overriding build settings that Vercel auto-detects.
- Set environment variables in the Vercel dashboard per environment (Production / Preview / Development); use Vercel CLI (`vercel env pull`) to sync to `.env.local`.

## Edge vs Serverless Functions

- Choose the runtime per route with `export const runtime = 'edge'` or `'nodejs'`.
- Edge runtime: ultra-low latency, globally distributed, but limited Node.js APIs (no `fs`, limited `crypto`).
- Node.js runtime: full Node.js APIs, longer cold start — use for DB connections, file I/O.
- Connect to databases from the Edge with connection-pooled drivers (`@neondatabase/serverless`, Supabase edge client).

## Environment Variables

- Access env vars with `process.env.VAR_NAME` — Vercel injects them at build time (public vars) and at runtime (secret vars).
- Use `NEXT_PUBLIC_` prefix for client-side accessible variables in Next.js.
- Never commit `.env` files; use `.env.local` for local development (gitignored).

## Image Optimization

- Vercel's Image Optimization runs `next/image` optimizations automatically — set `domains` or `remotePatterns` in `next.config.ts` for external image hosts.
- Cache optimized images at the CDN edge by setting an aggressive `Cache-Control` header on image routes.

## Cron Jobs

```json
// vercel.json
{
  "crons": [{ "path": "/api/cron/cleanup", "schedule": "0 2 * * *" }]
}
```
- Protect cron routes by verifying `Authorization: Bearer ${CRON_SECRET}` header.

## Performance

- Use Vercel's Analytics (`@vercel/analytics`) and Speed Insights (`@vercel/speed-insights`) for Core Web Vitals monitoring.
- Enable ISR (Incremental Static Regeneration) on Next.js pages with `revalidate` to cache at the CDN.
- Use Vercel KV (Redis), Vercel Postgres, or Vercel Blob for serverless-compatible storage.
