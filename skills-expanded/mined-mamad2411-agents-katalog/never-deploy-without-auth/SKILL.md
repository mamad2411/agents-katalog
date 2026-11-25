---
name: never-deploy-without-auth
description: Use before deploying any new web app to production (Vercel or otherwise) — checks that authentication (GitHub SSO) and authorization (allowlist) are wired up before the deploy, not after. Triggers on "deploy", "publica esto", "conecta a Vercel", "hazlo publico", scaffolding a new app, or any time a new site is about to go live.
allowed-tools: Read, Edit, Grep, Glob
---

# Never Deploy Without Auth

A publicly reachable app with no login is an open door — anyone with the URL can read personal data (trip plans, docs, budgets, addresses). Auth is not a follow-up task, it ships in the same deploy as the first public URL.

## Rule

Before running `vercel deploy --prod` (or any first production deploy) for a new app:
1. Check whether the app already has an auth gate. If not, treat that as a blocker, not a nice-to-have — say so explicitly instead of deploying open and planning to "add auth later."
2. If the app is single-user/personal (matches the pattern of `dar-docs`, `dar-trips`, etc.), use the exact same stack already proven in `dar-docs-web`:
   - **better-auth** with `socialProviders.github`, GitHub-only sign-in (no password).
   - Postgres session storage — reuse the existing shared Postgres project in its own schema (`options: "-c search_path=<app>_auth"`) rather than provisioning a new database, unless the user asks otherwise.
   - `src/middleware.ts` with a fail-closed gate: no `ALLOWED_GITHUB_USERNAME` configured → 503, not open access. Allowlist by GitHub username (`session.user.githubUsername`), not just "any authenticated GitHub user."
   - `secureHeaders`/CSP + rate limiting via `ts-sentinel` (`chain(secureHeaders(...), withTimeout(...), maxBodyBytes(...), rateLimitGlobal(...), rateLimit(...))`), matching the CSP directives to what the app actually loads (fonts, maps, analytics) — don't just copy dar-docs-web's CSP verbatim if the app doesn't use those same external hosts.
   - `/login` page + `/api/auth/[...all].ts` catch-all route, both excluded from the auth gate along with any 2FA verification page if 2FA is added.
3. **A GitHub OAuth App has exactly one callback URL.** Each app needs its own OAuth App registration (github.com/settings/developers) — cannot reuse another app's client id/secret. Creating this is a GitHub account action outside CLI reach — ask the user to create it and hand you the client id/secret, don't try to automate around it.
4. Required env vars to request from the user (or pull from an existing sibling app's Vercel project via `vercel env pull` where reusable, e.g. `DATABASE_URL`): `DATABASE_URL`, `BETTER_AUTH_SECRET` (generate a fresh random one, don't reuse another app's), `BETTER_AUTH_URL` (the new app's production URL), `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `ALLOWED_GITHUB_USERNAME`.
5. Only deploy to production once the middleware gate is in place AND the env vars are set in Vercel — a deploy with the code present but env vars missing still fails closed (503) per rule 2, which is the safe failure mode, but confirm with the user rather than leaving it silently locked.

If the user explicitly says a specific app is meant to be public with no login (e.g. a genuinely public landing page), that overrides this skill for that app — note the exception, don't apply auth where it wasn't asked for.
