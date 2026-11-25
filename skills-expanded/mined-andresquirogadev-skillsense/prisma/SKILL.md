# Prisma Skill

You are working with Prisma ORM. Apply these conventions.

## Schema (schema.prisma)

- Use `@@map("snake_case_table")` on models to keep DB tables in snake_case while Prisma models stay PascalCase.
- Use `@map("snake_case_col")` on fields for the same reason.
- Always add `@@index([field])` for columns used in `WHERE`, `ORDER BY`, or as foreign keys.
- Use `@db.Text` for long strings; use `@db.VarChar(255)` for constrained strings on PostgreSQL.
- Use `@updatedAt` for auto-updating timestamps.
- Use `enum` for fixed value sets; map to DB enums or use a string with `@db.VarChar`.

## Migrations

- Run `npx prisma migrate dev --name descriptive-name` during development — generates SQL and applies it.
- Run `npx prisma migrate deploy` in CI/production — never `migrate dev` in production.
- Never edit migration files by hand; instead, update schema and create a new migration.
- Use `npx prisma db push` for rapid prototyping when migration history doesn't matter.
- Introspect existing databases with `npx prisma db pull`.

## Prisma Client

- Instantiate a single PrismaClient and reuse it (module singleton pattern):
  ```ts
  // lib/prisma.ts
  import { PrismaClient } from '@prisma/client';
  const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };
  export const prisma = globalForPrisma.prisma ?? new PrismaClient();
  if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
  ```
- Always call `$disconnect()` in CLI scripts and tests; managed services handle it automatically.
- Use `$transaction([…])` for atomic operations or `$transaction(async (tx) => { … })` for interactive transactions.

## Queries

- Use `select` to fetch only needed fields — never over-fetch entire records.
- Use `include` for eager-loading relations; use nested `select` inside `include` to limit relation fields.
- Use `where: { id: { in: ids } }` for bulk lookups.
- Paginate with `skip` and `take`; use cursor-based pagination for large datasets.

## Type Safety

- Generated types from `@prisma/client` cover all models — use `Prisma.UserGetPayload<…>` for custom return types.
- Use `Prisma.validator<Prisma.UserUpdateInput>()` to narrow input types.
