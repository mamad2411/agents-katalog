---
description: Creating / Updating schemas, queries, actions, migrations, generations, sql
globs: 
alwaysApply: false
---
# Data Verification: 
- Use Supabase Tool to get real data and structure of our tables/schemas and check your assumptions when debugging.

# New Schema Creation:
- Include new schemas in @drizzle.config.ts (one schema at a time)
- After adding a schema, first delete the Migration folder with old schemas; then run "npm run db:generate" followed by "npm run db:migrate"

# Schema Modifications:
- For existing schema edits, provide pure SQL commands for Supabase editor
- Example: ALTER TABLE "wb-abc" ADD COLUMN IF NOT EXISTS "previous_week_3_sales" integer DEFAULT 0
- Do not provide SQL migrations or terminal commands

# CRUD
- When adding queries use queries/actions layer unless it's an exception

#### Database Structure and Flow
1. Create schema first: `/db/schema/[name]-schema.ts`
   - Export in `/db/schema/index.ts`
   - Add to schema in `/db/db.ts`
2. Create queries next: `/db/queries/[name]-queries.ts`
   - All database operations go here
   - Return `ActionResult` type
   - Handle try/catch blocks
3. Create actions last: `/actions/[name]-actions.ts`
   - Server actions wrap queries
   - Never write DB logic here
   - Only handle data passing and validation

`example-schema.ts` with the following code:

```ts
import { integer, pgTable, text, timestamp, uuid } from "drizzle-orm/pg-core";

export const exampleTable = pgTable("example", {
  id: uuid("id").defaultRandom().primaryKey(),
  name: text("name").notNull(),
  age: integer("age").notNull(),
  email: text("email").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at")
    .notNull()
    .defaultNow()
    .$onUpdate(() => new Date())
});

export type InsertExample = typeof exampleTable.$inferInsert;
export type SelectExample = typeof exampleTable.$inferSelect;
```

#### Drizzle config
import { config } from "dotenv"
import { defineConfig } from "drizzle-kit"

// Load environment variables from .env.local file
config({ path: ".env.local" })

// Export Drizzle ORM configuration
export default defineConfig({
  // Path to your schema files that define database tables and relationships
  schema: [
    "./db/schema/import-tasks-schema.ts" // example
  ],
  
  // Output directory for generated SQL migrations
  out: "./db/migrations",
  
  // Specify the database dialect as PostgreSQL
  dialect: "postgresql",
  
  // Database connection credentials
  // The ! operator asserts that DATABASE_URL will be defined in .env.local
  dbCredentials: {
    url: process.env.DATABASE_URL!
  }
}) 

#### Database Setup
- Create `/db/db.ts` with the following structure:

```typescript
import { config } from "dotenv"
import { defineConfig } from "drizzle-kit"

// Load environment variables from .env.local file
config({ path: ".env.local" })

// Export Drizzle ORM configuration
export default defineConfig({
  // Path to your schema files that define database tables and relationships
  schema: "./db/schema/wb-abc-schema.ts",
  
  // Output directory for generated SQL migrations
  out: "./db/migrations",
  
  // Specify the database dialect as PostgreSQL
  dialect: "postgresql",
  
  // Database connection credentials
  // The ! operator asserts that DATABASE_URL will be defined in .env.local
  dbCredentials: {
    url: process.env.DATABASE_URL!
  }
})```

Required environment variables:
- `DATABASE_URL`: Supabase connection string

Required package.json scripts:

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate"
  }
}
```

Notes:
- Import schemas from `./schema` as they're created
- Add each schema to the schema object
- Use `.env.local` for environment variables
- Run migrations after schema changes:
  ```bash
  
  npm run db:generate
  npm run db:migrate