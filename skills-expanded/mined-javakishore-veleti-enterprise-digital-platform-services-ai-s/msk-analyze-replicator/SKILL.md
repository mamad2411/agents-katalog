---
name: msk-analyze-replicator
description: Analyze Amazon MSK Replicator topology, source and target clusters, topic replication, replication lag, naming/configuration, permissions, failover, and DR behavior. Use for managed cross-cluster or cross-region replication.
---

# Analyze MSK Replicator

1. Identify source/target clusters, regions, replicated topics, and intended DR or migration model.
2. Inspect replicator state, replication lag, throughput, and errors.
3. Verify network and IAM prerequisites.
4. Evaluate consumer failover and offset/application implications.
5. Detect replication loops or topology assumptions that can create duplicated flows.
6. Do not initiate production failover without explicit authorization.

## Output
- Replication Topology
- Lag/Health Findings
- Security/Network Findings
- Failover Readiness
- Recommended Action
