---
name: consul-configuration-validation
description: >
  Validates Consul service definitions, config entries, and intentions
  (mesh-level authorization) before applying them to a production
  datacenter — syntax-checking agent config, dry-running catalog
  changes, and confirming intentions produce the intended allow/deny
  decisions. Use when a user asks to "validate a Consul service
  definition," "check my Consul config before applying," "test an
  intention before it goes live," "why did my Consul config entry not
  take effect," or "lint Consul HCL/JSON in CI."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# Consul Configuration Validation

## Purpose

Consul accepts a wide range of syntactically valid HCL/JSON that does
nothing useful at runtime: a `service-splitter` referencing a
`service-resolver` subset with zero matching instances, an intention
scoped to a service name that doesn't exist yet, or an agent config file
with a typo'd key that's silently ignored rather than rejected. None of
these fail loudly — they fail by having no effect, which is worse,
because the operator believes the change is live. This skill covers the
validation commands that catch these gaps before (or immediately after)
applying, distinct from
[consul-service-mesh-and-discovery-configuration](../consul-service-mesh-and-discovery-configuration/SKILL.md),
which covers writing the mesh/discovery configuration in the first
place.

## When to use

- Before applying a new or changed service definition, config entry
  (`service-resolver`/`service-splitter`/`service-router`/
  `service-intentions`), or agent configuration file to a production
  datacenter.
- Confirming an intention actually produces the intended allow/deny
  decision for a specific source/destination pair, rather than trusting
  the HCL reads correctly.
- Diagnosing why a config entry (subset filter, split weight, route)
  appears applied but has no observable effect on traffic.
- Wiring Consul config validation into CI so a bad service definition or
  intention is caught in review rather than after `consul config write`.
- Auditing an existing datacenter's intentions for unintended
  wildcard-allow rules before a security review.

## Prerequisites & environment

- The `consul` CLI matching (or compatible with) the target datacenter's
  server version, with network access to at least one server/agent for
  live checks (`consul intention check`, `consul catalog`).
- Read access to the Consul HTTP API (a valid ACL token if ACLs are
  enabled — most validation commands that touch the catalog or
  intentions require one) for anything beyond static file syntax
  checking.
- For CI-integrated validation: either a disposable Consul dev-mode
  instance (`consul agent -dev`) to apply candidate config entries
  against, or a non-production datacenter that mirrors production
  topology closely enough that subset/intention checks are meaningful.
- `consul-k8s`-managed CRDs (on Kubernetes) can additionally be
  validated with standard `kubectl apply --dry-run=server`, which
  catches schema errors but not the semantic gaps (subset mismatches,
  unreachable intentions) that need a live `consul intention check`.

## Step-by-step guidance

1. **Validate agent configuration file syntax before reloading an
   agent** — a config file with invalid HCL/JSON or an unknown key can
   prevent an agent from starting or reloading cleanly:
   ```bash
   consul validate /etc/consul.d/
   ```
   Run this against the actual config directory an agent loads from,
   not just a single file in isolation, since Consul merges multiple
   files in a directory and an interaction between two files can be the
   actual problem.

2. **Dry-run a service registration** against a disposable or dev-mode
   agent before registering it in production, to catch a malformed
   service definition (bad port type, invalid check interval) before it
   reaches the real catalog:
   ```bash
   consul agent -dev -config-dir=/tmp/consul-validate &
   consul services register payments-api.json
   consul catalog services
   ```

3. **Check what an intention actually resolves to**, rather than reading
   the HCL and assuming it's scoped correctly — this is the single most
   useful validation command for mesh authorization:
   ```bash
   consul intention check checkout-service payments-api
   ```
   This returns Consul's actual computed decision (`Allowed`/`Denied`)
   for that specific source/destination pair, accounting for all
   applicable intentions and default policy — far more reliable than
   manually tracing precedence rules across multiple intention files.

4. **List and review all intentions for a service before changing any
   one of them**, since intentions are evaluated together and a new
   narrow `allow` can be shadowed by an existing broader `deny` (or vice
   versa) depending on precedence:
   ```bash
   consul intention list
   consul intention get payments-api
   ```

5. **Validate config-entry references resolve to real, matching
   instances** before assuming a `service-splitter`/`service-router` is
   correctly wired:
   ```bash
   consul catalog nodes -service=payments-api
   consul catalog service payments-api -tags
   ```
   Cross-check the actual registered instances' metadata (`version` tag,
   in the canary example) against every `Filter` expression in the
   corresponding `service-resolver` — a subset with a filter matching
   zero instances is accepted by `consul config write` without any
   error.

6. **Confirm a config entry is actually stored and matches intent**
   after writing it — `consul config write` succeeding only means the
   entry was syntactically valid and accepted, not that it does what you
   intended:
   ```bash
   consul config write payments-api-splitter.hcl
   consul config read -kind service-splitter -name payments-api
   ```

7. **Wire validation into CI** as a gate before any config entry or
   intention reaches a production datacenter:
   ```bash
   consul validate ./consul-config/
   # then, against a disposable dev-mode instance:
   consul config write ./consul-config/service-resolver.hcl
   consul config write ./consul-config/service-splitter.hcl
   consul config read -kind service-splitter -name payments-api | \
     jq -e '.Splits | length > 0'
   ```
   Fail the pipeline on any non-zero exit from `consul validate` or a
   missing/empty config-entry read-back.

8. **For `consul-k8s` CRDs, dry-run against the API server first**, then
   confirm the Consul side actually reflects the intended state (CRD
   acceptance by Kubernetes doesn't guarantee the `consul-k8s` controller
   successfully reconciled it into Consul's catalog):
   ```bash
   kubectl apply --dry-run=server -f service-intentions.yaml
   kubectl apply -f service-intentions.yaml
   kubectl get serviceintentions payments-api -o yaml | \
     grep -A3 status
   ```

## Best practices

- Always follow `consul config write` with `consul config read` (or the
  Kubernetes CRD's `status` field) to confirm the entry landed as
  intended — successful write acceptance and correct runtime effect are
  different things.
- Use `consul intention check` as the authoritative answer to "will this
  call be allowed," not a manual read of the intention files — precedence
  rules across multiple intentions are easy to get wrong by inspection.
- Validate agent configuration directories (`consul validate`), not
  individual files, so cross-file interactions are caught the same way
  the running agent would encounter them.
- Cross-check `service-resolver` subset filters against actually
  registered instance metadata before relying on a
  `service-splitter`/`service-router` built on top of them — a filter
  matching zero instances is a silent no-op, not an error.
- Run intention and config-entry checks against a disposable/dev-mode
  Consul instance in CI rather than only validating syntax — semantic
  correctness (does this intention actually allow the right caller)
  can't be confirmed by schema validation alone.
- Periodically audit `consul intention list` datacenter-wide for
  wildcard `allow` rules that have outlived their original purpose —
  intention sprawl is as real a risk here as `AuthorizationPolicy`/
  `NetworkPolicy` sprawl in other meshes.

## Common pitfalls

- **Symptom:** `consul config write` succeeds for a `service-splitter`,
  but 100% of traffic still lands on one subset.
  **Fix:** Almost always a `service-resolver` subset filter matching
  zero registered instances — cross-check `consul catalog service
  <name> -tags` against every subset `Filter` expression before assuming
  the splitter itself is broken.

- **Symptom:** An intention explicitly allows `checkout-service →
  payments-api`, but `consul intention check` still returns `Denied`.
  **Fix:** A more specific or higher-precedence intention (or the
  datacenter's default policy) is overriding it — run `consul intention
  list` for the full picture rather than assuming the one intention you
  wrote is the only one in effect. Consul evaluates intentions by
  specificity, not just file order.

- **Symptom:** An agent fails to reload after a config file change, with
  a vague or no error in the logs.
  **Fix:** Run `consul validate` against the full config directory
  before reloading — it catches HCL/JSON syntax errors and unknown keys
  that the running agent's reload path may report unhelpfully or not at
  all.

- **Symptom:** A `consul-k8s` `ServiceIntentions` CRD applies cleanly per
  `kubectl apply` with no errors, but the corresponding Consul intention
  never takes effect.
  **Fix:** CRD acceptance by the Kubernetes API server only confirms
  schema validity, not that the `consul-k8s` controller successfully
  reconciled it into Consul — check the CRD's `status` field and the
  `consul-k8s` controller pod's logs, and confirm with `consul intention
  get` directly against Consul, not just `kubectl get`.

- **Symptom:** To unblock a failing intention check during
  troubleshooting, someone applies a temporary wildcard
  `Sources: [{Name: "*", Action: "allow"}]` intention "just to confirm
  it's an intentions problem," and it's left in place after the
  incident.
  **Fix:** A wildcard allow intention removes mesh authorization
  entirely for that destination service — treat it as a scoped,
  time-boxed diagnostic step only, applied in a non-production
  datacenter where possible, with an explicit tracked task to revert it
  and re-apply the correct narrow intention once the actual root cause
  (often a resolver/subset mismatch, not an intentions problem at all)
  is found.

## Worked example

**Scenario:** Validate the canary rollout config entries and intention
from the worked example in
[consul-service-mesh-and-discovery-configuration](../consul-service-mesh-and-discovery-configuration/SKILL.md)
before they reach production.

```bash
# 1. Syntax-check everything first
consul validate ./consul-config/

# 2. Confirm registered instances actually carry the version metadata
# the resolver subsets depend on
consul catalog service payments-api -tags
# expect instances tagged version=v1 and version=v2 respectively

# 3. Apply config entries to a disposable dev instance and read back
consul agent -dev -config-dir=/tmp/consul-validate &
consul config write ./consul-config/service-resolver.hcl
consul config write ./consul-config/service-splitter.hcl
consul config read -kind service-splitter -name payments-api

# 4. Confirm the intention produces the intended decision
consul config write ./consul-config/service-intentions.hcl
consul intention check checkout-service payments-api   # expect: Allowed
consul intention check some-other-service payments-api # expect: Denied
```

Only once `consul intention check` confirms both the intended allow and
the intended deny, and `consul catalog service payments-api -tags`
confirms both subsets have at least one matching instance, is the
change applied to the real production datacenter with `consul config
write` against it directly, followed by the same `consul intention
check` commands re-run against production to confirm parity.

## Cross-references

- [consul-service-mesh-and-discovery-configuration](../consul-service-mesh-and-discovery-configuration/SKILL.md) — writing the service definitions, config entries, and intentions this skill validates.
- [linkerd-configuration-validation](../linkerd-configuration-validation/SKILL.md) — the equivalent validation discipline for Linkerd proxy injection and traffic policy, useful for comparing pre-production check patterns across mesh choices.
- [cilium-configuration-validation](../cilium-configuration-validation/SKILL.md) — validating CNI-layer network policy underneath the mesh, relevant when Consul's mesh-level intentions need to be checked against a lower-level `CiliumNetworkPolicy` that could independently block the same traffic.
