---
name: mongodb-analyze-upgrade
description: Analyze self-managed MongoDB rolling upgrades across replica sets and sharded clusters, including version compatibility, FCV, driver compatibility, config servers, shards, mongos, rollback planning, and runtime validation. Use for upgrade planning or upgrade-related incidents.
---

# Analyze Upgrade

1. Identify current/target versions, topology, FCV, drivers, operators/automation, and dependencies.
2. Check supported upgrade path and compatibility requirements.
3. For sharded clusters, plan ordering across config servers, shards, and `mongos`.
4. Define health gates before advancing each phase.
5. Plan FCV changes separately from binary rollout.
6. Define rollback before starting.
7. Do not perform production upgrades without explicit authorization.

## Output
- Current/Target State
- Compatibility Findings
- Upgrade Sequence
- Validation/Rollback Gates
- Recommended Plan
