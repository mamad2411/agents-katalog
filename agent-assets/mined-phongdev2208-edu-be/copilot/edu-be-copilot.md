# EduNet Backend — Copilot Instructions

## Architecture Overview

NestJS 11 + TypeORM 0.3 + PostgreSQL backend for an e-learning platform. All routes are prefixed with `/api` (set in `src/main.ts`). Auth middleware runs globally on every request to attach `req.user` from JWT; protected endpoints additionally use `@UseGuards(AuthGuard)`.

### Domain Modules

Each feature lives in `src/<domain>/` with: `*.module.ts`, `*.controller.ts`, `*.service.ts`, `dto/`, `entities/`. Key domains: `auth`, `user`, `course`, `enrollment`, `lesson`, `material`, `assignment`, `quiz`, `review`, `schedule`, `teacher`, `student`, `support-ticket`, `category`, `session`, `password-reset`.

### Core Module (`src/core/`)

Global shared infrastructure — **do not duplicate these, import from `src/core/`**:

- **`decorators/`** — Custom param decorators: `@PaginationParams()`, `@SortingParams()`, `@FilteringParams()`, `@IncludeRelations()`, `@CurrentUser()`. Use these on controller methods for list endpoints.
- **`helpers/index.ts`** — `getWhere()`, `getOrder()`, `getRelations()` translate decorator params into TypeORM `findAndCount` options. Also exports `HttpExceptionFilter`.
- **`responses/base.responses.ts`** — `SuccessResponse<T>` and `ErrorResponse` wrappers. Every service method must return `CommonResponse<T>`.
- **`guards/auth.guard.ts`** — Checks `req.user` exists (set by middleware). Use `@UseGuards(AuthGuard)`.
- **`middlewares/auth.middleware.ts`** — Decodes JWT from `Authorization: Bearer <token>` header, loads user, attaches to `req.user`.
- **`services/jwt.service.ts`** — Password hashing (bcrypt), JWT sign/verify (jsonwebtoken). Provided globally via `CoreModule`.
- **`pipes/backendValidation.pipe.ts`** — Custom validation pipe returning `{ errors: { field: string[] } }` format. Used in auth routes via `@UsePipes(new BackendValidationPipe())`.
- **`utils/index.ts`** — `omit()` and `pick()` object helpers.

## Key Patterns — Follow These Exactly

### Response Wrapping

All service methods return `Promise<CommonResponse<T>>`. Use `SuccessResponse` for success, `ErrorResponse` to throw (it throws `HttpException` internally):

```typescript
// Success
return new SuccessResponse(data, HttpStatus.CREATED);
// Error (throws immediately)
return new ErrorResponse('Not found', HttpStatus.NOT_FOUND);
```

### Entity Conventions

- Decorator: `@Entity({ name: 'PascalPluralName' })` (e.g., `'Courses'`, `'Users'`)
- Primary key: `@PrimaryGeneratedColumn('uuid')`
- Timestamps: `@CreateDateColumn`, `@UpdateDateColumn` with `type: 'timestamp with time zone'`
- Soft deletes: `@DeleteDateColumn({ type: 'timestamp with time zone', nullable: true }) deletedAt: Date | null`
- Enums: Define as TypeScript `enum` in the entity file, use `@Column({ type: 'enum', enum: EnumName })`
- Relations use explicit `@JoinColumn({ name: 'foreignKeyId' })` with a separate `@Column({ type: 'uuid' })` for the FK

### DTO Conventions

- Use `class-validator` decorators (`@IsNotEmpty`, `@IsOptional`, `@IsString`, `@IsUUID`, etc.)
- `UpdateDto` always extends `PartialType(CreateDto)` from `@nestjs/mapped-types`
- DTOs live in `src/<domain>/dto/` as `create-<domain>.dto.ts` and `update-<domain>.dto.ts`

### Service Pattern (CRUD)

```typescript
@Injectable()
export class FooService {
  constructor(
    @InjectRepository(Foo) private readonly fooRepository: Repository<Foo>,
  ) {}

  async findAll(
    pagination: Pagination, sorts: Sorting[] | null,
    filters: Filtering[] | null, includes: Including | null,
  ): Promise<CommonResponse<PaginationResponseInterface<Foo>>> {
    const where = filters ? getWhere(filters) : {};
    const order = sorts ? getOrder(sorts) : { createdAt: 'DESC' };
    const relations = includes ? getRelations(includes) : [];
    const [rows, count] = await this.fooRepository.findAndCount({
      where, order, relations, skip: pagination.offset, take: pagination.limit,
    });
    return new SuccessResponse({ rows, count });
  }
  // create: repository.create() -> .save() -> SuccessResponse(saved, CREATED)
  // update: findOne -> Object.assign(entity, dto) -> .save()
  // remove: findOne -> .softDelete(id)
}
```

### Controller Pattern

```typescript
@Controller('foos')
export class FooController {
  @Get()
  findAll(
    @PaginationParams() pagination: Pagination,
    @SortingParams() sorts: Sorting[] | null,
    @FilteringParams() filters: Filtering[] | null,
    @IncludeRelations() includes: Including | null,
  ) { ... }
}
```

Apply `@UseGuards(AuthGuard)` at class level for fully protected resources, or per-method for mixed access.

### Module Pattern

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([Entity])],
  controllers: [Controller],
  providers: [Service],
  exports: [Service],
})
```

Register new modules in `src/app.module.ts` imports array.

## Query String API

Clients use these query params (handled by custom decorators):

- **Pagination:** `?page=1&size=10` (default: page=1, size=10; `size=unlimited` returns all)
- **Sorting:** `?sort=field:asc&&field2:desc`
- **Filtering:** `?filter=field:rule:value&&field2:rule:value` — rules: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `like`, `nlike`, `in`, `nin`, `isnull`, `isnotnull`
- **Relations:** `?include=relation1|relation2`

## Database & Migrations

- **DBCODE:** Use DBCODE extension to connect to the `Edunet` database (`edunet_db`, PostgreSQL on `localhost:5433`). Always verify schema via DBCODE before creating migrations.
- **Config:** `src/core/database/main.ts` (shared), `data-source.ts` (migrations), `seed-data-source.ts` (seeds)
- **Migrations:** `src/migrations/` — run via `npm run migration:migrate`, revert via `npm run migration:revert`. Both schema changes AND seed data live here (seed file: `1704000000000-SeedCourseData.ts`).
- **Seeds (legacy):** `src/seeds/` still exists for backward compat with `npm run seed:migrate`, but prefer placing new seed migrations in `src/migrations/`.
- **Generate migration:** `npm run migration:generate:name` (runs `scripts/migration-gen.ts`)
- **Migration authoring policy:** Create migration files via CLI commands only (project scripts or TypeORM CLI). Do not hand-write or manually create migration files.
- **Current migrations:** `InitialSchema` → `SyncEntitiesWithSchema` → `AddLastLoginToUsers` → `SeedCourseData` (all applied)
- `synchronize: false` — always use migrations, never auto-sync

## Auth Flow

1. `POST /api/auth/register` or `POST /api/auth/login` → returns `{ accessToken, refreshToken, user }`
2. Client sends `Authorization: Bearer <accessToken>` on subsequent requests
3. `AuthMiddleware` (global) decodes token, loads user, sets `req.user`
4. `AuthGuard` (per-route) rejects if `req.user` is null
5. Refresh: `POST /api/auth/refresh` with `{ refreshToken }` → new accessToken
6. Sessions stored in DB (`Session` entity) with `revoked` and `expiredAt` fields

## Import Paths

Use `src/` prefix paths (resolved by TypeScript `baseUrl: "./"` in tsconfig):

```typescript
import { getWhere } from 'src/core/helpers';
import { SuccessResponse } from 'src/core/responses/base.responses';
```

## Dev Commands

| Command | Purpose |
|---|---|
| `npm run start:dev` | Dev server with watch mode |
| `npm run migration:migrate` | Run pending migrations |
| `npm run migration:revert` | Revert last migration |
| `npm run seed:migrate` | Run seed data |
| `npm run build` | Production build |
| `npm run lint` | ESLint with auto-fix |
| `npm run format` | Prettier formatting |
