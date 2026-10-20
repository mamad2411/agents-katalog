---
name: opa-gatekeeper-policy-authoring
description: >
  Guides authoring Rego ConstraintTemplates and Constraints for OPA
  Gatekeeper on Kubernetes — admission webhook enforcement, parameterized
  policies, dry-run/audit mode before switching to deny, and debugging
  Rego that under- or over-matches. Use when the user asks to "write a
  Gatekeeper ConstraintTemplate", "write a Rego policy for Kubernetes
  admission", "block pods that violate our security baseline with OPA",
  "add a Constraint with parameters", "why isn't my Gatekeeper policy
  denying anything", or "should we use OPA/Gatekeeper or Kyverno for
  cluster policy".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: policy-and-governance-tooling
  maturity: stable
---

# OPA Gatekeeper Policy Authoring

## Purpose

OPA Gatekeeper packages the general-purpose Open Policy Agent as a
Kubernetes-native admission controller: it registers a `ValidatingWebhookConfiguration`
(and optionally a mutating one) that calls out to Rego policies on every
resource create/update, and it audits existing cluster state against the
same policies on a schedule so drift is caught even for resources created
before a policy existed. The core authoring unit is a **ConstraintTemplate**
(the reusable Rego logic plus a parameter schema) instantiated by one or
more **Constraints** (a concrete resource specifying which Rego template to
apply, to which resources, with which parameter values, in `deny` or
`dryrun` enforcement action). This skill covers the actual mechanics of
writing and testing that Rego, structuring templates so they're reusable
across teams via parameters, and the audit-before-enforce rollout
discipline that keeps a new policy from taking down a legitimate
deployment. It assumes the reader already understands *why* policy as
code matters operationally — see
[policy-as-code-guardrails](../../../devsecops/skills/policy-as-code-guardrails/SKILL.md)
for that framing — and goes deep specifically on Gatekeeper/Rego syntax
and rollout mechanics.

## When to use

- The user wants to write a new `ConstraintTemplate` (e.g. required
  labels, allowed image registries, resource limit requirements, no
  privileged containers) and the `Constraint` that instantiates it.
- The user has an existing Rego policy that isn't firing (no denials) or
  is firing on input it shouldn't (false positives) and needs help
  tracing the actual `input.review.object` structure Gatekeeper passes.
- The user is deciding between OPA/Gatekeeper and Kyverno for a new
  Kubernetes policy and wants the tradeoffs made concrete for their
  specific use case (see the decision guidance below and in
  [kyverno-policy-management](../kyverno-policy-management/SKILL.md)).
- The user wants to parameterize a policy so different teams/namespaces
  can supply different allowed values (e.g. per-team allowed registries)
  without duplicating the Rego.
- The user wants to roll out a new cluster-wide Constraint safely —
  starting in `dryrun`, reviewing violations, then switching to `deny`.
- The user wants to unit test Rego policies (`opa test`) before deploying
  them, or wants CI to run those tests on every policy change.

## Prerequisites & environment

- A Kubernetes cluster (1.21+ for stable `admissionregistration.k8s.io/v1`
  webhooks) with cluster-admin access to install the Gatekeeper CRDs and
  webhook configuration.
- **Gatekeeper** installed via its official Helm chart or manifest
  release (v3.x — the `ConstraintTemplate`/`Constraint` CRD shape used
  below is stable across the v3 line; always check the installed
  version's docs for template-status field names, which have changed
  across minor versions).
- Familiarity with **Rego** (OPA's declarative policy language) — this is
  the main learning-curve cost versus Kyverno's plain YAML; budget time
  for the team to learn `input`, rules, `some`/`every`, and set
  comprehensions rather than assuming it reads like a general-purpose
  language.
- `opa` CLI installed locally for `opa test` and `opa eval` — write and
  test Rego outside the cluster before deploying it as a ConstraintTemplate.
- `gator` (Gatekeeper's own test CLI, `gator test`/`gator verify`) for
  testing full Constraint + ConstraintTemplate + sample-resource bundles
  the way Gatekeeper will actually evaluate them, closer to production
  behavior than raw `opa eval` alone.
- A rollout plan: **every new or changed Constraint must be applied with
  `enforcementAction: dryrun` first**, not `deny`. Skipping this step is
  the single most common cause of an unplanned outage from policy
  rollout.

## Step-by-step guidance

1. **Write the Rego logic as a `violation` rule** inside a
   `ConstraintTemplate`. Gatekeeper's convention is a `package` matching
   the kind, and a `violation[{"msg": msg}]` rule (or `violation[msg]` in
   older syntax) that Gatekeeper collects as denial messages:
   ```yaml
   apiVersion: templates.gatekeeper.sh/v1
   kind: ConstraintTemplate
   metadata:
     name: k8srequiredlabels
   spec:
     crd:
       spec:
         names:
           kind: K8sRequiredLabels
         validation:
           openAPIV3Schema:
             type: object
             properties:
               labels:
                 type: array
                 items: { type: string }
     targets:
       - target: admission.k8s.gatekeeper.sh
         rego: |
           package k8srequiredlabels

           violation[{"msg": msg}] {
             required := input.parameters.labels
             provided := input.review.object.metadata.labels
             missing := required[_]
             not provided[missing]
             msg := sprintf("missing required label: %v", [missing])
           }
   ```

2. **Instantiate it with a `Constraint`**, scoping `match` tightly and
   starting in `dryrun`:
   ```yaml
   apiVersion: constraints.gatekeeper.sh/v1beta1
   kind: K8sRequiredLabels
   metadata:
     name: require-team-label
   spec:
     enforcementAction: dryrun   # start here — never `deny` on first rollout
     match:
       kinds:
         - apiGroups: [""]
           kinds: ["Namespace"]
     parameters:
       labels: ["team", "cost-center"]
   ```

3. **Inspect the actual admission review payload** before assuming a
   field path — `input.review.object` mirrors the resource's JSON, but
   nested fields (e.g. container-level `securityContext`) require
   iterating arrays with `[_]`, and typos here are the most common reason
   a policy silently never denies:
   ```rego
   package k8sdisallowedprivileged

   violation[{"msg": msg}] {
     c := input.review.object.spec.containers[_]
     c.securityContext.privileged == true
     msg := sprintf("privileged container not allowed: %v", [c.name])
   }
   ```
   Test the exact shape with `kubectl create --dry-run=server -o json` or
   by checking the audit logs of a recently created resource, rather than
   guessing at the schema.

4. **Unit-test the Rego with `opa test`** before deploying, covering both
   a case that must violate and one that must pass:
   ```rego
   package k8sdisallowedprivileged

   test_privileged_denied {
     count(violation) == 1 with input as {
       "review": {"object": {"spec": {"containers": [
         {"name": "app", "securityContext": {"privileged": true}}
       ]}}}
     }
   }

   test_nonprivileged_allowed {
     count(violation) == 0 with input as {
       "review": {"object": {"spec": {"containers": [
         {"name": "app", "securityContext": {"privileged": false}}
       ]}}}
     }
   }
   ```
   ```bash
   opa test policies/ -v
   ```

5. **Test the full Constraint bundle with `gator`**, which evaluates
   ConstraintTemplate + Constraint + sample resources the same way
   Gatekeeper does in-cluster (catching schema/parameter-wiring bugs
   `opa test` alone won't see):
   ```bash
   gator test --filename=policies/
   ```

6. **Deploy in `dryrun` and review violations before flipping to `deny`.**
   Query violations without blocking anything:
   ```bash
   kubectl get k8srequiredlabels require-team-label -o yaml \
     | grep -A5 "status:"
   ```
   Gatekeeper surfaces violations in the Constraint's `.status.violations`
   list (subject to a configurable limit) — review this for at least one
   full deploy cycle before enforcing.

7. **Switch to `deny` once dryrun is clean**, and add narrowly-scoped,
   documented exceptions via `excludedNamespaces` rather than disabling
   the Constraint:
   ```yaml
   spec:
     enforcementAction: deny
     match:
       excludedNamespaces: ["kube-system", "legacy-migration"]  # owner: platform-team, review: 2026-10-15
   ```

8. **Watch webhook failure behavior explicitly** — Gatekeeper's
   `failurePolicy` on the webhook configuration determines what happens
   if the Gatekeeper pods themselves are unreachable. `Fail` (the safer
   default for security-critical policies) blocks all matching admission
   requests cluster-wide if Gatekeeper is down; `Ignore` lets requests
   through unchecked during an outage. Choose deliberately per policy
   criticality, and monitor Gatekeeper pod health as a dependency of
   cluster admission itself.
   > **Warning — destructive action risk:** a `failurePolicy: Fail`
   >  Constraint combined with a Gatekeeper outage or a webhook
   >  misconfiguration can block **all** matching deploys cluster-wide,
   >  not just the specific resource that should fail. Before setting
   >  `Fail` on any new Constraint, confirm there's a rollback path
   >  (`kubectl delete constraint <name>` or patch `enforcementAction`
   >  back to `dryrun`) that on-call staff know how to execute quickly.

9. **Version-control ConstraintTemplates and Constraints together** in
   the same repo as application manifests (or a dedicated policy repo),
   and require PR review on changes — a policy change is a
   production-admission-behavior change.

## Best practices

- Keep the reusable logic in the `ConstraintTemplate` and all
  environment/team-specific values in `Constraint.spec.parameters` — this
  is what lets one Rego template serve many teams' differing allowlists
  without forking the Rego itself.
- Prefer `violation[{"msg": msg}]` (the newer, structured form) over bare
  `deny[msg]` for new templates — it's the form Gatekeeper's tooling and
  docs standardize on and supports richer metadata per violation.
- Scope `match` as tightly as possible (specific `kinds`, `namespaces`,
  or label selectors) rather than matching all resources cluster-wide —
  a loosely-scoped Constraint is both slower to evaluate and harder to
  reason about when debugging a false positive.
- Always roll out via `dryrun` → review → `deny`, never straight to
  `deny`, even for a policy that looks obviously correct — the risk
  isn't that the Rego is wrong, it's that real cluster state includes
  legitimate exceptions the author didn't anticipate.
- Write both a should-violate and a should-not-violate test case for
  every rule in `opa test` — a rule that compiles cleanly but has a typo'd
  field path will silently pass every input, and only a should-violate
  test catches that.
- Use `gator test`, not just `opa test`, before deploying — `opa test`
  validates the Rego logic in isolation; `gator test` validates that the
  ConstraintTemplate's parameter schema, the Constraint's parameter
  values, and the `match` block actually wire together the way Gatekeeper
  will evaluate them in-cluster.
- Set resource requests/limits on the Gatekeeper controller pods
  themselves and monitor their health — Gatekeeper being down is itself
  an admission-control availability incident, not just a policy concern.

## Common pitfalls

- **Symptom:** A new Constraint is deployed with `enforcementAction: deny`
  directly, and it immediately rejects a legitimate deployment, paging
  on-call.
  **Fix:** Always deploy new/changed Constraints with `enforcementAction:
  dryrun` first, review `.status.violations` for a representative period
  (a full deploy cycle), then switch to `deny` with documented namespace
  exceptions for anything legitimate the dry run surfaced.

- **Symptom:** The Rego compiles and the Constraint shows `Ready: true`,
  but it never denies anything — even a resource that obviously should
  violate it.
  **Fix:** Dump the actual `input` Gatekeeper evaluates (via `gator test
  --trace` or by comparing against a real admission review payload) and
  check for a mismatched field path or an assumption about array vs.
  scalar shape — e.g. checking `input.review.object.spec.securityContext`
  when the field is actually per-container at
  `input.review.object.spec.containers[_].securityContext`. This is the
  single most common Rego bug and produces a false negative that looks
  like a working, passing policy.
- **Fix (variant):** For rules using `not`, verify the rule isn't
  accidentally satisfied by a missing field being treated as "compliant"
  — `not provided[missing]` alone doesn't distinguish "field absent" from
  "field explicitly set to an empty/false value" unless the Rego is
  written to check for that distinction deliberately.

- **Symptom:** A single monolithic ConstraintTemplate handles labels,
  registries, and resource limits together with a giant parameter schema,
  and a change requested for one team's registry allowlist requires
  re-reviewing the whole template.
  **Fix:** Split into one ConstraintTemplate per concern (labels,
  registries, resource limits, non-root) with narrow parameter schemas,
  each with its own Constraint(s) — easier to test, easier to grant one
  team a scoped exception on one rule without touching the others.

- **Symptom:** A Gatekeeper pod outage combined with
  `failurePolicy: Fail` on a webhook blocks every deploy cluster-wide,
  including unrelated emergency hotfixes, during an incident.
  **Fix:** Treat Gatekeeper pod health as a monitored, alertable
  dependency of cluster admission; keep a documented, fast rollback path
  (deleting or patching the problem Constraint, or in a true emergency,
  patching the webhook's `failurePolicy` to `Ignore` temporarily) that
  on-call staff can execute without needing to understand Rego under
  pressure.

- **Symptom:** Audit mode (`dryrun`) shows zero violations for weeks, so
  the team assumes the policy is safe to enforce — then enforcing it
  immediately blocks a deploy from a workflow that only runs quarterly
  (e.g. a batch job or a DR failover) and wasn't exercised during the
  audit window.
  **Fix:** Make sure the dry-run review window covers infrequent but
  legitimate deploy paths, not just the common daily/weekly cadence, or
  explicitly flag the gap and stage a longer or targeted dry-run for
  those paths before enforcing cluster-wide.

## Worked example

A platform team wants to require that all container images referenced in
`Pod` specs come from an approved internal registry, enforced at
admission and parameterized so different clusters can use different
allowlists.

`templates/k8sallowedregistries.yaml`:
```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sallowedregistries
spec:
  crd:
    spec:
      names:
        kind: K8sAllowedRegistries
      validation:
        openAPIV3Schema:
          type: object
          properties:
            registries:
              type: array
              items: { type: string }
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sallowedregistries

        violation[{"msg": msg}] {
          c := input.review.object.spec.containers[_]
          not allowed(c.image)
          msg := sprintf("image %v is not from an approved registry", [c.image])
        }

        allowed(image) {
          registry := input.parameters.registries[_]
          startswith(image, registry)
        }
```

`policies/k8sallowedregistries_test.rego`:
```rego
package k8sallowedregistries

test_disallowed_registry_denied {
  count(violation) == 1 with input as {
    "review": {"object": {"spec": {"containers": [
      {"name": "app", "image": "docker.io/library/nginx:latest"}
    ]}}},
    "parameters": {"registries": ["registry.example.internal/"]}
  }
}

test_allowed_registry_passes {
  count(violation) == 0 with input as {
    "review": {"object": {"spec": {"containers": [
      {"name": "app", "image": "registry.example.internal/team-a/app:1.4.2"}
    ]}}},
    "parameters": {"registries": ["registry.example.internal/"]}
  }
}
```

`constraints/require-approved-registry.yaml` (rolled out `dryrun` first):
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAllowedRegistries
metadata:
  name: require-approved-registry
spec:
  enforcementAction: dryrun
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    excludedNamespaces: ["kube-system"]
  parameters:
    registries:
      - "registry.example.internal/"
```

CI wiring:
```bash
opa test policies/ -v
gator test --filename=templates/ --filename=constraints/
```

Rollout: after a one-week `dryrun` period, `kubectl get
k8sallowedregistries require-approved-registry -o jsonpath='{.status.violations}'`
shows zero unexpected hits, so the team patches `enforcementAction: deny`.
From then on, `kubectl apply -f pod-using-dockerhub.yaml` is rejected at
admission time with `admission webhook "validation.gatekeeper.sh" denied
the request: [require-approved-registry] image docker.io/library/nginx:latest
is not from an approved registry` — regardless of whether the apply came
from CI or a direct `kubectl` command.

## Cross-references

- [kyverno-policy-management](../kyverno-policy-management/SKILL.md) —
  the YAML-native alternative to writing Rego for the same class of
  Kubernetes admission policies; read this to decide which engine fits a
  given team/use case.
- [fairwinds-polaris-and-goldilocks](../fairwinds-polaris-and-goldilocks/SKILL.md) —
  a lighter-weight, opinionated tool for workload configuration scoring
  and right-sizing that complements (and can precede) writing custom
  Gatekeeper policies for the same properties.
- [policy-as-code-guardrails](../../../devsecops/skills/policy-as-code-guardrails/SKILL.md) —
  the broader rationale for policy as code, audit-first rollout
  discipline, and how admission policy fits alongside CI-time IaC checks.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) —
  where admission-time enforcement fits relative to earlier pipeline
  gates.
