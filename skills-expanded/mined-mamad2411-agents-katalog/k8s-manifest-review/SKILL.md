---
name: k8s-manifest-review
description: Reviews and writes Kubernetes / Helm manifests for production-readiness: resource requests/limits, probes, security contexts, PodDisruptionBudgets, standard labels, and validation via kubeconform/conftest. Triggers when authoring or reviewing k8s YAML or Helm charts, or before applying manifests to a cluster.
when_to_use: เขียน/รีวิว Deployment/Service/Helm chart, จะ apply manifest ขึ้น cluster, หรือเช็ค best practice ก่อน merge
---

## When to Use

Invoke this skill when the task involves any of:
- Authoring a new Deployment / StatefulSet / DaemonSet / Service / Ingress / Helm chart.
- Reviewing an existing k8s manifest or Helm chart before merge.
- Anything that will end in `kubectl apply`, `helm install/upgrade`, `kustomize build`, or an Argo/Flux sync.

Do NOT run live `kubectl apply` as part of review. Render and validate offline first. Treat the cluster as the last step the user triggers, not you.

## Steps

Run these in order. For each gate, report PASS / FAIL / N-A with the exact field that is missing — never a vague "looks fine".

**1. Render + structural lint first (fail fast).**
- Plain YAML: `kubeconform -strict -summary -schema-location default -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' manifests/`. `-strict` rejects unknown fields (catches typos like `limts:`).
- Helm: render real values, do not lint the templates blind — `helm template <release> ./chart -f values.yaml | kubeconform -strict -summary -`. Run once per environment values file (dev/staging/prod) since prod often diverges.
- Kustomize: `kustomize build overlays/prod | kubeconform -strict -summary -`.
- Confirm `apiVersion` is GA where one exists (`apps/v1`, `networking.k8s.io/v1`, `policy/v1` for PDB — `policy/v1beta1` is removed in 1.25+).

**2. Resource requests + limits — every container, including initContainers and sidecars.**
- Require `resources.requests.cpu`, `requests.memory`, `limits.memory` on each container. Missing requests => `BestEffort`/`Burstable` => first to be OOM-killed/evicted under pressure.
- Set `limits.memory == requests.memory` (memory is incompressible; bursting then getting OOM-killed is worse than a hard cap).
- Prefer NO `limits.cpu` (or set it generously). A CPU limit throttles via CFS quota and adds tail latency even when the node is idle — request guarantees the floor.
- Flag any limit that is >4x its request (noisy-neighbor / scheduling-lie risk).

**3. Probes — liveness, readiness, startup.**
- `readinessProbe`: required. Without it, traffic hits the pod before it can serve => 502s on rollout.
- `livenessProbe`: required, but must NOT point at the same deep dependency-checking endpoint as readiness. Liveness = "is this process wedged" (cheap, local). A liveness probe that checks the DB will cascade-restart every pod when the DB blips.
- `startupProbe`: required for slow-booting apps (JVM, migrations). Set `failureThreshold * periodSeconds` to cover worst-case boot, so liveness doesn't kill a pod mid-startup.
- Verify `initialDelaySeconds`/`timeoutSeconds`/`failureThreshold` are explicit, not relying on the 1s default timeout (too tight for most HTTP handlers).

**4. securityContext + Pod Security Standards (target `restricted`).**
Pod-level + container-level:
- `runAsNonRoot: true` and an explicit `runAsUser` (non-zero).
- `allowPrivilegeEscalation: false`.
- `readOnlyRootFilesystem: true` (add an `emptyDir` writable mount for `/tmp` and any cache dirs the app actually needs).
- `capabilities.drop: ["ALL"]`; add back only what is provably needed (e.g. `NET_BIND_SERVICE`).
- `seccompProfile.type: RuntimeDefault` (required by PSS restricted).
- Reject `privileged: true`, `hostNetwork`, `hostPID`, `hostIPC`, and `hostPath` mounts unless explicitly justified in the PR.

**5. Availability — PDB + replicas + spread + rollout.**
- `replicas >= 2` for anything serving traffic (a single replica = guaranteed downtime on node drain/upgrade).
- A `PodDisruptionBudget` (`policy/v1`) with `minAvailable` or `maxUnavailable`. Gotcha: `minAvailable: 1` with `replicas: 1` makes the node un-drainable forever — use `maxUnavailable: 1` for replicas of 2-3.
- `topologySpreadConstraints` across `topology.kubernetes.io/zone` (and `kubernetes.io/hostname`) so all replicas don't land on one node/zone.
- `strategy.rollingUpdate` with sane `maxUnavailable`/`maxSurge`; a `Recreate` strategy on a serving Deployment means a hard outage window.

**6. Standard labels + namespace.**
- Apply recommended `app.kubernetes.io/*` labels: `name`, `instance`, `version`, `component`, `part-of`, `managed-by`. Service selectors should target these, not ad-hoc keys.
- `metadata.namespace` set explicitly (never rely on the kubectl context default — a wrong-namespace apply is a silent prod incident).
- Service/Deployment selector labels must match the pod template labels exactly, or the Service routes to zero endpoints (it will NOT error — just black-holes traffic).

**7. Policy gate (conftest / OPA).**
- Run org policy as code: `conftest test --policy policy/ <(helm template ./chart -f values-prod.yaml)`.
- Common deny rules to verify pass: no `:latest` image tags (pin a digest or semver), images from approved registries only, every workload has the gates from steps 2-6.

**8. Emit a checklist report.** One line per gate: `[PASS|FAIL] <gate> — <resource/container> — <missing field or fix>`. Group FAILs at the top. End with the exact commands to re-validate.

## Common Errors

- **`helm lint` passing ≠ valid manifests.** `helm lint` checks template syntax, not the rendered Kubernetes objects. Always pipe `helm template` output through `kubeconform`.
- **kubeconform green but CRDs skipped.** Without `-schema-location` for the CRD catalog, custom resources are silently skipped, not validated. Watch the summary for `skipped` counts.
- **Selector/label drift.** Editing pod template labels without updating the Service/Deployment `selector` leaves the workload running but with zero endpoints. No error is raised — only an empty `kubectl get endpoints`.
- **`readOnlyRootFilesystem: true` with no writable mount.** App crashes on first write to `/tmp`, logs, or cache. Always pair with an `emptyDir`.
- **`minAvailable: 1` + `replicas: 1`.** Blocks `kubectl drain` / node autoscaler / cluster upgrades indefinitely. Catches teams by surprise during a maintenance window.
- **CPU limit causing latency.** Throttling shows as p99 spikes with the node nowhere near saturated. If you see CPU limits on a latency-sensitive service, flag it — remove the limit, keep the request.
- **`livenessProbe` pointed at a downstream dependency.** Turns a transient DB/cache outage into a restart storm across the whole fleet. Liveness must be local-only.
- **`policy/v1beta1` PodDisruptionBudget.** Removed in k8s 1.25+. Manifest renders fine offline against an old schema but fails on apply to a modern cluster.
- **One values file ≠ all environments.** Prod values often disable a probe, change replicas, or add a sidecar. Validate every env's rendered output, not just the default.

## Verify

A manifest is production-ready only when ALL of these are true:
- `kubeconform -strict` passes for every rendered environment with zero `skipped` resources you care about.
- `conftest test` (or the org policy gate) returns zero failures.
- Every container (init + sidecar included) has requests, a memory limit, and the security context from step 4.
- Every serving workload has readiness + liveness probes, `replicas >= 2`, a `policy/v1` PDB, and topology spread.
- No `:latest` tags; images pinned to digest or semver.
- Service selector resolves to a non-empty endpoint set (selector labels == pod template labels).

Report each as a checked line. If you cannot run a validator in this environment, say so explicitly and provide the exact command for the user to run — never claim a manifest is validated when it was only eyeballed.
