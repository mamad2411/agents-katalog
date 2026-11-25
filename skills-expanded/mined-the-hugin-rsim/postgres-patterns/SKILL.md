---
name: postgres-patterns
description: PostgreSQL best practices for query optimization, schema design, indexing, RLS, and connection management. Includes Drizzle ORM patterns for TypeScript — schema definition, type inference, query builder style. Based on Supabase and lobehub guidelines.
origin: ECC
group: domain
triggers:
  - "postgresql"
  - "postgres индекс"
  - "RLS"
  - "postgres оптимизация"
  - "sql схема"
  - "drizzle"
  - "drizzle orm"
  - "pgTable"
output: "optimized PostgreSQL queries, schema design, index strategy, RLS policies, Drizzle ORM schema and query patterns"
calls: []
---

# PostgreSQL Patterns

Quick reference for PostgreSQL best practices.

## When to Activate

- Writing SQL queries or migrations
- Designing database schemas
- Troubleshooting slow queries
- Implementing Row Level Security
- Setting up connection pooling
- Defining Drizzle ORM schemas and relations (TypeScript)

## Index Cheat Sheet

| Query Pattern | Index Type | Example |
|---|---|---|
| `WHERE col = value` | B-tree (default) | `CREATE INDEX idx ON t (col)` |
| `WHERE col > value` | B-tree | `CREATE INDEX idx ON t (col)` |
| `WHERE a = x AND b > y` | Composite | `CREATE INDEX idx ON t (a, b)` |
| `WHERE jsonb @> '{}'` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| `WHERE tsv @@ query` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| Time-series ranges | BRIN | `CREATE INDEX idx ON t USING brin (col)` |

## Data Type Quick Reference

| Use Case | Correct Type | Avoid |
|---|---|---|
| IDs | `bigint` | `int`, random UUID |
| Strings | `text` | `varchar(255)` |
| Timestamps | `timestamptz` | `timestamp` |
| Money | `numeric(10,2)` | `float` |
| Flags | `boolean` | `varchar`, `int` |

## Common Patterns

### Composite Index Order

```sql
-- Equality columns first, then range columns
CREATE INDEX idx ON orders (status, created_at);
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
```

### Covering Index (avoids table lookup)

```sql
CREATE INDEX idx ON users (email) INCLUDE (name, created_at);
-- SELECT email, name, created_at — no heap fetch needed
```

### Partial Index (smaller, faster)

```sql
CREATE INDEX idx ON users (email) WHERE deleted_at IS NULL;
```

### RLS Policy (optimized)

```sql
CREATE POLICY policy ON orders
  USING ((SELECT auth.uid()) = user_id);  -- Wrap in SELECT!
```

### UPSERT

```sql
INSERT INTO settings (user_id, key, value)
VALUES (123, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;
```

### Cursor Pagination (O(1) vs OFFSET O(n))

```sql
SELECT * FROM products WHERE id > $last_id ORDER BY id LIMIT 20;
```

### Queue Processing (skip locked)

```sql
UPDATE jobs SET status = 'processing'
WHERE id = (
  SELECT id FROM jobs WHERE status = 'pending'
  ORDER BY created_at LIMIT 1
  FOR UPDATE SKIP LOCKED
) RETURNING *;
```

## Diagnostics

```sql
-- Find unindexed foreign keys
SELECT conrelid::regclass, a.attname
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey)
  );

-- Find slow queries (requires pg_stat_statements)
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC;

-- Check table bloat
SELECT relname, n_dead_tup, last_vacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## Configuration Template

```sql
-- Connection limits (tune for RAM)
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET work_mem = '8MB';

-- Timeouts
ALTER SYSTEM SET idle_in_transaction_session_timeout = '30s';
ALTER SYSTEM SET statement_timeout = '30s';

-- Monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Security defaults
REVOKE ALL ON SCHEMA public FROM public;

SELECT pg_reload_conf();
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `OFFSET N` pagination | O(n) table scan | Cursor pagination with `id > $last` |
| `varchar(255)` | Arbitrary limit, no benefit | Use `text` |
| `float` for money | Rounding errors | `numeric(10,2)` |
| `timestamp` | No timezone info | `timestamptz` |
| Missing FK indexes | Slow JOINs | Index all foreign keys |
| `SELECT *` in RLS | Forces expression eval per row | Wrap auth calls in `SELECT` subquery |

---

*Based on Supabase Agent Skills — MIT License*

---

## Drizzle ORM (TypeScript)

> Применяй когда схема и запросы пишутся на TypeScript через Drizzle ORM.

### Config

```typescript
// drizzle.config.ts
export default defineConfig({
  dialect: 'postgresql',
  schema: './src/database/schemas/*',
  out: './src/database/migrations',
  strict: true,
});
```

### Naming Conventions

| Объект | Формат | Пример |
|---|---|---|
| Таблицы | plural snake_case | `users`, `session_groups` |
| Колонки | snake_case | `user_id`, `created_at` |

### Column Patterns

**Primary Key** — prefixed text ID (читаемый, distinguishable по типу):

```typescript
id: text('id')
  .primaryKey()
  .$defaultFn(() => idGenerator('agents'))
  .notNull(),
// Для внутренних таблиц: uuid вместо text
```

**Foreign Key** с cascade:

```typescript
userId: text('user_id')
  .references(() => users.id, { onDelete: 'cascade' })
  .notNull(),
```

**Timestamps** — через хелперы, не вручную:

```typescript
// _helpers.ts
export const createdAt = () => timestamptz('created_at').defaultNow().notNull();
export const updatedAt = () => timestamptz('updated_at').$onUpdate(() => new Date());
export const timestamps = { createdAt: createdAt(), updatedAt: updatedAt() };

// В схеме:
...timestamps,
```

**Indexes** — возвращай массив (не объект):

```typescript
(t) => [uniqueIndex('client_id_user_id_unique').on(t.clientId, t.userId)],
```

### Full Table Example

```typescript
export const agents = pgTable(
  'agents',
  {
    id: text('id')
      .primaryKey()
      .$defaultFn(() => idGenerator('agents'))
      .notNull(),
    slug: varchar('slug', { length: 100 })
      .$defaultFn(() => randomSlug(4))
      .unique(),
    userId: text('user_id')
      .references(() => users.id, { onDelete: 'cascade' })
      .notNull(),
    clientId: text('client_id'),
    config: jsonb('config').$type<AgentConfig>(),
    ...timestamps,
  },
  (t) => [uniqueIndex('client_id_user_id_unique').on(t.clientId, t.userId)],
);
```

### Type Inference

```typescript
export const insertAgentSchema = createInsertSchema(agents);
export type NewAgent = typeof agents.$inferInsert;
export type AgentItem  = typeof agents.$inferSelect;
```

### Junction Table (Many-to-Many)

```typescript
export const agentsKnowledgeBases = pgTable(
  'agents_knowledge_bases',
  {
    agentId: text('agent_id')
      .references(() => agents.id, { onDelete: 'cascade' }).notNull(),
    knowledgeBaseId: text('knowledge_base_id')
      .references(() => knowledgeBases.id, { onDelete: 'cascade' }).notNull(),
    userId: text('user_id')
      .references(() => users.id, { onDelete: 'cascade' }).notNull(),
    enabled: boolean('enabled').default(true),
    ...timestamps,
  },
  (t) => [primaryKey({ columns: [t.agentId, t.knowledgeBaseId] })],
);
```

### Query Style — критическое правило

**Всегда `db.select()`. Никогда `db.query.*`.**

`db.query.findMany/findFirst/with:` генерирует сложные lateral joins с `json_build_array` — хрупкие и трудно отлаживаемые.

**Select single row:**

```typescript
// ✅
const [result] = await db.select().from(agents).where(eq(agents.id, id)).limit(1);

// ❌
return db.query.agents.findFirst({ where: eq(agents.id, id) });
```

**Select with JOIN:**

```typescript
// ✅
const rows = await db
  .select({
    runId: evalRunTopics.runId,
    score: evalRunTopics.score,
    testCase: evalTestCases,
  })
  .from(evalRunTopics)
  .leftJoin(evalTestCases, eq(evalRunTopics.testCaseId, evalTestCases.id))
  .where(eq(evalRunTopics.runId, runId))
  .orderBy(asc(evalRunTopics.createdAt));

// ❌
return db.query.evalRunTopics.findMany({
  where: eq(evalRunTopics.runId, runId),
  with: { testCase: true },
});
```

**Aggregation:**

```typescript
// ✅
const rows = await db
  .select({
    id: datasets.id,
    name: datasets.name,
    count: count(testCases.id).as('count'),
  })
  .from(datasets)
  .leftJoin(testCases, eq(datasets.id, testCases.datasetId))
  .groupBy(datasets.id);
```

**One-to-Many — два отдельных запроса:**

```typescript
// ✅ Два простых запроса вместо relational with:
const [parent] = await db.select().from(datasets).where(eq(datasets.id, id)).limit(1);
if (!parent) return undefined;

const children = await db
  .select()
  .from(testCases)
  .where(eq(testCases.datasetId, id))
  .orderBy(asc(testCases.sortOrder));

return { ...parent, testCases: children };
```

**UPSERT:**

```typescript
await db
  .insert(settings)
  .values({ userId, key, value })
  .onConflictDoUpdate({
    target: [settings.userId, settings.key],
    set: { value: sql`excluded.value` },
  });
```

**Cursor pagination в Drizzle:**

```typescript
const rows = await db
  .select()
  .from(products)
  .where(gt(products.id, lastId))
  .orderBy(asc(products.id))
  .limit(20);
```

**Транзакции:**

```typescript
await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values(userData).returning();
  await tx.insert(profiles).values({ userId: user.id, ...profileData });
});
```

### Drizzle Anti-Patterns

| Anti-Pattern | Проблема | Fix |
|---|---|---|
| `db.query.*` с `with:` | Lateral joins, хрупко | `db.select()` + `leftJoin()` |
| One-to-many через `with:` | Сложный JSON в памяти | Два отдельных запроса |
| Indexes как объект | Deprecated синтаксис | Возвращай массив `(t) => [...]` |
| Ручные timestamp поля | Несогласованность | Хелперы `createdAt()`, `updatedAt()` |
| `$inferInsert` не экспортируется | Дублирование типов вручную | Всегда экспортируй `NewX` и `XItem` |
