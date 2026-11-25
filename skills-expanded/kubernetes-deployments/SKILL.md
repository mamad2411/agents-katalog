---
name: kubernetes-deployments
description: Writes production-ready Kubernetes workloads and debugs them - resource requests and limits, liveness/readiness/startup probes, rolling updates, PodDisruptionBudgets, autoscaling, security context, config and secrets, graceful shutdown, Helm or Kustomize, and kubectl troubleshooting. Use when writing or reviewing Deployment, Service, HPA or Helm/Kustomize manifests, when pods crash, restart, stay Pending or fail readiness, or when a rollout causes errors or downtime.
license: MIT
---

# Kubernetes Deployments

A Deployment that "works" in a demo can still drop requests on every rollout, get OOM-killed under load, and block node upgrades. Every production workload needs: requests, correct probes, a safe rollout strategy, a disruption budget, a restricted security context, and graceful shutdown. **Check the kubectl context before any command, and never apply, delete, scale or roll back in production without explicit confirmation.**

## When to use

- Writing or reviewing Deployments, StatefulSets, Services, HPAs, PDBs, Helm charts or Kustomize overlays.
- Pods in `CrashLoopBackOff`, `Pending`, `ImagePullBackOff`, `OOMKilled`, or failing readiness.
- Errors or dropped connections during rollouts or node drains.

## Safety rules

- Run `kubectl config current-context` (and check the namespace) before anything. Say which cluster you are on.
- Safe without asking: `get`, `describe`, `logs`, `events`, `top`, `kubectl diff`, `--dry-run=server`, `helm template`, `kubectl kustomize`.
- Ask first: `apply`, `delete`, `scale`, `rollout undo`/`restart`, `edit`, `patch`, `drain`, `cordon`, `helm upgrade/uninstall`, `kubectl debug` on production pods, anything touching Secrets. Show `kubectl diff` output with the request.

## Workflow

1. Read the existing manifests/chart and the cluster version (`kubectl version`); features vary by version.
2. Write or change the manifest using the checklist below and [references/hardened-deployment.md](references/hardened-deployment.md) as the baseline.
3. Render and validate: `helm template ...` or `kubectl kustomize <dir>`, then `kubectl apply --dry-run=server -f <file>` (server-side validation against the real API).
4. Preview: `kubectl diff -f <file>` (or `kubectl diff -k <dir>`). Summarize the diff.
5. Apply only after confirmation, then watch: `kubectl rollout status deployment/<name> -n <ns>`.
6. Verify: pods Ready, no restarts climbing, error rate and latency normal.

## Production checklist

### Resources

- [ ] **Requests** for CPU and memory on every container. The scheduler places pods by requests; without them, nodes get overcommitted and HPA CPU targets don't work.
- [ ] **Memory limit** set; commonly equal to the memory request. Exceeding it gets the container OOM-killed (exit code 137).
- [ ] **CPU limit**: a deliberate choice. A CPU limit causes throttling (latency spikes) even when the node is idle. Many teams set CPU requests and omit CPU limits for latency-sensitive services; keep them if the namespace requires them (LimitRange/ResourceQuota) or for noisy batch work.
- [ ] Size from observed usage (`kubectl top pods`, metrics over days), not guesses.

QoS: requests equal limits for all resources of all containers gives `Guaranteed`; some requests gives `Burstable`; none gives `BestEffort` (evicted first).

### Probes

| Probe | Question it answers | On failure | Rule |
| --- | --- | --- | --- |
| `startupProbe` | Has the app finished starting? | Restarts after threshold; holds off the others until success | Use for slow starters instead of a huge `initialDelaySeconds` |
| `readinessProbe` | Can it serve traffic right now? | Removed from Service endpoints; not restarted | May check critical dependencies it can't serve without |
| `livenessProbe` | Is the process stuck beyond recovery? | Container restarted | **Must not check downstream dependencies** (a DB outage would restart every pod); check only the process itself |

- [ ] Separate endpoints (for example `/healthz/live` and `/healthz/ready`), cheap, with no auth.
- [ ] `timeoutSeconds` and `failureThreshold` tolerate a GC pause or brief load spike. A liveness probe that's too aggressive causes restart storms.
- [ ] No liveness probe is better than a wrong one.

### Rollouts

- [ ] `replicas` of at least 2 for anything user-facing (3 across zones for critical services).
- [ ] `strategy.rollingUpdate`: `maxUnavailable: 0` and `maxSurge: 1` (or 25%) for zero-downtime rollouts with small replica counts. Defaults are 25% / 25%.
- [ ] `minReadySeconds` so a pod must stay Ready for a while before the rollout continues.
- [ ] Image pinned to an immutable tag or digest. Never `latest`.
- [ ] **When an HPA manages the Deployment, remove `replicas` from the manifest**, or every apply resets the replica count.
- [ ] `spec.selector` is immutable. Don't change selector labels on an existing Deployment; it needs a new Deployment.

### Disruptions and placement

- [ ] **PodDisruptionBudget** with `maxUnavailable: 1` (or `minAvailable` lower than replicas). Never `minAvailable` equal to replicas: it blocks node drains and cluster upgrades.
- [ ] Spread across zones and nodes: `topologySpreadConstraints` on `topology.kubernetes.io/zone` and `kubernetes.io/hostname` (`maxSkew: 1`, `whenUnsatisfiable: ScheduleAnyway` unless strict spread is required), or preferred pod anti-affinity.
- [ ] PDBs protect only against voluntary disruptions (drains, evictions), not node crashes.

### Autoscaling

- [ ] HPA (`autoscaling/v2`) with `minReplicas` of at least 2 and a sane `maxReplicas` (protect downstream systems and cost).
- [ ] CPU-utilization targets are a percentage of **requests**, so requests must be realistic.
- [ ] Scale on a metric that tracks load (CPU, requests per second, queue depth) and set `behavior.scaleDown` stabilization to avoid flapping.
- [ ] Requires a metrics pipeline (metrics-server for CPU/memory; an adapter for custom metrics).

### Security context

- [ ] Pod: `runAsNonRoot: true`, a non-zero `runAsUser`, `seccompProfile: { type: RuntimeDefault }`.
- [ ] Container: `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true` (mount an `emptyDir` for `/tmp` if needed), `capabilities: { drop: ["ALL"] }`, no `privileged`.
- [ ] `automountServiceAccountToken: false` unless the app calls the Kubernetes API; otherwise a dedicated ServiceAccount with minimal RBAC.
- [ ] Namespace enforces Pod Security Standards (`pod-security.kubernetes.io/enforce: restricted` where possible).
- [ ] NetworkPolicies: default deny, then allow required traffic (requires a CNI that enforces them).

### Config and secrets

- [ ] Config in ConfigMaps, secrets in Secrets, nothing baked into images.
- [ ] Secrets are only base64-encoded. Ensure encryption at rest is enabled, restrict RBAC on Secrets, and prefer an external store (External Secrets Operator, Secrets Store CSI Driver) or Sealed Secrets for GitOps.
- [ ] Pods don't restart when a ConfigMap changes. Environment variables never update; mounted files update eventually (not with `subPath`). Trigger rollouts with a config hash annotation (Helm) or `configMapGenerator` name suffixes (Kustomize).

### Graceful shutdown

On termination the pod is removed from endpoints **at the same time** as SIGTERM is sent, so some traffic can still arrive briefly.

- [ ] The app handles SIGTERM: stop accepting new work, finish in-flight requests, close connections, exit.
- [ ] A short `preStop` delay (a few seconds) so endpoints update before shutdown starts. An `exec` `sleep` needs a `sleep` binary in the image (distroless lacks it); Kubernetes also has a built-in `preStop: { sleep: { seconds: 5 } }` action, run by the kubelet (beta and on by default since 1.30, stable since 1.34; check your cluster version).
- [ ] `terminationGracePeriodSeconds` (default 30) longer than preStop plus the longest request drain.
- [ ] The app runs as PID 1 correctly (exec-form entrypoint; see `dockerfiles`).

### Labels

- [ ] Recommended labels: `app.kubernetes.io/name`, `app.kubernetes.io/instance`, `app.kubernetes.io/version`, `app.kubernetes.io/component`, `app.kubernetes.io/part-of`, `app.kubernetes.io/managed-by`.
- [ ] Selectors use stable labels only (name, instance), never `version`.

## Helm or Kustomize

| | Helm | Kustomize |
| --- | --- | --- |
| Model | Templated charts with values | Plain YAML plus patches and overlays |
| Strength | Packaging and distributing apps, releases with history | Readable diffs, no templating, built into kubectl (`-k`) |
| Weakness | Template logic gets complex; rendered output is hidden | Less suited to distributing configurable packages |
| Use when | Installing third-party software, or shipping a chart to many teams | Your own services with a few environment overlays |

Either way, render to plain YAML (`helm template`, `kubectl kustomize`) and review it; that's what the cluster receives.

## Debugging

| Symptom | Look at | Common causes |
| --- | --- | --- |
| `Pending` | `kubectl describe pod` events | Requests exceed free capacity, node selector/taints, PVC unbound, quota exceeded |
| `ImagePullBackOff` / `ErrImagePull` | `describe pod` | Wrong image name/tag, missing pull secret, registry auth or network |
| `CrashLoopBackOff` | `kubectl logs <pod> --previous` | App error at startup, missing config/env, wrong command, failing liveness probe |
| `OOMKilled` (exit 137) | `describe pod` (Last State), memory metrics | Limit too low or a memory leak |
| `CreateContainerConfigError` | `describe pod` | Referenced ConfigMap/Secret or key doesn't exist |
| Running but `0/1 Ready` | `describe pod` (readiness failures), app logs | Readiness endpoint failing, dependency down, wrong port/path |
| Errors during rollout | `kubectl rollout status`, events, app metrics | No readiness probe, no preStop delay, SIGTERM not handled, `maxUnavailable` too high |

Commands:

```bash
kubectl config current-context
kubectl get pods -n <ns> -o wide
kubectl describe pod <pod> -n <ns>
kubectl logs <pod> -n <ns> -c <container> --previous
kubectl get events -n <ns> --sort-by=.metadata.creationTimestamp
kubectl top pods -n <ns>
kubectl rollout status deployment/<name> -n <ns>
kubectl rollout history deployment/<name> -n <ns>
```

Changing commands (ask first): `kubectl rollout undo deployment/<name> -n <ns>`, `kubectl rollout restart ...`, `kubectl debug -it <pod> --image=busybox --target=<container>` (ephemeral debug container).

## Anti-patterns

- **Liveness probe that checks the database**: one DB blip restarts the whole fleet.
- **No requests**: noisy neighbors, unpredictable scheduling, broken HPA.
- **PDB with `minAvailable` equal to replicas**: node drains hang forever.
- **`replicas` in the manifest plus an HPA**: every deploy scales the service down.
- **`latest` tags**: you can't tell what's running or roll back reliably.
- **Running as root with a writable filesystem** by default.
- **Applying to the wrong cluster** because the context wasn't checked.
- **`kubectl edit` in production** instead of changing the source manifest: drift and lost changes.

## Done when

- Manifests pass `--dry-run=server`, and `kubectl diff` was reviewed with the user before applying.
- Every container has requests, a memory limit, correct probes and a restricted security context.
- Rollouts are zero-downtime (readiness, surge settings, preStop, SIGTERM handling) and a PDB exists.
- After apply: rollout complete, pods Ready, restarts stable, service metrics normal.

## References

- [references/hardened-deployment.md](references/hardened-deployment.md) — read when writing a new Deployment or reviewing one against a complete baseline (Deployment, Service, PDB, HPA, NetworkPolicy).
