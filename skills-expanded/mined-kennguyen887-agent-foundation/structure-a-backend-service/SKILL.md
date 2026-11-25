---
name: structure-a-backend-service
description: Use when scaffolding a backend service, adding a feature/module, or reviewing folder layout, file/class naming, DTO & entity structure, or the CQRS read/write split. Language-agnostic with TS/NestJS examples.
metadata:
  last-updated: 2026-06-23
  author: Ken Nguyễn <ntnpro@gmail.com>
---

## When to use

Reach for this when you are **creating a new service repo**, **adding a feature/module** to an
existing one, or **reviewing** whether code is laid out the team way. It answers "where does this
file go", "what do I name it", "how is a feature wired", "how do reads vs writes get split", and
"how are tests structured".

Scope: structure, naming, and wiring — **not** do/don't policy (additive migrations, no `process.env`
in business logic, HTTP-layer tests, backward-compat), which lives in the global instructions,
cross-referenced inline; follow both.

## Steps

Each convention: **portable principle** → **▸ Example (TS/NestJS)** (neutral `listing` domain;
`<feature>` / `<Entity>` = rename) → **▸ Other stacks**. Walk these in order when scaffolding.

### 0. Core principle (read first)

Organize **by feature, not by layer**. A feature owns its entry points, its read path, its write
path, its DTOs, and its events. Keep the transport/entry layer **thin** — it only validates input
and delegates. Centralize the **domain model** (persisted entities + domain types) and **shared base
classes** so features stay about behavior. Drive everything from **typed config**, never raw env
reads.

### 1. Lay out the repo

A service has one source tree split into **feature modules**, **centralized domain models**, two
tiers of shared code, **config factories**, and **schema migrations** as a top-level sibling of
source.

▸ **Example (TS/NestJS)** — copy the shape, swap the domain words:

```
<service-name>/                 # e.g. listings-service
├── src/
│   ├── main.ts                 # bootstrap: global validation pipe, filters, security headers, OpenAPI
│   ├── main.module.ts          # root module: imports every feature module + global providers
│   ├── config/                 # one factory per concern + a consts file of typed keys
│   │   ├── db.config.ts
│   │   ├── cache.config.ts
│   │   └── consts.ts           # configDb='db', configCache='cache', ... (no magic strings)
│   ├── domain/                 # domain layer: persisted models + non-persisted domain types
│   │   ├── entities/           # DB tables (ORM-mapped) — base.entity.ts + <entity>.entity.ts
│   │   └── models/             # domain enums, constants, value objects & type aliases (NO ORM/DB)
│   ├── modules/                # one folder per feature (listing, search, ...)
│   │   └── <feature>/          # see step 2 for the inside of a feature
│   ├── common/                 # app-wide shared business logic: services, constants, shared DTOs
│   └── shared/                 # lower-level: enums, utils, external-system adapters (e.g. search/)
├── libs/                       # vendored shared libraries (see "Shared libraries" below); path-alias resolved
├── migrations/                 # schema changes (DDL) — sibling of src/ (see global Migration Rules)
├── seeds/                      # initial/reference & test data (DML) — its own data-source + CLI, NOT migrations
├── test/                       # mirrors src/modules/; factories + setup live at the root (step 8)
├── ormconfig.migration.ts      # data-source used only by the migration CLI
├── .env.example                # every env var, with safe placeholder (see global Config Rules)
└── package.json
```

- **Two tiers of shared code, and the line between them matters.** `common/` = app-wide *business*
  building blocks (shared services, shared response DTOs, domain constants). `shared/` =
  lower-level, business-agnostic plumbing (enums, pure utils, adapters to external systems). When
  unsure: does it know about your domain? → `common/`. Could it live in any service? → `shared/`.
- **Truly cross-service code is a shared library, not a copied file.** Base classes every service
  needs (pagination response, ORM naming strategy, exception classes, auth guards, CQRS base,
  request logger) live in shared libraries — don't re-implement them per repo. ▸ *Example
  (TS/NestJS):* they sit under `libs/<lib-name>/` (e.g. `infra-common`, `infra-auth`, `infra-cqrs`,
  `infra-exception`), each a package with its own `src/` + build tsconfig, exposed under a
  placeholder path-alias scope `@org/*`. Two things make this work and must stay in sync:
  - **Resolved by path alias, not `npm install`.** The libs are NOT listed in `package.json`
    dependencies; they're mapped in the compiler config (`tsconfig` `paths`) **and** the test
    runner (e.g. `jest` `moduleNameMapper`) — both pointing `@org/<lib>` → `libs/<lib>/src`. Add a
    lib → add both mappings, or build/tests break.
  - **Vendored at a pinned version.** `libs/` is checked out from one central shared repo at a fixed
    tag (e.g. a `libs:build` script doing a meta-repo checkout), so every service runs the same
    version. Bump the tag deliberately; never hand-edit vendored lib code inside a service repo.
  ▸ *Other stacks:* a published internal package (pip/Maven/npm) or a git submodule pinned to a tag —
  the principle is one shared, version-pinned source of truth, not copy-paste.

### 2. Organize a feature module

Everything one feature needs lives in its own folder; reads and writes are **separate files**.

▸ **Example (TS/NestJS)** — inside `src/modules/<feature>/` (here `<feature>` = `listing`):

```
modules/<feature>/
├── <feature>.module.ts        # wires this feature: imports, controllers, providers, exports
├── <feature>.controller.ts    # HTTP/REST entry  (@Controller('listings'))
├── <feature>-cmd.controller.ts# transport entry  (@MessagePattern) — co-located, same handlers
├── <feature>.service.ts       # cross-handler domain logic / external calls (only when shared)
├── commands/                  # ONE write use-case per file (create-listing.ts, publish-listing.ts)
├── queries/                   # ONE read use-case per file  (get-listing-list.ts)
├── events/                    # domain events + their handlers (*.event.ts)
├── dto/
│   ├── inputs/                # request DTOs + index.ts barrel   (see step 4)
│   └── responses/             # response DTOs + index.ts barrel  (see step 4)
└── utils/                     # feature-only helpers (*.util.ts)
```

- **Split the read path from the write path (CQRS).** Each use-case is its own file under
  `commands/` (mutations) or `queries/` (reads). The entry layer dispatches to a bus; it contains
  no business logic. This keeps each use-case independently testable and greppable. ▸ *Other
  stacks:* separate `commands/` and `queries/` packages of one-class-per-use-case handlers; you do
  not need a CQRS framework to get the benefit — the split is the point.
- **One file per use-case holds the request + its handler together.** e.g. `create-listing.ts`
  exports `CreateListingCommand` (the input shape) and `CreateListingCommandHandler` (the behavior).
  Don't scatter a use-case across files.
- **Co-locate multiple transports.** REST and message-based entry points for the same feature sit
  side by side (`<feature>.controller.ts` + `<feature>-cmd.controller.ts`) and both delegate to the
  same command/query handlers. Add a transport without duplicating logic.
- **A `*.service.ts` is for logic shared by several handlers** (or external-API orchestration),
  not a dumping ground. If only one handler needs it, keep it in the handler.

### 3. Name files and classes

Predictable names are the whole point — you should be able to guess a path.

- **Files: `kebab-case`. Classes: `PascalCase`.** A file's class is the PascalCase of its name.
- **Role suffix on framework artifacts, none on use-cases.** ▸ *Example:* `*.controller.ts`,
  `*.service.ts`, `*.module.ts`, `*.entity.ts`, `*.dto.ts`, `*.event.ts`, `*.config.ts`,
  `*.util.ts`. Commands and queries take **no suffix** — the `commands/`/`queries/` folder already
  says what they are (`create-listing.ts`, not `create-listing.command.ts`).
- **Barrel files (`index.ts`) per significant folder**, used for clean folder-level imports and
  **batch registration** (`providers: [...CommandHandlers, ...QueryHandlers]`). ▸ *Other stacks:* a
  package `__init__.py` / `mod.rs` / package export that re-exports the folder.
- **Import paths:** shared libraries via alias (e.g. `@org/*`); everything local via relative paths.

### 4. Define DTOs — split inputs from responses

DTOs are the typed contract at the boundary; requests and responses never share a folder.

- **`dto/inputs/` vs `dto/responses/`.** Inputs validate incoming data; responses shape what goes
  out (and hide internal fields).
- **Every `inputs/` and `responses/` folder has an `index.ts` barrel** re-exporting its DTOs, so
  consumers import in **one line**, not one per file:
  `import { CreateListingRequestDto, GetListingQueryDto } from '../dto/inputs';`. When you add a DTO,
  add its `export * from './x.dto';` to that folder's `index.ts`. ▸ *Other stacks:* the package's
  re-export file (`__init__.py`, `mod.rs`, a package index).
- **Naming encodes direction & cardinality.** ▸ *Example:* inputs `Create<Entity>RequestDto`,
  `Update<Entity>RequestDto`, `Get<Entity>QueryDto`; responses `<Entity>ResDto`,
  `<Entity>ListResDto`. List responses extend a shared pagination-response base.
- **Validate on input, whitelist + transform.** ▸ *Example:* declarative validation decorators
  (`@IsUUID`, `@IsEnum`, `@Transform`) + a global validation pipe (`whitelist: true,
  transform: true`) that rejects unknown fields and turns validation errors into the standard
  `AppBadRequestException`.
- **Control output explicitly.** ▸ *Example:* `@Exclude()` on the class, `@Expose()` per field,
  `@Type(() => Nested)` for nested DTOs; map entity→DTO with `plainToInstance(<Entity>ResDto, data)`
  in the handler. ▸ *Other stacks:* an explicit serializer/schema (Pydantic model, Java DTO +
  mapper, Go struct with json tags) — never return the persistence model directly.

### 5. Define entities and access data

- **The domain layer splits in two — `entities/` vs `models/`.** ▸ *Example:* `src/domain/entities/`
  holds ORM-mapped **DB tables**; `src/domain/models/` holds **domain types that are not tables** —
  enums/value sets (`Gender`, `<Entity>Status`), domain constants, and type aliases/projections
  (`type <Entity>Object = <Entity>`). Pure types, no ORM decorators, no DB; one concept per
  kebab-case file, re-exported via the folder barrel. Put low-level/technical enums in
  `shared/enums/` instead — domain-central value sets belong in `domain/models/`. ▸ *Other stacks:*
  a `domain/` package split into persisted models and plain enums/value-objects/types.
- **All persistence models in one place, on a shared base.** ▸ *Example:* `src/domain/entities/`
  (not inside features). Every entity extends `BaseEntity`, which adds
  `createdAt`/`updatedAt`/`isDeleted` (audit + **soft delete**) — these are `select: false`, so you
  opt in. Soft-deleted rows are excluded with an explicit `WHERE isDeleted = false`. ▸ *Other
  stacks:* a base model / mixin contributing the same audit + soft-delete columns.
- **DB columns `snake_case`, code properties `camelCase`** — bridged by a naming strategy, so you
  never hand-name columns. ▸ *Other stacks:* the ORM's snake-case-to-camel mapping config.
- **Use the ORM's repository directly + a query builder; no custom repository wrapper layer.**
  ▸ *Example:* inject the typed repository into the handler and build queries with the query
  builder; **select only the columns you need**. Push every row filter (status/type/date/soft-delete)
  into the query — do not fetch broadly and filter in code (this is also a global rule).
- **Money/decimals go through a decimal transformer** (fixed precision/scale + a decimal type),
  never raw floats.
- **Migrations vs seeds are different tools — keep them apart.** **Migrations** change the *schema*
  (DDL: create/alter/drop tables & columns) or transform existing data; they are reversible
  (`up`/`down`) and immutable once merged. **Seeds** insert *initial/reference or test data* (DML).
  ▸ *Example:* `migrations/` with its own data-source + CLI, and a separate `seeds/` with its own
  data-source + CLI. Never seed production data inside a migration. For the full migration *rules*
  (additive-only, reversible, run on a fresh DB before commit) follow the global **Database &
  Migration Rules** — not restated here.

### 6. Wire the code patterns

- **Thin entry layer.** Controllers validate the DTO and dispatch to the matching handler; no
  business logic. (Matches the global "request handlers read top-to-bottom in one screenful" rule.)
- **Errors: throw typed domain exceptions, translate once at the edge.** ▸ *Example:* handlers
  throw `AppBadRequestException` / `AppNotFoundException`; a single global exception filter maps
  them to the HTTP/transport response. Don't format error responses inside handlers. ▸ *Other
  stacks:* a custom exception hierarchy + one global error handler/middleware.
- **Side effects via domain events, not inline calls.** ▸ *Example:* a handler emits an event
  (`<Entity>StatusChangedEvent`); an event handler publishes outward (an external pub/sub). Keep the
  use-case's own logic free of fan-out. ▸ *Other stacks:* an event bus / outbox.
- **External systems behind an adapter + base service** in `shared/`. ▸ *Example:*
  `shared/<external-system>/<system>-base.service.ts` centralizes auth/URL/error handling; adapters
  translate domain↔external shapes. Business code calls the adapter, never the HTTP client directly.
- **Cross-cutting concerns are global, declared once** (request logging, activity log, security
  headers, auth guards) — not re-added per controller.

### 7. Configuration

- **No raw env in business code.** ▸ *Example:* one config factory per concern in `src/config/`
  (`registerAs('<key>', () => ({...}))`), keys are constants in a `config/consts` file, read via
  `configService.get(configDb)`. ▸ *Other stacks:* a typed settings object / config service.
- **Per-environment files** (`.env.<NODE_ENV>`), and **every var in `.env.example` + validated at
  boot** (global **Config & Environment Rules** — fail fast, no silent fallback).

### 8. Testing (unit & integration)

The team tests **through the outermost boundary**, not isolated internals — so a "unit" of behavior
is verified the way it actually runs. Boot the app once, build data with factories, hit the real
transport, assert response **and** persisted state.

- **Tests mirror `src/modules/`.** One spec per controller/use-case under `test/modules/<feature>/`;
  factories and the boot harness live at the test root.
- **Boot the app once, share a context.** A single setup file builds the app from the **root
  module**, overrides **only external infra** (job queue, logger) with mocks, starts the transport
  + a client, and exposes a global `testContext = { app, module, client, dataSource }`. An
  aggregator entry globs and `require`s every `*.spec.ts` so the whole suite boots once (fast,
  shared DB). ▸ *Example:* `test/setup-app.ts` + a `test/<suite>.e2e.ts` entry. ▸ *Other stacks:* a
  shared fixture / `conftest` that starts the app + a real test DB once per run.
- **Exercise via the real boundary.** Each test sends a real request through the transport/HTTP
  client and asserts **both** the response shape **and** the persisted DB row (re-read it from the
  repository). Re-apply the same global validation pipe the app uses in prod.
- **Mock only what crosses the process boundary.** Stub external service calls
  (`jest.spyOn(ExternalService.prototype, 'method')`) and outbound HTTP (an HTTP-intercept lib);
  use a **real database**. Never mock the unit under test. Assert outbound side effects with
  spy-called-with.
- **Factories build data; clean up per test.** An `EntityFactory<T>` base with `make(overrides)`
  (random values via a faker lib) and `build()` (persist), plus a `FactoryContext(dataSource)` that
  tracks created rows and tears them down in `afterEach`. ▸ *Other stacks:* factory_boy / test-data
  builders + per-test truncation or a transactional rollback.
- **No isolated unit tests that bypass the boundary.** This matches the global **HTTP-layer testing
  rule**: if a behavior can't be reached through the boundary, *skip* it rather than unit-testing
  internals (no `tests/services/**`, `tests/validators/**`, `tests/utils/**` that bypass the route).
- **Coverage** is collected from `src/**` but excludes wiring with no logic (`*.module.ts`,
  `config/*`, `main.ts`, mocks).

### 9. Porting to a non-TS / non-NestJS stack

Keep the **principles** (left), swap the **realization** (right):

| Principle (portable)                          | Example (TS/NestJS)                            | Generic equivalent |
|-----------------------------------------------|------------------------------------------------|--------------------|
| Feature-based folders, not layer-based        | `src/modules/<feature>/`                       | one package per feature |
| Split read vs write use-cases                 | `commands/` + `queries/`, CQRS bus             | command/query handler packages (no framework needed) |
| Thin entry layer delegates                    | controller → `CommandBus`/`QueryBus`           | thin handler → use-case object |
| Multiple transports, one core                 | `*.controller.ts` + `*-cmd.controller.ts`      | HTTP + gRPC/queue adapters over shared handlers |
| Domain layer: persisted models vs domain types | `domain/entities/` (+`BaseEntity`) & `domain/models/` | persisted models + enums/value-objects |
| Inputs vs responses, validated & serialized   | `dto/inputs` + `dto/responses` + global pipe   | request schema + response serializer |
| Typed config, no raw env                       | config factories + typed keys + config service | typed settings module |
| Typed exceptions, one global translator        | `App*Exception` + global filter                | exception hierarchy + error middleware |
| Shared base code is a shared library           | `@org/infra-*` path alias                      | internal shared library/module |
| Test through the boundary, boot once, factories| `setup-app` + transport client + factories     | shared fixture + real test DB + data builders |

## Verification

A module/repo follows the conventions when **all** of these hold:

- **Layout:** `find src -maxdepth 2 -type d` shows `config/`, `domain/entities/`, `domain/models/`,
  `modules/`, `common/`, `shared/`; each feature under `modules/<feature>/` has its own `*.module.ts`
  and (where it has use-cases) `commands/` and/or `queries/`. No entity files live inside a feature
  folder. Schema changes live in `migrations/`, data in `seeds/` (separate data-sources); shared
  libs in `libs/`, mapped `@org/<lib>` → `libs/<lib>/src` in **both** `tsconfig` and the test runner.
- **Read/write split:** mutations live in `commands/`, reads in `queries/`; each use-case file
  holds its request type **and** its handler.
- **Naming:** framework files carry their role suffix and use-case files carry none; filenames are
  kebab-case and each class name is the PascalCase of its file name.
- **DTOs:** request DTOs only under `dto/inputs/`, response DTOs only under `dto/responses/`; no
  handler returns a raw entity.
- **Config:** `grep -rn "process.env" src/ --include='*.ts' | grep -v "src/config/"` returns only
  **bootstrap** files (`main.ts` / `main.module.ts` selecting the env file or port). Any hit inside
  `modules/`, `common/`, or `shared/` is a violation — env there must be read through `config/`.
  (Note the quoted `'*.ts'`: an unquoted glob fails under zsh.)
- **Tests:** `test/` mirrors `modules/`; specs hit the real transport/HTTP boundary and assert
  persisted state; only external infra is mocked. No unit-test files bypass the boundary.
- **Gates pass:** lint, build, and the test suite are green (your stack's equivalents of
  `pnpm lint` / `pnpm build` / `pnpm test`); `.env.example` lists every new var.

If porting to another language, the **Verification** above maps 1:1 — the folder names change, the
checks (feature folders exist, read/write split exists, no raw env in business code, no model
leakage in responses, tests run through the boundary) do not.

## Related

- [README](./README.md) — how project skills are organized and discovered.
- [write-service-code](./write-service-code.md) — how to write the code *inside* these files
  (control flow, async, query performance, events/SQS, logging, tests). This skill = **where & what**;
  that one = **how**.
- **Global assistant instructions** (highest authority for the do/don't *policy* this skill points
  at): *Database & Migration Rules*, *Config & Environment Rules*, *Testing Rules / HTTP-layer
  testing rule*, *Code Style — Function Size & Density*, *DRY — Parallel flows*. This skill says
  **where code goes and what it's named**; those say **what it must and must not do**.
