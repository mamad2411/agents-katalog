---
name: gpu-cost-optimizer
description: >-
  Run GPU cost visibility, chargeback, and reduction for a research Kubernetes
  cluster: Kubecost/OpenCost per-namespace and per-label allocation, Goldilocks
  rightsizing, spot/preemptible-with-checkpointing decision rules,
  scale-to-zero of idle research environments, and a recurring cost-review
  workflow with a standard report. Use whenever the user asks about GPU cloud
  spend, cost allocation, chargeback or showback per researcher/team/project,
  Kubecost, OpenCost, FinOps for Kubernetes, rightsizing requests and limits,
  Goldilocks, idle GPUs burning money, spot or preemptible instances for
  training, checkpointing strategy, reserved capacity for training runs, or
  "why is our Lambda bill so high". For the sharing techniques that fix
  underutilization use sibling gpu-sharing-advisor; for the autoscaling that
  reclaims idle capacity use gpu-autoscaling-engineer; for quota enforcement
  per tenant use researcher-tenancy-provisioner.
---

# GPU Cost Optimizer

## Purpose
Make GPU spend visible per researcher/project, then cut it in the order that matters — without slowing research down. Compute (GPUs above all) dominates GenAI platform cost; storage and network trail. Deliverable: a working allocation setup, a prioritized savings plan, and a monthly cost-review report the platform team can run on rails.

## Core model to hold in your head

**The GPU savings hierarchy** — work top-down, biggest lever first:
1. **Don't run the GPU at all**: scale-to-zero idle envs, consolidate empty nodes, kill abandoned workloads. An allocated-but-idle GPU costs exactly as much as a busy one.
2. **Share the GPU**: MIG/time-slicing for small models and notebooks (fractional-GPU case studies report up to ~95% price-performance gains) → gpu-sharing-advisor.
3. **Right-size**: correct requests/limits and pick the smallest GPU/slice that fits the model.
4. **Buy cheaper capacity**: spot/preemptible with checkpointing, reserved/committed pricing for the steady baseline.
5. Then storage (unclaimed PVs, snapshot sprawl, image size) and network.

**Waste taxonomy** to hunt for: idle-allocated GPUs (pod holds GPU, `DCGM_FI_DEV_GPU_UTIL` ≈ 0), oversized requests (CPU/mem far above usage), abandoned workloads (running, no traffic, owner gone), unclaimed/orphaned volumes, notebooks running overnight, dev envs alive on weekends.

**Two metering planes**: Kubernetes allocation (what a namespace *requested/held*) vs GPU telemetry (what it *used*, via DCGM). Chargeback on allocation (you reserved it, you pay), coach on utilization (the gap is the waste number you publish).

## Visibility: OpenCost vs Kubecost

| | OpenCost | Kubecost |
|---|---|---|
| License | Open source (CNCF) | Commercial, built on OpenCost |
| Allocation by namespace/label/pod | Yes | Yes |
| Savings insights (rightsizing, abandoned workloads, unclaimed PVs) | No — build from Prometheus yourself | Yes, in UI |
| Multi-cluster aggregation, historical trend depth | Basic | Yes |
| Cloud-bill integration | Cloud billing APIs where available | Deeper (e.g., AWS CUR) |

Setup notes for a managed GPU cloud like Lambda:
- Install via Helm through GitOps (gitops-platform-bootstrap). Cost data starts at install time — deploy visibility *first*, before optimizing, or you'll have no baseline.
- Cloud-bill integrations are hyperscaler-centric (AWS CUR etc.) — flag as not directly applicable. Use **custom pricing**: feed Lambda's published per-GPU-hour rates into OpenCost/Kubecost's custom pricing config so allocation math reflects real prices. Ask Lambda whether a billing API/export exists to reconcile against.
- **Label standard is the foundation of chargeback.** Enforce on every namespace at creation (researcher-tenancy-provisioner stamps these): `team`, `project`, `owner`, `env` (prod/research/scratch). Allocation by label is what turns a cluster bill into per-project chargeback. Unlabeled = charged to platform = platform team's incentive to fix.
- GPU line items: Kubecost prices `nvidia.com/gpu` requests against node cost. Under time-slicing, 10 virtual GPUs share one card — allocate by fraction of physical device (price per virtual GPU = card rate / replicas), or chargeback overstates by 10×.

## Rightsizing

- **Goldilocks** (Fairwinds): runs VPA in Recommender mode, dashboards recommended requests/limits from observed usage. Enable per namespace: `kubectl label namespace <ns> goldilocks.fairwinds.com/enabled=true`. Apply recommendations to CPU/memory of GPU pods too — oversized CPU/mem requests on GPU pods force bigger nodes than the GPU alone needs.
- **GPUs cannot be VPA'd.** Right-size the accelerator by *selection*, not by knob: compare `DCGM_FI_DEV_FB_USED` peak vs card memory; if a model peaks at 9 GB on an 80 GB H100, move it to a MIG `1g.18gb` slice or a smaller GPU type. That decision routes through gpu-sharing-advisor.
- Kubecost Savings Insights: right-size containers and nodes, remedy abandoned workloads, reclaim unclaimed volumes, PV right-sizing. Review monthly; alternatives if unavailable: KRR, StormForge.
- Storage quick wins: prefer the provider's gp3-equivalent tier (gp3 runs ~20% under gp2 on AWS; ask Lambda for tier pricing), `reclaimPolicy: Delete` for scratch StorageClasses, lifecycle/retention policies on datasets and logs, multi-stage builds to shrink multi-GB images (also speeds autoscaling cold starts).

## Spot/preemptible with checkpointing — decision rules

Spot-class capacity runs up to ~90% below on-demand (AWS reference; ask Lambda what interruptible/preemptible options and discounts exist, and what the interruption notice period is — AWS gives 2 minutes).

| Workload | Spot? | Condition |
|---|---|---|
| Training/fine-tuning with checkpointing | Yes — primary target | Checkpoint interval sized so max loss = interval; auto-resume from latest checkpoint on reschedule |
| Batch/offline inference, data prep | Yes | Idempotent or queue-driven (work returns to queue on kill) |
| Notebooks/interactive | Cautious | Only with aggressive auto-save and user consent |
| Online inference serving | No, unless | On-demand fallback capacity exists and SLO tolerates node loss |
| Anything without a resume path | No | Fix the workload first |

Checkpointing math: acceptable loss L minutes → checkpoint every ≤ L minutes; verify checkpoint write time ≪ interruption notice. Frameworks with native support: Ray, Kubeflow, Horovod (interruption handling + checkpoint/resume), PyTorch Lightning. Combine with a node autoscaler that falls back to on-demand when spot is unavailable. Run spot in a separate tainted node pool so only opted-in workloads land there.

**Reserved/guaranteed capacity**: for a known heavy training window, reserving beats both spot (no interruptions) and on-demand (discount + guaranteed availability — GPU scarcity is real). AWS's version is Capacity Blocks for ML (1–14 day reservations, extendable to ~6 months, schedulable up to 8 weeks ahead); ask Lambda what reservation/committed-use options they offer and at what discount. Long-lived baseline (always-on serving) → committed/reserved pricing (AWS RIs reach ~72% off as the reference point).

## Scale-to-zero for idle research environments

- KEDA `minReplicaCount: 0` + HTTP add-on for on-demand research endpoints; cron scaler for office-hours-only envs (scale dev namespaces to 0 nights/weekends) → mechanics in gpu-autoscaling-engineer.
- JupyterHub idle culler: cull notebook servers after N minutes idle — the single biggest saver for notebook-heavy research groups (a forgotten GPU notebook = a GPU-week).
- Node layer: consolidation must remove emptied GPU nodes (`WhenEmpty`, tuned delay); verify pools genuinely reach zero nodes — ask Lambda whether node pools support scale-to-zero.
- TTL abandoned-workload policy: any deployment in `env=scratch` untouched for 14 days gets flagged in the report, then reaped after owner notice.

## Cost-review workflow (monthly, ~1 hour)

1. Pull Kubecost/OpenCost allocation for the month, grouped by namespace and by `project` label.
2. Pull utilization: avg/peak `DCGM_FI_DEV_GPU_UTIL` and `FB_USED` per namespace.
3. Compute per project: GPU-hours allocated, effective utilization %, cost, month-over-month delta.
4. Walk savings insights: abandoned workloads, unclaimed PVs, rightsizing deltas, idle-GPU list.
5. Assign one named action per top-5 waste item; verify last month's actions landed (re-measure, don't assume).
6. Publish the report.

**Report format**:

| Project/namespace | GPU-hrs allocated | Avg GPU util % | Cost | Δ MoM | Top waste item | Action / owner |
|---|---|---|---|---|---|---|

Plus a header block: total spend, spend by capacity type (on-demand/spot/reserved), cluster GPU utilization, unallocated (unlabeled) %, and savings shipped last month (measured, not estimated).

## Guardrails
- Never optimize blind: visibility first, baseline before/after every change, and report *measured* savings only.
- Don't chargeback on unlabeled workloads — fix label hygiene first or the numbers breed distrust.
- Never push spot on workloads without a tested resume path; a failed 3-day training run costs more than the discount saved.
- Under-provisioning is a cost too: latency SLO breaches and researcher hours lost outweigh modest infra savings — pair every cut with the SLO check from gpu-autoscaling-engineer.
- Kubecost/OpenCost see from install time only; don't promise historical analysis that doesn't exist.
- Time-slicing/MIG change allocation units — update pricing config the same day sharing config changes, or chargeback silently breaks.

## Suggested effort
- Quick scan (half day): install-state check, allocation by namespace, idle-GPU list, top-5 waste actions.
- Standard engagement (2–3 days): custom pricing for the provider, label standard enforcement, Goldilocks rollout, spot policy, first monthly report.
- Ongoing: the monthly workflow above, ~1 hour once instrumented.
