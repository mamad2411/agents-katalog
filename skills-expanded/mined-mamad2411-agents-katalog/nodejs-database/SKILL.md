---
name: nodejs-database
description: "Acceso a datos en Node.js con Prisma 7, Drizzle y drivers nativos. Cubre PostgreSQL, SQL Server, migraciones, connection pooling, queries type-safe, raw SQL, y buenas prácticas de integración. Actívala al configurar ORM, diseñar esquemas de datos, optimizar queries, o migrar entre ORMs."
disable-model-invocation: true
---

# Node.js Database Access

Guía de acceso a datos en Node.js 2026. **Prisma 7 vs Drizzle** como ORMs. Drivers nativos para casos específicos.

---

## Elección del ORM

| Criterio | Prisma 7 | Drizzle |
|----------|----------|---------|
| **Abstracción** | Alta (schema.prisma) | Baja (SQL-like) |
| **Bundle size** | ~12MB CLI + ~2MB runtime | ~7.4KB runtime |
| **Serverless** | Cold start más lento | ⭐ Optimizado para serverless |
| **Type safety** | Excelente | ⭐ Excelente (inferido del schema) |
| **Migrations** | Built-in, maduro | Built-in (`drizzle-kit`) |
| **Relaciones** | API declarativa alta | API SQL-like con joins |
| **Raw SQL** | `$queryRaw` | Nativo con `sql` template |

**Regla**: Equipo que prefiere schema-first + abstracción → **Prisma 7**. Serverless + control SQL fino → **Drizzle**.

---

## Prisma 7

### Schema

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql" // o "sqlserver"
  url      = env("DATABASE_URL")
}

model Order {
  id          String   @id @default(uuid())
  orderNumber Int      @default(autoincrement())
  customerId  String
  status      String   @default("pending")
  totalAmount Decimal  @db.Decimal(18, 4)
  currency    String   @default("MXN")
  createdAt   DateTime @default(now()) @db.Timestamptz(3)
  updatedAt   DateTime @updatedAt @db.Timestamptz(3)

  items       OrderItem[]

  @@index([customerId, status])
  @@index([createdAt])
  @@map("orders")
}

model OrderItem {
  id         String   @id @default(uuid())
  orderId    String
  sku        String
  quantity   Int
  unitPrice  Decimal  @db.Decimal(18, 4)
  order      Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)

  @@map("order_items")
}
```

### Queries

```typescript
// Crear con items anidados
const order = await prisma.order.create({
  data: {
    customerId: 'CUST-001',
    totalAmount: 150,
    items: {
      create: [
        { sku: 'SKU-1', quantity: 2, unitPrice: 50 },
        { sku: 'SKU-2', quantity: 1, unitPrice: 50 },
      ],
    },
  },
  include: { items: true },
});

// Leer con filtros y paginación
const orders = await prisma.order.findMany({
  where: {
    customerId: 'CUST-001',
    status: { not: 'deleted' },
    createdAt: { gte: new Date('2026-01-01') },
  },
  orderBy: { createdAt: 'desc' },
  take: 20,
  skip: 0,
  select: {
    id: true,
    orderNumber: true,
    status: true,
    totalAmount: true,
    createdAt: true,
  },
});

// Batch update
await prisma.order.updateMany({
  where: {
    status: 'pending',
    createdAt: { lt: new Date(Date.now() - 24 * 60 * 60 * 1000) },
  },
  data: { status: 'expired' },
});

// Transaction (múltiples operaciones atómicas)
await prisma.$transaction(async (tx) => {
  const order = await tx.order.create({ data: { ... } });
  await tx.stock.decrement({ where: { sku }, data: { quantity } });
  return order;
});

// Raw SQL tipado
const result = await prisma.$queryRaw<OrderSummary[]>`
  SELECT id, status, total_amount
  FROM orders
  WHERE customer_id = ${customerId}
`;
```

---

## Drizzle

### Schema

```typescript
// db/schema.ts
import { pgTable, uuid, text, numeric, timestamp, integer, index } from 'drizzle-orm/pg-core';

export const orders = pgTable('orders', {
  id: uuid('id').defaultRandom().primaryKey(),
  orderNumber: integer('order_number').generatedAlwaysAsIdentity(),
  customerId: text('customer_id').notNull(),
  status: text('status').notNull().default('pending'),
  totalAmount: numeric('total_amount', { precision: 18, scale: 4 }).notNull(),
  currency: text('currency').notNull().default('MXN'),
  createdAt: timestamp('created_at', { withTimezone: true, precision: 3 }).defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true, precision: 3 }).$onUpdate(() => new Date()),
}, (table) => ({
  customerStatusIdx: index('idx_orders_customer_status').on(table.customerId, table.status),
}));

export const orderItems = pgTable('order_items', {
  id: uuid('id').defaultRandom().primaryKey(),
  orderId: uuid('order_id').references(() => orders.id, { onDelete: 'cascade' }),
  sku: text('sku').notNull(),
  quantity: integer('quantity').notNull(),
  unitPrice: numeric('unit_price', { precision: 18, scale: 4 }).notNull(),
});
```

### Queries

```typescript
import { eq, and, gte, desc, sql } from 'drizzle-orm';
import { db } from './db.js';

// Crear
const order = await db.insert(orders).values({
  customerId: 'CUST-001',
  totalAmount: '150.0000',
}).returning();

// Leer con filtros
const result = await db.select({
  id: orders.id,
  orderNumber: orders.orderNumber,
  status: orders.status,
  totalAmount: orders.totalAmount,
  createdAt: orders.createdAt,
})
  .from(orders)
  .where(and(
    eq(orders.customerId, 'CUST-001'),
    gte(orders.createdAt, new Date('2026-01-01')),
  ))
  .orderBy(desc(orders.createdAt))
  .limit(20)
  .offset(0);

// Joins con relaciones
const fullOrder = await db.query.orders.findFirst({
  where: eq(orders.id, id),
  with: { items: true },
});

// Batch update
await db.update(orders)
  .set({ status: 'expired' })
  .where(and(
    eq(orders.status, 'pending'),
    sql`${orders.createdAt} < now() - interval '24 hours'`,
  ));

// Transaction
await db.transaction(async (tx) => {
  const [order] = await tx.insert(orders).values({ ... }).returning();
  await tx.update(stock).set({ quantity: sql`${stock.quantity} - 1` });
  return order;
});
```

---

## Connection Pooling

```typescript
// Prisma: pooling configurado en schema
// connection_limit = 20

// Drizzle con pg (recomendado)
import { Pool } from 'pg';
import { drizzle } from 'drizzle-orm/node-postgres';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,                    // Conexiones máximas
  idleTimeoutMillis: 30000,   // Cerrar inactivas después de 30s
  connectionTimeoutMillis: 5000,
});

export const db = drizzle(pool);
```

⚠️ Con PgBouncer en transaction mode: `max: 5` en el pool de la app, `pool_mode = transaction` en PgBouncer.

---

## SQL Server con Node.js

```typescript
// Driver: tedious o mssql (wrapper sobre tedious)
import sql from 'mssql';

const pool = await sql.connect({
  server: 'localhost',
  database: 'miapp',
  user: 'app_user',
  password: process.env.DB_PASSWORD,
  options: {
    encrypt: true,
    trustServerCertificate: process.env.NODE_ENV !== 'production',
  },
  pool: { max: 10, min: 2, idleTimeoutMillis: 30000 },
});

// Query parametrizado
const result = await pool.request()
  .input('customerId', sql.NVarChar, customerId)
  .input('status', sql.NVarChar, status)
  .query('SELECT * FROM orders WHERE customer_id = @customerId AND status = @status');

// Prisma con SQL Server: provider = "sqlserver"
// Drizzle con SQL Server: drizzle-orm/mssql
```

---

## Migraciones

```bash
# Prisma: auto-detecta cambios del schema
npx prisma migrate dev --name add-cancelled-at
npx prisma migrate deploy    # Producción
npx prisma migrate status    # Estado

# Drizzle: genera SQL desde diff del schema
npx drizzle-kit generate
npx drizzle-kit migrate       # Aplica migraciones
npx drizzle-kit push          # Push directo (solo dev)
```

---

## Buenas prácticas

```typescript
// ✅ Connection management
// Un PrismaClient/DB por aplicación (singleton)
import { PrismaClient } from '@prisma/client';
const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };
export const prisma = globalForPrisma.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;

// ✅ Batch sobre loop
// ❌ N+1: una query por cada orden
for (const order of orders) {
  order.items = await prisma.orderItem.findMany({ where: { orderId: order.id } });
}
// ✅ Una query con include
const orders = await prisma.order.findMany({
  where: { customerId },
  include: { items: true },
});

// ✅ Paginación keyset
const page = await db.select().from(orders)
  .where(gte(orders.createdAt, cursor))
  .orderBy(desc(orders.createdAt))
  .limit(20);

// ✅ Select solo columnas necesarias
await db.select({ id: orders.id, status: orders.status }).from(orders);
```

---

## Checklist database

- [ ] ORM elegido según caso (Prisma: equipo grande, Drizzle: serverless)
- [ ] Connection pooling configurado (max connections, idle timeout)
- [ ] Migraciones versionadas y en CI
- [ ] Sin N+1: usar `include`/`with` o `in` batch queries
- [ ] Batch updates en vez de loop + update individual
- [ ] Raw SQL solo para queries complejas (reportes, analytics)
- [ ] SQL parametrizado siempre (Prisma/Drizzle lo manejan)
- [ ] PgBouncer si >200 conexiones concurrentes en PostgreSQL
