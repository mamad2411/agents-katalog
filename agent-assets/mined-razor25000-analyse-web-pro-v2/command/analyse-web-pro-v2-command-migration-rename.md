---
description: Safely rename database tables/columns to avoid data loss
---

# Database Migration Rename

Safely rename database tables or columns using Prisma migrations to avoid data loss.

## Context

Prisma by default does NOT rename tables or properties; it deletes and re-creates them. This command helps avoid data loss by properly renaming instead.

## Problem

Prisma generates destructive migrations:

```sql
-- AlterTable
ALTER TABLE "Post" DROP COLUMN "content",
ADD COLUMN "markdown" TEXT NOT NULL;
```

## Solution

Use RENAME operations instead:

```sql
-- AlterTable
ALTER TABLE "Post" RENAME COLUMN "content" TO "markdown";
```

## Instructions

1. Review the generated migration file
2. Replace DROP/ADD operations with RENAME operations
3. Test the migration on a backup database first
4. Apply the migration with `pnpm prisma migrate deploy`

Fix migration for: $ARGUMENTS
