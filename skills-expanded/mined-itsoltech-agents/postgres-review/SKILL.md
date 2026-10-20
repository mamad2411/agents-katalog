---
name: postgres-review
description: "Review PostgreSQL changes to schemas, migrations, queries, indexes, RLS, pooling, or rollback."
---

# Postgres Review

Review database changes for integrity, plan quality, migration safety, concurrency, tenant isolation, operational impact, and rollback or roll-forward readiness.

## Trigger boundary

Use this skill when a PostgreSQL diff changes schemas or migrations, queries/indexes/plans, RLS or tenant isolation, pooling, backups, concurrency, or rollback/roll-forward behavior.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no PostgreSQL schema, query, security, migration, or operational impact; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Cel dokumentu; Zasady ogólne; Warstwy odpowiedzialności
- [Shared JSONB and query design](../_shared/references/postgres/jsonb.md) - wspólne fakty; użyj ich jako review rubryku dla JSONB, partycjonowania, indeksów, zapytań i EXPLAIN
- [Shared planner statistics and concurrency](../_shared/references/postgres/planner-statistics.md) - wspólne fakty; użyj ich jako review rubryku dla statystyk, transakcji, blokad i capacity
- [04-connection-pooling.md](./references/04-connection-pooling.md) - Connection pooling; PgBouncer - tryby pracy; PgBouncer vs direct connection; PgBouncer i prepared statements
- [05-pgbouncer-konfiguracja-i-monitoring.md](./references/05-pgbouncer-konfiguracja-i-monitoring.md) - PgBouncer - konfiguracja i monitoring; PgBouncer - edge case'y produkcyjne; Migracje schematu; Migracje danych
- [06-point-in-time-recovery.md](./references/06-point-in-time-recovery.md) - Point-in-time recovery; Replikacja fizyczna i HA; Load balancing; Bezpieczeństwo
- [07-monitoring.md](./references/07-monitoring.md) - Monitoring; Logowanie; Testy i QA; Scenariusze testowe dla edge case'ów
- [Shared operational procedures](../_shared/references/postgres/operational-procedures.md) - wspólne procedury i SQL; oceniaj konkretne ryzyko rollout/incident/rollback
- [Shared minimum application settings](../_shared/references/postgres/minimum-application-settings.md) - wspólne ustawienia i komendy PgBouncer; traktuj jako rubryk, nie automatyczny nakaz zmiany
- [10-checklist-do-code-review.md](./references/10-checklist-do-code-review.md) - Checklist do code review
