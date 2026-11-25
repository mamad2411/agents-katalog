---
name: postgres-operations-debugging
description: "Diagnose PostgreSQL incidents involving plans, locks, pooling, replication, vacuum, or recovery."
---

# Postgres Operations Debugging

Debug PostgreSQL incidents with evidence from plans, locks, connections, logs, metrics, replication state, vacuum state, and recent migrations before changing settings.

## Trigger boundary

Use this skill when a PostgreSQL incident involves query plans, locks or connections, PgBouncer, logs/metrics, replication or HA state, vacuum, recovery, or recent migrations.

Do not load it for a small local edit with a deterministic cause and no database plan, lock, connection, replication, recovery, vacuum, migration, or operational-setting behavior change; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; EXPLAIN i analiza planów; Statystyki plannerowe; Blokady i współbieżność
- [02-pgbouncer-tryby-pracy.md](./references/02-pgbouncer-tryby-pracy.md) - PgBouncer - tryby pracy; PgBouncer vs direct connection; PgBouncer i prepared statements; PgBouncer i search_path
- [03-pgbouncer-konfiguracja-i-monitoring.md](./references/03-pgbouncer-konfiguracja-i-monitoring.md) - PgBouncer - konfiguracja i monitoring; PgBouncer - edge case'y produkcyjne; Direct connection - kiedy omijać PgBouncer; Backupy
- [04-patroni-i-automatyczny-failover.md](./references/04-patroni-i-automatyczny-failover.md) - Patroni i automatyczny failover; Load balancing; Replikacja logiczna; Sharding i rozproszenie danych
- [05-monitoring.md](./references/05-monitoring.md) - Monitoring; Logowanie
- [06-rozwiazywanie-problemow.md](./references/06-rozwiazywanie-problemow.md) - Rozwiązywanie problemów; Upgrade'y; Kontenery i Nomad
- [Shared operational procedures](../_shared/references/postgres/operational-procedures.md) - wspólne procedury i SQL; w debugowaniu zaczynaj od symptomów i aktualnego stanu
- [Shared minimum application settings](../_shared/references/postgres/minimum-application-settings.md) - wspólne ustawienia i komendy PgBouncer; nie zmieniaj konfiguracji bez dowodu z diagnostyki
