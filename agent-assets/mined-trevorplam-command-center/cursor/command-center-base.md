---
description: Core project conventions and stack. Applied to every request.
alwaysApply: true
---

# Agency Platform — Core Conventions

## Stack
- Next.js 16.1 (Turbopack is default for dev and build — no flags needed)
- React 19 with TypeScript 5 strict mode
- Tailwind CSS v4 (CSS-first config — no tailwind.config.js exists)
- Style Dictionary v4 (ESM-only, async API, W3C DTCG format)
- pnpm 10 with catalog: protocol for all dependencies
- Turborepo 2.7

## Critical rules
- NEVER use `user_metadata` for tenant_id. Always use `app_metadata`.
- NEVER write `any` type. Use `unknown` and narrow, or define the type.
- NEVER import from another app. Shared code goes in packages/.
- NEVER use the service role key in client-side code or NEXT_PUBLIC_ variables.
- NEVER use tailwind.config.js — Tailwind v4 uses CSS @theme {} only.
- NEVER use theme() in CSS files — use var(--token-name) instead.
- ALWAYS use named exports. No default exports except Next.js page components.
- ALWAYS use `cn()` from @agency/ui for merging Tailwind classes.
- ALWAYS use Server Components by default. Add 'use client' only when needed.
- ALWAYS use Port 6543 (Supavisor) for Supabase connections, never Port 5432.
- ALWAYS use **tw-animate-css** for animations: import in app globals.css (`@import "tw-animate-css"`), use its utility classes. Never use `tailwindcss-animate` or custom keyframes.
- Apps using Tailwind MUST include the **@source** directive in globals.css pointing at `packages/ui` (and any other shared UI) so Tailwind v4 scans those paths.

## File naming
- kebab-case for all files: user-profile.tsx, not UserProfile.tsx
- Exceptions: Next.js reserved files (page.tsx, layout.tsx, middleware.ts)

## Package manager
- All dependencies use "catalog:" protocol, not version strings
- Internal packages use "workspace:*" protocol
- Run `pnpm install` from the repository root, not from individual packages
