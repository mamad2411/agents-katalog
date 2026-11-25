---
name: tpl-fullstack-nextjs-trpc-drizzle
description: Template do pack (fullstack/05-nextjs-trpc-drizzle.md). Orienta o agente em stacks fullstack e arquitetura ponta a ponta alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: fullstack/05-nextjs-trpc-drizzle.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Next.js 15 + tRPC v11 + Drizzle + Neon + NextAuth v5

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `fullstack/05-nextjs-trpc-drizzle.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Framework:** Next.js 15 (App Router, React 19)
- **API:** tRPC v11
- **ORM:** Drizzle ORM + Neon (PostgreSQL serverless)
- **Auth:** Auth.js v5 (NextAuth v5)
- **UI:** shadcn/ui + Tailwind CSS v3
- **Language:** TypeScript 5.x (strict)
- **Testing:** Vitest + Playwright

---

## PROJECT STRUCTURE
```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   ├── (dashboard)/
│   │   └── dashboard/page.tsx
│   └── api/
│       ├── auth/
│       │   └── [...nextauth]/route.ts
│       └── trpc/
│           └── [trpc]/route.ts
├── server/
│   ├── auth.ts                 # NextAuth v5 config
│   ├── db/
│   │   ├── index.ts            # Drizzle + Neon client
│   │   └── schema.ts
│   └── api/
│       ├── root.ts
│       ├── trpc.ts             # Context, procedures
│       └── routers/
│           ├── post.ts
│           └── user.ts
├── trpc/
│   ├── react.tsx               # React client provider
│   └── server.ts               # RSC caller
└── components/
    └── ui/                     # shadcn components
```

---

## ARCHITECTURE RULES
1. **App Router + tRPC coexist cleanly** — Server Components call `createCaller(ctx)`; Client Components use `trpc.*` hooks.
2. **Drizzle schema files are the only migration source** — `drizzle-kit push` for dev, `drizzle-kit migrate` for prod.
3. **Auth.js v5 callbacks enrich JWT** — add `userId` and `role` to session/token in `jwt` callback.
4. **Neon serverless driver used in edge** — use `@neondatabase/serverless` + `ws` polyfill for edge runtime; `Pool` for Node runtime.
5. **No mixing RSC data fetching and tRPC** — choose per-page: RSC direct call or Client hook; don't nest both patterns.
6. **`protectedProcedure` = session check** — automatically redirects or throws `UNAUTHORIZED`.
7. **shadcn components are local** — never update shadcn by overwriting; treat as owned files.

---

## TRPC + APP ROUTER SETUP

```typescript
// src/server/api/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server'
import { cache }    from 'react'
import superjson    from 'superjson'
import { auth }     from '../auth'
import { db }       from '../db'

export const createTRPCContext = cache(async () => {
  const session = await auth()
  return { db, session }
})

const t = initTRPC.context<typeof createTRPCContext>().create({
  transformer: superjson,
})

export const createTRPCRouter   = t.router
export const createCallerFactory = t.createCallerFactory
export const publicProcedure    = t.procedure

export const protectedProcedure = t.procedure.use(async ({ ctx, next }) => {
  if (!ctx.session?.user?.id) throw new TRPCError({ code: 'UNAUTHORIZED' })
  return next({ ctx: { ...ctx, session: ctx.session } })
})

// src/app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch'
import { appRouter }           from '~/server/api/root'
import { createTRPCContext }   from '~/server/api/trpc'

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext: createTRPCContext,
  })

export { handler as GET, handler as POST }
```

---

## DRIZZLE + NEON SETUP

```typescript
// src/server/db/schema.ts
import { pgTable, text, boolean, timestamp, integer } from 'drizzle-orm/pg-core'
import { relations } from 'drizzle-orm'
import { createId }  from '@paralleldrive/cuid2'

export const users = pgTable('users', {
  id:            text('id').primaryKey().$defaultFn(createId),
  name:          text('name'),
  email:         text('email').notNull().unique(),
  emailVerified: timestamp('email_verified', { mode: 'date' }),
  image:         text('image'),
  role:          text('role', { enum: ['user', 'admin'] }).notNull().default('user'),
})

export const posts = pgTable('posts', {
  id:        text('id').primaryKey().$defaultFn(createId),
  title:     text('title').notNull(),
  content:   text('content').notNull(),
  published: boolean('published').notNull().default(false),
  authorId:  text('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  createdAt: timestamp('created_at', { mode: 'date' }).defaultNow(),
})

export const usersRelations = relations(users, ({ many }) => ({ posts: many(posts) }))
export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, { fields: [posts.authorId], references: [users.id] }),
}))

// src/server/db/index.ts
import { neon }    from '@neondatabase/serverless'
import { drizzle } from 'drizzle-orm/neon-http'
import * as schema from './schema'

const sql = neon(process.env.DATABASE_URL!)
export const db = drizzle(sql, { schema })
export type DB  = typeof db
```

---

## RSC + CLIENT HYBRID USAGE

```typescript
// src/trpc/server.ts (RSC side - no HTTP round trip)
import { createCallerFactory } from '~/server/api/root'
import { createTRPCContext }   from '~/server/api/trpc'

const createCaller = createCallerFactory(appRouter)
export const api = createCaller(await createTRPCContext())

// src/app/(dashboard)/dashboard/page.tsx — SERVER COMPONENT
import { api } from '~/trpc/server'

export default async function DashboardPage() {
  const posts = await api.post.list({ limit: 10 })
  // posts is fully typed from router return type
  return <PostList initialPosts={posts} />
}

// src/components/PostList.tsx — CLIENT COMPONENT (optimistic updates)
'use client'
import { trpc } from '~/trpc/react'

export function PostList({ initialPosts }: { initialPosts: Post[] }) {
  const { data: posts } = trpc.post.list.useQuery(
    { limit: 10 },
    { initialData: initialPosts }         // hydrate from RSC
  )

  const utils = trpc.useUtils()
  const create = trpc.post.create.useMutation({
    onMutate: async (newPost) => {
      await utils.post.list.cancel()
      const prev = utils.post.list.getData({ limit: 10 })
      utils.post.list.setData({ limit: 10 }, (old) =>
        old ? [{ ...newPost, id: 'temp', createdAt: new Date() }, ...old] : old
      )
      return { prev }
    },
    onError: (_, __, ctx) => utils.post.list.setData({ limit: 10 }, ctx?.prev),
    onSettled: () => utils.post.list.invalidate(),
  })

  return <ul>{posts?.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

---

## NEXTAUTH V5 CONFIG

```typescript
// src/server/auth.ts
import NextAuth, { type DefaultSession } from 'next-auth'
import GitHub   from 'next-auth/providers/github'
import Credentials from 'next-auth/providers/credentials'
import { DrizzleAdapter } from '@auth/drizzle-adapter'
import { db } from './db'

declare module 'next-auth' {
  interface Session { user: { id: string; role: 'user' | 'admin' } & DefaultSession['user'] }
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: DrizzleAdapter(db),
  providers: [GitHub],
  callbacks: {
    session: ({ session, user }) => ({
      ...session,
      user: { ...session.user, id: user.id, role: (user as typeof user & { role: string }).role ?? 'user' },
    }),
  },
  pages: { signIn: '/login' },
})
```

---

## ROUTING TABLE

| Procedure / Route | Type | Auth | Action |
|-------------------|------|------|--------|
| `post.list` | tRPC query | No | Paginated posts |
| `post.byId` | tRPC query | No | Single post |
| `post.create` | tRPC mutation | Yes | Create post |
| `post.publish` | tRPC mutation | Yes (owner) | Publish post |
| `post.delete` | tRPC mutation | Yes (owner) | Delete post |
| `user.me` | tRPC query | Yes | Current user |
| `user.update` | tRPC mutation | Yes | Update profile |
| GET /api/auth/[...nextauth] | HTTP | — | Auth endpoints |
| GET /dashboard | RSC page | Yes | Dashboard with RSC prefetch |
| GET /login | Client page | No | Auth.js sign-in |

---

## QUALITY GATES
- [ ] `tsc --noEmit` — zero errors
- [ ] `next build` — zero warnings
- [ ] RSC pages prefetch via `api.*` caller (no waterfall)
- [ ] Client mutations use optimistic updates for UX
- [ ] NextAuth session type augmented with `id` and `role`
- [ ] `drizzle-kit check` — migrations synced with schema
- [ ] `vitest run` — all unit tests pass
- [ ] `playwright test` — login + create post E2E passes
- [ ] Neon connection string in `.env.local`, never committed

---

## FORBIDDEN
- ❌ `fetch('/api/trpc/...')` from Client Components — use tRPC hooks
- ❌ `"use client"` on layout or page components that can be RSC
- ❌ `any` on tRPC return types or Drizzle query results
- ❌ Multiple Drizzle/Neon client instances
- ❌ `useEffect` for data loading — use tRPC hooks or RSC
- ❌ `session.user.id` without type augmentation
- ❌ Drizzle raw SQL without parameterization
- ❌ Environment variables without `NEXT_PUBLIC_` prefix accessed on client
