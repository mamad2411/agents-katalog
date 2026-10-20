---
name: vault-configuration-validation
description: >
  Guides validating HashiCorp Vault policies (HCL/Rego-less ACL
  policies), auth method configuration, and seal/storage configuration
  before rollout — catching an overly broad policy, a misconfigured
  auth-method role binding, or an unsafe seal migration before it
  reaches a production cluster. Use when the user asks to "validate this
  Vault policy before applying it", "review our Vault auth method
  configuration for least privilege", "check this seal migration plan is
  safe", "lint Vault HCL policies in CI", or "audit Vault policies for
  overly broad access". Distinct from vault-operations-and-pki-engine-
  configuration, which covers running the cluster itself.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: security-scanning-tooling
  maturity: stable
---

# Vault Configuration Validation

## Purpose

A Vault cluster's actual security guarantee is only as strong as its
policies, auth-method role bindings, and seal configuration — a
correctly-operated, highly-available Vault cluster (see
[vault-operations-and-pki-engine-configuration](../vault-operations-and-pki-engine-configuration/SKILL.md))
still leaks broad access if a policy grants `path "secret/*" {
capabilities = ["read"] }` instead of a scoped path, or if a Kubernetes
auth-method role binds to `bound_service_account_names: ["*"]` instead
of a specific service account. Because Vault policy changes take effect
immediately and apply broadly (a single policy can be attached to many
tokens/roles), an overly broad or subtly wrong policy is a
production-security-incident-in-waiting the moment it's applied, not
just a code-review nitpick. This skill covers validating policies, auth
method bindings, and seal/storage configuration changes *before*
rollout — via `vault policy fmt`/`vault policy read` inspection,
automated linting in CI, least-privilege review of path grants, and a
staged-rollout discipline for anything cluster-wide (seal migration,
storage backend changes).

## When to use

- The user has drafted a new or modified Vault ACL policy (HCL) and
  wants it reviewed for overly broad path grants or capability sets
  before applying it to a production cluster.
- The user wants CI-based linting/validation of Vault policy files
  version-controlled alongside application code, rather than manual
  review only at apply time.
- The user is configuring a new auth method (Kubernetes, AWS IAM, OIDC,
  AppRole) and wants the role/binding reviewed for least privilege
  before workloads start authenticating against it.
- The user is planning a seal migration (Shamir → auto-unseal, or
  changing auto-unseal KMS key) and wants the plan validated for safety
  before executing it against a live cluster.
- The user is auditing an existing Vault installation's policies for
  drift from least privilege (wildcard paths, `sudo` capabilities
  granted broadly, root tokens still in use for routine operations).
- Debugging why a token with an attached policy unexpectedly can (or
  cannot) access a specific path.

## Prerequisites & environment

- Vault CLI (`vault`) matching the target cluster's version, with at
  least read access to policies (`vault policy list`/`vault policy
  read`) for inspection — full validation of a *proposed* change can
  happen offline against the HCL file itself without live cluster
  access.
- Policy files version-controlled as HCL (or JSON) in a repo, not only
  ever written directly via `vault policy write` from an ad hoc shell —
  version control is what makes CI-based linting and PR review possible
  at all.
- `vault-lint` or an equivalent policy-linting tool (community tools
  exist; a lightweight in-house script checking for wildcard paths and
  broad capability sets is also a reasonable, low-dependency starting
  point — see the worked example) wired into CI for automated checks
  ahead of manual review.
- For auth-method review: read access to the specific auth method's
  role configuration (`vault read auth/kubernetes/role/<name>`,
  `vault read auth/aws/role/<name>`, etc.) to inspect bound
  constraints.
- For seal-migration review: a maintenance window and a tested rollback
  plan — a seal migration is a cluster-wide, one-way-in-practice
  operation on a live cluster and should never be attempted for the
  first time directly against production.

## Step-by-step guidance

1. **Format and syntax-check every policy file before review** — a
   trivial first gate that catches typos before they reach a human
   reviewer's attention:
   ```bash
   vault policy fmt -check policies/payments-prod-read.hcl
   ```

2. **Review every path grant for scope, not just syntax correctness.**
   A policy that's syntactically valid HCL can still be a
   least-privilege violation:
   ```hcl
   # Overly broad — grants read on every secret under kv-v2, not just this app's
   path "secret/data/*" {
     capabilities = ["read"]
   }
   ```
   ```hcl
   # Scoped — grants read only on this app's specific path
   path "secret/data/payments/prod/*" {
     capabilities = ["read"]
   }
   ```
   Flag any policy with a bare `*` path, a `*` in the middle of a
   segment beyond what's operationally necessary, or capabilities
   broader than the workload's actual need (`create`/`update`/`delete`
   granted to a workload that only ever reads) as requiring
   justification before approval.

3. **Treat `sudo` and root-token usage as high-scrutiny, rare
   exceptions**, not routine capabilities:
   ```hcl
   # Requires explicit justification — sudo capability bypasses most
   # other ACL restrictions for the granted path
   path "sys/raw/*" {
     capabilities = ["sudo", "read"]
   }
   ```
   ```bash
   # Audit whether the root token is still in routine use — it should
   # only ever be used for initial setup/emergency recovery, then revoked
   vault token lookup   # inspect the token currently in use for policy/display_name
   ```
   > **Warning:** a policy granting broad `sudo` capability, or routine
   > operational use of the initial root token instead of scoped,
   > named-identity tokens, undermines least privilege at the platform
   > level — flag both as findings requiring remediation, not accepted
   > operational convenience.

4. **Lint policy files in CI on every change**, catching common
   anti-patterns automatically before human review:
   ```bash
   #!/usr/bin/env bash
   # scripts/lint_vault_policies.sh (illustrative)
   set -euo pipefail
   fail=0
   for f in policies/*.hcl; do
     vault policy fmt -check "$f" || fail=1
     if grep -qE 'path\s+"\*"' "$f"; then
       echo "FAIL: $f grants a bare wildcard path"
       fail=1
     fi
     if grep -qE 'capabilities\s*=\s*\[.*"sudo"' "$f" && ! grep -q "# sudo-justified:" "$f"; then
       echo "FAIL: $f grants sudo capability without a '# sudo-justified:' comment"
       fail=1
     fi
   done
   exit $fail
   ```
   ```yaml
   # .github/workflows/vault-policy-lint.yml
   name: vault-policy-lint
   on: [pull_request]
   jobs:
     lint:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - run: ./scripts/lint_vault_policies.sh
   ```

5. **Validate auth-method role bindings scope to a specific identity**,
   not a wildcard match. Kubernetes auth method example:
   ```bash
   vault read auth/kubernetes/role/payments-prod
   ```
   ```hcl
   # Overly broad — any service account in any namespace can assume this role
   bound_service_account_names:      "*"
   bound_service_account_namespaces: "*"
   ```
   ```hcl
   # Scoped — only the specific service account/namespace pair
   bound_service_account_names:      "payments-svc"
   bound_service_account_namespaces: "payments-prod"
   ```
   AWS IAM auth method equivalent — bind to a specific IAM role/instance
   profile ARN, not `bound_iam_principal_arn: "*"`.

6. **Check token TTL and renewal configuration** on auth-method roles
   and policies — a long-lived, broadly-renewable token defeats much of
   the value of an auth method's identity binding:
   ```bash
   vault read auth/kubernetes/role/payments-prod | grep -E "ttl|max_ttl"
   ```
   Flag `token_max_ttl` set to `0` (unlimited) or an unusually long
   duration (weeks/months) on a role meant to authenticate a
   short-lived workload identity.

7. **Validate a seal-migration plan against a non-production cluster
   first**, never directly against production:
   ```bash
   # Dry-run/staging validation sequence before touching production
   vault operator seal   # confirm current seal type and status on staging
   vault status
   # Apply the new seal stanza to staging config, restart, confirm
   # migration completes and staging remains operable
   vault status   # confirm Type reflects the new seal mechanism
   ```
   Confirm the exact migration steps (config change, restart sequence,
   recovery-key handling) are rehearsed and documented, with a rollback
   plan (reverting the seal stanza and having the prior unseal/recovery
   material on hand) before scheduling a production maintenance window.

8. **Diff policy/auth-method state against the version-controlled source
   of truth periodically**, to catch configuration drift from ad hoc
   `vault policy write`/`vault write auth/.../role/...` changes made
   outside the reviewed change process:
   ```bash
   vault policy read payments-prod-read > /tmp/live-policy.hcl
   diff /tmp/live-policy.hcl policies/payments-prod-read.hcl
   ```

## Best practices

- Version-control every policy and auth-method role definition, and
  require PR review before applying — a `vault policy write` run
  directly from an operator's shell, with no review trail, is exactly
  how drift and over-broad grants accumulate unnoticed.
- Lint for wildcard paths and unjustified `sudo`/broad-capability grants
  in CI, so the cheapest, most common mistakes are caught before a
  human reviewer even looks at the diff.
- Scope every auth-method role binding to a specific identity (exact
  service account/namespace, exact IAM role ARN, exact OIDC
  claim/group) — a wildcard binding on an auth method undoes the
  identity-based access control the auth method exists to provide.
- Set short token TTLs on auth-method roles matching the actual
  workload lifecycle, and review any role with `token_max_ttl: 0` or an
  unusually long duration as a finding.
- Rehearse any seal migration against a non-production cluster first,
  with a documented rollback plan, before scheduling it against
  production — this is a cluster-wide, largely one-way operational
  change.
- Periodically diff live policy/auth-method state against the
  version-controlled source of truth to catch drift from unreviewed ad
  hoc changes.
- Revoke or tightly restrict the initial root token immediately after
  cluster setup, replacing routine operational access with scoped,
  named-identity tokens or auth-method-issued tokens.

## Common pitfalls

- **Symptom:** A policy review approves a change because the HCL syntax
  is valid and the diff "looks small," without checking whether the
  path grant itself is appropriately scoped.
  **Fix:** Make explicit least-privilege path review (not just syntax
  validity) a required checklist item on every policy PR — a
  one-character diff (`secret/data/payments/*` broadened to
  `secret/data/*`) is exactly the kind of "small" change most likely to
  pass an inattentive review.

- **Symptom:** An auth-method role uses a wildcard binding
  (`bound_service_account_names: "*"`) "temporarily, to get it working,"
  and the wildcard is still in place months later.
  **Fix:** Treat a wildcard binding as a blocking finding at initial
  setup, not something to scope down later — retrofitting a specific
  binding after workloads are already depending on the broad one is more
  disruptive than scoping it correctly from the start.

- **Symptom:** A seal migration is attempted directly against
  production during a routine maintenance window, with no prior
  staging rehearsal, and the cluster fails to come back up correctly
  after restart.
  **Fix:** Always rehearse the exact migration steps against a
  non-production cluster first, and have the prior seal's
  unseal/recovery material and a documented rollback path ready before
  touching production — a seal migration is not a low-risk
  configuration tweak.

- **Symptom:** The initial root token generated at cluster
  initialization is still being used for routine day-to-day operations
  a year later.
  **Fix:** Revoke the initial root token after setup (or restrict it to
  emergency-only use with tightly controlled access), and use
  auth-method-issued, scoped tokens for all routine operations —
  ongoing root-token use is a standing, unnecessary blast-radius risk.

- **Symptom:** Live Vault policy state has drifted from what's in the
  version-controlled repo, because someone ran `vault policy write`
  directly during an incident and never backported the change.
  **Fix:** Run a periodic diff of live policy/auth-method state against
  the repo (step 8) as a scheduled check, and require any emergency
  direct change to be backported to version control and reviewed
  within a fixed follow-up window (mirroring the emergency-change
  discipline in
  [critical-vulnerability-emergency-response](../../../devsecops/skills/critical-vulnerability-emergency-response/SKILL.md)).

## Worked example

A platform team reviews a pull request proposing a new Vault policy and
Kubernetes auth-method role for a `payments-svc` workload, before
applying either to production.

Proposed policy (`policies/payments-prod-read.hcl`):
```hcl
# Draft submitted in the PR
path "secret/data/*" {
  capabilities = ["read", "list"]
}
path "pki_int/issue/payments-svc" {
  capabilities = ["create", "update"]
}
```

CI lint output:
```
FAIL: policies/payments-prod-read.hcl grants a bare wildcard path
```

Reviewer requests the scope be narrowed; revised policy:
```hcl
path "secret/data/payments/prod/*" {
  capabilities = ["read", "list"]
}
path "pki_int/issue/payments-svc" {
  capabilities = ["create", "update"]
}
```
CI lint now passes (`vault policy fmt -check` clean, no wildcard-path
match).

Proposed auth-method role (also in the PR):
```hcl
# Draft submitted in the PR
bound_service_account_names:      "*"
bound_service_account_namespaces: "payments-prod"
token_ttl:     "1h"
token_max_ttl: "4h"
```
Reviewer flags the service-account wildcard as a required fix; revised:
```hcl
bound_service_account_names:      "payments-svc"
bound_service_account_namespaces: "payments-prod"
token_ttl:     "1h"
token_max_ttl: "4h"
```

Both changes are approved and merged, then applied to the cluster via
the same CI pipeline that ran the lint (not a manual `vault policy
write` from an operator's shell), keeping the version-controlled source
of truth and the live cluster state in sync from the outset.

## Cross-references

- [vault-operations-and-pki-engine-configuration](../vault-operations-and-pki-engine-configuration/SKILL.md) —
  operating the Vault cluster (seal/unseal, PKI engine, HA/DR topology)
  that this skill's policy and configuration validation protects.
- [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md) —
  the broader secrets-manager selection and least-privilege rationale
  this skill's Vault-specific policy review implements in HCL terms.
- [security-gate-exception-management](../../../devsecops/skills/security-gate-exception-management/SKILL.md) —
  if a genuinely broad grant is temporarily necessary (e.g. a migration
  needing wider read access for a bounded period), route it through a
  scoped, expiring exception rather than approving it as permanent
  policy.
- [opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md) —
  a comparable audit-before-enforce/least-privilege review discipline
  applied to Kubernetes admission policy rather than Vault ACL policy.
