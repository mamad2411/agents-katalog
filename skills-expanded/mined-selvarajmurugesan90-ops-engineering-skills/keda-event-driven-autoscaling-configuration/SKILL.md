---
name: keda-event-driven-autoscaling-configuration
description: >
  Configures KEDA (Kubernetes Event-Driven Autoscaling) `ScaledObject` and
  `ScaledJob` custom resources to scale pods based on external event-source
  metrics — Kafka consumer lag, SQS/Azure Queue depth, a Prometheus query,
  or a cron schedule — rather than only CPU/memory like the built-in HPA.
  Use when the user asks to "scale a deployment on Kafka lag," "autoscale
  on SQS queue depth," "write a KEDA ScaledObject," "scale to zero when
  idle," "add a cron-based scaling schedule," or "scale pods on a custom
  Prometheus metric." Distinct from Karpenter (which scales cluster
  nodes) and the stock HorizontalPodAutoscaler (CPU/memory only).
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# KEDA Event-Driven Autoscaling Configuration

## Purpose

The built-in Kubernetes `HorizontalPodAutoscaler` (HPA) can only scale on
metrics it understands natively — CPU and memory, or a custom/external
metric wired through the metrics API, which most teams never bother to
build. KEDA closes that gap: it runs as a **metrics adapter** that exposes
external event-source state (Kafka consumer lag, an SQS queue's message
count, a Prometheus query result, a cron window) to the standard HPA
machinery, and it can additionally **scale a workload to zero** replicas
when there is no work at all — something the stock HPA cannot do on its
own. KEDA operates entirely at the **pod** level, deciding how many
replicas of a `Deployment` (or how many `Job`s) should exist right now;
it says nothing about whether the *cluster* has enough node capacity to
run them, which is
[Karpenter](../../../observability-and-platform-extras/skills/karpenter-cluster-autoscaling/SKILL.md)'s
job. A cluster commonly runs both together: KEDA decides pod count from
event backlog, Karpenter provisions the nodes those pods land on. This
skill covers designing `ScaledObject`/`ScaledJob` and
`TriggerAuthentication` resources correctly; validating them (thresholds,
auth, cooldowns) before production is covered separately in
[keda-configuration-validation](../keda-configuration-validation/SKILL.md).

## When to use

- Scaling a `Deployment` up when a Kafka topic's consumer lag grows, and
  back down (including to zero) once the backlog drains.
- Scaling worker pods based on an AWS SQS, Azure Service Bus, or GCP
  Pub/Sub queue depth instead of CPU utilization, which correlates
  poorly with actual queue backlog for I/O-bound consumers.
- Driving scaling off an arbitrary Prometheus query (e.g. a custom
  business metric like "pending orders") rather than a resource metric.
- Running a predictable cron-based scaling schedule (e.g. scale up
  before a known daily batch window, scale down overnight).
- Converting a batch workload from a long-running `Deployment` poller
  into a `ScaledJob` that spawns one `Job` per unit of work and scales
  the number of concurrent `Job`s with backlog.
- Enabling scale-to-zero for a workload that is idle most of the time,
  to reduce cost, while ensuring cold-start latency is accounted for.

## Prerequisites & environment

- A Kubernetes cluster with the KEDA operator installed (commonly via
  the `kedacore/keda` Helm chart into a `keda` namespace), which installs
  the `keda-operator`, `keda-operator-metrics-apiserver`, and the KEDA
  CRDs (`ScaledObject`, `ScaledJob`, `TriggerAuthentication`,
  `ClusterTriggerAuthentication`).
- The target workload's `Deployment`/`StatefulSet` (for `ScaledObject`)
  already exists and is otherwise healthy — KEDA scales an existing
  workload, it does not create one.
- Network reachability from the KEDA operator to the event source
  (Kafka bootstrap brokers, the cloud queue's API endpoint, the
  Prometheus server) — a scaler that cannot reach its source fails
  silently from the workload's point of view (replica count just never
  changes) unless the operator's own logs are checked.
- Credentials for the event source (SASL/mTLS for Kafka, IAM role or
  access keys for SQS, a bearer token for a secured Prometheus) stored
  as a Kubernetes `Secret`, referenced via `TriggerAuthentication` —
  never inlined directly into the `ScaledObject` spec.
- The standard Kubernetes `metrics-server` is **not** required for KEDA
  scalers themselves (KEDA runs its own metrics adapter), but is still
  needed if the same `ScaledObject` also wants to blend in a CPU/memory
  trigger alongside an external one.

## Step-by-step guidance

1. **Start from the workload's existing scale target, and set an
   explicit floor and ceiling** — never leave `minReplicaCount` at its
   implicit default without thinking about cold-start latency:
   ```yaml
   apiVersion: keda.sh/v1alpha1
   kind: ScaledObject
   metadata:
     name: order-consumer-scaledobject
     namespace: orders
   spec:
     scaleTargetRef:
       name: order-consumer          # existing Deployment
     minReplicaCount: 1               # see warning below re: minReplicaCount: 0
     maxReplicaCount: 20
     cooldownPeriod: 300              # seconds at 0 activity before scaling toward min
     pollingInterval: 30              # seconds between metric checks
     triggers:
       - type: kafka
         metadata:
           bootstrapServers: kafka-broker-1.orders.svc:9092,kafka-broker-2.orders.svc:9092
           consumerGroup: order-consumer-group
           topic: order-events
           lagThreshold: "50"
           activationLagThreshold: "5"
         authenticationRef:
           name: order-consumer-kafka-auth
   ```
   **Warning:** `minReplicaCount: 0` (scale-to-zero) means the *first*
   event after an idle period has to wait for a pod to schedule, pull
   its image, and become ready before it's processed — for a
   latency-sensitive consumer this cold-start latency spike can violate
   an SLO even though "average" latency looks fine. Only use
   `minReplicaCount: 0` for genuinely bursty, latency-tolerant, or
   cost-dominant workloads; keep `minReplicaCount: 1` (or higher) for
   anything with a real online-latency requirement.

2. **Create a `TriggerAuthentication` referencing a Secret, not literal
   credentials in the trigger metadata**:
   ```yaml
   apiVersion: keda.sh/v1alpha1
   kind: TriggerAuthentication
   metadata:
     name: order-consumer-kafka-auth
     namespace: orders
   spec:
     secretTargetRef:
       - parameter: sasl
         name: kafka-scaler-credentials
         key: sasl-mechanism
       - parameter: username
         name: kafka-scaler-credentials
         key: username
       - parameter: password
         name: kafka-scaler-credentials
         key: password
       - parameter: tls
         name: kafka-scaler-credentials
         key: tls
   ```
   On a cloud provider, prefer workload identity over static secrets
   where the scaler supports it (`podIdentity: { provider: aws-eks }`
   for an IAM role bound via IRSA, or the Azure/GCP equivalents) so no
   long-lived credential material needs to be stored in the cluster at
   all.

3. **For a cloud queue depth trigger** (SQS shown; Azure Service Bus and
   GCP Pub/Sub scalers follow the same shape with provider-specific
   metadata keys):
   ```yaml
   apiVersion: keda.sh/v1alpha1
   kind: ScaledObject
   metadata:
     name: image-resize-worker-scaledobject
     namespace: media
   spec:
     scaleTargetRef:
       name: image-resize-worker
     minReplicaCount: 0
     maxReplicaCount: 50
     cooldownPeriod: 120
     triggers:
       - type: aws-sqs-queue
         metadata:
           queueURL: https://sqs.<REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/image-resize-jobs
           queueLength: "10"           # target messages-per-replica
           awsRegion: "<REGION>"
           identityOwner: operator     # use the KEDA operator's IRSA role
   ```
   `queueLength` is a *target*, not a hard cap: KEDA computes desired
   replicas as `ceil(currentQueueDepth / queueLength)`, bounded by
   `minReplicaCount`/`maxReplicaCount` — tune it based on how long one
   replica takes to process one message's worth of backlog, not an
   arbitrary round number.

4. **For a custom business metric**, use the Prometheus scaler against
   an existing Prometheus/Thanos endpoint:
   ```yaml
   triggers:
     - type: prometheus
       metadata:
         serverAddress: http://prometheus.monitoring.svc:9090
         metricName: pending_orders_count
         query: sum(pending_orders_total{queue="fulfillment"})
         threshold: "100"
         activationThreshold: "10"
   ```
   `threshold` sets the per-replica target the same way `queueLength`
   does for a queue scaler; `activationThreshold` (available on most
   scalers) controls the point below which KEDA scales to
   `minReplicaCount` (or zero) rather than merely capping growth — set
   it deliberately rather than leaving it equal to `threshold`, which
   would cause replicas to flap right at the boundary.

5. **For a predictable schedule, use the `cron` trigger**, typically
   combined with another trigger so cron sets a floor rather than being
   the only signal:
   ```yaml
   triggers:
     - type: cron
       metadata:
         timezone: America/New_York
         start: "0 6 * * 1-5"   # 6am weekdays
         end: "0 20 * * 1-5"    # 8pm weekdays
         desiredReplicas: "5"
     - type: kafka
       metadata:
         bootstrapServers: kafka-broker-1.orders.svc:9092
         consumerGroup: order-consumer-group
         topic: order-events
         lagThreshold: "50"
   ```
   KEDA takes the **maximum** replica count implied by any active
   trigger, so the cron trigger here guarantees at least 5 replicas
   during business hours while the Kafka trigger can still scale higher
   if lag spikes.

6. **For batch/queue-drain workloads, prefer `ScaledJob` over
   `ScaledObject`** so each unit of work gets its own `Job`/pod rather
   than being multiplexed onto a long-running consumer process:
   ```yaml
   apiVersion: keda.sh/v1alpha1
   kind: ScaledJob
   metadata:
     name: video-transcode-scaledjob
     namespace: media
   spec:
     jobTargetRef:
       parallelism: 1
       completions: 1
       backoffLimit: 2
       template:
         spec:
           containers:
             - name: transcoder
               image: registry.example.com/video-transcoder:1.4.2
           restartPolicy: Never
     minReplicaCount: 0
     maxReplicaCount: 30
     pollingInterval: 15
     successfulJobsHistoryLimit: 3
     failedJobsHistoryLimit: 3
     scalingStrategy:
       strategy: default
     triggers:
       - type: aws-sqs-queue
         metadata:
           queueURL: https://sqs.<REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/transcode-jobs
           queueLength: "1"
           awsRegion: "<REGION>"
   ```
   With `ScaledJob`, `maxReplicaCount` caps the number of **concurrent
   Jobs**, not a `Deployment`'s replica count — each scaled instance runs
   to completion and exits, which fits idempotent, one-shot batch work
   far better than an ever-running consumer pod that a `ScaledObject`
   would restart in place.

## Best practices

- Always set both `minReplicaCount` and `maxReplicaCount` explicitly —
  an unbounded `maxReplicaCount` (or one left at KEDA's default) can
  let a runaway backlog spike scale a workload out far enough to starve
  cluster capacity or a downstream dependency (a database connection
  pool, a rate-limited third-party API) that wasn't sized for that many
  concurrent callers.
- Treat `minReplicaCount: 0` as a deliberate cost/latency trade-off, not
  a default — document the expected cold-start time for the workload's
  image/readiness probe and confirm it's acceptable for the consumer of
  that workload before enabling scale-to-zero.
- Use `activationLagThreshold`/`activationThreshold` distinctly from the
  main `lagThreshold`/`threshold` so a workload doesn't flap between 0
  and 1 replicas right at the boundary of "any work at all."
- Keep `pollingInterval` proportional to how quickly the event source's
  metric actually changes — polling a slow-moving queue every 5 seconds
  wastes API calls against the source (and can hit rate limits on a
  cloud provider's queue API), while polling a fast-moving one only
  every few minutes delays reaction to a real backlog spike.
- Store event-source credentials in a `Secret` referenced by
  `TriggerAuthentication` (or use workload identity), and scope that
  Secret's RBAC access to only the namespace(s) that need it — the same
  least-privilege discipline applied to CI service accounts elsewhere in
  this repo.
- Combine a cron trigger with a reactive trigger (Kafka lag, queue
  depth) rather than relying on cron alone for workloads with a genuine
  business-hours pattern but occasional off-hours bursts.

## Common pitfalls

- **Symptom:** A workload scaled by KEDA with `minReplicaCount: 0`
  produces a burst of request timeouts or a visible latency spike every
  time it wakes up from idle.
  **Fix:** This is the cold-start cost of scale-to-zero. Either set
  `minReplicaCount: 1` (accepting the idle-cost trade-off) for anything
  with a real online-latency requirement, or pre-warm via a cron trigger
  that guarantees a floor of replicas during expected traffic windows,
  and separately reduce cold-start time itself (smaller image, faster
  readiness probe).

- **Symptom:** A `ScaledObject` targeting a `Deployment` that also has a
  manually-configured HPA on the same target shows replica count
  flapping unpredictably, or the HPA appears to be "fighting" KEDA.
  **Fix:** KEDA creates and manages its own HPA object behind the
  scenes for every `ScaledObject` — a second, independently-created HPA
  on the same `scaleTargetRef` conflicts with it. Delete the manual HPA
  and let KEDA's generated one be the only autoscaler for that target.

- **Symptom:** A `ScaledObject` never scales past `minReplicaCount`
  despite the event source clearly having a growing backlog (confirmed
  by directly checking the Kafka consumer group or queue depth).
  **Fix:** Check the `keda-operator` pod's logs for the specific
  scaler's error — most commonly a `TriggerAuthentication` referencing
  the wrong Secret key name, a network path the operator can't reach
  (firewall/security-group blocking the metrics adapter from the
  broker/queue endpoint), or a typo in `bootstrapServers`/`queueURL`.
  KEDA fails a broken trigger silently from the workload's perspective —
  it just never scales — so the operator's own logs, not the workload,
  are where the actual error surfaces.

- **Symptom:** A `ScaledJob` for a batch workload leaves large numbers
  of completed/failed `Job` objects accumulating in the namespace,
  slowing down `kubectl` operations and cluttering the namespace.
  **Fix:** Set `successfulJobsHistoryLimit` and
  `failedJobsHistoryLimit` to a small bounded number (a handful, not the
  default of keeping everything) rather than leaving cleanup to manual
  intervention.

- **Symptom:** Scaling reacts correctly to backlog growth but takes
  much longer than expected to scale back down once the backlog drains.
  **Fix:** This is very likely `cooldownPeriod` doing exactly what it's
  configured to do — KEDA intentionally waits `cooldownPeriod` seconds
  of sustained zero/low activity before scaling toward `minReplicaCount`,
  to avoid flapping on a momentarily-empty queue. Tune the value rather
  than treating the delay as a bug; a very low `cooldownPeriod` trades
  faster scale-down for more replica churn.

## Worked example

**Scenario:** `order-consumer` processes messages from the `order-events`
Kafka topic. Under normal load one replica keeps up; during flash-sale
traffic, lag can spike to thousands of messages and the team wants
automatic scale-out (bounded, to protect a downstream payment API) and
scale-back-in once the backlog clears, without ever going below one
running replica (an online consumer, not a pure batch job).

`TriggerAuthentication` referencing existing SASL credentials:
```yaml
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: order-consumer-kafka-auth
  namespace: orders
spec:
  secretTargetRef:
    - parameter: sasl
      name: kafka-scaler-credentials
      key: sasl-mechanism
    - parameter: username
      name: kafka-scaler-credentials
      key: username
    - parameter: password
      name: kafka-scaler-credentials
      key: password
```

`ScaledObject`:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-consumer-scaledobject
  namespace: orders
spec:
  scaleTargetRef:
    name: order-consumer
  minReplicaCount: 1
  maxReplicaCount: 15
  cooldownPeriod: 300
  pollingInterval: 20
  triggers:
    - type: kafka
      metadata:
        bootstrapServers: kafka-broker-1.orders.svc:9092,kafka-broker-2.orders.svc:9092
        consumerGroup: order-consumer-group
        topic: order-events
        lagThreshold: "100"
        activationLagThreshold: "10"
      authenticationRef:
        name: order-consumer-kafka-auth
```

`maxReplicaCount: 15` was chosen deliberately after confirming the
downstream payment API's connection pool and rate limit can absorb 15
concurrent consumer instances without being overwhelmed — a value picked
without that check would just move the bottleneck (and the incident)
downstream instead of preventing it. During a flash sale, lag crosses
100 messages per partition, KEDA's generated HPA scales `order-consumer`
toward 15 replicas over a few polling intervals, and once lag drops back
under the `activationLagThreshold` for a full `cooldownPeriod`, it scales
back to the `minReplicaCount` floor of 1 rather than to zero, keeping the
consumer warm for the next order.

## Cross-references

- [keda-configuration-validation](../keda-configuration-validation/SKILL.md) — validating this `ScaledObject`/`TriggerAuthentication` configuration (auth, thresholds, cooldowns) before it reaches production.
- [kubernetes-operator-development](../kubernetes-operator-development/SKILL.md) — the CRD/controller/reconciliation pattern KEDA itself is built on, useful background when debugging KEDA operator behavior directly.
- [karpenter-cluster-autoscaling](../../../observability-and-platform-extras/skills/karpenter-cluster-autoscaling/SKILL.md) — node-level autoscaling that complements KEDA's pod-level scaling; KEDA decides replica count, Karpenter provisions the nodes for them.
- [kafka-consumer-lag-and-partition-troubleshooting](../../../messaging-and-data-orchestration/skills/kafka-consumer-lag-and-partition-troubleshooting/SKILL.md) — diagnosing the underlying Kafka lag signal this skill's Kafka trigger consumes, when lag behaves unexpectedly independent of KEDA.
