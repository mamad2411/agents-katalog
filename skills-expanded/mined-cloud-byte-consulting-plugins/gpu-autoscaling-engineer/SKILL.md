---
name: gpu-autoscaling-engineer
description: >-
  Author and validate autoscaling for GPU workloads on Kubernetes: KEDA
  ScaledObjects with DCGM + application-metric dual triggers, scale-to-zero,
  asymmetric scale-up/scale-down behavior for expensive GPU nodes, warm pools
  via WhenEmpty consolidation, GPU node-pool sizing and taints. Use whenever
  the user mentions KEDA, ScaledObject, HPA for GPU or LLM inference, scale to
  zero, DCGM_FI_DEV_GPU_UTIL, autoscaling triggers, TTFT or tokens-per-second
  or p95 latency as scaling signals, GPU nodes not scaling down, cold starts on
  GPU nodes, warm GPU capacity, Karpenter/cluster-autoscaler for GPUs, or
  "pods scale but nodes don't". Also use to review existing ScaledObject/HPA
  YAML for GPU services. For choosing how to share one GPU across pods use
  sibling gpu-sharing-advisor; for Pending pods and nodes that never join use
  gpu-workload-troubleshooter; for the money view use gpu-cost-optimizer.
---

# GPU Autoscaling Engineer

## Purpose
Design the two coupled scaling loops for GPU services — pod scaling (KEDA/HPA on the right metrics) and node scaling (the cluster's node autoscaler) — so inference capacity follows demand without paying for idle accelerators or thrashing nodes that cost dollars per hour. Output is reviewed/authored YAML: ScaledObjects with dual triggers, scaling behavior blocks, and node-pool policy, plus the list of provider questions for a managed cluster like Lambda's.

## Core model to hold in your head

1. **GPUs are non-fractionable extended resources.** Each pod replica claims a whole `nvidia.com/gpu` (or a MIG slice / time-sliced virtual GPU — sibling gpu-sharing-advisor). Kubernetes auto-sets requests==limits for extended resources; fractional or mismatched values are validation errors. Consequence: pod scale-out translates almost 1:1 into node scale-out once current GPUs are consumed — every HPA decision is implicitly a node-provisioning decision.
2. **The scaling chain**: metric crosses threshold → KEDA (which creates/drives an HPA) adds replicas → replicas go Pending with `Insufficient nvidia.com/gpu` → node autoscaler sees unschedulable pods whose requirements intersect a GPU node pool → node launches → device plugin registers GPUs → pod schedules. A break at any link looks like "autoscaling is broken" (diagnose with gpu-workload-troubleshooter).
3. **CPU utilization is the wrong signal.** GPU services bottleneck on the accelerator and on request queues, not CPU. Scale on what users feel and what the GPU reports.
4. **GPU nodes are expensive and slow to arrive** (provision + driver/plugin ready + multi-GB image pull + model load). Therefore: scale up aggressively, scale down reluctantly, and engineer the cold-start path.

## Metric selection for LLM/inference serving

| Metric | Source | Use as trigger when |
|---|---|---|
| Request rate (RPS) | App /metrics → Prometheus | Demand-driven scaling; leading indicator |
| p95 latency | App /metrics → Prometheus | SLO protection; catches degradation at steady traffic |
| TTFT (time to first token) | Serving stack (vLLM etc.) | Streaming LLM UX; queue saturation shows here first |
| Tokens/sec throughput | Serving stack | Capacity planning; per-replica saturation ceiling |
| Queue depth / batch backlog | Serving stack or broker | Batch/async inference; the cleanest scale-to-zero signal |
| `DCGM_FI_DEV_GPU_UTIL` | DCGM-Exporter → Prometheus | Secondary/guard trigger; confirms replicas are actually busy |
| `DCGM_FI_DEV_FB_USED` | DCGM-Exporter | Not a scaling trigger — rightsizing evidence (KV-cache headroom) |

Rule: **one demand metric + one experience-or-GPU metric** as dual triggers. With multiple KEDA triggers, whichever crosses its threshold first drives scaling (effectively OR / max of computed replica counts) — demand spikes and latency creep both get a response.

## Reference ScaledObject (dual trigger, scale-to-zero, asymmetric behavior)

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: llm-inference-scaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-inference
  minReplicaCount: 0          # scale-to-zero; set 1+ for latency-critical prod
  maxReplicaCount: 8          # cap = aggregate GPU budget for this service
  pollingInterval: 15
  cooldownPeriod: 300         # wait 5m at zero-load before dropping to 0
  advanced:
    horizontalPodAutoscalerConfig:
      behavior:
        scaleUp:
          stabilizationWindowSeconds: 0      # react immediately
          policies:
          - type: Percent
            value: 100                       # may double replicas...
            periodSeconds: 5                 # ...every 5s
        scaleDown:
          stabilizationWindowSeconds: 120    # 2 min of calm before shrinking
          policies:
          - type: Percent
            value: 100
            periodSeconds: 30
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-server.monitoring.svc:9090
      metricName: gpu_inference_request_rate
      threshold: "40"
      query: sum(rate(http_requests_total{app="llm-inference"}[1m]))
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-server.monitoring.svc:9090
      metricName: gpu_inference_latency_p95
      threshold: "2"
      query: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{app="llm-inference"}[2m])) by (le))
  - type: prometheus
    metadata:
      serverAddress: http://prometheus-server.monitoring.svc:9090
      metricName: DCGM_FI_DEV_GPU_UTIL
      threshold: "70"
      query: avg(DCGM_FI_DEV_GPU_UTIL{pod=~"llm-inference-.*"})
```

Design notes:
- **Asymmetry is the point.** Instant doubling on the way up; a 120s stabilization window and stepped shrink on the way down. You accept a short tail of underutilized capacity to avoid re-buying a GPU node you just released. Tune the window to (node provision time + pod cold start) — never shorter.
- Validate after apply: `kubectl describe hpa keda-hpa-llm-inference-scaler` should show "successfully calculate a replica count from external metric". Kubernetes reports in milli-units: `2576m/2` means p95 = 2.576s vs threshold 2s.
- Scale-to-zero for HTTP services needs a buffer for the first request: KEDA's HTTP add-on (intercepts and holds traffic while activating 0→1), or a queue in front. Without one, first callers get errors, not just latency.
- Training/fine-tuning is not HPA territory — run as Jobs (queue-driven via a KEDA queue scaler if needed); autoscaling there means node provisioning per Job and consolidation after (Kueue/Volcano/KAI-scheduler are the heavier options if gang scheduling is needed).

## Node-pool design for GPU scaling

Pattern (Karpenter NodePool terms shown; translate to your provider's node-pool API):

- **Dedicated GPU pools, tainted.** Taint `nvidia.com/gpu=true:NoSchedule`; only GPU pods carry the toleration (`operator: Exists` on key `nvidia.com/gpu`, effect NoSchedule). This keeps cheap workloads off dollars-per-hour nodes. Pair the toleration with a nodeSelector (e.g., `nvidia.com/gpu.present: "true"` or a GPU-model label) — tolerations allow, they don't attract.
- **Limit by aggregate GPU count, not node count**: `limits: {nvidia.com/gpu: "10"}` caps a pool's blast radius in the unit that maps to spend, regardless of instance size mix.
- **Warm pool via `WhenEmpty` consolidation**: `consolidationPolicy: WhenEmpty` + `consolidateAfter: 5m` keeps a just-emptied GPU node alive 5 minutes for the next pod, instead of the default aggressive `WhenEmptyOrUnderutilized` repacking that churns expensive nodes. For strict cost control on batch pools, shorten to 30–60s.
- **startupTaints** for any DaemonSet that taints nodes during init (CNI, security agents) — otherwise the autoscaler misreads the taint as permanent and launches surplus nodes.
- **Cold-start engineering**: GPU images are 5+ GB; a measured example went from 1m16s pull to 654ms by pre-caching the image on the node's data volume (snapshot-preloaded). Ask the provider what's available: pre-pulled images in custom node images, image-streaming, local NVMe cache. Also bake models into a PVC/object-store mount rather than the image where possible.

**Lambda managed-K8s translation.** Karpenter's `EC2NodeClass`/instance-type selection, Bottlerocket AMIs, and capacity-type spread are AWS machinery — flag them, don't copy them. The portable pattern is: dedicated tainted GPU pool, aggregate GPU cap, warm-down delay, pre-cached images. Ask Lambda: (1) what the node-pool autoscaler is and whether it scales on unschedulable pods, (2) supported GPU types per pool and max nodes, (3) whether pools can scale to zero and node provision latency, (4) whether node images pre-bake NVIDIA driver + device plugin, (5) how to pre-cache large images on nodes, (6) billing granularity (per-minute vs per-hour changes how aggressive scale-down should be).

## Workflow
1. Baseline: instrument app metrics + DCGM-Exporter; a ServiceMonitor per service; 1 week of traffic and latency data.
2. Pick trigger pair + thresholds from the table (threshold = per-replica sustainable rate × safety factor 0.7–0.8; latency threshold = SLO).
3. Author ScaledObject from the reference; set maxReplicaCount from the GPU budget; decide minReplicaCount 0 vs 1 by cold-start tolerance.
4. Configure the node pool (taint, aggregate limit, consolidation delay); confirm quota headroom with the provider.
5. Load-test (k6 or similar); watch `kubectl get hpa,scaledobject,pods,nodes -w`; verify scale-up latency end-to-end (trigger→serving), then verify scale-down completes and nodes are reclaimed.
6. Tune: if replicas flap, widen scaleDown stabilization; if scale-up lags spikes, lower thresholds or add a queue-depth trigger; if nodes churn, raise consolidateAfter.

## Guardrails
- Never scale GPU pods on CPU/memory. Never use DCGM utilization as the *only* trigger — it lags demand and reads misleading on shared GPUs (time-slicing/MPS report the physical device).
- HPA and VPA must not both drive the same workload's resources.
- On time-sliced nodes, `maxReplicaCount` and node math change meaning: 10 virtual GPUs per card — size thresholds per virtual replica's real throughput, which is contention-dependent.
- Scale-down stabilization shorter than node-provision time guarantees thrash. Measure provision time on the actual provider before tuning.
- A ScaledObject on a Deployment whose pods lack the GPU-pool toleration scales pods into permanent Pending — validate the full chain, not the YAML in isolation.
- Keep every ScaledObject and node-pool spec in Git (gitops-platform-bootstrap); scaling config drift is a cost incident waiting to happen.

## Suggested effort
Medium-high — per service: metrics wiring, one ScaledObject, one load test (half a day). Platform-wide node-pool policy plus provider Q&A is a short engagement; revisit thresholds quarterly against gpu-cost-optimizer's report.
