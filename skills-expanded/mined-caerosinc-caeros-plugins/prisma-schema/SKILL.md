---
name: prisma-schema
description: Model data in schema.prisma, fields, relations, indexes, enums, and the migrations workflow (migrate dev, deploy, db push). Use when the user edits a Prisma schema or manages migrations.
---

# Prisma Schema and Migrations

## Anatomy

```prisma
datasource db {
  provider = "postgresql"          // also mysql, sqlite, sqlserver, mongodb, cockroachdb
  url      = env("DATABASE_URL")   // never hardcode; keep in .env (gitignored)
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  role      Role     @default(MEMBER)
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String  @id @default(cuid())
  title     String
  published Boolean @default(false)
  author    User    @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId  String

  @@index([authorId, published])
}

enum Role { MEMBER ADMIN }
```

After every schema change run `npx prisma generate` (usually implied by
`migrate dev`) so the typed client matches.

## Relations cheat sheet

- **1-n**: array field on the one side (`posts Post[]`), scalar FK +
  `@relation(fields, references)` on the many side. Both sides must exist.
- **1-1**: make the FK `@unique` on the owning side.
- **m-n implicit**: `tags Tag[]` on both models; Prisma manages the join
  table. Use an explicit join model instead when you need extra columns
  (e.g. `assignedAt`) on the relation.
- **Self-relations**: name them, `@relation("ManagerReports")` on both sides.
- `onDelete`: `Cascade`, `SetNull`, `Restrict`. The default for required
  relations effectively blocks parent deletion; choose deliberately.

Constraints and indexes: `@unique`, `@@unique([a, b])`, `@@index([a, b])`,
`@map("db_column")` / `@@map("db_table")` to keep DB snake_case with Prisma
camelCase. Postgres-specific types via `@db.Text`, `@db.Uuid`, `@db.JsonB`.

## Migrations workflow

Development (against a dev database only):

```bash
npx prisma migrate dev --name add-posts   # diff schema, create SQL migration, apply, regenerate client
npx prisma migrate dev --create-only      # write SQL to review/edit BEFORE applying
npx prisma migrate status
```

Production/CI:

```bash
npx prisma migrate deploy                 # applies pending migrations, never generates or resets
```

Rules that prevent pain:
- Commit the whole `prisma/migrations/` directory; never edit an applied
  migration file.
- `migrate dev` may RESET the database when history and DB disagree; that is
  why it refuses to run against production.
- Hand-edit generated SQL (via `--create-only`) for data backfills, custom
  indexes (`CREATE INDEX CONCURRENTLY`), or renames (Prisma sees a rename as
  drop + add; rewrite it as `ALTER TABLE ... RENAME COLUMN`).

## db push vs migrate

`npx prisma db push` syncs schema to DB with no migration files: right for
prototyping and schemaless-ish early development. Once real data or a second
environment exists, switch to migrations and baseline (see
`prisma-troubleshooting`). Do not mix both against the same database.

## Introspection (existing database first)

```bash
npx prisma db pull        # writes models from the live DB into schema.prisma
npx prisma generate
```

Then adopt migrations by baselining the current state.

## Tooling

- `npx prisma studio`: browser GUI over your data.
- `npx prisma validate` and `npx prisma format`: CI-friendly schema checks.
- The Prisma MCP server in this plugin exposes migrate-status, migrate-dev,
  and migrate-reset as tools, plus documentation search; reach for the docs
  tool when a schema attribute looks off, the syntax evolves.
