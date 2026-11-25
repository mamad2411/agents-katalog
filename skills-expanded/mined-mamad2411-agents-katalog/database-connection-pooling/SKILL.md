---
name: database-connection-pooling
description: Manage database connection pooling. Use when tuning
  application-to-database connection usage.
metadata:
  tags: database, connection, pooling
---

# Database Connections & Pooling

## Use this skill when
- Configuring pool sizes
- Diagnosing connection exhaustion
- Handling timeouts and checkouts

## Do not use this skill when
- Query/schema tuning
- Network-level tuning

## Instructions
1. Size pool to DB connection limits, not arbitrarily large.
2. Balance waiting versus concurrent queries: small pools can beat big ones.
3. Set idle timeout, max lifetime, and checkout timeout.
4. Avoid holding connections during slow external calls.
5. Watch for connection leaks (checkout without return).
6. Use health checks to evict broken connections.
7. Monitor active vs idle vs waiting.

## Checklist
- No leaked connections
- Pool size is justified by limits and workload

## Output Format
- Pool params | workload | limits | risk notes

## Common Mistakes
- Pool of thousands because “more is better”
- Leaks from missing close/return
