---
name: nestjs-starter
description: >
  Scaffolds a complete NestJS project from scratch following AlgoAce production 
  architecture, then generates domain modules with full CRUD. Generates: auth 
  guards (Cognito JWT + roles + environment + super-admin), global exception 
  filter with error codes/registry, Zod validation pipe, custom decorators 
  (@Public, @Roles, @Environment, @SuperAdmin, @User), Pino logger with 
  AsyncLocalStorage request context, OpenTelemetry instrumentation, Prometheus 
  metrics, request middleware, logging/metrics interceptors, Prisma ORM with 
  PostgreSQL, SQS notification pipeline (producer + consumer with OnModuleInit 
  Firebase + error handlers), S3 pre-signed uploads, Docker setup (local 
  PostgreSQL + production multi-container with CloudWatch + Grafana Alloy), 
  GitHub Actions CI/CD, env validation, seed scripts, utility services, and 
  domain modules with controllers, services, Zod DTOs, tenant scoping, AppLogs 
  audit trail, and optional FCM notifications. Use when creating a new NestJS 
  app, starting a new project, bootstrapping a backend, scaffolding a new API, 
  or when the user says "create a X app", "build me a new NestJS project", 
  "scaffold a backend for X", "start a new app", or describes any new 
  application that needs a NestJS backend with domain modules.
---

# NestJS Project Scaffolder — AlgoAce Production Architecture

You are scaffolding a brand new NestJS project using the AlgoAce production
architecture. The generated project is a **starter** — the infrastructure is
identical across all projects, only the domain logic and database schema change.

## Before You Start: Interview the User

Ask these questions in order before generating anything:

1. **What is the app?** (e.g., "therapy platform", "blog", "restaurant management")
2. **Is this a multi-tenant app?** (Does one admin own data that other users belong to?)
   - YES → add `adminId` FK on entities, tenant-scope all queries
   - NO → skip tenant scoping, but still create Users table with ADMIN role for future use
3. **What are the main domain entities?** (e.g., "posts, categories, comments")
4. **What user roles does the app need besides ADMIN?**
   ADMIN is always present. Common patterns:
   - Two roles: ADMIN + USER
   - Three roles: ADMIN + MANAGER + USER
   - Optional: SUPER_ADMIN for platform-level operations
5. **Does it need push notifications?** If yes → SQS + FCM. If no → skip.
6. **Does it need file uploads?** If yes → S3. If no → skip.
7. **Does it need scheduled jobs?** If yes → @nestjs/schedule + cron leader. If no → skip.
8. **Does it need CI/CD pipeline?** If yes → GitHub Actions + list required secrets. If no → skip.
9. **Does it need an admin panel module?** If yes → stats, reports, user management. If no → skip.
10. **Auth provider?** (default: AWS Cognito)
11. **Project name?** (kebab-case)

After the user answers, confirm before generating:
```
I'll set up:
✅ Multi-tenant (adminId scoping on all entities)
✅ ADMIN + THERAPIST + PATIENT roles
✅ Push notifications (SQS + FCM)
❌ File uploads (skipped)
❌ Scheduled jobs (skipped)
❌ CI/CD pipeline (skipped — can add later)
✅ Admin panel module

Proceed?
```

## Multi-Tenancy (conditional)

### If user said YES to multi-tenant:

Every entity gets an `adminId` FK. Every service method starts with:
```ts
const adminId = currentUser.userType === "ADMIN"
  ? currentUser.id
  : (currentUser.adminId as string);
```
Every query filters by `adminId`. Non-negotiable in multi-tenant mode.

### If user said NO to multi-tenant:

- Still create Users table with ADMIN role (useful for app management later)
- Do NOT add `adminId` FK on domain entities
- Services use simple `currentUser.id` for ownership
- No adminId derivation needed

## Generation Order

### Phase 1: Project Foundation

1. Initialize NestJS project
2. Install all dependencies — read `@references/dependencies.md`
3. Create folder structure — read `@references/folder-structure.md`
4. Create config files — read `@references/config-files.md`

### Phase 2: Core Infrastructure (order matters)

5. **Config constants** — `src/config/index.ts`
   Keys: IS_PUBLIC_KEY, ROLES_KEY, ENVIRONMENT_KEY, IS_SUPER_ADMIN_KEY, SQS_QUEUES

6. **Type definitions** — `src/types/index.ts` + `src/types/express.d.ts`
   SqsNotificationPayload (with recipientUserId), AppEnv, Express request extension

7. **Environment validation** — read `@references/env-config.md`

8. **AsyncLocalStorage** — `src/localStorage/request-storage.ts`
   Read `@references/observability.md`

9. **Prisma setup** — module, service, base schema (with Users, FcmTokens, Notifications, AppLogs)
   Read `@references/prisma-setup.md`
   Users model ALWAYS includes: timezone, fcmTokens (with deviceId), accountStatus, isNotificationSeen

10. **Logger** — Pino with ALS context (requestId, userId, ip on every log line)
    Read `@references/observability.md`

11. **OpenTelemetry instrumentation** — MUST be FIRST import in main.ts/worker.ts
    Read `@references/observability.md`

12. **Custom decorators** — @Public, @Roles, @Environment, @SuperAdmin, @User
    Read `@references/auth-system.md`

13. **Guards** — auth (writes userId to ALS store), roles, env, throttler
    Read `@references/auth-system.md`

14. **Exception filter + error codes + registry**
    Read `@references/error-system.md`

15. **Zod validation pipe**
    Read `@references/infrastructure.md`

16. **Middleware** — wraps next() in ALS requestContextStorage.run(), uses crypto.randomUUID()
    Read `@references/observability.md`

17. **Interceptors** — logging + metrics
    Read `@references/observability.md`

18. **Utility service** — Cognito JWT verifier, date helpers
    Read `@references/infrastructure.md`

### Phase 3: Service Infrastructure (conditional)

19. **SQS notification pipeline** — ONLY if notifications selected
    Consumer uses OnModuleInit for Firebase, has SqsConsumerEventHandler for errors,
    re-throws on failure, stores adminId on Notification rows
    Read `@references/notification-patterns.md`

20. **S3 storage service** — ONLY if file uploads selected
    Read `@references/infrastructure.md`

21. **Prometheus metrics** — always include
    Read `@references/observability.md`

### Phase 4: Entry Points

22. **main.ts** — read `@references/bootstrap.md`
    Uses ConfigService.get("PORT"), registers middleware via app.use(),
    CORS with allowedHeaders (Content-Type, Authorization, Accept-Encoding, X-Request-Id)

23. **worker.ts** — read `@references/bootstrap.md`

24. **app.module.ts** — guard order: Throttler → EnvGuard → AuthGuard → RolesGuard
    Read `@references/bootstrap.md`

25. **worker.module.ts** — includes PrometheusModule + MetricsController
    Read `@references/bootstrap.md`

26. **app.controller.ts** — health-check + health-check-db + dev-only endpoints:
    - GET /health-check — @Public, returns { status: "ok" }
    - GET /health-check-db — @Public, runs SELECT 1 against DB
    - DELETE /empty-database — @Environment("development") @Public
    - DELETE /empty-cognito — @Environment("development") @Public

### Phase 5: Domain Modules

For EACH domain module, read `@references/module-patterns.md`:
27. Prisma model (read `@references/prisma-setup.md`)
28. Error codes + registry entries
29. DTOs — Zod schemas
30. Service — tenant-scoped CRUD + AppLogs + comments on every line
31. Controller — thin, decorated
32. Module + wire into app.module.ts
33. Notification consumer handler if applicable (read `@references/notification-patterns.md`)

### Phase 6: DevOps & Tooling

34. **Docker setup** — read `@references/docker-cicd.md`
    - Dockerfile (multi-stage)
    - compose.local.yml (PostgreSQL with pg_isready healthcheck)
    - compose.yml (backend + worker + grafana-alloy, awslogs driver on both services)
    - .dockerignore (MUST create — security risk without it)

35. **Grafana Alloy** — read `@references/config-alloy.md`
    - config.alloy at project root (compose.yml references it, deploy FAILS without it)

36. **CI/CD** — ONLY if user selected. Read `@references/docker-cicd.md`
    Generate ci.yml + deploy.yml, then list ALL GitHub secrets user must configure.
    If skipped, tell user: "CI/CD skipped. You can add it later."

37. **.env.example** + **.env.local** — read `@references/env-config.md`
    Generate BOTH: .env.example (template) AND .env.local (pre-filled with local defaults)

38. **Seed script** — `src/prisma/seed.ts`
    Comprehensive seed data across ALL tables:
    - If multi-tenant: 2 tenants (ADMINs) to test isolation
    - 3+ users per role per tenant
    - Domain entities with realistic data in all tables
    - Enough data to test pagination, filtering, dashboard queries

39. **Config files** — read `@references/config-files.md`
    .prettierrc, tsconfig.json, eslint.config.mjs — match AlgoAce standards

40. README.md + AGENTS.md

### Phase 7: Verify

```bash
npx prisma validate && npx prisma generate && npm run lint && npm run build
```

## Users Model — Always Includes These Fields

Regardless of the domain, every Users model has:

```prisma
model Users {
  id                 String        @id @default(uuid()) @db.Uuid
  cognitoId          String        @unique
  email              String        @unique
  firstName          String
  lastName           String
  userType           UserType      @default(USER)
  accountStatus      AccountStatus @default(ACTIVE)
  timezone           String?       // User's timezone (e.g., "Asia/Karachi")
  
  // Multi-tenant FK (null for ADMIN, set for subordinates)
  adminId            String?       @db.Uuid
  admin              Users?        @relation("TenantUsers", fields: [adminId], references: [id], onDelete: Cascade)
  tenantUsers        Users[]       @relation("TenantUsers")
  
  // Notification state
  isNotificationSeen Boolean       @default(true)
  
  // FCM tokens — one per device, includes deviceId for management
  fcmTokens          FcmTokens[]
  
  createdAt          DateTime      @default(now())
  updatedAt          DateTime      @updatedAt

  // Back-relations added per domain module
  @@index([adminId])
}

model FcmTokens {
  id       String @id @default(uuid()) @db.Uuid
  token    String
  deviceId String // Identifies the physical device
  userId   String @db.Uuid
  user     Users  @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  @@unique([userId, deviceId]) // One token per device per user
}
```

FCM token management endpoints (always generate in Users module):
- PATCH /users/fcm/:userId — update/remove FCM token by deviceId
  - Body: { fcmToken?, deviceId, isFcmUpdate: boolean }
  - If isFcmUpdate=true: remove old token for deviceId, add new one
  - If isFcmUpdate=false: just remove token for deviceId (logout)

## What Is Always Included (every project)

- Guards (auth, roles, env, throttler) + guard registration order
- Exception filter + error handling shape + Prisma error map
- Zod validation pipe + all decorators
- AsyncLocalStorage for request context (requestId, userId, ip)
- Logger with ALS context + fatal/verbose methods
- OpenTelemetry instrumentation + Prometheus metrics (API + worker)
- PreRequest middleware with ALS run() + crypto.randomUUID()
- Logging/Metrics interceptors
- Bootstrap sequence (main.ts, worker.ts)
- Prisma module/service
- Docker setup (Dockerfile, compose.local with healthcheck, compose.yml with awslogs)
- .dockerignore
- config.alloy (Grafana Alloy — compose.yml references it)
- .env.example + .env.local
- Config files (.prettierrc, tsconfig.json, eslint.config.mjs)
- Health-check + health-check-db + dev-only empty endpoints
- Users model with timezone, fcmTokens, accountStatus
- AppLogs audit trail pattern
- Comprehensive seed data
- Comments on every function and logic line

## What Is Optional (ask the user)

- SQS + FCM notification pipeline
- S3 pre-signed uploads
- Scheduled jobs (@nestjs/schedule + cron leader)
- CI/CD (GitHub Actions → ECR → EC2)
- SUPER_ADMIN role
- Admin panel module
- Multi-tenant scoping

## Rules

- **Never use `class-validator`** — always Zod
- **Never use `any` type** — TypeScript strict
- **Never put business logic in controllers** — controllers are thin
- **Never skip tenant scoping** — if multi-tenant, every query filters by `adminId`
- **Never throw `new Error(...)`** in request paths — use `ErrorCodes.*`
- **Imports**: `src/...` absolute for cross-module, relative for siblings
- **Dates**: Luxon `DateTime` for timezone/calendar math
- **Always write AppLogs** for create/update/delete
- **Guard order**: Throttler → EnvGuard → AuthGuard → RolesGuard
- **instrumentation.ts** must be FIRST import in main.ts and worker.ts
- **Cron jobs** only run when `IS_CRON_LEADER=true`
- **No source code on EC2** — only Docker images from ECR
- **Comment ALL files, not just TypeScript** — Dockerfile (every stage, every RUN/COPY), compose.yml (every service, every directive), compose.local.yml, .dockerignore, config.alloy, main.ts, worker.ts, guards, middleware, interceptors, pipes, decorators, logger, prisma files, config files, types, utils, SQS modules. Every file a developer would open must be self-explanatory to a non-developer.
- **Use crypto.randomUUID()** — not uuid package
- **No single-character variable names** — `u` → `cognitoUser`, `e` → `error`, `t` → `token`, `r` → `response`. Exception: array callbacks where context is obvious (.map((item) => ...)).
- **process.env allowed in 2 files ONLY** — `instrumentation.ts` and `logger/index.logger.ts` (both run before ConfigModule loads). Each must have a comment explaining why. Everything else uses ConfigService.
- **ConfigService.get()** for all env vars — never process.env in app code (except the 2 files above)
- **Store deviceId with FCM tokens** — for per-device token management
- **Store timezone on Users** — for timezone-aware operations