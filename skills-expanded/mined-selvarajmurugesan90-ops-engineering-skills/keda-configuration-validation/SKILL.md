---
name: keda-configuration-validation
description: >
  Validates a KEDA `ScaledObject`/`ScaledJob` configuration before
  production — confirming `TriggerAuthentication` actually resolves and
  authenticates, scaling thresholds match real workload capacity, and
  `cooldownPeriod`/`minReplicaCount` won't cause flapping or cold-start
  latency spikes. Use when the user asks to "review a KEDA ScaledObject
  before deploying," "validate TriggerAuthentication," "check if KEDA
  scaling thresholds are safe," "why does my ScaledObject never scale,"
  or "audit KEDA configs for production readiness."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# KEDA Configuration Validation

## Purpose

A KEDA `ScaledObject` that applies cleanly with `kubectl apply` gives no
guarantee it actually scales anything — a `TriggerAuthentication`
referencing the wrong Secret key, a threshold picked without regard to
how much load one replica can actually absorb, or a `cooldownPeriod` left
at a value nobody reasoned about can all pass admission and simply sit
there doing nothing useful (or actively harmful) once real traffic hits
it. Unlike a broken `Deployment`, a broken `ScaledObject` usually fails
**silently**: the workload keeps running at whatever replica count it
happened to be at, with no error surfaced anywhere the workload's own
logs or status would show it. This skill is a pre-production validation
checklist for KEDA configuration built per
[keda-event-driven-autoscaling-configuration](../keda-event-driven-autoscaling-configuration/SKILL.md),
in the same spirit as
[kafka-configuration-validation](../../../messaging-and-data-orchestration/skills/kafka-configuration-validation/SKILL.md)
and
[metallb-configuration-validation](../metallb-configuration-validation/SKILL.md)
validate their respective domains' configs before go-live.

## When to use

- Before promoting a newly authored `ScaledObject`/`ScaledJob` from
  staging to production.
- Reviewing a pull request that adds or modifies KEDA scaling
  configuration, `TriggerAuthentication`, or `ClusterTriggerAuthentication`.
- A `ScaledObject` exists and shows no errors, but the workload never
  scales up (or never scales down) as expected.
- Auditing an existing cluster's `ScaledObject`/`ScaledJob` resources for
  missing `maxReplicaCount` ceilings, missing authentication, or
  thresholds that were never validated against real capacity.
- As a gate in a CI/CD pipeline that provisions `ScaledObject`/`ScaledJob`
  resources via Helm, Kustomize, or a GitOps operator.

## Prerequisites & environment

- `kubectl` access to the namespace containing the `ScaledObject`/
  `ScaledJob` and to the `keda` (or wherever the operator is installed)
  namespace, to read operator logs.
- Read access to the event source itself (Kafka consumer group offsets,
  the cloud queue's actual depth, the Prometheus query run directly)
  independent of what KEDA reports, so KEDA's view can be cross-checked
  rather than trusted alone.
- A documented capacity baseline for the target workload — how much
  backlog one replica can process per unit time — without this, a
  threshold review has nothing concrete to validate against beyond "it's
  a number that isn't zero."
- The KEDA operator version in use (trigger metadata keys and defaults
  have changed across KEDA major versions) so the review matches the
  scaler's actual supported parameters rather than a different version's
  documentation.

## Step-by-step guidance

1. **Confirm the `ScaledObject`/`ScaledJob` actually produced a working
   HPA and is in a healthy state**, not just that the CRD applied:
   ```bash
   kubectl get scaledobject order-consumer-scaledobject -n orders
   kubectl describe scaledobject order-consumer-scaledobject -n orders
   ```
   A healthy `ScaledObject` shows `READY: True` and `ACTIVE` reflecting
   current trigger state in its status conditions, and a corresponding
   generated HPA:
   ```bash
   kubectl get hpa -n orders
   ```
   If no HPA was generated, or it shows `<unknown>` for its target
   metric, the trigger itself is failing — proceed to step 3 rather than
   assuming the workload is simply idle.

2. **Validate `TriggerAuthentication` actually resolves**, not just that
   it references a Secret that exists:
   ```bash
   kubectl get triggerauthentication order-consumer-kafka-auth -n orders -o yaml
   kubectl get secret kafka-scaler-credentials -n orders -o jsonpath='{.data}' | jq 'keys'
   ```
   Confirm every `key` referenced in `secretTargetRef` actually exists in
   the Secret's data (a key name typo is the single most common cause of
   an authentication trigger failing silently), and that the
   `TriggerAuthentication`'s namespace matches the `ScaledObject`'s
   namespace — a `TriggerAuthentication` is namespace-scoped; only a
   `ClusterTriggerAuthentication` can be referenced across namespaces.

3. **Pull the KEDA operator's own logs for the specific scaler**, since a
   failing trigger produces no error on the workload side at all:
   ```bash
   kubectl -n keda logs -l app=keda-operator --tail=200 | grep -i "order-consumer\|error"
   ```
   Look specifically for authentication failures (wrong SASL mechanism,
   expired credentials, IAM role missing a permission), connectivity
   errors (DNS resolution failure, timeout reaching the broker/queue
   endpoint — often a network policy or security group blocking the
   operator's pod network), and metadata parsing errors (a threshold or
   URL field with the wrong type/format for that scaler version).

4. **Validate scaling thresholds against actual per-replica capacity**,
   not an arbitrary round number:
   ```bash
   # Cross-check what the trigger reports vs. reality, independent of KEDA
   kafka-consumer-groups.sh --bootstrap-server broker-101:9092 \
     --describe --group order-consumer-group
   ```
   Confirm `lagThreshold`/`queueLength`/`threshold` was set from a
   measured "how much backlog can one replica clear per polling
   interval" figure (from a load test or historical throughput data),
   not copied from an example. A threshold set too low causes
   over-provisioning (cost) and can also outrun the `maxReplicaCount`
   ceiling into a downstream dependency's capacity limit; a threshold set
   too high means real backlog growth goes unaddressed for far longer
   than intended.

5. **Validate `minReplicaCount`/`maxReplicaCount` bounds are both
   present and deliberate**:
   ```bash
   kubectl get scaledobject order-consumer-scaledobject -n orders \
     -o jsonpath='{.spec.minReplicaCount}{" / "}{.spec.maxReplicaCount}{"\n"}'
   ```
   Flag any `ScaledObject`/`ScaledJob` with no explicit
   `maxReplicaCount` (KEDA's default ceiling is high enough to be
   effectively unbounded for most workloads) as a finding — an
   unconstrained ceiling can scale a workload out far enough to exhaust
   node capacity or overwhelm a downstream dependency during a genuine
   backlog spike. Separately, flag `minReplicaCount: 0` on anything
   without an explicitly reviewed and accepted cold-start latency
   budget — this is the single most consequential setting to get wrong,
   since it fails silently in normal operation and only bites during the
   exact moment a real user is waiting on the first request after idle.

6. **Validate `cooldownPeriod` and `pollingInterval` against the event
   source's actual volatility**:
   ```bash
   kubectl get scaledobject order-consumer-scaledobject -n orders \
     -o jsonpath='{.spec.cooldownPeriod}{" / "}{.spec.pollingInterval}{"\n"}'
   ```
   A `cooldownPeriod` far shorter than the natural period of the event
   source's bursts causes replica flapping (scale out, cool down, scale
   out again within minutes); a `pollingInterval` longer than the
   backlog can safely grow within delays legitimate scale-out. Neither
   has a universally "correct" value — validate both were chosen against
   the specific event source's observed pattern, not left at defaults.

7. **For `ScaledJob`, validate `backoffLimit`, job history limits, and
   that `restartPolicy: Never` is set** so failed units of work don't
   restart in place indefinitely:
   ```bash
   kubectl get scaledjob video-transcode-scaledjob -n media -o yaml | \
     grep -E "backoffLimit|restartPolicy|successfulJobsHistoryLimit|failedJobsHistoryLimit"
   ```
   Confirm history limits are set to small bounded values — an
   unbounded history of completed/failed `Job` objects degrades
   `kubectl`/API server performance over time in a namespace with high
   job churn.

8. **If configuration is managed via Helm/Kustomize/GitOps, run this
   validation against the rendered manifest in CI**, not only against
   whatever happens to already be live in the cluster:
   ```bash
   helm template order-consumer ./charts/order-consumer | \
     kubectl apply --dry-run=server -f -
   ```
   A dry-run server-side apply catches schema-level mistakes (wrong
   field name, wrong type) before merge; it does not catch the
   semantic issues in steps 2–6 above, which still require the checks
   against a running or staging cluster.

## Best practices

- Encode the non-negotiable baseline (an explicit `maxReplicaCount`, a
  reviewed decision on `minReplicaCount: 0`, `TriggerAuthentication`
  instead of inline credentials) as a policy check (OPA/Conftest, or a
  small validation script run in CI against rendered manifests) rather
  than a manual review that's easy to skip under deadline pressure.
- Validate authentication and connectivity in a staging cluster pointed
  at the same (or an equivalent) event source before promoting to
  production — a `TriggerAuthentication` that works against a staging
  Kafka cluster's ACLs can still fail against production's stricter
  ACLs if they weren't provisioned identically.
- Load-test the target workload to establish its real per-replica
  throughput before setting a threshold, rather than guessing and
  tuning reactively in production after the first incident.
- Re-validate after any change to the event source side (a Kafka
  partition count change, a queue provider migration, a Prometheus
  metric rename) — the `ScaledObject` can remain syntactically valid
  while silently referencing a topic/metric that no longer means what
  it did when the threshold was chosen.
- Track KEDA operator version alongside the cluster's Kubernetes
  version in upgrade planning — scaler metadata keys and defaults have
  changed across KEDA major versions, and a validation pass against
  stale documentation can approve a config a newer/older operator
  interprets differently.

## Common pitfalls

- **Symptom:** A `ScaledObject` shows `READY: True` in `kubectl
  describe`, but the workload never scales despite a confirmed real
  backlog.
  **Fix:** `READY` reflects that the `ScaledObject` spec itself is valid
  and the generated HPA exists — it does not confirm the trigger is
  successfully authenticating against the event source. Check the
  `keda-operator` pod logs (step 3) for the actual scaler error, which
  is invisible from the `ScaledObject`'s own status.

- **Symptom:** A `TriggerAuthentication` was created in a different
  namespace than the `ScaledObject` referencing it, and the trigger
  silently never authenticates.
  **Fix:** `TriggerAuthentication` is namespace-scoped and must live in
  the same namespace as the `ScaledObject` that references it via
  `authenticationRef`. Use a `ClusterTriggerAuthentication` instead if
  the same credential genuinely needs to be shared across namespaces,
  and scope its RBAC access accordingly.

- **Symptom:** A production `ScaledObject` was approved in review with a
  `queueLength`/`lagThreshold` copied from a different workload's
  configuration or from documentation, and the workload either
  over-scales (wasting cost) or under-reacts to real backlog growth.
  **Fix:** A threshold is not a universal constant — validate it against
  a measured per-replica throughput figure for *this* specific workload,
  from a load test or historical data, every time, rather than reusing a
  value that happened to work for a different service.

- **Symptom:** A `ScaledObject` with `minReplicaCount: 0` passes review
  with no discussion, and months later a latency incident traces back to
  cold-start delay on the first request after an idle period.
  **Fix:** Treat `minReplicaCount: 0` as a required discussion item in
  every review, not a default to wave through — confirm the workload's
  actual cold-start time (image pull, container start, readiness probe)
  was measured and is acceptable for whatever depends on that workload's
  latency, and document the decision explicitly rather than leaving it
  implicit.

- **Symptom:** A `ScaledObject` was validated once at creation and never
  revisited; six months later it references a Kafka topic that was
  renamed, and the trigger has been silently non-functional (workload
  stuck at `minReplicaCount`) the entire time.
  **Fix:** Validation is not a one-time gate — re-run the authentication
  and connectivity checks (steps 2–3) whenever the underlying event
  source changes, and consider an automated periodic check (a CronJob or
  monitoring rule) that alerts if a `ScaledObject`'s trigger has been in
  a failing state for longer than a defined threshold, rather than
  relying on someone noticing the workload never scales.

## Worked example

**Scenario:** A pull request adds a `ScaledObject` for a new
`invoice-processor` `Deployment`, scaling on SQS queue depth, ahead of a
production rollout. This skill's checklist runs as the pre-merge review.

Submitted config:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: invoice-processor-scaledobject
  namespace: billing
spec:
  scaleTargetRef:
    name: invoice-processor
  minReplicaCount: 0
  cooldownPeriod: 30
  triggers:
    - type: aws-sqs-queue
      metadata:
        queueURL: https://sqs.us-east-1.amazonaws.com/<AWS_ACCOUNT_ID>/invoice-jobs
        queueLength: "1"
        awsRegion: us-east-1
        identityOwner: operator
```

Review findings:
1. **No `maxReplicaCount` set** — flagged as a hard blocker. Without a
   ceiling, a backlog spike (e.g. a batch re-processing job accidentally
   enqueuing thousands of messages) could scale `invoice-processor` out
   far enough to exhaust the `billing` namespace's database connection
   pool. Fix requested: `maxReplicaCount: 10`, chosen after confirming
   the invoicing database's connection pool can serve 10 concurrent
   processor instances comfortably.
2. **`queueLength: "1"`** — questioned: this means KEDA targets roughly
   one replica per one queued message, which is aggressive for a
   processor that takes ~20 seconds per invoice. Fix requested:
   `queueLength: "5"`, based on a quick load test showing one replica
   comfortably clears 5 queued invoices within one `pollingInterval`.
3. **`cooldownPeriod: 30`** — questioned against the queue's known burst
   pattern (invoices frequently arrive in small clusters seconds apart).
   A 30-second cooldown risks flapping between 0 and a few replicas
   repeatedly. Fix requested: `cooldownPeriod: 180`.
4. **`minReplicaCount: 0`** — accepted, since invoice processing is
   fully asynchronous and has no online-latency requirement a human is
   waiting on; the ~10-second cold start was measured and confirmed
   acceptable for this use case, and this reasoning is added as a code
   comment in the manifest for future reviewers.

Revised, approved config:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: invoice-processor-scaledobject
  namespace: billing
spec:
  scaleTargetRef:
    name: invoice-processor
  minReplicaCount: 0   # accepted: async batch work, ~10s cold start measured OK
  maxReplicaCount: 10  # bounded by invoicing DB connection pool capacity
  cooldownPeriod: 180  # invoices arrive in small bursts; avoids flapping
  triggers:
    - type: aws-sqs-queue
      metadata:
        queueURL: https://sqs.us-east-1.amazonaws.com/<AWS_ACCOUNT_ID>/invoice-jobs
        queueLength: "5"   # ~20s/invoice, validated via load test
        awsRegion: us-east-1
        identityOwner: operator
```
Only after all four findings are addressed does the PR pass validation
and merge.

## Cross-references

- [keda-event-driven-autoscaling-configuration](../keda-event-driven-autoscaling-configuration/SKILL.md) — the `ScaledObject`/`ScaledJob`/`TriggerAuthentication` design this skill validates against a production baseline.
- [metallb-configuration-validation](../metallb-configuration-validation/SKILL.md) — the same "the CRD's status field looks fine but doesn't confirm the underlying system is actually working" validation pattern, applied to load-balancer networking instead of autoscaling.
- [testkube-kubernetes-native-test-execution](../testkube-kubernetes-native-test-execution/SKILL.md) — running an in-cluster load test against the scaled workload to derive the real per-replica throughput figure this skill's threshold checks depend on.
- [kafka-configuration-validation](../../../messaging-and-data-orchestration/skills/kafka-configuration-validation/SKILL.md) — validating the Kafka-side consumer group/lag configuration a Kafka-triggered `ScaledObject` depends on.
- [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md) — broader secret-handling practices this skill's `TriggerAuthentication` validation applies specifically to KEDA triggers.
