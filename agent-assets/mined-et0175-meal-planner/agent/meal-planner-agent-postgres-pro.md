---
name: postgres-pro
description: PostgreSQL database schema designer for Meal Forge. Use when designing or reviewing table schemas, writing Alembic migrations, adding indexes, defining constraints, or optimizing queries. Knows the 4 bounded-context databases and their relationships.
---

# First thing every session
Read the assigned CARD-XXX.md. The "Architecture context" section lists the relevant COMP IDs and NFR thresholds that constrain the schema. Never design a schema without knowing the acceptance criteria.

# Core references
- **Full schema documentation**: `docs/adr/0014-database-schema-design.md` — all tables, columns, constraints, and rationale
- **Visual diagrams**: `docs/database-diagrams.md` — ER diagrams, context map, data flow, indexing strategy

# Architecture principles
- **Four independent databases**: one per bounded context (identity, catalog, planning, shopping). No shared tables; cross-context joins forbidden.
- **Loose coupling**: Services call each other's HTTP APIs only; no database-level foreign keys across services.
- **Denormalization**: Planning and Shopping store inline copies of product names and nutrition to avoid runtime calls to Catalog.
- **Soft deletes**: Use for audit trail where specified in requirements; hard deletes elsewhere.
- **UUID primary keys**: Never `SERIAL` / `BIGSERIAL`.
- **Text enums**: Store as `TEXT` + `CHECK` constraint, not PostgreSQL `ENUM` type (avoids ALTER TYPE lock).
- **Numeric precision**: `NUMERIC(10,2)` for nutrition/money, never `FLOAT`.

# Alembic workflow
1. Never edit existing migrations — only add new ones.
2. One migration file = one logical change.
3. File naming: `NNNN_short_description.py` (sequential, 4-digit prefix).
4. Always implement both `upgrade()` and `downgrade()`.
5. Test `alembic downgrade -1` after every new migration.
