# Core API

NestJS backend service providing RESTful APIs for authentication, user management, notifications, and file storage.

## Technology Stack

- **Framework**: NestJS with TypeScript
- **Database**: PostgreSQL with MikroORM
- **Cache/Queue**: Redis + BullMQ
- **Authentication**: Passport.js with JWT
- **File Storage**: AWS S3 SDK (RustFS for dev)

## Module Structure

Each feature follows this layout:

```
src/<feature>/
  <feature>.module.ts      NestJS module and DI wiring
  <feature>.controller.ts  HTTP request handlers
  <feature>.service.ts     business logic
  <feature>.entity.ts      MikroORM entity definition
  dtos/                    request/response validation DTOs
  # Optional sub-folders:
  providers/               custom providers
  strategies/              Passport strategies
  guards/                  auth/role guards
  channels/                notification delivery channels
```

### Core Modules

- **`auth/`**: OTP-based authentication, JWT token management, RBAC — [details](src/auth/README.md)
- **`user/`**: User registration, profile management, account verification
- **`notification/`**: Multi-channel notifications (SMS, Email, Push) — [details](src/notification/README.md)
- **`storage/`**: S3-compatible file storage with presigned URLs
- **`roles/`**: Role definitions and permission management
- **`sms/`**: SMS provider integration

### Shared Libraries (`src/libs/orm/`)

Always extend these — never reimplement:

| File | Purpose |
|---|---|
| `orm.entity.base.ts` | Base entity: `id`, `createdAt`, `updatedAt`, soft-delete |
| `orm.provider.base.ts` | DI providers for MikroORM entity managers |
| `orm.repository.service.base.ts` | Reusable CRUD and transaction helpers |
| `orm.service.migration.ts` | Migration generation and execution |
| `orm.types.factory.ts` | Shared DB/TypeScript type helpers |

## Adding a New Module

1. Create `src/<feature>/` with the standard files
2. Define the entity extending `BaseEntity`:

```typescript
import { BaseEntity } from '@/libs/orm/orm.entity.base';

@Entity()
export class Item extends BaseEntity {
  @Property()
  name: string;
}
```

3. Create DTOs with `class-validator` decorators
4. Implement service injecting `EntityManager` or extending the base repository service
5. Register the module in `src/app.module.ts`
6. Restart the dev server — `MigrationService` auto-generates and runs pending migrations on startup (non-prod only)

## File Naming Conventions

Pattern: `<feature>.<role>.ts`

```
user.service.ts
user.entity.ts
user.controller.ts
create-item.dto.ts
update-item.dto.ts
jwt-payload.interface.ts
notification-channel.type.ts
```

Test files: `<feature>.spec.ts` or `<feature>.test.ts`

## Error Handling

Use NestJS built-in exceptions for standard HTTP errors (`BadRequestException`, `UnauthorizedException`, etc.).

For domain-specific errors extend `HttpException`:

```typescript
import { HttpException, HttpStatus } from '@nestjs/common';

export class ItemNotFoundException extends HttpException {
  constructor(id: string) {
    super(`Item ${id} not found`, HttpStatus.NOT_FOUND);
  }
}
```

## Code Organization

- Each module is self-contained — import only from `src/libs/` or other modules' exported services
- Use DTOs for all request/response boundaries
- Use `JwtAuthGuard` for authentication, `RolesGuard` for authorization
- Use `@Public()` on endpoints that skip JWT auth
- Use `@CurrentUser()` to access the authenticated user in controllers

## Commands

```bash
pnpm --filter core-api start:dev  # dev server with watch mode
pnpm --filter core-api build      # compile to dist/
pnpm --filter core-api lint       # ESLint check
```

Tests are currently unstable — use `lint` + `build` as the verification loop.

## API

- **Base URL**: `http://localhost:4000/api/v1`
- **Authentication**: `Authorization: Bearer <jwt-token>`
- **Content-Type**: `application/json`
