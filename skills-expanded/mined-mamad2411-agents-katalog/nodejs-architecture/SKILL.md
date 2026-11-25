---
name: nodejs-architecture
description: "Arquitectura de aplicaciones Node.js. Cubre Clean Architecture, Hexagonal (Ports & Adapters), Vertical Slices, Modular Monolith, DI (tsyringe vs manual), monorepo con Turborepo, event-driven (EventEmitter, RabbitMQ), y project structure. Actívala al diseñar la estructura de un proyecto Node.js nuevo, evaluar migraciones arquitectónicas, o definir convenciones de equipo."
disable-model-invocation: true
---

# Node.js Architecture

Guía de estilos arquitectónicos aplicados a Node.js + TypeScript.

---

## Tabla de decisión

| Arquitectura | Tamaño | Complejidad dominio | Recomendado para |
|-------------|--------|---------------------|------------------|
| **Vertical Slices** | Pequeño-Mediano | Media | Startups, entregas rápidas |
| **Clean Architecture** | Mediano-Grande | Alta | Dominios ricos, largo plazo |
| **Hexagonal (Ports & Adapters)** | Mediano-Grande | Alta | Alta testeabilidad, múltiples adapters |
| **Modular Monolith** | Mediano-Grande | Alta | Migrar de monolito a microservicios gradualmente |

---

## Vertical Slices (recomendado para la mayoría)

```
src/
├── modules/
│   └── orders/
│       ├── orders.controller.ts    # HTTP handlers
│       ├── orders.service.ts       # Lógica de negocio
│       ├── orders.repository.ts    # Acceso a datos
│       ├── orders.schema.ts        # Zod schemas
│       ├── orders.routes.ts        # Definición de rutas
│       ├── orders.test.ts          # Tests
│       └── index.ts                # Exporta rutas
│   └── customers/
│       ├── customers.controller.ts
│       ├── customers.service.ts
│       └── ...
├── shared/
│   ├── middleware/
│   │   ├── auth.ts
│   │   ├── error-handler.ts
│   │   └── validation.ts
│   ├── errors/
│   │   └── app-error.ts
│   └── utils/
│       ├── pagination.ts
│       └── logger.ts
├── config/
│   ├── env.ts
│   └── database.ts
├── index.ts
└── app.ts
```

Cada módulo es autónomo. Un equipo puede trabajar en `orders/` sin tocar `customers/`.

---

## Clean Architecture

```
src/
├── modules/
│   └── orders/
│       ├── domain/                  # Entidades, value objects, reglas
│       │   ├── order.entity.ts
│       │   ├── order-item.entity.ts
│       │   ├── order-status.value-object.ts
│       │   └── order.repository.ts  # Interfaz (puerto)
│       ├── application/             # Casos de uso
│       │   ├── create-order.use-case.ts
│       │   ├── cancel-order.use-case.ts
│       │   └── ports/
│       │       ├── order.repository.port.ts
│       │       └── payment-gateway.port.ts
│       ├── infrastructure/           # Implementaciones concretas
│       │   ├── prisma-order.repository.ts
│       │   ├── stripe-payment.gateway.ts
│       │   └── orders.controller.ts
│       └── presentation/            # DTOs, validators
│           ├── create-order.dto.ts
│           └── create-order.schema.ts
```

### Regla de dependencia

```
Presentation → Application → Domain ← Infrastructure
```

**Domain no depende de nada externo.** Infrastructure implementa puertos definidos en Domain/Application.

### Ejemplo

```typescript
// domain/order.repository.ts (puerto)
export interface IOrderRepository {
  save(order: Order): Promise<Order>;
  findById(id: string): Promise<Order | null>;
}

// application/create-order.use-case.ts
export class CreateOrderUseCase {
  constructor(
    private readonly orderRepo: IOrderRepository,
    private readonly paymentGateway: IPaymentGateway,
  ) {}

  async execute(input: CreateOrderInput): Promise<Order> {
    const order = Order.create(input);
    await this.orderRepo.save(order);
    return order;
  }
}

// infrastructure/prisma-order.repository.ts
export class PrismaOrderRepository implements IOrderRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async save(order: Order): Promise<Order> {
    await this.prisma.order.upsert({ ... });
    return order;
  }
}
```

---

## DI — tsyringe vs manual

```typescript
// ✅ DI manual: simple, sin bibliotecas, bueno para proyectos pequeños
export function createOrderController(prisma: PrismaClient) {
  const repo = new PrismaOrderRepository(prisma);
  const service = new OrderService(repo);
  return new OrderController(service);
}

// Para proyectos grandes: tsyringe
import { container, injectable, inject } from 'tsyringe';

@injectable()
export class OrderService {
  constructor(
    @inject('IOrderRepository') private readonly repo: IOrderRepository,
  ) {}
}

// Registrar
container.register('IOrderRepository', { useClass: PrismaOrderRepository });
container.register('IPaymentGateway', { useClass: StripePaymentGateway });

// Resolver
const service = container.resolve(OrderService);
```

---

## Monorepo — Turborepo

```
packages/
├── apps/
│   ├── api/                 # Backend Node.js
│   │   ├── src/
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── web/                 # Frontend React
├── packages/
│   ├── shared/              # Tipos, DTOs, validators compartidos
│   │   ├── src/
│   │   │   ├── types/
│   │   │   └── schemas/
│   │   └── package.json
│   ├── database/            # Prisma schema + client
│   │   ├── prisma/
│   │   └── package.json
│   └── config-eslint/
├── package.json             # Workspaces
├── turbo.json
└── pnpm-workspace.yaml
```

```json
// turbo.json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**/*.ts", "test/**/*.ts"]
    },
    "lint": {},
    "typecheck": {
      "dependsOn": ["^build"]
    }
  }
}
```

---

## Event-Driven

```typescript
// EventEmitter para comunicación entre módulos
import { EventEmitter } from 'node:events';

// Event bus compartido (módulos se comunican sin acoplarse)
interface AppEvents {
  'order.created': [order: Order];
  'payment.completed': [paymentId: string, orderId: string];
}

const eventBus = new EventEmitter<AppEvents>();

// orders.module.ts — emite evento
eventBus.emit('order.created', order);

// shipping.module.ts — reacciona al evento
eventBus.on('order.created', async (order) => {
  await shippingService.schedulePickup(order);
});

// notifications.module.ts — reacciona al mismo evento
eventBus.on('order.created', async (order) => {
  await emailService.sendConfirmation(order);
});
```

### RabbitMQ / BullMQ para producción

```typescript
import { Queue } from 'bullmq';

const orderQueue = new Queue('orders', {
  connection: { host: process.env.REDIS_HOST, port: 6379 },
});

// Productor
await orderQueue.add('order.created', { orderId: order.id }, {
  attempts: 3,
  backoff: { type: 'exponential', delay: 1000 },
});

// Consumidor (otro proceso)
import { Worker } from 'bullmq';

const worker = new Worker('orders', async (job) => {
  if (job.name === 'order.created') {
    await handleOrderCreated(job.data);
  }
}, { connection: { host: process.env.REDIS_HOST, port: 6379 } });
```

---

## Reglas de acoplamiento

- **Módulos no se importan entre sí.** Si dos módulos necesitan comunicarse → event bus o service layer compartido.
- **Capa de datos solo en infrastructure/repository.** Service nunca importa Prisma/Drizzle directamente.
- **DTOs en presentation o interface.** Domain no conoce HTTP.
- **Compartido (`shared/`) solo para middleware, errores base, utilidades puras sin lógica de negocio.**

---

## Checklist de arquitectura

- [ ] Estructura elegida según tamaño y complejidad
- [ ] Módulos desacoplados (no se importan entre sí)
- [ ] Domain sin dependencias externas (si Clean Architecture)
- [ ] DI manual para proyectos pequeños, tsyringe para grandes
- [ ] Monorepo con Turborepo para multi-app
- [ ] Event bus (EventEmitter local, BullMQ producción) para comunicación entre módulos
- [ ] Un archivo por responsabilidad
- [ ] Interfaces para dependencias externas (DB, APIs) — permiten testing y reemplazo
