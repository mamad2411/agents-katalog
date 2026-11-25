---
name: follow-lib-better-auth
description: Use Better Auth for authentication and authorization
argument-hint: "[scope]"
related:
  - deep-review-codebase
  - follow-lib-jose
  - follow-lib-simplewebauthn
---

## Goal

Set up the latest Better Auth for type-safe authentication and authorization in TypeScript projects

## Scope

Works with Next.js, Nuxt, SvelteKit, SolidStart, Hono, Elysia, TanStack Start, Express, Cloudflare Workers, Expo, or any TypeScript-capable backend

Boundaries:
- Use this skill when a full auth framework is needed (sessions, providers, plugins, adapters)
- For JWT sign/verify only → use `/follow-lib-jose` instead
- For WebAuthn/passkeys without an auth framework → use `/follow-lib-simplewebauthn` instead
- To review existing auth design/security → use `/deep-review-codebase`

- Latest: `better-auth@1.7.5` (verified 2026-09-16)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Setup | `workflows/setup-auth/SKILL.md` — install, `auth.ts`, database adapter | Providers | `workflows/config-providers/SKILL.md` — social/email plugins config 
### 1. Install

> Goal: install Better Auth and a database adapter

1. Run `bun add better-auth` (or `pnpm add better-auth` per the project's package manager)
2. Check the latest version at `https://www.npmjs.com/package/better-auth` (currently v1.7.4, verified 2026-09-16)
3. Install a database adapter if not using the built-in Kysely (e.g. `@better-auth/prisma-adapter`, `@better-auth/drizzle-adapter`)
4. Set the `BETTER_AUTH_SECRET` and `BETTER_AUTH_URL` environment variables
5. Use `bunx auth@latest init` to scaffold a Next.js project (optional)

### 2. Configure

> Goal: create the auth config with plugins and session settings

1. Create `auth.ts` using `betterAuth()` and export it as `auth` or as the default export
2. Provide the database directly (e.g. `new Database('./sqlite.db')`, `new Pool({...})`) or through an adapter
3. Enable features such as `emailAndPassword: { enabled: true }` or `socialProviders`
4. Add the needed plugins in `plugins: [...]` (e.g. `twoFactor()`, `organization()`, `passkey()`)
5. Set `trustedOrigins` strictly
6. Use `bunx auth@latest generate` for the schema, or `bunx auth@latest migrate` with the built-in Kysely adapter

### 3. Integrate

> Goal: wire auth into the frontend and backend routes

1. Create the API route for the auth handler per framework (e.g. `toNextJsHandler(auth)`, `toElysiaHandler(auth)`, mount `/api/auth/*`)
2. Use `createAuthClient` from `better-auth/react` (or `/vue`, `/svelte`, `/solid`, `/client`) in the frontend
3. Use `authClient.signIn.email()`, `authClient.signUp.email()`, `authClient.signOut()`, and `authClient.useSession()`
4. Handle roles/permissions via plugins such as `admin` or `organization`

### 4. Secure

> Goal: keep the auth flow secure

1. Use an environment variable for `BETTER_AUTH_SECRET` — at least 32 high-entropy characters
2. Define `trustedOrigins` strictly
3. Never expose admin or debug endpoints unnecessarily
4. Use `https` in production

### 5. Test

> Goal: test auth flows and protected routes

1. Test sign in / sign up
2. Test protected routes
3. Verify session refresh
4. Test social providers if enabled

## Rules

### 1. Security

- Use environment variables for secrets
- Define `trustedOrigins` strictly
- Do not expose admin endpoints unnecessarily
- Use HTTPS in production

### 2. Type Safety

- Use the type-safe client (`better-auth/react`, `/vue`, `/svelte`, `/solid`, `/client`)
- Define session options correctly

### 3. Database

- Pick the adapter matching the project's ORM
- Run `bunx auth@latest generate` or `bunx auth@latest migrate` before testing

### 4. Framework Integration

- Use the handler prepared by the framework when one exists
- Always mount the auth handler at the same base path

### 5. Plugins

- Enable only the necessary plugins
- Install the client plugin counterpart when a plugin requires it (e.g. `twoFactorClient`)

### 6. Upgrade

- Upgrade `better-auth` and `@better-auth/*` together
- Read the migration guide before a major upgrade (e.g. v1.7 has breaking changes for OAuth, MCP, SCIM)
- Use /deep-review-codebase if needed
- Use /follow-lib-jose if needed
- Use /follow-lib-simplewebauthn if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Auth flows work correctly
- Type-safe end to end
- Session security passes
- Database schema matches the Better Auth config
- Protected routes behave correctly
