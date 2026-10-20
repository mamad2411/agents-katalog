---
name: mongodb-analyze-profiler-telemetry
description: Analyze MongoDB profiler, diagnostic logs, mongostat, mongotop, current operations, and native runtime telemetry to isolate performance and operational anomalies. Use for evidence collection in self-managed MongoDB incidents.
---

# Analyze Profiler and Telemetry

1. Define the investigation time window and symptom before collecting telemetry.
2. Use profiler/current-operation evidence carefully to avoid unnecessary production overhead.
3. Correlate `mongostat`, `mongotop`, server status, and logs with host/application telemetry.
4. Identify query, namespace, connection, replication, or storage patterns.
5. Treat profiler activation or verbosity changes as operational changes requiring authorization.
6. Separate observed telemetry from inference.

## Output
- Telemetry Scope
- Key Runtime Signals
- Correlated Operations
- Evidence Gaps
- Recommended Next Skill
