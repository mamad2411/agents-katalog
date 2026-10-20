---
name: "trpc"
description: "tRPC end-to-end type-safe APIs: T3 Stack setup, routers, procedures, Zod validation, React Query integration, middleware, subscriptions"
---

# tRPC Skill

## When to activate
- Building the T3 Stack (Next.js + tRPC + Drizzle/Prisma + TypeScript)
- Wanting end-to-end type safety between your Next.js frontend and backend without REST or GraphQL
- Writing type-safe API procedures with Zod input validation
- Setting up tRPC with React Query for data fetching in React
- Adding middleware (auth, rate limiting, logging) to tRPC procedures

## When NOT to use
- APIs consumed by non-TypeScript clients (mobile apps, third parties) — use REST instead
- Public APIs — tRPC is designed for same-codebase full-stack TypeScript
- When GraphQL's flexibility is needed — use the GraphQL skill

## Instructions

### Installation (T3 Stack)

```bash
# Scaffold a full T3 Stack app
npx create-t3-app@latest my-app

# Or add tRPC to existing Next.js
npm install @trpc/server @trpc/client @trpc/react-query @tanstack/react-query zod
```

### Project structure

```
src/
├── server/
│   ├── trpc.ts          # tRPC instance, context, middleware
│   ├── routers/
│   │   ├── _app.ts      # Root router (combines all routers)
│   │   ├── user.ts      # User procedures
│   │   └── post.ts      # Post procedures
├── app/
│   └── api/
│       └── trpc/
│           └── [trpc]/
│               └── route.ts   # Next.js App Router handler
└── trpc/
    └── client.ts        # Client-side tRPC setup
```

### tRPC instance setup

```typescript
// server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server'
import { getServerSession } from 'next-auth'
import type { Session } from 'next-auth'
import superjson from 'superjson'
import { ZodError } from 'zod'
import { db } from '@/db'

// Context — available to all procedures
export async function createTRPCContext(opts: { headers: Headers }) {
  const session = await getServerSession()
  return { db, session, headers: opts.headers }
}

type Context = Awaited<ReturnType<typeof createTRPCContext>>

const t = initTRPC.context<Context>().create({
  transformer: superjson,  // handles Date, Map, Set serialisation
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError: error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    }
  },
})

// Base procedures
export const router = t.router
export const publicProcedure = t.procedure

// Protected procedure — requires authentication
const isAuthed = t.middleware(({ ctx, next }) => {
  if (!ctx.session?.user) throw new TRPCError({ code: 'UNAUTHORIZED' })
  return next({ ctx: { ...ctx, session: ctx.session } })
})
export const protectedProcedure = t.procedure.use(isAuthed)

// Rate-limited procedure
const rateLimit = t.middleware(async ({ ctx, next }) => {
  const userId = ctx.session?.user?.id ?? ctx.headers.get('x-forwarded-for')
  const key = `ratelimit:${userId}`
  const count = await redis.incr(key)
  if (count === 1) await redis.expire(key, 60)
  if (count > 100) throw new TRPCError({ code: 'TOO_MANY_REQUESTS' })
  return next()
})
export const rateLimitedProcedure = publicProcedure.use(rateLimit)
```

### Defining procedures (queries and mutations)

```typescript
// server/routers/user.ts
import { z } from 'zod'
import { router, publicProcedure, protectedProcedure } from '../trpc'
import { TRPCError } from '@trpc/server'

export const userRouter = router({
  // Query — GET equivalent
  getById: publicProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(async ({ ctx, input }) => {
      const user = await ctx.db.query.users.findFirst({
        where: eq(users.id, input.id),
        columns: { id: true, name: true, email: true, createdAt: true },
      })
      if (!user) throw new TRPCError({ code: 'NOT_FOUND', message: 'User not found' })
      return user
    }),

  // Query — list with pagination
  list: protectedProcedure
    .input(z.object({
      cursor: z.string().optional(),
      limit: z.number().int().min(1).max(100).default(20),
    }))
    .query(async ({ ctx, input }) => {
      const items = await ctx.db.query.users.findMany({
        limit: input.limit + 1,
        where: input.cursor ? gt(users.id, input.cursor) : undefined,
        orderBy: asc(users.id),
      })
      const hasMore = items.length > input.limit
      return {
        items: items.slice(0, input.limit),
        nextCursor: hasMore ? items[input.limit - 1].id : null,
      }
    }),

  // Mutation — POST/PUT equivalent
  update: protectedProcedure
    .input(z.object({
      name: z.string().min(1).max(100).optional(),
      bio:  z.string().max(500).optional(),
    }))
    .mutation(async ({ ctx, input }) => {
      const [updated] = await ctx.db
        .update(users)
        .set({ ...input, updatedAt: new Date() })
        .where(eq(users.id, ctx.session.user.id))
        .returning()
      return updated
    }),

  // Mutation — delete
  delete: protectedProcedure
    .input(z.object({ id: z.string().uuid() }))
    .mutation(async ({ ctx, input }) => {
      if (ctx.session.user.id !== input.id) {
        throw new TRPCError({ code: 'FORBIDDEN' })
      }
      await ctx.db.delete(users).where(eq(users.id, input.id))
      return { success: true }
    }),
})
```

### Root router

```typescript
// server/routers/_app.ts
import { router } from '../trpc'
import { userRouter } from './user'
import { postRouter } from './post'

export const appRouter = router({
  user: userRouter,
  post: postRouter,
})

export type AppRouter = typeof appRouter
```

### Next.js App Router handler

```typescript
// app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch'
import { appRouter } from '@/server/routers/_app'
import { createTRPCContext } from '@/server/trpc'

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext: () => createTRPCContext({ headers: req.headers }),
    onError: process.env.NODE_ENV === 'development'
      ? ({ path, error }) => console.error(`tRPC error on ${path}:`, error)
      : undefined,
  })

export { handler as GET, handler as POST }
```

### Client-side setup

```typescript
// trpc/client.ts
import { createTRPCReact } from '@trpc/react-query'
import type { AppRouter } from '@/server/routers/_app'

export const trpc = createTRPCReact<AppRouter>()

// app/providers.tsx
'use client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { httpBatchLink } from '@trpc/client'
import superjson from 'superjson'
import { trpc } from '@/trpc/client'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [httpBatchLink({ url: '/api/trpc', transformer: superjson })],
    })
  )
  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </trpc.Provider>
  )
}
```

### Usage in React components

```tsx
'use client'
import { trpc } from '@/trpc/client'

function UserProfile({ userId }: { userId: string }) {
  // Query — type-safe, auto-fetches, React Query under the hood
  const { data: user, isLoading, error } = trpc.user.getById.useQuery({ id: userId })

  // Mutation
  const updateMutation = trpc.user.update.useMutation({
    onSuccess: () => {
      trpc.useUtils().user.getById.invalidate({ id: userId })
    },
  })

  if (isLoading) return <Spinner />
  if (error) return <Error message={error.message} />

  return (
    <div>
      <h1>{user.name}</h1>
      <button onClick={() => updateMutation.mutate({ name: 'New Name' })}>
        {updateMutation.isPending ? 'Saving...' : 'Update'}
      </button>
    </div>
  )
}
```

### Server-side calls (Server Components / Server Actions)

```typescript
// In Server Components — call procedures directly without HTTP
import { createCaller } from '@/server/routers/_app'
import { createTRPCContext } from '@/server/trpc'

export default async function Page() {
  const ctx = await createTRPCContext({ headers: new Headers() })
  const caller = createCaller(ctx)
  const user = await caller.user.getById({ id: '123' })
  return <div>{user.name}</div>
}
```

## Example

**User:** Add a `tasks` router to a T3 app — create, list (paginated), complete, delete — with authentication required, Zod validation, and a React component that uses all four procedures.

**Expected output:**
- `server/routers/task.ts` — 4 procedures, all using `protectedProcedure`
- `server/routers/_app.ts` — updated to include `task: taskRouter`
- `components/TaskList.tsx` — `useQuery` for list, `useMutation` for create/complete/delete, optimistic updates on `onMutate`

---
