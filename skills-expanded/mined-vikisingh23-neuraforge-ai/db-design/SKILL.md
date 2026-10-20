---
name: db-design
description: Describe your data needs in plain English — get entities, relationships, migrations, and indexes
category: developer-tools
triggers:
  - "design database"
  - "create schema"
  - "design tables"
---

Design database schemas from plain English requirements.

## How to use
Describe your data: "I need users, orders, and payments with relationships"

Generates: entity diagram, TypeORM/EF/Django/JPA entities, migrations, indexes.
Always includes: UUID primary keys, audit fields, soft deletes, version column.

For full instructions, read `agents/db-design.md`.
