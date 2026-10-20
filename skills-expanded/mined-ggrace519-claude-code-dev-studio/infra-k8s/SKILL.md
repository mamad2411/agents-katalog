---
name: infra-k8s
description: Kubernetes platform specialist. Owns cluster design, namespaces and RBAC, workload patterns (Deployments, StatefulSets, Jobs), autoscaling, ingress, and GitOps delivery. Auto-invoked for K8s manifest, cluster, controller, or deployment work.
---

# Kubernetes Platform

Kubernetes rewards discipline and punishes drift. Requests/limits, PDBs,
graceful shutdown, and GitOps are the difference between a platform and an
incident factory.

## When to reach for this

- Writing or reviewing workload manifests (Deployment / StatefulSet / Job / CronJob)
- Designing cluster layout: node pools, namespaces, RBAC, quotas, ingress
- Tuning autoscaling (HPA / VPA / Cluster Autoscaler / Karpenter)
- Setting up or restructuring GitOps delivery (Argo CD / Flux) and promotion

## Principles

1. **Requests are promises, limits are guards.** Set requests from observed p95
   usage — they drive scheduling and bin-packing. Set memory limit ≈ request
   (memory is incompressible; overcommit means OOMKill). Consider leaving CPU
   limits off for latency-sensitive services to avoid throttling; CPU is
   compressible and requests already protect neighbors.
2. **A PDB for every production workload.** Nodes drain — upgrades, autoscaler
   consolidation, spot reclaim. Without a PodDisruptionBudget, a routine node
   roll is an outage. `minAvailable: 1` minimum; never a PDB that permits zero
   disruptions on a 1-replica workload (it just blocks the drain instead).
3. **Graceful shutdown is a contract.** Handle SIGTERM; add a `preStop` sleep
   (5–10 s) so endpoint/load-balancer deregistration propagates before the
   process exits; size `terminationGracePeriodSeconds` (default 30 s) to the
   real drain time. In-flight 502s on every deploy trace back here.
4. **GitOps over kubectl.** Cluster state lives in Git; Argo CD / Flux reconciles
   it; humans don't `kubectl apply` to production. Drift is then detectable and
   revertible, and "what changed" has one answer.
5. **NetworkPolicies default-deny.** Deny all ingress/egress per namespace, then
   allowlist the east-west flows each service actually needs. Retrofitting onto
   an open cluster is painful; starting default-deny is cheap.
6. **Probes are not optional.** Readiness gates traffic, liveness restarts
   wedged processes — they are different questions; never point liveness at a
   dependency-checking endpoint or one flaky downstream restarts your whole fleet.

## Production workload skeleton (the parts reviews catch)

```yaml
spec:
  replicas: 3                      # ≥2 + PDB, spread across zones
  template:
    spec:
      terminationGracePeriodSeconds: 45
      topologySpreadConstraints:   # zone spread for multi-AZ resilience
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
      containers:
        - resources:
            requests: { cpu: 250m, memory: 256Mi }   # from observed p95
            limits:   { memory: 256Mi }              # mem limit = request
          readinessProbe: { httpGet: { path: /ready, port: 8080 } }
          livenessProbe:  { httpGet: { path: /healthz, port: 8080 } }
          lifecycle:
            preStop: { exec: { command: ["sleep", "8"] } }
---
apiVersion: policy/v1
kind: PodDisruptionBudget
spec: { minAvailable: 2, selector: { matchLabels: { app: svc } } }
```

## Pitfalls

- HPA scaling on CPU while the real bottleneck is queue depth or memory — scale
  on the saturating signal (custom/external metrics)
- HPA and VPA both managing the same dimension on one workload — they fight
- `latest` image tags or mutable tags in GitOps repos — reconciliation becomes
  non-deterministic; pin digests or immutable tags
- StatefulSets used for things that aren't stateful (slower rollouts, manual PVC
  cleanup) — a Deployment + PVC or external store is usually right
- CronJobs without `concurrencyPolicy: Forbid` and idempotent payloads —
  overlapping runs double-process
- Cluster-admin RBAC handed to CI; scope deploy roles per namespace

---
*Related: `infra-networking` (CNI, ingress, mesh beyond the cluster),
`infra-observability` (cluster + workload metrics), `infra-sre` (SLOs the
rollout strategy must protect), `infra-finops` (bin-packing and node sizing) ·
domain agent: `infra-architect` · output/ADR format: `playbook-conventions`*
