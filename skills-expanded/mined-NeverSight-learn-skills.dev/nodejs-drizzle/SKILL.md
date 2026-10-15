---
name: nodejs-drizzle
description: "Drizzle ORM en Node.js (v1.0 RC, 2026). Cubre schema declaration, queries SQL-like y relacionales, relaciones (one-to-one, one-to-many, many-to-many), transacciones y savepoints, migrations con drizzle-kit, Zod validation (createInsertSchema/createSelectSchema), prepared statements, connection pooling, SQL Server + PostgreSQL, y estrategia híbrida con Prisma. Actívala cuando el proyecto use Drizzle como ORM, al diseñar schemas type-safe, optimizar queries serverless, o decidir entre Drizzle y Prisma."
---

# Drizzle ORM — TypeScript ORM SQL-first

Guía de Drizzle ORM v1.0-rc (2026). Thin typed layer sobre SQL. Sin deps, serverless-ready, bundle mínimo (~7.4KB). Soporte nativo PostgreSQL, SQL Server (MSSQL), MySQL, SQLite, Turso/LibSQL, CockroachDB.

---

## Setup

```bash
# PostgreSQL
npm i drizzle-orm@rc pg
npm i -D drizzle-kit@rc @types/pg

# SQL Server
npm i drizzle-orm@rc mssql
npm i -D drizzle-kit@rc @types/mssql
```

```typescript
// db/connection.ts — PostgreSQL con node-postgres
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema.js';
import * as relations from './relations.js';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

export const db = drizzle(pool, { schema: { ...schema, ...relations } });

// Singleton en dev (evita múltiples pools con hot reload)
// ponytail: globalThis guard, basta para evitar el multi-pool en dev
const globalForDrizzle = globalThis as unknown as { db: typeof db };
export const db = globalForDrizzle.db ?? drizzle(pool, { schema: { ...schema, ...relations } });
if (process.env.NODE_ENV !== 'production') globalForDrizzle.db = db;
```

```typescript
// drizzle.config.ts
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './src/db/migrations',
  dialect: 'postgresql', // o 'mssql'
  dbCredentials: { url: process.env.DATABASE_URL! },
});
```

---

## Schema declaration

```typescript
// db/schema.ts — PostgreSQL
import {
  pgTable, uuid, text, varchar, integer, numeric, real, boolean,
  date, timestamp, jsonb, serial, bigserial, pgEnum,
  primaryKey, foreignKey, index, uniqueIndex, check,
  type AnyPgColumn,
} from 'drizzle-orm/pg-core';
import { sql } from 'drizzle-orm';

// Enum nativo PostgreSQL
export const orderStatusEnum = pgEnum('order_status', [
  'pending', 'confirmed', 'shipped', 'delivered', 'cancelled',
]);

// Tabla orders
export const orders = pgTable('orders', {
  id: uuid('id').defaultRandom().primaryKey(),
  orderNumber: bigserial('order_number', { mode: 'number' }),
  customerId: uuid('customer_id').notNull(),
  status: orderStatusEnum('status').notNull().default('pending'),
  totalAmount: numeric('total_amount', { precision: 18, scale: 4 }).notNull(),
  currency: text('currency').notNull().default('MXN'),
  notes: text('notes'),
  metadata: jsonb('metadata').$type<{ source: string; tags: string[] }>(),
  isUrgent: boolean('is_urgent').default(false),
  createdAt: timestamp('created_at', { withTimezone: true, precision: 3 }).defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true, precision: 3 })
    .$onUpdate(() => new Date()),
}, (table) => ({
  // Índices
  customerStatusIdx: index('idx_orders_customer_status')
    .on(table.customerId, table.status),
  createdAtIdx: index('idx_orders_created_at').on(table.createdAt),
  // Constraints compuestos
  positiveAmountCheck: check('chk_orders_positive', sql`${table.totalAmount} > 0`),
}));

// Tabla order_items
export const orderItems = pgTable('order_items', {
  id: uuid('id').defaultRandom().primaryKey(),
  orderId: uuid('order_id')
    .notNull()
    .references(() => orders.id, { onDelete: 'cascade' }),
  sku: varchar('sku', { length: 50 }).notNull(),
  quantity: integer('quantity').notNull(),
  unitPrice: numeric('unit_price', { precision: 18, scale: 4 }).notNull(),
  lineNumber: integer('line_number').notNull(),
}, (table) => ({
  orderSkuUnique: uniqueIndex('uq_order_items_sku').on(table.orderId, table.sku),
}));

// Tabla customers
export const customers = pgTable('customers', {
  id: uuid('id').defaultRandom().primaryKey(),
  name: varchar('name', { length: 200 }).notNull(),
  email: varchar('email', { length: 320 }).notNull().unique(),
  createdAt: timestamp('created_at', { withTimezone: true, precision: 3 }).defaultNow(),
});
```

### SQL Server (MSSQL) — equivalente

```typescript
// db/schema.ts — SQL Server
import {
  mssqlTable, uniqueIdentifier, nvarchar, int, decimal, bit,
  datetime2, primaryKey, foreignKey, index,
} from 'drizzle-orm/mssql-core';
import { sql } from 'drizzle-orm';

export const orders = mssqlTable('orders', {
  id: uniqueIdentifier('id').default(sql`NEWID()`).primaryKey(),
  customerId: uniqueIdentifier('customer_id').notNull(),
  status: nvarchar('status', { length: 20 }).notNull().default('pending'),
  totalAmount: decimal('total_amount', { precision: 18, scale: 4 }).notNull(),
  currency: nvarchar('currency', { length: 3 }).notNull().default('MXN'),
  createdAt: datetime2('created_at', { precision: 3 }).default(sql`SYSDATETIME()`),
  updatedAt: datetime2('updated_at', { precision: 3 }),
}, (table) => ({
  customerStatusIdx: index('idx_orders_customer_status')
    .on(table.customerId, table.status),
}));
```

---

## Definición de relaciones (Relational Queries)

```typescript
// db/relations.ts
import { defineRelations } from 'drizzle-orm';
import * as schema from './schema.js';

export const relations = defineRelations(schema, (r) => ({
  customers: {
    orders: r.many.orders(), // customer → many orders
  },
  orders: {
    items: r.many.orderItems(), // order → many items
    customer: r.one.customers({  // order → one customer
      from: r.orders.customerId,
      to: r.customers.id,
    }),
  },
  orderItems: {
    order: r.one.orders({       // item → one order
      from: r.orderItems.orderId,
      to: r.orders.id,
    }),
  },
}));
```

### Relaciones many-to-many (tabla puente)

```typescript
// Tabla puente
export const usersToGroups = pgTable('users_to_groups', {
  userId: uuid('user_id').notNull().references(() => users.id),
  groupId: uuid('group_id').notNull().references(() => groups.id),
}, (t) => [primaryKey({ columns: [t.userId, t.groupId] })]);

// Relaciones definidas con .through()
export const relations = defineRelations(schema, (r) => ({
  users: {
    groups: r.many.groups({         // user → many groups
      from: r.users.id.through(r.usersToGroups.userId),
      to: r.groups.id.through(r.usersToGroups.groupId),
    }),
  },
  groups: {
    users: r.many.users({           // group → many users
      from: r.groups.id.through(r.usersToGroups.groupId),
      to: r.users.id.through(r.usersToGroups.userId),
    }),
  },
}));
```

---

## Queries SQL-like (Core API)

### SELECT básico

```typescript
import { eq, ne, gt, gte, lt, lte, and, or, not, like, ilike,
  isNull, isNotNull, inArray, notInArray, between, asc, desc,
  count, countDistinct, sum, avg, max, min, sql } from 'drizzle-orm';

// ✅ Select todas las columnas
const allOrders = await db.select().from(orders);

// ✅ Select parcial
const summaries = await db.select({
  id: orders.id,
  status: orders.status,
  total: orders.totalAmount,
}).from(orders);

// ✅ Select con expresiones SQL
const result = await db.select({
  id: orders.id,
  yearMonth: sql<string>`to_char(${orders.createdAt}, 'YYYY-MM')`,
}).from(orders);

// ✅ Distinct
const uniqueStatuses = await db
  .selectDistinct({ status: orders.status })
  .from(orders);

// ✅ $count — helper para count(*)
const total = await db.$count(orders);
const pendingCount = await db.$count(orders, eq(orders.status, 'pending'));
```

### WHERE — filtros

```typescript
// Filtro simple
await db.select().from(orders).where(eq(orders.id, orderId));

// AND / OR combinados
await db.select().from(orders).where(and(
  eq(orders.customerId, customerId),
  or(eq(orders.status, 'pending'), eq(orders.status, 'confirmed')),
  gte(orders.totalAmount, '100.0000'),
));

// IN / NOT IN
await db.select().from(orders).where(
  inArray(orders.status, ['pending', 'confirmed']),
);

// LIKE / ILIKE
await db.select().from(customers).where(
  ilike(customers.name, '%acme%'),
);

// Condicional — undefined omite el filtro
const searchOrders = async (status?: string) => {
  return db.select().from(orders).where(
    status ? eq(orders.status, status) : undefined,
  );
};

// Filtro con raw SQL
await db.select().from(orders).where(
  sql`${orders.createdAt} < now() - interval '24 hours'`,
);
```

### JOINs

```typescript
// INNER JOIN
const result = await db.select()
  .from(orders)
  .innerJoin(customers, eq(orders.customerId, customers.id));

// LEFT JOIN con campos seleccionados
const ordersWithCustomer = await db.select({
  orderId: orders.id,
  orderStatus: orders.status,
  customerName: customers.name,
  customerEmail: customers.email,
})
  .from(orders)
  .leftJoin(customers, eq(orders.customerId, customers.id));

// Multiple joins
await db.select()
  .from(orders)
  .innerJoin(customers, eq(orders.customerId, customers.id))
  .leftJoin(orderItems, eq(orders.id, orderItems.orderId));
```

### ORDER BY, LIMIT, OFFSET

```typescript
// Paginación clásica
await db.select().from(orders)
  .orderBy(desc(orders.createdAt))
  .limit(20)
  .offset(0);

// Multiple order by
await db.select().from(orders)
  .orderBy(asc(orders.status), desc(orders.totalAmount));
```

### Agregaciones y GROUP BY

```typescript
// Agregación con group by
const stats = await db.select({
  status: orders.status,
  count: count(orders.id),
  total: sum(orders.totalAmount),
  avg: avg(orders.totalAmount),
})
  .from(orders)
  .groupBy(orders.status);

// HAVING — filtro post-agregación
await db.select({
  customerId: orders.customerId,
  total: sum(orders.totalAmount),
})
  .from(orders)
  .groupBy(orders.customerId)
  .having(({ total }) => gt(total, '10000.0000'));

// Subquery con $count
const customersWithCount = await db.select({
  id: customers.id,
  name: customers.name,
  orderCount: db.$count(orders, eq(orders.customerId, customers.id)),
}).from(customers);
```

### WITH (CTEs)

```typescript
// CTE con subquery
const recentOrders = db.$with('recent_orders').as(
  db.select().from(orders)
    .where(gte(orders.createdAt, new Date('2026-01-01')))
);

const result = await db.with(recentOrders)
  .select()
  .from(recentOrders)
  .where(eq(recentOrders.status, 'pending'));
```

### INSERT, UPDATE, DELETE

```typescript
// INSERT — retornando la fila creada
const [newOrder] = await db.insert(orders).values({
  customerId: 'CUST-001',
  totalAmount: '150.0000',
  status: 'pending',
}).returning();

// INSERT múltiple
await db.insert(orderItems).values([
  { orderId: newOrder.id, sku: 'SKU-A', quantity: 2, unitPrice: '50.0000', lineNumber: 1 },
  { orderId: newOrder.id, sku: 'SKU-B', quantity: 1, unitPrice: '50.0000', lineNumber: 2 },
]);

// INSERT ... ON CONFLICT (upsert) — PostgreSQL
await db.insert(orders).values({ ... })
  .onConflictDoUpdate({ target: orders.id, set: { status: 'confirmed' } });

// UPDATE
await db.update(orders)
  .set({ status: 'confirmed', updatedAt: new Date() })
  .where(eq(orders.id, orderId));

// UPDATE con expresión SQL
await db.update(orders)
  .set({ totalAmount: sql`${orders.totalAmount} * 1.16` })
  .where(eq(orders.status, 'pending'));

// DELETE
await db.delete(orders).where(eq(orders.id, orderId));
```

---

## Queries relacionales (Relational Queries API)

```typescript
// findMany — todos los customers con sus orders
const customersWithOrders = await db.query.customers.findMany({
  with: { orders: true },
});

// findFirst — un order con items
const order = await db.query.orders.findFirst({
  where: (t, { eq }) => eq(t.id, orderId),
  with: {
    items: true,
    customer: true,
  },
});

// Nested relations (3 niveles)
const fullOrder = await db.query.customers.findMany({
  with: {
    orders: {
      with: {
        items: true,
      },
    },
  },
});

// Partial select en relaciones
const partial = await db.query.orders.findMany({
  columns: { id: true, status: true, totalAmount: true },
  with: {
    items: {
      columns: { sku: true, quantity: true, unitPrice: true },
    },
    customer: {
      columns: { name: true, email: true },
    },
  },
});

// Filtros anidados — orders con items cuyo quantity > 5
const bigOrders = await db.query.orders.findMany({
  with: {
    items: {
      where: (t, { gt }) => gt(t.quantity, 5),
    },
  },
  where: (t, { eq }) => eq(t.status, 'pending'),
});

// Orden en relaciones
await db.query.customers.findMany({
  orderBy: (t, { asc }) => asc(t.name),
  with: {
    orders: {
      orderBy: (t, { desc }) => desc(t.createdAt),
      limit: 5,  // Solo últimos 5 orders por customer
    },
  },
});

// Filtro por existencia de relación (solo customers que tienen orders)
await db.query.customers.findMany({
  with: { orders: true },
  where: (t) => ({ orders: true }),
});

// extras — campos calculados
const withCounts = await db.query.customers.findMany({
  extras: {
    totalSpent: (t) =>
      sql<number>`coalesce(sum(${orders.totalAmount}), 0)`.mapWith(Number),
  },
});
```

---

## Transacciones

```typescript
// ✅ Transacción plana
const newBalance = await db.transaction(async (tx) => {
  await tx.update(orders)
    .set({ status: 'confirmed' })
    .where(eq(orders.id, orderId));

  const [updated] = await tx.select({ total: orders.totalAmount })
    .from(orders).where(eq(orders.id, orderId));
  return updated.total;
});

// ✅ Rollback explícito
await db.transaction(async (tx) => {
  const [order] = await tx.select({ status: orders.status })
    .from(orders).where(eq(orders.id, orderId));

  if (order.status !== 'pending') {
    tx.rollback(); // Lanza excepción que revierte la transacción
  }
  await tx.update(orders).set({ status: 'cancelled' }).where(eq(orders.id, orderId));
});

// ✅ Savepoints (transacciones anidadas)
await db.transaction(async (tx) => {
  await tx.insert(orders).values({ ... });

  await tx.transaction(async (tx2) => {
    // Savepoint: si falla, solo revierte este bloque
    await tx2.insert(orderItems).values(items);
  });
});

// ✅ Transacción + relational queries
await db.transaction(async (tx) => {
  const user = await tx.query.users.findFirst({
    where: (t, { eq }) => eq(t.id, userId),
    with: { posts: true },
  });
  // ...
});

// ✅ Configuración de transacción PostgreSQL
await db.transaction(async (tx) => {
  // ...
}, {
  isolationLevel: 'read committed',
  accessMode: 'read write',
  deferrable: true,
});
```

---

## Prepared statements (máximo rendimiento)

```typescript
// Prepared statement sin placeholders
const allPending = db.select().from(orders)
  .where(eq(orders.status, 'pending'))
  .prepare('get_pending_orders');

const result1 = await allPending.execute();
const result2 = await allPending.execute(); // Reutiliza el plan

// Prepared statement con placeholders
const orderById = db.select().from(orders)
  .where(eq(orders.id, sql.placeholder('id')))
  .prepare('get_order_by_id');

const order1 = await orderById.execute({ id: 'uuid-1' });
const order2 = await orderById.execute({ id: 'uuid-2' });

// Relational query preparada
const customersWithOrders = db.query.customers.findMany({
  where: (t, { eq }) => eq(t.id, sql.placeholder('customerId')),
  with: { orders: { limit: sql.placeholder('orderLimit') } },
}).prepare('customers_with_orders');

const result = await customersWithOrders.execute({
  customerId: 'uuid-1',
  orderLimit: 5,
});
```

---

## Zod validation (built-in — `drizzle-orm/zod`)

> ⚠️ `drizzle-zod` standalone está deprecado. Usar `drizzle-orm/zod`. Disponible desde `drizzle-orm@1.0.0-beta.15`.

```typescript
import { createInsertSchema, createSelectSchema, createUpdateSchema } from 'drizzle-orm/zod';
import { z } from 'zod';

// Schema de inserción — infiere tipos del schema de DB
export const insertOrderSchema = createInsertSchema(orders, {
  totalAmount: z.string().regex(/^\d+\.\d{4}$/, 'Must be DECIMAL(18,4)'),
  currency: z.string().length(3).default('MXN'),
}).pick({ customerId: true, totalAmount: true, notes: true });
// Tipado: { customerId: string; totalAmount: string; notes?: string | null }

// Schema de select (para params de búsqueda)
export const selectOrderSchema = createSelectSchema(orders);

// Schema de update (todos los campos opcionales)
export const updateOrderSchema = createUpdateSchema(orders);

// Uso en endpoint Express/Fastify
app.post('/api/orders', async (req, res) => {
  const parsed = insertOrderSchema.parse(req.body); // Valida entrada
  const [order] = await db.insert(orders).values(parsed).returning();
  res.status(201).json(order);
});
```

---

## Migraciones con drizzle-kit

```bash
# Generar migración SQL desde diff del schema TypeScript
npx drizzle-kit generate

# Aplicar migraciones pendientes
npx drizzle-kit migrate

# Push directo (solo dev, sin archivos de migración)
npx drizzle-kit push

# Verificar estado de migraciones (drift)
npx drizzle-kit check

# Eliminar todas las tablas (⚠️ solo dev)
npx drizzle-kit drop
```

### Migrator programático (para CI/CD)

```typescript
// db/migrate.ts
import { migrate } from 'drizzle-orm/node-postgres/migrator';
import { db } from './connection.js';

await migrate(db, { migrationsFolder: './src/db/migrations' });
console.log('Migrations applied');
process.exit(0);
```

### Estructura de archivos generada

```
src/db/migrations/
├── 0000_black_panther.sql       # CREATE TABLE orders...
├── 0001_swift_cable.sql          # ALTER TABLE orders ADD COLUMN...
└── meta/
    ├── _journal.json            # Historial de migraciones aplicadas
    └── 0000_snapshot.json       # Snapshot del schema en cada paso
```

---

## Connection pooling

```typescript
// pg (node-postgres) — recomendado para PostgreSQL
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,                       // Conexiones máximas
  idleTimeoutMillis: 30000,      // Cerrar inactivas tras 30s
  connectionTimeoutMillis: 5000, // Timeout de conexión
});

export const db = drizzle(pool);

// postgres.js — recomendado para serverless
import postgres from 'postgres';

const sql = postgres(process.env.DATABASE_URL, {
  max: 10,
  idle_timeout: 20,
  connect_timeout: 10,
  prepare: false, // Desactivar prepared statements en serverless
});

export const db = drizzle(sql);
```

⚠️ Con PgBouncer en transaction mode: `max: 5`, desactivar prepared statements (`prepare: false`).

---

## SQL Server (MSSQL) con Drizzle

```typescript
// connection.ts
import { drizzle } from 'drizzle-orm/mssql';
import mssql from 'mssql';

const pool = await mssql.connect({
  server: process.env.DB_HOST!,
  database: process.env.DB_NAME!,
  user: process.env.DB_USER!,
  password: process.env.DB_PASSWORD!,
  options: {
    encrypt: true,
    trustServerCertificate: process.env.NODE_ENV !== 'production',
  },
  pool: { max: 10, min: 2, idleTimeoutMillis: 30000 },
});

export const db = drizzle(pool);
```

```typescript
// drizzle.config.ts — SQL Server
export default defineConfig({
  schema: './src/db/schema.ts',
  out: './src/db/migrations',
  dialect: 'mssql',
  dbCredentials: {
    server: process.env.DB_HOST!,
    database: process.env.DB_NAME!,
    user: process.env.DB_USER!,
    password: process.env.DB_PASSWORD!,
    options: { encrypt: true },
  },
});
```

### Tipos SQL Server más comunes

| Drizzle MSSQL | SQL Server | Notas |
|---------------|-----------|-------|
| `uniqueIdentifier()` | `UNIQUEIDENTIFIER` | GUID |
| `nvarchar({ length: N })` | `NVARCHAR(N)` | Unicode string |
| `int()` | `INT` | 4-byte integer |
| `decimal({ precision: P, scale: S })` | `DECIMAL(P, S)` | Exacto |
| `bit()` | `BIT` | Boolean |
| `datetime2({ precision: 3 })` | `DATETIME2(3)` | Fecha+hora |
| `varbinary()` | `VARBINARY(MAX)` | Binario |

---

## Type helpers

```typescript
import { type InferSelectModel, type InferInsertModel } from 'drizzle-orm';

// Inferir tipos desde el schema
type Order = typeof orders.$inferSelect;         // o InferSelectModel<typeof orders>
type NewOrder = typeof orders.$inferInsert;      // o InferInsertModel<typeof orders>

// Select parcial: usar el tipo inferido + Pick/Omit
type OrderSummary = Pick<Order, 'id' | 'status' | 'totalAmount' | 'createdAt'>;

// Columnas tipadas: getColumns() para excluir campos
import { getColumns } from 'drizzle-orm';
const { metadata, notes, ...publicColumns } = getColumns(orders);
await db.select(publicColumns).from(orders); // Excluye metadata y notes
```

---

## Logging

```typescript
// Logger por defecto
const db = drizzle(pool, { logger: true });

// Logger custom (e.g., con pino)
import type { Logger } from 'drizzle-orm/logger';

class PinoDrizzleLogger implements Logger {
  logQuery(query: string, params: unknown[]): void {
    logger.debug({ query, params }, 'drizzle query');
  }
}

const db = drizzle(pool, { logger: new PinoDrizzleLogger() });
```

---

## Raw SQL y escape hatches

```typescript
// Ejecutar SQL crudo parametrizado
const result = await db.execute(
  sql`SELECT * FROM orders WHERE created_at < ${cutoffDate}`,
);

// sql`` para cualquier expresión SQL
await db.select({
  id: orders.id,
  fullAddress: sql<string>`concat(${customers.city}, ', ', ${customers.country})`,
}).from(orders).innerJoin(customers, eq(orders.customerId, customers.id));

// .mapWith() para castear tipos en runtime
await db.select({
  count: sql`count(*)`.mapWith(Number),
}).from(orders);

// Printing SQL (debugging sin ejecutar)
const { sql: queryText, params } = db.select().from(orders)
  .where(eq(orders.status, 'pending'))
  .limit(10)
  .toSQL();
console.log({ queryText, params });
```

---

## Estrategia híbrida: Prisma + Drizzle

```typescript
// Prisma para writes (migraciones, relaciones complejas, Studio)
// Drizzle para reads de alto rendimiento (hot paths, reportes, serverless)

// Read side con Drizzle
class OrderReadRepository {
  async getCustomerOrders(customerId: string) {
    return db.query.orders.findMany({
      where: (t, { eq }) => eq(t.customerId, customerId),
      columns: { id: true, status: true, totalAmount: true, createdAt: true },
      orderBy: (t, { desc }) => desc(t.createdAt),
    });
  }

  async getDashboardStats() {
    return db.select({
      status: orders.status,
      count: count(orders.id),
      revenue: sum(orders.totalAmount),
    }).from(orders).groupBy(orders.status);
  }
}
```

---

## ¿Drizzle o Prisma?

| Criterio | Drizzle | Prisma 7 |
|----------|---------|----------|
| **Bundle size** | ~7.4KB runtime | ~2MB runtime |
| **Serverless cold start** | ⭐ Instantáneo | Bueno (sin Rust engine desde v7) |
| **API style** | SQL-like (sin learning curve si sabés SQL) | Schema-first + API declarativa |
| **Relaciones anidadas** | `.query` API + `with` | `include` anidado |
| **Migraciones** | `drizzle-kit generate/migrate` | `prisma migrate dev/deploy` |
| **Raw SQL** | ⭐ Nativo con `sql` template | `$queryRaw` |
| **Tooling visual** | `drizzle-studio` (beta) | Prisma Studio (maduro) |
| **Type safety** | ⭐ Inferido del schema (const generics) | ⭐ Generado por CLI |
| **Ecosistema** | Creciente | Consolidado |

**Regla 2026**: Serverless / Edge / bundle-sensitive → **Drizzle**. Equipo que prefiere schema-first + tooling visual → **Prisma 7**.

---

## Checklist Drizzle

- [ ] Connection pool con `max` explícito (20 para PostgreSQL, 10 para serverless)
- [ ] Schema definido en TypeScript con column types correctos (precision/scale en decimals, timezone en timestamps)
- [ ] Relaciones definidas con `defineRelations()` para la API relacional
- [ ] Zod schemas con `createInsertSchema`/`createUpdateSchema` en boundaries HTTP
- [ ] Migraciones generadas con `drizzle-kit generate`, aplicadas en CI
- [ ] Prepared statements para queries de alto tráfico (>100 req/s)
- [ ] `CancellationToken` / `AbortSignal` propagado a queries async
- [ ] Sin N+1: usar `with` en relational queries o `inArray` en batch
- [ ] Logging de queries solo en dev (`logger: true` condicional)
- [ ] `returning()` en INSERT cuando se necesita el ID generado
- [ ] PgBouncer: `prepare: false` y `max` reducido
- [ ] Singleton `db` instance (globalThis guard en dev)
