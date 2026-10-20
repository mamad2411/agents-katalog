---
name: mongodb-diagnose-runtime
description: Diagnose self-managed MongoDB incidents end-to-end across replica sets, sharding, queries, indexes, WiredTiger, memory, disk I/O, connections, locks, security, Kubernetes, and application evidence. Use when the failing MongoDB layer is unknown.
---

# Diagnose Runtime

1. Resolve cluster, environment, application path, time window, and symptom.
2. Gather independent evidence in parallel from MongoDB status/profiling, logs, host or Kubernetes metrics, and application telemetry.
3. Inspect topology health, elections, connections, query latency, indexes, locks, WiredTiger cache, storage, replication lag, and sharding state.
4. Correlate the first abnormal database signal with application failures.
5. Separate database, host, network, Kubernetes, and application causes.
6. Route to focused `mongodb-*` skills.
7. Do not treat a slow application request as proof MongoDB is the root cause.

## Output
- Incident Scope
- First Confirmed Failure
- Database Evidence
- Failing Layer
- Recommended Action
- Remaining Unknowns
