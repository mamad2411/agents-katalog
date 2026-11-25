---
name: analyze-database
description: Analyze PostgreSQL behavior for query latency, connection-pool issues, locks, transactions, indexes, schema constraints, and runtime database symptoms. Use when a service investigation involves database errors, slow queries, blocked requests, pool exhaustion, transactional failures, or suspected PostgreSQL contribution to an incident.
---

# Analyze Database

1. Read `.digital-platform-ai/dependencies.yaml`, environment metadata, and service instructions when present.
2. Identify the PostgreSQL database, schema, environment, and affected application path.
3. Inspect available evidence for:
   - query latency
   - connection usage
   - application connection-pool saturation
   - locks and blocking
   - transaction duration
   - query plans
   - index usage
   - constraint or schema failures
4. Correlate database evidence with application logs and traces.
5. Distinguish database-server problems from application connection-pool or transaction-management problems.
6. Do not recommend schema or index changes without supporting evidence.
7. Do not execute mutating SQL unless explicitly authorized.

## Output

Return:

- Database Findings
- Supporting Evidence
- Application vs Database Impact
- Recommended Action
- Remaining Unknowns
