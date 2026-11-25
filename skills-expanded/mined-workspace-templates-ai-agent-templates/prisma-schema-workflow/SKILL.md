---
name: prisma-schema-workflow
description: Evolves a Prisma schema safely with named migrations, seed scripts, type-safe queries and a check for destructive changes.
---

# Prisma schema workflow

Treat `schema.prisma` and the migration SQL as reviewed code.

## Steps

1. Read `schema.prisma`, the latest migrations and `package.json` scripts. Confirm which database and whether migrations are used (`prisma migrate`) or push (`db push`). Do not mix them on one database.
2. Edit the schema: explicit `@id`, `@unique`, `@@index` for each foreign key and filter, relation names when a model has two relations to another, and `onDelete` behavior stated rather than default.
3. Generate the migration with `npx prisma migrate dev --name add_invoice_status` using a descriptive name. Use `--create-only` when the change needs hand edits.
4. Open the generated `migration.sql` and read it. Stop and ask before any `DROP`, a type change, or a new required column on a populated table. For the latter, add it optional, backfill, then make it required in a later migration.
5. Run `npx prisma generate` and fix type errors; they are the list of code to update.
6. Write queries with `select` or `include` for only what the caller needs. Use `$transaction` for related writes, and `createMany` for bulk inserts.
7. Keep `prisma/seed.ts` idempotent with `upsert`, and run it with `prisma db seed`.
8. In CI and production use `prisma migrate deploy`, never `migrate dev`.

## Rules

- Never edit a migration that has already been applied elsewhere; add a new one.
- On drift, run `migrate diff` to see it before any reset, and never reset a shared database.

## Report

The schema diff, the migration SQL highlights, code changes and how you verified them.
