---
description: Run Database Schema Integrity and Migration Safety Checks
globs: ["prisma/schema.prisma", "**/migrations/**/*.sql", "**/migrations/**/*.ts"]
---
# Data: Schema Integrity & Migration Safety

<audit_rules>
- You MUST verify that all database migrations are backward compatible. Destructive operations (dropping tables, renaming columns without retaining the old one) MUST include a clear rollout plan.
- You MUST ensure every schema change includes an application-level plan to handle data drift between deployment phases (e.g., writing to both old and new columns temporarily).
- You MUST verify that referential integrity is maintained via foreign keys (`@relation` in Prisma) and cascading deletes are used thoughtfully to prevent orphaned records.
- You MUST enforce soft-delete patterns (e.g., adding a `deletedAt` DateTime column) instead of hard deletes (`DELETE FROM`) for critical business data (e.g., users, orders).
- You MUST verify that Prisma configurations utilize connection pooling (e.g., Prisma Accelerate or PgBouncer) for serverless environments.
</audit_rules>

<example_good>
```prisma
// Soft delete pattern with referential integrity
model User {
  id        String    @id @default(cuid())
  email     String    @unique
  deletedAt DateTime? // Soft delete flag
  orders    Order[]
}

model Order {
  id        String   @id @default(cuid())
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Restrict)
}
```
</example_good>

<example_bad>
```sql
-- BAD: Destructive migration that will cause downtime during deployment
ALTER TABLE "User" DROP COLUMN "email";
ALTER TABLE "User" ADD COLUMN "emailAddress" VARCHAR(255);
```
</example_bad>

