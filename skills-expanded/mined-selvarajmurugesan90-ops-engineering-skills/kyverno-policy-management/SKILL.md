---
name: kyverno-policy-management
description: >
  Guides writing Kyverno ClusterPolicy/Policy resources using its
  YAML-native validate/mutate/generate rule syntax — a Rego-free
  alternative to OPA/Gatekeeper for Kubernetes admission control — plus
  audit-vs-enforce rollout and PolicyReport-based reporting. Use when the
  user asks to "write a Kyverno policy", "mutate resources on admission
  to inject a sidecar or default", "auto-generate a NetworkPolicy or
  ResourceQuota per namespace", "should we use Kyverno or OPA/Gatekeeper",
  or "why is my Kyverno validate rule not blocking/passing as expected".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: policy-and-governance-tooling
  maturity: stable
---

# Kyverno Policy Management

## Purpose

Kyverno is a Kubernetes-native policy engine that expresses admission
policies as plain Kubernetes YAML (`ClusterPolicy`/`Policy` custom
resources) instead of a separate policy language — a team that already
reads and writes Kubernetes manifests can read and modify a Kyverno rule
without learning Rego. Beyond validation (the OPA/Gatekeeper-equivalent
"allow or deny this resource"), Kyverno natively supports **mutate**
rules (rewrite or inject fields into a resource on admission — e.g. add a
sidecar, default a label) and **generate** rules (auto-create a companion
resource when a triggering resource appears — e.g. a default
`NetworkPolicy` or `ResourceQuota` whenever a new `Namespace` is created),
both of which OPA/Gatekeeper handles less directly. This skill covers
Kyverno's actual rule syntax across all three rule types, its
`background`/`validationFailureAction` audit-vs-enforce controls, and
`PolicyReport` output for visibility — and gives explicit guidance on
when Kyverno's YAML-native approach is the better fit than OPA/Gatekeeper
versus when Rego's generality is worth the learning-curve cost.

## When to use

- The user wants to write a `ClusterPolicy` or namespaced `Policy` to
  validate, mutate, or auto-generate Kubernetes resources, without
  writing Rego.
- The user wants to inject or default fields on admission (a sidecar
  container, an annotation, a resource limit default) rather than only
  reject non-compliant resources — a `mutate` rule use case Kyverno
  handles more directly than Gatekeeper.
- The user wants a companion resource auto-created whenever a triggering
  resource is created (e.g. a default-deny `NetworkPolicy` for every new
  `Namespace`) — a `generate` rule use case.
- The user is deciding between Kyverno and OPA/Gatekeeper for a new
  policy and wants the concrete tradeoffs for their team/use case, not
  just an abstract comparison.
- The user has a Kyverno `validate` rule that isn't blocking (or is
  over-blocking) resources it should, and needs help debugging the
  pattern-matching syntax.
- The user wants policy compliance reporting (`PolicyReport` /
  `ClusterPolicyReport`) surfaced to a dashboard or CI step.

## Prerequisites & environment

- A Kubernetes cluster (1.21+ recommended for the admission webhook
  behavior Kyverno relies on) with cluster-admin access to install the
  Kyverno CRDs, controller, and webhook configurations.
- **Kyverno** installed via its Helm chart or static manifests (the
  `kyverno.io/v1` and `kyverno.io/v2beta1` API groups have both existed
  across recent versions — check which API version the installed
  Kyverno release expects, since field names for match/exclude blocks
  have shifted between them).
- No Rego required — this is Kyverno's core value proposition versus
  OPA/Gatekeeper — but understanding its own pattern-matching DSL
  (`pattern`/`anyPattern` blocks, JMESPath for dynamic values) is still
  necessary; it is simpler than Rego but not zero-learning-curve.
- `kyverno` CLI installed locally for `kyverno test` (offline unit testing
  against sample resources) before deploying policies to a live cluster.
- A rollout plan: **every new or changed policy must be applied with
  `validationFailureAction: Audit` first**, not `Enforce` — identical
  discipline to Gatekeeper's `dryrun`, and for the same reason (surfacing
  what a policy would have blocked before it can break a legitimate
  deploy).
- For `generate` rules specifically: understand that generated resources
  can persist after the triggering policy is deleted unless
  `generateExisting`/cleanup behavior is deliberately configured — treat
  generate-rule rollout with extra care since it creates new cluster
  state, not just gates existing requests.

## Step-by-step guidance

1. **Write a `validate` rule in `Audit` mode first**, using Kyverno's
   `pattern` block (structural match against the resource) rather than
   Rego:
   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: require-run-as-non-root
   spec:
     validationFailureAction: Audit   # start here, not Enforce
     background: true                 # also evaluate existing resources, not just new admissions
     rules:
       - name: check-runAsNonRoot
         match:
           any:
             - resources:
                 kinds: ["Pod"]
         validate:
           message: "Containers must set securityContext.runAsNonRoot: true"
           pattern:
             spec:
               securityContext:
                 runAsNonRoot: true
   ```

2. **Use `anyPattern` for "one of several acceptable shapes"** rather than
   a single rigid `pattern`, when more than one configuration is
   compliant:
   ```yaml
   validate:
     message: "Must use either a read-only root filesystem or an explicit exception annotation"
     anyPattern:
       - spec:
           containers:
             - securityContext:
                 readOnlyRootFilesystem: true
       - metadata:
           annotations:
             policy.example.com/rootfs-exception: "?*"
   ```

3. **Review `PolicyReport`/`ClusterPolicyReport` results** generated
   during the audit period before enforcing:
   ```bash
   kubectl get clusterpolicyreport -o wide
   kubectl get policyreport -A -o jsonpath='{.items[*].summary}'
   ```

4. **Switch to `Enforce` once audit is clean**, with a documented,
   time-boxed exclusion for genuine exceptions:
   ```yaml
   spec:
     validationFailureAction: Enforce
     rules:
       - name: check-runAsNonRoot
         match:
           any:
             - resources:
                 kinds: ["Pod"]
         exclude:
           any:
             - resources:
                 namespaces: ["legacy-migration"]  # owner: platform-team, review: 2026-10-01
   ```
   > **Warning — destructive action risk:** switching `validationFailureAction`
   > to `Enforce` on a broadly-scoped `ClusterPolicy` blocks every
   > matching admission cluster-wide the moment it's applied — not just
   > new deploys from CI, but any `kubectl apply`. Confirm the audit
   > period covered representative traffic and that a rollback
   > (`kubectl patch clusterpolicy <name> --type merge -p
   > '{"spec":{"validationFailureAction":"Audit"}}'`) is understood by
   > on-call before enforcing against production namespaces.

5. **Use `mutate` rules to inject or default fields** rather than only
   rejecting non-compliant resources — useful for defaults that don't
   need a human decision (e.g. a default `imagePullPolicy`, an
   observability sidecar):
   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: add-default-resources
   spec:
     rules:
       - name: default-resource-limits
         match:
           any:
             - resources:
                 kinds: ["Pod"]
         mutate:
           patchStrategicMerge:
             spec:
               containers:
                 - (name): "*"
                   resources:
                     limits:
                       +(memory): "512Mi"   # only sets if not already present
   ```
   Test mutate rules especially carefully — unlike validate rules, a
   mutate bug silently changes what gets deployed rather than rejecting
   it, which is harder to notice.

6. **Use `generate` rules for auto-provisioned companion resources**,
   being deliberate about cleanup behavior:
   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: default-deny-networkpolicy
   spec:
     rules:
       - name: generate-default-deny
         match:
           any:
             - resources:
                 kinds: ["Namespace"]
         generate:
           apiVersion: networking.k8s.io/v1
           kind: NetworkPolicy
           name: default-deny-all
           namespace: "{{request.object.metadata.name}}"
           synchronize: true   # keep generated resource in sync with policy changes
           data:
             spec:
               podSelector: {}
               policyTypes: ["Ingress", "Egress"]
   ```
   With `synchronize: true`, editing or deleting the policy also updates
   or removes the generated resource — understand this before rollout, so
   deleting the policy doesn't unexpectedly remove protective
   NetworkPolicies teams have come to depend on.

7. **Unit test policies offline with `kyverno test`** before applying to
   a cluster:
   ```bash
   kyverno test policies/require-run-as-non-root/
   ```
   ```yaml
   # policies/require-run-as-non-root/kyverno-test.yaml
   name: test-require-non-root
   policies:
     - ../require-run-as-non-root.yaml
   resources:
     - resources/pod-root.yaml
     - resources/pod-nonroot.yaml
   results:
     - policy: require-run-as-non-root
       rule: check-runAsNonRoot
       resource: pod-root
       result: fail
     - policy: require-run-as-non-root
       rule: check-runAsNonRoot
       resource: pod-nonroot
       result: pass
   ```

8. **Wire `PolicyReport` output into CI or a dashboard** so compliance
   status is visible without manually querying the cluster:
   ```bash
   kubectl get policyreport -A -o json | \
     jq '[.items[].results[] | select(.result=="fail")] | length'
   ```

9. **Version-control policies alongside application manifests**, PR-review
   changes, and keep one policy per concern rather than one giant
   multi-rule `ClusterPolicy` covering unrelated checks.

## Best practices

- Choose Kyverno when the target is Kubernetes-only, the team is more
  comfortable with YAML than a new DSL, and the use case benefits from
  `mutate`/`generate` (defaulting fields, auto-provisioning companion
  resources) — these are first-class Kyverno concepts that are more
  awkward to express in OPA/Gatekeeper. Choose OPA/Gatekeeper
  ([opa-gatekeeper-policy-authoring](../opa-gatekeeper-policy-authoring/SKILL.md))
  when policies need to run outside Kubernetes too (CI-time Terraform
  plan checks via Conftest, API authorization), when logic is complex
  enough that Rego's real programming constructs (helper functions,
  recursion, set operations) pay off over pattern-matching YAML, or when
  the org has already standardized on OPA elsewhere and wants one engine.
- Prefer `pattern`/`anyPattern` blocks for straightforward structural
  checks; reach for JMESPath expressions only when a pattern block
  genuinely can't express the condition — pattern blocks stay readable to
  someone who's never seen Kyverno before, which is the point of choosing
  Kyverno.
- Test `mutate` rules more cautiously than `validate` rules — a
  validate-rule bug rejects things it shouldn't (loud, visible failure);
  a mutate-rule bug silently changes what gets deployed (quiet,
  potentially discovered much later).
- Understand `synchronize: true` on `generate` rules before using it in
  production — it means deleting or editing the policy also
  deletes/edits the generated resource, which is powerful but surprising
  if the team expects generated resources to be independent once
  created.
- Roll out every new or changed policy `Audit` → review `PolicyReport` →
  `Enforce`, identically to the Gatekeeper `dryrun` → `deny` pattern —
  the two engines differ in syntax, not in the rollout discipline needed.
- Keep one `ClusterPolicy` per concern (non-root, registry allowlist,
  resource defaults) rather than bundling unrelated rules into one
  resource, so a scoped exception or a rollback doesn't have to touch
  unrelated rules.

## Common pitfalls

- **Symptom:** A new `ClusterPolicy` is applied directly with
  `validationFailureAction: Enforce` and immediately blocks a legitimate
  deploy, triggering an incident.
  **Fix:** Always deploy with `validationFailureAction: Audit` first,
  review `PolicyReport`/`ClusterPolicyReport` results for a representative
  period, then switch to `Enforce` with documented, time-boxed
  `exclude` blocks for anything legitimate the audit surfaced.

- **Symptom:** A `validate` rule with a `pattern` block never fails,
  even for a resource that clearly violates the intended rule.
  **Fix:** Kyverno's `pattern` matching requires the field structure to
  match exactly, including array-vs-object shape; a common cause is
  writing `pattern: {spec: {containers: {securityContext: ...}}}`
  (treating `containers` as an object) when it's actually a list and
  needs `containers: - securityContext: ...`. Run `kyverno test` against
  a sample resource that should fail and inspect the actual result before
  trusting the policy is live.

- **Symptom:** A `mutate` rule intended to set a default resource limit
  ends up overwriting a value teams had deliberately set higher than the
  default.
  **Fix:** Use the `+()` conditional-anchor syntax (`+(memory): "512Mi"`)
  which only applies the patch when the field is absent, rather than an
  unconditional patch that always overwrites — verify this with
  `kyverno test` cases covering both "field absent" and "field already
  set" resources.

- **Symptom:** A `generate` rule with `synchronize: true` is deleted as
  part of a policy cleanup, and previously-generated `NetworkPolicy`
  resources teams depended on for isolation silently disappear along with
  it, temporarily removing network segmentation.
  **Fix:** Before deleting or disabling a `generate` policy with
  `synchronize: true`, check what resources it has generated
  (`kubectl get networkpolicy -A -l kyverno.io/generated-by-policy) and
  decide deliberately whether to detach (patch `synchronize: false`
  first, which stops further sync but leaves existing generated resources
  in place) versus a full removal.

- **Symptom:** Team picked Kyverno for everything, including a CI-time
  check on Terraform plans, and finds the policy awkward to express or
  simply unsupported.
  **Fix:** Kyverno's design center is Kubernetes admission (and, via
  newer `ClusterCleanupPolicy`/JSON payload support, some non-Kubernetes
  JSON validation) — but non-Kubernetes IaC gating (Terraform plan JSON,
  arbitrary CI artifacts) is squarely OPA/Conftest's use case as covered
  in [policy-as-code-guardrails](../../../devsecops/skills/policy-as-code-guardrails/SKILL.md).
  Use Kyverno for Kubernetes-native admission policy and OPA/Conftest for
  IaC/CI-time checks rather than forcing one engine to do both.

## Worked example

A platform team standardizes on Kyverno (team is Kubernetes-YAML-fluent,
no existing Rego investment) for three policies: validating non-root
containers, defaulting a memory limit via mutation, and auto-generating a
default-deny NetworkPolicy per namespace.

`policies/require-non-root.yaml` (Audit, then Enforce after a clean week):
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-run-as-non-root
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: check-runAsNonRoot
      match:
        any:
          - resources:
              kinds: ["Pod"]
      exclude:
        any:
          - resources:
              namespaces: ["legacy-migration"]  # owner: platform-team, review: 2026-10-01
      validate:
        message: "Containers must set securityContext.runAsNonRoot: true"
        pattern:
          spec:
            securityContext:
              runAsNonRoot: true
```

`policies/default-memory-limit.yaml`:
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: default-memory-limit
spec:
  rules:
    - name: set-default-memory-limit
      match:
        any:
          - resources:
              kinds: ["Pod"]
      mutate:
        patchStrategicMerge:
          spec:
            containers:
              - (name): "*"
                resources:
                  limits:
                    +(memory): "512Mi"
```

`policies/default-deny-netpol.yaml`:
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: default-deny-networkpolicy
spec:
  rules:
    - name: generate-default-deny
      match:
        any:
          - resources:
              kinds: ["Namespace"]
      generate:
        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy
        name: default-deny-all
        namespace: "{{request.object.metadata.name}}"
        synchronize: true
        data:
          spec:
            podSelector: {}
            policyTypes: ["Ingress", "Egress"]
```

Offline test before rollout:
```bash
kyverno test policies/require-non-root/
```
```yaml
# policies/require-non-root/kyverno-test.yaml
name: test-require-non-root
policies:
  - ../require-non-root.yaml
resources:
  - resources/pod-root.yaml
  - resources/pod-nonroot.yaml
results:
  - policy: require-run-as-non-root
    rule: check-runAsNonRoot
    resource: pod-root
    result: fail
  - policy: require-run-as-non-root
    rule: check-runAsNonRoot
    resource: pod-nonroot
    result: pass
```

After applying, creating a namespace `team-payments` automatically
provisions `NetworkPolicy/default-deny-all` in that namespace, and
`kubectl get policyreport -n team-payments` confirms the non-root policy
is passing for all existing Pods before the team flips it from `Audit` to
`Enforce`.

## Cross-references

- [opa-gatekeeper-policy-authoring](../opa-gatekeeper-policy-authoring/SKILL.md) —
  the Rego-based alternative; read this to decide which engine fits a
  given team/use case, especially for non-Kubernetes (CI/IaC) policy
  needs Kyverno doesn't cover.
- [fairwinds-polaris-and-goldilocks](../fairwinds-polaris-and-goldilocks/SKILL.md) —
  a lighter-weight, no-authoring-required option for common workload
  configuration checks (resource limits, probes, security context) that
  may cover a policy before it's worth writing a custom Kyverno rule for
  it.
- [policy-as-code-guardrails](../../../devsecops/skills/policy-as-code-guardrails/SKILL.md) —
  the broader policy-as-code rationale and audit-before-enforce
  discipline this skill's rollout steps follow.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) —
  where Kyverno's admission-time enforcement fits relative to earlier
  CI-time pipeline gates.
