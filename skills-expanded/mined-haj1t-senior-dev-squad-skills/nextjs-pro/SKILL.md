---
name: nextjs-pro
description: "Next.js App Router, Server Components, Server Actions, ISR, streaming, middleware. Use when building or reviewing Next.js apps."
---

# Next.js Pro

## Purpose

Implement Next.js applications using production-proven patterns. Covers App Router, React Server Components, data fetching, Server Actions, streaming, ISR, Middleware, and performance optimization.

## When to Use

**Use this when:**
- Building a Next.js application using the App Router with React Server Components, Server Actions, or streaming
- Deciding between RSC, React Query, Server Actions, or Route Handlers for a particular data-fetching scenario
- Diagnosing slow TTFB, large client bundles, or excessive re-renders in an existing Next.js project

**Use this ESPECIALLY when:**
- The page boundary between server and client components is unclear and `'use client'` is spreading across the tree
- ISR vs. dynamic rendering vs. on-demand revalidation needs to be chosen for a high-traffic route
- Implementing auth-gated layouts with Middleware where redirect logic and token validation run at the edge

**Don't skip when:**
- Adding a new route group that mixes public and authenticated segments — layout nesting and auth wrapper placement must be deliberate
- Shipping to production with any `useEffect` data fetch still in place — Server Components may make it unnecessary and harmful
- Deploying to a non-Vercel host where Edge Runtime, ISR, and image optimization behavior can differ from local development

## Core Patterns

### 1. App Router Structure

```
app/
  (marketing)/
    page.tsx              ← Public landing
    layout.tsx            ← Marketing layout (no auth wrapper)
  (dashboard)/
    layout.tsx            ← Auth-required layout
    page.tsx              ← Dashboard home
    projects/
      page.tsx            ← /projects (paginated list)
      [id]/
        page.tsx          ← /projects/:id
        settings/
          page.tsx        ← /projects/:id/settings
  api/
    v1/
      projects/
        route.ts          ← GET, POST /api/v1/projects
        [id]/
          route.ts        ← GET, PATCH, DELETE /api/v1/projects/:id
```

### 2. Data Fetching Strategy

| Pattern | Use Case | Example |
|---------|----------|---------|
| **RSC (default)** | Initial page data | `async function Page()` |
| **React Query** | Client-side mutations + refetch | TanStack Query, SWR |
| **Server Actions** | Form submissions | `'use server'` functions |
| **Route Handlers** | External API consumption | Webhooks, mobile clients |

```tsx
// ✅ RSC: Fetch on server, zero client JS
async function ProjectPage({ params }: { params: { id: string } }) {
  const project = await db.projects.findUnique({
    where: { id: params.id },
    include: { tasks: true },
  })
  if (!project) notFound()
  return <ProjectDetail project={project} />
}

// ✅ Server Action for mutations
async function createProject(formData: FormData) {
  'use server'
  const name = formData.get('name') as string
  await db.projects.create({ data: { name } })
  revalidatePath('/projects')
}
```

### 3. Route Design

```tsx
// ✅ Parallel routes for complex layouts
app/
  @analytics/   ← Parallel route (analytics panel)
  @chat/        ← Parallel route (chat panel)
  page.tsx      ← Default view

// ✅ Intercepting routes for modals
app/
  feed/
    page.tsx           ← /feed
    photo/
      [id]/
        page.tsx       ← /feed/photo/:id (full page)
  @modal/
    photo/
      [id]/
        page.tsx       ← Intercepted modal
```

### 4. Error Handling

```tsx
// error.tsx — per-route error boundary
'use client'
export default function Error({ error, reset }: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <ErrorState
      message={error.message}
      onRetry={reset}
    />
  )
}

// not-found.tsx — per-route 404
export default function NotFound() {
  return <EmptyState message="Project not found" />
}

// global-error.tsx — last resort (replaces root layout)
export default function GlobalError({ error, reset }: Props) {
  return <html><body><ErrorFallback /></body></html>
}
```

### 5. Loading & Streaming

```tsx
// loading.tsx — per-route loading state
export default function Loading() {
  return <ProjectListSkeleton />
}

// Streaming with Suspense
async function ProjectPage() {
  return (
    <div>
      <h1>Project Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <ProjectStats />         ← Slow data (streamed)
      </Suspense>
      <Suspense fallback={<ListSkeleton />}>
        <ProjectList />          ← Fast data (renders first)
      </Suspense>
    </div>
  )
}
```

### 6. Middleware

```tsx
// middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value

  // Protected routes
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  // Internationalization
  if (request.nextUrl.pathname.startsWith('/en') || ...) {
    // rewrite to locale-specific page
  }
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/v1/:path*'],
}
```

### 7. ISR & Caching

```tsx
// Incremental Static Regeneration
async function BlogPage() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 }  // Revalidate every hour
  })
  return <BlogList posts={posts} />
}

// On-demand revalidation
// POST /api/revalidate
export async function POST(request: Request) {
  const { path } = await request.json()
  revalidatePath(path)
  return Response.json({ revalidated: true })
}
```

### Performance Checklist

- [ ] Server Components by default (`'use client'` only when needed)
- [ ] Images use `next/image` with `sizes` prop
- [ ] Fonts self-hosted via `next/font`
- [ ] Route segments are dynamic only when needed (`dynamic = 'force-static'` where possible)
- [ ] Streaming used for slow data (Suspense boundaries)
- [ ] No `useEffect` for data fetching (use RSC or React Query)
- [ ] Metadata API used for SEO (`generateMetadata`)
- [ ] Bundle minimized: dynamic imports for heavy libraries
- [ ] Edge runtime considered for auth/cookies middleware

## Related Skills

- **frontend-senior-engineer** — for deep React component design, custom hooks, and complex client-state patterns that sit inside Next.js pages
- **backend-senior-engineer** — when Route Handlers grow into a substantial API layer that needs service separation, database transactions, and rate limiting
- **supabase-pro** — when Next.js Server Components and Server Actions connect to Supabase for auth, real-time subscriptions, or storage
- **performance-engineer** — for Core Web Vitals forensics, bundle analysis, and ISR/CDN cache strategy tuning beyond the checklist
- **security-reviewer** — for CSRF posture in Server Actions, CSP headers in middleware, and OAuth callback route hardening
- **devops-release-engineer** — for Vercel/self-hosted deployment pipelines, preview environments, and environment variable management across stages
- **code-reviewer** — when Route Handlers expose a public or mobile-consumed API and versioning, error envelope, and contract stability matter
