---
name: db-migrate
description: Create and run Prisma database migrations
user_invocable: true
---

# Database Migration

When asked to create a migration:
1. Modify the Prisma schema in `prisma/schema.prisma`
2. Run `npx prisma migrate dev --name <migration_name>`
3. Verify the migration SQL looks correct
4. Run `npx prisma generate` to update the client
5. Update any affected TypeScript types
