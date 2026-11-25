# Drizzle ORM Skill

You are working with Drizzle ORM. Apply these conventions.

## Schema Definition

- Define schemas in `src/db/schema.ts` using Drizzle's table helpers:
  ```ts
  import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';
  export const users = pgTable('users', {
    id: serial('id').primaryKey(),
    email: text('email').notNull().unique(),
    createdAt: timestamp('created_at').defaultNow().notNull(),
  });
  ```
- Export all table definitions; Drizzle infers TypeScript types automatically.
- Use `$inferSelect` and `$inferInsert` for type inference:
  ```ts
  export type User = typeof users.$inferSelect;
  export type NewUser = typeof users.$inferInsert;
  ```

## Database Client

- Create `src/db/index.ts` as the singleton connection:
  ```ts
  import { drizzle } from 'drizzle-orm/postgres-js';
  import postgres from 'postgres';
  import * as schema from './schema.js';
  const queryClient = postgres(process.env.DATABASE_URL!);
  export const db = drizzle(queryClient, { schema });
  ```
- For serverless environments, use `drizzle-orm/neon-http` or `drizzle-orm/vercel-postgres`.

## Migrations

- Configure `drizzle.config.ts` at the project root.
- Generate migrations: `npx drizzle-kit generate`.
- Apply migrations: `npx drizzle-kit migrate`.
- Inspect schema drift: `npx drizzle-kit check`.

## Queries

- Use the query builder with full type safety:
  ```ts
  const user = await db.select().from(users).where(eq(users.id, id)).limit(1);
  const result = await db.query.users.findFirst({ where: eq(users.id, id), with: { posts: true } });
  ```
- Prefer the `db.query` relational API for queries that include relations.
- Use `db.insert(table).values({ … }).returning()` to get inserted rows back.
- Use `db.transaction(async (tx) => { … })` for atomic operations.

## Indexes & Relations

- Define relations with `relations()` helper — used by the relational query API, not the DB schema itself.
- Add DB indexes in the table definition: `index('email_idx').on(table.email)`.
