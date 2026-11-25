---
name: knative-configuration-validation
description: >
  Validates Knative Service/Revision configuration and autoscaling
  annotations before deploy — catching missing resource limits,
  contradictory min/max scale settings, unsafe traffic splits, and
  timeout misconfigurations that a normal `kubectl apply` won't reject.
  Use when the user asks to "validate a Knative Service before deploy,"
  "check Knative autoscaling annotations," "review a canary traffic
  split," "add a pre-deploy gate for Knative config," or "why did my
  Knative Service apply succeed but behave wrong."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: serverless-and-alternative-compute
  maturity: stable
---

# Knative Configuration Validation

## Purpose

`kubectl apply` on a Knative `Service` almost always succeeds even when
the resulting configuration is operationally unsafe — contradictory
min/max scale bounds, a concurrency target mismatched to actual
per-pod capacity, a traffic split that sends production load to an
unvalidated revision, or a timeout shorter than the workload's real
latency all pass schema validation and only surface later as an
incident, a cost overrun, or a silent outage. This skill is the
pre-deploy gate for Knative Serving configuration, complementing
[knative-serverless-configuration](../knative-serverless-configuration/SKILL.md),
which covers how to build that configuration in the first place, the
same way
[aws-lambda-configuration-validation](../aws-lambda-configuration-validation/SKILL.md)
gates Lambda configuration before it ships.

## When to use

- Before merging or applying a change to a Knative `Service`/`Revision`
  manifest, especially one touching autoscaling annotations or the
  `traffic` block.
- Reviewing a GitOps PR (ArgoCD/Flux-managed) that modifies Knative
  Serving resources.
- Diagnosing a Knative Service that deployed successfully but behaves
  unexpectedly (never scales down, drops requests on scale-down, or
  routes traffic somewhere unintended).
- Auditing existing Knative Services across a namespace/cluster for
  missing resource limits or unsafe defaults.
- Adding a CI or admission-time gate specific to Knative resources,
  distinct from generic Kubernetes manifest linting.

## Prerequisites & environment

- `kubectl` with read access to `services.serving.knative.dev` and
  `revisions.serving.knative.dev` in the target namespace(s).
- `yq` or `jq` for parsing manifest/CLI output in scripted checks.
- Optional but recommended: a policy engine already in use for
  cluster-wide admission control (OPA/Gatekeeper or Kyverno) to enforce
  these checks at admission time rather than only in CI — see the
  `policy-and-governance-tooling` domain's skills for the underlying
  policy-engine setup; this skill focuses on what to check, not which
  engine enforces it.
- Familiarity with the target cluster's actual node capacity and
  downstream service capacity (databases, third-party APIs) — several
  checks here are only meaningful relative to real infrastructure
  limits, not the manifest in isolation.

## Step-by-step guidance

1. **Validate min/max scale bounds are internally consistent and
   intentional**, not copy-pasted defaults:
   ```bash
   kubectl get ksvc checkout-api -n prod -o json | \
     jq '.spec.template.metadata.annotations | {
       min: ."autoscaling.knative.dev/min-scale",
       max: ."autoscaling.knative.dev/max-scale",
       target: ."autoscaling.knative.dev/target"
     }'
   ```
   Flag as findings: `min-scale` greater than `max-scale` (a
   misconfiguration Knative may accept without complaint but that
   produces undefined scaling behavior), `max-scale` unset (meaning
   unbounded — dangerous for a workload with an expensive or
   rate-limited downstream dependency), and `min-scale: 0` on a path
   explicitly documented as latency-sensitive.

2. **Validate every container in the revision template sets both
   `resources.requests` and `resources.limits`.** An unset
   `resources.requests` means the Kubernetes scheduler can pack the pod
   anywhere regardless of actual usage, and Knative's own autoscaling
   decisions (concurrency-based, not CPU-based) don't protect against a
   resource-starved pod that looks "up" but is thrashing:
   ```bash
   kubectl get ksvc checkout-api -n prod -o json | \
     jq '.spec.template.spec.containers[] | select(.resources.requests == null or .resources.limits == null)'
   ```
   Any non-empty output here is a required fix before deploy, not an
   optional improvement.

3. **Validate `timeoutSeconds` against the workload's real observed
   latency**, not left at the Knative default:
   ```bash
   kubectl get ksvc checkout-api -n prod -o jsonpath='{.spec.template.spec.timeoutSeconds}'
   ```
   Compare against actual p99 latency from existing observability data
   before deploy; a timeout shorter than real p99 latency causes
   legitimate slow requests to be cut off as failures, while a timeout
   far longer than necessary delays detecting a genuinely hung request.

4. **Validate the `traffic` block sums to 100% and doesn't route
   production-percentage traffic to an unvalidated revision.** Before
   any deploy that changes `traffic` percentages:
   ```bash
   kubectl get ksvc checkout-api -n prod -o json | \
     jq '[.spec.traffic[].percent] | add'
   ```
   A sum other than `100` means the manifest is malformed (Knative will
   reject some malformed splits, but a split summing to slightly under
   100 due to a typo can still apply and silently drop the remainder of
   requests to no revision). Separately, flag any traffic change that
   sends more than a small validation percentage (a project-specific
   threshold, e.g. 10–20%) to a revision with no prior production
   traffic history, unless the change is an explicit, reviewed full
   cutover.

5. **Validate revision-level IAM/RBAC and network policy scope**, if
   the cluster uses a service mesh (Istio) alongside Knative — a
   revision's `ServiceAccount` should be scoped to only what that
   specific workload needs, the same discipline as validating a Lambda
   execution role or a Dapr component's scope:
   ```bash
   kubectl get ksvc checkout-api -n prod -o jsonpath='{.spec.template.spec.serviceAccountName}'
   kubectl get serviceaccount <name> -n prod -o yaml
   ```

6. **Wire these checks into CI as a required gate**, using the cluster's
   actual downstream capacity as an input rather than hardcoding
   thresholds:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   SVC=checkout-api
   NS=prod
   MAX=$(kubectl get ksvc "$SVC" -n "$NS" -o jsonpath='{.spec.template.metadata.annotations.autoscaling\.knative\.dev/max-scale}')
   if [ -z "$MAX" ]; then
     echo "FAIL: $SVC has no max-scale set — unbounded scaling risk"
     exit 1
   fi
   REQ=$(kubectl get ksvc "$SVC" -n "$NS" -o jsonpath='{.spec.template.spec.containers[0].resources.requests}')
   if [ -z "$REQ" ]; then
     echo "FAIL: $SVC container has no resources.requests set"
     exit 1
   fi
   echo "OK: $SVC passed baseline Knative config checks"
   ```

## Best practices

- Run these checks as a required CI/admission-time gate on every
  manifest change touching a Knative `Service`, not only before a
  first deploy — a revision can be edited directly in the cluster
  outside GitOps, and drift is exactly what re-validation catches.
- Treat "no `max-scale` set" as a hard failure by default, not a
  warning — an unbounded Knative Service can consume unplanned cluster
  capacity and cost under a traffic spike or a retry storm from a
  misbehaving client.
- Validate traffic-split changes against the same review rigor as a
  production deploy gate elsewhere in the stack (an approval step, a
  canary percentage ceiling) — a `traffic` patch is a production
  change even though it needs no image rebuild.
- Cross-check `resources.requests`/`limits` against actual observed
  usage (via `kubectl top pod` or cluster metrics) periodically, not
  just at initial validation — a workload's real resource profile
  drifts as its code changes.
- Keep the validation script itself version-controlled alongside the
  manifests it checks, so a change to what's considered a passing
  configuration is reviewable the same way the manifests are.

## Common pitfalls

- **Symptom:** A Knative Service manifest applies cleanly, but the
  revision scales to an unexpectedly large number of pods during a
  traffic spike, exhausting cluster capacity or a shared downstream
  connection pool.
  **Fix:** `max-scale` was left unset (unbounded); validate every
  Service has an explicit `max-scale` sized against real downstream
  capacity before deploy, and treat an unset value as a required fix,
  not an acceptable default.

- **Symptom:** A revision appears healthy in `kubectl get pods` but
  actual request latency degrades under moderate load.
  **Fix:** `resources.requests`/`limits` were unset or under-sized;
  Knative's concurrency-based autoscaler doesn't account for CPU
  starvation, so a pod can be within its concurrency target while
  still CPU-throttled — validate resource requests/limits are set and
  sized against measured usage, not left as Kubernetes defaults (no
  limit at all).

- **Symptom:** A canary traffic-split change applies successfully, but
  a large percentage of requests unexpectedly land on the new,
  unvalidated revision.
  **Fix:** The `traffic` block's percentages were miscalculated or a
  stale block from a previous change wasn't fully replaced; validate
  the sum equals 100 and that the percentage assigned to any revision
  without prior production traffic history stays within an agreed
  small validation threshold before wider promotion.

- **Symptom:** Requests to a Service intermittently fail with a
  timeout error under normal (not degraded) load.
  **Fix:** `timeoutSeconds` is set shorter than the workload's real p99
  latency; pull actual latency data from observability tooling and set
  the timeout with meaningful headroom above it, rather than leaving
  the Knative default unexamined.

- **Symptom:** A security review finds a Knative revision's service
  account has cluster-wide or namespace-admin-equivalent permissions.
  **Fix:** The revision was deployed without a dedicated
  `serviceAccountName`, inheriting the namespace's `default` service
  account; assign and scope a dedicated service account per Service and
  validate it as part of every pre-deploy check, not just at initial
  creation.

## Worked example

**Scenario:** A CI pipeline is about to apply a change to `checkout-api`
that raises `max-scale` from `20` to unset (accidentally dropped during
a manifest refactor) and adds a new `traffic` split sending 40% of
production traffic to an unvalidated revision.

Validation run against the proposed manifest:
```bash
$ jq '.spec.template.metadata.annotations."autoscaling.knative.dev/max-scale"' proposed-checkout-api.json
null
$ jq '[.spec.traffic[].percent] | add' proposed-checkout-api.json
100
$ jq '.spec.traffic' proposed-checkout-api.json
[
  { "revisionName": "checkout-api-00003", "percent": 60 },
  { "revisionName": "checkout-api-00004", "percent": 40, "tag": "canary" }
]
```
Two findings block the merge: `max-scale` is unset (fails the required
"every Service has an explicit max-scale" check), and the new revision
`checkout-api-00004` — with no prior production traffic history — is
assigned 40%, well above the team's agreed 10–20% initial-validation
threshold. The fix applied: restore `max-scale: "20"` in the manifest,
and reduce `checkout-api-00004`'s initial split to `10` with
`checkout-api-00003` at `90`, promoting further only after the canary's
error-rate and latency metrics are reviewed at the smaller percentage.

## Cross-references

- [knative-serverless-configuration](../knative-serverless-configuration/SKILL.md) — how the Service/Revision/traffic configuration validated here is built and operated.
- [aws-lambda-configuration-validation](../aws-lambda-configuration-validation/SKILL.md) — the same pre-deploy validation discipline applied to AWS Lambda configuration.
- [dapr-configuration-validation](../dapr-configuration-validation/SKILL.md) — equivalent pre-deploy validation for Dapr component configs, often deployed alongside Knative on the same cluster.
