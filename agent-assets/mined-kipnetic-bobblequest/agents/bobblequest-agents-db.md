# @t/db — Agent Guide

## What this owns

Persistence ports and Drizzle-backed implementations for the database layer.
Responsible for: Postgres connection pool (via `postgres` driver), Drizzle ORM schema,
migrations, and repository implementations for `User`, `Project`, and `Embedding` domain
entities. Also ships InMemory variants used in unit/CI tests.

## Layout

```
packages/db/
  src/
    entities/
      ports/          DbClient, UserRepository, ProjectRepository,
                       EmbeddingStore, VectorSearchResult (interfaces/types only)
      schemas/        Drizzle table definitions (users, projects, embeddings)
      types/          Pure TS type files (excluded from coverage — no executable code)
    infrastructure/
      drizzle/        DrizzleDbClientImpl, DrizzleUserRepositoryImpl,
                       DrizzleProjectRepositoryImpl, DrizzleEmbeddingStoreImpl
      in-memory/      InMemoryUserRepository, InMemoryProjectRepository,
                       InMemoryEmbeddingStore (test doubles)
    dependency-injection/
      registerDbDI.ts  (see DI Registrar below)
  migrations/         SQL migration files (managed by drizzle-kit)
  tests/
    infrastructure/   Unit tests — both Drizzle AND InMemory variants required
    integration/      Live Postgres tests (separate config; Docker-gated)
    setup/            stubLogging.ts  (required setupFile)
```

## DI Registrar

File: `packages/db/src/dependency-injection/registerDbDI.ts`

Signature: `registerDbDI(container: Container, opts: RegisterDbDIOptions): void`

Selection logic:
- `environment === 'testing'` — binds InMemory repositories only; no `DbClient` registered.
  Any code that resolves `DB_DEPENDENCY_KEY` in a test will fail fast.
- all other environments — requires `config.db.url`; registers `DrizzleDbClientImpl` +
  three Drizzle-backed repository singletons that share the pool.

Exported keys: `DB_DEPENDENCY_KEY`, `USER_REPOSITORY_DEPENDENCY_KEY`,
`PROJECT_REPOSITORY_DEPENDENCY_KEY`, `EMBEDDING_STORE_DEPENDENCY_KEY`
(aliases of `@t/dependency-injection` canonical tokens).

## Consumers

Wired by `apps/api/src/composition.ts` — NOT `apps/website`.
`buildContainer()` in the API composition root calls `registerDbDI` alongside
`registerCacheDI` and `registerQueueDI`. The website composition root
(`apps/website/src/lib/composition.ts`) does not mount the DB layer.

## Conventions

- Port-first: all app code depends on port interfaces, never on Drizzle classes directly.
- Both test suites must stay green: Drizzle-backed tests (unit, `tests/infrastructure/Drizzle*.test.ts`)
  AND InMemory tests (`tests/infrastructure/InMemory*.test.ts`).
- No raw `DbClient` leakage: Drizzle client is internal to `@t/db`; apps never import it.
- `fileParallelism: false` in `vitest.config.ts` — integration tests share one Postgres DB;
  parallel file execution causes cross-file truncation races. Unit tests are fast enough
  that the sequential overhead is negligible.
- Coverage thresholds 100% (statements/branches/functions/lines); schema index callbacks and
  pure type files are explicitly excluded in `vitest.config.ts` because v8 cannot instrument
  Drizzle schema callbacks reliably.
- Migration commands: `bun run db:generate` / `bun run db:migrate` (drizzle-kit).
- Integration tests require Docker: `bun run db:test:up` before running
  `bun run test:integration`.

## Links

- Architecture doc: `docs/architecture/platform/database.md`
- Migrations guide: `packages/db/migrations/README.md`
