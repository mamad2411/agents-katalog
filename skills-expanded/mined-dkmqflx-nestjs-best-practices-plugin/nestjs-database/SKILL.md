---
name: nestjs-database
description: NestJS database and ORM best practices (TypeORM, Prisma, Mongoose). Use when integrating a database in NestJS — repositories, entities, migrations, transactions, or query performance. Triggers on TypeOrmModule, @InjectRepository, PrismaService, @Entity, migrations, or N+1 queries.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Database & ORM

Best-practices reference for integrating a database into NestJS through TypeORM, Prisma, or Mongoose. Covers async module configuration, repository injection, schema lifecycle (migrations vs `synchronize`), transactions, relation loading, projection, DTO mapping, and indexing/pagination. Examples favor TypeORM with Prisma notes where the idiom differs.

## When to Apply

- Wiring `TypeOrmModule`/`MongooseModule`/`PrismaModule` with `ConfigService`
- Injecting repositories or model services into providers
- Choosing between `synchronize` and migrations for schema changes
- Writing multi-step writes that must be atomic (transactions)
- Loading relations efficiently (avoiding N+1 queries)
- Selecting only needed columns / not over-fetching
- Returning data from controllers without leaking ORM entities
- Indexing queried columns and paginating large result sets

## Rules

- `async-module-config` - configure the data layer with `forRootAsync` + `ConfigService`; never hardcode credentials
- `repository-pattern` - inject repositories/services into providers; keep DB access out of controllers
- `migrations-not-synchronize` - set `synchronize: false` in production and manage schema with migrations
- `transactions-for-multi-write` - wrap multi-step writes in a transaction (`QueryRunner` / `dataSource.transaction` / `prisma.$transaction`)
- `avoid-n-plus-one` - load relations explicitly (`relations`/`leftJoin`/`include`); never query inside a loop
- `select-needed-columns` - project specific fields; avoid `SELECT *` and over-fetching
- `separate-entities-from-dtos` - map ORM entities to response DTOs; don't expose persistence models directly
- `index-and-pagination` - index queried columns and paginate large results with `take`/`skip`

## How to Use

Read individual rule files in `rules/` for the rationale plus incorrect/correct examples. Each rule is self-contained; apply the ones relevant to the change you are making. Default to TypeORM idioms; Prisma/Mongoose equivalents are noted inline where they differ.
