---
name: stack-knowledge
description: Project technology stack patterns for Next.js + Neon Postgres + Drizzle ORM + Better Auth + Tailwind CSS
user-invocable: false
---

# Stack Knowledge

This skill provides stack-specific patterns for agents making architectural and implementation decisions.

## Neon Postgres

- Use `@neondatabase/serverless` driver with Drizzle ORM
- Connection: `DATABASE_URL` env var pointing to Neon's pooled connection string
- Neon branching: each Vercel preview deployment can get its own database branch
- No Row-Level Security — authorization happens in the application layer via Better Auth middleware
- Migrations: `drizzle-kit push` for development, `drizzle-kit migrate` for production
- Always use connection pooling in serverless environments

## Drizzle ORM

- All database access goes through Drizzle — no raw SQL in application code
- Define schemas in `src/db/schema/` with one file per entity
- Index every column used in WHERE, JOIN, or ORDER BY
- Use partial indexes when filtering on constant conditions (e.g., `status = 'active'`)
- Infer types from schema: `type User = typeof users.$inferSelect`

## Better Auth

- Configure with Drizzle adapter pointing at Neon
- After adding/changing plugins, always run: `npx @better-auth/cli@latest generate`
- Import plugins from dedicated paths: `import { twoFactor } from "better-auth/plugins/two-factor"`
- Infer session types: `typeof auth.$Infer.Session`
- Environment variables: `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`
- Server-side auth: `auth.api.getSession()`

## Next.js App Router

- Server Components by default — only add `"use client"` for interactivity/hooks/browser APIs
- Server actions for mutations, route handlers for webhooks/external integrations
- Parallel data fetching with `Promise.all()` — never sequential awaits
- Wrap async server components in `<Suspense>` with meaningful fallbacks
- Dynamic imports via `next/dynamic` for heavy components not needed on first paint

## Tailwind CSS

- Utility-first — avoid custom CSS unless absolutely necessary
- Use `cn()` utility (clsx + tailwind-merge) for conditional classes
- Design tokens via CSS custom properties in `globals.css`
