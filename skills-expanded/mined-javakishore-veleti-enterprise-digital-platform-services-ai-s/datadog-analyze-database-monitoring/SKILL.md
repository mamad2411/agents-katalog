---
name: datadog-analyze-database-monitoring
description: Analyze Datadog Database Monitoring telemetry for query performance, wait time, load, execution behavior, blocking, and database-related application latency. Use when database performance may contribute to an application incident or regression.
---

# Analyze Database Monitoring

1. Resolve database technology, environment, instance, application service, and time window.
2. Inspect query/load telemetry, latency, waits, execution patterns, and relevant database signals available in DBM.
3. Correlate database activity with APM spans and application errors.
4. Identify whether a database symptom is workload-driven, query-specific, capacity-related, or downstream of another event.
5. Route database-specific diagnosis to the relevant `postgres-*`, `mongodb-*`, or `cosmosdb-*` skill where applicable.

## Output
- Database Signals
- Query/Load Findings
- Application Correlation
- Failure Assessment
- Recommended Next Skill
