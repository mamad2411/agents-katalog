---
name: model-serving-and-scaling
description: >
  Guides deploying ML/LLM models for online inference with autoscaling,
  latency budgets, batching, canary/shadow rollout, and cost control. Use
  when the user asks to "serve a model", "deploy a model for inference",
  set up autoscaling for a model endpoint, reduce inference latency or cost,
  do a canary/shadow rollout of a new model version, or choose between
  batch/online/streaming serving.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Model Serving And Scaling

## Purpose

A model that scores well offline still has to be served: it needs to handle
production traffic patterns within a latency budget, scale up and down with
demand without wasting money on idle GPUs, and roll out new versions without
a single bad deploy taking down the whole user base. Model serving and
scaling is the operational layer between "we have a good model" and "users
get fast, reliable, cost-effective predictions" — and it is where most of the
recurring infrastructure cost and the highest-blast-radius incidents (a bad
rollout to 100% of traffic) actually live.

## When to use

- The user is choosing a serving pattern (online/real-time, batch, or
  streaming) for a model or deciding between them for a given use case.
- The user needs to set up or tune autoscaling for a model inference
  endpoint (Kubernetes HPA, KServe, SageMaker endpoints, Vertex AI
  endpoints, or a custom autoscaler).
- The user is trying to reduce inference latency (cold start, batching,
  quantization, hardware choice) or inference cost.
- The user wants to design a canary, shadow, or blue/green rollout for a new
  model version.
- The user is serving an LLM and needs to think about request batching,
  KV-cache management, or GPU memory sizing.
- The user is debugging inference latency spikes, cold-start latency, or
  endpoint cost overruns.

## Prerequisites & environment

- A packaged, versioned model artifact ready to serve (see
  [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)).
- A serving runtime: TorchServe, Triton Inference Server, KServe, BentoML,
  a cloud-managed endpoint (SageMaker, Vertex AI, Azure ML), or, for LLMs,
  vLLM/TGI (Text Generation Inference) for high-throughput batched
  inference.
- A container/orchestration platform (Kubernetes ≥ 1.25 typical for
  self-managed serving) or a managed inference service.
- Defined latency and throughput SLOs for the use case (e.g. p95 ≤ 200 ms
  for a synchronous user-facing call) before choosing hardware/batching
  strategy — sizing decisions are meaningless without a target.
- Monitoring already wired to track latency, error rate, and (per
  [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md))
  prediction quality once deployed.
- GPU or CPU inventory/quota appropriate to the model size — e.g. a 7B
  parameter LLM in fp16 needs roughly 14+ GB of GPU memory just for weights,
  before accounting for KV-cache and batching overhead; validate actual
  memory needs empirically per model and serving stack rather than assuming.

## Step-by-step guidance

1. **Choose the serving pattern based on latency tolerance, not habit:**
   - **Online/real-time** (synchronous request/response): needed when a
     user or an upstream service is waiting on the result within a tight
     latency budget (typically tens to low-hundreds of milliseconds).
   - **Batch**: appropriate when predictions are needed on a schedule over a
     large dataset with no per-request latency requirement (e.g. nightly
     churn scoring for the whole customer base) — much cheaper per
     prediction since it can run on spot/preemptible capacity and maximize
     throughput via large batch sizes.
   - **Streaming**: appropriate when predictions need to happen continuously
     on an event stream (e.g. real-time fraud scoring on a transaction
     stream) with moderate latency tolerance (seconds, not milliseconds).
2. **Right-size the serving hardware to the model and SLO**, validated with
   a load test on realistic input shapes — don't extrapolate from a single
   warm request.
3. **Configure autoscaling on a signal that reflects actual load**, not just
   CPU utilization for GPU-bound or I/O-bound inference workloads. Example
   Kubernetes HPA using a custom metric (requests-in-flight or queue depth):
   ```yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: fraud-scorer-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: fraud-scorer-serving
     minReplicas: 2
     maxReplicas: 20
     metrics:
       - type: Pods
         pods:
           metric:
             name: inference_requests_in_flight
           target:
             type: AverageValue
             averageValue: "10"
     behavior:
       scaleDown:
         stabilizationWindowSeconds: 300   # avoid flapping on brief dips
       scaleUp:
         stabilizationWindowSeconds: 0
         policies:
           - type: Percent
             value: 100
             periodSeconds: 60
   ```
4. **Keep a warm minimum replica count** (`minReplicas: 2` above) sized to
   avoid cold-start latency for the baseline traffic level — scale-to-zero
   is attractive for cost but reintroduces cold-start latency on the next
   request, which may violate latency SLOs for user-facing paths.
5. **For LLM serving specifically**, use a batching-aware inference server
   (vLLM, TGI, Triton with dynamic batching) rather than naive one-request-
   at-a-time serving — continuous/dynamic batching materially improves GPU
   utilization and throughput for transformer inference. Size KV-cache
   memory budget explicitly against expected concurrent sequence count and
   max sequence length.
6. **Roll out new model versions progressively, never straight to 100%**:
   - **Shadow**: send production traffic to the new version in parallel,
     log its predictions, but don't act on them — compare offline before
     any user-facing exposure.
   - **Canary**: route a small percentage (e.g. 5%) of live traffic to the
     new version, monitor latency/error rate/prediction quality proxies,
     and ramp up gradually (5% → 25% → 50% → 100%) only as each stage looks
     healthy.
   - **Blue/green**: run both versions fully provisioned, cut traffic over
     at once — faster full rollout, fastest possible rollback (flip
     traffic back), but doubles resource cost during the transition window.
7. **Automate the rollback trigger** where possible — a canary stage that
   breaches an error-rate or latency threshold should automatically halt
   the rollout and revert traffic, not wait for a human to notice a
   dashboard.
8. **Never delete or deprovision the previous production serving
   deployment until the new version has been fully validated at 100%
   traffic for a reasonable soak period** — keep it scaled down but
   available for fast rollback, not torn down immediately after cutover.
9. **Track cost per prediction** alongside latency — right-sizing replica
   count, batch size, and hardware choice (e.g. spot instances for batch,
   smaller/quantized models where quality allows) is a recurring operational
   task, not a one-time setup step.

## Best practices

- Define latency/throughput SLOs before choosing hardware or a serving
  framework — "make it fast" without a target leads to over- or
  under-provisioning.
- Load test with realistic input distributions (payload size, batch
  composition, concurrency pattern) rather than a synthetic single-request
  benchmark that doesn't reflect production traffic shape.
- Prefer progressive rollout (canary or shadow) as the default for any model
  version change, reserving instant blue/green cutover for cases where
  canarying isn't feasible (e.g. a hard schema break).
- Separate the serving runtime's health (process up, responding) from model
  health (predictions still good) in monitoring — a healthy process serving
  degraded predictions is the more dangerous failure mode.
- Quantize or distill where quality tolerates it, particularly for LLMs —
  meaningful latency/cost reductions are often available at acceptable
  quality cost, but validate the quality impact on your actual eval set
  before committing, not just on published leaderboard numbers.
- Keep serving configuration (replica counts, autoscaling thresholds,
  hardware type) in version control alongside the model version it's tuned
  for — these are coupled and should change together deliberately, not
  drift independently.

## Common pitfalls

- **Symptom:** A new model version is rolled out to 100% of traffic and an
  hour later a subtle regression (e.g. a schema mismatch causing garbage
  predictions on 3% of requests) is discovered, after it has already
  affected the full user base.
  **Fix:** Always canary or shadow a new version before full cutover, with
  automated health checks (error rate, latency, and where available a
  prediction-quality proxy) gating each ramp-up stage — never treat
  "deploy straight to 100%" as a safe default, and always keep the previous
  version's deployment ready for immediate rollback rather than tearing it
  down on cutover.

- **Symptom:** An endpoint scaled to zero (or a very low minimum) during
  off-peak hours causes the first request after an idle period to take
  several seconds to multiple times longer than steady-state latency (cold
  start), breaching the latency SLO intermittently and unpredictably.
  **Fix:** Keep a warm minimum replica count sized to the lowest expected
  traffic level rather than scaling to zero for latency-sensitive online
  serving; reserve scale-to-zero for genuinely latency-tolerant batch/async
  workloads.

- **Symptom:** Autoscaling is configured on CPU utilization for a GPU-bound
  model server, so the autoscaler never triggers even though GPU is
  saturated and request queues are growing, causing latency to degrade
  silently under load.
  **Fix:** Scale on a signal that reflects the actual bottleneck — GPU
  utilization, requests-in-flight, or queue depth for GPU/I/O-bound
  workloads — not CPU utilization, which is frequently a poor proxy for
  inference server load.

- **Symptom:** Someone runs a cleanup that deprovisions the prior model
  version's serving deployment immediately after cutover to save cost, and
  the team then can't roll back quickly when the new version has issues a
  day later.
  **Fix:** Keep the previous version's deployment scaled down (not deleted)
  for a defined soak period after cutover; treat immediate deprovisioning of
  the last-known-good serving deployment as a destructive action requiring
  explicit confirmation, not routine cleanup.

## Worked example

Rolling out `fraud-scorer` version 14 (from
[model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md))
to replace version 13 in production.

1. **SLO:** p95 latency ≤ 50 ms per scoring request, sustained throughput up
   to 2,000 requests/second at peak.
2. **Load test:** version 14 is load tested at 2x expected peak traffic on
   the target hardware (2 vCPU / 4 GB per replica), confirming p95 latency
   of 38 ms and identifying that 6 replicas comfortably cover peak load with
   headroom.
3. **Autoscaling:** HPA configured with `minReplicas: 4` (covers steady-state
   traffic with no cold start), `maxReplicas: 20`, scaling on
   `inference_requests_in_flight`.
4. **Shadow phase (24h):** version 14 receives a mirrored copy of production
   traffic; its predictions are logged but not acted on. Comparison against
   version 13's live predictions shows no unexpected divergence.
5. **Canary phase:** 5% of live traffic routed to version 14 for 24 hours;
   latency, error rate, and false-positive-rate proxy all remain within
   expected bounds. Ramped to 25%, then 50%, then 100% over the following
   three days, each stage gated on the same health checks.
6. **Post-cutover:** version 13's deployment is scaled down to a single
   standby replica (not deleted) for a two-week soak period, giving instant
   rollback capability while version 14 is monitored in production (see
   [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md))
   before version 13's resources are finally reclaimed.

## Cross-references

- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)
- [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)
- [llmops-fine-tuning-and-deployment](../llmops-fine-tuning-and-deployment/SKILL.md)
