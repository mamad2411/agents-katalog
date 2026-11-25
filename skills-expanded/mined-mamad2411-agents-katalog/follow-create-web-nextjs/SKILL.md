---
name: follow-create-web-nextjs
description: Guidelines for structuring and developing Next.js 16 applications
argument-hint: "[scope]"
related:
  - deep-review-codebase
  - follow-create-web
  - follow-create-mobile
  - follow-best-practice
  - setup-cicd
  - run-dev
---

## Goal

Define guidelines for developing Next.js 16 applications at peak performance

## Scope

Structure and develop Next.js 16 applications with App Router, React 19.3, Cache Components, and TypeScript

- Packages: `next` 16.x (Node >= 20.9, TypeScript >= 5.1, Turbopack is the stable default for both dev and build, React Compiler stable), `react`/`react-dom` 19.x — always verify the latest versions with `/deep-research` + `/follow-best-practice` (no pinning in this file — per `/update-devin-global-skills`)
- Scaffold: `bun create next-app@latest my-app --ts --app --tailwind --src-dir --import-alias "@/*"` (Turbopack default; flags `--react-compiler`, `--biome`; `next dev/build --webpack` fallback allowed)

## Execute

### 1. Project Structure

> Goal: Create the App Router structure with an `app/` directory

1. Use App Router with an `app/` directory
2. Create `app/layout.tsx` for the root layout
3. Create `app/page.tsx` for the home page
4. Create `app/globals.css` for global styles
5. Create `app/error.tsx`, `loading.tsx`, `not-found.tsx` for error handling
6. Use `app/api/` for API routes
7. Use route groups `(group)` to organize routes without affecting the URL

### 2. Directory Organization

> Goal: Organize supporting directories outside `app/`

1. Use `components/` for React components (ui, features)
2. Use `hooks/` for custom React hooks
3. Use `lib/` for utilities and helpers
4. Use `types/` for TypeScript types
5. Use `public/` for static assets

### 3. Configuration

> Goal: Set up Next.js 16 config and scripts

1. Set up `next.config.ts` for the Next.js config
2. Set up `tsconfig.json` with strict mode (TypeScript 5.1+)
3. Set up `package.json` scripts (dev, build, start, lint, typecheck)
4. Create `proxy.ts` for auth checks only (no database calls) — replaces `middleware.ts`
5. Use Turbopack for dev and build (stable default in Next.js 16 — fall back to `next dev --webpack` / `next build --webpack` when needed)

### 4. Server And Client Components

> Goal: Separate Server and Client Components correctly

1. Server Components are the default (no `useState`, `useEffect`)
2. Use Client Components only when interactivity is needed (`'use client'`)
3. Push `'use client'` as deep as possible in the tree
4. Pass Server Components as `children` of Client Components
5. Avoid non-serializable props from Server → Client (functions, dates)

### 5. Data Fetching And Cache Components

> Goal: Use Server Components for data fetching and Cache Components for explicit caching

1. Use Server Components for data fetching (no `useEffect`)
2. Use `Promise.all` for parallel data fetching (avoid waterfalls)
3. `params` and `searchParams` are `Promise`s in Next.js 15+ and must be `await`ed
4. Use the `'use cache'` directive for Cache Components (Next.js 16 — explicit opt-in caching)
5. Use `generateMetadata` for SEO on every page
6. Use `generateStaticParams` for static generation; invalidate the cache with `updateTag()`/`revalidateTag()` from `next/cache`

### 6. Server Actions

> Goal: Use Server Actions for form handling and mutations

1. Use Server Actions for form handling and mutations
2. Validate inputs with Zod schemas
3. Return typed error objects
4. Use the `'use server'` directive for Server Actions
5. Test forms without client-side JavaScript

### 7. Performance

> Goal: Tune performance with Turbopack, React Compiler, and PPR

1. Use `next/image` for image optimization
2. Use `next/link` for navigation
3. Use dynamic imports for code splitting
4. Use Suspense boundaries for streaming (instead of `loading.tsx` when granular control is needed)
5. Use Partial Prerendering (PPR) for a static shell + dynamic islands
6. Use React Compiler instead of manual `memo`/`useMemo`/`useCallback` (stable in Next.js 16)
7. Use React 19.3 features: View Transitions, `useEffectEvent()`

### 8. Caching Strategy

> Goal: Use the explicit caching APIs of Next.js 16

1. `fetch()` is not cached by default in Next.js 15+
2. Use the `'use cache'` directive for Cache Components (Next.js 16)
3. Use `next: { revalidate: seconds }` for time-based revalidation
4. Use `next: { tags: ['tag'] }` for tag-based revalidation
5. Use `updateTag()` and `revalidateTag()` for cache invalidation
6. Use `cache: 'force-cache'` for static data
7. Use `cache: 'no-store'` for always-fresh data

## Rules

### 1. Directory Structure

- Use an `app/` directory for App Router
- Use route groups `(group)` to organize routes
- Use `components/` for shared components (ui, features)
- Use `hooks/` for custom hooks
- Use `lib/` for utilities
- Use `types/` for TypeScript types

### 2. Server And Client Components

- Server Components are the default
- Use `'use client'` only when interactivity, state, or browser APIs are needed
- Push `'use client'` as deep as possible in the tree
- Pass Server Components as `children` of Client Components
- Avoid `useEffect` for data fetching; use Server Components instead

### 3. Data Fetching And Caching

- Use Server Components for data fetching
- Use `Promise.all` for parallel fetches
- `params` and `searchParams` are `Promise`s and must be `await`ed
- Use the `'use cache'` directive for explicit caching (Next.js 16)
- Use an explicit `revalidate` or `cache` in every `fetch()`
- Use `generateMetadata` on every page

### 4. Server Actions

- Validate inputs with Zod
- Return typed error objects
- Test forms without client-side JavaScript
- Use the `'use server'` directive

### 5. Performance

- Use `next/image` for images
- Use `next/link` for navigation
- Use Suspense boundaries for streaming
- Use PPR for a static + dynamic hybrid
- Use React Compiler instead of manual memoization
- Use dynamic imports for heavy components

### 6. Proxy (formerly Middleware)

- Use `proxy.ts` instead of `middleware.ts` (Next.js 16)
- Use it for auth checks only
- Never make database calls in the proxy
- Runs on the Edge Runtime

- Use /deep-review-codebase if needed
- Use /follow-create-mobile-cross-with-capacitor if needed (create web nextjs)
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /deep-review-codebase if needed
- Use /run-dev if needed

## File Structure

Canonical file structure + layer table: [templates/file-structure-web-nextjs.md](templates/file-structure-web-nextjs.md)

## Expected Outcome

- A correctly structured Next.js 16 project
- Server Components as the default, Client Components only when needed
- App Router with streaming, PPR, and Cache Components
- TypeScript strict mode
- Better performance with Turbopack, React Compiler, and Suspense
- Server Actions for mutations
