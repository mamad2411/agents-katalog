---
name: prisma-postgresql-schema
description: >
  Analyze, build, and structure PostgreSQL table data using Prisma ORM. Use this
  skill whenever the user wants to: design or review Prisma schemas, create or
  refactor Prisma models, define relationships (1-1, 1-N, N-M), generate Prisma
  migrations, reverse-engineer existing schemas into Prisma format, audit Prisma
  model structures, or build typed data models from raw definitions using Prisma.
  Trigger on keywords like "prisma", "schema.prisma", "prisma model", "prisma
  migrate", "datasource", "generator", "relation", "@relation", "@@index",
  "@@unique", "prisma client", "tabela prisma", "modelo prisma", or any request
  to design, inspect, or generate Prisma schema for PostgreSQL. Also trigger when
  the user pastes raw Prisma SDL, a list of fields, or asks to convert SQL DDL to
  Prisma. Always use this skill over any generic postgresql-schema skill when
  Prisma is involved.
allowed-tools: Read, Write, Glob, Grep, Agent
---

# Prisma + PostgreSQL Schema Skill

Skill for analyzing, building, and structuring Prisma schemas targeting PostgreSQL.
Covers model design, relation mapping, migration generation, and type output.

---

## Workflow

### 1. Identify the task type

| Task | Description |
|---|---|
| **Analyze** | User provides existing `schema.prisma` — review structure, spot issues |
| **Build** | User describes what they need — generate Prisma models from scratch |
| **Structure** | User provides raw fields or SQL DDL — convert and normalize to Prisma |
| **Migrate** | Diff between old and new schema — generate safe migration |
| **Type Models** | Generate TypeScript types / Zod schemas from Prisma models |
| **Relations** | Design or fix 1-1, 1-N, N-M relationships in Prisma |

---

### 2. Prisma file header (always include)

Every `schema.prisma` starts with:

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

---

### 3. Analyze mode

When given an existing `schema.prisma`:

- Check for missing `@@index` on relation fields (FK columns)
- Flag models missing `createdAt` / `updatedAt`
- Verify naming conventions (PascalCase models, camelCase fields)
- Check relation completeness (both sides of `@relation` defined)
- Spot missing `onDelete` / `onUpdate` policies
- Flag `String` fields that should be `enum`
- Check UUID vs auto-increment consistency
- Detect missing `@@unique` constraints where applicable
- Flag optional fields (`?`) that should be required

Output format: structured audit report per issue:
- **Issue**: What's wrong
- **Location**: `Model.field`
- **Fix**: Suggested Prisma SDL

---

### 4. Build mode

When generating models from scratch:

**Standard base fields for every model:**
```prisma
model Example {
  id        String   @id @default(uuid()) @db.Uuid
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

**Naming conventions:**
- Models: PascalCase, singular (`User`, `WalletTransaction`)
- Fields: camelCase (`walletAddress`, `isActive`)
- Enums: PascalCase, values in SCREAMING_SNAKE_CASE
- Relation fields: camelCase, named after the related model

**Index rules:**
- Always add `@@index` on relation fields (`userId`, `walletId`, etc.)
- Add `@@index` on fields used in `where`, `orderBy`, or `include` frequently
- Use `@@unique` for natural unique keys (email, slug, etc.)

**Enum pattern:**
```prisma
enum UserRole {
  ADMIN
  USER
  MODERATOR
}

model User {
  role UserRole @default(USER)
}
```

---

### 5. Relations

Read `/references/relations.md` for full patterns on each relation type.

Quick reference:

**1-to-many:**
```prisma
model User {
  id    String  @id @default(uuid()) @db.Uuid
  posts Post[]
}

model Post {
  id     String @id @default(uuid()) @db.Uuid
  userId String @db.Uuid
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
}
```

**Many-to-many (explicit join table — preferred):**
```prisma
model Post {
  id   String      @id @default(uuid()) @db.Uuid
  tags PostToTag[]
}

model Tag {
  id    String      @id @default(uuid()) @db.Uuid
  posts PostToTag[]
}

model PostToTag {
  postId String @db.Uuid
  tagId  String @db.Uuid
  post   Post   @relation(fields: [postId], references: [id], onDelete: Cascade)
  tag    Tag    @relation(fields: [tagId], references: [id], onDelete: Cascade)

  @@id([postId, tagId])
  @@index([tagId])
}
```

**onDelete policies:**
| Policy | Use when |
|---|---|
| `Cascade` | Child should be deleted with parent |
| `Restrict` | Block parent delete if children exist |
| `SetNull` | Nullify FK on parent delete (field must be optional) |
| `NoAction` | DB-level default |

---

### 6. Structure / Convert mode

When converting SQL DDL → Prisma:

1. Map SQL types → Prisma types (see `/references/type-mappings.md`)
2. Convert `FOREIGN KEY` → `@relation` with proper `fields`/`references`
3. Convert `UNIQUE` constraints → `@@unique`
4. Convert `INDEX` → `@@index`
5. Replace `SERIAL` → `@default(autoincrement())`
6. Replace `gen_random_uuid()` → `@default(uuid())`
7. Add `@db.*` type hints when precision/type matters

---

### 7. Migrate mode

When the user wants to generate or apply migrations:

**Step 1 — Classify the risk:**

| Risk | Examples |
|---|---|
| **LOW** | New model, new optional field, new index |
| **MEDIUM** | Adding required field with default, renaming |
| **HIGH** | Removing field/model, changing type, required field without default |

**Step 2 — Generate migration SQL for review:**

```sql
-- Migration: <short description>
-- Prisma equivalent: prisma migrate dev --name <migration_name>
-- Risk: LOW / MEDIUM / HIGH

BEGIN;
ALTER TABLE "users" ADD COLUMN "display_name" TEXT;
CREATE INDEX CONCURRENTLY "idx_users_display_name" ON "users"("display_name");
COMMIT;
```

**Step 3 — Confirm with the user** before executing (especially MEDIUM or HIGH risk).

**Step 4 — Delegate execution to the `prisma-migrator` agent:**

```
Agent(
  subagent_type: "prisma-migrator",
  prompt: "Run: npx prisma migrate dev --name <migration_name>. Schema is at prisma/schema.prisma."
)
```

---

### 8. Type Models mode

Generate TypeScript types or Zod schemas from Prisma models on request.

Read `/references/type-mappings.md` for full type mapping table.

**Zod example from Prisma model:**
```ts
import { z } from 'zod'

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(['ADMIN', 'USER', 'MODERATOR']),
  createdAt: z.date(),
  updatedAt: z.date(),
})

export type User = z.infer<typeof UserSchema>
```

---

## Output rules

- Always output valid Prisma SDL — no pseudocode
- Include the full `schema.prisma` header when building from scratch
- Add `// reason: ...` comments for non-obvious decisions
- When building from scratch: show full schema first, then briefly explain key decisions
- For audits: one issue per block, direct and concise
- Never omit `@@index` on relation fields — it's a hard rule

---

## Reference files

- `references/type-mappings.md` — PostgreSQL / TypeScript / Zod ↔ Prisma type mappings
- `references/relations.md` — Full patterns for 1-1, 1-N, N-M, self-relations
- `references/common-patterns.md` — Soft delete, multi-tenancy, audit log, pagination
