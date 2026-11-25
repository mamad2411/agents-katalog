---
name: tpl-backend-graphql-apollo
description: Template do pack (backend/05-graphql-apollo.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/05-graphql-apollo.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: GraphQL API (Apollo Server + Prisma)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/05-graphql-apollo.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK

| Technology | Version | Purpose |
|------------|---------|---------|
| Node.js | 22.x | Runtime |
| TypeScript | 5.4+ | Language |
| Apollo Server | 4.x | GraphQL server |
| GraphQL | 16.x | Query language |
| Prisma | 5.x | ORM + migrations |
| PostgreSQL | 16 | Primary database |
| DataLoader | 2.x | Batching + caching (N+1 prevention) |
| Zod | 3.x | Input validation |
| jsonwebtoken | 9.x | JWT tokens |
| Vitest | 1.x | Unit tests |
| graphql-ws | 5.x | WebSocket-based subscriptions |

---

## PROJECT STRUCTURE

```
src/
├── schema/
│   ├── typeDefs/
│   │   ├── user.graphql      # SDL type definitions
│   │   ├── post.graphql
│   │   └── auth.graphql
│   └── index.ts              # mergeTypeDefs + makeExecutableSchema
├── resolvers/
│   ├── user/
│   │   ├── queries.ts        # User queries
│   │   ├── mutations.ts      # User mutations
│   │   └── fields.ts         # Field resolvers (e.g., User.posts)
│   ├── auth/
│   │   ├── mutations.ts
│   │   └── subscriptions.ts
│   └── index.ts              # mergeResolvers
├── dataloaders/
│   ├── userLoader.ts         # DataLoader for batching user queries
│   ├── postLoader.ts
│   └── index.ts              # Loader factory per request
├── services/
│   └── users/
│       └── users.service.ts
├── context/
│   └── index.ts              # Context builder (auth + loaders + prisma)
├── middleware/
│   └── auth.ts               # Token extraction + user injection
├── lib/
│   └── prisma.ts             # Prisma client singleton
├── server.ts                 # Apollo Server + Express setup
└── generated/
    └── graphql.ts            # codegen output (never edit manually)
prisma/
├── schema.prisma
└── migrations/
codegen.yml
```

---

## ARCHITECTURE RULES

- **Schema-first development**: always write `.graphql` SDL files first, then resolvers
- Resolvers are thin: validate inputs with Zod, call service, return result
- Services contain all business logic — resolvers never query Prisma directly
- DataLoaders are created **per request** (in context factory) — never shared across requests
- Authentication is checked in context builder for protected operations; resolvers check `context.user`
- Never return internal error details in GraphQL errors — use user-friendly messages
- `codegen.yml` regenerated whenever schema changes: `npx graphql-codegen`

### Schema-First vs Code-First Decision

| Use Schema-First (SDL) | Use Code-First |
|------------------------|----------------|
| Team has frontend + mobile consumers | Solo backend dev, schema evolves fast |
| Contract-first with external teams | TypeScript-centric team, schema from types |
| This project's choice ✅ | Schema-as-code preference |

---

## RESOLVER RULES

```typescript
// src/resolvers/user/queries.ts
import { z } from 'zod'
import { QueryResolvers } from '../../generated/graphql'
import { UserService } from '../../services/users/users.service'
import { GraphQLError } from 'graphql'

const paginationSchema = z.object({
  first: z.number().int().min(1).max(100).default(20),
  after: z.string().optional(),
})

export const userQueries: QueryResolvers = {
  me: async (_parent, _args, context) => {
    if (!context.user) {
      throw new GraphQLError('Not authenticated', {
        extensions: { code: 'UNAUTHENTICATED' },
      })
    }
    return context.services.users.getById(context.user.id)
  },

  users: async (_parent, args, context) => {
    if (!context.user?.isAdmin) {
      throw new GraphQLError('Not authorized', {
        extensions: { code: 'FORBIDDEN' },
      })
    }
    const { first, after } = paginationSchema.parse(args)
    return context.services.users.list({ first, after })
  },
}
```

### Field Resolvers

```typescript
// src/resolvers/user/fields.ts — NEVER query DB here, use DataLoader
import { UserResolvers } from '../../generated/graphql'

export const UserFieldResolvers: UserResolvers = {
  posts: async (parent, _args, context) => {
    // DataLoader batches all `posts` field calls in a single query
    return context.loaders.postsByUserId.load(parent.id)
  },
  // total is computed, not stored
  postCount: async (parent, _args, context) => {
    const posts = await context.loaders.postsByUserId.load(parent.id)
    return posts.length
  },
}
```

---

## DATALOADER PATTERN

DataLoaders MUST be created fresh per request to avoid cross-request cache pollution.

```typescript
// src/dataloaders/userLoader.ts
import DataLoader from 'dataloader'
import { prisma } from '../lib/prisma'
import type { User } from '@prisma/client'

export function createUserLoader() {
  return new DataLoader<string, User | null>(
    async (ids: readonly string[]) => {
      const users = await prisma.user.findMany({
        where: { id: { in: ids as string[] } },
      })
      // Result MUST be in same order as input ids
      const userMap = new Map(users.map(u => [u.id, u]))
      return ids.map(id => userMap.get(id) ?? null)
    },
    { cache: true } // cache within a single request context
  )
}

// src/dataloaders/index.ts
export function createLoaders() {
  return {
    userById: createUserLoader(),
    postsByUserId: createPostsByUserIdLoader(),
  }
}
```

```typescript
// src/context/index.ts
import { Request } from 'express'
import { prisma } from '../lib/prisma'
import { createLoaders } from '../dataloaders'
import { verifyToken } from '../middleware/auth'
import { UserService } from '../services/users/users.service'

export async function buildContext({ req }: { req: Request }) {
  const user = verifyToken(req.headers.authorization)  // null if unauthenticated
  return {
    user,
    prisma,
    loaders: createLoaders(),  // new instances per request
    services: {
      users: new UserService(prisma),
    },
  }
}

export type GraphQLContext = Awaited<ReturnType<typeof buildContext>>
```

---

## SUBSCRIPTION EXAMPLE

```typescript
// src/resolvers/auth/subscriptions.ts
import { SubscriptionResolvers } from '../../generated/graphql'
import { PubSub } from 'graphql-subscriptions'

export const pubsub = new PubSub()
export const USER_JOINED = 'USER_JOINED'

export const authSubscriptions: SubscriptionResolvers = {
  userJoined: {
    subscribe: (_parent, _args, context) => {
      if (!context.user?.isAdmin) throw new Error('Forbidden')
      return pubsub.asyncIterator([USER_JOINED])
    },
    resolve: (payload) => payload.userJoined,
  },
}
```

---

## ROUTING TABLE

| Trigger | Operation | Field | Auth | Resolver |
|---------|-----------|-------|------|---------|
| Get self | Query | `me` | Bearer | userQueries.me |
| List users | Query | `users(first, after)` | Bearer + Admin | userQueries.users |
| Get user | Query | `user(id)` | Bearer + Admin | userQueries.user |
| Register | Mutation | `register(input)` | Public | authMutations.register |
| Login | Mutation | `login(input)` | Public | authMutations.login |
| Refresh | Mutation | `refreshToken(token)` | Public | authMutations.refresh |
| Update profile | Mutation | `updateMe(input)` | Bearer | userMutations.updateMe |
| Delete account | Mutation | `deleteAccount` | Bearer | userMutations.deleteAccount |
| New user joined | Subscription | `userJoined` | Bearer + Admin | authSubscriptions.userJoined |

---

## QUALITY GATES

Before opening a PR, verify ALL of the following:

- [ ] `npx tsc --noEmit` passes — no type errors in resolvers or context
- [ ] `npx graphql-codegen` run — generated types match current schema
- [ ] `vitest run` passes with zero failures
- [ ] No resolver queries Prisma directly — goes through services
- [ ] DataLoaders used for all field resolvers that load relations
- [ ] New queries/mutations have authenticated + unauthenticated test cases
- [ ] `extensions.code` set on all `GraphQLError` throws (UNAUTHENTICATED, FORBIDDEN, BAD_USER_INPUT)
- [ ] Subscription handlers check authentication
- [ ] Input fields validated with Zod before passing to services
- [ ] No `any` in resolver return types — use generated types from codegen

---

## FORBIDDEN

- **NEVER** query Prisma inside resolvers — only call services or use DataLoaders
- **NEVER** share DataLoader instances across requests — always create per request in context
- **NEVER** use `context.prisma` directly in field resolvers — use `context.loaders`
- **NEVER** return raw database errors to the client — map to user-friendly `GraphQLError`
- **NEVER** skip the `extensions.code` on GraphQL errors — clients need machine-readable codes
- **NEVER** define types inline in resolvers — use SDL `.graphql` files and codegen
- **NEVER** use Apollo Server 3 patterns with AS4 — the context API changed
- **NEVER** use `graphql-subscriptions` PubSub in production with multiple instances — use Redis PubSub
- **NEVER** disable persisted queries in production (enable APQ for performance)
- **NEVER** expose introspection in production (`introspection: process.env.NODE_ENV !== 'production'`)
