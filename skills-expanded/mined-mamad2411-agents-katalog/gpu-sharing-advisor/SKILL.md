---
name: gpu-sharing-advisor
description: >-
  Decide between MIG, MPS, and time-slicing for sharing NVIDIA GPUs across
  Kubernetes workloads, and produce the config to implement the choice. Use
  whenever the user asks about GPU sharing, fractional GPUs, partitioning a
  GPU, MIG profiles, Multi-Process Service, time-slicing, GPU oversubscription,
  virtual GPUs, "our GPUs sit idle", low GPU utilization, running many small
  models on one GPU, packing inference replicas, or letting multiple
  researchers or notebooks share an A100/H100/H200/L4. Also use when reviewing
  a time-slicing ConfigMap, a MIG strategy (single vs mixed), or
  nvidia.com/mig-* resource requests. For scaling the shared workloads up and
  down use sibling gpu-autoscaling-engineer; for per-team GPU quotas use
  researcher-tenancy-provisioner; for the cost report that motivates sharing
  use gpu-cost-optimizer.
---

# GPU Sharing Advisor

## Purpose
Turn "our GPUs are expensive and mostly idle" into a per-workload sharing decision — MIG, MPS, time-slicing, or exclusive whole-GPU — backed by utilization evidence and shipped as concrete NVIDIA device plugin / GPU Operator configuration. Built for research clusters (inference testing, data collection, model training) on managed Kubernetes such as Lambda's, where the NVIDIA layer (device plugin, GPU Operator, DCGM) is fully in the customer's control even though the control plane is not.

## Core model to hold in your head

Kubernetes treats a GPU as an **extended resource** (`nvidia.com/gpu`) exposed by a device plugin DaemonSet that registers with the kubelet. By default, allocating a GPU to a Pod reserves the **whole physical device for the Pod's entire lifecycle**, even when idle: no fractions, no sharing, and GPU resources must be set in `limits` (requests are auto-set equal; specifying only requests is invalid). This design guarantees isolation — and guarantees waste for research workloads, because:

- **Model sizes vary wildly.** A distilled or 1B-parameter model needs a fraction of a modern GPU. Concrete math: Llama-3.2-1B needs ~1.8 GB to load and serve; on a 24 GB L4 that leaves **92% of GPU memory reserved but unused**. Ten time-sliced replicas turn that one L4 into 10 schedulable virtual GPUs.
- **Usage is bursty.** Training/fine-tuning spikes to 100% during matrix ops and drops between epochs and data-loading steps; interactive notebooks idle most of the day.
- **The scheduler can't defragment.** Small workloads monopolize whole devices; the cluster ends up with many GPUs partially utilized but fully reserved. Fractional-GPU case studies report up to ~95% price-performance improvement from sharing.

**Utilization-waste math (do this before recommending anything):** per workload, waste% = 1 − (peak `DCGM_FI_DEV_FB_USED` / GPU memory), cross-checked against `DCGM_FI_DEV_GPU_UTIL`. Sharing is justified when memory waste > 50% or average compute util < 30% sustained. Get these from DCGM-Exporter/Prometheus (see sibling gpu-autoscaling-engineer for the metrics pipeline).

## The three techniques compared

| Feature | MIG | MPS | Time-slicing |
|---|---|---|---|
| Resource isolation | Strong (hardware-level partitions) | None/limited (per-client address spaces on Volta+) | None |
| Memory protection | Dedicated memory per instance | Partial — bandwidth still shared, no fault isolation | None — co-tenants can OOM each other |
| Fault isolation | Yes | No — one process's fatal error can disrupt others | No |
| Performance | Predictable, guaranteed | Better utilization, added latency, concurrent execution | Depends on workload; sequential interleaving |
| Overhead | Minimal | Low | Highest — context-switch save/restore per slice |
| Scalability | Limited by profile count (max 7 slices) | High | High (replica count is arbitrary) |
| Best for | Multi-tenant, production inference, strict SLAs | HPC / cooperative multi-process, latency-tolerant batch | Non-critical dev/test, small-model inference, notebooks |
| Hardware | Ampere+ only (A100, H100, H200…) | All CUDA GPUs | All CUDA GPUs (the only option on pre-Ampere / L4-class) |
| K8s support | GPU Operator + MIG Manager, first-class | Not in upstream device plugin (tracked; forks exist) | First-class via device plugin ConfigMap |

## MIG (Multi-Instance GPU)
Partitions one physical Ampere+ GPU into up to 7 isolated instances, each with dedicated memory and compute. Profiles are named `<slices>g.<memory>gb`; e.g., an A100-40GB yields up to seven `1g.5gb` instances. H200 profile table (from the NVIDIA MIG user guide):

| MIG profile | GPU slices | Memory (GB) | Instances per GPU |
|---|---|---|---|
| 1g.18gb | 1 | 18 | 7 |
| 1g.35gb | 1 | 35 | 4 |
| 2g.35gb | 2 | 35 | 3 |
| 3g.70gb | 3 | 70 | 2 |
| 4g.70gb | 4 | 70 | 1 |
| 7g.141gb | 7 | 141 | 1 |

Instances surface as extended resources; a Pod requests a slice, not a GPU:

```yaml
resources:
  limits:
    nvidia.com/mig-1g.18gb: 1
```

Two configuration strategies:
- **Single strategy** — every slice on a node is the same size. Use when teams have similar needs; simplest quota story (fair, uniform slices).
- **Mixed strategy** — heterogeneous slices per GPU (e.g., 16×1g.10gb + 8×2g.20gb + 8×3g.40gb across eight H100s). Use when one cluster serves image, NLP, and video workloads with different footprints; match slice to model footprint to avoid overprovisioning.

Implement via the NVIDIA GPU Operator (deploys MIG Manager). Reconfiguring MIG geometry disrupts workloads on that GPU — treat profile layout as slow-moving platform config, not per-job tuning.

## MPS (Multi-Process Service)
Lets multiple processes submit CUDA work concurrently, sharing compute dynamically while each client keeps its own GPU address space (Volta+). Reduces idle time and scheduling latency for cooperative multi-process workloads. Costs: shared global memory bandwidth, **no fault isolation** (a crashing client can take down its peers), synchronization/contention complexity. Kubernetes caveat: the upstream NVIDIA device plugin does not support MPS partitioning (GitHub issue #443); a community fork (nebuly-ai/k8s-device-plugin) enables fractional MPS requests. On a managed cluster, prefer MIG or time-slicing unless you have a specific HPC-style multi-process pattern and accept running a forked plugin.

## Time-slicing
Interleaves processes on one GPU in round-robin execution time slices — oversubscription, not partitioning. No memory or fault isolation; context-switching overhead; latency varies with co-tenant count. It is the only sharing option for GPUs without MIG (L4, L40S, older cards) and can even subdivide a MIG slice. Recipe — ConfigMap consumed by the NVIDIA device plugin (or GPU Operator):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: time-slicing-config
  namespace: nvidia-device-plugin
data:
  any: |-
    version: v1
    flags:
      migStrategy: none
    sharing:
      timeSlicing:
        resources:
        - name: nvidia.com/gpu
          replicas: 10
```

Point the device plugin Helm values at `config.name: time-slicing-config`, then verify the node now advertises 10 schedulable GPUs per physical device:

```
kubectl get nodes -o custom-columns=NAME:.metadata.name,GPUs:.status.allocatable."nvidia\.com/gpu"
```

Pods still request `nvidia.com/gpu: 1` — they get one *virtual* replica. Mixed GPU fleets (A100 + L4 + H100): use node-specific named configs in the ConfigMap plus node labels selecting which config applies, instead of one `any:` block. Size `replicas` from the waste math: replicas ≈ floor(GPU memory / (model footprint + runtime overhead)), capped where p95 latency remains acceptable under contention — load-test, don't guess.

## Decision rules

| Workload pattern | Recommendation | Why |
|---|---|---|
| Small-model inference testing, dev/test endpoints, many replicas of a distilled model | **Time-slicing** | Max packing, works on all GPUs, latency tolerance is acceptable in test |
| Strict tenant isolation, untrusted co-tenants, production inference with SLAs, chargeback-clean boundaries | **MIG** (single strategy for uniform teams, mixed for diverse footprints) | Hardware isolation, dedicated memory, predictable performance |
| Latency-tolerant batch / cooperative multi-process HPC on the same team | **MPS** | Concurrent execution beats round-robin; fault-isolation risk contained within one team |
| Training, fine-tuning, any job that saturates the GPU | **Exclusive whole GPU(s)** | Sharing only adds contention; bin-pack via scheduler instead |
| Interactive notebooks (JupyterHub) | Time-slicing or small MIG slices, per trust level | Notebooks idle most of the time; see researcher-tenancy-provisioner |
| Small models on MIG-capable fleet with mixed trust | MIG slice per tenant, optionally time-sliced within a tenant's slice | Layered: isolation between tenants, packing within |

Tie-breakers: need memory protection → never time-slicing/MPS. Pre-Ampere or L-series hardware → time-slicing is the only option. Latency-sensitive → MIG > MPS > time-slicing.

## Workflow
1. **Inventory**: list GPU workloads, model memory footprints, latency tolerance, trust boundaries between owners. Pull 7 days of `DCGM_FI_DEV_GPU_UTIL` and `DCGM_FI_DEV_FB_USED` per pod.
2. **Ask the provider (Lambda)**: which GPU types are in each node pool, which are MIG-capable, whether the GPU Operator / device plugin is pre-installed or customer-managed, and whether node images ship the NVIDIA driver + container toolkit. On Lambda Managed Kubernetes the NVIDIA stack is typically usable as-is — this skill's configs apply unchanged; only node provisioning is provider-specific.
3. **Classify** each workload with the decision table; compute waste% to justify.
4. **Design**: MIG geometry per node type (single vs mixed) and/or time-slicing replica counts per GPU type; name the resulting extended resources so tenancy quotas can reference them.
5. **Implement** via GPU Operator / device plugin ConfigMap; roll out to one node pool first.
6. **Validate**: allocatable resources on nodes, then load-test a representative pod per slice/replica and confirm p95 latency and no OOM from co-tenants.
7. **Hand off**: scaling policy for shared replicas → gpu-autoscaling-engineer; quota per researcher on the new resource names → researcher-tenancy-provisioner.

## Guardrails
- Never propose MPS or time-slicing across trust boundaries — no memory or fault isolation means one tenant can crash or starve another. Isolation requirement → MIG or whole GPU, full stop.
- GPU requests live in `limits` (requests==limits, non-fractionable). "0.5 GPU" is expressed via a MIG slice or a time-sliced replica, never a decimal.
- Time-slicing changes what `nvidia.com/gpu: 1` means cluster-wide on affected nodes — announce it, and account for it in autoscaling thresholds and cost allocation (10 virtual GPUs ≠ 10× capacity).
- DCGM utilization metrics on shared GPUs reflect the physical device, not one tenant — don't feed them raw into per-workload autoscaling without labels/scoping.
- MIG reconfiguration is disruptive; schedule geometry changes as maintenance, and keep profile layout in Git (see gitops-platform-bootstrap).
- Don't run forked device plugins for MPS on a production cluster without an explicit maintenance owner.

## Suggested effort
Medium — utilization evidence pull, a decision table pass per workload class, and one or two config artifacts. A full fleet re-partition (MIG geometry + quotas + rollout) is a multi-day engagement with load testing.
