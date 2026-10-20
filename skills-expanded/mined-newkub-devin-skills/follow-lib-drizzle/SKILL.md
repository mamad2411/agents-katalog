---
name: follow-lib-drizzle
description: Install and use Drizzle ORM 0.45+ for type-safe database operations with SQL-like syntax
argument-hint: "[scope]"
related:
  - refactor
  - follow-tool-drizzle-kit
  - run-drizzle-studio
  - follow-lib-zod
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Install and use the latest Drizzle ORM for type-safe database operations with SQL-like syntax and the relational query API, following official best practices

## Scope

For projects that need type-safe database access on PostgreSQL, MySQL, SQLite, SingleStore, MSSQL, or CockroachDB

- Install the latest `drizzle-orm` and `drizzle-kit`
- Configure `drizzle.config.ts`
- Create database schema and migrations
- Use the type-safe query builder and relational queries
- Support serverless/edge drivers

Boundaries:
- Use this skill only when the project selects/uses Drizzle ORM
- For ORM-agnostic data access patterns (repository pattern, mappers) → use `/refactor` orm scope (`refactor/SKILL.md` `### 3` **orm** bullet → repository boundary)
- If the task focuses on the `drizzle-kit` CLI (generate/migrate/push/studio) → use `/follow-tool-drizzle-kit`
- Other ORMs (Prisma, TypeORM) are out of scope — do `/refactor` orm scope (`refactor/SKILL.md` `### 3` **orm** bullet → one type-safe ORM) instead

- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### Workflows

| Topic | Workflow |
|-------|----------|
| Setup | `workflows/setup-drizzle/SKILL.md` — install, `schema.ts`, db client |
| Schema design | `workflows/define-schema/SKILL.md` — dialect tables, columns, indexes, `relations()` |
| Relational queries | `workflows/query-relational/SKILL.md` — `db.query`, `with`/`columns`/`extras`, vs `select()` |
| Mutations/transactions | `workflows/use-transactions/SKILL.md` — insert/update/delete, `returning`, upsert, nested tx |
| Migrate | `workflows/migrate-schema/SKILL.md` — generate/migrate/push flow, rollback |
| Seed/fixtures | `workflows/seed-data/SKILL.md` — `drizzle-seed`, `seed()`/`reset()`, deterministic fixtures |
| Optimize | `workflows/optimize-queries/SKILL.md` — indexes, relations, select/where perf |
| drizzle-kit CLI deep dive | `/follow-tool-drizzle-kit` — `generate`/`migrate`/`push`/`pull`/`studio`/`check` |

### 1. Check Precondition

> Goal: verify the environment before starting

1. Confirm a Bun or Node.js runtime is available (`bun --version` or `node --version`)
2. Confirm a database server or a designated SQLite file exists
3. Read the project's `package.json`
4. If there is no `package.json` → stop and report

### 2. Setup

> Goal: install Drizzle ORM, the driver, and drizzle-kit

1. Run `bun add drizzle-orm@0.45.3` or `bun add drizzle-orm` (latest stable)
2. Install the driver matching the runtime and database — see details in 
3. Run `bun add -D drizzle-kit@0.31.11` or `bun add -D drizzle-kit`
4. Verify the dependencies are in `package.json`
5. If you want the v1.0 RC (`drizzle-orm@rc`, `drizzle-kit@rc`) → see the notes in Rules

### 3. Configure

> Goal: create `drizzle.config.ts` and pick the dialect/driver

1. Create `drizzle.config.ts` with `defineConfig` — see examples in 
2. Set `dialect` per database: `postgresql`, `mysql`, `sqlite`, `singlestore`, `mssql`, or `cockroach`
3. Set `driver` only when using a special driver: `turso`, `d1-http`, `expo`, `aws-data-api`, `pglite`, `neon-http`, `bun-sql`
4. Set `schema`, `out`, and `dbCredentials.url` read from `DATABASE_URL` or an appropriate environment variable
5. Never hardcode credentials in `drizzle.config.ts`

### 4. Define Schema

> Goal: create the database schema with type-safe columns

1. Create `src/db/schema.ts` or split into files under `src/db/schema/`
2. Define tables, columns, indexes, and relations — see 
3. Use `pgTable` (PostgreSQL/CockroachDB), `mysqlTable` (MySQL/SingleStore), `sqliteTable` (SQLite), `mssqlTable` (MS SQL)
4. Specify `notNull`, `unique`, `defaultNow` as needed
5. Derive types from the schema with `typeof table.$inferSelect` and `$inferInsert`
6. Define `relations()` to enable the relational query API on v0.x; on the v1.0 RC use `defineRelations()` instead

### 5. Create Client

> Goal: create the database client for the runtime in use

1. Create `src/db/index.ts` per runtime — see 
2. For SQLite: enable WAL mode (`PRAGMA journal_mode = WAL`) for performance
3. For relational queries: pass the `schema` object into `drizzle()`, e.g. `drizzle(url, { schema })`
4. Export the `db` instance with all schema imported
5. Never expose client credentials in source code

### 6. Manage Migrations

> Goal: pick a migration strategy and run migrations

1. Choose the strategy by use case — see [references/cli.md](references/cli.md)
   - Rapid prototyping: `bunx drizzle-kit push`
   - Production/team: `bunx drizzle-kit generate` then `bunx drizzle-kit migrate`
   - Existing database: `bunx drizzle-kit pull`
2. For production: generate migrations with `bunx drizzle-kit generate --name=<name>`
3. Review the migration files in the output directory
4. Run migrations with `bunx drizzle-kit migrate`
5. Check drift with `bunx drizzle-kit check`

### 7. Query Data

> Goal: use type-safe queries and the relational API

1. Import `db` and the schema from `src/db`
2. Use the SQL-like API: `db.insert()`, `db.select().from()`, `db.update()`, `db.delete()` — see 
3. Use the relational API: `db.query.<table>.findMany({ with: {...} })` for nested data
4. Use `db.transaction()` for atomic operations — see 
5. Use `eq`, `and`, `or`, `like`, `gt`, etc. from `drizzle-orm` for filters

### 8. Inspect With Studio

> Goal: use Drizzle Studio to browse data

1. Run `bunx drizzle-kit studio` to open the GUI
2. Use it to browse, filter, and edit records during development
3. Never use it in production

## Rules

### 1. Installation

- `bun add drizzle-orm` or pin a verified latest version
- `bun add -D drizzle-kit` for dev tools
- Use the driver matching the chosen runtime/database

### 2. Configuration

- Create `drizzle.config.ts` with `defineConfig`
- Specify `dialect` (required), `driver` (optional), `schema`, `out`, and `dbCredentials`
- Read the database URL from environment variables

### 3. Schema

- Define the schema in separate files or with glob patterns
- Use type inference from the schema (`$inferSelect`, `$inferInsert`)
- Use `relations()` for v0.x (latest stable)
- On the v1.0 RC use `defineRelations()` and `getColumns()` instead of `getTableColumns`
- Never hardcode credentials

### 4. Migrations

- Choose the migration strategy by use case
- Production must generate + migrate
- Development may use push
- Check drift with `check`
- The v1.0 RC has `drizzle-kit up`, `check` commutativity, `--ignore-conflicts`, `push --explain`

### 5. Driver Selection

- Use the driver appropriate for the runtime and database
- Serverless: `neon-http`, `neon-serverless`, `vercel-pg`, `planetscale-serverless`, `d1`
- Edge/browser: `pglite`
- See details in 

### 6. Version Notes

- Latest stable: `drizzle-orm@0.45.3` + `drizzle-kit@0.31.11` (verified 2026-09-24)
- v1.0 RC: `drizzle-orm@rc` + `drizzle-kit@rc` (currently `1.0.0-rc.4`, verified 2026-09-13) with breaking changes: `relations()` → `defineRelations()`, `getTableColumns` → `getColumns`, `--strict` removed, migration folder v3
- Check the version in `package.json` before choosing APIs

- Use `/refactor` orm scope (`refactor/SKILL.md` `### 3` **orm** bullet → repository boundary) if you need an ORM-agnostic data access pattern
- Use `/follow-tool-drizzle-kit` if the task focuses on the drizzle-kit CLI
- Use /run-drizzle-studio if needed
- Use /follow-lib-zod if Zod is the validator
- Use /follow-best-practice if needed
- Use /use-my-packages-on-registry if needed
- Use /setup-cicd if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Drizzle ORM is installed and working with the correct driver
- Schema is configured correctly per column types and dialect
- Migrations are managed with the appropriate strategy
- Type-safe queries and the relational API work
- Transactions support rollback and nested savepoints
- Performance is optimized with WAL mode and indexes
