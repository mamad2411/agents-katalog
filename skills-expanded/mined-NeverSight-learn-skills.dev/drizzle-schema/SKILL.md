---
name: drizzle-schema
description: "[Pragmatic DDD Architecture] Guide for creating PostgreSQL tables and defining relations using Drizzle ORM. Use when creating new schemas, managing PostgreSQL indexes, enums, mapping column names to camelCase for the domain, and explicitly exporting constraint names."
---

# PostgreSQL Schemas with Drizzle ORM

## 1. Core Principles

All database schemas for this project are monolithic and centrally located within **`src/shared/infrastructure/drizzle-postgres/schema.ts`**. No exceptions.

- **Monolithic Schema**: Do not create distributed schema files across Bounded Contexts. All `pgTable`, `pgEnum`, and `relations` are defined in the central file to prevent circular dependencies in Drizzle queries.
- **Naming Conventions**: DB tables must be `snake_case` (e.g., `audit_logs`). TypeScript variables must be `camelCase` (e.g., `auditLogs`).
- **Column Names**: Define explicit `snake_case` names when initializing columns `uuid("folder_id")` and map them to `camelCase` for the application layer.
- **Timestamp Standard**: All tables should at minimum contain `createdAt` (with `.defaultNow().notNull()`) and, when mutable, `updatedAt` (with `.$onUpdate(...)`).
- **Enums**: Use explicit `pgEnum("enum_name", [...])` rather than Native PostgreSQL types for application enums.

## 2. Table Definition Format

Always follow this structure when defining a new table, including explicit foreign key cascades.

```typescript
import {
  pgTable,
  uuid,
  varchar,
  text,
  timestamp,
  uniqueIndex,
} from "drizzle-orm/pg-core";

// 1. Dependent Tables (Foreign Keys)
export const workspaces = pgTable("workspaces", {
  id: uuid().primaryKey(),
  name: varchar({ length: 40 }).notNull(),
  ownerId: uuid("owner_id").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// 2. Main Table & References
export const folders = pgTable(
  "folders",
  {
    id: uuid().primaryKey(),
    // Explicit snake_case -> camelCase mapping, with onDelete behavior
    workspaceId: uuid("workspace_id")
      .references(() => workspaces.id, { onDelete: "cascade" })
      .notNull(),
    name: varchar({ length: 30 }).notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
  },
  // 3. Composite unique indexes
  (table) => [uniqueIndex().on(table.workspaceId, table.name)],
);
```

## 3. Explicit Constraint Names (Crucial)

To map infrastructure errors (like `UniqueConstraintViolation`) to domain errors cleanly in our Repositories, Drizzle requires explicit constraint name tracking. 
Always export constraint constants at the bottom of the file using Drizzle's `getTableName` utility.

```typescript
import { getTableName } from "drizzle-orm";

// ─── Constraint name constants ───
export const FK_FOLDERS_WORKSPACE =
  `${getTableName(folders)}_${folders.workspaceId.name}_${getTableName(workspaces)}_${workspaces.id.name}_fk` as const;

export const UNIQUE_FOLDERS_WORKSPACE_NAME =
  `${getTableName(folders)}_${folders.workspaceId.name}_${folders.name.name}_index` as const;
```

## 4. Better Auth Integration (Auth Schema)

This project uses **Better Auth** for authentication, which natively integrates with Drizzle. Do NOT create Auth tables manually from scratch.

1. **CLI Generation**: When updating or initializing Auth schemas, use the Better Auth CLI to automatically generate the necessary boilerplate setup.
2. **Monolithic Copy**: Do NOT leave the generated schema in a standalone Auth file. Copy the final generated output directly into our unified `schema.ts`.
3. **Custom Fields Extension**: If you must add custom domain-specific fields to the Better Auth base tables (like `users` or `sessions`), structure the table by separating the generated fields from your custom fields using a clear comment logic:

```typescript
export const users = pgTable("users", {
  // Better-auth generated
  id: uuid("id").primaryKey(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  emailVerified: boolean("email_verified").default(false).notNull(),
  image: text("image"),
  
  // Custom columns
  plan: subscriptionPlanEnum("subscription_plan").default("free").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

## 5. Workflows

- Run `npm run db:generate` to use Drizzle-kit to create SQL migrations after updating `schema.ts`.
- Run `npm run db:push` or apply the migrations depending on the environment.
- Run `npm run db:studio` for visual inspection via Drizzle Studio.
- The `schema.ts` file acts as the source of truth for the `drizzle.config.ts`.
- Repositories import this schema directly to query or write properties correctly separated from domain objects.