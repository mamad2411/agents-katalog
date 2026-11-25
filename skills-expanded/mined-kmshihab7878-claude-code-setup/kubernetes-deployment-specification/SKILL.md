---
name: Kubernetes Deployment Specification
description: Reference for Kubernetes Deployment fields, patterns, and troubleshooting.
---

# Kubernetes Deployment Specification Reference

Comprehensive reference for Kubernetes Deployment resources, covering all key fields, best practices, and common patterns.

## Overview

A Deployment provides declarative updates for Pods and ReplicaSets. It manages the desired state of your application, handling rollouts, rollbacks, and scaling operations.

## When to use this skill

- Authoring or reviewing a Kubernetes `Deployment` manifest.
- Pinning down which Deployment fields are mandatory vs recommended.
- Picking an update strategy (`RollingUpdate` vs `Recreate`) and its parameters.
- Choosing replica count, surge/unavailable budgets, and `revisionHistoryLimit`.
- Setting probes (startup / liveness / readiness), security context, and resource requests/limits.
- Picking a deployment pattern: high-availability, sidecar, init container.
- Diagnosing common Deployment failure modes (`ImagePullBackOff`, `CrashLoopBackOff`, stuck rollouts).

## Reference map

The detailed reference material lives behind pointers so an invocation loads only what it needs.

| When | Read |
|---|---|
| You need a complete annotated `Deployment` manifest (all fields in one place) | [`references/complete-spec.md`](references/complete-spec.md) |
| You need detail on a specific field group | [`references/field-reference.md`](references/field-reference.md) |
| You're picking a deployment pattern (HA, sidecar, init container) | [`references/patterns.md`](references/patterns.md) |
| A Deployment is misbehaving | [`references/troubleshooting.md`](references/troubleshooting.md) |

## Field reference index

| Group | Covers | See |
|---|---|---|
| Metadata fields | required (`name`, `labels` selector parity) + recommended labels/annotations (`app.kubernetes.io/*`) | [`field-reference.md`](references/field-reference.md#metadata-fields) |
| Replica management | `replicas`, `revisionHistoryLimit`, selectors | [`field-reference.md`](references/field-reference.md#replica-management) |
| Update strategy | `RollingUpdate` vs `Recreate`, `maxSurge`, `maxUnavailable`, `minReadySeconds`, `progressDeadlineSeconds` | [`field-reference.md`](references/field-reference.md#update-strategy) |
| Pod template | `template.metadata`, labels parity with selector | [`field-reference.md`](references/field-reference.md#pod-template) |
| Container configuration | image, ports, env, `envFrom`, command/args | [`field-reference.md`](references/field-reference.md#container-configuration) |
| Resource management | `resources.requests` + `resources.limits` for cpu/memory; QoS tiers | [`field-reference.md`](references/field-reference.md#resource-management) |
| Health checks | `startupProbe`, `livenessProbe`, `readinessProbe`; HTTP / TCP / exec / gRPC | [`field-reference.md`](references/field-reference.md#health-checks) |
| Security context | non-root, read-only filesystem, drop capabilities, seccomp | [`field-reference.md`](references/field-reference.md#security-context) |
| Volumes | `configMap`, `secret`, `emptyDir`, `persistentVolumeClaim`, `projected` | [`field-reference.md`](references/field-reference.md#volumes) |
| Scheduling | `nodeSelector`, node affinity, pod (anti-)affinity, tolerations, topology-spread | [`field-reference.md`](references/field-reference.md#scheduling) |

## Common patterns (one-line summaries)

- **High availability** — `replicas: 3+`, `maxUnavailable: 0`, pod anti-affinity by hostname.
- **Sidecar container** — primary app + sidecar container in the same pod (logging, proxy, secrets refresh) with shared `emptyDir` volume.
- **Init container** — run setup or dependency-wait steps before main containers start (DB migrations, fetching config).

Full YAML for each pattern: [`references/patterns.md`](references/patterns.md).

## Production checklist

- [ ] Set resource requests and limits.
- [ ] Implement all three probe types (startup, liveness, readiness).
- [ ] Use specific image tags (not `:latest`).
- [ ] Configure security context (non-root, read-only filesystem).
- [ ] Set replica count `>= 3` for HA.
- [ ] Configure pod anti-affinity for spread.
- [ ] Set appropriate update strategy (`maxUnavailable: 0` for zero-downtime).
- [ ] Use ConfigMaps and Secrets for configuration.
- [ ] Add standard labels and annotations.
- [ ] Configure graceful shutdown (`preStop` hook, `terminationGracePeriodSeconds`).
- [ ] Set `revisionHistoryLimit` for rollback capability.
- [ ] Use ServiceAccount with minimal RBAC permissions.

## Performance tuning

**Fast startup:**

```yaml
spec:
  minReadySeconds: 5
  strategy:
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
```

**Zero-downtime updates:**

```yaml
spec:
  minReadySeconds: 10
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

**Graceful shutdown:**

```yaml
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
        - name: app
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 15 && kill -SIGTERM 1"]
```

## Troubleshooting

Common failure modes — load the full catalog in [`references/troubleshooting.md`](references/troubleshooting.md) when diagnosing:

- **Pods not starting** — `kubectl describe deployment <name>`, then drill into the failing pod (`get pods -l app=<app>`, `describe pod`, `logs`).
- **`ImagePullBackOff`** — wrong image name/tag, missing `imagePullSecrets`, registry credentials.
- **`CrashLoopBackOff`** — application crashes, overly aggressive liveness probe, resource limits, missing dependencies.
- **Rollout stuck in progress** — `progressDeadlineSeconds` exceeded, readiness probe never succeeds, cluster resource pressure.

## Related resources

- [Kubernetes Deployment API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#deployment-v1-apps)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
