---
name: database-sql
description: SQL database standards using Prisma + PostgreSQL — schema design, migrations, query patterns, transactions, indexing, what to avoid. Load when writing or reviewing any database schema, Prisma queries, or migration files.
user-invocable: false
stack: database/postgres-prisma
paths:
  - "**/prisma/**"
  - "**/schema.prisma"
  - "**/migrations/**"
  - "**/*.repository.*"
  - "**/*.sql"
---

Full standards in [sql.md](sql.md). Always-on summary:

> **Scope — applies only if this project uses postgres-prisma.** This layer shares `**/*.repository.*`, `**/*.sql`, `**/migrations/**` with `dynamodb`, `neon` in `layers/database/`, so more than one may load at once and their rules conflict. If the project is not using postgres-prisma, ignore this layer.
> See `docs/adr/0001-layer-glob-collision-and-dispatcher-routing-policy.md`.

**Stack:** PostgreSQL + Prisma ORM

**Schema rules:**
- Every table has `id` (cuid/uuid), `createdAt`, `updatedAt`
- Soft deletes with `deletedAt DateTime?` — never hard delete user data
- Foreign keys always explicit with `onDelete` behaviour defined
- snake_case for column names (`@@map`), PascalCase for Prisma models

**Query rules:**
- Never raw SQL unless Prisma cannot express it — use `$queryRaw` with tagged templates only
- Always select only needed fields — `findMany({ select: { id: true, name: true } })` — never `findMany(` without `select:` on large tables
- N+1 is never acceptable — use `include` or `select` with nested relations
- Wrap multi-step operations in `prisma.$transaction()`

**Safe migrations — expand-contract pattern** (required for any rename, removal, or type change on a live table):
1. **Expand** — add new column (nullable), dual-write in app, deploy
2. **Migrate** — backfill existing rows in batches (≤1000 rows/query), add NOT NULL with `NOT VALID` + `VALIDATE` to avoid table lock
3. **Contract** — remove old column after confirming zero references in running code

```bash
# Never drop a column without deploying the app change first
# Always diff before applying to production
npx prisma migrate diff --from-schema-datasource prisma/schema.prisma --to-schema-datamodel prisma/schema.prisma --script
grep -E 'DROP COLUMN|NOT NULL|ALTER TYPE' prisma/migrations/*/migration.sql   # flag for review
```

**Never:**
- Store passwords in plaintext (use bcrypt/argon2)
- Store tokens or secrets in the database without hashing
- Delete rows that have audit/compliance value — use soft deletes
- Run migrations in application startup code
- Use `deleteMany` without a `where` clause
- Apply a breaking schema change (rename/drop/type change) in a single deploy — always use expand-contract


**Related skills — apply together:**
- `error-handling` — Prisma P2002/P2025 map to ConflictError/NotFoundError in errorHandler
- `typescript-patterns` — type repository return values and Zod-inferred input types
- `api-conventions` — cursor pagination contract used in repositories matches the API response shape
- `security` — never raw SQL with string interpolation; always parameterized via Prisma