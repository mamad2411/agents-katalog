# Next.js Skill

You are working on a Next.js project. Apply these conventions and best practices.

## App Router (Next.js 13+)

- Use the `app/` directory with the App Router by default. Avoid `pages/` for new code.
- Server Components are the default. Add `"use client"` only when you need browser APIs, event handlers, or React hooks.
- Colocate `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, and `not-found.tsx` in route segments.
- Use `generateMetadata()` for dynamic SEO metadata; use the `metadata` export for static metadata.
- Prefer `import { notFound } from 'next/navigation'` over manual 404 handling.

## Data Fetching

- Fetch data directly in Server Components with `async/await` — no `useEffect` for server data.
- Use Route Handlers (`app/api/route.ts`) instead of `pages/api/` for API endpoints.
- Cache with `fetch(url, { next: { revalidate: 60 } })` or `{ cache: 'no-store' }` for dynamic data.
- Use `unstable_cache` from `next/cache` for caching non-fetch async operations.
- Call `revalidatePath()` or `revalidateTag()` in Server Actions after mutations.

## Server Actions

- Mark async functions with `'use server'` at the top of the file or at function level.
- Validate all Server Action inputs with Zod before processing.
- Return `{ error: string }` on failure and `{ success: true, data: … }` on success — never throw.
- Use `useFormState` / `useActionState` (React 19) in Client Components to display Server Action results.

## Routing & Navigation

- Use `<Link href="…">` from `next/link` for client-side navigation — never `<a>` for internal routes.
- Use `useRouter()` from `next/navigation` (not `next/router`) in Client Components.
- Use `redirect()` from `next/navigation` in Server Components and Server Actions.
- Dynamic segments: `[slug]` for single, `[...slug]` for catch-all, `[[...slug]]` for optional.

## Images & Fonts

- Always use `<Image>` from `next/image` — never bare `<img>` for content images.
- Load fonts with `next/font/google` or `next/font/local`; assign to `className` on `<html>`.

## Environment Variables

- Prefix client-exposed variables with `NEXT_PUBLIC_`.
- Server-only secrets must NOT have the prefix or they will be leaked to the client.
- Access via `process.env.VAR_NAME`; validate at startup with a schema (e.g., `@t3-oss/env-nextjs`).

## Performance

- Use `<Suspense>` boundaries around async Server Components to enable streaming.
- Lazy-load heavy Client Components with `dynamic(() => import('…'), { ssr: false })`.
- Add `export const dynamic = 'force-static'` to routes that should be fully static.

## TypeScript

- Define route params as `{ params: Promise<{ slug: string }> }` in Next.js 15+ (params are async).
- `cookies()`, `headers()`, and `searchParams` are also async in Next.js 15+: always `await` them.
- Use `NextRequest` / `NextResponse` for Route Handler types.
