---
name: "nextjs"
description: "Next.js App Router patterns: Server Components, Server Actions, route handlers, middleware, parallel routes, ISR"
---

# Next.js Skill

## When to activate
- Building a Next.js application using the App Router
- Deciding between Server Components and Client Components
- Writing Server Actions for form submissions and mutations
- Setting up route handlers (API endpoints in App Router)
- Implementing authentication with NextAuth or a JWT pattern
- Configuring middleware for redirects and auth guards
- Optimizing data fetching with React `cache()` and `unstable_cache`
- Using parallel routes, intercepting routes, or route groups

## When NOT to use
- Pages Router projects — the patterns differ significantly
- Pure SPAs with no server rendering (use Vite + React)
- NestJS or Express backends — use NestJS skill
- Static sites with no dynamic data (use Astro)

## Instructions

### App Router directory structure
```
app/
├── (auth)/              # Route group — no URL segment
│   ├── login/
│   │   └── page.tsx
│   └── layout.tsx       # Auth-specific layout
├── (dashboard)/
│   ├── dashboard/
│   │   ├── page.tsx     # Server Component by default
│   │   └── loading.tsx  # Suspense boundary UI
│   └── layout.tsx
├── api/
│   └── webhooks/
│       └── stripe/
│           └── route.ts # Route Handler
├── layout.tsx           # Root layout (required)
└── page.tsx             # Home page
components/
├── ui/                  # Presentational (can be server or client)
└── forms/               # Always client components (useState/events)
lib/
├── auth.ts
├── db.ts
└── actions/             # Server Actions
    └── user.ts
```

### Server vs. Client Components
```tsx
// Server Component (default) — runs on server, never sent to client
// Can: await fetch, read DB, access env vars
// Cannot: useState, useEffect, browser APIs, event handlers
export default async function UserProfile({ id }: { id: string }) {
  const user = await db.user.findUnique({ where: { id } })
  return <div>{user.name}</div>
}

// Client Component — add 'use client' directive
'use client'
import { useState } from 'react'

export function LikeButton({ initialCount }: { initialCount: number }) {
  const [count, setCount] = useState(initialCount)
  return <button onClick={() => setCount(c => c + 1)}>{count} likes</button>
}
```

Rule: default to Server Components. Add `'use client'` only when you need interactivity, browser APIs, or React hooks.

### Data fetching patterns
```tsx
// Server Component — direct async/await, no useEffect, no useState
export default async function PostList() {
  const posts = await db.post.findMany({ where: { published: true } })
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}

// Deduplication — React cache() wraps a function so multiple components
// calling it in one render share one fetch
import { cache } from 'react'
export const getUser = cache(async (id: string) => {
  return db.user.findUnique({ where: { id } })
})

// Static generation with revalidation
async function getProducts() {
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 }, // ISR — revalidate every hour
  })
  return res.json()
}
```

### Server Actions
```tsx
// lib/actions/user.ts
'use server'
import { revalidatePath } from 'next/cache'
import { z } from 'zod'

const UpdateSchema = z.object({
  name: z.string().min(1),
})

export async function updateUser(formData: FormData) {
  const parsed = UpdateSchema.safeParse({ name: formData.get('name') })
  if (!parsed.success) return { error: parsed.error.flatten() }

  await db.user.update({ where: { id: getCurrentUserId() }, data: parsed.data })
  revalidatePath('/dashboard/profile')
  return { success: true }
}

// In a Server Component:
export default function ProfileForm({ user }: { user: User }) {
  return (
    <form action={updateUser}>
      <input name="name" defaultValue={user.name} />
      <button type="submit">Save</button>
    </form>
  )
}
```

### Route Handlers
```ts
// app/api/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'

export async function POST(req: NextRequest) {
  const body = await req.text()
  const sig = req.headers.get('stripe-signature')!

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  if (event.type === 'checkout.session.completed') {
    await handleCheckoutCompleted(event.data.object)
  }

  return NextResponse.json({ received: true })
}
```

### Middleware
```ts
// middleware.ts (root level)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
}
```

### Parallel and intercepting routes
```
app/
├── @modal/          # Parallel route — renders alongside main content
│   └── (.)photo/    # Intercepting route — intercepts /photo/[id]
│       └── [id]/
│           └── page.tsx
├── photo/
│   └── [id]/
│       └── page.tsx
└── layout.tsx       # Accepts { children, modal } as props
```

### Error and loading boundaries
```tsx
// app/dashboard/loading.tsx — shown during Suspense
export default function Loading() {
  return <DashboardSkeleton />
}

// app/dashboard/error.tsx — error boundary for this segment
'use client'
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <p>{error.message}</p>
      <button onClick={reset}>Retry</button>
    </div>
  )
}
```

### Environment variables
- `NEXT_PUBLIC_*` — exposed to the browser
- All others — server-only (never accessible in Client Components)
- Never import a server-only env var inside a Client Component — it returns `undefined` silently

## Example

**User:** Add a paginated blog posts page at `/blog` that fetches from PostgreSQL, with a "New Post" modal that opens at `/blog/new` but doesn't navigate away from the posts list.

**Expected output:**
- `app/blog/page.tsx` — Server Component, fetches posts with `db.post.findMany`, renders `<PostList>` + `<Link href="/blog/new">`
- `app/@modal/(.)blog/new/page.tsx` — Intercepting route showing a `<NewPostModal>` Client Component
- `app/blog/new/page.tsx` — Full-page fallback for direct navigation
- `app/layout.tsx` — Updated to accept `modal` parallel route slot and render it alongside `children`
- `lib/actions/post.ts` — `createPost` Server Action with Zod validation + `revalidatePath('/blog')`

---
