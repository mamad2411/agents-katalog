---
name: mongodb-operations-debugging
description: "Diagnose MongoDB incidents involving query plans, indexes, replication, sharding, or backups."
---

# MongoDB Operations Debugging

Debug MongoDB incidents using explain output, index state, profiler or slow query data, replication metrics, shard state, driver config, and recent schema/index changes.

## Trigger boundary

Use this skill when a MongoDB incident involves query plans or indexes, profiler/slow queries, replication or sharding state, driver configuration, backups, or recent schema/index changes.

Do not load it for a small local edit with a deterministic cause and no database query, index, replication, sharding, backup, or operational-state behavior change; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Query optimization; Aggregation pipeline; Connection pooling i konfiguracja drivera
- [02-replication-lag.md](./references/02-replication-lag.md) - Replication lag; Sharding; Shard key; Balancer, chunks i operacje sharded cluster
- [03-observability-i-monitoring.md](./references/03-observability-i-monitoring.md) - Observability i monitoring; Slow query workflow; Storage, system operacyjny i self-managed deployment; Kontenery i MongoDB
- [04-importy-eksporty-i-bulk-operations.md](./references/04-importy-eksporty-i-bulk-operations.md) - Importy, eksporty i bulk operations; Dane tymczasowe, TTL i retencja; Time series collections; Change streams
