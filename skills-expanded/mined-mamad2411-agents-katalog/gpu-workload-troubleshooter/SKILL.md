---
name: gpu-workload-troubleshooter
description: >-
  Decision-tree diagnosis for GPU workloads on Kubernetes: pods stuck Pending
  with Insufficient nvidia.com/gpu, FailedScheduling, missing device plugin
  signatures, nodes that launch but never register GPUs, node pools that won't
  scale, unhealthy GPU hardware (AcceleratedHardwareReady false),
  CrashLoopBackOff during slow model loads, and OOMKilled vs CUDA
  out-of-memory. Use whenever the user reports a pod pending, GPU not
  detected, "0/N nodes are available", nvidia.com/gpu not allocatable,
  scheduling failures, taint/toleration mismatches, node autoscaler not
  reacting, NodeClaim stuck, gpu resource not registered, exit code 137,
  liveness probe killing an inference server, CUDA OOM, or "it worked
  yesterday". Includes kubectl commands per step. For designing (rather than
  debugging) autoscaling use sibling gpu-autoscaling-engineer; for sharing
  semantics use gpu-sharing-advisor; for quota rejections at creation see
  researcher-tenancy-provisioner.
---

# GPU Workload Troubleshooter

## Purpose
Walk a broken GPU workload from symptom to root cause along a fixed decision tree, with the exact command at each step — instead of the usual flailing between "add more tolerations" and "delete the node". Built for research clusters on managed K8s (Lambda): hardware and node-image layers escalate to the provider with evidence; everything above is yours to fix.

## Core model to hold in your head

**The GPU scheduling chain** — every failure is a broken link; find the link, not the symptom:

```
driver on node → container toolkit → device plugin DaemonSet registers nvidia.com/gpu with kubelet
→ node advertises allocatable GPUs → scheduler matches pod (limits + tolerations + selectors/affinity)
→ [if no fit: autoscaler provisions a node whose pool constraints intersect the pod's requirements]
→ kubelet + device plugin allocate the device → container starts → model loads → probes pass
```

**Extended-resource semantics you must hold**: GPUs are non-fractionable extended resources; set them in `limits` (requests auto-set equal — differing values are a validation error; requests-only is invalid). No overcommit. A GPU is reserved for the pod's whole lifecycle even if idle. Under time-slicing/MIG the *unit* changes (virtual GPU / slice) but the semantics don't — `nvidia.com/gpu: 10` allocatable on a 1-GPU node means time-slicing is active (gpu-sharing-advisor).

**Two different "won't run" families**: rejected at *creation* (`Forbidden: exceeded quota` — a ResourceQuota admission failure; fix quota or request, see researcher-tenancy-provisioner) vs stuck *Pending* after creation (scheduling — this tree).

## The decision tree

### 1. Pod is Pending
```
kubectl describe pod <pod> | grep -A5 Events
kubectl get pod <pod> -o jsonpath='{.status.conditions[?(@.type=="PodScheduled")]}'
```
Branch on the FailedScheduling message:

**A. `Insufficient nvidia.com/gpu`** (e.g., `0/2 nodes are available: 2 Insufficient nvidia.com/gpu`). Check what nodes actually advertise:
```
kubectl get nodes -o custom-columns=NAME:.metadata.name,GPUs:.status.allocatable."nvidia\.com/gpu"
kubectl get node <gpu-node> -o jsonpath='{.status.allocatable}' | jq .
```
- **Allocatable shows 0 / field absent on a GPU node → device plugin problem.** The #1 signature. Verify the DaemonSet exists, is scheduled on that node, and is healthy:
  ```
  kubectl get ds -A | grep -i -e nvidia -e device-plugin
  kubectl get pods -n <plugin-ns> -o wide | grep <node>
  kubectl logs -n <plugin-ns> <plugin-pod>
  ```
  Common causes: plugin DaemonSet's nodeSelector/tolerations don't match the node; node image lacks the NVIDIA driver/toolkit (ask Lambda which node images are GPU-enabled); plugin crashed after a driver upgrade. No device plugin = scheduler is blind to GPUs no matter what the hardware has.
- **Allocatable > 0 but all consumed → capacity.** `kubectl describe node <node> | grep -A8 "Allocated resources"` shows GPU requests vs capacity. Either autoscaling should add nodes (branch D) or sharing should stretch them (gpu-sharing-advisor).

**B. `node(s) had untolerated taint {nvidia.com/gpu: true}`** — pod lacks the toleration for the GPU pool taint. Fix the workload:
```yaml
tolerations:
- key: "nvidia.com/gpu"
  operator: "Exists"
  effect: "NoSchedule"
```
This is the most common self-inflicted wound: pools taint GPU nodes deliberately; every GPU pod needs the matching toleration. The inverse mistake — *removing the taint* to make things fit — invites CPU workloads onto GPU nodes; never do it.

**C. `didn't match node selector/affinity`** — pod pins something no node (or pool) offers, e.g. `nodeSelector: {karpenter.k8s.aws/instance-gpu-name: a100}` on an L4-only fleet, or a label misspelling (`nvidia.com/gpu.present: "true"` requires GPU feature discovery to be running). Compare pod spec vs `kubectl get nodes --show-labels`. Remember tolerations only *allow*, selectors *attract* — a pod needs both to land on tainted GPU nodes.

**D. Pod is Unschedulable but no new node appears.** Check in order:
1. Is the pod actually marked unschedulable? PodScheduled reason must be `Unschedulable`. Pods waiting on PVC binding, image pulls, or init containers do **not** trigger node autoscaling.
2. Autoscaler logs — e.g. Karpenter: `kubectl -n karpenter logs -l app.kubernetes.io/name=karpenter --all-containers=true --tail=100 | grep -i -e unschedulable -e "no.*match" -e error`. Look for "Unable to schedule pod": it means **no node pool's constraints intersect the pod's requirements** (pod demands GPU type/zone/arch that no pool allows). Fix the pool requirements or the pod's.
3. Pool at its aggregate limit (`limits: nvidia.com/gpu: "10"` reached) — raise deliberately, it's the spend cap.
4. Provider capacity/quota: insufficient-capacity errors usually retry through; account quota errors don't. On Lambda ask about GPU availability per type and account limits; broaden acceptable GPU types/zones if the pool is overly narrow.

### 2. Node launched but pods still Pending
```
kubectl get nodeclaims          # Karpenter-style provisioners
kubectl describe nodeclaim <name>
```
Signature: **`Initialized: False` with "gpu resource not registered"** — the instance is up, but the device plugin never registered `nvidia.com/gpu` on it. Causes: node image without driver/toolkit (wrong image family for GPU — confirm with Lambda which images are accelerated), device plugin DaemonSet not landing (selector/toleration), or GPU Operator still initializing. Also check `startupTaints`: CNIs/agents that taint nodes during init must be declared to the autoscaler or it misreads readiness and can churn extra nodes.

### 3. GPU node unhealthy
Node-monitoring agents surface granular conditions; **`AcceleratedHardwareReady: False`** = GPU hardware failure, typically remediated fast (Karpenter Node Auto Repair force-replaces after 10 min vs 30 for generic conditions). Evidence gathering:
```
kubectl describe node <node> | grep -A12 Conditions
kubectl debug node/<node> -it --image=<approved-registry>/nvidia-cuda@sha256:<approved-digest> -- nvidia-smi
# DCGM: check DCGM_FI_DEV_XID_ERRORS, DCGM_FI_DEV_GPU_TEMP in Prometheus
```
On managed K8s, failed GPU hardware is the provider's to replace: cordon/drain the node, open a ticket with Lambda including node name, XID errors, and timestamps; verify auto-repair/replacement behavior with them. Unhealthy-GPU pods often show as stuck ContainerCreating or CrashLoop *despite* the node looking Ready — trust DCGM/XID over the Ready condition.

`kubectl debug node` is a privileged host-debug path. Use it only with incident approval, provider authorization, a digest-pinned image from an approved registry, and audit logging. Prefer provider diagnostics/DCGM first, and do not run host-debug sessions on shared production nodes unless the incident requires it and the node has been isolated.

### 4. Scheduled, but CrashLoopBackOff / restarts during model load
```
kubectl describe pod <pod>      # exit code, restart reason, events
kubectl logs <pod> --previous   # what it printed before dying
```
- **Killed by probes, not crashing**: exit 137 + "Liveness probe failed" events + clean logs = the kubelet is killing a healthy-but-slow server. Large models take minutes to pull weights and warm up; default probes assume seconds. Fix with a startupProbe budgeted to worst-case load, keeping liveness tight afterward:
  ```yaml
  startupProbe:
    httpGet: { path: /health, port: 8080 }
    periodSeconds: 10
    failureThreshold: 60        # 10m budget: threshold × period ≥ worst-case model load
  livenessProbe:
    httpGet: { path: /health, port: 8080 }
    periodSeconds: 10
    failureThreshold: 3
  readinessProbe:               # gate on model actually loaded, not TCP-up
    httpGet: { path: /ready, port: 8080 }
    periodSeconds: 5
  ```
- **Slow image pulls masquerading as hangs**: multi-GB GPU images (5 GB+) pull for minutes; `describe pod` shows the Pulled event with timing (a measured case: 1m16s cold vs 654ms with node-side pre-caching). Persistent pull slowness during scale-out → pre-cache images / mount models from PVC or object storage instead of baking into the image (gpu-autoscaling-engineer covers the cold-start design).
- **Genuine crash on load** → branch 5.

### 5. OOM: host RAM vs VRAM — different failures, different fixes

| Signal | It is | Fix |
|---|---|---|
| Pod OOMKilled, exit code 137, `describe` shows reason OOMKilled | **Host RAM** — container breached its memory limit (model loading commonly stages weights through CPU RAM, spiking far above steady state) | Raise `resources.limits.memory` (size for load-time peak, not steady state); check LimitRange defaults aren't clamping (a namespace default of 8Gi silently OOMs a 13B load) |
| App log shows `CUDA out of memory` / `torch.cuda.OutOfMemoryError`, pod Running or CrashLooping with a Python/CUDA stack trace, no OOMKilled reason | **VRAM** — the GPU's memory is exhausted; Kubernetes limits don't govern VRAM | Smaller batch/context/precision (quantize), bigger GPU or MIG slice, or fewer co-tenants: under time-slicing/MPS there is **no VRAM protection** — a neighbor can consume the memory your pod needs. Check `DCGM_FI_DEV_FB_USED` vs `FB_FREE` per GPU and who else is on the card |

Sporadic VRAM OOM only at busy hours on shared nodes = co-tenant contention → move the workload to an isolated MIG slice or exclusive GPU (gpu-sharing-advisor decision table).

## Quick reference

```
kubectl describe pod <pod>                                          # events: the first read, always
kubectl get nodes -o custom-columns=NAME:.metadata.name,GPUs:.status.allocatable."nvidia\.com/gpu"
kubectl get ds -A | grep -i nvidia                                  # device plugin present?
kubectl get nodeclaims && kubectl describe nodeclaim <n>            # provisioning status conditions
kubectl -n karpenter logs -l app.kubernetes.io/name=karpenter --all-containers=true -f --tail=20
kubectl get pod <pod> -o jsonpath='{.status.conditions}' | jq       # PodScheduled reason
kubectl logs <pod> --previous                                       # pre-crash output
kubectl get events -n <ns> --sort-by=.lastTimestamp | tail -20
kubectl get quota -n <ns>                                           # admission-time rejections
```

## Guardrails
- Fix the broken link; never blanket-fix: no `privileged: true`, no taint removal, no quota bump, no probe deletion just to make a symptom disappear — each converts a visible failure into an invisible one.
- Read status conditions (pods, nodes, NodeClaims) before logs — provisioners put the diagnosis in `describe` output.
- Prefer centralized logs over `kubectl logs` for anything historical; pod logs die with the pod.
- On shared GPUs, per-pod symptoms can have per-*card* causes — always establish who else is on the device before blaming the workload.
- Hardware and node-image faults are provider-side on managed K8s: collect evidence (conditions, XID, timestamps), cordon, escalate to Lambda — don't burn hours reinstalling drivers on nodes you don't image.
- After any fix, verify the *chain*, not the pod: allocatable resources correct → schedules → loads → serves → scales.

## Suggested effort
Low per incident when the tree is followed (most cases resolve at step 1A/1B in minutes). Recurring incidents of the same class = a platform defect — route to the owning sibling skill (autoscaling, sharing, tenancy) instead of re-diagnosing.
