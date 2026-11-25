---
name: web-app-development
description: Build, review, upgrade, secure, or deploy full-stack web applications and APIs. Covers MERN (MongoDB, Express, React, Node), Next.js full-stack, React/Vite SPAs with Node APIs, Django, FastAPI, and Flask, with Postgres or MongoDB. Use this skill whenever the user mentions MERN, Express, Mongoose, Next.js, React, Vite, Node, Django, FastAPI, REST API, backend, full-stack, login/auth, dashboards, CRUD apps, npm audit, CVEs or security patches, dependency upgrades, or asks which stack to choose, even if they only say "web app" or "build me a backend". Not for static marketing/landing sites or for iOS/Android apps.
---

# Web app development

Stacks covered, and when each is the default. Details in `references/stack-decision.md`.

| Situation | Default |
|---|---|
| Document-shaped data, JS team, API also serves a mobile app | MERN (TypeScript, Express 5, Mongoose, React + Vite) |
| SEO plus app in one codebase, small team | Next.js + Postgres |
| Admin panel, auth, ORM, migrations out of the box | Django + Postgres |
| API-first, async, or ML/AI-heavy backend | FastAPI + Postgres |

## Workflow

1. **Detect the stack** from the repo (`package.json` deps, `manage.py`, `pyproject.toml`). Greenfield: choose via `references/stack-decision.md` and give one recommendation with the reason.
2. **Check freshness.** Read `references/current-state.md`. Security patch levels change weekly (Next.js shipped three security releases in about ten days in Sept 2026), so for any Next.js, Express-ecosystem, or Django task always confirm the current patched version live, whatever the snapshot date says.
3. **Run `scripts/preflight.sh`** in the project root. Fix FAIL lines before other work; report WARN lines.
4. **Read the playbook** for the stack: `mern.md`, `nextjs.md`, `django.md`, or `fastapi.md`. Always read `security-baseline.md` when touching auth, uploads, database queries, or deployment.
5. **Make the smallest change.** Never combine a framework major upgrade with feature work in one commit.
6. **Verify by running it:** type-check or `manage.py check`, tests, production build, then hit the changed endpoint or page. State plainly what you did not run.

## Hard rules

- Never state a framework version or patched-version number from memory. Take it from `current-state.md` or a live source, and name the source.
- Validate every input at the boundary with a schema (zod, Pydantic, Django forms/serializers). Never trust `req.body`, `req.query`, or path params.
- Never pass request data straight into a MongoDB filter. Cast through a schema and set `sanitizeFilter` (see `mern.md`).
- Anything with a `NEXT_PUBLIC_`, `VITE_`, or `REACT_APP_` prefix ships to the browser. Never put a secret there.
- Do not write your own password hashing or session crypto. Use argon2id or bcrypt through a maintained library, and httpOnly + Secure + SameSite cookies for sessions.
- File uploads always get size and count limits, content-type verification, and storage outside the web root.
- SQL schemas change only through migrations (Alembic, Django, Drizzle/Prisma migrate). Never auto-sync schema in production.
- Pin the runtime (`.nvmrc` + `engines`, or `.python-version`) and commit the lockfile.
- After any dependency change, run the audit (`npm audit`, `pip-audit`) and report the result.

## Output style

Give exact commands and file paths. When you reject an obvious alternative, say why in one line. Separate verified facts (with source) from opinionated defaults.
