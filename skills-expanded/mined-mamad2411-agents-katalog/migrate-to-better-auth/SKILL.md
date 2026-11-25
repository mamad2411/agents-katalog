---
name: migrate-to-better-auth
description: Migrate any existing authentication system (NextAuth, Passport, Lucia, Clerk, custom JWT, session-based) to better-auth. Detects the current auth setup, prompts the user to select better-auth features/plugins, generates a phased migration plan, rewrites auth config and routes, and refactors seed data. Use when user wants to switch to better-auth, replace an existing auth library, or mentions NextAuth migration, Lucia, Passport, Clerk, or custom auth refactor.
---

# Migrate to Better-Auth

Migrate any auth system to [better-auth](https://better-auth.com) incrementally. Never rewrite everything at once — plan first, execute one phase at a time.

> **Depends on**: `better-auth/skills` for setup patterns (`npx skills add better-auth/skills`). This skill handles the *migration* layer on top.

## Quick Start

1. Audit the existing auth setup.
2. Prompt the user to select better-auth features.
3. Generate a migration plan via `/refactor-codebase`.
4. Execute phases: schema → server config → routes → client → seed data.

## Workflow

### 1. Audit existing auth

Identify: auth library, auth methods, DB schema (tables + column names + types), ORM/adapter, seed files, and framework. Summarize to the user before proceeding.

### 2. Prompt user to select features

Present this checklist and ask for confirmation:

```
Auth methods: email/password, OAuth (which providers?), magic link, passkeys, phone/OTP, anonymous
Plugins:      2FA, organization/multi-tenant, admin roles, API keys, SSO/OIDC, JWT, HIBP breach detection
Session:      database-backed (default) | Redis-backed
```

### 3. Map old schema → better-auth schema

Produce a field mapping table before touching code. Flag breaking type changes — especially `emailVerified` Date → boolean. See [REFERENCE.md](REFERENCE.md) for mappings by source library.

### 4. Generate the migration plan

Invoke `/refactor-codebase` with a Refactor PRD covering: current library + schema, target better-auth config, the mapping table, and seed files. Standard phases:

1. Install & scaffold — `better-auth`, schema generation, env vars
2. Schema migration — alter DB tables
3. Server config — write `auth.ts` with confirmed features/plugins
4. Route handlers — replace old routes with `auth.handler`
5. Client — replace session hooks with `authClient`
6. Seed data — update fixtures (step 5)
7. Cleanup — remove old auth library

### 5. Refactor seed data

If seed files exist, invoke `/refactor-codebase` scoped to those files: rename columns, coerce `emailVerified` to boolean, add required fields (`createdAt`, `updatedAt`, `accountId`, `providerId`). Keep data behavior identical — no new users or roles unless asked.

### 6. Verify after each phase

```bash
npx tsc --noEmit && npm test
curl -X POST http://localhost:3000/api/auth/sign-in/email \
  -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"password"}'
```

Report results before starting the next phase.

## Guardrails

- Do not remove the old auth library until all phases pass verification.
- Never silently cast `emailVerified` Date → boolean — write an explicit migration script.
- Flag missing OAuth env vars before starting; do not proceed until user confirms.
- If no auth tests exist, recommend a smoke test as Phase 0.

## References

- [REFERENCE.md](REFERENCE.md) — schema mappings per library, ORM adapter snippets, seed before/after examples, env var checklist.
- `better-auth/skills` — framework setup (`npx skills add better-auth/skills`).
