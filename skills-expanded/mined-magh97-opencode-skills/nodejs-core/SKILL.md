---
name: nodejs-core
description: "Guía principal de Node.js (24 LTS / 26 Current): runtime, ESM vs CJS, TypeScript 7, async/await, streams, eventos, Temporal, debugging y node:test. Úsala para cualquier tarea Node.js: proyectos, migraciones, revisión o entorno."
---

# Node.js Core Development Guide

Guía canónica para desarrollo Node.js moderno. Node 24 LTS y 26 Current. TypeScript 7 con Go compiler. Todo código sigue estas reglas salvo indicación contraria.

## Versiones

| Versión | Tipo | Lanzamiento | LTS hasta | V8 | Novedades clave |
|---------|------|------------|-----------|-----|-----------------|
| Node 22 | LTS | Abr 2024 | Abr 2027 | 12.7 | ESM estable, `require(esm)` |
| Node 24 | LTS | Oct 2024 | Abr 2028 | 13.x | `randomUUIDv7()`, `node:sqlite` |
| **Node 26** | **Current** | May 2026 | ~Abr 2029 (LTS) | **14.6** | **Temporal API default**, **Undici 8**, test runner snapshots |

- **Proyectos nuevos** → Node 24 LTS en producción, Node 26 para features como Temporal API.
- **Migraciones** → 22 → 24 directo. 24 → 26 en Oct 2026 cuando entre a LTS.

---

## ESM vs CommonJS (estado 2026)

### Línea de tiempo resuelta

| Hito | Fecha | Estado |
|------|-------|--------|
| `require(esm)` experimental | Node 22 | Experimental |
| `require(esm)` estable | Node 22.12 / 24 LTS | ✅ Estable y sin flag |
| ESM default en paquetes npm | 2025-2026 | Mayoría de paquetes populares migrados |

✅ **Regla 2026: ESM por defecto para proyectos nuevos.** CJS solo para compatibilidad legacy.

```json
// package.json
{
  "type": "module",
  "scripts": {
    "dev": "tsx --watch src/index.ts",
    "build": "tsgo --noEmit && vite build"
  }
}
```

### Sintaxis ESM

```typescript
// ✅ ESM moderno
import { readFile } from 'node:fs/promises';
import express from 'express';
import { z } from 'zod';

export async function loadConfig(path: string) {
  const raw = await readFile(path, 'utf-8');
  return ConfigSchema.parse(JSON.parse(raw));
}

// CJS que consume ESM (estable en Node 24+)
// const { loadConfig } = await import('./config.js');

// ⚠️ __dirname / __filename no existen en ESM
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
```

### Package exports moderno

```json
{
  "name": "miapp-lib",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    },
    "./utils": {
      "types": "./dist/utils.d.ts",
      "import": "./dist/utils.js"
    }
  }
}
```

---

## TypeScript 7 (Project Corsa — Go Compiler)

```bash
# Instalar la versión estable más reciente
# (verifica si TypeScript 7 ya salió de RC al momento de instalar)
npm install -D typescript@latest

# Compilar con Go compiler (tsgo)
npx tsgo --noEmit           # Type-check 10x más rápido
npx tsgo --outDir dist      # Emitir .js

# tsconfig.json mínimo
```

```json
{
  "compilerOptions": {
    "target": "ES2024",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### Breaking changes TS 7

| Cambio | Impacto | Acción |
|--------|---------|--------|
| `strict: true` por defecto | ✅ Bueno. Si quieres `false`, explícito. | Mantener `strict: true`. |
| ES5 target eliminado | Solo afecta si compilabas a ES5 | `target: "ES2022"` mínimo |
| Compiler API removida en `tsgo` | Plugins/bundlers que usaban TS API programáticamente | Usar `tsgo` CLI o migrar a `@oxc-transform/typescript` para plugins |
| Deprecations TS 6 → errores en TS 7 | `out`, `charset`, `keyofStringsOnly` | Revisar tsconfig |

### tsx (recomendado para desarrollo)

```bash
npm install -D tsx

# Ejecutar TypeScript directamente (sin compilar)
npx tsx src/index.ts            # Ejecución única
npx tsx --watch src/index.ts    # Hot reload en desarrollo
```

---

## Temporal API (Node 26 default)

```typescript
// ✅ Temporal — reemplaza a Date. Inmutable, timezone-aware, preciso.
import { Temporal } from 'node:temporal'; // Node 26 (o polyfill en 24-)

// Fecha actual en UTC
const now = Temporal.Now.instant();
// Fecha en zona específica
const mexicoCity = now.toZonedDateTimeISO('America/Mexico_City');
console.log(mexicoCity.toString()); // 2026-06-23T09:30:00-06:00[America/Mexico_City]

// Aritmética de fechas sin mutación
const nextWeek = now.add({ days: 7 });
const firstOfMonth = now.toPlainDate().with({ day: 1 });

// Comparación
const isAfter = Temporal.PlainDate.compare(date1, date2) > 0;

// Duración exacta
const duration = Temporal.Duration.from({ hours: 2, minutes: 30 });
console.log(duration.total('minutes')); // 150

// Formateo con Intl (sin biblioteca externa)
const formatted = mexicoCity.toLocaleString('es-MX', {
  dateStyle: 'long',
  timeStyle: 'short',
});
```

---

## Async/Await moderno

```typescript
// ✅ Top-level await (ESM, desde Node 14.8)
const config = await loadConfig('./config.json');

// ✅ Promise.allSettled — no falla si una promesa falla
const results = await Promise.allSettled([
  fetchUser(id1),
  fetchUser(id2),
  fetchUser(id3),
]);
for (const result of results) {
  if (result.status === 'fulfilled') console.log(result.value);
  else console.error('Failed:', result.reason);
}

// ✅ AbortSignal para cancelar operaciones
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);

try {
  const data = await fetch(url, { signal: controller.signal });
} catch (err) {
  if (err.name === 'AbortError') console.log('Request cancelled');
} finally {
  clearTimeout(timeout);
}

// ✅ for await...of con streams
async function* generatePages(apiUrl: string) {
  let page = 1;
  while (true) {
    const data = await fetch(`${apiUrl}?page=${page}`).then(r => r.json());
    if (data.length === 0) break;
    yield data;
    page++;
  }
}

for await (const page of generatePages('/api/orders')) {
  await processOrders(page);
}
```

---

## Streams

```typescript
import { createReadStream, createWriteStream } from 'node:fs';
import { pipeline } from 'node:stream/promises';
import { Transform } from 'node:stream';
import { createGzip } from 'node:zlib';

// ✅ pipeline (maneja backpressure y limpieza automáticamente)
await pipeline(
  createReadStream('input.csv'),
  new Transform({
    transform(chunk, encoding, callback) {
      // Procesar chunk
      const processed = processChunk(chunk.toString());
      callback(null, processed);
    },
  }),
  createGzip(),
  createWriteStream('output.csv.gz'),
);

// ✅ Streams consumibles con for await
import { Readable } from 'node:stream';
async function* generateData() {
  for (let i = 0; i < 1000; i++) {
    yield JSON.stringify({ id: i, value: Math.random() }) + '\n';
  }
}
const readable = Readable.from(generateData());
for await (const chunk of readable) {
  // chunk es string
}
```

---

## Eventos y EventEmitter

```typescript
import { EventEmitter } from 'node:events';

// EventEmitter tipado
interface OrderEvents {
  created: [order: Order];
  cancelled: [orderId: string, reason: string];
  error: [error: Error];
}

class OrderService extends EventEmitter<OrderEvents> {
  async create(data: CreateOrderInput) {
    const order = await this.save(data);
    this.emit('created', order);
    return order;
  }
}

// Consumir con async iterators (Node 22+)
const service = new OrderService();
const events = on(service, 'created', { signal: abortController.signal });
for await (const [order] of events) {
  await sendConfirmationEmail(order);
}
```

---

## Debugging

```bash
# Inspector built-in de Node
node --inspect-brk src/index.ts      # Pausa al inicio, puerto 9229
# Chrome: chrome://inspect → Open dedicated DevTools

# VS Code launch.json
{
  "type": "node",
  "request": "launch",
  "name": "Debug TS (tsx)",
  "runtimeExecutable": "npx",
  "runtimeArgs": ["tsx", "--inspect-brk", "src/index.ts"],
  "skipFiles": ["<node_internals>/**"]
}
```

### Utilidades de debug

```typescript
import { debuglog } from 'node:util';
const debug = debuglog('miapp:orders');

debug('Processing order %s for customer %s', orderId, customerId);
// Solo se imprime si NODE_DEBUG=miapp:orders está seteado

// --watch (Node 22+) reinicia al guardar archivos
// node --watch --experimental-strip-types src/index.ts
```

---

## `node:test` (test runner nativo)

```typescript
import { describe, it, beforeEach, mock } from 'node:test';
import assert from 'node:assert/strict';

describe('OrderService', () => {
  let service: OrderService;

  beforeEach(() => {
    service = new OrderService(mockRepository());
  });

  it('creates order successfully', async () => {
    const order = await service.create({
      customerId: 'CUST-001',
      amount: 100,
    });
    assert.ok(order.id);
    assert.strictEqual(order.status, 'pending');
  });

  it('throws on negative amount', async () => {
    await assert.rejects(
      () => service.create({ customerId: 'X', amount: -100 }),
      { message: /amount must be positive/ },
    );
  });
});
```

Para proyectos con coverage, watch mode, snapshot testing → Vitest (ver `nodejs-testing`).

---

## Convenciones de código

### Naming

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Archivos | `kebab-case.ts` | `order-service.ts`, `create-order.handler.ts` |
| Clases/Interfaces | `PascalCase` | `OrderService`, `ICreateOrderInput` |
| Funciones | `camelCase` | `createOrder()`, `calculateTotal()` |
| Variables | `camelCase` | `orderId`, `totalAmount` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_RETRY_ATTEMPTS`, `DEFAULT_PAGE_SIZE` |
| Type imports | `import type { ... }` | `import type { Order, Customer } from './types.js'` |

### Estructura de proyecto

```
src/
├── index.ts                    # Entry point
├── config/
│   ├── env.ts                  # Zod-validated config
│   └── database.ts             # DB connection setup
├── modules/
│   └── orders/
│       ├── orders.controller.ts  # HTTP handlers
│       ├── orders.service.ts    # Business logic
│       ├── orders.repository.ts # Data access
│       ├── orders.schema.ts     # Zod schemas
│       ├── orders.routes.ts     # Route definitions
│       └── orders.test.ts       # Tests
├── shared/
│   ├── middleware/
│   │   ├── error-handler.ts
│   │   ├── auth.ts
│   │   └── validation.ts
│   ├── errors/
│   │   └── app-error.ts
│   └── utils/
│       └── pagination.ts
└── types/
    └── global.d.ts
```

---

## Reglas de oro

1. **ESM por defecto.** `"type": "module"` en proyectos nuevos. `import` y `export`, no `require`.
2. **TypeScript 7 `strict: true`.** Sin excepciones. No `any` sin justificación explícita.
3. **`node:` prefix para built-ins.** `import fs from 'node:fs/promises'`, no `import fs from 'fs'`.
4. **Zod para validación de entrada.** Toda frontera (API, CLI, config) valida con Zod.
5. **`AbortSignal` en todo async.** Permite cancelación y evita memory leaks.
6. **`for await...of` y streams en vez de cargar todo en memoria.** Para archivos grandes y paginación.
7. **`pipeline()` sobre `.pipe()`.** Maneja backpressure y limpieza correctamente.
8. **No `console.log` en producción.** Usar `pino` o al menos `debuglog`.
9. **`.env` con Zod.** Validar todas las variables de entorno al arrancar.
10. **Un archivo por responsabilidad.** Controller no mezcla lógica de negocio ni acceso a datos.

---

## Sub-skills del kit

> 📁 Cada sub-skill tiene su propio `SKILL.md` con el detalle; el subagente `.opencode/agent/node.md` decide cuál cargar según la tarea.


| Skill | Cuándo cargarla |
|-------|-----------------|
| `nodejs-express` | Express 5, Fastify, Hono — REST APIs, middleware, routing |
| `nodejs-performance` | Worker threads, clustering, profiling, memory leaks, streams |
| `nodejs-security` | Helmet, CORS, rate limiting, JWT, input validation, OWASP |
| `nodejs-testing` | Vitest, node:test, Playwright, MSW, Testcontainers |
| `nodejs-database` | Prisma 7, SQL Server + PostgreSQL, connection pooling, migrations (overview) |
| `nodejs-database` → `references/prisma.md` | Prisma 7 — schema PSL, CRUD, nested writes, interactive transactions, client extensions, migrate, seed, Accelerate |
| `nodejs-database` → `references/drizzle.md` | Drizzle ORM — schema TS, queries SQL-like/relacionales, drizzle-kit, Zod, MSSQL, prepared statements |
| `nodejs-deployment` | Docker, PM2, CI/CD, pino, OpenTelemetry |
| `nodejs-architecture` | Clean/Hexagonal, DI, monorepo, event-driven |

---

## Stack recomendado por defecto

| Propósito | Herramienta | Paquete |
|-----------|-------------|---------|
| Runtime | Node.js 24 LTS | — |
| TypeScript | TS 7 (Go compiler) | `typescript@7` |
| Dev runner | tsx | `tsx` |
| HTTP framework | Express 5 o Fastify | `express@5` / `fastify` |
| Validación | Zod | `zod` |
| Logger | Pino | `pino` |
| ORM | Prisma 7 o Drizzle | `@prisma/client` / `drizzle-orm` (ver `nodejs-database` y sus `references/`) |
| Testing | Vitest + node:test | `vitest` |
| Linting | ESLint 9 flat config | `eslint` |
| Formatting | Prettier | `prettier` |
