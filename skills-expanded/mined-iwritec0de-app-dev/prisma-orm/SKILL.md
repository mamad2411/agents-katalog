---
name: prisma-orm
description: >-
  Prisma ORM expertise for schema design, migrations, client usage, and deployment.
  Use when writing Prisma schemas, creating migrations, querying with Prisma Client,
  defining relations, or deploying database changes. Triggers on "prisma", "prisma schema",
  "prisma migrate", "prisma client", "prisma relation", "@@map", "@@index",
  "prisma generate", "prisma studio", "prisma deploy".
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Prisma ORM Skill

You are a Prisma ORM expert for TypeScript applications.

## Critical Rules

- **Run `prisma generate` after schema changes** — the client is code-generated, not runtime
- **Use `migrate dev` in development** — creates migration files and applies them
- **Use `migrate deploy` in production** — applies pending migrations without creating new ones
- **Never use `db push` in production** — it doesn't create migration files and can lose data
- **Name relations explicitly** — when a model has multiple relations to the same target
- **Add `@@index` for query performance** — Prisma doesn't auto-create indexes on FKs
- **Use transactions for multi-step operations** — `prisma.$transaction()` for consistency

## Schema Design

```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  @@map("users")
  @@index([email])
}

model Post {
  id       String @id @default(uuid())
  title    String
  content  String?
  author   User   @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId String @map("author_id")

  @@map("posts")
  @@index([authorId])
}
```

Key attributes: `@id`, `@unique`, `@default()`, `@map()`, `@relation()`, `@@map()`, `@@index()`, `@@unique()`. Read `reference/schema-patterns.md` for all types and patterns.

## Relations

| Type | Schema Pattern |
|------|---------------|
| One-to-One | FK with `@unique` on one side, optional `?` field on other |
| One-to-Many | FK on "many" side, array `[]` on "one" side |
| Many-to-Many (implicit) | Array `[]` on both sides, Prisma creates junction table |
| Many-to-Many (explicit) | Junction model with two `@relation` fields |
| Self-relation | Model references itself (e.g., `parent`/`children`) |

## Client Usage

```typescript
// Create with relation
const user = await prisma.user.create({
  data: { email: 'a@b.com', name: 'Alice', posts: { create: { title: 'Hello' } } },
  include: { posts: true },
});

// Query with filtering
const posts = await prisma.post.findMany({
  where: { author: { email: { contains: '@company.com' } } },
  orderBy: { createdAt: 'desc' },
  take: 20,
  skip: 0,
  select: { id: true, title: true, author: { select: { name: true } } },
});

// Cursor pagination (preferred over offset)
const next = await prisma.post.findMany({
  cursor: { id: lastId },
  skip: 1,
  take: 20,
  orderBy: { id: 'asc' },
});
```

Read `reference/client-patterns.md` for CRUD recipes, nested writes, transactions, and error handling.

## Migrations

```bash
# Development: create and apply migration
npx prisma migrate dev --name add_user_table

# Production: apply pending migrations
npx prisma migrate deploy

# Reset database (development only)
npx prisma migrate reset

# Generate client after schema change
npx prisma generate

# Browse database
npx prisma studio
```

Read `reference/migration-workflow.md` for CI/CD integration, handling drift, and rollback strategies.

## Advanced

- **Raw queries** — `prisma.$queryRaw` for complex SQL not supported by client
- **Transactions** — `prisma.$transaction([...])` for sequential, or `prisma.$transaction(async (tx) => {...})` for interactive
- **Middleware** — `prisma.$use()` for logging, soft delete, audit trails
- **Connection pooling** — use `pgbouncer=true` in connection string for serverless

## Anti-Patterns

- **Don't use `db push` in prod** — no migration history, can drop columns
- **Don't skip `@@index`** — Prisma doesn't auto-index foreign keys
- **Don't fetch all fields** — use `select` to reduce payload
- **Don't ignore N+1** — use `include` to eager-load relations
- **Don't edit migration files** — create new migrations to fix issues
- **Don't use `prisma migrate dev` in CI** — use `prisma migrate deploy`

## Related

- `reference/schema-patterns.md` — Model patterns, field types, attributes, enums, multi-file schemas
- `reference/client-patterns.md` — CRUD recipes, filtering, transactions, raw SQL, error handling
- `reference/migration-workflow.md` — Dev vs prod workflow, seeding, CI/CD, rollback
