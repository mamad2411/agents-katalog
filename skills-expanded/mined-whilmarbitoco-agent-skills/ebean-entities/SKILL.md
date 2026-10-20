---
name: ebean-entities
description: >
  Extends agent's knowledge of mapping Ebean entities: JPA annotations,
  naming conventions, relationships, soft-delete, auditing, and enum mapping.
  Use when designing entity classes or fixing relationship mapping errors.
compatibility: Java 21+
metadata:
  domain: persistence
  level: intermediate
  stack: [java-21, ebean-15]
  version: "1.0.0"
---

# Ebean Entities

Ebean entities are POJOs annotated with `jakarta.persistence.*` and optionally
`io.ebean.annotation.*`. They support lazy loading, dirty checking, and
automatic auditing.

## Concepts

- **`@Entity` + `@Table`** — mark a class as a persistent entity
- **`@Id` + `@GeneratedValue`** — identity column (auto-increment in SQLite)
- **`@ManyToOne` / `@OneToMany`** — relationships with lazy loading by default
- **`@WhenCreated` / `@WhenModified`** — automatic timestamp auditing
- **`@SoftDelete`** — sets a flag instead of deleting the row
- **`@DbEnumValue`** — annotates a method that returns the DB value for an enum; storage type is `VARCHAR` (default) or `INTEGER`
- **`@Index`** — adds database indexes via DDL generation

## Rules

1. Keep entities as plain classes (not records) — Ebean needs setters/field access.
2. Use `@Version` for optimistic locking on concurrent-write entities.
3. Always define `equals()`/`hashCode()` based on the business key or `@Id`.
4. Use `@SoftDelete` instead of physical deletes when data retention matters.
5. Annotate `@ManyToOne` with `@JoinColumn(name = "foreign_key_col")`.
6. Use `@DbEnumValue(storage = DbEnumType.VARCHAR)` for string-stored enums — more readable than ordinals.
7. Keep `FetchType.LAZY` as default; use `EAGER` only when always needed.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- ebean-setup — configuration and server setup
- ebean-queries — type-safe query building
