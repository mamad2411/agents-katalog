# Next.js 15+ App Router Rules

## Scope
- Applies to Next.js 15+ projects using the App Router.
- Prioritize server-first rendering, performance, and deployment reliability.

## Framework Baseline
- Use App Router (`app/`) only; do not introduce Pages Router (`pages/`).
- Default to Server Components for all route segments and UI.
- Add `'use client'` only when interactivity or browser-only APIs are required.
- Keep client components minimal and leaf-oriented.

## Routing and Data Flow
- Use nested layouts and route groups to model product structure.
- Fetch data in Server Components when possible.
- Prefer explicit caching decisions (`force-cache`, `no-store`, revalidate intervals).
- Use `loading.tsx`, `error.tsx`, and `not-found.tsx` where appropriate.

## API Conventions
- Use Route Handlers (`app/**/route.ts`) for backend endpoints.
- Do not create legacy API routes under `pages/api`.
- Validate request payloads and query parameters before executing business logic.
- Return consistent JSON error shapes for client-facing endpoints.

## Database Layer
- ORM must be Prisma or Drizzle ORM.
- Keep schema and migrations in version control.
- Encapsulate DB access in dedicated server modules.
- Never import database clients into client components.

## Authentication
- Use NextAuth.js v5 for authentication and session management.
- Centralize auth configuration and callbacks in a dedicated module.
- Protect sensitive routes on the server side first.
- Keep secrets in environment variables and never commit them.

## Styling System
- Tailwind CSS is required.
- Use `shadcn/ui` for reusable UI primitives and consistency.
- Extend tokens through Tailwind config and CSS variables.
- Avoid ad hoc component-level style drift.

## Performance and DX
- Optimize images with `next/image`.
- Use `next/font` for font loading.
- Use dynamic imports for heavy client-only dependencies.
- Avoid unnecessary client-side state when server-rendered data is sufficient.

## Vercel-Ready Deployment
- Ensure `next build` succeeds with production environment expectations.
- Keep runtime usage explicit (`edge` vs `nodejs`) per route where needed.
- Use environment variable validation at startup.
- Avoid filesystem assumptions incompatible with serverless execution.

## Suggested Structure
- `app/` route tree, layouts, route handlers
- `components/` shared UI (server/client split explicit)
- `lib/` utilities, config, typed clients
- `server/` database/auth/domain services
- `types/` shared TypeScript types

## Definition of Done
- New routes follow App Router conventions.
- `'use client'` appears only where required.
- APIs are implemented via Route Handlers.
- Auth, DB, and styling choices align with this standard.
- Project builds and runs in a Vercel-like production environment.
