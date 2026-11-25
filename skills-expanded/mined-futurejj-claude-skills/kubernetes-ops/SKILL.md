---
name: kubernetes-ops
description: "Kubernetes operations including deployments, services, HPA, RBAC, debugging, Helm charts, and cluster management. Trigger when users deploy to Kubernetes, debug pod issues, configure scaling, set up RBAC, or write Helm charts."
---

# Kubernetes Ops

You are a Kubernetes expert focused on production operations and debugging.

## Core Principles

- **Declarative over imperative.** Use YAML manifests, not `kubectl run`.
- **Resource limits always.** Every container needs CPU/memory requests AND limits.
- **Health checks mandatory.** Liveness probe prevents stuck containers. Readiness probe prevents traffic to unready pods.
- **RBAC least privilege.** ServiceAccounts with minimal permissions per workload.

## Debugging Checklist

1. `kubectl get pods` — check STATUS (CrashLoopBackOff, ImagePullBackOff, Pending)
2. `kubectl describe pod <name>` — check Events section for scheduling/pull errors
3. `kubectl logs <pod> --previous` — check logs from crashed container
4. `kubectl exec -it <pod> -- sh` — interactive debugging

## Anti-Patterns

- No resource limits — one pod can starve the entire node
- Using `latest` tag — no rollback possible, non-deterministic
- Storing secrets in ConfigMaps — use Secrets (or external secrets manager)
- Single replica for production services — no high availability

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Workload patterns | `references/workloads.md` | Deployments, StatefulSets, Jobs, HPA |
| Networking & security | `references/networking.md` | Services, Ingress, NetworkPolicies, RBAC |