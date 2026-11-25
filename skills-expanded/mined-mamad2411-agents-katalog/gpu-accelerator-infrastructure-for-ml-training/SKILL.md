---
name: gpu-accelerator-infrastructure-for-ml-training
description: >
  Guides standing up GPU accelerator infrastructure on Kubernetes for ML
  training and serving workloads — installing the NVIDIA GPU Operator,
  partitioning GPUs with Multi-Instance GPU (MIG), designing GPU node pools,
  and scheduling/bin-packing training and serving pods onto that capacity
  without fragmentation or idle spend. Use when the user asks to "add GPU
  nodes to a cluster", "install the NVIDIA GPU Operator", "set up MIG
  partitioning", "carve up an A100/H100 into smaller GPU slices", design a
  GPU node pool or bin-packing/scheduling strategy for training and serving
  workloads sharing the same cluster, or reduce idle GPU spend.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# GPU Accelerator Infrastructure For ML Training

## Purpose

GPUs are the single most expensive line item in most ML platforms, and they
are also the resource most likely to sit idle or fragmented if the
underlying infrastructure isn't deliberately designed. This skill covers
building the Kubernetes-native GPU platform layer: installing the NVIDIA
GPU Operator so nodes expose `nvidia.com/gpu` as a schedulable resource,
partitioning large GPUs (A100/H100) into right-sized Multi-Instance GPU
(MIG) slices instead of handing a whole 80GB card to a job that needs 10GB,
and designing node pools and bin-packing/scheduling rules so training and
serving workloads share capacity efficiently instead of each landing on its
own mostly-idle node. Getting this layer wrong is expensive twice over: too
loose, and jobs fragment GPUs and burn budget on underutilized hardware;
too rigid, and legitimate training jobs queue for hours waiting on capacity
that technically exists but isn't schedulable in the shape they asked for.
This skill covers the infrastructure that must exist *before* a job can even
request a GPU correctly — validating that a specific job's request against
that infrastructure is covered by
[gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md).

## When to use

- Standing up GPU support on a new or existing Kubernetes cluster (on-prem,
  EKS/AKS/GKE, or a bare-metal cluster) for the first time.
- Installing or upgrading the NVIDIA GPU Operator, device plugin, or DCGM
  (Data Center GPU Manager) exporter.
- Deciding whether and how to partition A100/H100/H200 GPUs with MIG for
  workloads that don't need a full GPU (inference, notebooks, small
  fine-tuning jobs).
- Designing GPU node pools — which GPU SKU per pool, taints/tolerations,
  autoscaling behavior, and how training and serving workloads should be
  separated or shared across pools.
- Reducing GPU fragmentation or idle spend caused by poor bin-packing
  (many nodes running one small job each instead of packed onto fewer
  nodes).
- Enabling GPU time-slicing or MPS (Multi-Process Service) for workloads
  that can tolerate sharing a GPU without hard MIG partitioning.

## Prerequisites & environment

- Kubernetes ≥ 1.24 with Helm ≥ 3.8 for installing the GPU Operator chart.
- Nodes with NVIDIA GPUs (data-center class: A100, H100, H200, L4, L40S,
  or older V100/T4) and a supported host OS (Ubuntu 20.04/22.04, RHEL 8/9,
  or a cloud provider's GPU-optimized AMI/image).
- Node Feature Discovery (NFD) — installed automatically by the GPU
  Operator by default — to label nodes with GPU hardware facts the
  operator and scheduler use.
- Cluster admin permissions to install cluster-scoped operators/CRDs
  (`ClusterPolicy`, `NodeFeatureDiscovery`) and to label/taint nodes.
- MIG support requires an A100/H100/H200-class GPU (MIG is not available on
  T4/L4/V100) and a driver version compatible with the desired MIG profile
  set — check the NVIDIA GPU Operator release notes for the driver/MIG
  compatibility matrix before choosing profiles.
- For managed Kubernetes (EKS/AKS/GKE), decide whether to use the cloud
  provider's own GPU device plugin/AMI or the NVIDIA GPU Operator — mixing
  both on the same node causes device plugin conflicts (see Common
  pitfalls).

## Step-by-step guidance

1. **Install the NVIDIA GPU Operator via Helm**, letting it manage the
   driver, container toolkit, device plugin, and DCGM exporter as a
   coordinated stack rather than installing each piece by hand:
   ```bash
   helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
   helm repo update
   helm install gpu-operator nvidia/gpu-operator \
     --namespace gpu-operator --create-namespace \
     --set driver.version="550.90.07" \
     --set mig.strategy=mixed \
     --set devicePlugin.config.name=mig-parted-config
   ```
   `mig.strategy=mixed` allows nodes to run a combination of MIG-partitioned
   and non-MIG GPUs in the cluster (vs. `single`, which requires a
   cluster-wide uniform MIG layout). If nodes already have NVIDIA drivers
   pre-installed (common on cloud GPU-optimized images), set
   `driver.enabled=false` so the operator doesn't try to install a
   conflicting driver.

2. **Verify the device plugin is healthy and GPUs are schedulable** before
   trusting the cluster to run anything on them:
   ```bash
   kubectl get pods -n gpu-operator
   kubectl get nodes -o json | jq '.items[].status.capacity | select(.["nvidia.com/gpu"])'
   ```
   A node with a physically present GPU but no `nvidia.com/gpu` entry in
   `status.capacity` means the device plugin isn't running correctly on
   that node — a training job's pod will still schedule (onto CPU-only
   scheduling) unless its resource request is validated, which is exactly
   the silent-fallback failure mode covered in
   [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md).

3. **Partition large GPUs with MIG when workloads don't need a full card.**
   Define the MIG layout in a `ConfigMap` referenced by `mig-parted-config`,
   then apply a profile per node via label:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: mig-parted-config
     namespace: gpu-operator
   data:
     config.yaml: |
       version: v1
       mig-configs:
         all-3g.20gb:
           - devices: all
             mig-enabled: true
             mig-devices:
               "3g.20gb": 2      # 2x A100-80GB sliced into 3g.20gb instances
         all-1g.10gb:
           - devices: all
             mig-enabled: true
             mig-devices:
               "1g.10gb": 7      # max 1g.10gb slices on an 80GB A100
   ```
   ```bash
   kubectl label node gpu-node-a100-01 nvidia.com/mig.config=all-3g.20gb --overwrite
   ```
   Larger profiles (`7g.80gb`, a whole card) suit large training jobs;
   smaller profiles (`1g.10gb`, `2g.20gb`) suit inference and notebooks.
   Mixing profile sizes on one node is possible but adds scheduling
   complexity — start with a uniform profile per node pool.

4. **Design node pools around workload shape, not just GPU SKU.** Separate
   pools for training (larger GPUs, full-card or large MIG slices, tolerant
   of longer scheduling latency) and serving (smaller MIG slices or
   time-sliced GPUs, low-latency autoscaling) prevent a long-running
   training job from starving a latency-sensitive serving deployment of
   capacity, and vice versa:
   ```yaml
   # Example node pool taint/label convention
   # Training pool: full A100s, tainted so only training jobs land here
   kubectl taint nodes gpu-node-a100-01 workload=training:NoSchedule
   kubectl label nodes gpu-node-a100-01 gpu-pool=training gpu-sku=a100-80gb

   # Serving pool: MIG-partitioned L4/A100 slices for inference
   kubectl taint nodes gpu-node-l4-01 workload=serving:NoSchedule
   kubectl label nodes gpu-node-l4-01 gpu-pool=serving gpu-sku=l4
   ```
   Pods then carry matching `tolerations` and `nodeSelector`/`nodeAffinity`
   — see the worked example below for the full pod spec.

5. **Bin-pack deliberately** rather than letting the default scheduler
   spread pods across nodes. For MIG slices and fractional GPU workloads,
   use a `PriorityClass` plus the Kubernetes scheduler's default bin-packing
   behavior on `nvidia.com/gpu` requests, or adopt a batch scheduler (Kueue,
   Volcano, or YuniKorn) for gang-scheduling and queueing when many small
   jobs compete for a fixed pool:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: mig-inference-worker
   spec:
     nodeSelector:
       gpu-pool: serving
     tolerations:
       - key: workload
         operator: Equal
         value: serving
         effect: NoSchedule
     containers:
       - name: worker
         image: registry.internal/inference:1.4.0
         resources:
           limits:
             nvidia.com/mig-1g.10gb: 1
   ```
   Without an explicit bin-packing policy, the default scheduler's
   least-requested-resources heuristic tends to *spread* pods across nodes
   to balance load — the opposite of what you want for GPU cost efficiency,
   where consolidating small jobs onto fewer fully-packed nodes (and letting
   the cluster autoscaler/Karpenter scale down empty nodes) is usually
   cheaper. See
   [karpenter-cluster-autoscaling](../../../observability-and-platform-extras/skills/karpenter-cluster-autoscaling/SKILL.md)
   for consolidation-aware node autoscaling that complements this.

6. **Enable time-slicing or MPS for workloads that tolerate GPU sharing**
   without hard MIG isolation (e.g. many low-traffic inference replicas):
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: time-slicing-config
     namespace: gpu-operator
   data:
     any: |
       version: v1
       flags:
         migStrategy: none
       sharing:
         timeSlicing:
           resources:
             - name: nvidia.com/gpu
               replicas: 4
   ```
   Time-slicing gives no memory or fault isolation between the 4 sharing
   pods (unlike MIG) — use it only for workloads where one noisy neighbor
   degrading another is an acceptable tradeoff for higher utilization, never
   for multi-tenant workloads with different trust boundaries.

7. **Monitor GPU utilization, not just allocation**, using the DCGM
   exporter the GPU Operator installs, scraped by Prometheus:
   ```promql
   avg by (node) (DCGM_FI_DEV_GPU_UTIL)
   ```
   A node pool where `nvidia.com/gpu` is 100% *allocated* (every slice
   claimed by a pod) but `DCGM_FI_DEV_GPU_UTIL` sits at 5% means jobs are
   holding GPU resources without using them — a capacity-planning problem
   worth catching before provisioning more nodes.

## Best practices

- Treat MIG profile choice as a capacity-planning decision, not a one-time
  default — re-evaluate profile sizes as workload mix shifts between
  training and serving, since a mismatched profile forces jobs to queue for
  a larger slice than they need or wastes memory on a slice larger than the
  job uses.
- Keep training and serving GPU pools physically or logically separate
  (taints + node pools) so a long training job's resource hold never blocks
  a latency-sensitive serving deployment's ability to scale up.
- Prefer MIG over time-slicing whenever workloads have different trust
  boundaries or need predictable memory isolation — time-slicing shares a
  memory space and gives no protection against one workload's memory usage
  starving another's.
- Pin driver and CUDA toolkit versions explicitly in the GPU Operator
  `ClusterPolicy` rather than tracking "latest," and roll out driver
  upgrades to a canary node pool first — a driver bump that breaks a
  specific CUDA version used by training images is a cluster-wide outage
  if rolled out everywhere at once.
- Pair GPU node pools with cluster-autoscaler/Karpenter consolidation so
  idle GPU nodes scale to zero during off-hours rather than running
  20%-utilized nodes around the clock — GPUs are the most expensive
  instance type in almost every cloud's catalog.
- Label node pools with the GPU SKU and MIG profile explicitly
  (`gpu-sku=a100-80gb`, `mig-profile=3g.20gb`) so scheduling decisions and
  cost attribution are visible from `kubectl get nodes --show-labels`
  rather than tribal knowledge.

## Common pitfalls

- **Symptom:** A training job that requests no GPU resource (or a
  malformed resource key) schedules successfully onto a CPU-only node,
  runs to completion at a fraction of expected speed, and nobody is
  alerted — the job "succeeds" with a garbage checkpoint or simply takes
  10x longer with no error.
  **Warning:** This is a genuinely dangerous silent-failure mode, not just
  a slow job — a multi-hour or multi-day training run silently falling
  back to CPU wastes the entire compute budget for that run and can delay
  a release with no signal until someone notices the wall-clock time.
  **Fix:** Never rely on "the job didn't error" as a signal it used a GPU.
  Enforce GPU scheduling correctness *before* the job runs — see
  [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md)
  for admission-time validation and in-job fail-fast checks — and alert on
  `DCGM_FI_DEV_GPU_UTIL` being near-zero for a pod that has a GPU resource
  request, which independently catches drivers/toolkit mismatches that let
  a pod schedule onto a GPU node but silently execute CPU-only kernels.

- **Symptom:** Installing the NVIDIA GPU Operator on a managed Kubernetes
  cluster (EKS/AKS/GKE) that already ships its own GPU device plugin or
  pre-installed driver results in two device plugins registering the same
  `nvidia.com/gpu` resource, causing pods to schedule but fail at
  container-create time with driver/library version mismatches.
  **Fix:** Check whether the managed cluster's GPU-optimized node image
  already installs a driver and device plugin before installing the GPU
  Operator; if so, either use the cloud provider's native tooling instead
  of the GPU Operator, or explicitly disable the operator's `driver` and
  `devicePlugin` components (`driver.enabled=false`,
  `devicePlugin.enabled=false` if the cloud plugin is kept) so exactly one
  device plugin manages the resource.

- **Symptom:** A MIG profile change (e.g. switching a node from
  `all-1g.10gb` to `all-3g.20gb`) is applied while pods are still running
  on that node's existing MIG instances, and those pods are evicted
  mid-training with no checkpoint saved.
  **Fix:** Cordon and drain the node before changing its MIG profile label
  (`kubectl cordon` then `kubectl drain --ignore-daemonsets`) — the GPU
  Operator's MIG manager reconfigures the physical GPU when the label
  changes, which requires resetting any GPU currently in use, destroying
  the state of anything running on it.

- **Symptom:** GPU nodes show low average utilization (10-20%) despite
  `nvidia.com/gpu` capacity being fully allocated across the pool, and the
  team concludes they need to buy more GPU nodes.
  **Fix:** This is usually a bin-packing/right-sizing problem, not a
  capacity problem — check whether small jobs are each claiming a full GPU
  or an oversized MIG slice instead of the smallest profile that fits, and
  whether jobs are actually GPU-bound at all (a data-loading-bottlenecked
  training job can hold a GPU near-idle while waiting on I/O). Fix the
  workload's resource request and data pipeline before provisioning more
  hardware.

- **Symptom:** After enabling GPU time-slicing to increase inference
  throughput, one tenant's memory-heavy request causes CUDA
  out-of-memory errors in an unrelated tenant's replica sharing the same
  physical GPU.
  **Fix:** Time-slicing shares GPU memory with no isolation between
  replicas — this is expected behavior, not a bug. Move workloads that
  need memory isolation to MIG partitioning instead, which enforces a hard
  memory boundary per instance, and reserve time-slicing for workloads
  from a single trust boundary with well-understood memory footprints.

## Worked example

**Scenario:** A platform team has four A100-80GB nodes and needs to support
both large fine-tuning jobs (need most of a GPU) and a fleet of small
inference services (each needs ~10GB). They partition two nodes for
training (full-card) and two for serving (MIG-sliced), with monitoring to
catch idle capacity.

Training node pool (full A100, no MIG):
```bash
kubectl label nodes gpu-node-a100-01 gpu-node-a100-02 \
  gpu-pool=training gpu-sku=a100-80gb
kubectl taint nodes gpu-node-a100-01 gpu-node-a100-02 \
  workload=training:NoSchedule
```

Serving node pool (MIG `1g.10gb` x7 per card):
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mig-parted-config
  namespace: gpu-operator
data:
  config.yaml: |
    version: v1
    mig-configs:
      all-1g.10gb:
        - devices: all
          mig-enabled: true
          mig-devices:
            "1g.10gb": 7
```
```bash
kubectl label nodes gpu-node-a100-03 gpu-node-a100-04 \
  gpu-pool=serving nvidia.com/mig.config=all-1g.10gb --overwrite
kubectl taint nodes gpu-node-a100-03 gpu-node-a100-04 \
  workload=serving:NoSchedule
```

Training job pod spec (targets the training pool, requests a full GPU):
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: finetune-llm-run-214
spec:
  template:
    spec:
      nodeSelector:
        gpu-pool: training
      tolerations:
        - {key: workload, operator: Equal, value: training, effect: NoSchedule}
      containers:
        - name: trainer
          image: registry.internal/finetune:2.3.0
          resources:
            limits:
              nvidia.com/gpu: 1
      restartPolicy: Never
```

Inference deployment (targets the serving pool, requests one MIG slice per
replica, 14 replicas fit across the two serving nodes):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fraud-scorer-inference
spec:
  replicas: 14
  template:
    spec:
      nodeSelector:
        gpu-pool: serving
      tolerations:
        - {key: workload, operator: Equal, value: serving, effect: NoSchedule}
      containers:
        - name: server
          image: registry.internal/fraud-scorer-server:8
          resources:
            limits:
              nvidia.com/mig-1g.10gb: 1
```
`DCGM_FI_DEV_GPU_UTIL` dashboards per pool then show whether the training
pool is actually compute-bound during runs and whether the 14 serving
replicas are bin-packed at the expected 7-per-node density rather than
spread thin across more nodes than needed.

## Cross-references

- [gpu-accelerator-configuration-validation](../gpu-accelerator-configuration-validation/SKILL.md) — validating that a specific job's resource requests/tolerations actually match this infrastructure before it runs, catching silent CPU fallback.
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md) — the pipeline layer that submits training jobs onto the GPU infrastructure built here.
- [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md) — serving-side autoscaling and latency concerns for workloads running on the serving GPU pool.
- [ray-distributed-ml-orchestration](../ray-distributed-ml-orchestration/SKILL.md) and [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md) — orchestration tools that schedule distributed training/serving workloads onto this GPU infrastructure.
- [karpenter-cluster-autoscaling](../../../observability-and-platform-extras/skills/karpenter-cluster-autoscaling/SKILL.md) — node-level autoscaling and consolidation that complements the bin-packing strategy here.
- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — cloud-provider-specific GPU node pool/AMI considerations that interact with the GPU Operator install choice.
