---
name: aks-inspect-argocd
description: Inspect Argo CD application state for AKS workloads, including sync status, health, target revision, resource drift, hooks, sync waves, failed syncs, and Git-to-cluster differences. Use for GitOps deployment failures, out-of-sync resources, hook failures, or deployment drift.
---

# Inspect ArgoCD

1. Resolve the Argo CD application and environment from service/ops metadata.
2. Inspect sync status, health, target revision, last operation, resource status, hooks, and sync-wave ordering.
3. Compare desired Git revision with live resources.
4. Identify OutOfSync, Degraded, Missing, Progressing, hook, or permission failures.
5. Correlate ArgoCD events with deployment, startup-job, image, and rollout evidence.
6. Do not sync, rollback, or refresh production applications destructively unless explicitly authorized.

## Output
- Application Sync/Health
- Desired vs Live Revision
- Drift/Hook Findings
- Impacted Resources
- Recommended Action
