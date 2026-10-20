---
name: mongodb-inspect-cluster
description: Inspect a self-managed MongoDB deployment across standalone, replica set, or sharded topology, including members, mongos, config servers, shards, storage, security, version, configuration, and runtime health. Use as the primary entry point when the MongoDB failure domain is not yet known.
---

# Inspect Cluster

1. Read `.digital-platform-ai/mongodb.yaml`, service metadata, environments, and relevant instructions.
2. Resolve environment, topology, hosts/pods, replica sets, shards, routers, and application dependencies.
3. Inspect topology, member health, versions, storage engine, authentication, TLS, resource state, and recent changes.
4. For sharded clusters, inspect config servers, `mongos`, shards, shard keys, and balancer state.
5. Identify the likely investigation domain and route to focused `mongodb-*` skills.
6. Do not mutate production configuration unless explicitly authorized.

## Output
- Cluster Context
- Topology
- Runtime State
- Scope Assessment
- Recommended Next Skill
