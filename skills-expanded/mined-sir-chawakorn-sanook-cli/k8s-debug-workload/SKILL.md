---
name: k8s-debug-workload
description: Systematically diagnoses live Kubernetes workload failures — CrashLoopBackOff, ImagePullBackOff, OOMKilled, pending pods, failing probes — by gathering describe/logs/events/node status and isolating root cause. Triggers when a pod won't start, keeps restarting, or a deployment is stuck/unhealthy in a cluster.
when_to_use: pod CrashLoopBackOff/ImagePullBackOff/OOMKilled/Pending, probe fail, rollout ค้าง, service ไม่มา endpoint
---

## When to Use

A live K8s workload is broken and you have `kubectl` access. Specifically:

- Pod stuck `Pending`, `ContainerCreating`, `Init:*`, or `Terminating`
- Pod `CrashLoopBackOff`, `Error`, `OOMKilled`, or restart count climbing
- `ImagePullBackOff` / `ErrImagePull` / `InvalidImageName`
- Readiness/liveness/startup probe failing — pod `Running` but `0/1 READY`
- `kubectl rollout` stuck, deployment shows old + new ReplicaSet both alive
- Service has no endpoints / traffic 503s even though pods look up

Do NOT use for: writing new manifests from scratch, Helm chart authoring, cluster provisioning. This skill is for diagnosing something already deployed.

## Steps

**0. Pin the target. Never debug "the cluster" — debug one object.**
```
kubectl get pods -n <ns> -o wide          # find the bad pod, note NODE + IP
kubectl get deploy,rs,pod -n <ns> -l app=<x>   # see the ownership chain
```
Always pass `-n <ns>` explicitly. Default namespace is a trap. Grab the exact pod name (`<deploy>-<rs-hash>-<rand>`) for everything below.

**1. Read the symptom from `STATUS` + `RESTARTS`, then branch. Do not guess — the status string already names the failure layer:**

| STATUS | Layer | Jump to |
|---|---|---|
| `Pending` | scheduling / quota | Step 4 |
| `ContainerCreating` stuck | volume / CNI / image | Step 2 + Step 4 |
| `ImagePullBackOff`/`ErrImagePull` | image / registry auth | Step 2 |
| `CrashLoopBackOff`/`Error` | container exits | Step 3 |
| `OOMKilled` (in RESTARTS detail) | memory limit | Step 3 + Step 4 |
| `Running` but `0/N READY` | probe / app slow-start | Step 5 |
| Pod fine, Service 503 | endpoints / selector / port | Step 6 |

**2. Always start with `describe` — events are the highest-signal source and most people skip them.**
```
kubectl describe pod <pod> -n <ns>
```
Read the bottom `Events:` block first. It literally prints `Failed to pull image`, `0/3 nodes available: insufficient memory`, `Liveness probe failed: ...`. Then for image pulls:
- `ErrImagePull` + `not found` → wrong tag/repo. Check `Image:` field vs what was actually pushed.
- `ErrImagePull` + `unauthorized`/`denied` → missing/expired `imagePullSecrets`. Verify: `kubectl get sa <sa> -n <ns> -o jsonpath='{.imagePullSecrets}'` and that the secret exists + is type `kubernetes.io/dockerconfigjson`.
- `InvalidImageName` → typo / bad chars in image string.
- Stuck `ContainerCreating` with no pull error → volume mount or CNI, go to Step 4.

**3. For crashes, get BOTH current and previous logs — the crash output lives in `--previous`.**
```
kubectl logs <pod> -n <ns> --previous --tail=200       # the run that died
kubectl logs <pod> -n <ns> --tail=100                  # current attempt
kubectl logs <pod> -n <ns> -c <container> --previous   # if multi-container/init
```
Then decode the exit:
```
kubectl get pod <pod> -n <ns> -o jsonpath='{.status.containerStatuses[*].lastState.terminated}'
```
Read `reason` + `exitCode`:
- `OOMKilled` → real memory cap hit. Go to Step 4 for limits. Bump `resources.limits.memory` or fix the leak — do NOT just raise the limit blindly if RSS grows unbounded.
- exit `137` → SIGKILL (OOM or failed liveness kill). Cross-check `Events` for `Liveness probe failed`.
- exit `143` → SIGTERM, usually probe-triggered restart or graceful shutdown loop.
- exit `1`/`2` + app stack trace in `--previous` → app bug / bad config. Check env vars + mounted ConfigMap/Secret are present: `kubectl exec <pod> -- env` won't work if crashing, so read the manifest's `envFrom`/`valueFrom` and confirm the referenced ConfigMap/Secret exists.
- exit `0` looping → app runs to completion then restarts; wrong `restartPolicy` or missing long-running command.
- CrashLoop with empty logs → fails before logging; check `command`/`args` override, entrypoint, or missing config file mount.

**4. For `Pending`/OOM, check scheduling constraints and node pressure — the scheduler tells you exactly why in events.**
```
kubectl describe pod <pod> -n <ns> | grep -A10 Events    # "0/N nodes available: ..."
kubectl describe node <node>                             # Allocatable, Taints, pressure
kubectl top pod <pod> -n <ns>; kubectl top nodes         # needs metrics-server
```
Match the scheduler reason:
- `insufficient cpu/memory` → requests too high vs `Allocatable`, or nodes full. Lower `requests` or scale nodes.
- `node(s) had untolerated taint` → pod lacks matching `tolerations`. Check `Taints:` on node.
- `didn't match node affinity/selector` → `nodeSelector`/`affinity` points at labels no node has.
- `had volume node affinity conflict` → PV is zone-locked, pod scheduled to wrong zone.
- `pod has unbound immediate PersistentVolumeClaims` → PVC `Pending`: `kubectl get pvc -n <ns>` then `describe pvc` (usually no provisioner / no matching StorageClass).
- Node shows `MemoryPressure`/`DiskPressure True` → node-level, not pod-level; evictions incoming.

**5. For `Running` but not `READY`, the probe config is wrong far more often than the app.**
```
kubectl describe pod <pod> -n <ns> | grep -iA3 -e Liveness -e Readiness -e Startup
kubectl get pod <pod> -n <ns> -o jsonpath='{.spec.containers[*].readinessProbe}'
```
Check, in order:
- Probe `path`/`port` actually served by the app? Wrong port = permanent fail. Confirm against `containerPort` and what the app binds.
- `initialDelaySeconds` too short for slow boot → use a `startupProbe` instead of inflating liveness delay.
- Probe hits a path requiring auth → returns 401/403, counts as fail; use a dedicated unauthenticated `/healthz`.
- From inside (if it stays up): `kubectl exec <pod> -n <ns> -- wget -qO- localhost:<port><path>` to reproduce what kubelet sees.
- Liveness too aggressive → kills a healthy-but-busy pod, looks like CrashLoop (exit 137/143). Relax `timeoutSeconds`/`failureThreshold`.

**6. For "pod up but Service dead", verify the selector→endpoint chain — a 503 with healthy pods is almost always a selector or port mismatch.**
```
kubectl get endpointslices -n <ns> -l kubernetes.io/service-name=<svc>   # EMPTY = broken
kubectl get svc <svc> -n <ns> -o wide
kubectl describe svc <svc> -n <ns>
```
- Empty endpoints → Service `selector` labels don't match pod labels (`kubectl get pod --show-labels`), OR pods aren't `READY` (go to Step 5 — unready pods are excluded from endpoints).
- Endpoints present but traffic fails → Service `targetPort` ≠ container's listening port. Confirm `targetPort` maps to the real `containerPort`/app port.
- DNS: `kubectl run tmp --rm -it --image=busybox -n <ns> -- nslookup <svc>` to confirm resolution; check `kube-dns`/CoreDNS pods are up if it fails.
- `NetworkPolicy` silently dropping traffic: `kubectl get netpol -n <ns>` — a default-deny with no matching allow rule blackholes connections with no error.

**7. Propose ONE narrow fix, name the exact field changed, and give a verify command. Don't shotgun multiple changes at once — you won't know which one worked.**

## Common Errors

- **Skipping `--previous`** — `kubectl logs <pod>` on a crashlooping pod shows the *current* (already-restarted, possibly empty) attempt. The actual crash output is in `--previous`. This is the #1 missed clue.
- **Trusting `kubectl logs` when the pod never started** — Init containers and pre-entrypoint failures produce no app logs; the answer is in `describe` Events, not logs.
- **Raising the memory limit to "fix" OOMKilled** — if RSS grows unbounded it's a leak; a higher limit just delays the kill and masks the bug. Confirm steady-state vs leak via `kubectl top pod` over time before touching limits.
- **Confusing liveness vs readiness** — a failing *readiness* probe takes the pod out of Service endpoints (traffic stops) but does NOT restart it. A failing *liveness* probe *restarts* it (exit 137/143, looks like a crash). The fix differs: readiness = app not ready / wrong probe; liveness = probe too aggressive or app hung.
- **Forgetting unready pods are excluded from endpoints** — a "Service has no endpoints" bug is frequently a probe problem in disguise (Step 5), not a selector problem.
- **`top` returns error** — needs metrics-server installed; if absent, read `resources` requests/limits from the manifest and node `Allocatable` from `describe node` instead.
- **Editing the live pod instead of the controller** — `kubectl edit pod` changes get wiped on the next restart. Patch the Deployment/StatefulSet (`kubectl set resources` / `kubectl edit deploy`) so the change survives.
- **`ContainerCreating` blamed on the image** when it's actually a stuck PVC or CNI — check Events for `FailedMount`/`FailedAttachVolume` vs pull errors; they look similar from the outside.
- **Ignoring the ownership chain** — restarting a single pod when the Deployment template is the bug just respawns the same broken pod. Fix the template, then `rollout restart`.

## Verify

After applying a fix, confirm with a runnable check — never declare done on "looks fixed":

```
kubectl rollout status deploy/<name> -n <ns> --timeout=120s   # waits, exits non-zero on fail
kubectl get pods -n <ns> -l app=<x> -w                        # watch RESTARTS stay 0, READY = N/N
```
Then re-confirm the original symptom is gone:
- Crash fixed → `RESTARTS` stops climbing for ≥2 min and `lastState.terminated` is no longer present.
- Image fixed → STATUS leaves `ImagePullBackOff`, reaches `Running`.
- Pending fixed → pod has a `NODE` assigned in `-o wide`.
- Probe fixed → `READY` shows `N/N`, no new `probe failed` events.
- Service fixed → `kubectl get endpointslices -n <ns> -l kubernetes.io/service-name=<svc>` lists pod IPs, and a request from an in-cluster `busybox` pod succeeds.

If the verify command fails, do NOT relax the probe/assertion or bump a limit to force green — go back to the matching step and find the real cause.
