---
name: mongodb-analyze-kubernetes
description: Analyze self-managed MongoDB running on Kubernetes, including StatefulSets or supported MongoDB operators, pods, services, PVCs, scheduling, probes, storage, replica/sharded topology, rolling operations, and runtime failures. Use for Kubernetes-hosted MongoDB incidents.
---

# Analyze Kubernetes Deployment

1. Read `.digital-platform-ai/aks.yaml` or Kubernetes context when present.
2. Identify whether MongoDB is deployed through an operator or custom Kubernetes resources.
3. Inspect pods, services, StatefulSets/custom resources, PVCs, scheduling, probes, and recent events.
4. Map Kubernetes resources to replica-set or sharded-cluster roles.
5. Correlate pod restarts, storage/network events, and operator reconciliation with MongoDB state.
6. Route AKS-specific infrastructure issues to `aks-*` skills.
7. Do not manually fight operator reconciliation without understanding ownership.

## Output
- Kubernetes/MongoDB Topology
- Pod/PVC/Operator Evidence
- Database Correlation
- Failure Layer
- Recommended Action
