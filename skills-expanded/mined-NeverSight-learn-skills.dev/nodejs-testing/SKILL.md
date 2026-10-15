---
name: nodejs-testing
description: "Testing en Node.js con Vitest 4/5, node:test, Playwright y MSW. Cubre unit tests, integration tests, mocking (vi.fn, MSW), Testcontainers, snapshot testing, coverage, y TDD. Stack recomendado 2026: Vitest + Playwright + MSW + Testcontainers. Actívala al escribir tests, configurar CI/CD, o definir estrategia de testing."
disable-model-invocation: true
---

# Node.js Testing

Guía de testing en Node.js 2026. **Vitest 4/5 como runner principal.** `node:test` para utilidades simples.

---

## Stack de testing

| Herramienta | Propósito | Paquete |
|-------------|-----------|---------|
| **Vitest 4/5** | Runner + assertions + coverage | `vitest` |
| **Playwright** | E2E y component testing | `@playwright/test` |
| **MSW** | Mock de HTTP a nivel red | `msw` |
| **Testcontainers** | PostgreSQL/SQL Server real en tests | `@testcontainers/postgresql` |
| **supertest** | HTTP assertions para Express/Fastify | `supertest` |

---

## Vitest — Unit & Integration Tests

### Setup

```bash
npm install -D vitest @vitest/coverage-v8
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.test.ts', 'src/types/**'],
    },
    // Timeout para integration tests
    testTimeout: 10_000,
  },
});
```

### Unit test AAA

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { OrderService } from './orders.service.js';

describe('OrderService', () => {
  let service: OrderService;
  const mockRepo = {
    create: vi.fn(),
    findById: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    service = new OrderService(mockRepo);
  });

  it('creates order with valid data', async () => {
    // Arrange
    const input = { customerId: 'CUST-001', amount: 100 };
    mockRepo.create.mockResolvedValue({ id: '1', ...input, status: 'pending' });

    // Act
    const order = await service.create(input);

    // Assert
    expect(order.id).toBe('1');
    expect(order.status).toBe('pending');
    expect(mockRepo.create).toHaveBeenCalledWith(input);
  });

  it('throws on negative amount', async () => {
    // Arrange
    const input = { customerId: 'CUST-001', amount: -100 };

    // Act & Assert
    await expect(() => service.create(input))
      .rejects.toThrow('amount must be positive');
  });
});
```

### Mocking con vi.fn y vi.mock

```typescript
// Mock de módulo completo
vi.mock('../database/prisma.js', () => ({
  prisma: {
    order: {
      findMany: vi.fn(),
      create: vi.fn(),
      findUnique: vi.fn(),
    },
  },
}));

// Mock parcial (solo algunas funciones)
import * as paymentService from './payment.service.js';
vi.spyOn(paymentService, 'processPayment')
  .mockResolvedValue({ id: 'pay_123', status: 'succeeded' });

// Mock de fecha
vi.setSystemTime(new Date('2026-06-23T12:00:00Z'));

// Mock de variable de entorno
vi.stubEnv('DATABASE_URL', 'postgresql://test:test@localhost:5432/test');
```

### Parametrized tests

```typescript
it.each([
  ['pending', true],
  ['confirmed', true],
  ['shipped', false],
  ['delivered', false],
  ['cancelled', false],
])('canCancel status=%s → %s', (status, expected) => {
  const order = { status };
  expect(canCancel(order)).toBe(expected);
});
```

---

## Integration Tests con Express

```typescript
import supertest from 'supertest';
import { createApp } from '../app.js';

describe('Orders API', () => {
  let request: supertest.Agent;

  beforeAll(async () => {
    const app = await createApp({ db: testDb });
    request = supertest(app);
  });

  it('POST /api/orders creates order', async () => {
    const res = await request
      .post('/api/orders')
      .send({ customerId: 'CUST-001', amount: 100 })
      .expect(201);

    expect(res.body).toMatchObject({
      id: expect.any(String),
      status: 'pending',
      customerId: 'CUST-001',
      amount: '100.00',
    });
  });

  it('POST /api/orders returns 400 on invalid input', async () => {
    const res = await request
      .post('/api/orders')
      .send({ customerId: '', amount: -5 })
      .expect(400);

    expect(res.body.error.code).toBe('VALIDATION_ERROR');
  });

  it('GET /api/orders/:id returns 404 if not found', async () => {
    await request
      .get('/api/orders/non-existent')
      .expect(404);
  });
});
```

---

## MSW — Mock Service Worker

```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

// Define los handlers de APIs externas
const stripeHandlers = [
  http.post('https://api.stripe.com/v1/charges', () => {
    return HttpResponse.json({ id: 'ch_test_123', status: 'succeeded' });
  }),

  http.post('https://api.stripe.com/v1/charges', async ({ request }) => {
    const body = await request.text();
    if (body.includes('amount=0')) {
      return HttpResponse.json(
        { error: { message: 'Invalid amount' } },
        { status: 400 },
      );
    }
    return HttpResponse.json({ id: 'ch_test_456', status: 'succeeded' });
  }),
];

const server = setupServer(...stripeHandlers);

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Ahora tu código que llama a Stripe usará MSW en vez de la red real.
```

---

## Testcontainers (PostgreSQL real)

```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql';
import { PrismaClient } from '@prisma/client';

describe('OrderRepository (integration)', () => {
  let container: PostgreSqlContainer;
  let prisma: PrismaClient;

  beforeAll(async () => {
    container = await new PostgreSqlContainer('postgres:18-alpine')
      .withDatabase('test')
      .withUsername('test')
      .withPassword('test')
      .start();

    prisma = new PrismaClient({
      datasources: { db: { url: container.getConnectionUri() } },
    });
    await prisma.$executeRawUnsafe('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"');
    // Ejecutar migraciones
  }, 30_000);

  afterAll(async () => {
    await prisma.$disconnect();
    await container.stop();
  });

  it('persists and retrieves orders', async () => {
    const repo = new OrderRepository(prisma);

    await repo.create({ customerId: 'CUST-001', amount: 100 });
    const orders = await repo.findByCustomer('CUST-001');

    expect(orders).toHaveLength(1);
    expect(orders[0].amount.toString()).toBe('100');
  });
});
```

---

## Playwright E2E (2026 features)

```bash
npm install -D @playwright/test
npx playwright install
```

```typescript
import { test, expect } from '@playwright/test';

test.describe('Orders E2E', () => {
  test('creates order and sees it in list', async ({ page }) => {
    await page.goto('/orders');

    // Click en "New Order"
    await page.getByRole('button', { name: 'New Order' }).click();

    // Fill form
    await page.getByLabel('Customer ID').fill('CUST-001');
    await page.getByLabel('Amount').fill('100');
    await page.getByRole('button', { name: 'Create' }).click();

    // Assert aparece en la lista
    await expect(page.getByText('CUST-001')).toBeVisible();
    await expect(page.getByText('100.00')).toBeVisible();
  });

  // AI assertion (Playwright 2026 agent mode)
  test('validates required fields', async ({ page }) => {
    await page.goto('/orders/new');
    await page.getByRole('button', { name: 'Create' }).click();

    // AI-powered assertion
    await expect(page).toMatchAriaSnapshot(`
      - text: Customer ID is required
      - text: Amount must be positive
    `);
  });
});
```

---

## `node:test` — para utilidades simples

```typescript
import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { calculateShipping } from './shipping.js';

describe('calculateShipping', () => {
  it('returns 0 for orders >= 100', () => {
    assert.strictEqual(calculateShipping(150), 0);
  });

  it('returns 99 for orders < 100', () => {
    assert.strictEqual(calculateShipping(50), 99);
  });
});
```

Cuándo usar `node:test`: librerías simples, sin watch mode, sin snapshot, sin coverage fancy.

---

## Checklist de testing

- [ ] Vitest como runner principal (coverage, watch, snapshots)
- [ ] Integration tests con supertest + base de datos real (Testcontainers)
- [ ] MSW para mock de APIs externas (Stripe, email, etc.)
- [ ] Playwright para E2E críticos (happy paths)
- [ ] AAA o Given/When/Then en nombres de tests
- [ ] Mock solo lo externo (APIs, DB si no es integration test)
- [ ] Sin mock de logger (usar pino con level silent en tests)
- [ ] Tests independientes: no comparten estado mutable
- [ ] Coverage ≥ 80% en lógica de negocio
- [ ] CI ejecuta tests con `--reporter=github-actions`
