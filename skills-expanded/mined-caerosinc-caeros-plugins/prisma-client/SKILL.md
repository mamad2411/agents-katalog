---
name: prisma-client
description: Query with Prisma Client, typed CRUD, filtering, relations without N+1, transactions, aggregations, and error handling. Use when the user writes application code against a Prisma schema.
---

# Prisma Client

One `PrismaClient` instance per process. In hot-reload dev servers, cache it
on `globalThis` or every reload leaks a connection pool.

```ts
import { PrismaClient } from "@prisma/client"
const prisma = globalThis.prisma ?? new PrismaClient()
if (process.env.NODE_ENV !== "production") globalThis.prisma = prisma
```

## CRUD and filtering

```ts
await prisma.user.create({ data: { email: "a@b.co", posts: { create: [{ title: "Hi" }] } } })
await prisma.user.findUnique({ where: { email: "a@b.co" } })
await prisma.post.findMany({
  where: { published: true, title: { contains: "redis", mode: "insensitive" },
           author: { is: { role: "ADMIN" } } },
  orderBy: { createdAt: "desc" },
  take: 20, skip: 0,                       // offset paging; prefer cursor for deep pages
  select: { id: true, title: true, author: { select: { email: true } } },
})
await prisma.user.upsert({ where: { email }, update: { name }, create: { email, name } })
await prisma.post.updateMany({ where: { authorId }, data: { published: false } })
await prisma.user.createMany({ data: rows, skipDuplicates: true })
```

- `select` and `include` are mutually exclusive at the same level; `select`
  trims payloads, `include` adds full relations. `omit` drops sensitive
  fields (`omit: { password: true }`).
- Cursor pagination: `{ take: 20, skip: 1, cursor: { id: lastId } }`.
- Filters compose with `AND`/`OR`/`NOT`; relation filters use
  `some`/`every`/`none` on list relations.

## N+1 avoidance

The bug: loop over users, then query posts per user. Fixes, in order:

1. `include`/`select` the relation in the first query (Prisma batches this
   into a minimal number of queries).
2. `relationLoadStrategy: "join"` (Postgres/MySQL) pushes the fetch into a
   single SQL JOIN when the DB round trips dominate.
3. Fluent calls inside GraphQL resolvers,
   `prisma.user.findUnique({ where }).posts()`, are automatically batched by
   the client's dataloader; use that form instead of `post.findMany` per
   parent.
4. Last resort: one `findMany({ where: { authorId: { in: ids } } })` and
   group in memory.

## Transactions

```ts
// Batch: all-or-nothing list of independent writes
await prisma.$transaction([
  prisma.account.update({ where: { id: a }, data: { balance: { decrement: 100 } } }),
  prisma.account.update({ where: { id: b }, data: { balance: { increment: 100 } } }),
])

// Interactive: read-then-write logic inside one DB transaction
await prisma.$transaction(async (tx) => {
  const from = await tx.account.findUniqueOrThrow({ where: { id: a } })
  if (from.balance < 100) throw new Error("insufficient")
  await tx.account.update({ where: { id: a }, data: { balance: { decrement: 100 } } })
  await tx.account.update({ where: { id: b }, data: { balance: { increment: 100 } } })
}, { isolationLevel: "Serializable", timeout: 10_000 })
```

Keep interactive transactions short; a slow external call inside one holds a
DB connection hostage. Atomic counters (`increment`/`decrement`) often remove
the need for a transaction entirely.

## Aggregations and raw escape hatch

```ts
await prisma.post.count({ where: { published: true } })
await prisma.order.aggregate({ _sum: { total: true }, _avg: { total: true }, where })
await prisma.order.groupBy({ by: ["status"], _count: true, orderBy: { status: "asc" } })
await prisma.$queryRaw`SELECT date_trunc('month', "createdAt") m, sum(total) FROM "Order" GROUP BY 1`
```

`$queryRaw` as a tagged template is parameterized (safe);
`$queryRawUnsafe` with string concatenation is the SQL injection you were
warned about.

## Error handling

Catch `Prisma.PrismaClientKnownRequestError` and switch on `e.code`:

| Code | Meaning |
|---|---|
| P2002 | unique constraint violated (`e.meta.target` names fields) |
| P2025 | record not found (update/delete/`findUniqueOrThrow`) |
| P2003 | foreign key constraint failed |
| P2024 | connection pool timeout (see `prisma-troubleshooting`) |

Never string-match error messages; codes are stable, messages are not.
