---
name: diagram-ai
description: Create, update, validate, format, sync, and export dbdiagram.io DBML database diagrams. Use when the user asks for database diagrams, DBML files, dbdiagram.io workflows, SQL-to-DBML conversion, DBML-to-SQL conversion, Prisma schema export, Flyway migrations, Liquibase changelogs, or optional dbdiagram.io cloud sync.
---

# diagram-ai

Use this skill to manage dbdiagram.io diagrams with DBML as the source of truth.

## When to Use

- User asks for database diagrams, DBML files, or dbdiagram.io workflows
- SQL-to-DBML or DBML-to-SQL conversion
- Prisma schema export, Flyway migrations, or Liquibase changelogs from DBML
- Optional dbdiagram.io cloud sync (pull/push)

## Workflow

- Create or update `.dbml` files first.
- Read existing `.dbml` files before editing.
- Preserve tables, relationships, notes, enums, indexes, table groups, diagram views, and layout-related content unless the user asks to remove them.
- Prefer local file mode unless the user explicitly enables dbdiagram.io API sync.
- Validate DBML before reporting that a diagram is ready.
- Export SQL, Prisma, Flyway, or Liquibase artifacts only from DBML.

## DBML Guidance

- Include a `Project` block for new diagrams.
- Use valid dbdiagram.io DBML syntax.
- Include primary keys, foreign keys, indexes, enums, and notes when useful.
- Prefer short-form refs such as `Ref: orders.user_id > users.id`.
- Use explicit join tables for physical many-to-many schemas.
- Use `TableGroup` and `DiagramView` for larger schemas.

## CLI Commands

Use these commands when they fit the task:

```bash
dbdiagram-ai-create --prompt "Create ecommerce database diagram" --out database.dbml
dbdiagram-ai-update database.dbml --prompt "Add payment and shipment tables"
dbdiagram-ai-validate database.dbml
dbdiagram-ai-format database.dbml
dbdiagram-ai-from-sql schema.sql --out database.dbml
dbdiagram-ai-pull --diagram-id <id> --out database.dbml
dbdiagram-ai-push database.dbml --diagram-id <id>
dbdiagram-ai-export-sql database.dbml --out schema.sql --dialect postgres
dbdiagram-ai-export-prisma database.dbml --out prisma/schema.prisma
dbdiagram-ai-export-flyway database.dbml --out db/migration --version 1 --name init_schema --dialect postgres
dbdiagram-ai-export-liquibase database.dbml --out db/changelog/db.changelog-master.yaml --format yaml
```

## MCP

When MCP is configured, prefer the `dbdiagram-ai` MCP tools for structured file reads, writes, validation, formatting, conversion, cloud pull/push, and exports.

## Safety

- Never overwrite an existing DBML file without reading it first.
- Never overwrite Flyway migration files unless `--force` is explicit.
- Never expose `DBDIAGRAM_API_TOKEN`.
- Keep cloud sync optional and disabled unless configured.

## Preview

Save local diagrams as `.dbml`. The user can preview them with the official dbdiagram.io VS Code extension or dbdiagram.io.

## Instructions

- Create or update `.dbml` files first; read existing `.dbml` files before editing
- Preserve tables, relationships, notes, enums, indexes, table groups, diagram views, and layout content unless the user asks to remove them
- Prefer local file mode unless the user explicitly enables dbdiagram.io API sync
- Include a `Project` block for new diagrams; use valid DBML syntax with PKs, FKs, indexes, enums, and notes when useful
- Validate DBML before reporting a diagram ready; export SQL, Prisma, Flyway, or Liquibase only from DBML
- Never overwrite an existing DBML file without reading it first; never overwrite Flyway migrations unless `--force` is explicit
- Never expose `DBDIAGRAM_API_TOKEN`
