---
name: nextjs-conventions
description: Next.js App Router patterns, conventions, and best practices. Use when building or reviewing Next.js components, pages, routes, or configuration.
---

# Next.js App Router Conventions

## Component Patterns
- Server Components by default -- no directive needed
- "use client" only for hooks, event handlers, browser APIs, GSAP
- Data fetching in Server Components using async/await directly
- Pass serialisable data to Client Components as props

## Route Organisation
- Route groups `(marketing)`, `(dashboard)` for layout separation
- `page.tsx` for route content
- `layout.tsx` for shared UI (persists across child navigations)
- `loading.tsx` for streaming suspense fallbacks
- `error.tsx` for error boundaries
- `not-found.tsx` for 404 states

## Metadata
- Static: `export const metadata: Metadata = { ... }`
- Dynamic: `export async function generateMetadata({ params }): Promise<Metadata> { ... }`
- Always include: title, description, openGraph, twitter

## Data Fetching
- Server Components: `fetch()` with caching options or direct DB queries
- Route Handlers: `app/api/` for external API endpoints
- Server Actions: `"use server"` functions for mutations
- Client: TanStack Query for complex client-side data needs

## Rendering
- Static Generation (default): pages pre-rendered at build time
- Dynamic: `export const dynamic = 'force-dynamic'` for per-request
- ISR: `export const revalidate = 3600` for timed revalidation

For full API reference, see: https://nextjs.org/docs
