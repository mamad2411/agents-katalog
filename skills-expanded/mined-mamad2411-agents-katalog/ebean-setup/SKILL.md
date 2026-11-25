---
name: ebean-setup
description: >
  Extends agent's knowledge of configuring Ebean ORM in a Maven project:
  dependencies, entity scanning, server configuration, and programmatic setup.
  Use when adding Ebean to a new project or troubleshooting startup errors.
compatibility: Java 21+
metadata:
  domain: persistence
  level: beginner
  stack: [java-21, ebean-15, maven-3.9]
  version: "1.0.0"
---

# Ebean Setup

Ebean is a JPA-compatible ORM with a simpler API, compile-time query generation,
and first-class Maven integration via the `ebean-maven-plugin`.

## Concepts

- **ebean-starter** — Spring-Boot-free bundle that pulls in the right ebean dependencies
- **ebean-ddl-generator** — generates `migration-*.ddl` files from entity classes
- **ServerConfig** — programmatic configuration (DataSource, entity packages, DDL mode)
- **ebean.mf** — manifest file for entity scanning (alternative to package-level annotation)
- **DDL modes** — `none`, `dropCreate`, `migrations`, `create` — pick per environment

## Rules

1. Use `ebean-starter` for dependency management — don't wire individual modules.
2. Configure `ServerConfig` in code, not XML. Constructor-inject DataSource.
3. Scan only packages that contain entities — disable `runWithScanner=false` for production.
4. Use `DbMigration` API or `ebean-ddl-generator` to generate migration scripts, not `ddl.generate`/`ddl.run` (those produce create-all DDL, not migrations).
5. Use `ddl.migration.version` with semantic versioning for migration file names.
6. Register all entity classes explicitly via `addPackage()` or `@Entity` + scanning.
7. Set `defaultServer(true)` on your primary DataSource-backed config.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- ebean-entities — entity mapping and conventions
- ebean-queries — type-safe query building
- database-migrations — migration management
