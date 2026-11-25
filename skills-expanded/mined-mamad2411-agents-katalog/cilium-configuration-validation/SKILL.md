---
name: cilium-configuration-validation
description: >
  Validates CiliumNetworkPolicy, CiliumClusterwideNetworkPolicy, and
  Hubble observability configuration before a production rollout —
  syntax-checking policy files offline, confirming which endpoints and
  identities a policy actually selects, and using Hubble flow data to
  prove a policy enforces what it's meant to instead of trusting the
  YAML. Use when a user asks to "validate a CiliumNetworkPolicy before
  applying it," "check if this policy will actually match my pods,"
  "confirm kube-proxy replacement is healthy before a rollout," "test
  an egress FQDN policy before merging," or "why is Hubble showing
  drops I didn't expect."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# Cilium Configuration Validation

## Purpose

A `CiliumNetworkPolicy` that applies cleanly to the Kubernetes API server
tells you nothing about whether it actually matches the pods you intend,
enforces the L7 rule you wrote, or leaves a gap that silently falls back
to a broader allow. The failure modes here are quiet: an
`endpointSelector` with a typo'd label matches zero pods (policy is a
no-op, traffic flows as if unprotected), an L7 HTTP rule attached to the
wrong port never engages the proxy, and a `toFQDNs` egress rule that
never observed the corresponding DNS lookup never resolves to an actual
allowed IP. None of these produce an error — they produce a policy that
"applied successfully" while doing something other than what was
intended. This skill covers the commands and checks that catch this
before (or immediately after) a change reaches production, distinct
from
[cilium-ebpf-cni-and-mesh-configuration](../cilium-ebpf-cni-and-mesh-configuration/SKILL.md),
which covers installing Cilium and writing this configuration in the
first place.

## When to use

- Before applying a new or changed `CiliumNetworkPolicy` or
  `CiliumClusterwideNetworkPolicy` to a production cluster.
- Confirming a policy's `endpointSelector`/`fromEndpoints`/`toEndpoints`
  label matchers actually resolve to the real, currently-running pods,
  not just that the YAML parses.
- Validating an L7 HTTP, DNS, or Kafka rule is actually being enforced
  at the proxy layer, not silently falling through to L3/L4-only
  behavior.
- Confirming kube-proxy replacement and the Cilium agent's own health
  are in a good state before trusting any policy check that depends on
  them.
- Wiring Cilium policy validation into CI so a policy change that would
  match zero pods, or open an unintended allow, is caught in review.
- Auditing Hubble flow data after a policy change to prove the intended
  traffic is allowed and everything else is dropped, rather than
  assuming the policy did what the YAML says.

## Prerequisites & environment

- The `cilium` CLI and `hubble` CLI matching (or compatible with) the
  installed Cilium version — mismatched CLI versions can misreport
  status fields that changed between releases.
- Hubble enabled (`cilium hubble enable`) with `hubble port-forward`
  reachable, since most of the semantic checks here depend on live flow
  data, not just static policy inspection.
- `kubectl` read access to `CiliumNetworkPolicy`,
  `CiliumClusterwideNetworkPolicy`, and `CiliumIdentity` custom
  resources in the namespaces being validated.
- Exec access into a Cilium agent pod (`kubectl exec -n kube-system
  ds/cilium -- cilium ...`) for commands that inspect the agent's live
  policy repository and endpoint state, since some checks reflect the
  agent's actual enforced state rather than what's stored in the
  Kubernetes API.
- For CI-integrated validation: a disposable cluster (kind/k3d) with
  Cilium installed, since offline YAML linting alone cannot confirm a
  label selector matches real running pods or that an L7 rule engages
  the per-node Envoy proxy.

## Step-by-step guidance

1. **Check overall Cilium and Hubble health before trusting any
   downstream policy check** — a degraded agent makes every other
   signal unreliable:
   ```bash
   cilium status --verbose
   hubble status
   ```
   Confirm `KubeProxyReplacement` and `Cilium health` both report a
   fully healthy state, not just "OK" with warnings buried in
   `--verbose` output.

2. **Validate policy file syntax and schema offline** before it reaches
   the cluster, catching YAML/JSON errors and unknown fields early:
   ```bash
   kubectl apply --dry-run=server -f payments-api-ingress.yaml
   ```
   `--dry-run=server` is required, not `--dry-run=client` — client-side
   dry-run only checks the manifest is well-formed YAML matching the
   CRD's Go type; it cannot catch a `CiliumNetworkPolicy`-specific
   validation error the API server's admission webhook would reject.

3. **Confirm the policy's selectors actually match real, running
   endpoints** — this is the single most common silent failure:
   ```bash
   kubectl get cep -n payments -l app=payments-api
   kubectl exec -n kube-system ds/cilium -- cilium endpoint list | grep payments
   ```
   A `CiliumEndpoint` (`cep`) list with zero results for the labels used
   in `endpointSelector`/`fromEndpoints` means the policy is a no-op —
   it applied without error but selects nothing, and unselected traffic
   is not implicitly denied by an empty selector the way you might
   expect.

4. **Confirm an L7 rule is actually being enforced by the proxy**, not
   just present in the policy spec:
   ```bash
   kubectl exec -n kube-system ds/cilium -- cilium policy get
   hubble observe --namespace payments --protocol http --verdict DROPPED
   ```
   Send a request that the L7 rule should reject (wrong method or path)
   and confirm it shows up in `hubble observe` as `DROPPED` with an
   HTTP-layer reason — if it instead shows `FORWARDED`, the L7 rule
   isn't engaging, most often because the `toPorts.ports` protocol/port
   in the policy doesn't match the real traffic's actual port.

5. **Validate `toFQDNs` egress rules against real DNS behavior**, since
   an FQDN policy that never observes the corresponding DNS lookup has
   nothing to pin the allow to:
   ```bash
   hubble observe --namespace payments --protocol dns
   hubble observe --namespace payments --to-fqdn "api.stripe.com"
   ```
   If the DNS query itself is being dropped (check the DNS egress rule
   allowing port 53 to `kube-dns` is present and not shadowed), the
   `toFQDNs` rule has no resolved IP to allow and all traffic to that
   hostname is denied regardless of the rule looking correct on paper.

6. **Prove default-deny is actually in effect** before considering a
   namespace policy-complete — apply the intended default-deny plus
   allow rules to a staging namespace and confirm via Hubble that
   everything not explicitly allowed shows `DROPPED`:
   ```bash
   kubectl apply -f default-deny.yaml -f allow-checkout.yaml -n payments-staging
   hubble observe --namespace payments-staging --verdict DROPPED
   hubble observe --namespace payments-staging --verdict FORWARDED
   ```
   Confirm the `FORWARDED` list contains only the intended flows and
   `DROPPED` contains everything else you expect to be blocked — an
   empty `DROPPED` list in a namespace that's supposed to be locked down
   is itself a signal something isn't enforcing.

7. **Wire this into CI as a gate**, failing the pipeline on a non-zero
   `--dry-run=server` exit, an empty `CiliumEndpoint` match for any
   selector referenced by a changed policy, or (in a disposable cluster)
   an `hubble observe` check that doesn't show the expected
   allow/deny split:
   ```bash
   kubectl apply --dry-run=server -f ./cilium-policies/ || exit 1
   ```

8. **Re-check kube-proxy replacement health after any Cilium upgrade**
   before trusting policy behavior post-upgrade, since eBPF datapath
   changes between versions can shift enforcement subtly even when the
   policy YAML hasn't changed:
   ```bash
   cilium connectivity test
   cilium status --verbose | grep -i "KubeProxyReplacement"
   ```

## Best practices

- Treat `kubectl apply --dry-run=server` as necessary but not
  sufficient — it only proves the manifest is schema-valid, never that
  the selector matches real pods or the L7 rule engages the proxy.
  Always follow with a live `CiliumEndpoint`/`hubble observe` check.
- Validate every changed policy's selectors against `kubectl get cep`
  in the exact namespace and label set being changed, not a
  similarly-named one — a namespace mismatch is the most common reason
  a policy silently matches nothing.
- Use `hubble observe --verdict DROPPED` as the source of truth for "is
  this actually being blocked," and `--verdict FORWARDED` as the source
  of truth for "is this actually being allowed" — don't infer either
  from the policy YAML alone.
- Validate `toFQDNs` rules only after confirming DNS egress itself is
  allowed and observed by Hubble — an FQDN rule with no visibility into
  the DNS lookup has no IP to pin its allow decision to.
- Run the full validation pass (schema, selector match, L7 enforcement,
  default-deny proof) in a staging namespace before applying the same
  policy to production, and re-run the `hubble observe` checks against
  production immediately after applying to confirm parity.
- Re-run `cilium connectivity test` after any Cilium version upgrade as
  part of validation, not just at initial install — see
  [cilium-ebpf-cni-and-mesh-configuration](../cilium-ebpf-cni-and-mesh-configuration/SKILL.md)
  for the install-time guidance this complements.

## Common pitfalls

- **Symptom:** A `CiliumNetworkPolicy` applies with no errors, but
  traffic that should be restricted flows exactly as if the policy
  didn't exist.
  **Fix:** Almost always an `endpointSelector`/`fromEndpoints` label
  mismatch. Run `kubectl get cep -n <ns> -l <the exact labels used in
  the policy>` — an empty result means the policy selects nothing, and
  Cilium does not treat an empty selector as "deny by default" for that
  policy; it's simply inert.

- **Symptom:** An L7 HTTP method/path rule is present in the policy but
  a request that should be rejected still gets through.
  **Fix:** The `toPorts.ports` protocol/port in the policy doesn't match
  the real traffic's port, so the per-node Envoy proxy never sees the
  request and it falls through to whatever the L3/L4 portion alone
  allows. Confirm the real service port with `hubble observe --protocol
  http` and align it with the policy's `toPorts` before assuming the L7
  rule logic itself is wrong.

- **Symptom:** A `toFQDNs` egress rule for a specific hostname works in
  one environment but denies everything in another, despite identical
  policy YAML.
  **Fix:** The environment where it fails likely has a separate,
  narrower (or missing) DNS egress rule, so the FQDN lookup itself never
  completes and there's no resolved IP for the rule to allow. Check
  `hubble observe --protocol dns` in the failing environment for the
  actual DNS query/response before assuming the FQDN rule syntax is
  wrong.

- **Symptom:** `kubectl apply --dry-run=server` passes cleanly in CI,
  but the same policy breaks real traffic the moment it's applied to
  production.
  **Fix:** Schema-level dry-run cannot know whether the label selector
  matches any real pod or whether traffic actually flows on the port
  named in the policy — both require live cluster state. Add a staging
  apply-and-observe step (`hubble observe --verdict DROPPED/FORWARDED`)
  to the CI gate rather than relying on dry-run alone.

- **Symptom:** During an incident, someone applies a broad allow-all
  `CiliumNetworkPolicy` (empty `ingress`/`egress` selectors matching
  everything) "to rule out policy as the cause," confirms traffic now
  flows, and it's still in place days later.
  **Fix:** This is a real security regression, not a neutral diagnostic
  step — it removes network policy enforcement for every workload it
  matches. Treat it as strictly time-boxed, prefer testing the change
  in a non-production namespace first, and use `hubble observe --verdict
  DROPPED` to find the actual over-restrictive rule instead of removing
  policy wholesale. Re-apply the original scoped policy (or a corrected
  version) before closing the incident, not "later."

## Worked example

**Scenario:** Validate the `payments-api` default-deny, ingress, and
egress policies from the worked example in
[cilium-ebpf-cni-and-mesh-configuration](../cilium-ebpf-cni-and-mesh-configuration/SKILL.md)
before they reach production.

```bash
# 1. Agent/Hubble health first
cilium status --verbose
hubble status

# 2. Schema-level validation
kubectl apply --dry-run=server -f payments-policies.yaml

# 3. Apply to staging and confirm selectors actually match
kubectl apply -f payments-policies.yaml -n payments-staging
kubectl get cep -n payments-staging -l app=payments-api
# expect: at least one CiliumEndpoint listed, not zero

# 4. Confirm L7 enforcement: a disallowed method should be dropped
curl -X DELETE http://payments-api.payments-staging/charges/123
hubble observe --namespace payments-staging --protocol http --verdict DROPPED
# expect: the DELETE request shown as DROPPED

# 5. Confirm the allowed path still works and shows FORWARDED
curl -X POST http://payments-api.payments-staging/charges
hubble observe --namespace payments-staging --protocol http --verdict FORWARDED

# 6. Confirm egress to the payment processor resolves and is allowed
hubble observe --namespace payments-staging --protocol dns
hubble observe --namespace payments-staging --to-fqdn "api.stripe.com"
```

Only once step 4 shows the DELETE request as `DROPPED`, step 5 shows the
POST as `FORWARDED`, and step 6 shows a resolved DNS lookup followed by
an allowed flow to `api.stripe.com:443`, is the same manifest applied to
the production `payments` namespace, followed by the same
`hubble observe` checks re-run against production to confirm parity
before the change is considered complete.

## Cross-references

- [cilium-ebpf-cni-and-mesh-configuration](../cilium-ebpf-cni-and-mesh-configuration/SKILL.md) — writing the CiliumNetworkPolicy and Hubble configuration this skill validates.
- [linkerd-configuration-validation](../linkerd-configuration-validation/SKILL.md) — the equivalent validation discipline for Linkerd injection and traffic/authorization policy, useful when comparing pre-production checks across mesh/CNI choices.
- [consul-configuration-validation](../consul-configuration-validation/SKILL.md) — validating Consul intentions, relevant when Consul mesh authorization and Cilium's CNI-layer policy both apply to the same traffic and need to agree.
