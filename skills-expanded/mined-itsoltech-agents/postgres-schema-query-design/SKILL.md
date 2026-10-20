---
name: postgres-schema-query-design
description: "Design PostgreSQL schemas, queries, migrations, indexes, JSONB, pooling, and data access."
---

# Postgres Schema Query Design

Design PostgreSQL around real access patterns, explicit constraints, migration safety, query plans, transaction boundaries, and application persistence needs.

## Process

1. Identify access patterns, trust boundaries, runtime constraints, ownership, and operational requirements before choosing structure.
2. Prefer the simplest design that satisfies current requirements and leaves clear extension points for known near-term changes.
3. Make data flow, failure handling, observability, and rollout constraints explicit.
4. Translate the design into concrete implementation and review checks before coding.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Cel dokumentu; Zasady ogólne; Warstwy odpowiedzialności
- [Shared JSONB and query design](../_shared/references/postgres/jsonb.md) - wspólne fakty dla projektowania JSONB, partycjonowania, indeksów, zapytań i EXPLAIN
- [Shared planner statistics and concurrency](../_shared/references/postgres/planner-statistics.md) - wspólne fakty dla projektowania statystyk, transakcji, blokad, persistence i capacity
- [04-connection-pooling.md](./references/04-connection-pooling.md) - Connection pooling; PgBouncer vs direct connection; PgBouncer i prepared statements; PgBouncer i search_path
- [05-migracje-danych.md](./references/05-migracje-danych.md) - Migracje danych; Bezpieczeństwo; Schematy i uprawnienia; Testy i QA
- [06-procedury-operacyjne.md](./references/06-procedury-operacyjne.md) - Procedury operacyjne; Minimalny zestaw ustawień dla aplikacji
