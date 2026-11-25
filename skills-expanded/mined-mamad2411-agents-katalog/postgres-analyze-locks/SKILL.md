---
name: postgres-analyze-locks
description: Analyze PostgreSQL locks, blocking sessions, deadlocks, long-running transactions, MVCC impact, transaction age, and concurrency on Azure Flexible Server. Use for blocked queries, deadlocks, or transaction contention.
---

# Analyze Locks and Transactions

1. Identify blocked/blocking sessions and transaction boundaries.
2. Inspect lock modes, wait events, transaction age, deadlock evidence, and affected queries.
3. Correlate contention with indexes, query plans, application transaction scope, and deployment changes.
4. Evaluate long-running transactions for vacuum/MVCC side effects.
5. Distinguish lock waits from CPU/storage/network latency.
6. Do not terminate production sessions without explicit authorization.

## Output
- Blocking Graph
- Transaction Evidence
- Contention Source
- Application Impact
- Recommended Action
