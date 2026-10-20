---
name: dapr-configuration-validation
description: >
  Validates Dapr component configurations — state store, pub/sub, and
  binding components — before deploy, catching missing scopes, inline
  secrets, unbounded retries, and resiliency gaps that `kubectl apply`
  won't reject. Use when the user asks to "validate a Dapr component
  before deploy," "check Dapr component scoping," "review a Dapr
  pub/sub config for secrets," "add a pre-deploy gate for Dapr
  components," or "why did my Dapr component apply but not work as
  expected."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: serverless-and-alternative-compute
  maturity: stable
---

# Dapr Configuration Validation

## Purpose

A Dapr `Component` manifest almost always applies cleanly even when it
is operationally unsafe — an unscoped state store reachable by every
app in the namespace, a plaintext credential inlined under
`spec.metadata`, a pub/sub component with no dead-letter or retry
policy, or a binding pointed at the wrong environment's backend all
pass Kubernetes' schema validation and only surface later as a security
finding, a silent data-loss incident, or a cross-environment data leak.
This skill is the pre-deploy validation gate for Dapr component
configuration, complementing
[dapr-distributed-runtime-configuration](../dapr-distributed-runtime-configuration/SKILL.md),
which covers building that configuration in the first place — the same
role
[aws-lambda-configuration-validation](../aws-lambda-configuration-validation/SKILL.md)
plays for Lambda and
[knative-configuration-validation](../knative-configuration-validation/SKILL.md)
plays for Knative Serving.

## When to use

- Before merging or applying a new or changed Dapr `Component` manifest
  (state store, pub/sub, binding, secret store) to any environment.
- Reviewing a GitOps PR that touches `dapr.io/v1alpha1` `Component` or
  `Resiliency` resources.
- Auditing existing components across a namespace/cluster for missing
  `scopes`, inline secrets, or absent resiliency policies.
- Diagnosing a component that deployed successfully but behaves
  unexpectedly (reachable by unintended apps, or silently dropping
  messages under load).
- Adding a CI or admission-time gate specific to Dapr resources.

## Prerequisites & environment

- `kubectl` read access to `components.dapr.io` and
  `resiliencies.dapr.io` in the target namespace(s).
- `yq`/`jq` for parsing manifest output in scripted checks.
- A list of which `app-id`s are legitimately allowed to use each
  component — this is domain knowledge that must come from the team
  owning the component, not something derivable from the manifest
  alone; validation checks that `scopes` exists and is non-empty, but
  confirming it's the *correct* set of apps still requires a human
  reviewer with that context.
- Awareness of which secret store/reference mechanism the organization
  standardizes on (Kubernetes Secrets, Vault, a cloud KMS-backed
  store) so inline-secret detection knows what a *correct* reference
  looks like, not just that a `secretKeyRef` exists syntactically.

## Step-by-step guidance

1. **Validate every component has non-empty `scopes`.** An unscoped
   component is usable by any Dapr-enabled app in the namespace:
   ```bash
   kubectl get components.dapr.io -n prod -o json | \
     jq '.items[] | select((.scopes // []) | length == 0) | .metadata.name'
   ```
   Any component name in the output is a required fix — add explicit
   `scopes` listing only the intended `app-id`s — not an item to note
   for later.

2. **Validate no component embeds a secret-shaped value directly under
   `spec.metadata`.** A `value` field (as opposed to `secretKeyRef`)
   holding something that looks like a password, connection string, or
   API key is a finding:
   ```bash
   kubectl get components.dapr.io -n prod -o json | \
     jq '.items[] | .spec.metadata[] | select(.value != null and (.name | test("(?i)password|secret|token|key")))'
   ```
   Any match here should be replaced with `secretKeyRef` pointing at a
   Kubernetes `Secret` or the organization's standard secret store
   component, and the exposed value rotated if it was ever applied to
   a live cluster (and doubly so if committed to source control).

3. **Validate a `Resiliency` policy exists for components/apps that
   matter operationally** (anything on a critical request path or
   holding data with a durability requirement) — Dapr does not require
   one, and its absence is easy to miss:
   ```bash
   kubectl get resiliencies.dapr.io -n prod -o json | \
     jq '[.items[].spec.targets.components // {} | keys[]] + [.items[].spec.targets.apps // {} | keys[]]'
   ```
   Cross-check the resulting list of targets against the full list of
   components/apps in the namespace; anything on the critical list
   (defined per-project, e.g. anything backing a customer-facing
   checkout or payment flow) with no matching target is a finding.

4. **Validate retry/circuit-breaker policies aren't set to unbounded or
   effectively-infinite values** without an accompanying timeout —
   `maxRetries: -1` (Dapr's "retry forever" value) with no `timeout`
   at the same target can hold a caller's request open indefinitely
   during a sustained downstream outage:
   ```bash
   kubectl get resiliencies.dapr.io -n prod -o json | \
     jq '.items[].spec.policies.retries | to_entries[] | select(.value.maxRetries == -1)'
   ```
   Flag any `maxRetries: -1` policy and confirm a `timeout` policy is
   also attached to the same target — infinite retries alone, without a
   bound on total wait time, is a latent hang risk.

5. **Validate pub/sub components used for anything with a durability
   requirement aren't silently using an at-most-once or otherwise
   lossy configuration** — check the component's `type` and any
   delivery-guarantee-affecting metadata fields against what the
   backing broker actually supports, and confirm the application
   consuming it acknowledges messages correctly (Dapr's pub/sub API
   requires an explicit success/retry/drop response from the
   subscriber; an app that always returns success regardless of
   processing outcome silently causes message loss on real failures).

6. **Wire these checks into CI as a required gate**:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   NS=prod
   UNSCOPED=$(kubectl get components.dapr.io -n "$NS" -o json | \
     jq -r '.items[] | select((.scopes // []) | length == 0) | .metadata.name')
   if [ -n "$UNSCOPED" ]; then
     echo "FAIL: unscoped Dapr component(s) found: $UNSCOPED"
     exit 1
   fi
   INLINE_SECRETS=$(kubectl get components.dapr.io -n "$NS" -o json | \
     jq -r '.items[] | .metadata.name as $n | .spec.metadata[]? |
       select(.value != null and (.name | test("(?i)password|secret|token|key"))) | $n')
   if [ -n "$INLINE_SECRETS" ]; then
     echo "FAIL: possible inline secret in component(s): $INLINE_SECRETS"
     exit 1
   fi
   echo "OK: Dapr components passed baseline validation"
   ```

## Best practices

- Run these checks as a required CI/admission gate on every change
  touching `Component`/`Resiliency` resources, not only before a
  first deploy — a component can be hand-edited directly in a cluster
  outside GitOps, and periodic re-validation catches that drift.
- Treat "no `scopes`" and "inline secret-shaped value" as hard failures
  by default, not warnings — both are common, easy-to-introduce
  mistakes with real security consequences, not edge cases.
- Maintain a project-specific "critical component/app" list (anything
  backing checkout, payments, or other high-stakes flows) so the
  resiliency-policy check has a concrete bar to check against, rather
  than requiring a policy on literally every component regardless of
  importance.
- Validate resiliency policies for sane bounds (a `timeout` paired with
  any unbounded retry policy) rather than only checking that a policy
  exists at all — a policy that exists but still allows an effectively
  infinite hang doesn't actually protect anything.
- Keep the validation script itself under version control next to the
  component manifests it checks, so changes to what counts as a passing
  configuration go through the same review as the manifests.

## Common pitfalls

- **Symptom:** A security review finds a state store or pub/sub
  component is reachable by an application that has no legitimate
  reason to use it.
  **Fix:** The component manifest omitted `scopes`; add explicit
  `scopes` restricted to the actual set of `app-id`s that need it, and
  add a CI check that fails on any component with empty/missing
  `scopes` going forward.

- **Symptom:** A credential (broker password, API key) is found in
  plaintext inside a component manifest, either in a cluster or in
  source control.
  **Fix:** Replace the inline `value` with `secretKeyRef` pointing at a
  Kubernetes `Secret` or the standard secret store component, purge the
  plaintext value from git history if it was committed, and rotate the
  exposed credential immediately — treat this as a live security
  incident, not just a config cleanup.

- **Symptom:** A service-to-service call via Dapr's invocation building
  block occasionally hangs for a very long time during a downstream
  outage, well beyond any reasonable expected latency.
  **Fix:** A retry policy set to `maxRetries: -1` (retry forever) has
  no accompanying `timeout` target; add a bounded timeout alongside the
  retry policy so a sustained outage fails the caller's request instead
  of holding it open indefinitely.

- **Symptom:** Messages published to a pub/sub component are missing
  under load, and no error appears anywhere in application logs.
  **Fix:** The subscribing application is likely returning a success
  response to Dapr regardless of actual processing outcome (a common
  mistake when adapting existing message-handling code to Dapr's
  pub/sub HTTP contract); fix the subscriber to return the correct
  retry/drop response on processing failure, and add a dead-letter
  target so exhausted retries are recorded rather than silently
  dropped.

- **Symptom:** A component intended only for a staging environment is
  found configured with a production backend's connection details (or
  vice versa) during an audit.
  **Fix:** Component manifests weren't namespaced/labeled clearly per
  environment, or an environment-specific overlay was applied to the
  wrong target; validate component `metadata` values (hostnames,
  connection endpoints) against an expected-environment allowlist as
  part of the CI gate, not just at manual review time.

## Worked example

**Scenario:** A CI pipeline is about to apply a new `orders-statestore`
component with no `scopes` field and a `redisPassword` value inlined
directly as plaintext, alongside a `Resiliency` policy that sets
`maxRetries: -1` for calls to `order-fulfillment-service` with no
`timeout`.

Validation run:
```bash
$ kubectl get components.dapr.io -n prod -o json | \
    jq '.items[] | select((.scopes // []) | length == 0) | .metadata.name'
"orders-statestore"
$ kubectl get components.dapr.io -n prod -o json | \
    jq '.items[] | .spec.metadata[] | select(.value != null and (.name | test("(?i)password")))'
{
  "name": "redisPassword",
  "value": "<REDACTED-EXAMPLE-VALUE>"
}
$ kubectl get resiliencies.dapr.io -n prod -o json | \
    jq '.items[].spec.policies.retries | to_entries[] | select(.value.maxRetries == -1)'
{
  "key": "retryForever",
  "value": { "policy": "exponential", "maxRetries": -1 }
}
```
Three findings block the merge: the component has no `scopes`, it has
an inline plaintext password instead of a `secretKeyRef`, and the
attached retry policy has no paired timeout. The fixes applied: add
`scopes: [order-service, order-fulfillment-service]`; replace the
inline `redisPassword` value with `secretKeyRef` against a
`orders-redis-secret` Kubernetes Secret and rotate the credential that
was briefly inlined; and add a `timeouts` policy bound to the same
target as `retryForever` so a sustained outage fails fast instead of
hanging indefinitely. The pipeline is re-run only after all three
findings are resolved.

## Cross-references

- [dapr-distributed-runtime-configuration](../dapr-distributed-runtime-configuration/SKILL.md) — how the component scoping, secret references, and resiliency policies validated here are built and operated.
- [aws-lambda-configuration-validation](../aws-lambda-configuration-validation/SKILL.md) — the same pre-deploy validation discipline applied to AWS Lambda configuration.
- [knative-configuration-validation](../knative-configuration-validation/SKILL.md) — equivalent pre-deploy validation for Knative Serving configuration, often deployed on the same cluster as Dapr components.
