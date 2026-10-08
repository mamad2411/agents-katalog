---
name: nextjs-expert
description: Build and modify Next.js App Router codebases using TypeScript, Tailwind CSS, and Prisma. Use for creating pages/layouts/components, route handlers (`app/api/*/route.ts`), server actions, and Prisma schema changes or database workflows in Next.js projects.
---

# Nextjs Expert

## Overview
Create production-ready Next.js features for this repo using App Router patterns, strict TypeScript, Tailwind styling, and Prisma for data access. Favor clear, minimal changes that match existing conventions.

## Quick Start
- Scan `app/`, `components/`, `lib/`, and `prisma/schema.prisma` before editing.
- Confirm the route, data source, and UI requirements; clarify server vs. client behavior.
- Start from templates in `assets/` and adjust to the specific task.

## Core Tasks

### Pages and Components
- Create route files as `app/<route>/page.tsx` and layouts as `app/<route>/layout.tsx`.
- Default to Server Components; add `"use client"` only when using hooks, state, or browser APIs.
- Place reusable UI in `components/`; keep route-only UI next to the route.

### Route Handlers and APIs
- Implement APIs in `app/api/<name>/route.ts` with named `GET`, `POST`, etc.
- Validate request bodies with Zod and return typed JSON responses via `NextResponse`.
- Include explicit status codes for error cases.

### Prisma and Database
- Update models in `prisma/schema.prisma` and keep relations explicit.
- Prefer `npx prisma migrate dev` for schema changes; use `npx prisma db push` only when migrations are not required.
- Keep database access in server-only modules and avoid client-side Prisma usage.

## Conventions
- TypeScript strict: no `any` unless justified; prefer `@/*` path alias.
- Tailwind CSS is the styling default; keep class lists readable and grouped.
- Use clear, imperative naming for components and functions (e.g., `UserTable`, `createOrder`).

## Assets
- `assets/app-page.tsx`: basic App Router page template.
- `assets/route-handler.ts`: API route handler starter.
- `assets/prisma-model.prisma`: model scaffold for new tables.

## References
- `references/stack.md`: stack assumptions and defaults.
