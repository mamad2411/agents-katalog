---
name: postgres-analyze-pgbouncer
description: Analyze Azure PostgreSQL Flexible Server built-in PgBouncer where supported/enabled, including pooling mode, client/server connections, saturation, transaction/session semantics, prepared statements, and application behavior. Use for high-concurrency connection pooling incidents.
---

# Analyze PgBouncer

1. Confirm PgBouncer support and configuration for the deployed Flexible Server.
2. Identify pool mode, client concurrency, server connection limits, and application pool settings.
3. Inspect pool saturation, waits, connection churn, and transaction/session assumptions.
4. Evaluate compatibility with prepared statements and session-level features for the selected pool mode.
5. Distinguish PgBouncer saturation from PostgreSQL connection or application pool problems.
6. Do not change production pool settings without explicit authorization.

## Output
- Pool Configuration
- Client/Server Connection State
- Compatibility Findings
- Bottleneck
- Recommended Action
