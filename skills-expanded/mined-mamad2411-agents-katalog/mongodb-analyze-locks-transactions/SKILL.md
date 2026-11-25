---
name: mongodb-analyze-locks-transactions
description: Analyze MongoDB concurrency, locks, long-running operations, multi-document transactions, write conflicts, transaction lifetime, and contention. Use for blocked operations, transaction latency, or concurrency incidents.
---

# Analyze Locks and Transactions

1. Identify slow/blocked operations and transaction boundaries.
2. Inspect current operations, lock acquisition/waiting, transaction duration, and write conflicts.
3. Correlate contention with query plans, indexes, document access, and workload concurrency.
4. Evaluate whether transaction scope is larger or longer than business consistency requires.
5. Distinguish lock contention from storage or CPU stalls.
6. Do not terminate production operations without explicit authorization.

## Output
- Blocking/Transaction Evidence
- Contention Source
- Query/Index Correlation
- Application Impact
- Recommended Action
