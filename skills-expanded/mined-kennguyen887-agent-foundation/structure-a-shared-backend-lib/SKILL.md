---
name: structure-a-shared-backend-lib
description: Use when organizing a shared backend infrastructure library that many services depend on (e.g. @org/infra-*) — how to split it into focused packages by dependency weight, expose one barrel per package, avoid dependency cycles with peer deps, version/publish it, decide what belongs in the lib vs a service, and the canonical primitives it should provide (a base entity with soft-delete + audit columns, base pagination/response DTOs, column transformers, type helpers). NestJS/TypeORM reference, framework-flexible. The backend twin of structure-a-shared-ui-lib.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Structure a shared backend library

A library of cross-cutting infrastructure (`@org/infra-*`) that every backend service imports, so the
fleet is consistent and DRY. This is the *where & how it's packaged*; the framework primitives inside
it are in `write-cross-cutting-code` and `design-an-error-model`. Frontend equivalent:
`structure-a-shared-ui-lib`.

## When to use
You're starting or reorganizing the shared lib behind a fleet of services, deciding which package a
new primitive goes in, or pulling duplicated infra out of services into one place.

## 1. Split into focused packages by dependency weight
- **Several small packages, not one mega-package** — each owns one concern and pulls only the deps it
  needs, so a service that wants typed errors doesn't drag in the whole AWS/cache stack.
- **Order packages from zero-dep core → heavier**, and let the light ones be depended on by the heavy
  ones (never the reverse), so there are **no cycles**:
  - `infra-exception` / `infra-types` — **zero framework deps**; the error model + shared types. Anything
    can import it.
  - `infra-auth` — guards/decorators; depends on the error package (peer), nothing heavier.
  - `infra-cqrs` — base command/query/event classes; orthogonal, used by event-driven services.
  - `infra-common` — the workhorse (pipes, interceptors, middleware, DTOs, base entity, utils, cache,
    messaging clients). Highest reuse; may depend on the lighter packages.
  ```
  @org/infra-exception  (0 deps)  ←─ @org/infra-auth ←─┐
  @org/infra-types      (0 deps)  ←───────────────────┼─ @org/infra-common
  @org/infra-cqrs       (framework only) ←────────────┘
  ```
▸ *Other stacks:* a Go `internal/` module set, a Python namespace package, a Java multi-module
artifact. Principle: **partition by concern + dependency direction; the foundational package has the
fewest deps and is imported by the rest, never the reverse.**

## 2. One barrel per package; import from the package root
- Each package exposes a single `index.ts` (barrel) that re-exports its public surface. Services import
  from the **package root** (`@org/infra-common`), **never deep paths** (`@org/infra-common/src/...`) —
  so internals can move without breaking consumers.
  ```ts
  // infra-common/src/index.ts
  export * from './typeorm'; export * from './pipes'; export * from './dto'; export * from './utils'; /* … */
  // in a service:
  import { BaseEntity, BaseQueryDto, Nullable } from '@org/infra-common';   // root, not a deep path
  ```
▸ *Other stacks:* a package's public API file / `__init__.py` / exported module list. Principle: one
published surface per package; internals are private.

## 3. Version, publish, and depend on the framework as a peer
- **Publish as versioned packages** (a private registry or a workspace monorepo); services pin a
  version and upgrade deliberately. A breaking change to a shared contract (error body, base DTO) is a
  **major** bump — it ripples to every service.
- **The framework itself is a `peerDependency`**, not a bundled dep — so the lib uses the *service's*
  framework version and you don't ship two copies. Keep the lib's own runtime deps minimal.
▸ *Other stacks:* semver + a lockfile; peer/provided scope (Maven `provided`, Go module replace).
Principle: explicit versions, framework as peer, treat shared contracts as a public API.

## 4. What belongs in the lib vs a service
- **In the lib:** cross-cutting concerns reused by ≥2 services and stable contracts — the error model,
  base entity, pagination/response DTOs, auth guards/decorators, messaging clients, pipes,
  interceptors, middleware, common utils (decimal/date/PII-mask/chunk), config helpers.
- **In a service:** domain entities, feature handlers, domain events, anything that changes per
  product. **Don't push volatile business logic into the lib** — every change there forces a fleet-wide
  bump. (DRY parallel flows still applies *within* a service; promote to the lib only once it's stable
  and genuinely shared.)

## 5. Canonical primitives the lib should provide
So every service is consistent, the lib ships the building blocks services extend:
- **A base entity** — a uuid primary key + `createdAt`/`updatedAt` + a soft-delete flag, with audit
  columns `select: false` (excluded from default reads, fetched only when asked). Services extend it
  and add domain columns; soft-delete and timestamps come for free.
  ```ts
  export abstract class IdentityEntity { @PrimaryGeneratedColumn('uuid') id!: string; }
  export abstract class BaseEntity extends IdentityEntity {
    @CreateDateColumn({ select: false }) createdAt!: Date;
    @UpdateDateColumn({ select: false }) updatedAt!: Date;
    @Column({ type: 'boolean', default: false, select: false }) isDeleted!: boolean;
  }
  ```
- **Base pagination + response DTOs** — a `BaseQueryDto` (`pageIndex`/`pageSize` with `offset`/`limit`
  getters) and a `PaginationResponse` (`total`/`pageIndex`/`pageSize`) so every list endpoint paginates
  and shapes results identically. An `IdUUIDParams` for `:id` routes.
- **Column transformers** — decimal (string ↔ number with fixed scale), boolean, and a PII-masking
  transformer, applied at the DB boundary so money/flags/secrets are handled the same everywhere.
- **Type helpers** — `Nullable<T> = T | null` (the agreed "absent" value, see `write-service-code` §3),
  `Optional<T, K>` for partial shapes.
▸ *Other stacks:* a base model/ActiveRecord with timestamps + soft-delete, a shared pagination struct,
value-object converters. Principle: the lib provides the canonical base types so services don't
reinvent (and drift on) them.

## Verification
- The lib is **several concern-focused packages**, the foundational one (errors/types) has **zero
  framework deps**, and dependencies point one way (no cycles).
- Each package has **one barrel**; services import from the **package root**, not deep paths.
- The framework is a **peer dep**; packages are **versioned**; shared-contract changes are major bumps.
- Only **cross-cutting + stable** code lives in the lib; volatile domain logic stays in services.
- Services **extend the lib's base entity + base DTOs** rather than redefining timestamps/soft-delete/pagination.

## Related
- `write-cross-cutting-code` — the pipes/guards/interceptors/decorators that live in the lib.
- `design-an-error-model` — the `infra-exception` package's content (the error contract).
- `structure-a-backend-service` — a service that *consumes* this lib (and its `libs/` section).
- `structure-a-shared-ui-lib` — the frontend twin (a shared UI/design-system lib).
- `write-service-code` (§3 nullability, §5 transformers) · `code-conventions` (DRY parallel flows).
