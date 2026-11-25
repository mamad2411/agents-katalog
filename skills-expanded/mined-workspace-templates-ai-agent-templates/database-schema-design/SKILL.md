---
name: database-schema-design
description: Models entities, keys, relationships and constraints for a new feature, and states the reason for any denormalization before writing DDL.
---

# Database schema design

Start from what the application must ask of the data, not from the UI.

## Steps

1. Write the ten most important reads and writes in plain sentences ("orders for a customer, newest first"). The schema must make these cheap.
2. Name the entities and their relationships: one-to-many, many-to-many (needs a join table), or one-to-one (usually merge them unless the data is optional or large).
3. Choose primary keys. Use a surrogate key (bigint identity or UUID v7) and keep natural identifiers as separate unique columns. Never use an email or name as a key.
4. Pick types carefully: `numeric` for money (or integer cents), `timestamptz` for instants, text with a length check instead of unbounded text where a limit exists, enums via a lookup table or check constraint.
5. Add constraints in the schema: `NOT NULL` by default, foreign keys with an explicit `ON DELETE` choice, `UNIQUE` on every real uniqueness rule, `CHECK` for ranges and states.
6. Normalize to third normal form first. Denormalize only for a named, measured read problem, and then record the source of truth and how the copy stays in sync.
7. Index each foreign key and each query filter from step 1. Do not add speculative indexes.
8. Add `created_at`, `updated_at` and soft delete only where the product needs history.

## Rules

- No comma-separated lists or repeated columns (`tag1`, `tag2`).
- Every denormalized column gets a comment saying why.
- Write the migration as reversible, and check it runs on a copy of production data.

## Report

An ER summary, the DDL, the query-to-index mapping, and each trade-off with its reason.
