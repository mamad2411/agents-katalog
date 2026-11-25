---
name: argo-rollouts-progressive-delivery
description: >
  Configures the Argo Rollouts `Rollout` CRD as a drop-in replacement for
  a Kubernetes `Deployment`, covering canary and blue-green strategy
  mechanics, traffic management integration (service mesh/ingress
  controllers), and `AnalysisTemplate`/`AnalysisRun` for automated
  metric-based promotion and rollback. Use when the user asks to
  "convert a Deployment to an Argo Rollout," "configure canary steps with
  setWeight/pause," "wire up an AnalysisTemplate against Prometheus/
  Datadog," "fix a Rollout stuck mid-canary," or "automate rollback on
  bad metrics with Argo Rollouts."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: gitops-argo-ecosystem
  maturity: stable
---

# Argo Rollouts Progressive Delivery

## Purpose

Argo Rollouts replaces the Kubernetes `Deployment` controller with a
`Rollout` CRD that understands canary and blue-green *strategies* natively
— traffic-weighted steps, paused promotion gates, and automated
analysis-driven rollback — rather than the all-or-nothing rolling update a
plain `Deployment` performs. This skill assumes you already know *why*
progressive delivery reduces blast radius (see
[blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md)
for the tool-agnostic rationale and a introductory Argo Rollouts example)
and goes deep on the `Rollout` CRD's actual mechanics: strategy
configuration, traffic-provider integration, `AnalysisTemplate` metric
providers, and the controller/CLI operations for inspecting and
recovering a rollout in progress. This matters operationally because a
misconfigured analysis query or traffic-routing integration doesn't fail
loudly — it silently produces a rollout that never promotes, never rolls
back, or (worse) reports healthy while serving errors.

## When to use

- Migrating an existing `Deployment` to a `Rollout` to gain canary/
  blue-green strategies.
- Configuring canary `steps` (weights, pauses, analysis gates) or a
  blue-green strategy's preview/active service split.
- Wiring an `AnalysisTemplate` to a specific metrics backend (Prometheus,
  Datadog, CloudWatch, Wavefront, New Relic, or a Kubernetes `Job`-based
  custom check) to gate promotion automatically.
- Integrating traffic management (Istio `VirtualService`, NGINX/ALB
  ingress annotations, SMI, or Argo Rollouts' native traffic router) so
  canary weight actually controls real traffic split, not just replica
  count.
- Diagnosing a `Rollout` stuck `Paused`/`Progressing` indefinitely, or one
  that promoted/rolled back unexpectedly.
- Deciding rollback strategy: `abort` vs. `undo` vs. manual `promote`.

## Prerequisites & environment

- Argo Rollouts controller ≥ 1.6 installed cluster-wide, plus the
  `kubectl argo rollouts` plugin (or standalone `kubectl-argo-rollouts`
  binary) matching the controller's major version for CLI operations and
  the terminal dashboard (`kubectl argo rollouts dashboard`).
- For **canary with real traffic-weighting** (not just replica-ratio
  approximation): a supported traffic provider — Istio, NGINX Ingress
  (with the `nginx.ingress.kubernetes.io/canary*` annotations Argo
  Rollouts manages), AWS ALB Ingress Controller, SMI, or Traefik. Without
  one, canary weight is approximated by pod replica ratio, which is
  coarse-grained at low replica counts (a 10% weight target with 3 total
  replicas cannot be represented exactly).
- For **automated analysis**: a metrics backend reachable from the
  cluster (Prometheus is the most common `AnalysisTemplate` provider) with
  the queries/dashboards for the service's key signals already defined —
  this skill assumes those metrics already exist, not that you build
  observability from scratch (see
  [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)
  for that).
- The workload's existing `Deployment` manifest, to be converted (`kind:
  Deployment` → `kind: Rollout`, `spec.strategy` replaced).

## Step-by-step guidance

1. **Convert a `Deployment` to a `Rollout`** — same `spec.template`,
   `spec.selector`, `spec.replicas`; `spec.strategy` is replaced with an
   Argo Rollouts strategy block:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Rollout
   metadata:
     name: payments-api
   spec:
     replicas: 10
     revisionHistoryLimit: 5
     selector:
       matchLabels: { app: payments-api }
     template:
       metadata:
         labels: { app: payments-api }
       spec:
         containers:
           - name: payments-api
             image: ghcr.io/example/payments-api:1.4.2
     strategy:
       canary: {}   # or blueGreen: {} — filled in below
   ```
   A plain `Deployment` cannot be edited in-place into a `Rollout` (they
   are different kinds); apply the new `Rollout` and delete the old
   `Deployment` deliberately, or use `kubectl argo rollouts` tooling to
   assist migration (`argo rollouts convert deployment` pattern varies by
   version — verify by checking `kubectl argo rollouts --help` for the
   installed version).

2. **Configure canary steps with weighted traffic and an analysis gate**,
   using an Istio `VirtualService` reference for real traffic split:
   ```yaml
   spec:
     strategy:
       canary:
         canaryService: payments-api-canary
         stableService: payments-api-stable
         trafficRouting:
           istio:
             virtualService:
               name: payments-api-vsvc
               routes: [primary]
         steps:
           - setWeight: 10
           - pause: { duration: 5m }
           - analysis:
               templates: [{ templateName: success-rate-check }]
               args:
                 - { name: service-name, value: payments-api-canary }
           - setWeight: 50
           - pause: { duration: 10m }
           - setWeight: 100
   ```
   The `canaryService`/`stableService` pair and `trafficRouting.istio`
   block are what let Argo Rollouts actually shift the declared *traffic
   percentage* via the mesh, independent of the canary/stable ReplicaSet's
   relative pod counts — without `trafficRouting` configured, `setWeight`
   only approximates weight via replica ratio.

3. **Configure blue-green** when you want a full environment swap with an
   explicit promotion gate rather than incremental traffic weighting:
   ```yaml
   spec:
     strategy:
       blueGreen:
         activeService: payments-api-active
         previewService: payments-api-preview
         autoPromotionEnabled: false
         prePromotionAnalysis:
           templates: [{ templateName: smoke-test-check }]
         scaleDownDelaySeconds: 300
   ```
   `previewService` lets you (or an automated smoke test) hit the new
   version directly before flipping `activeService`;
   `autoPromotionEnabled: false` requires an explicit
   `kubectl argo rollouts promote payments-api`;
   `scaleDownDelaySeconds` keeps the old ReplicaSet warm after promotion
   so an immediate rollback doesn't require a cold start.

4. **Define `AnalysisTemplate`s against the metrics that actually gate
   promotion**, parameterized so the same template works for canary and
   ad hoc runs:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: AnalysisTemplate
   metadata:
     name: success-rate-check
   spec:
     args:
       - name: service-name
     metrics:
       - name: error-rate
         interval: 1m
         count: 5
         successCondition: result[0] <= 0.01
         failureLimit: 2
         provider:
           prometheus:
             address: http://prometheus.monitoring:9090
             query: |
               sum(rate(http_requests_total{service="{{args.service-name}}",status=~"5.."}[5m]))
               /
               sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))
   ```
   `count: 5` with `failureLimit: 2` means the analysis samples the query
   5 times at the given interval and tolerates up to 2 failing samples
   before failing the whole analysis — tune both, not just the threshold,
   since a single noisy sample shouldn't abort an otherwise-healthy
   rollout.

5. **Use a background `AnalysisRun` for checks that should run for the
   whole rollout duration**, not just at a discrete step, when metric
   noise or slow-to-manifest regressions matter:
   ```yaml
   steps:
     - setWeight: 20
     - analysis:
         templates: [{ templateName: success-rate-check }]
       # background analysis via .spec.strategy.canary.analysis (not a step)
   ```
   Configuring `spec.strategy.canary.analysis` (as opposed to a step-level
   `analysis`) runs the `AnalysisRun` continuously in the background for
   the rollout's full duration, aborting immediately if it fails at any
   point — appropriate for slow-onset regressions a single-step check at
   10% weight might miss.

6. **Operate the rollout: inspect, pause, promote, abort, roll back:**
   ```bash
   kubectl argo rollouts get rollout payments-api --watch
   kubectl argo rollouts promote payments-api            # skip remaining pause/advance one step
   kubectl argo rollouts promote payments-api --full      # skip straight to 100%
   kubectl argo rollouts pause payments-api               # manually pause an in-progress rollout
   kubectl argo rollouts abort payments-api               # halt, revert traffic to stable
   kubectl argo rollouts undo payments-api                # revert to previous revision entirely
   ```
   > **Warning — destructive/overriding action:** `promote --full` skips
   > *all* remaining steps and analysis gates, going straight to 100%
   > traffic on the new version. Reserve it for cases where you've
   > independently verified health and are deliberately bypassing the
   > configured gates (e.g., analysis is known-broken and you've verified
   > manually) — it is not a "speed up a slow rollout" shortcut for
   > routine releases.

7. **Set `dryRun`/`measurementRetention` and dashboard for observability
   into why an analysis failed:**
   ```bash
   kubectl argo rollouts dashboard   # local web UI: http://localhost:3100
   kubectl get analysisrun -n <ns>
   kubectl describe analysisrun <name> -n <ns>   # per-measurement results
   ```

## Best practices

- Always pair `trafficRouting` with a real mesh/ingress integration for
  services where precise weight matters — relying on replica-ratio
  approximation at low replica counts (e.g., 3 replicas) means `setWeight:
  10` can't actually be represented and rounds to the nearest whole pod.
- Set `analysis` at the background (whole-rollout) level for regressions
  that manifest slowly (memory leaks, cache-warmup-dependent latency), and
  step-level `analysis` for fast-onset regressions (error rate spikes) —
  using only step-level checks can let a rollout fully promote before a
  slow regression shows up.
- Tune `count`/`failureLimit`/`interval` together with the success
  threshold — a single flaky sample aborting an otherwise-good rollout
  erodes trust in the gate exactly like the generic canary-noise pitfall
  in [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md).
- Keep `scaleDownDelaySeconds` (blue-green) or the canary ReplicaSet's
  scale-down timing non-zero so a same-minute rollback doesn't require a
  fresh cold start on the previous version.
- Version-pin the exact image tag/digest under analysis — an
  `AnalysisRun`'s results are only attributable to a specific build if the
  tag didn't move mid-rollout; combine with
  [container-build-and-release](../../../devops/skills/container-build-and-release/SKILL.md)'s
  immutable-tag guidance.
- Manage `Rollout` specs the same way as any other GitOps-tracked
  resource — see
  [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
  for how an `Application`'s sync policy and health checks interact with a
  `Rollout` (Argo CD has native `Rollout` health-check support built in,
  unlike arbitrary CRDs).

## Common pitfalls

- **Symptom:** A canary rollout is stuck at an intermediate `setWeight`
  (e.g., 20%) indefinitely, with no error surfaced.
  **Fix:** Distinguish a manual `pause: {}` (no duration — waits for an
  explicit `promote`) from an `analysis` step whose `AnalysisRun` is
  stuck `Inconclusive`/never satisfying its success condition. Run
  `kubectl get analysisrun -n <ns>` and `kubectl describe analysisrun
  <name>` — a common root cause is a Prometheus query referencing a label
  selector that doesn't match the canary Pods' actual labels, so the
  query returns no data and never satisfies `successCondition`.

- **Symptom:** Argo CD shows the `Rollout` as perpetually `Progressing`,
  never `Healthy`, even though `kubectl argo rollouts get rollout` shows
  it fully promoted at 100%.
  **Fix:** Confirm Argo CD's version has native `Rollout` health check
  support enabled (bundled in recent Argo CD releases) — an outdated
  or misconfigured Argo CD install falls back to generic health logic
  that doesn't understand `Rollout` status subresources correctly.

- **Symptom:** `kubectl argo rollouts abort` was run to stop a bad
  canary, but traffic didn't fully revert to the stable version for
  several minutes.
  **Fix:** Check the traffic provider's own propagation delay (Istio
  `VirtualService`/`DestinationRule` changes, ALB target group
  deregistration) — `abort` updates the `Rollout`'s desired traffic split
  immediately, but the underlying mesh/ingress controller still needs its
  normal reconciliation/propagation time; this is a traffic-provider
  characteristic, not an Argo Rollouts bug, and matters when setting
  incident-response expectations.

- **Symptom:** A background `analysis` correctly detects a regression and
  aborts, but the canary ReplicaSet's pods keep running and consuming
  resources well after the abort.
  **Fix:** `abort` reverts traffic and marks the rollout degraded but by
  default does not immediately scale down the canary ReplicaSet — check
  `scaleDownDelaySeconds`/`abortScaleDownDelaySeconds` settings; set an
  explicit `abortScaleDownDelaySeconds` if leftover canary capacity is a
  cost/security concern rather than assuming abort tears everything down
  instantly.

- **Symptom:** Promoting via `kubectl argo rollouts promote --full` was
  used routinely "to save time," and a genuinely bad release reached
  100% traffic because every analysis gate was skipped along with the
  pauses.
  **Fix:** `--full` bypasses *all* remaining steps and analysis, not just
  the timed pauses — reserve it strictly for cases where health was
  already verified through another path; for routine speed-ups, shorten
  `pause.duration` values in the `Rollout` spec itself instead so the
  analysis gates still run.

## Worked example

**Scenario:** Convert `payments-api` to a canary `Rollout` with
Istio-based traffic weighting, a background error-rate analysis for the
whole rollout duration, and a step-level latency check before reaching
50% weight.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: payments-api
spec:
  replicas: 10
  revisionHistoryLimit: 5
  selector:
    matchLabels: { app: payments-api }
  template:
    metadata:
      labels: { app: payments-api }
    spec:
      containers:
        - { name: payments-api, image: ghcr.io/example/payments-api:1.4.2 }
  strategy:
    canary:
      canaryService: payments-api-canary
      stableService: payments-api-stable
      trafficRouting:
        istio:
          virtualService: { name: payments-api-vsvc, routes: [primary] }
      analysis:
        templates: [{ templateName: error-rate-background }]
      steps:
        - setWeight: 10
        - pause: { duration: 5m }
        - analysis:
            templates: [{ templateName: latency-check }]
        - setWeight: 50
        - pause: { duration: 10m }
        - setWeight: 100
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: error-rate-background
spec:
  metrics:
    - name: error-rate
      interval: 1m
      count: 30
      failureLimit: 3
      successCondition: result[0] <= 0.01
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_requests_total{service="payments-api-canary",status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{service="payments-api-canary"}[5m]))
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: latency-check
spec:
  metrics:
    - name: p99-latency
      interval: 1m
      count: 5
      successCondition: result[0] <= 0.3
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="payments-api-canary"}[5m])) by (le))
```

If `error-rate-background`'s continuous check fails at any point (say, 8
minutes in, after already passing the 5-minute `latency-check` gate at
10% weight), the whole rollout aborts and traffic reverts fully to
`payments-api-stable` — demonstrating why the background analysis
matters even after a step-level gate has already passed.

## Cross-references

- [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
- [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md)
- [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md)
- [container-build-and-release](../../../devops/skills/container-build-and-release/SKILL.md)
