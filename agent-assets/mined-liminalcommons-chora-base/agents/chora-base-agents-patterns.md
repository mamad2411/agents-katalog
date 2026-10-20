# SAP-034: React Database Integration - Common Patterns

**SAP**: SAP-034 (react-database-integration)
**Domain**: Patterns
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **3 common database patterns** for Next.js 15+ projects:

1. Database Seeding (Development/Testing) - Test data creation
2. Connection Pooling (Production) - Serverless optimization
3. Soft Deletes - Non-destructive data removal

**For ORM setup** (Prisma, Drizzle), see [../providers/AGENTS.md](../providers/AGENTS.md)

**For advanced workflows** (migrations, queries, RLS), see [../workflows/AGENTS.md](../workflows/AGENTS.md)

**For troubleshooting**, see [../troubleshooting/AGENTS.md](../troubleshooting/AGENTS.md)

---

## Pattern 1: Database Seeding (Development/Testing)

**Use Case**: Create test data for development and testing environments

**When to Use**:
- Setting up local development environment
- Populating staging database
- Creating fixtures for E2E tests

**When NOT to Use**:
- ❌ Production databases (risk of data corruption)
- ❌ User-facing environments

---

### Prisma Seed Script

Create `prisma/seed.ts`:

```typescript
// prisma/seed.ts

import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // Prevent seeding production
  if (process.env.NODE_ENV === 'production') {
    throw new Error('Cannot seed production database');
  }

  console.log('🌱 Seeding database...');

  // Create test users (upsert = create or update)
  const alice = await prisma.user.upsert({
    where: { email: 'alice@example.com' },
    update: {},
    create: {
      email: 'alice@example.com',
      name: 'Alice',
      posts: {
        create: [
          { title: 'Hello World', content: 'First post!', published: true },
          { title: 'Draft Post', content: 'Coming soon...', published: false },
        ],
      },
    },
  });

  const bob = await prisma.user.upsert({
    where: { email: 'bob@example.com' },
    update: {},
    create: {
      email: 'bob@example.com',
      name: 'Bob',
    },
  });

  console.log('✅ Seeded users:', alice, bob);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

**Add to package.json**:

```json
{
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  },
  "scripts": {
    "db:seed": "npx prisma db seed"
  }
}
```

**Run Seed**:

```bash
# Install tsx (TypeScript executor)
npm install -D tsx

# Run seed script
npm run db:seed

# Expected: "✅ Seeded users: ..."
```

**Features**:
- `upsert()` - Create if not exists, update if exists (idempotent)
- Nested creates - Create related records in single transaction
- Environment guard - Prevents accidental production seeding

---

### Drizzle Seed Script

Create `scripts/seed.ts`:

```typescript
// scripts/seed.ts

import { db } from '@/lib/db';
import { users, posts } from '@/lib/schema';
import { eq } from 'drizzle-orm';

async function main() {
  if (process.env.NODE_ENV === 'production') {
    throw new Error('Cannot seed production database');
  }

  console.log('🌱 Seeding database...');

  // Create test users (with conflict resolution)
  const [alice] = await db
    .insert(users)
    .values({ email: 'alice@example.com', name: 'Alice' })
    .onConflictDoUpdate({
      target: users.email,
      set: { name: 'Alice' },
    })
    .returning();

  // Create posts for Alice
  await db.insert(posts).values([
    { title: 'Hello World', content: 'First post!', published: true, authorId: alice.id },
    { title: 'Draft Post', content: 'Coming soon...', published: false, authorId: alice.id },
  ]);

  console.log('✅ Seeded users and posts');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => {
    process.exit(0);
  });
```

**Add to package.json**:

```json
{
  "scripts": {
    "db:seed": "tsx scripts/seed.ts"
  }
}
```

**Run Seed**:

```bash
# Install tsx
npm install -D tsx

# Run seed script
npm run db:seed

# Expected: "✅ Seeded users and posts"
```

**Features**:
- `onConflictDoUpdate()` - Upsert functionality
- Batch inserts - Insert multiple records efficiently
- Transaction safety - All operations succeed or all fail

---

## Pattern 2: Connection Pooling (Production)

**Use Case**: Optimize database connections for serverless environments (Vercel, Netlify, AWS Lambda)

**Why Needed**:
- Serverless functions create new connections per invocation
- Database has limited connection limit (e.g., 100-500 max)
- Without pooling, connection exhaustion occurs

**When to Use**:
- ✅ Production deployments
- ✅ Serverless environments
- ✅ High-traffic applications

---

### Supabase Pooler (Recommended)

**Environment Variables**:

`.env.production`:

```bash
# Pooled connection (for queries) - Port 6543
DATABASE_URL="postgres://postgres.xxx:PASSWORD@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# Direct connection (for migrations) - Port 5432
POSTGRES_URL_NON_POOLING="postgres://postgres.xxx:PASSWORD@aws-0-us-west-1.compute.amazonaws.com:5432/postgres"
```

**Why Two URLs?**:
- **Pooled (6543)**: For application queries (fast, shared connections)
- **Direct (5432)**: For migrations (requires exclusive connection)

---

### Prisma Configuration

```prisma
// prisma/schema.prisma

datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")               // Pooled (queries)
  directUrl = env("POSTGRES_URL_NON_POOLING")   // Direct (migrations)
}
```

**Behavior**:
- Queries use `DATABASE_URL` (pooled)
- Migrations use `directUrl` (direct)

---

### Drizzle Configuration

```typescript
// lib/db.ts

import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

// Use pooled connection in production
const connectionString = process.env.DATABASE_URL!;

// Configure connection pooling
const client = postgres(connectionString, {
  max: 1, // Max connections per serverless function
  idle_timeout: 20, // Close idle connections after 20s
  connect_timeout: 10, // Connection timeout 10s
});

export const db = drizzle(client, { schema });
```

**Pooling Benefits**:
- 90% reduction in connection overhead
- No connection exhaustion errors
- Automatic connection recycling

---

## Pattern 3: Soft Deletes

**Use Case**: Mark records as deleted without physically removing them from database

**Benefits**:
- Data recovery (undo delete)
- Audit trail (who deleted, when)
- Referential integrity preserved
- Compliance (data retention requirements)

**When to Use**:
- ✅ User accounts
- ✅ Important business data
- ✅ Multi-tenant applications
- ✅ Compliance requirements (GDPR, HIPAA)

**When to Use Hard Delete**:
- ❌ Truly sensitive data (passwords, tokens)
- ❌ GDPR "right to be forgotten" requests
- ❌ Storage-constrained databases

---

### Prisma Soft Delete

**Schema Update** (`prisma/schema.prisma`):

```prisma
model User {
  id        String    @id @default(cuid())
  email     String    @unique
  name      String?
  deletedAt DateTime? // NULL = active, Date = soft-deleted

  @@map("users")
}
```

**Implementation**:

```typescript
// Soft delete user
await prisma.user.update({
  where: { id: userId },
  data: { deletedAt: new Date() },
});

// Query only non-deleted users
const activeUsers = await prisma.user.findMany({
  where: { deletedAt: null },
});

// Restore soft-deleted user
await prisma.user.update({
  where: { id: userId },
  data: { deletedAt: null },
});
```

**Global Middleware** (auto-exclude soft-deleted records):

```typescript
// lib/db.ts

prisma.$use(async (params, next) => {
  // Exclude soft-deleted users from all queries
  if (params.action === 'findMany' && params.model === 'User') {
    params.args.where = {
      ...params.args.where,
      deletedAt: null,
    };
  }

  return next(params);
});
```

**Benefits of Middleware**:
- No need to add `deletedAt: null` to every query
- Centralized logic (single source of truth)
- Prevents accidental inclusion of deleted records

---

### Drizzle Soft Delete

**Schema Update** (`lib/schema.ts`):

```typescript
export const users = pgTable('users', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 255 }),
  deletedAt: timestamp('deleted_at'), // NULL = active, Date = soft-deleted
});
```

**Implementation**:

```typescript
import { isNull, isNotNull } from 'drizzle-orm';

// Soft delete user
await db
  .update(users)
  .set({ deletedAt: new Date() })
  .where(eq(users.id, userId));

// Query only non-deleted users
const activeUsers = await db
  .select()
  .from(users)
  .where(isNull(users.deletedAt));

// Query only deleted users
const deletedUsers = await db
  .select()
  .from(users)
  .where(isNotNull(users.deletedAt));

// Restore soft-deleted user
await db
  .update(users)
  .set({ deletedAt: null })
  .where(eq(users.id, userId));
```

**Best Practices**:
- Always add index on `deletedAt` for performance
- Document soft delete behavior in API documentation
- Consider hard delete after retention period (e.g., 90 days)

---

## Version History

**1.0.0 (2025-11-10)** - Initial patterns extraction from awareness-guide.md
- Pattern 1: Database Seeding (Development/Testing)
- Pattern 2: Connection Pooling (Production)
- Pattern 3: Soft Deletes
- Complete code examples for both Prisma and Drizzle
