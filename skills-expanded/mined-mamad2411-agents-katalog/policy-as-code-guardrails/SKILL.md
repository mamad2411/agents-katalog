---
name: policy-as-code-guardrails
description: >
  Guides writing and enforcing security/compliance policies as code using
  Open Policy Agent (OPA)/Rego, Kyverno, or Conftest, applied to
  Kubernetes admission control, CI/CD pipeline gates, and Infrastructure
  as Code (Terraform/CloudFormation) review. Use when the user asks to
  "write an OPA policy", "block insecure Terraform/Kubernetes configs",
  "add admission control guardrails", "enforce that all images must be
  signed/non-root/from an approved registry", or "codify our security
  baseline as automated policy instead of a manual checklist". Explains
  what enforcement actually guarantees versus what still needs separate
  controls.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# Policy as Code & Guardrails

## Purpose

Security and compliance requirements ("containers must not run as root",
"S3 buckets must not be public", "images must come from an approved
registry and be signed") are traditionally enforced through manual
review checklists or after-the-fact audits — both slow, inconsistent,
and easy to skip under deadline pressure. Policy as Code expresses these
requirements as machine-readable, version-controlled rules (Rego for Open
Policy Agent, Kyverno's YAML-based policies, Sentinel for HashiCorp
products) and enforces them automatically at a control point: a
Kubernetes admission webhook rejecting a non-compliant pod at creation
time, a CI step failing a plan that would create a public S3 bucket, a
pre-merge check blocking a Dockerfile that runs as root. This turns
security requirements from documentation into guardrails that hold even
when nobody remembers to check the checklist — but it only guarantees
what the policy actually checks, and only at the point where it's wired
in; a policy engine is not a substitute for the underlying controls
(scanning, signing, least privilege) it's verifying the presence of.

## When to use

- The user asks to "write an OPA/Rego policy" or "add Kyverno policies"
  for a Kubernetes cluster.
- The user wants to block Terraform/CloudFormation/Pulumi plans that
  would create insecure infrastructure (public storage buckets,
  unencrypted volumes, overly permissive security groups/IAM) before
  `apply` runs.
- The user wants to enforce that container images are signed, scanned,
  non-root, or from an approved registry, at the Kubernetes admission
  layer rather than trusting CI alone.
- A security team wants to "codify" a manual review checklist so it
  becomes an automated, consistent gate instead of a document reviewers
  interpret inconsistently.
- The user is troubleshooting a policy that's too strict (blocking
  legitimate deploys) or too permissive (letting through what it should
  block), and needs help writing/testing Rego or Kyverno rules.
- The user wants a "dry-run"/audit mode before switching a new policy to
  enforcing, to avoid a surprise outage from a policy rollout.

## Prerequisites & environment

- **Open Policy Agent (OPA)** + **Rego** — general-purpose policy engine
  usable for Kubernetes admission (via Gatekeeper), CI/CD gates, API
  authorization, and more; steeper learning curve (Rego is its own
  declarative language) but the most flexible and widely adopted option.
- **Gatekeeper** — OPA's Kubernetes-native wrapper, providing
  `ConstraintTemplate`/`Constraint` CRDs so Rego policies integrate with
  standard Kubernetes admission webhooks and audit results as native
  resources.
- **Kyverno** — Kubernetes-native alternative to OPA/Gatekeeper using
  plain YAML instead of Rego; lower learning curve for teams already
  comfortable with Kubernetes manifests, slightly less general-purpose
  outside the Kubernetes context.
- **Conftest** — runs OPA/Rego policies against structured config files
  (Terraform plan JSON, Kubernetes YAML, Dockerfiles via a parser) outside
  a live cluster, useful for CI-time IaC policy checks before anything is
  applied.
- **HashiCorp Sentinel** — policy-as-code tied specifically to Terraform
  Cloud/Enterprise; relevant if already standardized on that platform.
- A Kubernetes cluster with admission webhook support (standard in any
  reasonably current distribution) if enforcing at the cluster level;
  cluster-admin or equivalent to install Gatekeeper/Kyverno.
- A staged rollout plan: **every new policy should run in `audit`/`dry-run`
  mode first**, not `enforce`, to surface what it would have blocked
  against real traffic/manifests before it can cause an outage.

## Step-by-step guidance

1. **Start with an audit-only policy** to see impact before blocking
   anything. Kyverno example requiring non-root containers, in audit mode:
   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: require-run-as-non-root
   spec:
     validationFailureAction: Audit   # start here, not Enforce
     rules:
       - name: check-runAsNonRoot
         match:
           resources:
             kinds: [Pod]
         validate:
           message: "Containers must set runAsNonRoot: true"
           pattern:
             spec:
               securityContext:
                 runAsNonRoot: true
   ```

2. **Write the equivalent in Rego/OPA/Gatekeeper** if standardizing on
   OPA instead:
   ```rego
   package k8s.security

   deny[msg] {
     input.request.kind.kind == "Pod"
     container := input.request.object.spec.containers[_]
     not container.securityContext.runAsNonRoot
     msg := sprintf("container %v must set runAsNonRoot: true", [container.name])
   }
   ```

3. **Review audit results for a full deploy cycle** (at least a week, or
   however long covers your normal deployment cadence) before flipping to
   enforcing — this catches legitimate workloads the policy would have
   broken (e.g. a base image that genuinely needs root for a startup
   step) so you can add a scoped exception rather than breaking
   production on rollout day.

4. **Switch to enforcing once audit is clean**, and add a documented,
   narrowly-scoped exception mechanism for genuine exceptions rather than
   disabling the policy for a whole namespace:
   ```yaml
   spec:
     validationFailureAction: Enforce
     rules:
       - name: check-runAsNonRoot
         exclude:
           resources:
             namespaces: ["legacy-migration"]   # documented, time-boxed exception
   ```

5. **Add IaC-time policy checks with Conftest** so violations are caught
   before `terraform apply`, not after a resource already exists:
   ```rego
   package terraform.security

   deny[msg] {
     resource := input.resource_changes[_]
     resource.type == "aws_s3_bucket"
     resource.change.after.acl == "public-read"
     msg := sprintf("S3 bucket %v must not be public-read", [resource.address])
   }
   ```
   ```yaml
   # CI step
   - name: Terraform plan
     run: terraform plan -out=plan.tfplan && terraform show -json plan.tfplan > plan.json
   - name: Conftest policy check
     run: conftest test plan.json --policy policies/
   ```

6. **Enforce supply-chain policies at admission** (signed images,
   approved registries) as a defense-in-depth layer even when CI already
   checks these, since CI checks can be bypassed by anyone who can push
   directly to the registry or apply manifests outside the pipeline:
   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: restrict-image-registries
   spec:
     validationFailureAction: Enforce
     rules:
       - name: allowed-registries
         match:
           resources:
             kinds: [Pod]
         validate:
           message: "Images must come from approved registry"
           pattern:
             spec:
               containers:
                 - image: "registry.example.internal/*"
   ```

7. **Unit-test policies themselves**, not just run them against live
   traffic — both OPA (`opa test`) and Kyverno (`kyverno test`) support
   writing test cases with expected allow/deny outcomes:
   ```bash
   opa test policies/ -v
   ```

8. **Version-control policies and review changes like code** (PR review,
   changelog) — a policy change is a security-relevant change to
   production behavior and should go through the same rigor as
   application code, including a rollback plan.

## Best practices

- Always roll out new policies in audit/dry-run mode first, and review
  actual audit hits before enforcing — this is the single highest-value
  habit for avoiding "the new policy broke prod on a Friday."
- Keep policies narrowly scoped and composable (one policy per concern:
  non-root, registry allowlist, resource limits) rather than one giant
  monolithic policy — easier to test, easier to grant a scoped exception
  to one rule without disabling everything else.
- Enforce supply-chain and admission policies as defense-in-depth even
  when the same check exists in CI — CI can be bypassed by direct
  `kubectl apply`/console access or a misconfigured pipeline, whereas an
  admission-time policy applies regardless of how the request arrived.
- Be explicit about what a passing policy check actually proves: a policy
  requiring `runAsNonRoot: true` proves that field is set — it says
  nothing about whether the application itself is secure, whether its
  image is vulnerability-free, or whether it's from a trusted source.
  Don't let "policy passed" get conflated with "workload is safe."
- Time-box and document every exception (a namespace exclusion, a policy
  override annotation) with an owner and a review date — undocumented,
  permanent exceptions are how guardrails quietly become no-ops.
- Unit test policies against both cases that should pass and cases that
  should fail — a policy that's never been tested against a
  should-be-rejected input can silently be a no-op due to a typo in a
  field path.

## Common pitfalls

- **Symptom:** A new Gatekeeper/Kyverno policy is deployed directly in
  `Enforce` mode and immediately blocks a legitimate deployment,
  triggering an incident.
  **Fix:** Always deploy new policies in `Audit`/`dry-run` first, review
  what they would have blocked over a representative time window, then
  switch to enforcing with documented exceptions for anything legitimate
  the audit surfaced.

- **Symptom:** A Rego policy compiles and runs without error but never
  actually denies anything, even for input that should clearly violate
  it.
  **Fix:** Check the exact JSON path being matched against the real
  admission request/plan JSON (log or dump `input` and compare field
  names/nesting) — a common cause is a typo'd field path or an
  assumption about input structure that doesn't match what Gatekeeper or
  Conftest actually passes in.

- **Symptom:** The team believes "we have policy enforcement, so we're
  compliant," and treats it as equivalent to a full security review.
  **Fix:** Clarify explicitly what the policy checks (e.g. "runAsNonRoot
  is set") versus what it doesn't (image content, application logic,
  business risk) — policy as code automates checking for the presence of
  specific, narrowly-defined properties; it is not a substitute for
  broader review or for controls like
  [sast-integration](../sast-integration/SKILL.md) and
  [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md)
  that check different things entirely.

- **Symptom:** A policy is bypassed because a workload was applied
  directly to the cluster by an admin outside the normal CI/CD path,
  and the equivalent CI-time check never ran.
  **Fix:** This is expected if enforcement only exists in CI — add the
  same policy at the admission-controller layer (Gatekeeper/Kyverno) so
  it applies regardless of how the resource was created, not only to
  pipeline-originated changes.

- **Symptom:** Namespace-wide exceptions accumulate over time ("legacy",
  "migration", "temp-exception") and are never revisited, quietly
  hollowing out the policy's effectiveness.
  **Fix:** Require an expiry/review date and owner on every exception at
  creation time, and schedule periodic (e.g. quarterly) exception
  reviews to close out ones that are no longer needed.

## Worked example

A platform team codifies three baseline Kubernetes security requirements
as Kyverno policies, rolling them out audit-first, plus an OPA/Conftest
check blocking public S3 buckets in Terraform CI.

`policies/require-non-root.yaml` (rolled out in Audit, then Enforce after
a clean week):
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
        resources:
          kinds: [Pod]
      exclude:
        resources:
          namespaces: ["legacy-migration"]  # exception owner: platform-team, review: 2026-10-01
      validate:
        message: "Containers must set securityContext.runAsNonRoot: true"
        pattern:
          spec:
            securityContext:
              runAsNonRoot: true
```

`policies/s3-public-block.rego` (checked via Conftest in CI before
`terraform apply`):
```rego
package terraform.security

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket_acl"
  resource.change.after.acl == "public-read"
  msg := sprintf("%v must not set a public-read ACL", [resource.address])
}

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket_public_access_block"
  resource.change.after.block_public_acls == false
  msg := sprintf("%v must set block_public_acls = true", [resource.address])
}
```

`opa test` case verifying the policy actually fires on bad input:
```rego
package terraform.security

test_public_bucket_denied {
  results := deny with input as {
    "resource_changes": [{
      "type": "aws_s3_bucket_acl",
      "address": "aws_s3_bucket_acl.example",
      "change": {"after": {"acl": "public-read"}}
    }]
  }
  count(results) == 1
}
```
CI wiring:
```yaml
- name: Conftest policy check
  run: |
    terraform show -json plan.tfplan > plan.json
    conftest test plan.json --policy policies/
```
Result: a plan that would set a public-read ACL fails CI with `FAIL - main
- aws_s3_bucket_acl.example must not set a public-read ACL` before
`apply` ever runs, and a pod without `runAsNonRoot` is rejected by the
API server at creation time regardless of whether it came from CI or a
direct `kubectl apply`.

## Cross-references

- [secure-cicd-gates](../secure-cicd-gates/SKILL.md) — where IaC policy
  checks (Conftest/OPA) fit relative to SAST/SCA gates in the overall
  pipeline.
- [secrets-management](../secrets-management/SKILL.md) — a common
  policy-as-code target (e.g. "no plaintext secret fields in manifests")
  that this skill's enforcement mechanisms can codify.
- [container-image-hardening](../container-image-hardening/SKILL.md) —
  many of the properties enforced by admission policies (non-root,
  read-only filesystem, no privilege escalation) originate as
  image/container build practices this skill only verifies are present.
