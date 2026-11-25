---
name: deployment
description: Deploying to Vercel — environments, env vars, preview deployments, logs, and Next.js-on-Vercel gotchas. Use when setting up hosting, debugging a failed deploy or a prod-only bug, or managing environment variables.
---

The app deploys to Vercel via git integration: every push to a PR branch gets a preview deployment with its own URL; merging to the production branch deploys prod. Don't deploy from local machines (`vercel --prod` by hand) except in emergencies — git is the deploy trail.

## Environments and env vars

Vercel has three env scopes: **Development** (`vercel dev` / pulled locally), **Preview** (PR deployments), and **Production**. Rules:

- `NEXT_PUBLIC_*` vars are inlined into the client bundle **at build time** — changing one requires a redeploy, and it is public. Secrets (Stripe secret key, `DATABASE_URL`, AWS keys, webhook secrets) must NEVER carry the prefix.
- Preview and Production point at different databases/Stripe modes. A preview deployment writing to the prod database is the classic self-inflicted incident — check scoping when adding any var.
- Manage vars with the CLI so changes are reproducible: `vercel env add NAME preview`, `vercel env pull .env.local` to sync local dev. **Production-scoped vars, production deploys and promotions are human-only**: propose the exact command (e.g. `vercel env add NAME production`) and let the human run it, unless they explicitly approve that specific action. If the team uses Doppler, Doppler is the source of truth and syncs to Vercel — edit there, not in the Vercel dashboard.

## Day-to-day CLI

```bash
vercel ls                      # recent deployments + states
vercel inspect <url>           # build info for one deployment
vercel logs <url>              # runtime logs (function invocations)
vercel env ls                  # what's set where
vercel redeploy <url>          # rebuild without a new commit
```

The Vercel MCP (configured in this plugin) covers most of this conversationally — deployments, logs, env listings — prefer it for inspection, the CLI for mutations.

## Next.js-on-Vercel gotchas

- **Route handler duration**: serverless functions have a max duration (plan-dependent). Long work (report generation, bulk matching) belongs in a queue or background function, not a request handler. `export const maxDuration = 60` raises the cap per route where the plan allows.
- **Webhooks and body parsing**: Stripe webhook routes need the raw body — in App Router use `await request.text()` before any JSON parsing (see the stripe skill).
- **ISR/cache surprises**: `fetch` in server components caches by default in production only — a page that's live locally and stale on Vercel is usually a missing `revalidate`/`no-store`. Debug caching on a preview deployment, not localhost.
- **Region vs database region**: put the function region next to Postgres (`vercel.json` → `"regions"`), otherwise every query pays cross-region latency.
- **Build-time env**: a var referenced during `next build` (e.g. in a generated sitemap) must exist in the Vercel build env, not just at runtime.

## Debugging a prod-only failure

1. `vercel logs` (or the Vercel MCP) for the failing function — the stack trace is usually there.
2. Reproduce on a preview deployment with prod-scoped NON-secret config where possible.
3. Check env scoping diffs: `vercel env ls` — the bug is disproportionately often a var present in Development, missing in Production.
4. Sentry has the client-side half of the story; Vercel logs have the server half.
