---
name: spring-mongo-lightweight-migration
description: Annotation-driven MongoDB migration runner for Spring Boot — `@MongoMigration` methods on `MigrationScript` beans execute in order at startup, with history in `{prefix}_migrations` collection. No Mongock dependency.
category: backend
tags: [spring-boot, mongodb, migration, annotation-driven, idempotent]
triggers:
  - "mongo migration spring boot"
  - "mongock 없이 마이그레이션"
  - "annotation-based mongo migration"
scope: user
version: 1.0.0
---

# Spring Boot + MongoDB Lightweight Migration

Annotation-driven migration runner: discover `@MongoMigration` methods on `MigrationScript`-implementing beans, execute in `order`, record results in a `{prefix}_migrations` collection so already-run migrations are skipped.

## When to use
- Spring Boot + MongoDB project that needs versioned schema/data changes.
- Want to avoid the footprint of Mongock / Flyway-for-Mongo.
- Idempotent, startup-triggered migrations are acceptable.

## Steps
1. Create 4 infra files: `@MongoMigration` annotation, `MigrationScript` marker interface, `MongoMigrationConfig` (collects beans), `MongoMigrationRunner` (`@EventListener(ApplicationReadyEvent.class)` discovers + runs + records).
2. Convention: one `V{nnn}_{Desc}.java` per migration, `@Component implements MigrationScript`, annotate method with `@MongoMigration(id, order, description)`.
3. Each method must be idempotent — guard with `collectionExists` / pre-check.
4. For multi-tenant: wrap tenant loop around `runMigrations()` body; filter executed IDs per tenant via `TenantContextHolder`.
5. History schema: `migrationId, description, executedAt, durationMs, status(SUCCESS|FAILED), error?`.

## Rules
| Item | Rule |
|------|------|
| id | unique, immutable |
| order | numeric ascending |
| idempotency | history-based skip |
| failure | logged as FAILED, retried on next startup |
| rollback | none — write reverse migration |
| deletion | never delete a committed migration file |

See `content.md` for reference implementation sketch.
