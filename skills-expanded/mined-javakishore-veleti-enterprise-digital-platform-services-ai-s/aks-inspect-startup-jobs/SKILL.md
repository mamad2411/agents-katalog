---
name: aks-inspect-startup-jobs
description: Inspect Kubernetes Jobs, init containers, Helm/Argo pre-sync or startup hooks, migration jobs, and other prerequisite workloads that run before or during application pod deployment. Use when pods depend on startup jobs, migrations, bootstrap steps, or deployment hooks.
---

# Inspect Startup Jobs

1. Read service instructions and ops deployment definitions to identify prerequisite jobs, init containers, and hooks.
2. Inspect Job status, completions, failures, backoff, logs, exit codes, and relevant events.
3. Inspect init-container status for blocked pods.
4. For ArgoCD-managed workloads, correlate PreSync/Sync/PostSync hooks with application rollout.
5. Determine whether application pods are waiting on, blocked by, or deployed after a failed prerequisite.
6. Do not rerun jobs or migrations unless explicitly authorized.

## Output
- Startup Prerequisites
- Job/Init Status
- Failure Evidence
- Deployment Impact
- Recommended Action
