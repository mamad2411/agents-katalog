---
name: postgres-diagnose-runtime
description: Diagnose Azure Database for PostgreSQL Flexible Server incidents end-to-end across queries, locks, connections, PgBouncer, compute, storage, HA, replicas, networking, Entra authentication, extensions, and application telemetry. Use when the failing layer is not yet known.
---

# Diagnose Runtime

1. Resolve server, database, environment, application path, time window, and symptom.
2. Gather independent evidence in parallel from Azure/PostgreSQL metrics and logs, query statistics, locks, connections, application telemetry, and recent platform changes.
3. Inspect compute/storage pressure, connection saturation, query latency, blocking, HA/replica state, network, and authentication.
4. Build a timeline around the first confirmed abnormal signal.
5. Separate PostgreSQL engine, Azure managed platform, network, identity, and application causes.
6. Route to focused `postgres-*` skills.
7. Do not treat an application timeout as proof PostgreSQL is the root cause.

## Output
- Incident Scope
- First Confirmed Failure
- Supporting Evidence
- Failing Layer
- Recommended Action
- Remaining Unknowns
