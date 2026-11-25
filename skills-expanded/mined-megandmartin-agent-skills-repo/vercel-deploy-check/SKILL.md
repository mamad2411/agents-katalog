---
name: vercel-deploy-check
description: Pre-deploy gate and post-deploy verification for Vercel — env vars set, build passes locally, no secrets shipped to the client, then live status, key routes, and console errors checked after. Use when the user says "deploy this", "is it safe to ship", "push to production", "the deploy broke", or "check the live site". Don't use for scanning the repo for leaked keys in git history — use env-secrets-hygiene.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Builder Dev, Vercel, Deployment, Verification]
    related_skills: [env-secrets-hygiene, api-endpoint-tester, git-ship-flow, bug-triage-protocol]
---

# Vercel Deploy Check

The gate between "works on my machine" and "live for real users." Runs a fixed pre-flight (build, env, client-bundle secrets) before anything ships, and a fixed post-flight (status codes, key routes, console errors) after — because a deploy isn't done when Vercel says "Ready", it's done when the pages actually work.

## When to Use

- Before any production deploy, especially the first one for a project.
- After a deploy, to verify the live site instead of assuming.
- When a deploy "succeeded" but the site is broken (white screen, 500s, missing env).
- **Not for:** auditing git history for leaked keys — use `env-secrets-hygiene`. Not for deep API testing — use `api-endpoint-tester`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Local prod build | `npm run build` (must exit 0 — this is the gate) |
| List env vars needed | `grep -rhoE "process\.env\.[A-Z0-9_]+" src/ app/ lib/ 2>/dev/null \| sort -u` |
| List env vars set on Vercel | `vercel env ls` |
| Secrets in client bundle? | `grep -rlE "(sk_live\|sk_test\|service_role\|-----BEGIN)" .next/static/ 2>/dev/null` (any hit = stop) |
| Deploy to preview | `vercel` (safe default — never straight to prod) |
| Promote to production | `vercel --prod` (gate behind confirm) |
| Check a live route | `curl -s -o /dev/null -w "%{http_code} %{time_total}s" https://site.com/route` |
| Instant rollback | `vercel rollback` (or Promote a previous deployment in the dashboard) |

## Procedure

### Pre-deploy

1. **Precheck** — `command -v vercel node npm`; `vercel whoami` confirms auth. `git status` clean and pushed (deploys should be reproducible from a commit).
2. **Build locally** — `npm run build`. Exit code 0 or stop; a build that fails locally fails on Vercel, just slower. Fix errors here, not in the deploy loop.
3. **Env parity** — diff the vars the code reads (grep in table) against `vercel env ls` for the target environment (Production vs Preview are separate!). Every missing var gets added: `vercel env add NAME production`. Remember `NEXT_PUBLIC_*`/`VITE_*` vars are baked in at build time — changing them later requires a redeploy.
4. **Client-secret scan** — after the local build, run the bundle grep from the table. Only publishable/anon keys belong in client code; `service_role`, `sk_live`, private keys never. Any hit: stop, move the usage server-side (API route/server component), rebuild, rescan. If the key was ever committed, run `env-secrets-hygiene`.
5. **Preview first** — `vercel` → preview URL. Click through the core flow once on preview. Success: the thing the app exists to do works there.
6. **Confirm, then production** — production deploys are user-facing; show the user what's shipping (branch, commit, env changes) and get an explicit yes before `vercel --prod`.

### Post-deploy

7. **Status sweep** — curl the key routes (home, main app page, one API route, auth page): expect 200s (or intended redirects), and note times; >3s on a simple page is a finding.
8. **Browser check** — open the prod URL, open devtools console: zero red errors is the bar. Test the core flow once as a real user, logged in and logged out.
9. **Deliver** — report via the template. If anything fails: `vercel rollback` restores the previous deployment in seconds — roll back first, debug second (`bug-triage-protocol`).

## Output Template

```
## Deploy Check — <project> @ <commit>
Pre-flight
  Build: ✅ exit 0        Env parity: ✅ (added: STRIPE_SECRET_KEY)
  Client bundle secrets: ✅ none      Preview flow: ✅ <what was tested>
Production: ✅ deployed <url>  (confirmed by user)
Post-flight
  /            → 200  0.4s
  /dashboard   → 200  0.9s
  /api/health  → 200  0.2s
  Console errors: 0
  Core flow live: ✅ <flow> works logged-in and logged-out
Rollback if needed: vercel rollback
```

## Pitfalls

- **"Ready" but white screen** — build succeeded, runtime env var missing (works locally via `.env.local`). Recovery: check Vercel runtime logs for `undefined` env reads, `vercel env add` the missing var to Production, redeploy; then add that var to the parity list permanently.
- **Env var set in Preview, not Production** — preview works, prod breaks. Recovery: `vercel env ls` and read the environment column, not just the name; mirror deliberately.
- **Secret in the client bundle** — a server key referenced in a client component ships to every visitor. Recovery: treat as leaked — rotate the key now (`env-secrets-hygiene`), move usage server-side, rebuild, rescan, redeploy.
- **`NEXT_PUBLIC_` var changed but site unchanged** — build-time vars don't update on edit. Recovery: trigger a fresh deploy after changing any public var.
- **Deploying uncommitted local state** — prod runs code that exists nowhere in git. Recovery: always deploy from a clean, pushed commit; if it already happened, commit the working tree immediately so prod is reproducible.

## Verification

- [ ] Local `npm run build` exited 0 before any deploy
- [ ] Env vars code needs ⊆ env vars set for Production (grep vs `vercel env ls`)
- [ ] Client-bundle secret grep came back empty
- [ ] Preview verified before production; user explicitly confirmed the prod deploy
- [ ] All key routes return expected status codes on the live URL
- [ ] Browser console clean on the live core flow
- [ ] Rollback command included in the report
