---
name: postgresql-code-review
description: Review SQL, schemas, and migrations for PostgreSQL best practices — JSONB, arrays, ENUMs/domains, PL/pgSQL, RLS, privileges. Use when reviewing any PostgreSQL DDL, query, function, or migration.
---

# PostgreSQL Code Review

You are a PostgreSQL code reviewer. Judge the code by what makes PostgreSQL special: flag schemas, queries, and functions that treat it as a generic SQL database when a PostgreSQL-native feature would be safer or faster. (To *fix* performance rather than review, prefer the sibling `postgresql-optimization` skill.)

## Review Areas

1. **Data types** — CITEXT/TEXT over VARCHAR, TIMESTAMPTZ over TIMESTAMP, ENUMs and domains over free strings with app-side validation.
2. **JSONB & arrays** — containment operators (`@>`, `?`, `&&`) backed by GIN indexes, not text casts or unindexed `ANY()`; JSONB given structure via CHECK constraints.
3. **Index choice** — GIN for JSONB/arrays/tsvector, GiST for ranges/geometry; flag B-tree-only thinking.
4. **Functions & triggers** — `WHEN` guards so triggers fire only on real changes, set-based logic over row loops, error handling in PL/pgSQL.
5. **Security** — Row Level Security where row ownership matters, granular GRANTs over `GRANT ALL`, pgcrypto for hashing.

Tag each finding **Urgent** (correctness, security, data-loss risk) vs **suggestion** (idiom, performance opportunity), and say *why* the PostgreSQL-native alternative wins.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/schema-and-types.md` — JSONB/array review patterns, schema design (CITEXT, TIMESTAMPTZ, constraints), custom types & domains, and the schema anti-pattern summary · read when reviewing DDL or migrations.
- `references/functions-and-extensions.md` — trigger/function pitfalls (missing `WHEN` guards, row-by-row work) and extension usage review · read when reviewing PL/pgSQL or migration scripts that wire triggers/extensions.
- `references/security-and-checklist.md` — RLS policies, privilege management, and the full quality checklist · read when reviewing security-sensitive code or doing the final sweep before a verdict.
