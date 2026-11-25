---
name: blue-green-canary-deployments
description: >
  Designs and executes progressive delivery strategies — blue-green
  cutover, canary rollout, and traffic-shifted releases — with automated
  health checks and rollback triggers, typically on Kubernetes. Use when
  the user asks to "reduce deployment risk," "set up canary/blue-green
  deployments," "do a zero-downtime release," "gradually shift traffic to
  a new version," or "automatically roll back a bad deploy."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Blue-Green and Canary Deployments

## Purpose

Deploying a new version by simply replacing the old one ("recreate" or a
rolling update with no verification) means any regression is discovered by
users, at 100% of traffic, with rollback happening only after someone
notices. Blue-green and canary strategies exist to decouple *deploying* new
code from *exposing* it to all traffic, so that a bad release affects a
small, quickly-reversible blast radius (or none at all, in blue-green's
case) instead of the whole user base. This matters operationally because
it turns "did the deploy work?" from a question answered by incident
reports into one answered by automated health signals before full rollout.

## When to use

- A service has user-facing risk from bad releases and needs progressive
  exposure instead of an instant full cutover.
- Setting up zero-downtime deploys where the old version keeps serving
  traffic until the new version is verified healthy.
- Implementing automated canary analysis (error rate, latency, custom
  metrics) that triggers an automatic rollback rather than relying on a
  human noticing a dashboard.
- Deciding between blue-green (full environment swap) and canary
  (incremental traffic percentage) for a given service's risk profile and
  infrastructure cost tolerance.
- Diagnosing a rollout that got "stuck" partway (e.g., a canary at 20%
  traffic that never promoted or rolled back).

## Prerequisites & environment

- A deployment platform supporting traffic splitting: Kubernetes with a
  service mesh (Istio, Linkerd) or an ingress supporting weighted
  routing, or a progressive-delivery controller — Argo Rollouts ≥ 1.6 or
  Flagger ≥ 1.x are the common choices; plain Kubernetes `Deployment`
  rolling updates alone do not give you traffic-percentage control, only
  pod-replacement pacing.
- Health/metrics signals available for automated analysis: a metrics
  backend (Prometheus is the common default for both Argo Rollouts
  `AnalysisTemplate` and Flagger) exposing error rate, latency, and
  saturation for the service.
- For blue-green specifically: enough infrastructure capacity to run two
  full environments (or replica sets) simultaneously during the cutover
  window, plus a router/load balancer or DNS layer that can flip traffic
  atomically.
- Load-bearing dependencies (database schema, downstream contracts) must
  be backward/forward compatible across the two versions running
  simultaneously — see the "Common pitfalls" entry on schema migrations.

## Step-by-step guidance

1. **Choose the strategy based on risk and cost tolerance.** Blue-green
   gives instant, full-traffic rollback (flip the router back) at the
   cost of running double capacity briefly. Canary gives fine-grained,
   metric-driven risk containment (bad version only ever sees a fraction
   of traffic) at the cost of more complex automation and a longer
   rollout window. Many teams combine them: canary for routine releases,
   blue-green for high-risk or infrequent major changes.

2. **Blue-green with a Kubernetes Service selector flip** (simple
   approach, no mesh required):
   ```yaml
   # New version deployed as "green", labeled distinctly from "blue"
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: payments-api-green
   spec:
     replicas: 5
     selector:
       matchLabels: { app: payments-api, slot: green }
     template:
       metadata:
         labels: { app: payments-api, slot: green }
       spec:
         containers:
           - name: payments-api
             image: ghcr.io/example/payments-api:1.4.2
   ---
   # Cutover: flip the Service selector from slot: blue to slot: green
   apiVersion: v1
   kind: Service
   metadata:
     name: payments-api
   spec:
     selector: { app: payments-api, slot: green }   # was: slot: blue
     ports: [{ port: 80, targetPort: 3000 }]
   ```
   Verify `green` health (readiness probes green, smoke tests passing)
   *before* applying the selector flip. Keep `blue` running, unscaled,
   for a rollback window; flipping the selector back is the rollback.

3. **Canary with Argo Rollouts** (traffic-percentage steps with automated
   analysis):
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Rollout
   metadata:
     name: payments-api
   spec:
     replicas: 10
     strategy:
       canary:
         steps:
           - setWeight: 10
           - pause: { duration: 5m }
           - analysis:
               templates:
                 - templateName: success-rate-check
           - setWeight: 50
           - pause: { duration: 10m }
           - setWeight: 100
     template:
       metadata:
         labels: { app: payments-api }
       spec:
         containers:
           - name: payments-api
             image: ghcr.io/example/payments-api:1.4.2
   ---
   apiVersion: argoproj.io/v1alpha1
   kind: AnalysisTemplate
   metadata:
     name: success-rate-check
   spec:
     metrics:
       - name: error-rate
         interval: 1m
         successCondition: result[0] <= 0.01
         provider:
           prometheus:
             address: http://prometheus.monitoring:9090
             query: |
               sum(rate(http_requests_total{app="payments-api",status=~"5.."}[5m]))
               /
               sum(rate(http_requests_total{app="payments-api"}[5m]))
   ```
   The rollout automatically pauses at each step, runs the analysis
   query, and **aborts and rolls back automatically** if `error-rate`
   exceeds the threshold — no human needs to be watching for the common
   failure mode.

4. **Flagger equivalent** (canary via a `Canary` CR wrapping an existing
   Deployment, commonly paired with Istio or a supported ingress):
   ```yaml
   apiVersion: flagger.app/v1beta1
   kind: Canary
   metadata:
     name: payments-api
   spec:
     targetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: payments-api
     progressDeadlineSeconds: 600
     analysis:
       interval: 1m
       threshold: 5
       stepWeight: 10
       maxWeight: 50
       metrics:
         - name: request-success-rate
           thresholdRange: { min: 99 }
           interval: 1m
     service:
       port: 80
   ```

5. **Verify before promoting, promote deliberately.** Whether via
   `pause:` steps that require an operator to confirm (`kubectl argo
   rollouts promote payments-api`) or fully automated analysis, never
   promote to 100% purely on a fixed timer with no health signal attached
   — the whole point of canary is that the *signal*, not the clock,
   decides.

6. **Roll back explicitly when analysis fails or a human calls it.**
   ```bash
   kubectl argo rollouts abort payments-api     # halt and revert to stable
   kubectl argo rollouts undo payments-api      # revert to previous revision
   ```
   For blue-green's Service-selector approach, rollback is simply
   flipping the selector back to `blue` — keep `blue` running unscaled
   (not deleted) until `green` has fully soaked, specifically so this is
   available.

## Best practices

- Keep the previous version's environment/replica set warm (not
  terminated) for a defined soak period after cutover/promotion, so
  rollback is "flip back" rather than "redeploy from scratch."
- Base promotion/rollback decisions on the same metrics that page
  on-call for the service (error rate, latency, saturation) — a canary
  analysis using different signals than production alerting can pass
  while production alerting would have failed, or vice versa.
- Start canary weight small (5-10%) for high-traffic services — even a
  short exposure at 10% of a large fleet's traffic is a meaningful sample
  size for catching regressions without meaningful user impact.
- Ensure database/schema changes are backward-compatible with the
  previous version for the entire overlap window — both blue-green and
  canary run two versions concurrently against (usually) the same
  datastore. Use expand/contract migration patterns (add new column
  nullable → dual-write → backfill → switch reads → drop old column)
  rather than migrations that assume only the new version's code exists.
- Automate the rollback trigger; don't rely solely on a human watching a
  dashboard during the rollout window, especially for releases that ship
  outside business hours.
- Tag/version the specific image under test so canary results are
  attributable to an exact build — this is where
  [container-build-and-release](../container-build-and-release/SKILL.md)'s
  immutable-tag practice matters most; a canary running a `latest` tag
  that moved mid-rollout invalidates the whole analysis.

## Common pitfalls

- **Symptom:** Canary rollout appears stuck at an intermediate weight
  (e.g., 20%) indefinitely.
  **Fix:** Check whether a manual `pause` step is waiting on an explicit
  `promote` command that nobody issued, versus an automated analysis step
  that's failing its query (misconfigured Prometheus address/label
  selector) and therefore never satisfying its success condition — the
  fix differs (promote manually vs. fix the analysis query).

- **Symptom:** Canary/blue-green rollout passes all health checks but a
  downstream service or the database breaks once the old version is
  fully retired.
  **Fix:** This usually means a backward-incompatible schema or contract
  change shipped as part of the release — audit for migrations that
  aren't safe for both versions to run against simultaneously, and adopt
  an expand/contract pattern for future schema changes.

- **Symptom:** Automated rollback triggers on every release, even ones
  that turn out to be fine, causing the team to stop trusting (and
  eventually disable) the analysis gate.
  **Fix:** The analysis threshold is likely too tight relative to normal
  metric noise — baseline the metric's normal variance first (e.g., what
  does error rate look like across a *stable* deploy) and set thresholds
  with margin above that noise floor, rather than an arbitrary round
  number.

- **Symptom:** Blue-green cutover causes a brief spike of dropped
  connections at the exact moment of the flip.
  **Fix:** Ensure the router/Service waits for the new environment's
  readiness probes to pass *and* drains in-flight connections from the
  old environment gracefully (connection draining / `preStop` hook with a
  delay) rather than flipping and terminating old pods simultaneously.

- **Symptom:** Canary at 100% weight for a long time before someone
  notices it never finished promoting, leaving mixed versions running
  far longer than intended.
  **Fix:** Alert on rollout state (Argo Rollouts/Flagger both expose
  status conditions) explicitly, rather than treating "no alert fired"
  as equivalent to "rollout completed."

## Worked example

**Scenario:** Release `payments-api:1.4.2` as a canary, targeting a
30-minute automated rollout with an error-rate gate, on a cluster already
running Argo Rollouts.

1. Update the `Rollout` resource's image to `1.4.2` (via the GitOps
   config repo, per
   [gitops-workflow](../gitops-workflow/SKILL.md)) and let the operator
   reconcile it.
2. Argo Rollouts creates the canary ReplicaSet at `setWeight: 10` and
   begins routing 10% of traffic to `1.4.2`.
3. After the 5-minute pause, the `success-rate-check` `AnalysisTemplate`
   queries Prometheus; if 5xx rate over the last 5 minutes for the canary
   pods is ≤ 1%, analysis passes and the rollout proceeds to
   `setWeight: 50`.
4. If the analysis instead shows a 4% error rate (above the 1% threshold),
   Argo Rollouts automatically aborts: traffic weight returns to 0% for
   the canary, 100% to the stable `1.4.1` ReplicaSet, and the rollout
   status is marked `Degraded` — no manual intervention was required to
   contain the blast radius to the ~10% of traffic that saw the canary
   for those 5 minutes.
5. On success at `setWeight: 100`, the previous stable ReplicaSet (`1.4.1`)
   is scaled down but not deleted immediately, preserving a fast-rollback
   option (`kubectl argo rollouts undo payments-api`) during the
   post-release soak window.

## Cross-references

- [container-build-and-release](../container-build-and-release/SKILL.md)
- [gitops-workflow](../gitops-workflow/SKILL.md)
- [environment-promotion-strategy](../environment-promotion-strategy/SKILL.md)
