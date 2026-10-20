---
alwaysApply: true
---
# Drizzle ORM Database Interactions

All database interactions in this project **must** use Drizzle ORM with the schema and queries defined in [src/db/schema.ts](mdc:src/db/schema.ts).

## Schema Location

- **Database schema**: [src/db/schema.ts](mdc:src/db/schema.ts)
- All table definitions are exported from this file
- Currently defined tables: `usersTable`

## Guidelines

### 1. Always Import from Schema

```typescript
import { usersTable } from "@/db/schema";
```

### 2. Use Drizzle Query Syntax

Always use Drizzle's query builder methods instead of raw SQL:

```typescript
// ✅ Correct - Use Drizzle queries
import { db } from "@/db";
import { usersTable } from "@/db/schema";
import { eq } from "drizzle-orm";

// Select
const users = await db.select().from(usersTable);
const user = await db.select().from(usersTable).where(eq(usersTable.id, 1));

// Insert
const newUser = await db.insert(usersTable).values({
  name: "John Doe",
  age: 30,
  email: "john@example.com"
}).returning();

// Update
await db.update(usersTable)
  .set({ age: 31 })
  .where(eq(usersTable.id, 1));

// Delete
await db.delete(usersTable).where(eq(usersTable.id, 1));
```

### 3. Never Use Raw SQL

```typescript
// ❌ Incorrect - Do not use raw SQL queries
await db.execute("SELECT * FROM users");
```

### 4. Type Safety

- Leverage Drizzle's type inference for type-safe queries
- Use `InferSelectModel` and `InferInsertModel` for type definitions:

```typescript
import { type InferSelectModel, type InferInsertModel } from "drizzle-orm";
import { usersTable } from "@/db/schema";

export type User = InferSelectModel<typeof usersTable>;
export type NewUser = InferInsertModel<typeof usersTable>;
```

### 5. Add New Tables to Schema

When creating new tables, always add them to [src/db/schema.ts](mdc:src/db/schema.ts) using Drizzle's table definition syntax.

## Database Connection

Ensure you have a properly configured database connection that exports a `db` instance using Drizzle's connection setup.

## Migration

Use Drizzle Kit for schema migrations:
- Generate migrations: `npx drizzle-kit generate`
- Run migrations: `npx drizzle-kit push` or `npx drizzle-kit migrate`
