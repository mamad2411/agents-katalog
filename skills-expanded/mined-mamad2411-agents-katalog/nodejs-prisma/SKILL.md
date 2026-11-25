---
name: nodejs-prisma
description: "Prisma 7 ORM en Node.js (2026). Cubre schema declaration (PSL), modelos y relaciones, Prisma Client CRUD, nested writes, filtering/sorting/pagination, interactive transactions y batch, middleware con client extensions ($extends), migraciones con Prisma Migrate, seeding, SQL Server + PostgreSQL, raw SQL con $queryRaw, Prisma Accelerate, connection pooling, y estrategia híbrida con Drizzle. Actívala cuando el proyecto use Prisma como ORM, al diseñar schemas, implementar queries type-safe, o configurar migraciones."
---

# Prisma 7 ORM — Schema-first TypeScript ORM

Guía de Prisma 7 (Nov 2025). Sin Rust engine por defecto, ESM nativo, driver adapters obligatorios. Schema declarativo (PSL), auto-generated client, Prisma Migrate, Prisma Studio.

---

## Setup

```bash
npm i @prisma/client
npm i -D prisma
```

```typescript
// prisma.config.ts — Configuración Prisma 7
import { defineConfig, env } from 'prisma/config';

export default defineConfig({
  schema: 'prisma/schema.prisma',
  migrations: {
    path: 'prisma/migrations',
    seed: 'tsx prisma/seed.ts',
  },
  datasource: {
    url: env('DATABASE_URL'),
    // Prisma 7: directUrl está deprecated, usar solo url
  },
});
```

```bash
# Generar Prisma Client (tipos + runtime)
npx prisma generate

# O con driver adapter explícito
npx prisma generate --generator client
```

```typescript
// db/prisma.ts — Singleton PrismaClient
// ponytail: globalThis guard, basta para evitar multi-instancia en dev
import { PrismaClient } from '../prisma/generated/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development'
    ? ['query', 'info', 'warn', 'error']
    : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

---

## Schema (Prisma Schema Language)

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
  output   = "./generated/client"
}

datasource db {
  provider = "postgresql" // o "sqlserver", "mysql", "sqlite", "cockroachdb"
}

// ── Enums ──
enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED

  @@map("order_status")
}

// ── Models ──
model Customer {
  id        String   @id @default(uuid())
  name      String   @db.VarChar(200)
  email     String   @unique @db.VarChar(320)
  createdAt DateTime @default(now()) @db.Timestamptz(3)

  orders    Order[]

  @@map("customers")
}

model Order {
  id          String      @id @default(uuid())
  orderNumber Int         @default(autoincrement())
  customerId  String      @db.Uuid
  status      OrderStatus @default(PENDING)
  totalAmount Decimal     @db.Decimal(18, 4)
  currency    String      @default("MXN") @db.VarChar(3)
  notes       String?     @db.Text
  isUrgent    Boolean     @default(false)
  createdAt   DateTime    @default(now()) @db.Timestamptz(3)
  updatedAt   DateTime    @updatedAt @db.Timestamptz(3)

  customer    Customer    @relation(fields: [customerId], references: [id])
  items       OrderItem[]

  @@index([customerId, status])
  @@index([createdAt])
  @@map("orders")
}

model OrderItem {
  id         String  @id @default(uuid())
  orderId    String  @db.Uuid
  sku        String  @db.VarChar(50)
  quantity   Int
  unitPrice  Decimal @db.Decimal(18, 4)
  lineNumber Int

  order      Order   @relation(fields: [orderId], references: [id], onDelete: Cascade)

  @@unique([orderId, sku])
  @@map("order_items")
}
```

### Tipos nativos PostgreSQL más usados

| PSL | PostgreSQL | Notas |
|-----|-----------|-------|
| `String` + `@db.Uuid` | `UUID` | GUID |
| `String` + `@db.VarChar(N)` | `VARCHAR(N)` | Texto limitado |
| `String` + `@db.Text` | `TEXT` | Texto ilimitado |
| `Int` | `INTEGER` | 4-byte |
| `BigInt` | `BIGINT` | 8-byte |
| `Float` | `DOUBLE PRECISION` | |
| `Decimal` + `@db.Decimal(P, S)` | `DECIMAL(P, S)` | Exacto |
| `Boolean` | `BOOLEAN` | |
| `DateTime` + `@db.Timestamptz(3)` | `TIMESTAMPTZ(3)` | Con timezone |
| `DateTime` + `@db.Date` | `DATE` | Solo fecha |
| `Json` | `JSONB` | |
| `Bytes` | `BYTEA` | Binario |

### Relaciones

```prisma
model User {
  id    Int     @id @default(autoincrement())
  posts Post[]
}

model Post {
  id       Int  @id @default(autoincrement())
  title    String
  author   User @relation(fields: [authorId], references: [id])
  authorId Int

  categories Category[]
}

model Category {
  id    Int    @id @default(autoincrement())
  name  String @unique
  posts Post[]
}

// Relación implícita many-to-many (Prisma maneja la tabla puente)
// Genera automáticamente: CREATE TABLE "_CategoryToPost" ("A" INT, "B" INT)

// Relación explícita many-to-many (tú defines la tabla puente)
model PostCategory {
  postId     Int
  categoryId Int
  post       Post     @relation(fields: [postId], references: [id])
  category   Category @relation(fields: [categoryId], references: [id])

  @@id([postId, categoryId])
  @@map("post_categories")
}

// Self-relation (manager/reports)
model Employee {
  id        Int        @id @default(autoincrement())
  name      String
  managerId Int?
  manager   Employee?  @relation("Manager", fields: [managerId], references: [id])
  reports   Employee[] @relation("Manager")
}

// One-to-one
model User {
  id      Int      @id @default(autoincrement())
  profile Profile?
}

model Profile {
  id     Int  @id @default(autoincrement())
  userId Int  @unique
  user   User @relation(fields: [userId], references: [id])
}
```

---

## Prisma Client — CRUD

### SELECT

```typescript
// findUnique — por ID o campo unique
const user = await prisma.user.findUnique({
  where: { email: 'elsa@prisma.io' },
});

// findFirst — primer registro que cumple filtro
const firstAdmin = await prisma.user.findFirst({
  where: { role: 'ADMIN' },
  orderBy: { createdAt: 'asc' },
});

// findMany — todos los que cumplen
const users = await prisma.user.findMany({
  where: {
    email: { endsWith: '@prisma.io' },
    role: { not: 'DELETED' },
  },
  orderBy: { createdAt: 'desc' },
  take: 20,
  skip: 0,
});

// findMany con relación eager-loaded
const usersWithPosts = await prisma.user.findMany({
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
    },
  },
});

// findMany con select (solo campos necesarios)
const summaries = await prisma.order.findMany({
  select: {
    id: true,
    status: true,
    totalAmount: true,
    customer: {
      select: { name: true, email: true },
    },
  },
});

// findMany con include + select combinados
const result = await prisma.user.findMany({
  include: {
    _count: { select: { posts: true } }, // cuenta de posts
    posts: {
      select: { title: true, createdAt: true },
      take: 3, // solo últimos 3 posts
    },
  },
});
```

### Filtros avanzados

```typescript
// AND / OR / NOT
const result = await prisma.order.findMany({
  where: {
    AND: [
      { status: 'PENDING' },
      { createdAt: { gte: new Date('2026-01-01') } },
    ],
    OR: [
      { totalAmount: { gt: 10000 } },
      { isUrgent: true },
    ],
    NOT: { customerId: excludedCustomerId },
  },
});

// Filtro por relación
const usersWithPosts = await prisma.user.findMany({
  where: {
    posts: {
      some: { published: true }, // al menos un post publicado
    },
  },
});

// Filtro por relación con todos cumpliendo condición
const usersAllPostsPublished = await prisma.user.findMany({
  where: {
    posts: {
      every: { published: true }, // TODOS los posts publicados
    },
  },
});

// Filtro sin relación (usuarios sin posts)
const usersNoPosts = await prisma.user.findMany({
  where: {
    posts: { none: {} },
  },
});

// Filtros de string
const search = await prisma.customer.findMany({
  where: {
    name: { contains: 'acme', mode: 'insensitive' },
    email: { startsWith: 'contact' },
  },
});

// Filtros de fecha
const recent = await prisma.order.findMany({
  where: {
    createdAt: {
      gte: new Date('2026-06-01'),
      lt: new Date('2026-07-01'),
    },
  },
});

// in / notIn
await prisma.order.findMany({
  where: { status: { in: ['PENDING', 'CONFIRMED'] } },
});

// isNull
await prisma.order.findMany({
  where: { notes: null }, // o { notes: { not: null } }
});
```

### INSERT

```typescript
// create — un registro
const user = await prisma.user.create({
  data: {
    email: 'alice@prisma.io',
    name: 'Alice',
    posts: {
      create: [
        { title: 'Hello World' },
        { title: 'Prisma is great' },
      ],
    },
  },
  include: { posts: true },
});

// createMany — batch insert
const result = await prisma.user.createMany({
  data: [
    { email: 'bob@prisma.io', name: 'Bob' },
    { email: 'carol@prisma.io', name: 'Carol' },
  ],
  skipDuplicates: true,
});
// Returns: { count: 2 }

// createManyAndReturn — batch insert + select (PostgreSQL, SQLite)
const users = await prisma.user.createManyAndReturn({
  data: [
    { email: 'dave@prisma.io', name: 'Dave' },
    { email: 'eve@prisma.io', name: 'Eve' },
  ],
  select: { id: true, email: true },
});
```

### UPDATE

```typescript
// update — un registro
await prisma.order.update({
  where: { id: orderId },
  data: { status: 'CONFIRMED' },
});

// updateMany — batch
await prisma.order.updateMany({
  where: {
    status: 'PENDING',
    createdAt: { lt: new Date(Date.now() - 24 * 60 * 60 * 1000) },
  },
  data: { status: 'EXPIRED' },
});

// updateManyAndReturn — batch + select (PostgreSQL, SQLite)
const expired = await prisma.order.updateManyAndReturn({
  where: { status: 'PENDING' },
  data: { status: 'EXPIRED' },
  select: { id: true },
});

// Operaciones atómicas en números
await prisma.post.update({
  where: { id: 42 },
  data: {
    views: { increment: 1 },
    likes: { decrement: 2 },
  },
});

// upsert — update or create
await prisma.user.upsert({
  where: { email: 'alice@prisma.io' },
  update: { name: 'Alice Updated' },
  create: { email: 'alice@prisma.io', name: 'Alice' },
});

// connect / disconnect para relaciones
await prisma.post.update({
  where: { id: 42 },
  data: {
    categories: {
      connect: [{ id: 1 }, { id: 2 }],
      disconnect: [{ id: 3 }],
    },
  },
});

// connectOrCreate
await prisma.post.update({
  where: { id: 42 },
  data: {
    categories: {
      connectOrCreate: {
        where: { name: 'NewCat' },
        create: { name: 'NewCat' },
      },
    },
  },
});
```

### DELETE

```typescript
// delete — un registro
await prisma.user.delete({ where: { id: 7 } });

// deleteMany — batch
await prisma.order.deleteMany({
  where: { status: 'CANCELLED' },
});

// Cascading delete manual (si no hay onDelete: Cascade en el schema)
const [deletedPosts, deletedUser] = await prisma.$transaction([
  prisma.post.deleteMany({ where: { authorId: 7 } }),
  prisma.user.delete({ where: { id: 7 } }),
]);
```

---

## Transacciones

### Nested writes (transacción implícita)

```typescript
// Todas las operaciones anidadas corren en una sola transacción
const team = await prisma.team.create({
  data: {
    name: 'Engineering',
    members: {
      create: [
        { email: 'alice@prisma.io', role: 'LEAD' },
        { email: 'bob@prisma.io', role: 'DEV' },
      ],
    },
  },
  include: { members: true },
});
```

### Sequential `$transaction([])`

```typescript
// Array de operaciones independientes, ejecutadas secuencialmente
const [deletedPosts, deletedUser] = await prisma.$transaction([
  prisma.post.deleteMany({ where: { authorId: 7 } }),
  prisma.user.delete({ where: { id: 7 } }),
]);
```

### Interactive `$transaction(async (tx) => {})`

```typescript
// Read-modify-write con lógica de negocio dentro de la transacción
const result = await prisma.$transaction(async (tx) => {
  // 1. Leer
  const sender = await tx.account.update({
    data: { balance: { decrement: 100 } },
    where: { email: 'alice@prisma.io' },
  });

  // 2. Validar
  if (sender.balance < 0) {
    throw new Error('Insufficient funds');
  }

  // 3. Escribir
  return tx.account.update({
    data: { balance: { increment: 100 } },
    where: { email: 'bob@prisma.io' },
  });
}, {
  maxWait: 5000,  // tiempo máximo para adquirir la transacción
  timeout: 10000, // tiempo máximo de ejecución
  isolationLevel: 'Serializable',
});
```

### Niveles de aislamiento

| Nivel | PostgreSQL | SQL Server |
|-------|-----------|------------|
| `ReadUncommitted` | ✅ | ✅ |
| `ReadCommitted` | ✅ (default) | ✅ (default) |
| `RepeatableRead` | ✅ | ✅ |
| `Snapshot` | — | ✅ |
| `Serializable` | ✅ | ✅ |

### Retry en conflictos de transacción (P2034)

```typescript
import { Prisma } from '../prisma/generated/client';

async function withRetry<T>(fn: () => Promise<T>, maxRetries = 5): Promise<T> {
  for (let retries = 0; retries < maxRetries; retries++) {
    try {
      return await fn();
    } catch (error) {
      if (error instanceof Prisma.PrismaClientKnownRequestError && error.code === 'P2034') {
        continue; // Write conflict, retry
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}

await withRetry(() =>
  prisma.$transaction(
    [prisma.resource.deleteMany({ where: { name: 'X' } }), prisma.resource.createMany({ data })],
    { isolationLevel: 'Serializable' },
  ),
);
```

---

## Client Extensions ($extends)

### Query middleware (logging + audit)

```typescript
const prismaWithMiddleware = prisma.$extends({
  name: 'logging-audit',
  query: {
    $allModels: {
      async $allOperations({ model, operation, args, query }) {
        const start = Date.now();
        const result = await query(args);
        const duration = Date.now() - start;

        if (duration > 500) {
          logger.warn({ model, operation, duration, args }, 'Slow query');
        }
        return result;
      },
    },
  },
});
```

### Result extensions (campos virtuales computados)

```typescript
const prismaWithVirtuals = prisma.$extends({
  result: {
    user: {
      fullName: {
        needs: { firstName: true, lastName: true },
        compute(user) {
          return `${user.firstName} ${user.lastName}`;
        },
      },
    },
  },
});

const user = await prismaWithVirtuals.user.findFirst({
  where: { id: 1 },
  // fullName está disponible sin pedirlo en select
});
```

### Model extensions (métodos custom en modelos)

```typescript
const prismaWithMethods = prisma.$extends({
  model: {
    user: {
      async signUp(email: string, name: string) {
        return prismaWithMethods.user.create({
          data: { email, name },
        });
      },
    },
  },
});

const user = await prismaWithMethods.user.signUp('new@prisma.io', 'New User');
```

### Client extensions (métodos a nivel cliente)

```typescript
const prismaWithClient = prisma.$extends({
  client: {
    $log: (message: string) => console.log(`[PRISMA] ${message}`),
  },
});

await prismaWithClient.$log('Application started');
```

### Row-Level Security con extensions

```typescript
// Cada request obtiene su propio extended client con tenant scoping
function getTenantClient(tenantId: string) {
  return prisma.$extends({
    query: {
      order: {
        async $allOperations({ args, query }) {
          // Enforce tenant scoping en todas las queries de Order
          if (args.where && 'AND' in args.where) {
            args.where.AND.push({ tenantId });
          } else {
            args.where = { ...args.where, tenantId };
          }
          return query(args);
        },
      },
    },
  });
}
```

---

## Migraciones (Prisma Migrate)

```bash
# Desarrollo: genera migración desde diff del schema
npx prisma migrate dev --name add-order-notes

# Aplicar migraciones pendientes en CI/producción
npx prisma migrate deploy

# Reset (⚠️ borra la DB, recrea y aplica migraciones + seed)
npx prisma migrate reset

# Estado de migraciones
npx prisma migrate status

# Diff entre schema y base de datos (sin generar migración)
npx prisma migrate diff
```

### Estructura de migraciones

```
prisma/migrations/
├── 20260101000000_init/
│   └── migration.sql
├── 20260115000000_add_order_notes/
│   └── migration.sql
└── migration_lock.toml
```

### Custom migration SQL

Dentro de `migration.sql` puedes editar el SQL generado. Ejemplo: agregar un índice partial o `CREATE EXTENSION IF NOT EXISTS "uuid-ossp"` manualmente.

---

## Seeding

```typescript
// prisma/seed.ts
import { PrismaClient } from '../prisma/generated/client';

const prisma = new PrismaClient();

async function main() {
  // Upsert para idempotencia
  const admin = await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      email: 'admin@example.com',
      name: 'Admin',
      role: 'ADMIN',
    },
  });

  const categories = await Promise.all(
    ['Tech', 'Business', 'Design'].map((name) =>
      prisma.category.upsert({
        where: { name },
        update: {},
        create: { name },
      }),
    ),
  );

  console.log('Seed completed');
}

main()
  .then(async () => { await prisma.$disconnect(); })
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
```

Ejecutar: `npx prisma db seed` (usa el comando definido en `prisma.config.ts`).

---

## Raw SQL

```typescript
// $queryRaw — SELECT tipado
interface OrderSummary {
  id: string;
  total: number;
  customer_name: string;
}

const orders = await prisma.$queryRaw<OrderSummary[]>`
  SELECT o.id, o.total_amount as total, c.name as customer_name
  FROM orders o
  JOIN customers c ON c.id = o.customer_id
  WHERE o.status = 'PENDING'
  ORDER BY o.created_at DESC
  LIMIT 50
`;

// $executeRaw — INSERT/UPDATE/DELETE sin retorno
await prisma.$executeRaw`
  UPDATE orders
  SET status = 'EXPIRED'
  WHERE status = 'PENDING' AND created_at < now() - interval '24 hours'
`;

// $queryRawUnsafe / $executeRawUnsafe (⚠️ solo con valores confiables)
const tableName = 'orders';
await prisma.$executeRawUnsafe(`TRUNCATE TABLE "${tableName}" CASCADE`);
```

---

## Prisma Studio

```bash
# GUI para ver/editar datos en el navegador
npx prisma studio
# Por defecto en http://localhost:5555
# Prisma 7.6+: modo oscuro disponible
```

---

## SQL Server (MSSQL)

```prisma
// schema.prisma
datasource db {
  provider = "sqlserver"
}

model Order {
  id          String   @id @default(uuid()) @db.UniqueIdentifier
  orderNumber Int      @default(autoincrement())
  customerId  String   @db.UniqueIdentifier
  status      String   @default("pending") @db.NVarChar(20)
  totalAmount Decimal  @db.Decimal(18, 4)
  currency    String   @default("MXN") @db.NVarChar(3)
  createdAt   DateTime @default(now()) @db.DateTime2(3)
  updatedAt   DateTime @updatedAt @db.DateTime2(3)

  @@index([customerId, status])
  @@index([createdAt])
  @@map("orders")
}
```

```typescript
// prisma.config.ts — SQL Server
export default defineConfig({
  schema: 'prisma/schema.prisma',
  datasource: {
    url: env('DATABASE_URL'), // sqlserver://HOST:1433;database=DB;user=USER;password=PASS;encrypt=true
  },
});
```

⚠️ SQL Server requiere TCP/IP habilitado. Para Azure SQL: `encrypt=true` + `trustServerCertificate=false`.

---

## Connection Pooling y Serverless

### Conexión directa (monolito/servidor)

```typescript
// Prisma maneja su propio pool. Configurar en connection string:
// postgresql://USER:PASS@HOST:5432/DB?connection_limit=20&pool_timeout=10
```

### Prisma Accelerate (serverless/edge)

```
// prisma.config.ts — URL de Accelerate en vez de conexión directa
datasource: {
  url: env('ACCELERATE_URL'), // prisma://...
}
```

Accelerate provee connection pooling gestionado + cache global. Ideal para:
- Serverless (Lambda, Cloudflare Workers)
- Edge functions
- >200 conexiones concurrentes

### PgBouncer

```
// Connection string con PgBouncer (modo transaction):
// postgresql://USER:PASS@PGBOUNCER_HOST:6432/DB?pgbouncer=true&connection_limit=5&pool_timeout=10
```

---

## Performance tips

```typescript
// ✅ Select solo lo necesario
await prisma.user.findMany({
  select: { id: true, email: true }, // vs include de todas las columnas
});

// ✅ Include anidado con filtros (evita N+1)
await prisma.user.findMany({
  include: {
    posts: { where: { published: true } },
    _count: { select: { posts: true } },
  },
});

// ✅ Batch sobre loop individual
await prisma.user.updateMany({
  where: { role: 'TEMP' },
  data: { role: 'USER' },
});
// ❌ NO: for (const user of users) await prisma.user.update(...)

// ✅ findFirst con índice
await prisma.order.findFirst({
  where: { customerId, status: 'PENDING' },
  orderBy: { createdAt: 'asc' },
});
// Asegúrate de tener @@index([customerId, status, createdAt])

// ✅ Paginación keyset (más rápido que offset en tablas grandes)
const page = await prisma.order.findMany({
  where: { createdAt: { lt: cursor } },
  orderBy: { createdAt: 'desc' },
  take: 20,
});
```

---

## ¿Prisma o Drizzle?

| Criterio | Prisma 7 | Drizzle |
|----------|----------|---------|
| **Enfoque** | Schema-first declarativo (PSL) | Schema en TypeScript (SQL-like) |
| **Bundle** | ~2MB client runtime | ~7.4KB runtime |
| **Type safety** | Generado por CLI | Inferido del schema TS |
| **Relaciones** | API declarativa `include`/`select` | `with` en relational queries |
| **Migraciones** | `prisma migrate dev/deploy` | `drizzle-kit generate/migrate` |
| **Tooling** | ⭐ Prisma Studio, VSCode extension | `drizzle-studio` (beta) |
| **Raw SQL** | `$queryRaw` / `$executeRaw` | ⭐ `sql` template nativo |
| **Serverless** | Bueno (sin Rust engine en v7) + Accelerate | ⭐ Nativo (zero deps) |
| **Ecosistema** | ⭐⭐⭐⭐⭐ Consolidado | ⭐⭐⭐ Creciente |

**Regla 2026**: Schema-first + tooling + equipo grande → **Prisma 7**. SQL explícito + serverless puro + bundle mínimo → **Drizzle**. Ambos son excelentes.

---

## Checklist Prisma

- [ ] `prisma.config.ts` configurado con `datasource.url` (no `directUrl`)
- [ ] `prisma generate` ejecutado tras cada cambio de schema
- [ ] PrismaClient como singleton (`globalThis` guard en dev)
- [ ] Migraciones versionadas (`prisma migrate dev`) + aplicadas en CI (`prisma migrate deploy`)
- [ ] Seed idempotente (upsert, no create directo)
- [ ] Nested writes (`create: [...]`) para operaciones dependientes en vez de N queries
- [ ] `include`/`select` con filtros para evitar N+1
- [ ] Batch updates (`updateMany`/`deleteMany`) sobre loops
- [ ] `$transaction` para operaciones atómicas multi-modelo
- [ ] Retry en P2034 (transaction write conflicts)
- [ ] Raw SQL parametrizado con `$queryRaw` template literal (nunca `$queryRawUnsafe` con input usuario)
- [ ] Connection pool configurado (`connection_limit`, `pool_timeout`)
- [ ] Accelerate o PgBouncer en serverless/alta concurrencia
- [ ] `clientExtensions` para cross-cutting concerns (logging, audit, soft-delete)
