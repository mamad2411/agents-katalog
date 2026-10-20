---
name: aks-inspect-cluster
description: Inspect AKS cluster context, node pools, health, capacity, Kubernetes version, scheduling pressure, and cluster-level signals. Use when an investigation must identify the correct AKS cluster or determine whether cluster-level conditions contribute to a service issue.
---

# Inspect Cluster

1. Read `.digital-platform-ai/aks.yaml` and environment metadata when present.
2. Resolve the target environment to the correct AKS cluster.
3. Inspect cluster and node-pool health, version, capacity, pressure, scheduling conditions, and recent cluster-level events.
4. Identify whether the issue is service-scoped, namespace-scoped, node-scoped, or cluster-scoped.
5. Do not mutate cluster configuration unless explicitly authorized.

## Output
- Cluster Context
- Node/Capacity Findings
- Cluster-Level Evidence
- Scope Assessment
- Recommended Next Skill
