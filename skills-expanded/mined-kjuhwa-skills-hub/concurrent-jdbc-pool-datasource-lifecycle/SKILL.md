---
tags: [backend, concurrent, jdbc, pool, datasource, lifecycle]
name: concurrent-jdbc-pool-datasource-lifecycle
description: Manage a pool of short-lived JDBC targets for monitoring agents with dual maps (active vs all) and periodic revalidation
category: backend
version: 1.0.0
trigger: multi-tenant JDBC agent, per-target connection lifecycle, monitoring pool management
source_project: lucida-domain-dpm
---

# Concurrent JDBC pool lifecycle for monitoring agents

A monitoring agent connects to N targets that go up and down unpredictably. Keep two maps — one for currently-reachable targets, one for all known targets — and rotate between them on a validation timer.

## Shape
- `activeQueryManagerMap`: targets whose last probe succeeded; drive collection from this map.
- `allQueryManagerMap`: superset including failed targets retained for retry.
- Small per-target pool (e.g. `MAX_JDBC_CONNECTIONS = 3`) — monitoring is lightweight, don't exhaust the target.
- Validation tick (e.g. 30s): probe everything in `allQueryManagerMap`; promote on success, demote on failure.

## Steps
1. Wrap the DataSource in a `QueryManager` holding connection metadata, last-probe timestamp, consecutive failures.
2. On "add target": put into `allQueryManagerMap`; probe once; if OK, also put into `activeQueryManagerMap`.
3. Collection loop iterates `activeQueryManagerMap` only — never block the loop on a dead target.
4. A single-threaded validator iterates `allQueryManagerMap` every `VALIDATION_INTERVAL`; promote/demote based on probe result.
5. On remove: close + remove from both maps.
6. Guardrail: never loop `activeQueryManagerMap` inside the validator — promotion/demotion mid-iteration causes ConcurrentModification; snapshot the keyset.
