---
name: kubernetes-operations
description: "Kubernetes operating guidance: resource sizing, probe semantics, affinity, RBAC and NetworkPolicy patterns, autoscaling options, and a catalog of failure modes (Pending pods, OOMKilled, slow rollouts, ImagePullBackOff, CrashLoopBackOff). Use when sizing workloads or diagnosing why a pod will not schedule, start, or stay up."
---

# Kubernetes operations pattern library

## Resource sizing

| Field | What it does |
|---|---|
| `resources.requests.cpu` | Scheduling guarantee — kubelet reserves this |
| `resources.requests.memory` | Same for memory |
| `resources.limits.cpu` | Throttle ceiling — exceeding causes CFS throttling (latency!) |
| `resources.limits.memory` | Hard kill — exceeding = OOMKilled |

**Set requests** at p50 of actual usage. **Set memory limit** at p99 + 20% headroom. **Don't set CPU limit** for latency-sensitive workloads.

## Probe semantics

| Probe | Fail behavior | Use for |
|---|---|---|
| Readiness | Remove from Service endpoints | "Should this receive traffic?" |
| Liveness | Kill + restart pod | "Is the pod alive (not just slow)?" |
| Startup | Delay liveness checks | "Boot time exceeded liveness timeout" |

Common mistake: making liveness == readiness. They serve different purposes; liveness should be lighter (kill pod is a big hammer).

## Affinity patterns

- **Preferred anti-affinity across zones**: spread replicas; preferred so small clusters can still schedule
- **Required anti-affinity for stateful**: one replica per node (DB)
- **TopologySpreadConstraint** (newer than anti-affinity): finer control, better for many pods

## RBAC patterns

| Need | Use |
|---|---|
| Workload reads its own ConfigMap | ServiceAccount + Role + RoleBinding (namespace-local) |
| Workload reads across namespaces | ClusterRole + RoleBinding per namespace (still scoped) |
| Operator that manages CRDs cluster-wide | ClusterRole + ClusterRoleBinding |
| Admin access | Never via bot; humans only via SSO |

## NetworkPolicy patterns

```
1. Default-deny in every namespace (baseline)
2. Allow ingress from named sources (other namespace, named workload)
3. Allow egress to named destinations + DNS
4. Document the policy at each Pod's labels
```

For Cilium/Calico, add L7 rules (HTTP methods, paths, headers).

## Common failure modes catalog

### Pod won't schedule

- Check `kubectl describe pod <name>` for events
- Common: insufficient CPU/memory across all nodes; check requests vs node capacity
- Common: anti-affinity too strict; relax to preferred
- Common: taints on nodes (NoSchedule); add tolerations or untaint

### OOMKilled

- Check memory limit vs actual peak usage
- Check for memory leaks (use `kubectl top pod` + Prometheus)
- Container processes have own OOM scoring; init/sidecar limits differ from main

### Slow rollout

- `maxUnavailable: 0` requires extra capacity; check requests
- Readiness probe taking too long; tune `periodSeconds` + `failureThreshold`
- PDB blocking rollout; check `minAvailable`

### ImagePullBackOff

- Image doesn't exist (typo, wrong tag)
- Registry auth missing (`imagePullSecrets` or IRSA/Workload Identity)
- Rate-limited by Docker Hub (use registry mirror)

### CrashLoopBackOff

- Container exits non-zero; check `kubectl logs --previous`
- Liveness probe failing too early; tune `initialDelaySeconds` or use startup probe
- Bad config / missing env var
- Resource limit too low (OOM immediately on startup)

## Autoscaling

- **HPA**: scales replicas based on metric (CPU/memory/custom)
- **VPA**: adjusts resource requests/limits (rarely used in conjunction with HPA)
- **KEDA**: event-driven autoscaling from queues, streams, schedules
- **Cluster Autoscaler**: adds/removes nodes based on pending pods

Custom metrics > CPU alone for most real workloads.

## Cross-references

- See `terraform-patterns` for cluster + node group provisioning
- See `service-mesh` for L7 traffic management
- See `monitoring-observability` for SLI/SLO/SLA + Prometheus
- See `kubernetes-security` (in LibreSecOps) for Pod Security Standards + admission policies
