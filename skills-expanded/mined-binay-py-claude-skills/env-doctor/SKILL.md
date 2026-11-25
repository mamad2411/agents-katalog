---
name: env-doctor
description: Check a project's environment variables against its code — variables the code reads that .env.example doesn't document, stale keys nothing reads, keys unset in .env/.env.local (undefined at runtime), secrets exposed to the browser through VITE_/NEXT_PUBLIC_/REACT_APP_-style prefixes, real-looking keys inside .env.example, and .env files committed to git or missing from .gitignore. Never prints values. Use for "works on my machine" bugs, onboarding a repo, before open-sourcing or deploying, or when a variable is undefined.
---

# env-doctor

`scripts/env-doctor.mjs` is zero-dependency Node 22+ and read-only unless `--fix-example`.

```
node env-doctor.mjs [project-dir]
node env-doctor.mjs . --fix-example     # append missing keys (empty) to .env.example, backup kept
```

It finds variable reads in JS/TS (`process.env.X`, `process.env["X"]`, destructuring, `import.meta.env.X`, `Deno.env.get`, `Bun.env`), Python (`os.environ[...]`, `.get`, `os.getenv`), Ruby, Go, PHP, Rust, and `${X}` in shell scripts, Dockerfiles and docker-compose. In Cloudflare Workers projects (a `wrangler.toml/json/jsonc` or `.dev.vars`) it also reads `env.X` and treats `.dev.vars` as the local env file, ignoring names the wrangler config declares as bindings or `[vars]`. It skips `node_modules`, build output and virtualenvs, and ignores standard runtime variables (NODE_ENV, PORT, HOME, CI…).

| Severity | Finding |
|---|---|
| high | a secret-named variable with a **browser-exposed prefix** (`VITE_SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_STRIPE_SECRET`): it ships in the JS bundle. Publishable/anon/site keys are allowed |
| high | a real-looking key or credentialed URL in `.env.example` (localhost/`user:pass` placeholders are fine) |
| high | `.env` / `.env.local` committed to git, or present in git history |
| medium | variables used in code but missing from `.env.example`, or no example file at all |
| medium | variables used in code but not set in any local env file; an env file not in `.gitignore` |
| low | example keys no code reads (or that only a framework config reads); keys set but empty |

## Acting on it
- Browser-exposed secret: move the call server-side (API route, edge function), drop the public prefix, and **rotate the key**, because it's already in every shipped bundle.
- Committed `.env`: `git rm --cached .env`, add it to `.gitignore`, rotate everything in it. History keeps the old values.
- After `--fix-example`, give each new key a placeholder and a one-line comment saying where to get it.

## Limits
Static scan: dynamic names (`process.env[name]`) and variables read only by tools or framework config files (e.g. `DATABASE_URL` read by Prisma's schema) aren't seen, which is why "stale" is only low severity. Hosted env (Vercel/Cloudflare dashboards) isn't checked.
