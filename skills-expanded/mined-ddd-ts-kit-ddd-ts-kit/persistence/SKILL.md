---
name: persistence
description: >-
  Use when adding a table, a repository, a lookup, a read model or a migration, replacing
  the in-memory adapter by a real one, choosing an ORM, or when persistence types leak out
  of infrastructure. Mapper, unit of work, optimistic concurrency, Drizzle, Knex, Prisma,
  TypeORM, OpenSearch.
argument-hint: "<context> <Aggregate>"
allowed-tools:
  - Read
  - Edit
  - Bash(npx ddd-ts-kit generate *)
  - Bash(npx ddd-ts-kit check *)
  - Bash(npx ddd-ts-kit list *)
  - Bash(npm test *)
---

# Persistence

Subject: `$ARGUMENTS`

```bash
npx ddd-ts-kit generate repository <ctx> <Aggregate> [--tenant-scoped] [--personal <column>,... [--subject <column>] [--erasure pseudonymise|row]] --json
```

writes the port (an abstract class extending the kernel `Repository<Aggregate>` in
`domain/repositories/`), the adapter of the project's ORM with its mapper and table in
`infrastructure/persistence/`, the fake, and one `repositoryContract` spec that both must
pass. `generate command --aggregate` creates it when missing. Fill the `todos` places: the
lookups of the port, the columns, the mapper.

Read model of a projection: `generate read-model <ctx> <Name> --field <name>:<type>...` writes
port (over `ReadModelStore<Row>`), table, store adapter, fake and `readModelContract` spec,
not `port` then `adapter`.

## Rules, whatever the technology

- **One repository per aggregate root**, whole-aggregate load and save. Add only the lookups
  a use case needs, named in the ubiquitous language; a screen reads through a read port.
- **Rows stay inside.** The mapper translates row to aggregate (`rehydrate`) and back; it is
  the one place for a type assertion. No ORM type crosses the port.
- **Each context owns its tables**, in its own database schema and in a file of its own: the
  tables file of `infrastructure/persistence/` (Drizzle, Knex, TypeORM; `shared/infrastructure/persistence/` with modules) or on Prisma
  `prisma/schema/<context>.prisma` (an earlier single `prisma/schema.prisma` moves first: the
  generator refuses with the steps). A stored field changes its column and the mapper in one commit. No foreign key, join or
  query across contexts: reference by identifier, a published contract or a local projection (`context/extractable`).
- **Transactions belong to the application.** The unit of work is a middleware of the command
  bus; a repository picks up the ambient transaction, never receives one, never commits.
  Domain events are dispatched at its end, before the commit. A unit of work of your own
  builds `run` on `withinUnitOfWork` of the kernel and passes `unitOfWorkContract`.
- **Optimistic concurrency** on the aggregate's `version`: a conflicting save raises
  `ConcurrencyError`; so does a deadlock or a serialization failure
  (`TransactionConflictError`): retry the command, never map the driver error. A taken unique
  value (an email) raises `UniqueViolationError` (`CONFLICT`), never retried; the handler names
  its refusal. Count then insert has no version: `advisoryLock` of the ORM package first, never
  a raw `pg_advisory_xact_lock`.
- **Audit and tenant columns are standard**: `created_at`, `created_by`, `updated_at`,
  `updated_by`, and `tenant_id` with `--tenant-scoped`, stamped by the adapter from
  `ExecutionScope` and `Clock`. The domain ignores them.
- **Files never in a table.** No binary or base64 column (`persistence/no-file-content`): the
  content lives in the `FileStorage` port (`stack.storage`), a row keeps the key, size, media
  type and checksum of its `StoredFile`, and `FileStaging` orders the write (staged before the
  transaction, recorded, moved to its key with the commit, an orphan in `staging/` purged a day
  later). `docs/concepts/file-storage.md`.
- **Multi-tenant**: every statement on tenant data is confined to the tenant of the work
  (`tenancy/scoped-statement`). Under `stack.tenancy: shared-table` (or another strategy, or to
  become multi-tenant), read [tenancy.md](tenancy.md) first.
- **Outbox in the same transaction** as the business write (`events/outbox-required`).
- **An event-sourced aggregate** (chosen per aggregate, `generate aggregate ... --event-sourced`)
  keeps the same port: under `stack.eventSourcing: on`, read [event-sourcing.md](event-sourcing.md)
  first.
- **What a table keeps of a person is declared** (`--personal`), with its erasure, export and
  retention: under `stack.privacy: on` (the default with an ORM), read
  [personal-data.md](personal-data.md) first when a table keeps something of a person.
  `privacy/declared-field` (a warning) reports a personal column no declaration names.
- **Searches** use `Page` and `PageRequest` of the kernel, a cursor ending on a unique
  tie-breaker; under `stack.search: opensearch`, read [search.md](search.md) first.
- **Queries may skip aggregates**: `generate query` writes a read port and an in-memory
  reader; replace the reader by an adapter that queries the tables and returns the shape of
  the port.
- **Migrations** are generated from the schema, named by what they do
  (`npm run db:generate add-invoices`, which writes `<timestamp>_add-invoices`; it refuses
  to run without the name; under drizzle-kit a rename is never left for it to guess, since
  without a terminal it fails: add then drop in a later migration, or `-- <name> --custom`;
  never under `script` or another pseudo-terminal, where it waits), applied with
  `npm run db:migrate`, committed, forward-only, and compatible with the version still running.
  A table of `generate repository` reaches no database until then, on the four ORM: the specs
  pass before it, on the in-process database. `db:migrate` reads `DATABASE_URL` from the shell,
  else from `.env`. Under TypeORM it builds first, `db:generate` does not:
  `npm run build && npm run db:generate migrations/add-invoices`. Under Knex the steps are the
  same, and a migration holds its SQL and never calls `createTables`; what `db:generate` does not
  write there is in [migrations.md](migrations.md).
  Under drizzle-kit, `drizzle-generate` (what `db:generate` runs) formats the snapshot and journal it wrote with the project's formatter, and
  warns when the SQL changes a primary key in an order that fails, which
  `persistence/primary-key-order` reports until fixed: reorder it (old key dropped first) or
  write it with `--custom`. One `db:generate` writes every schema change made since the last one
  as one migration: to keep two apart (a table, then a constraint once it is filled), change the
  schema in two steps, with a `db:generate` after each. Under `agents.profile: regulated` (or any
  sandbox where a command cannot reach the database), when a merge brings a migration from the
  main branch before yours is merged, or as a worker of a parallel build, read
  [migrations.md](migrations.md) first; `persistence/migration-history` reports a forked or
  unordered history.

## By ORM

`stack.orm` decides what is generated. Each package provides the unit of work with an
ambient transaction, the outbox store and the processed-event store, and documents its
dialects: `@ddd-ts-kit/drizzle` (the default, PostgreSQL, one schema per context),
`@ddd-ts-kit/knex`, `@ddd-ts-kit/prisma`, `@ddd-ts-kit/typeorm`. With `none` or `custom` the
generated adapter is in-memory, held to the same contract suite, behind a `TODO(platform)`.

An outside system is not storage: a provider an environment runs without (a sandbox, a demo)
is simulated by an adapter of production code, `npx ddd-ts-kit generate adapter <ctx> <Port> --kind simulated`, never by a
repository nor by the fake of `test/fakes/`, which production code never imports. Its records
keep the shape the system sends and go through the translator of `infrastructure/anti-corruption/`.

Anything else (another query builder, a document store) is `stack.orm: custom`: provide in
`src/platform/database/` a `UnitOfWork`, an `OutboxStore` and a `ProcessedEventStore`, each
passing its contract suite of `@ddd-ts-kit/testing/contracts`, then the repository adapters.
Nothing in `domain/` or `application/` changes: that is the test of the boundary. A niche
store needs a decision record.

## Tests

The contract spec in `test/integration/` runs the fake and the adapter through the same
suite; adapter specs run on an in-process PostgreSQL unless a database URL is given. Add
what is specific to the adapter: every column mapped, the tenant filter, a rollback.

Finish with
`npx ddd-ts-kit check --rule layer/domain-purity --rule context/extractable --rule ports/implements-never-extends`
and the integration specs of the context.
