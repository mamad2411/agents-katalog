---
name: nestjs-fastify
description: >
  NestJS 11 (CommonJS + Jest) and NestJS 12 (ESM + Vitest) with Fastify 5 — setup patterns
  for pnpm monorepos.
  Invoke automatically when configuring NestJS with Fastify, setting up tsconfig paths,
  adding @types/express, configuring Fastify plugins, handling PATCH endpoints,
  POST requests with empty body, or running compiled builds.
---

# NestJS 11/12 + Fastify 5 — Setup Patterns for pnpm Monorepos

## Check the project's NestJS major first

NestJS 12 is **ESM-only** (every `@nestjs/*` package ships `"type": "module"`). That is about the
*packages*: a **new** NestJS 12 app follows the ESM shape below, but an **existing** CommonJS app
can move to 12 and stay CommonJS + Jest — Node loads the ESM packages through `require(esm)`
(§ "Migrating an existing NestJS 11 app to 12 — keep CommonJS + Jest"). Never mix module formats
inside one app.

| | NestJS 11 | NestJS 12 |
|---|---|---|
| Module format | CommonJS | ESM (`"type": "module"` in the app's `package.json`) |
| tsconfig | `module: CommonJS` (sections below) | `module`/`moduleResolution: nodenext` (§ "NestJS 12 — ESM setup") |
| Relative imports | `./foo` | `./foo.js` (required by `nodenext`) |
| Test runner | Jest + ts-jest | Vitest (official `nestjs/typescript-starter`) — see `test-patterns` |
| TypeScript | 5.x / 6.0 | 6.0 — **not 7** (TS 7 ships no JS compiler API; typescript-eslint, ts-jest and `@nestjs/swagger` need ≤ 6) |

Unless a section says otherwise, the rest of this skill applies to both majors. A new project
should start on the current major (12); existing NestJS 11 projects migrate deliberately, not
piecemeal.

## Migrating an existing NestJS 11 app to 12 — keep CommonJS + Jest

Verified in a production pnpm monorepo (Fastify 5). The official migration guide
makes the ESM switch optional; staying CommonJS keeps the diff to dependencies and test config —
**no application code changed**. One PR per step, validated on staging in between:

1. **Node ≥ 24.9 everywhere** (CI, Dockerfile, `engines`, `.nvmrc`). Jest can `require()` ESM only
   from Node 24.9; older Node fails with `ERR_REQUIRE_ASYNC_MODULE`/`ERR_REQUIRE_ESM`.
2. **Jest 29 → 30** (ts-jest `^29.4.14` supports it), still on NestJS 11. In a monorepo, pin
   `jest`/`jest-environment-node` explicitly in apps that stay on 29 (e.g. Expo + Detox) — they had
   been resolving their `jest` peer to whatever the workspace held and silently jump to 30.
3. **Coupled libraries first.** `@sentry/nestjs` 10 doesn't accept Nest 12; v11 does (and accepts 11),
   but v11 replaced `sendDefaultPii` with `dataCollection`, and **leaving it unset collects request
   bodies, cookies, user info, DB query data and GenAI I/O by default** — set every category
   explicitly. Check every `@nestjs/*`-coupled dependency's peer range the same way.
4. **NestJS 12**: `@nestjs/common`/`core`/`platform-fastify`/`testing` `^12`, `@nestjs/swagger` `^12`,
   `@nestjs/schedule` `^12` (renumbered from 6.x), `@nestjs/cli` `^12`, `@nestjs/throttler` `^6.7.1`
   (first 6.x declaring 12). TypeScript can stay 5.x (`@nestjs/swagger` 12 accepts `^5.5 || ^6`).

Two test-runner settings are mandatory on step 4 — both found the hard way:

```jsonc
// apps/api/package.json
"scripts": {
  // Without it every suite fails with "Must use import to load ES Module: …/@nestjs/common/index.js",
  // even on Node 24.9+ — Jest only loads ESM through Node's VM-modules loader.
  "test": "NODE_OPTIONS=--experimental-vm-modules jest --passWithNoTests"
},
"jest": {
  // A 2-vCPU CI runner gives Jest cores-1 = 1 worker, i.e. every file in ONE process; with ESM
  // loaded through VM modules, memory accumulates across files until "JavaScript heap out of
  // memory" (~2 GB). Locally (many cores) it never shows. Reproduce with `jest -i` +
  // `--max-old-space-size=2048`. Two workers recycled at 1 GB fix it at the same speed.
  "maxWorkers": 2,
  "workerIdleMemoryLimit": "1GB"
}
```

Stryker runs Jest in its own processes: add `"testRunnerNodeArgs": ["--experimental-vm-modules"]`
to `stryker.conf.json` (verify with `stryker run --dryRunOnly`). Apply the same flag to every
extra Jest config script (`jest --config …`).

Prove "no behavior change" instead of assuming it: before upgrading, record status + body for the
error paths the reworked adapter error mapping could touch (404, wrong method, 401, malformed
JSON, validation, extra property, wrong content-type, 413, wrong credentials) and the OpenAPI JSON;
diff both after the upgrade, locally and again on staging.

## NestJS 12 — ESM setup

Mirrors the official `nestjs/typescript-starter` (verified 2026-10 in a pnpm monorepo, with
`tsc` builds instead of `nest build`).

```json
// apps/api/package.json (excerpt)
{
  "type": "module",
  "scripts": {
    "build": "tsc -p tsconfig.build.json",
    "start": "node dist/main.js",
    "type-check": "tsc --noEmit",
    "test": "vitest run"
  },
  "dependencies": {
    "@nestjs/common": "^12.1.2",
    "@nestjs/core": "^12.1.2",
    "@nestjs/platform-fastify": "^12.1.2",
    "@nestjs/swagger": "^12.0.2",
    "@fastify/static": "^10.1.5"
  }
}
```

```json
// apps/api/tsconfig.json
{
  "compilerOptions": {
    "target": "ES2023",
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "isolatedModules": true,
    "rootDir": "./src",
    "outDir": "./dist",
    "strict": true,
    "strictPropertyInitialization": false,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "types": ["node"]
  },
  "include": ["src/**/*"]
}
```

- **`.js` on every relative import** (`import { AppModule } from './app.module.js'`) — `nodenext`
  rejects extensionless ESM imports at compile time.
- **Workspace packages consumed by the API must be ESM too** (`"type": "module"`, `exports`
  with `"import"`) — see `shared-kernel`.
- **`main.ts` template is unchanged** (`import 'dotenv/config'` first, then `reflect-metadata`).
- **Decorator metadata under Vitest works without SWC** (Vitest 4+/5 transformer emits it).
  Keep one DI test that injects a class dependency without `@Inject()` as a guard — see
  `test-patterns` § Vitest.
- `@nestjs/core` 12 does not export `package.json` — `require('@nestjs/core/package.json')`
  throws; read versions from the lockfile instead.

## tsconfig — do not define `paths` for workspace packages

Pointing `paths` from `@myapp/*` to `.ts` source files corrupts the `rootDir` inferred by
TypeScript and generates TS6059 errors (`File is not under 'rootDir'`).

**Rule:** Never define `paths` in the API's `tsconfig.json` for workspace packages.
Let pnpm workspace resolve them via the compiled `dist/` output.

**Required tsconfig.json for NestJS API in pnpm monorepo:**

```json
{
  "compilerOptions": {
    "module": "CommonJS",
    "moduleResolution": "node",
    "ignoreDeprecations": "5.0",
    "target": "ES2022",
    "outDir": "./dist",
    "strict": true,
    "strictPropertyInitialization": false,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts"]
}
```

**Critical:**
- **DO NOT define `paths`** — causes conflict with rootDir/outDir and TS6059
- **`rootDir` depends on the TypeScript major:** on TS 5.x leave it out (inferred via
  `include`); **on TS 6+ it is required** whenever `outDir` is set — without it the build fails
  with TS5011 (`The 'rootDir' setting must be explicitly set`). Set `"rootDir": "./src"`. The old
  "never set rootDir" advice only existed because of `paths` (above), which you still must not use.
- **TS 6+: `types` defaults to `[]`** — `@types/*` are no longer auto-included; list them
  (`"types": ["node"]`, plus the test runner's types where needed).
- **`strictPropertyInitialization: false`** — DTOs with class-validator have no initializers;
  without this, TypeScript throws TS2564 on all DTO fields

---

## `@types/express` required in NestJS + Fastify

Guards and interceptors that import `Request` from `@nestjs/common` do not compile without
`@types/express`, even when Fastify is the platform.

```json
{
  "devDependencies": {
    "@types/express": "^5.0.0",
    "fastify": "^5.7.2"
  }
}
```

- `@types/express` — for NestJS internal typings that reference Express types
- `fastify` in devDependencies — for `FastifyReply` and `FastifyRequest` typings

---

## Fastify plugin versions for NestJS 11 (Fastify 5)

NestJS 11 uses Fastify 5 internally. Plugins built for Fastify 4 (pre-v12/v7/v9) are
incompatible and cause an immediate crash on boot — and the reverse is equally true: pin the
old NestJS-10-era versions (`@fastify/helmet@^11.x`, `@fastify/static@^6.x`,
`@fastify/multipart@^8.x`) against NestJS 11 and you get the same crash from the other
direction.

| Package | Correct version (NestJS 11 / Fastify 5) |
|---|---|
| `@nestjs/platform-fastify` | `^11.1.29`+ (earlier 11.x pins older `@fastify/static` majors — see below) |
| `fastify` | `^5.7.2`+ (first patched version for the Content-Type bypass CVE) |
| `@fastify/helmet` | `^13.x` |
| `@fastify/static` | `^10.1.2`+ (patched version; also the first range `@nestjs/platform-fastify@11.1.29` accepts) |
| `@fastify/multipart` | `^10.x` |

**Typical error:** `FastifyError: fastify-plugin: @fastify/helmet - expected '4.x' fastify version, '5.x' is installed` (or vice-versa if versions are pinned backwards).

**IMPORTANT:** Never use the `helmet` package (Express middleware) with Fastify — it crashes on init.
Always use `@fastify/helmet`.

**Before upgrading across this NestJS 10→11 / Fastify 4→5 boundary**, check for two
Fastify-5-specific breaking changes that bite silently rather than crashing on boot:
- Wildcard (`*`) route parameters lost their standalone greedy-match meaning — routes must
  name the wildcard param explicitly.
- `FastifyAdapter({ logger: ... })` no longer accepts a custom logger *instance* — only a
  boolean or a pino options object. Passing an instance (rather than `false`/`true`) silently
  breaks in a way TypeScript won't catch if the option is typed loosely.

Neither breaking change fails fast — audit routes and `main.ts`'s `FastifyAdapter(...)` call
for both before flipping the major version, not after.

---

## Jest + ESM-only transitive dependencies (NestJS 11 / CommonJS)

Node 22.12+ can `require()` an ESM-only package, so a CommonJS NestJS app runs fine — but
**Jest's CommonJS runtime cannot**. Example: `@fastify/static@10.1.5` (needed by Swagger UI)
depends on `content-disposition@3`, which is ESM-only. A test that boots the app and calls
`SwaggerModule.setup()` dies with `process.exit called with "1"` and a misleading
`The "@fastify/static" package is missing` log. Probe the real error with a one-line test
(`require('@fastify/static')` inside `it()`), then let ts-jest transpile just those packages:

```javascript
// apps/api/jest.config.js
const ESM_ONLY = ['content-disposition'];
module.exports = {
  testEnvironment: 'node',
  transform: {
    '^.+\\.ts$': ['ts-jest', { tsconfig: 'tsconfig.json' }],
    '^.+\\.js$': ['ts-jest', { tsconfig: { allowJs: true }, isolatedModules: true }],
  },
  // pnpm paths look like node_modules/.pnpm/content-disposition@3.0.0/node_modules/content-disposition/
  transformIgnorePatterns: [`/node_modules/(?!(\\.pnpm/)?(${ESM_ONLY.join('|')}))`],
};
```

On NestJS 12 with ESM + Vitest this problem does not exist. On NestJS 12 kept on CommonJS + Jest
(migration section above), Jest 30 + `--experimental-vm-modules` loads ESM packages directly, so
this transform list is *probably* unnecessary — not verified in practice.

---

## `@fastify/static` required in runtime dependencies

`@nestjs/platform-fastify` attempts to load `@fastify/static` during initialization, even
if `useStaticAssets()` is never called — and as of `@nestjs/swagger@11`, Swagger's own
Fastify-side UI setup (`SwaggerModule.setup(...)`) declares `@fastify/static` as a genuine
peer dependency too, not just an internal implementation detail. Without the package, either
the process exits silently on boot, or (with Swagger mounted) it throws
`The "@fastify/static" package is missing` when `SwaggerModule.setup()` runs.

**Rule:** Always include `@fastify/static` in `dependencies` (not `devDependencies`), pinned
to a range both `@nestjs/platform-fastify` and `@nestjs/swagger` accept — check both peers'
`peerDependencies` before picking a version; `^10.1.2` satisfies both as of
`@nestjs/platform-fastify@11.1.29` / `@nestjs/swagger@11.4.6`.

```json
{
  "dependencies": {
    "@nestjs/platform-fastify": "^11.1.29",
    "@nestjs/swagger":    "^11.0.0",
    "@fastify/static":    "^10.1.2",
    "@fastify/helmet":    "^13.0.0",
    "@fastify/multipart": "^10.0.0"
  }
}
```

---

## Workspace packages must be compiled before running the API

A workspace package with `"main": "src/index.ts"` causes Node.js to attempt to execute
TypeScript at runtime when the API runs as `node dist/main.js`.

**Correct package.json for a workspace package:**

```json
{
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "exports": {
    ".": {
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  }
}
```

**Build order:** workspace package builds must run BEFORE the API build.
In a dev script or CI pipeline, always run `pnpm build` in `packages/*` before `apps/api`.

---

## Guards — extract resource ID from multiple param name conventions

NestJS apps commonly mix two URL patterns for the same resource:

| Route pattern | `request.params` keys |
|---|---|
| `GET /resource/:id` | `{ id }` — owner route (summary, update, delete) |
| `GET /resource/:resourceId/children` | `{ resourceId }` — sub-resource routes |

A guard that only reads `request.params.resourceId` silently fails on `GET /resource/:id`
— the param key is `id`, not `resourceId`, so the guard gets `undefined` and throws 403
even for authorized users.

**Pattern — read both param name conventions:**

```typescript
// ❌ Misses owner routes (/resource/:id)
resourceId = request.params?.resourceId ?? request.body?.resource_id;

// ✅ Handles both /resource/:id and /resource/:resourceId/children
resourceId = request.params?.resourceId
          ?? request.params?.id
          ?? request.body?.resource_id;
```

**When to apply:** any guard that resolves a parent resource ID from the URL. Check both
the owner routes (`@Get(':id')`) and sub-resource routes (`@Get(':resourceId/children')`)
when writing or reviewing a guard.

---

## PATCH endpoint required for every entity with an edit form

Every entity that has an edit form in the frontend needs a `PATCH /<entity>/:id` endpoint.
Missing this causes `Cannot PATCH /api/v1/...` (404) in the frontend.

**Required artifacts per module:**

| File | Minimum content |
|---|---|
| `dto/update-<entity>.dto.ts` | `PartialType(OmitType(CreateDto, ['owner_id', ...] as const))` |
| `use-cases/update-<entity>.use-case.ts` | `EntityNotFoundException` (domain) if not found + `update().eq('id').select().single()` |
| `<entity>.controller.ts` | `@Patch('<entity>/:id')` with `@Param('id')` + typed body |
| `<entity>.module.ts` | use case registered in `providers` |

**DTO pattern:**

```typescript
import { OmitType, PartialType } from '@nestjs/swagger';
import { CreateEntityDto } from './create-entity.dto';

export class UpdateEntityDto extends PartialType(
  OmitType(CreateEntityDto, ['owner_id', 'created_at'] as const),
) {}
```

**Use case pattern:**

```typescript
async execute(id: string, dto: UpdateEntityDto): Promise<Entity> {
  const { data: existing } = await this.supabase.client
    .from('table').select('id').eq('id', id).single();
  if (!existing) throw new EntityNotFoundException('Entity', id);   // domain exception → 404 via the filter

  const { data, error } = await this.supabase.client
    .from('table').update(dto).eq('id', id).select().single();
  if (error || !data) throw new DatabaseException('PERSISTENCE_FAILED', error?.message ?? 'Update failed');
  return data as Entity;
}
```

Use cases throw the plugin's domain / infrastructure exceptions (`dev-patterns:error-handling`),
never `NotFoundException` / `InternalServerErrorException` from `@nestjs/common` — the
`AppExceptionFilter` maps them to the HTTP status (`dev-core:error-handling`).

**Controller pattern:**

```typescript
@Patch(':id')
@ApiOperation({ summary: 'Update entity' })
update(@Param('id') id: string, @Body() dto: UpdateEntityDto) {
  return this.updateEntity.execute(id, dto);
}
```

**Rule:** When generating any backend module, check whether there is a corresponding edit screen
in the frontend. If yes, PATCH is required. Verify that all HTTP verbs are present in the
controller: POST (create), GET (list/find), PATCH (update), DELETE/archive when applicable.

---

## POST requests with empty body require `JSON.stringify({})`

When the client sets `Content-Type: application/json` (the default for most API clients),
Fastify rejects POST requests with no body with error 500:
`"Body cannot be empty when content-type is set to 'application/json'"`.

This commonly affects action endpoints like `/deactivate`, `/archive`, `/cancel`, `/activate`.

**Solution — client side:** send `body: JSON.stringify({})` for POST endpoints without a payload:

```typescript
export function deactivateItem(id: string): Promise<void> {
  return apiRequest<void>(`/items/${id}/deactivate`, {
    method: 'POST',
    body: JSON.stringify({}),  // required — Fastify rejects empty body when Content-Type is JSON
  });
}
```

**When to apply:** any POST endpoint that takes no request body: `/deactivate`, `/archive`,
`/cancel`, `/activate`, `/resolve`, `/confirm`.

---

## Compiled build — new endpoints require rebuild and restart

When the API runs as `node dist/main.js`, adding new endpoints to a controller does NOT
hot-reload. The new routes return 404 until a full rebuild and process restart.

**Diagnosis:**

```bash
ps aux | grep node   # "node dist/main.js" → compiled build, no hot reload
```

**Solution:**

```bash
cd apps/api
pnpm build                                    # recompile TypeScript → dist/
pkill -f "node dist/main.js"                  # kill old process
node dist/main.js &                           # start with new dist
```

**Verification:** in the NestJS boot log, confirm the new route appears:

```
[RouterExplorer] Mapped {/api/v1/items/:id/deactivate, POST} route
```

**For development:** prefer `nest start --watch` to avoid this issue entirely.

---

## CORS — list all frontend origins explicitly, and all methods explicitly

With Fastify, `app.enableCors()` must include every frontend origin (port) explicitly.
Unlisted origins receive a silent CORS error in the browser.

**Also list `methods` explicitly — without it, `@fastify/cors`'s preflight
response only allowed `GET, HEAD, POST`.** Every `PATCH`/`DELETE`/`PUT`
call from a real browser client failed at the preflight stage, before the
request ever reached a controller — a typical symptom is an admin panel
whose delete/edit buttons fail silently while every curl test passes.
**`curl`-based testing will never catch this** — CORS is a browser-only
enforcement mechanism, `curl` and React Native's `fetch` don't apply it at
all, so an endpoint can look fully verified (curl 200/204, correct
response body) while being completely unreachable from any actual browser
tab. If a project has more than one browser-based frontend (e.g. a mobile
web build + an admin dashboard), test each one — the first browser client
to call `PATCH`/`DELETE` is usually the first to notice.

```typescript
app.enableCors({
  origin: ['http://localhost:8081', 'http://localhost:8082'],
  methods: ['GET', 'HEAD', 'POST', 'PATCH', 'PUT', 'DELETE'],
  credentials: true,
});
```

---

## main.ts — required template

```typescript
import 'dotenv/config';       // FIRST line — loads .env before any module
import 'reflect-metadata';
import { NestFactory } from '@nestjs/core';
import { FastifyAdapter, NestFastifyApplication } from '@nestjs/platform-fastify';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create<NestFastifyApplication>(
    AppModule,
    new FastifyAdapter(),
  );
  // ... configuration ...
  await app.listen(process.env.PORT ?? 3000, '0.0.0.0');
}
bootstrap();
```

**`dotenv` must be in `dependencies`** (not devDependencies) in the API's `package.json`.
NestJS does not load `.env` automatically — without `dotenv/config` as the first import,
the process aborts with missing environment variable errors.

---

## Filtering `timestamptz` by local calendar date — `utcRangeForLocalDate`

When a controller accepts `?date=YYYY-MM-DD` to filter a `timestamptz` column, it must also
accept `?tz=` (the user's IANA timezone) and compute the UTC bounds dynamically. Never
hardcode an offset like `-03:00` — it breaks for any user outside that timezone.

**Controller pattern:**
```typescript
@Get('resource')
async list(
  @Param('resourceId') resourceId: string,
  @Query('date') date?: string,
  @Query('tz') tz?: string,
) {
  return this.listUseCase.execute(resourceId, date, tz);
}
```

**Use case pattern:**
```typescript
async execute(resourceId: string, date?: string, tz = process.env.APP_DEFAULT_TZ ?? 'UTC') {
  if (date) {
    const { start, end } = utcRangeForLocalDate(date, tz);
    return this.repo.findByResource(resourceId, { start, end });
  }
  return this.repo.findByResource(resourceId);
}
```

**Helper function — no external libraries required:**
```typescript
function utcRangeForLocalDate(dateStr: string, tz: string): { start: string; end: string } {
  // Derive the UTC offset by comparing noon UTC with its local representation.
  // Using noon avoids DST boundary edge cases that affect midnight.
  const noonUtc = new Date(`${dateStr}T12:00:00Z`);
  const localNoonStr = noonUtc.toLocaleString('sv-SE', { timeZone: tz }); // "YYYY-MM-DD HH:MM:SS"
  const localNoon = new Date(localNoonStr.replace(' ', 'T') + 'Z'); // parse as UTC to get ms value
  const offsetMs = noonUtc.getTime() - localNoon.getTime(); // positive for UTC- zones (e.g. UTC-3 = +3h)

  const startMs = new Date(`${dateStr}T00:00:00Z`).getTime() + offsetMs;
  return {
    start: new Date(startMs).toISOString(),                        // local midnight in UTC
    end:   new Date(startMs + 24 * 60 * 60 * 1000 - 1).toISOString(), // local 23:59:59.999 in UTC
  };
}
// UTC-3 example: date="2026-06-25", tz="America/Argentina/Buenos_Aires"
//   → start: "2026-06-25T03:00:00.000Z"  end: "2026-06-26T02:59:59.999Z"
// UTC+5:30 example: date="2026-06-25", tz="Asia/Kolkata"
//   → start: "2026-06-24T18:30:00.000Z"  end: "2026-06-25T18:29:59.999Z"
```

**When to apply:** any use case that filters `timestamptz` rows by calendar day
(daily schedules, metrics by date, history grouped by day). A plain `date` column type
(e.g. `occurred_on DATE`) does not need this — filter with `.eq('occurred_on', dateStr)`.

**The `tz` default** is a backend fallback only, for whatever timezone makes sense as
this project's default. The frontend must always send `tz` explicitly — relying on
the backend default for every request hides per-user timezone bugs until someone
outside that default zone hits them.

## Deactivate / reactivate — always two separate POST endpoints

When a resource supports soft-delete toggling (`is_active` flag), implement **two dedicated action endpoints** — never a single `PATCH` that accepts `is_active` in the body.

```
POST /resource/:id/deactivate   → DeactivateResourceUseCase  (sets is_active = false)
POST /resource/:id/reactivate   → ReactivateResourceUseCase  (sets is_active = true)
```

**Why not `PATCH /:id` with `{ is_active: true }`?**

`UpdateResourceUseCase` typically applies partial updates from a DTO. If `is_active` is not explicitly declared in `UpdateResourceDto`, the field will be stripped by class-validator / class-transformer and will never reach the database — the PATCH silently succeeds but the record stays inactive.

Adding `is_active` to the update DTO is also undesirable: it conflates lifecycle management with field editing, and allows a PATCH from an edit form to accidentally reactivate a record.

**Pattern:**

```typescript
// reactivate-resource.use-case.ts
@Injectable()
export class ReactivateResourceUseCase {
  constructor(private readonly repo: IResourceRepository) {}

  async execute(id: string): Promise<Resource> {
    const item = await this.repo.findById(id);
    if (!item) throw new EntityNotFoundException('Resource', id);   // never @nestjs/common's NotFoundException
    return this.repo.reactivate(id);
  }
}

// resource.controller.ts
@Post(':id/reactivate')
@ApiOperation({ summary: 'Reactivate resource' })
reactivate(@Param('id') id: string) {
  return this.reactivateResource.execute(id);
}
```

```typescript
// IResourceRepository
reactivate(id: string): Promise<Resource>;

// SupabaseResourceRepository
async reactivate(id: string): Promise<Resource> {
  const { data, error } = await this.supabase.client
    .from('resources')
    .update({ is_active: true })
    .eq('id', id)
    .select()
    .single();
  if (error || !data) throw new DatabaseException('PERSISTENCE_FAILED', error?.message ?? 'Reactivate failed');
  return data as Resource;
}
```

**Frontend hook** must call `POST /resource/:id/reactivate` — never `PATCH` with `{ is_active: true }`.

```typescript
export function reactivateResource(id: string): Promise<void> {
  return apiRequest<void>(`/resources/${id}/reactivate`, {
    method: 'POST',
    body: JSON.stringify({}),  // required — Fastify rejects empty body when Content-Type is JSON
  });
}
```

---

## @IsIn instead of @IsEnum for string literal arrays

`@IsEnum([...])` with a plain array of strings does validate correctly — the only defect is the
error message: it doesn't list the allowed values, so the client gets a vague validation error.
`@IsIn([...])` reports them (`status must be one of the following values: ...`).

**Rule:** prefer `@IsIn([...])` for a useful message on any field whose valid values are a
hard-coded list:

```typescript
import { IsIn, IsOptional } from 'class-validator';

// ⚠️ Validates, but the error message doesn't list the allowed values
@IsEnum(['REQUESTED', 'SCHEDULED', 'COMPLETED', 'CANCELLED'])
status?: string;

// ✅ Correct
@IsIn(['REQUESTED', 'SCHEDULED', 'COMPLETED', 'CANCELLED'])
@IsOptional()
status?: string;
```

`@IsEnum(EnumType)` with a real TypeScript `enum` object is fine.
For partial enums (e.g. "status can only be set to X or Y on create") always prefer `@IsIn`.

---

## `whitelist: true` + local DTO classes — fields are silently stripped

When a controller declares its own local DTO classes (instead of importing from `shared-types`), the global `ValidationPipe` with `whitelist: true` **silently removes any field not decorated with a class-validator decorator in that local class**. The request body reaches the use-case already stripped — no error, no log, the field simply disappears.

**This is the most common silent bug when adding a new field to an existing endpoint.**

Checklist when a field is not persisting:
1. Is the field declared with a decorator in the **local DTO class** in the controller file? (not just in the shared-types interface)
2. Does it appear in **both** Create and Update DTOs if both endpoints need it?
3. Is the decorator `@IsOptional()` present for nullable/optional fields?

```typescript
// ✅ Correct — both create and update declare the field
class CreateResourceDto {
  @ApiPropertyOptional() @IsString() @IsOptional() doctor_name?: string;
}

class UpdateResourceDto {
  @ApiPropertyOptional() @IsString() @IsOptional() doctor_id?: string | null;
  @ApiPropertyOptional() @IsString() @IsOptional() doctor_name?: string | null;
}
```

```typescript
// ❌ Silent bug — doctor_name in shared-types but not in local DTO
class UpdateResourceDto {
  // doctor_id and doctor_name absent → whitelist strips them before use-case
  @ApiPropertyOptional() @IsString() @IsOptional() notes?: string;
}
```

**Note on nullable fields in update DTOs:** use `string | null` as the TypeScript type and `@IsOptional()` to allow sending `null` to clear a field. `@IsOptional()` in class-validator short-circuits all other validators for `null`/`undefined`, so `@IsString()` will not reject `null`.

---

## Orphan process holding the port (PPID = 1)

`nest start --watch` compiles and manages its own child process `node dist/main.js`. If a `node dist/main.js` process is started independently (e.g. manually, by a boot script, from another terminal) with PPID = 1 (init), it **is not a child of the watcher** and is not restarted when files change.

**Symptom:** compiled dist files have a recent timestamp, but the server still serves old code — because the live process is the PPID=1 orphan, not the watcher's child.

**Diagnosis:**
```bash
# Find which process is listening on the port
lsof -i :3000 -n -P | grep LISTEN

# Check the PPID — if it is 1, it is an orphan independent of the watcher
ps -o pid,ppid,command -p <PID>

# Check when the process was started
ps -o pid,lstart,command -p <PID>
```

**Fix:** kill the orphan and start a new process with the right environment variables:
```bash
kill $(lsof -ti :3000)
cd apps/api && node -r dotenv/config dist/main.js > /tmp/api.log 2>&1 &
```

`nest start --watch` then detects the free port and starts its own child, or the new process starts directly from the already-compiled dist.

**Note:** `node -r dotenv/config` loads the `.env` file from the current directory — equivalent to what the NestJS CLI does internally via `dotenv`.
