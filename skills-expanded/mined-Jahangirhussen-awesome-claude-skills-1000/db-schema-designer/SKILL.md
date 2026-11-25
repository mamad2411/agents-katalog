---
name: db-schema-designer
description: >
  Trigger when the user wants to design, generate, or evolve a database schema from a plain English description, requirements list, or data model sketch. Also trigger for migration file generation, model definitions, or schema reviews.
source:
  repository: armaneker/claude-code-skills
  original_path: saas-builder-kit/skills/db-schema-designer
  original_name: db-schema-designer
status: canonical
---
# DB Schema Designer

You are an expert database architect. When this skill is triggered, design production-quality database schemas with migrations and model definitions.

## Workflow

1. **Clarify requirements** (if not already clear):
   - Target database: Postgres (default), MySQL, or SQLite
   - ORM/migration tool: Prisma, Drizzle, Knex, raw SQL, TypeORM, or SQLAlchemy
   - Existing schema to evolve (ask user to paste it or point to a file)
   - Scale expectations: rows per table, read/write ratio, multi-tenant?

2. **Design the schema** following these principles:
   - Use surrogate primary keys (`id UUID DEFAULT gen_random_uuid()` for Postgres, `id VARCHAR(36)` for MySQL)
   - Always include `created_at TIMESTAMPTZ DEFAULT NOW()` and `updated_at TIMESTAMPTZ DEFAULT NOW()` on every table
   - Normalize to 3NF unless denormalization is explicitly justified by performance requirements
   - Name tables as plural nouns (`users`, `orders`, `line_items`), columns as snake_case
   - Use foreign key constraints with explicit `ON DELETE` behavior — never silently cascade unless intent is clear
   - Add indexes on every foreign key column and every column used in `WHERE`, `ORDER BY`, or `JOIN` clauses
   - Use `NOT NULL` by default; allow NULL only when absence has semantic meaning

3. **Output format** — produce all three artifacts:

### Artifact 1: Entity-Relationship Summary
Plain English table listing:
```
users: id, email (unique), name, role (enum), created_at, updated_at
orders: id, user_id (FK → users), status (enum), total_cents, created_at, updated_at
line_items: id, order_id (FK → orders), product_id (FK → products), quantity, unit_price_cents
```

### Artifact 2: Migration File
Match the user's chosen tool. If none specified, default to Prisma schema + raw SQL migration.

**Prisma example:**
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  orders    Order[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users")
}

enum Role {
  USER
  ADMIN
}
```

**Raw SQL (Postgres) example:**
```sql
CREATE TABLE users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email       TEXT NOT NULL UNIQUE,
  name        TEXT,
  role        TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

### Artifact 3: TypeScript/Python Model Types
Generate typed model interfaces or classes matching the schema.

```typescript
export interface User {
  id: string;
  email: string;
  name: string | null;
  role: 'user' | 'admin';
  createdAt: Date;
  updatedAt: Date;
}

export type CreateUserInput = Pick<User, 'email' | 'name'> & { role?: User['role'] };
export type UpdateUserInput = Partial<Pick<User, 'name' | 'role'>>;
```

## Common Pitfalls — Avoid These

- **Storing money as FLOAT/DOUBLE** — always use `INTEGER` (cents) or `NUMERIC(19,4)`
- **Missing updated_at triggers** — Postgres doesn't auto-update this; add the trigger
- **UUID primary keys without indexes** — UUID PKs are clustered in InnoDB by default (bad); use `CUID` or sequential UUIDs (UUIDv7) for Postgres
- **Soft deletes without partial indexes** — if using `deleted_at`, add `WHERE deleted_at IS NULL` partial indexes on frequently queried columns
- **Polymorphic associations** — avoid `entity_type / entity_id` patterns; use separate junction tables
- **Storing arrays in comma-separated strings** — use proper array columns or junction tables
- **Missing `ON DELETE` specification** — always be explicit: `RESTRICT`, `CASCADE`, or `SET NULL`

## Multi-Tenant Schemas

If the app is multi-tenant, add `organization_id` (FK) to every tenant-scoped table and include it in composite indexes:

```sql
CREATE INDEX idx_orders_org_user ON orders(organization_id, user_id);
```

Enable Row-Level Security in Postgres for strict tenant isolation:
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
  USING (organization_id = current_setting('app.current_org_id')::UUID);
```

## Seeding

Always generate a seed file alongside migrations:
```typescript
// prisma/seed.ts
await prisma.user.upsert({
  where: { email: 'admin@example.com' },
  update: {},
  create: { email: 'admin@example.com', name: 'Admin', role: 'ADMIN' },
});
```
