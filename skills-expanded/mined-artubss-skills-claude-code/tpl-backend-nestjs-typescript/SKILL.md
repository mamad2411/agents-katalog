---
name: tpl-backend-nestjs-typescript
description: Template do pack (backend/07-nestjs-typescript.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/07-nestjs-typescript.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: NestJS REST API

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/07-nestjs-typescript.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK

| Technology | Version | Purpose |
|------------|---------|---------|
| Node.js | 22.x | Runtime |
| TypeScript | 5.4+ | Language |
| NestJS | 10.x | Framework |
| PostgreSQL | 16 | Primary database |
| Prisma | 5.x | ORM + migrations |
| Passport | 0.7+ | Auth strategies |
| passport-jwt | 4.x | JWT strategy |
| @nestjs/jwt | 10.x | JWT module |
| class-validator | 0.14+ | DTO validation |
| class-transformer | 0.5+ | Request transformation |
| Jest | 29.x | Unit tests |
| Supertest | 7.x | e2e tests |
| @nestjs/testing | 10.x | Test module utilities |

---

## PROJECT STRUCTURE

```
src/
├── app.module.ts           # Root module — imports feature modules
├── main.ts                 # Bootstrap: create app, pipes, guards, listen
├── modules/
│   ├── auth/
│   │   ├── auth.module.ts
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── strategies/
│   │   │   ├── jwt.strategy.ts
│   │   │   └── jwt-refresh.strategy.ts
│   │   ├── guards/
│   │   │   ├── jwt-auth.guard.ts
│   │   │   └── roles.guard.ts
│   │   └── decorators/
│   │       ├── current-user.decorator.ts
│   │       └── roles.decorator.ts
│   └── users/
│       ├── users.module.ts
│       ├── users.controller.ts
│       ├── users.service.ts
│       ├── users.repository.ts  # Wraps Prisma for users domain
│       ├── dto/
│       │   ├── create-user.dto.ts
│       │   ├── update-user.dto.ts
│       │   └── user-response.dto.ts
│       └── interceptors/
│           └── user-transform.interceptor.ts
├── common/
│   ├── decorators/
│   ├── filters/
│   │   └── http-exception.filter.ts
│   ├── interceptors/
│   │   └── transform.interceptor.ts   # Wraps responses in { data, meta } envelope
│   └── pipes/
│       └── parse-uuid.pipe.ts
├── database/
│   └── prisma.service.ts    # Injectable Prisma client
└── config/
    └── configuration.ts     # Typed config with @nestjs/config
test/
├── app.e2e-spec.ts
└── jest-e2e.json
```

---

## ARCHITECTURE RULES

- **Controller → Service → Repository (→ Prisma)** — never skip
- Controllers: only receive request, call service, return response — no business logic
- Services: business logic only — no HTTP types, no direct Prisma import
- Repositories: Prisma wrapper for domain — no business logic, no validators
- Every module imports only what it needs — avoid importing `AppModule` in tests
- Global pipes, guards, filters, and interceptors registered in `main.ts` (not per-controller)
- DTOs are interfaces for validation only — business objects are separate
- `class-transformer` `plainToInstance` used in interceptors to strip sensitive fields

---

## NESTJS MODULE STRUCTURE

### When to Create a New Module

Create a new module when the domain:
1. Has its own database entity (table/model)
2. Has at least one controller endpoint
3. Has business logic that doesn't belong to an existing module

**Do NOT** create a module for:
- Simple utility functions → put in `common/`
- Config providers → use `@nestjs/config`
- Database access only → add to existing module's repository

### Module Template

```typescript
// src/modules/posts/posts.module.ts
import { Module } from '@nestjs/common'
import { PostsController } from './posts.controller'
import { PostsService } from './posts.service'
import { PostsRepository } from './posts.repository'
import { DatabaseModule } from '../../database/database.module'

@Module({
  imports: [DatabaseModule],   // Only import what this module needs
  controllers: [PostsController],
  providers: [PostsService, PostsRepository],
  exports: [PostsService],     // Only export if other modules need this service
})
export class PostsModule {}
```

---

## DECORATOR RULES

### Guards

Guards run BEFORE interceptors and pipes. Use `@UseGuards` on controller or route level; global guards registered in `main.ts`.

```typescript
// src/modules/auth/guards/jwt-auth.guard.ts
import { Injectable, ExecutionContext, UnauthorizedException } from '@nestjs/common'
import { AuthGuard } from '@nestjs/passport'
import { Reflector } from '@nestjs/core'
import { IS_PUBLIC_KEY } from '../decorators/public.decorator'

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super()
  }

  canActivate(context: ExecutionContext) {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ])
    if (isPublic) return true
    return super.canActivate(context)
  }
}

// src/modules/auth/guards/roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ])
    if (!requiredRoles?.length) return true
    const { user } = context.switchToHttp().getRequest()
    return requiredRoles.includes(user.role)
  }
}
```

### Custom Decorators

```typescript
// src/modules/auth/decorators/current-user.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common'

export const CurrentUser = createParamDecorator(
  (_data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest()
    return request.user  // injected by JwtStrategy.validate()
  },
)

// src/modules/auth/decorators/roles.decorator.ts
import { SetMetadata } from '@nestjs/common'
export const Roles = (...roles: string[]) => SetMetadata('roles', roles)

// src/common/decorators/public.decorator.ts
import { SetMetadata } from '@nestjs/common'
export const IS_PUBLIC_KEY = 'isPublic'
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true)
```

### Usage in Controller

```typescript
// src/modules/users/users.controller.ts
import { Controller, Get, Patch, Body, HttpCode } from '@nestjs/common'
import { CurrentUser } from '../auth/decorators/current-user.decorator'
import { Roles } from '../auth/decorators/roles.decorator'
import { UpdateUserDto } from './dto/update-user.dto'
import { UsersService } from './users.service'

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get('me')
  getMe(@CurrentUser() user: AuthUser) {
    return this.usersService.findById(user.id)
  }

  @Patch('me')
  @HttpCode(200)
  updateMe(@CurrentUser() user: AuthUser, @Body() dto: UpdateUserDto) {
    return this.usersService.update(user.id, dto)
  }

  @Get()
  @Roles('admin')
  findAll() {
    return this.usersService.findAll()
  }
}
```

### DTOs with class-validator

```typescript
// src/modules/users/dto/create-user.dto.ts
import { IsEmail, IsString, MinLength, IsEnum, IsOptional } from 'class-validator'
import { Transform } from 'class-transformer'

export class CreateUserDto {
  @IsEmail({}, { message: 'Invalid email format' })
  @Transform(({ value }) => value?.toLowerCase().trim())
  email: string

  @IsString()
  @MinLength(2, { message: 'Name must be at least 2 characters' })
  name: string

  @IsString()
  @MinLength(8, { message: 'Password must be at least 8 characters' })
  password: string

  @IsEnum(['admin', 'user'], { message: 'role must be admin or user' })
  @IsOptional()
  role?: 'admin' | 'user' = 'user'
}
```

### Response Transform Interceptor

```typescript
// src/common/interceptors/transform.interceptor.ts
import { CallHandler, ExecutionContext, Injectable, NestInterceptor } from '@nestjs/common'
import { map, Observable } from 'rxjs'
import { plainToInstance } from 'class-transformer'

export interface Response<T> {
  data: T
  timestamp: string
}

@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, Response<T>> {
  intercept(_context: ExecutionContext, next: CallHandler<T>): Observable<Response<T>> {
    return next.handle().pipe(
      map(data => ({
        data,
        timestamp: new Date().toISOString(),
      })),
    )
  }
}
```

---

## GLOBAL SETUP IN MAIN.TS

```typescript
// src/main.ts
import { NestFactory, Reflector } from '@nestjs/core'
import { ValidationPipe, ClassSerializerInterceptor } from '@nestjs/common'
import { AppModule } from './app.module'
import { JwtAuthGuard } from './modules/auth/guards/jwt-auth.guard'
import { RolesGuard } from './modules/auth/guards/roles.guard'
import { TransformInterceptor } from './common/interceptors/transform.interceptor'
import { HttpExceptionFilter } from './common/filters/http-exception.filter'

async function bootstrap() {
  const app = await NestFactory.create(AppModule)
  const reflector = app.get(Reflector)

  app.setGlobalPrefix('api/v1')
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }))
  app.useGlobalGuards(new JwtAuthGuard(reflector), new RolesGuard(reflector))
  app.useGlobalInterceptors(new ClassSerializerInterceptor(reflector), new TransformInterceptor())
  app.useGlobalFilters(new HttpExceptionFilter())

  await app.listen(process.env.PORT ?? 3000)
}
bootstrap()
```

---

## ROUTING TABLE

| Trigger | Method | Route | Auth | Controller Action |
|---------|--------|-------|------|------------------|
| Register | POST | `/api/v1/auth/register` | Public | AuthController.register |
| Login | POST | `/api/v1/auth/login` | Public | AuthController.login |
| Refresh token | POST | `/api/v1/auth/refresh` | Refresh JWT | AuthController.refresh |
| Get own profile | GET | `/api/v1/users/me` | JWT | UsersController.getMe |
| Update profile | PATCH | `/api/v1/users/me` | JWT | UsersController.updateMe |
| Change password | POST | `/api/v1/users/me/password` | JWT | UsersController.changePassword |
| List all users | GET | `/api/v1/users` | JWT + admin role | UsersController.findAll |
| Get user by ID | GET | `/api/v1/users/:id` | JWT + admin role | UsersController.findOne |
| Delete user | DELETE | `/api/v1/users/:id` | JWT + admin role | UsersController.remove |

---

## QUALITY GATES

Before opening a PR, verify ALL of the following:

- [ ] `npx tsc --noEmit` passes — zero type errors
- [ ] `jest --passWithNoTests` passes — unit and e2e
- [ ] `ValidationPipe({ whitelist: true })` active — unknown properties stripped
- [ ] All new DTOs use `class-validator` decorators — no manual validation in controllers
- [ ] Response DTOs use `@Exclude()` on sensitive fields (`password`, `hashedToken`)
- [ ] Guards cover all endpoints — `@Public()` explicitly applied where auth is optional
- [ ] No direct Prisma usage in controllers or services — goes through repository
- [ ] Module only exports what other modules actually consume
- [ ] No circular imports between modules — use `forwardRef()` only as last resort
- [ ] `nest build` passes without errors

---

## FORBIDDEN

- **NEVER** use `@Injectable()` without including the class in a module's `providers` array
- **NEVER** import `PrismaService` directly into controllers — use repositories
- **NEVER** use `req.body` directly in controllers — always use typed DTOs
- **NEVER** bypass `ValidationPipe` by omitting `@Body()` decorator
- **NEVER** use `forwardRef()` as a first solution — redesign the dependency instead
- **NEVER** use `@Global()` module decorator except for `DatabaseModule` and `ConfigModule`
- **NEVER** throw raw `Error` — always throw `HttpException` subclasses (`NotFoundException`, etc.)
- **NEVER** put business logic in guards — guards only answer "can this pass?" (boolean)
- **NEVER** put auth logic in services — use guards and strategies (Passport)
- **NEVER** expose the Prisma model type directly in API responses — use response DTOs
