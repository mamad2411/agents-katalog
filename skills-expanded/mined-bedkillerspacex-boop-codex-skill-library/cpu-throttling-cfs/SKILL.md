---
name: cpu-throttling-cfs
description: >
  Diagnose Linux CFS CPU throttling for owned containers and cgroups v1/v2:
  cpu.max / cpu.cfs_quota_us, throttled periods, hard limits vs requests in
  Kubernetes, and fixing false “CPU not saturated” latency. Use when pods show
  throttling metrics, high latency with low utilization, or noisy-neighbor limits.
---

# CPU Throttling (CFS)

## Scope And Authorization

- **In scope:** Hosts, VMs, and Kubernetes clusters you operate; container cgroup CPU settings you may change under change control.
- **Out of scope:** Deliberately degrading third-party multi-tenant hosts without authorization.
- Prefer staging reproduction; production profile with low overhead tools first.
- Pair limit changes with capacity planning and `code-quality-standards` for app efficiency fixes.

## When To Use

- Latency spikes while container CPU usage graphs look “low” relative to limit.
- Kubernetes `container_cpu_cfs_throttled_seconds` / throttled periods rising.
- Setting or reviewing `resources.limits.cpu` vs `requests.cpu`.
- Differentiating app slowness from CFS quota throttling vs steal time / noisy neighbors.
- cgroup v1 vs v2 metric path differences during node upgrades.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General K8s autoscaling design | HPA/VPA skills |
| Memory OOM / psi memory | memory pressure skills |
| App profiling (CPU hot methods) | language profilers / continuous profiling |
| Completely fair scheduler kernel deep dive for non-container hosts only | kernel performance runbooks |
| Implementation quality baseline | `code-quality-standards` |

## CFS quota basics

| Knob | Meaning |
| --- | --- |
| `cpu.cfs_period_us` / period | Window for quota accounting (often 100ms) |
| `cpu.cfs_quota_us` / `cpu.max` | Allowed CPU time per period; `-1` or `max` = unlimited |
| Throttled | Threads runnable but denied CPU because quota exhausted |
| Request (K8s) | Scheduling guarantee / weight — **not** the same as hard throttle limit |
| Limit (K8s) | Maps to CFS quota — **primary throttle source** |

Example: 100m limit → ~10ms CPU per 100ms period → multi-threaded apps can throttle heavily despite “10% of one core” looking small.

## Workflow

### 1. Confirm scope and success criteria

1. Identify workload, namespace, node pool, and whether limits are set.
2. Success: throttling explained with cgroup evidence; either limits raised, removed, app concurrency reduced, or accepted with docs; latency improved or risk accepted.

### 2. Detect throttling in Kubernetes

```bash
# Metrics (PromQL examples)
# rate(container_cpu_cfs_throttled_seconds_total[5m])
# rate(container_cpu_cfs_throttled_periods_total[5m]) /
#   rate(container_cpu_cfs_periods_total[5m])

kubectl top pod -n NS POD
kubectl get pod -n NS POD -o jsonpath='{.spec.containers[*].resources}{"\n"}'
kubectl describe pod -n NS POD | rg -i 'Limit|Request|Throttle|Kubernetes'
```

### 3. Inspect cgroup on the node (owned node access)

```bash
# Find container cgroup (containerd/docker paths vary)
# cgroup v2 example:
cat /sys/fs/cgroup/path/to/container/cpu.stat
# look for: nr_throttled, throttled_usec
cat /sys/fs/cgroup/path/to/container/cpu.max

# cgroup v1 example:
cat /sys/fs/cgroup/cpu,cpuacct/.../cpu.stat
# nr_throttled, throttled_time
cat /sys/fs/cgroup/cpu,cpuacct/.../cpu.cfs_quota_us
cat /sys/fs/cgroup/cpu,cpuacct/.../cpu.cfs_period_us
```

### 4. Correlate with symptoms

| Symptom | Likely if |
| --- | --- |
| High latency, low “CPU % of limit” | Throttled periods high; multi-thread burst |
| CPU % at 100% of limit | Saturation + throttle (expected under load) |
| Low throttle, high latency | App locks, I/O, GC, downstream — not CFS |
| Only some replicas | Hot keys / uneven traffic / different limits |

Profile app **after** confirming throttle rate; otherwise you optimize the wrong layer.

### 5. Remediation options

1. **Raise or remove CPU limit** (keep request for scheduling); many latency-sensitive services run with request only.
2. **Right-size**: match limit to measured p95 CPU with headroom for bursts.
3. **Reduce threads** / worker pools so the app does not oversubscribe a tiny quota.
4. **Isolate**: dedicated node pools for latency-critical workloads.
5. **CFS period experiments** (advanced, platform-level): rarely first choice; document kernel/runtime support.
6. Fix inefficient code if usage legitimately needs more CPU.

```yaml
# Example: request without limit (cluster policy may forbid — know your standards)
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
  # limits:
  #   cpu: "500m"   # consider removing for latency paths
```

### 6. Verify

```bash
# Before/after: throttled ratio and p99 latency
# Load test in staging with same limits as prod
```

1. Confirm `cpu.max` / quota changed on running cgroup after rollout.
2. Watch for noisy-neighbor regressions if limits removed on multi-tenant nodes.
3. Ensure HPA still behaves (HPA often uses request-based utilization).

### 7. Hand off

1. Document platform policy: when CPU limits are mandatory.
2. Dashboards: throttled ratio panel next to latency.
3. Ticket app owners if thread pools are unbounded.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Diagnosis | cgroup throttle metrics + latency | “CPU is 20%, so not CPU” |
| Limits | Intentional, load-tested | Copy 100m limits everywhere |
| Threads | Bounded pool vs quota | 200 JVM threads on 0.1 CPU |
| Fix | Measure then change one knob | Randomly remove all isolation |
| HPA | Understand util vs request | Max out HPA against wrong metric |

## Output Checklist

- [ ] Workload and resource requests/limits recorded
- [ ] Throttle metrics or cgroup `cpu.stat` evidence captured
- [ ] Correlated with latency/errors
- [ ] Alternative causes checked (I/O, locks, GC)
- [ ] Remediation chosen (limit, request, app, isolation)
- [ ] Staging verification under load
- [ ] Prod change window + rollback
- [ ] Dashboards/alerts updated
- [ ] Cluster policy compatibility checked
- [ ] Residual noisy-neighbor risk noted

## Rules

- CFS throttling can hurt latency long before utilization charts “look full.”
- Do not remove all limits on hostile multi-tenant nodes without platform approval.
- Authorized nodes/clusters only.
- Focus on **CFS quota throttling diagnosis and remediation** for containers.
