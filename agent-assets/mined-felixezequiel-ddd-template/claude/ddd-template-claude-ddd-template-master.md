# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm test                    # Run all tests (230 tests, node:test via SWC)
npm run test:watch          # Run tests in watch mode
npm run typecheck           # Type check only (tsc, no emit)
npm start                   # Start HTTP + GraphQL servers (MikroORM + SQLite)
npm run migration:create    # Create a new MikroORM migration
npm run migration:up        # Run pending migrations

# Run a single test file
node --import @swc-node/register/esm-register --test src/shared/domain/valueObjects/ValueObject.test.ts
```

## Architecture

DDD template using Hexagonal Architecture (Ports & Adapters) with TypeScript.

**Stack:** TypeScript 5.9 | Node.js 24 | node:test | ESM | SWC on-the-fly (no build step) | MikroORM + SQLite

### Layer Structure

```
src/
├── shared/              # Shared kernel (base classes for all bounded contexts)
│   ├── domain/          # Identifier, ValueObject, Entity, AggregateRoot, DomainEvent
│   ├── application/     # UseCase interface, ApplicationService, DomainEventManager, UnitOfWork
│   ├── ports/           # RepositoryPort, EventPublisherPort, LoggerPort
│   └── infrastructure/
│       ├── logging/     # ConsoleLogger, LoggerRegistry, @log decorator
│       ├── events/      # EventEmitterEventBus
│       ├── http/        # HttpServer (GET/POST, route params)
│       ├── graphql/     # GraphqlServer
│       └── persistence/ # AggregateTracker, TrackedUnitOfWork, AggregatePersister
│           └── adapters/  # MikroOrmUnitOfWork, InMemoryUnitOfWork, NoOpUnitOfWork
│
├── modules/<context>/   # Bounded contexts
│   ├── domain/          # Identifiers, ValueObjects, Entities, Aggregates, Events
│   ├── application/     # Commands, Queries, Ports (primary/secondary), UseCases
│   ├── infrastructure/
│   │   ├── http/        # REST controllers
│   │   ├── graphql/     # GraphQL resolvers
│   │   ├── persistence/
│   │   │   ├── in-memory/   # InMemoryRepository (tests)
│   │   │   └── mikro-orm/   # ORM entities, schemas, mappers, repositories, persisters
│   │   └── notifications/
│   ├── bootstrap/       # <Context>Module.ts (vertical slice wiring)
│   └── integrationTests/
│
├── migrations/          # MikroORM migration files
├── mikro-orm.config.ts  # MikroORM configuration (SQLite)
├── main.ts              # Composition root (monolith entry point)
└── context/docs/        # Architecture Decision Records (ADRs)
```

**Dependency rule:** dependencies point inward — infrastructure -> application -> domain. Domain never imports from outer layers.

### Key Base Classes

- **Identifier** — UUID-based identity. Subclass for each domain ID (e.g., `UserId extends Identifier`).
- **ValueObject\<Props\>** — Immutable via `Object.defineProperty` with `writable: false`. Equality by value. Props are `protected` — subclasses expose domain-meaningful getters.
- **Entity\<Id, Props\>** — Has identity + protected props. Equality by ID. Subclasses expose getters.
- **AggregateRoot\<Id, Props\>** — Extends Entity. Auto-tracks itself via `setOnTrack()` callback when domain events are added. Supports `reconstitute()` static factory for persistence hydration (no events emitted).

### Automatic Aggregate Tracking & Event Dispatch

Aggregates auto-register themselves for persistence and event draining — use cases don't need to manually return aggregates.

**How it works:**

1. At startup, `AggregateRoot.setOnTrack(callback)` wires a global callback that calls `AggregateTracker.track(aggregate)`
2. `AggregateTracker` uses `AsyncLocalStorage` with a stack-based design for request-scoped, async-safe tracking
3. When a use case calls `aggregate.addDomainEvent(event)`, the aggregate auto-registers itself (once per drain cycle)
4. `TrackedUnitOfWork.begin()` pushes a new scope; `commit()` drains tracked aggregates and delegates to `onCommit(aggregates)`
5. `ApplicationService` gets tracked aggregates from the UnitOfWork, drains their events, dispatches/publishes, then commits

**UseCase returns `Promise<T>` directly** — no wrapper types needed. The tracking infrastructure handles the rest.

**UnitOfWork implementations:**

| Implementation       | Purpose    | Persistence                                                                      |
| -------------------- | ---------- | -------------------------------------------------------------------------------- |
| `MikroOrmUnitOfWork` | Production | Forks EM on begin, routes aggregates to `AggregatePersister`s, flushes on commit |
| `InMemoryUnitOfWork` | Testing    | Routes aggregates to `InMemoryRepositoryAdapter`s                                |
| `NoOpUnitOfWork`     | Benchmarks | All operations are no-ops                                                        |

### Command Factory Pattern

Commands use a private constructor + static `of()` factory that receives primitives and constructs VOs internally:

```typescript
CreateUserCommand.of(userId: string, name: string, email: string)
AddAddressCommand.of(userId: string, addressId: string, street: string, number: string, city: string, state: string, zipCode: string)
```

Adapters always call `Command.of()` — never construct VOs directly.

### HTTP Routing

`HttpServer` supports GET and POST with route parameter extraction (`:param` patterns):

```
POST /users                     # Create user
GET  /users/:userId             # Get user by ID
POST /users/:userId/addresses   # Add address to user
```

### Persistence Layer (MikroORM)

- **ORM entities** are plain classes (no domain coupling) in `persistence/mikro-orm/entities/`
- **All ORM entity classes MUST `extends PlainObject`** from `@mikro-orm/core`. MikroORM uses property accessors (proxies) on managed entities; without `PlainObject`, calling `em.upsert(SomeClass, plainInstance)` re-uses identity-mapped proxies and returns proxy values from getters, breaking mappers and triggering subtle hydration bugs. `PlainObject` opts the class out of MikroORM's hydration interception so mappers can read raw primitives safely. Includes child entities (e.g., `AddressEntity`) — every class registered in an `EntitySchema` must extend it.
- **EntitySchema** definitions in `persistence/mikro-orm/schemas/` (no decorators on entities)
- **Mappers** convert between domain aggregates and ORM entities (`toDomain()` / `toOrmEntity()`)
- **AggregatePersister** interface: each module provides a persister that `supports()` its aggregate type and `persist()`s it
- Domain `reconstitute()` factories hydrate aggregates from persistence without emitting domain events
- SQLite database stored in `data/database.sqlite` (gitignored)

## TypeScript Constraints

- **Decorators** require SWC — `@swc-node/register/esm-register` transforms legacy TS decorators at runtime. They do NOT work with native Node.js type stripping.
- **`exactOptionalPropertyTypes: true`** — optional props need explicit `| undefined` in type declarations.
- **Generic constraints** — use `object` instead of `Record<string, unknown>` to accept TS interfaces.
- **ValueObject/Entity encapsulation** — `props` is `protected`. Subclasses must expose public getters with domain-meaningful names (e.g., `get value()` not `props.value`).
- **ValueObject immutability** — `Object.defineProperty` enforces runtime immutability; `readonly` alone is compile-time only. Use `props!: Props` (definite assignment assertion) when set via `Object.defineProperty`.

## Test Conventions

- **Co-located:** `Foo.ts` + `Foo.test.ts` side by side in the same directory.
- **Integration tests** in `<module>/integrationTests/`.
- **Performance benchmarks** in `<module>/performanceTests/`.
- **Framework:** `node:test` (`describe`/`it`) + `node:assert/strict`.
- **UnitOfWork in tests:** use `InMemoryUnitOfWork` with `InMemoryRepositoryAdapter`. Set up `AggregateRoot.setOnTrack()` + `AggregateTracker.track()` in `beforeEach`, reset with `setOnTrack(null)` in `afterEach`.
- Fakes/spies use in-memory implementations (e.g., `InMemoryUserRepository`).
