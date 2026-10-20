---
description: NestJS, Prisma, Redis, and BullMQ backend implementation standards
globs:
  - "apps/api/**"
  - "prisma/**"
alwaysApply: false
---

# Backend

## Purpose

Standardise NestJS API implementation: configuration, persistence, queues, validation, and service-layer logic. Layer boundaries are owned by `architecture.mdc`; HTTP contract shape by `api-design.mdc`.

## Required patterns

### Bootstrap (`main.ts`)

- Global prefix: `api` (routes are written without it: `@Controller('health')` → `/api/health`).
- Global `ValidationPipe`: `whitelist: true`, `forbidNonWhitelisted: true`, `transform: true`.
- CORS from typed config (`corsOrigin`).
- Listen on `host` + `port` from config.

### Configuration & env

- All env access goes through `@nestjs/config` with:
  - `configuration.ts` — typed `AppConfig` factory.
  - `env.validation.ts` — `class-validator` schema; fail fast on boot.
- Inject via `ConfigService<AppConfig, true>` with `{ infer: true }` on `get()`.
- New env var registration is a multi-surface change — see `infra.mdc` for the full checklist.

### Feature module anatomy

```
features/<name>/
  <name>.module.ts
  <name>.controller.ts
  <name>.service.ts
  dto/                    # request/response DTOs (class-validator)
  <name>.service.spec.ts  # service unit tests (testing.mdc)
```

- **Controller**: HTTP mapping only. Return types are `@monolith/types` or DTOs.
- **Service**: business logic, Prisma calls, queue enqueueing. Constructor injection only.
- **DTO**: `class-validator` + `class-transformer`. Never trust raw `req.body`.
- Register the module in `app.module.ts`.

### Prisma

- Use `PrismaService` from `infrastructure/database/`. Do not instantiate `PrismaClient` elsewhere.
- Migrations via `pnpm db:migrate`; never hand-edit applied migration SQL without team review.
- `directUrl` for migrations (Supabase pooler pattern); runtime uses `DATABASE_URL`.
- Prefer explicit `select` / `include` over fetching whole models when exposing API data.
- Multi-step writes that must commit-or-roll-back together: `prisma.$transaction`.

### Redis & BullMQ

- Connection from `redisUrl` and `bullmqPrefix` in `AppConfig`.
- Queue names live in `infrastructure/queue/queue.constants.ts` (`QUEUE_NAMES`).
- Processors are `@Processor(QUEUE_NAMES.x)` classes colocated with the owning feature.
- Jobs must be idempotent — retries are expected.

### Errors

- Throw Nest HTTP exceptions (`NotFoundException`, `BadRequestException`, …) from services/controllers.
- Response shape and what not to leak: `api-design.mdc` + `security.mdc`.

## Forbidden patterns

- `process.env` reads outside `config/`.
- Prisma client instantiated outside `PrismaService`.
- Business logic in controllers or DTO classes.
- Skipping DTO validation "for internal endpoints".
- Synchronous blocking on work that should be queued (emails, webhooks, heavy transforms).
- Empty `catch` blocks or swallowed errors.

## Implementation expectations

- Order for new endpoints: DTO → service method → controller route → type in `@monolith/types` if consumed by web/mobile.
- Health checks follow `features/health/` — extend for DB/Redis readiness when required.
- Run `pnpm --filter @monolith/api test` after service changes.

## Examples

**Good — service with Prisma**

```typescript
@Injectable()
export class OrdersService {
  constructor(private readonly prisma: PrismaService) {}

  async findById(id: string): Promise<OrderSummary | null> {
    return this.prisma.order.findUnique({
      where: { id },
      select: { id: true, status: true },
    });
  }
}
```

**Good — enqueue job**

```typescript
await this.ordersQueue.add('send-confirmation', { orderId }, { attempts: 3 });
```

**Bad — env in service**

```typescript
const url = process.env.DATABASE_URL; // use ConfigService
```
