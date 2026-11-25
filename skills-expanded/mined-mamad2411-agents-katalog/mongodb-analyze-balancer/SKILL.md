---
name: mongodb-analyze-balancer
description: Analyze MongoDB sharded-cluster balancer behavior, chunk or range migrations, balancing windows, migration failures, resource impact, and uneven distribution. Use for balancer performance or migration incidents.
---

# Analyze Balancer

1. Inspect balancer state, active/recent migrations, collection distribution, and configured windows.
2. Correlate migration activity with network, disk, replication, and application latency.
3. Identify migration failures or persistent imbalance.
4. Distinguish shard-key problems from temporary balancing work.
5. Avoid legacy/manual chunk operations unless the deployed MongoDB version and evidence justify them.
6. Do not stop the balancer in production without explicit authorization.

## Output
- Balancer State
- Migration Evidence
- Resource Impact
- Distribution Findings
- Recommended Action
