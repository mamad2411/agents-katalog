---
name: knative-serverless-configuration
description: >
  Configures Knative Serving on Kubernetes — Service/Revision resources,
  scale-to-zero and concurrency-based autoscaling, and traffic splitting
  across revisions for canary/blue-green rollouts. Use when the user
  asks to "deploy a Knative Service," "scale a Knative revision to
  zero," "split traffic between Knative revisions," "canary a Knative
  deploy," "why won't my Knative pod scale down," or "run serverless
  workloads on our own Kubernetes cluster."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: serverless-and-alternative-compute
  maturity: stable
---

# Knative Serverless Configuration

## Purpose

Knative Serving brings the request-driven, scale-to-zero model of
managed FaaS platforms to any container running on Kubernetes — a
`Service` resource generates immutable `Revision`s on every spec change,
each revision scales independently based on concurrent request load
(down to zero when idle), and traffic is explicitly split across
revisions rather than always routing to "latest." This is the
foundation-level skill for running serverless workloads on
self-managed or on-prem Kubernetes without depending on a cloud
provider's FaaS product; validating the resulting config before deploy
is covered separately in
[knative-configuration-validation](../knative-configuration-validation/SKILL.md),
and event routing (as opposed to request-driven serving) is covered in
[knative-eventing-configuration](../knative-eventing-configuration/SKILL.md).

## When to use

- Standing up a new Knative `Service` for an HTTP workload that should
  scale to zero when idle.
- Tuning autoscaling behavior (`target` concurrency, min/max scale,
  scale-down delay) for a revision that either cold-starts too often or
  never scales down.
- Splitting traffic between two revisions for a canary rollout or
  blue/green cutover.
- Diagnosing a Knative revision stuck at one replica, or one that scales
  down before in-flight requests finish.
- Deciding whether a workload belongs on Knative Serving vs. a plain
  Kubernetes `Deployment` vs. a managed FaaS platform.

## Prerequisites & environment

- A Kubernetes cluster (≥ 1.27 recommended for current Knative Serving
  releases — check the specific Knative release's support matrix, since
  minimum Kubernetes version requirements move with each Knative minor
  version) with Knative Serving installed, plus a networking layer
  (Kourier, Istio, or Contour) configured as the ingress.
- `kubectl` and, optionally, the `kn` CLI for a friendlier interactive
  workflow (`kubectl` + YAML is used here since it's what CI pipelines
  apply).
- Cluster-autoscaler or sufficient static node capacity — Knative scales
  pods, not nodes; if the underlying node pool can't grow, pod-level
  scale-up requests will queue or fail regardless of Knative
  configuration.
- Familiarity with standard Kubernetes resource requests/limits, since
  Knative `Revision`s are still ordinary pods underneath and are subject
  to the same scheduling constraints.

## Step-by-step guidance

1. **Define the `Service` as the single source of truth**; every applied
   change creates a new immutable `Revision`:
   ```yaml
   apiVersion: serving.knative.dev/v1
   kind: Service
   metadata:
     name: checkout-api
     namespace: prod
   spec:
     template:
       metadata:
         annotations:
           autoscaling.knative.dev/target: "50"
           autoscaling.knative.dev/min-scale: "1"
           autoscaling.knative.dev/max-scale: "20"
       spec:
         containers:
           - image: registry.example.com/checkout-api:1.4.2
             resources:
               requests: { cpu: "250m", memory: "256Mi" }
               limits: { cpu: "1", memory: "512Mi" }
             ports:
               - containerPort: 8080
   ```
   `metadata.name` here becomes the `Service` name; each `kubectl apply`
   with a changed `spec.template` produces a new `Revision`
   (`checkout-api-00002`, etc.) without touching prior revisions.

2. **Set autoscaling annotations to match the workload's actual
   concurrency profile**, not defaults copied from an example:
   - `autoscaling.knative.dev/target` — the concurrent-request target
     per pod the autoscaler tries to maintain; too high causes latency
     spikes under burst, too low over-provisions pods.
   - `autoscaling.knative.dev/min-scale` — floor on replica count; `0`
     enables true scale-to-zero (accepting a cold start on the next
     request after idle), `1`+ keeps at least that many pods warm.
   - `autoscaling.knative.dev/max-scale` — ceiling on replica count,
     sized against downstream capacity exactly as with any autoscaler.
   - `autoscaling.knative.dev/scale-down-delay` — how long to wait
     before scaling down after load drops, avoiding thrashing on bursty
     traffic.
   ```yaml
   annotations:
     autoscaling.knative.dev/target: "50"
     autoscaling.knative.dev/min-scale: "0"
     autoscaling.knative.dev/max-scale: "20"
     autoscaling.knative.dev/scale-down-delay: "30s"
   ```

3. **Split traffic across revisions explicitly**, rather than always
   pointing 100% at `@latest`, once more than one revision exists:
   ```yaml
   apiVersion: serving.knative.dev/v1
   kind: Service
   metadata:
     name: checkout-api
     namespace: prod
   spec:
     template:
       metadata:
         name: checkout-api-00002
       spec:
         containers:
           - image: registry.example.com/checkout-api:1.5.0
     traffic:
       - revisionName: checkout-api-00001
         percent: 90
       - revisionName: checkout-api-00002
         percent: 10
         tag: canary
   ```
   The `tag: canary` field also creates a stable, addressable URL
   (`canary-checkout-api.prod.example.com`) for the new revision,
   letting the canary be hit directly for validation before shifting
   more of the `traffic` percentage split to it.

4. **Promote or roll back by adjusting the `traffic` block only** — no
   redeploy needed to shift percentages:
   ```bash
   kubectl patch ksvc checkout-api -n prod --type=merge -p '
   {"spec":{"traffic":[
     {"revisionName":"checkout-api-00001","percent":50},
     {"revisionName":"checkout-api-00002","percent":50,"tag":"canary"}
   ]}}'
   ```
   Rolling back to 100% on the prior revision is the same patch with
   `percent: 100` on `checkout-api-00001` and the new revision removed
   (or set to `0`) — no image rebuild or redeploy required, since the
   old revision's pods are simply scaled back up if they'd scaled down.

5. **Confirm graceful scale-down doesn't drop in-flight requests.** The
   `terminationGracePeriodSeconds` on the revision's pod template
   (inherited from the standard Kubernetes pod spec) should exceed the
   longest expected request duration, so Knative's scale-down doesn't
   SIGKILL a pod mid-request:
   ```yaml
   spec:
     template:
       spec:
         timeoutSeconds: 300
         containers:
           - image: registry.example.com/checkout-api:1.5.0
   ```
   `timeoutSeconds` here bounds how long Knative will wait for a
   response before considering the request failed — set it to
   comfortably exceed the workload's real p99 latency.

6. **Decide Knative Serving vs. a plain `Deployment` per workload**, not
   as a blanket platform choice: request-driven workloads with bursty
   or intermittent traffic that benefit from scale-to-zero and built-in
   revision/traffic-splitting are a good fit; always-on workloads with
   steady baseline traffic (where scale-to-zero never triggers and the
   revision/traffic machinery adds no value) are often simpler as a
   plain `Deployment` + HPA.

## Best practices

- Set `min-scale: 0` only for genuinely bursty/intermittent workloads
  that can tolerate a cold start; for latency-sensitive paths, use
  `min-scale: 1`+ and treat it as a deliberate cost/latency tradeoff,
  the same discipline as `min-instances` on managed FaaS platforms.
- Always route through the `traffic` block's percentage split for
  production changes, using a `tag`-based canary URL to validate a new
  revision under a small percentage of production traffic before
  shifting further.
- Size `resources.requests`/`limits` on the revision template
  realistically — Knative's autoscaler reacts to concurrent requests,
  not CPU, so a pod that's resource-starved under its own concurrency
  target will still look "healthy" to the autoscaler while actually
  degrading.
- Keep old revisions around (Knative retains a configurable history) so
  a rollback is a `traffic` patch, not a rebuild — but prune very old,
  unused revisions periodically since each retained revision's pods can
  still be scaled up and consumes cluster resources when active.
- Pair Knative Serving's own autoscaling with cluster-level node
  autoscaling — a `max-scale` that's achievable in principle but can't
  actually schedule new pods due to node capacity limits behaves the
  same as a `max-scale` that's too low.

## Common pitfalls

- **Symptom:** A revision never scales down to zero even after
  extended idle time.
  **Fix:** Check for `min-scale` set above `0` (deliberately or by a
  copied-and-forgotten annotation), an external health-check/monitoring
  probe generating steady low-level traffic, or a `scale-down-delay`
  set unreasonably high; confirm the actual annotation values with
  `kubectl get revision <name> -o jsonpath='{.metadata.annotations}'`.

- **Symptom:** In-flight requests get cut off (client sees a connection
  reset) during scale-down under fluctuating traffic.
  **Fix:** `terminationGracePeriodSeconds`/`timeoutSeconds` on the
  revision's pod spec is shorter than real request duration; raise it
  to comfortably exceed observed p99 latency so Knative waits for
  requests to complete before terminating a scaling-down pod.

- **Symptom:** A canary revision tagged and routed to 10% of traffic
  shows healthy metrics, but the full rollout at 100% immediately
  degrades.
  **Fix:** 10% of traffic may not have exercised a code path or load
  pattern that only appears at full traffic volume (e.g. a connection
  pool sized for the canary's share, not full production load); size
  canary resource limits/connection pools for eventual 100% traffic
  even while receiving only a fraction, or extend the canary duration
  and traffic percentage before full cutover.

- **Symptom:** Cold starts on a `min-scale: 0` revision are much slower
  than expected, causing user-visible timeouts on the first request
  after idle.
  **Fix:** Check the container image size and startup time (an
  uncompressed/unoptimized image or a slow application bootstrap adds
  directly to cold-start latency) — reduce image size, or move the
  workload to `min-scale: 1`+ if the cold-start latency can't be
  reduced enough to meet the SLO.

- **Symptom:** `max-scale` is set generously, but the revision still
  can't scale past a lower number of pods under real load.
  **Fix:** The cluster's node autoscaler or static node capacity likely
  can't schedule more pods (resource requests too large for available
  node capacity, or a `ResourceQuota` on the namespace); check
  `kubectl describe pod` for the unschedulable revision's pending pods
  and the reason field, not just the Knative-level `max-scale` setting.

## Worked example

**Scenario:** Rolling out `checkout-api:1.5.0` as a canary alongside the
current `1.4.2`, with 10% of traffic on the canary, `min-scale: 1` to
avoid cold starts on this latency-sensitive path, and a plan to shift to
100% after validating error rates.

Initial state — `checkout-api-00001` running `1.4.2` at 100% traffic.
Apply the new revision without shifting traffic yet:
```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: checkout-api
  namespace: prod
spec:
  template:
    metadata:
      name: checkout-api-00002
      annotations:
        autoscaling.knative.dev/target: "50"
        autoscaling.knative.dev/min-scale: "1"
        autoscaling.knative.dev/max-scale: "20"
    spec:
      timeoutSeconds: 30
      containers:
        - image: registry.example.com/checkout-api:1.5.0
          resources:
            requests: { cpu: "250m", memory: "256Mi" }
            limits: { cpu: "1", memory: "512Mi" }
  traffic:
    - revisionName: checkout-api-00001
      percent: 100
    - revisionName: checkout-api-00002
      percent: 0
      tag: canary
```
The canary is validated directly via its tag URL
(`canary-checkout-api.prod.example.com`), then traffic is shifted
incrementally:
```bash
kubectl patch ksvc checkout-api -n prod --type=merge -p '
{"spec":{"traffic":[
  {"revisionName":"checkout-api-00001","percent":90},
  {"revisionName":"checkout-api-00002","percent":10,"tag":"canary"}
]}}'
```
After error-rate and latency metrics on the 10%-weighted canary look
healthy for the agreed validation window, traffic is shifted fully:
```bash
kubectl patch ksvc checkout-api -n prod --type=merge -p '
{"spec":{"traffic":[
  {"revisionName":"checkout-api-00002","percent":100}
]}}'
```
`checkout-api-00001` remains available (scaled to its own `min-scale`)
for an immediate rollback patch if a problem surfaces after full cutover.

## Cross-references

- [knative-configuration-validation](../knative-configuration-validation/SKILL.md) — validating the Service/Revision config and autoscaling annotations shown here before they reach production.
- [knative-eventing-configuration](../knative-eventing-configuration/SKILL.md) — the event-driven (as opposed to request-driven) Knative component, for brokers/triggers/sources instead of HTTP Services.
- [google-cloud-functions-configuration](../google-cloud-functions-configuration/SKILL.md) — Cloud Run/Cloud Functions Gen2 implements a managed variant of the same scale-to-zero, revision-based model shown here.
