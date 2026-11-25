---
name: follow-lib-tanstack-db
description: Use TanStack DB end to end — collections, live queries, optimistic mutations, sync backends, joins
argument-hint: "[framework] [sync-backend]"
related:
  - follow-lib-tanstack-ecosystem
  - run-test
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack DB fully — a reactive client store: collections, live queries (filter/join/order), optimistic mutations, sync engines (Query, ElectricSQL, localStorage, local-only)

## Scope

Use when you need a local-first/reactive data layer that queries client-side like a DB — versus `follow-query` (plain server cache) — **0.x**: the API may change, check the latest docs before implementing

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install Packages

> Goal: core + framework adapter + collection driver

1. `bun add @tanstack/db @tanstack/react-db` (React; `vue-db`/`solid-db`/`svelte-db` also exist)
2. Pick the driver per backend:
   - REST/Query sync → `bun add @tanstack/query-db-collection`
   - ElectricSQL realtime sync → `bun add @tanstack/electric-db-collection`
   - localStorage persist → `localStorageCollectionOptions` from `@tanstack/db`
   - in-memory only → `localOnlyCollectionOptions`

### 2. Create Collections

> Goal: typed collections synced with the backend

```ts
import { createCollection } from '@tanstack/react-db'
import { queryCollectionOptions } from '@tanstack/query-db-collection'

export const todosCollection = createCollection(
  queryCollectionOptions({
    queryClient,
    queryKey: ['todos'],
    queryFn: () => fetch('/api/todos').then((r) => r.json()),
    getKey: (t) => t.id,
    onInsert: async ({ transaction }) => { /* POST → server */ },
    onUpdate: async ({ transaction }) => { /* PATCH */ },
    onDelete: async ({ transaction }) => { /* DELETE */ },
    schema: todoSchema,  // zod/standard schema → runtime + type safety
  }),
)
```

- `electricCollectionOptions({ shape: { url, params } })` for ElectricSQL — realtime push
- `localStorageCollectionOptions({ storageKey })` — offline persistence
- `startSync`/eager vs lazy sync per the options

### 3. Live Queries

> Goal: reactive queries like a DB

```ts
import { useLiveQuery, eq, gt } from '@tanstack/react-db'

const { data, isLoading } = useLiveQuery((q) =>
  q.from({ todo: todosCollection })
   .join({ todo: todosCollection }, ({ todo }) => eq(todo.listId, list.id))  // joins
   .where(({ todo }) => gt(todo.priority, 0))
   .orderBy(({ todo }) => todo.createdAt, 'desc')
   .select(({ todo }) => ({ id: todo.id, title: todo.title })),
)
```

- Operators: `eq`, `gt`, `lt`, `like`, `inArray`, `and`, `or` — imported from the adapter
- `groupBy` + aggregates (`count`, `sum`, `avg`) for summary queries
- Multi-collection joins — the live query re-evaluates when any collection changes
- Non-hook usage: `liveQueryCollectionOptions` builds a reusable derived collection

### 4. Mutations (Optimistic)

> Goal: writes the UI sees immediately

1. `collection.insert(item)` / `collection.update(key, (d) => {...})` / `collection.delete(key)` — automatically optimistic
2. Transaction API: `mutationFn` in `useOptimisticMutation`/`createOptimisticAction` for custom flows
3. Write handlers (`onInsert`/`onUpdate`/`onDelete`) persist to the server — on failure → auto rollback
4. Pending states: `tx.state`/`isPersisted` track whether the mutation has synced yet

### 5. Verify

> Goal: sync + optimistic + joins really work

1. `/run-typecheck` + `/run-test`
2. Mutation: the UI changes immediately → server confirms → rollback on error
3. The live query re-renders when the collection changes; the multi-collection join updates correctly
4. On failure → `/resolve-errors` max 3 rounds

## Rules

- `getKey` must be stable + unique — never use the array index
- The collection driver must match the backend; Query-backed needs the app's same `queryClient`
- Add a `schema` (standard schema) on the collection — you get types + runtime validation
- Use DB only for data needing live query/optimistic/local-first — plain fetching still uses `follow-query`
- 0.x API — pin the version, read the changelog before upgrading
- Use `/follow-lib-tanstack-ecosystem` for the overview

## Expected Outcome

- Collections sync with the chosen backend driver
- Live queries (filter/join/aggregate) react correctly
- Optimistic mutations + rollback work
