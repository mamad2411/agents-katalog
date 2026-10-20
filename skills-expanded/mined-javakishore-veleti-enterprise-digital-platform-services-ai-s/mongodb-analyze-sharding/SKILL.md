---
name: mongodb-analyze-sharding
description: Analyze self-managed MongoDB sharded clusters including config server replica sets, mongos routers, shards, metadata, chunk distribution, balancer state, migrations, and cluster health. Use for horizontal-scaling or sharded-cluster incidents.
---

# Analyze Sharding

1. Map config servers, `mongos` routers, shards, databases, collections, and zones.
2. Inspect shard availability, metadata consistency, chunk distribution, and balancer activity.
3. Identify uneven data/traffic distribution and failed or long-running migrations.
4. Correlate routing or metadata problems with application errors.
5. Route shard-key problems to `mongodb-analyze-shard-key`.
6. Do not manually move chunks in production without explicit authorization.

## Output
- Sharded Topology
- Metadata/Balancer State
- Distribution Findings
- Routing/Availability Impact
- Recommended Action
