---
name: linkerd-configuration-validation
description: >
  Validates a Linkerd installation, proxy injection, and traffic/
  authorization policy before a production rollout — running the
  built-in health checks, confirming which connections are actually
  mTLS-secured, and dry-running policy changes against real traffic
  patterns. Use when a user asks to "check if Linkerd is healthy,"
  "verify a pod actually got the sidecar injected," "test a
  TrafficSplit/ServiceProfile/AuthorizationPolicy before applying it,"
  "why isn't traffic using mTLS," or "validate Linkerd config in CI
  before merging."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# Linkerd Configuration Validation

## Purpose

Linkerd's simplicity relative to Istio doesn't remove the two failure
modes that matter most before a production rollout: a workload that
looks meshed but isn't actually injected (so it silently falls back to
plaintext, unproxied traffic), and a traffic-split or authorization
policy that's syntactically valid but doesn't match the real Service
topology or caller identities. Both fail quietly — a missing sidecar
doesn't error, it just doesn't encrypt or observe traffic, and a
misdirected `TrafficSplit` doesn't error, it just sends 100% of traffic
to the wrong backend. This skill covers the validation commands and
checks that catch these before they reach production, distinct from
[linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md),
which covers writing the configuration in the first place.

## When to use

- Before promoting a Linkerd install, upgrade, or certificate rotation
  to production, to confirm control-plane and data-plane health.
- Confirming a specific workload actually received proxy injection and
  is participating in mTLS, not just assuming the namespace annotation
  worked.
- Validating a `TrafficSplit`, `ServiceProfile`, `Server`, or
  `AuthorizationPolicy` resource against real traffic before or
  immediately after applying it, to catch a misconfiguration while
  blast radius is still small.
- Wiring Linkerd health/policy checks into CI so a manifest change that
  would break mTLS or misdirect traffic is caught in review, not after
  merge.
- Diagnosing "it looks meshed but something's still wrong" — the
  proxy is present, but traffic behaves unexpectedly.

## Prerequisites & environment

- `linkerd` CLI matching the installed control-plane version — a
  mismatched CLI can report false negatives/positives on some checks.
- The `viz` extension installed (`linkerd viz install`) for
  traffic-level checks (`edges`, `stat`, `tap`) — the base `linkerd
  check` only validates the control plane itself, not live traffic.
- `kubectl` access to the namespaces being validated, including read
  access to `Server`, `AuthorizationPolicy`, `TrafficSplit`, and
  `ServiceProfile` custom resources.
- For CI-integrated validation: a cluster (or a disposable
  kind/k3d cluster) the pipeline can apply manifests to with
  `--dry-run=server`, since some validity checks (e.g. whether a
  referenced Service actually exists) require server-side awareness
  that `--dry-run=client` doesn't have.

## Step-by-step guidance

1. **Run the control-plane health check first, always** — a control
   plane in a degraded state makes every downstream check unreliable:
   ```bash
   linkerd check
   linkerd check --proxy    # also checks injected data-plane proxies
   linkerd viz check        # checks the viz extension specifically
   ```
   `linkerd check` exits non-zero on any failing check — treat any
   non-zero exit as a hard blocker in CI, not a warning to eyeball.

2. **Confirm a specific workload actually has the proxy injected**,
   rather than trusting the namespace annotation was sufficient:
   ```bash
   kubectl get pod <pod-name> -n payments -o jsonpath='{.spec.containers[*].name}'
   # expect: <app-container> linkerd-proxy
   linkerd identity <pod-name> -n payments
   ```
   `linkerd identity` prints the pod's actual TLS identity certificate
   details — an error here (rather than a valid cert) means the proxy
   isn't running or hasn't completed identity issuance yet.

3. **Confirm mTLS is actually in effect on the connections that matter**,
   not just that both pods have a proxy container:
   ```bash
   linkerd viz edges deployment -n payments
   ```
   Look at the `TLS` column for each edge — `true` means mTLS is
   active for that specific connection; anything else (`no
   identity`/blank) means that connection is unencrypted, regardless of
   whether both pods individually look meshed.

4. **Dry-run policy and routing changes against a non-production
   namespace or a copy of production traffic shape before applying to
   production**, since Linkerd has no built-in "would this
   `AuthorizationPolicy` deny anything" simulator — the closest
   equivalent is applying to a staging namespace with representative
   `ServiceAccount` identities and watching `linkerd viz tap`:
   ```bash
   kubectl apply -f authz-policy.yaml -n payments-staging
   linkerd viz tap deploy/payments-api -n payments-staging
   ```
   Watch for `tap` output showing responses your policy should be
   denying (an unexpected caller identity still getting through) or
   over-denying (an expected caller identity getting rejected).

5. **Validate `ServiceProfile` and `TrafficSplit` resources reference
   real Services and routes** before applying, since a typo in a
   `service:`/`host:` field is accepted by the Kubernetes API (it's just
   a string) but silently does nothing at the data plane:
   ```bash
   kubectl get svc payments-api-v1 payments-api-v2 -n payments
   kubectl apply --dry-run=server -f trafficsplit.yaml
   kubectl get trafficsplit payments-api-canary -n payments -o yaml
   ```
   After applying for real, confirm the split is actually being honored,
   not just accepted:
   ```bash
   linkerd viz stat trafficsplit -n payments
   ```

6. **Check certificate expiry proactively**, not only when `linkerd
   check` happens to flag it during a routine run:
   ```bash
   linkerd check --output json | jq '.categories[] | select(.name=="linkerd-identity")'
   ```
   Wire this into a scheduled CI job (daily, not just pre-deploy) so
   issuer-certificate expiry is caught with weeks of lead time, not
   discovered when new pods start failing to join the mesh.

7. **Integrate into CI as a gate**, failing the pipeline on any
   non-zero `linkerd check`/`linkerd viz check` exit code, and on any
   `TrafficSplit`/`ServiceProfile`/`AuthorizationPolicy` manifest whose
   referenced Service or `ServiceAccount` doesn't resolve via
   `kubectl apply --dry-run=server`:
   ```bash
   linkerd check --output json > check.json || (cat check.json && exit 1)
   ```

## Best practices

- Run `linkerd check --proxy` (not just the base `linkerd check`)
  whenever validating a specific application namespace — the base check
  only covers the control plane, and most rollout-blocking issues live
  in the data plane.
- Treat `linkerd viz edges` as the source of truth for "is mTLS actually
  happening," not the presence of a `linkerd-proxy` container — a
  present-but-misconfigured proxy (wrong skip-port annotation, stale
  identity) still shows up as injected while not actually securing
  traffic.
- Validate in a staging namespace with realistic `ServiceAccount`
  identities before applying a new `AuthorizationPolicy` to production —
  a policy that's too narrow fails closed and breaks real traffic
  immediately, which is a worse failure mode to discover live than in
  staging.
- Keep certificate-expiry checks on a recurring schedule (daily/weekly),
  independent of deploy cadence — a low-traffic service might not
  redeploy for months, long enough for an issuer cert to expire
  unnoticed between deploys.
- Fail CI hard on any non-zero `linkerd check` exit code rather than
  logging and continuing — a "warning" from `linkerd check` about
  identity or control-plane health is exactly the kind of thing that's
  easy to defer until it becomes an incident.

## Common pitfalls

- **Symptom:** `linkerd check` passes, but a specific workload's traffic
  is still unencrypted per `linkerd viz edges`.
  **Fix:** `linkerd check` validates the control plane's own health, not
  every individual data-plane connection. Always follow with `linkerd
  check --proxy` for the specific namespace and `linkerd viz edges` for
  the specific connection in question — a healthy control plane doesn't
  guarantee every workload is correctly injected or configured.

- **Symptom:** A `TrafficSplit` was applied and `kubectl get
  trafficsplit` shows it exists with the intended weights, but
  `linkerd viz stat` shows 100% of traffic still on the old backend.
  **Fix:** Callers are likely resolving the version-specific backend
  Service (`payments-api-v1`) directly instead of the root Service name
  the `TrafficSplit` targets. Grep calling services' configuration/DNS
  targets for the backend name specifically, not just confirm the
  `TrafficSplit` resource's own YAML looks correct.

- **Symptom:** A new `AuthorizationPolicy` was validated successfully by
  `kubectl apply --dry-run=server` (no schema errors) but breaks
  production traffic the moment it's applied for real.
  **Fix:** Schema-level dry-run only checks the manifest is
  well-formed — it cannot know whether the `MeshTLSAuthentication`
  identity referenced actually matches any real caller's
  `ServiceAccount` identity. Always test a new authorization policy in
  staging with `linkerd viz tap` watching real request flow first, and
  roll production application behind a fast-revert plan.

- **Symptom:** A certificate-expiry warning from `linkerd check` was
  seen once, in a pre-deploy check weeks ago, and then never surfaced
  again until identity issuance actually started failing.
  **Fix:** Pre-deploy checks only run on deploy cadence — a service that
  isn't redeployed won't re-trigger the check. Schedule `linkerd check`
  independently (e.g. a daily CI cron job posting to an alerting
  channel) so certificate expiry is caught on a calendar cadence, not
  only a deploy cadence.

- **Symptom:** To unblock a failing connectivity test, someone
  temporarily deletes the `AuthorizationPolicy` or annotates the
  workload to skip proxy injection entirely, confirms traffic now
  flows, and ships that as the "validated" state.
  **Fix:** This masks the actual problem (likely a wrong
  `MeshTLSAuthentication` identity or a missing `Server` selector) and
  ships a workload with no authorization enforcement or no mTLS at all.
  Treat removing a policy or disabling injection as a debugging-only,
  non-production action with an explicit tracked revert — never let it
  become the shipped configuration.

## Worked example

**Scenario:** Before promoting a new `AuthorizationPolicy` restricting
`payments-api` to `checkout-service` callers only (from the worked
example in
[linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md)),
validate it end-to-end.

```bash
# 1. Control plane and data plane health
linkerd check
linkerd check --proxy -n payments

# 2. Confirm injection on the actual running pods
kubectl get pods -n payments -l app=payments-api \
  -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.spec.containers[*].name}{"\n"}{end}'

# 3. Apply to staging first, then tap live traffic
kubectl apply -f authz-policy.yaml -n payments-staging
linkerd viz tap deploy/payments-api -n payments-staging --to deploy/checkout-service
linkerd viz tap deploy/payments-api -n payments-staging --to deploy/some-other-caller
```

`tap` output for the `checkout-service` caller should show normal
request/response pairs; the `some-other-caller` test should show the
connection being denied at the policy layer (confirming the policy
actually blocks unauthorized callers, not just that it deployed without
error). Only after both are confirmed in staging:

```bash
kubectl apply -f authz-policy.yaml -n payments
linkerd viz edges deployment -n payments
linkerd viz tap deploy/payments-api -n payments
```

A final `viz edges` check confirms `checkout-service → payments-api`
still shows `TLS: true`, and a spot-check `tap` in production confirms
no unexpected caller is still getting through before the change is
considered complete.

## Cross-references

- [linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md) — writing the Linkerd installation, injection, and traffic/authorization policy this skill validates.
- [cilium-configuration-validation](../cilium-configuration-validation/SKILL.md) — the equivalent validation discipline for Cilium network policy and Hubble observability, if the cluster also runs Cilium as CNI underneath Linkerd.
- [consul-configuration-validation](../consul-configuration-validation/SKILL.md) — the equivalent validation discipline for Consul service definitions and intentions, useful when comparing pre-production checks across mesh choices.
