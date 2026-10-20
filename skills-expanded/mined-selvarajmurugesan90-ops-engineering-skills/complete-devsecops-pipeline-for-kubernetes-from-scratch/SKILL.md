---
name: complete-devsecops-pipeline-for-kubernetes-from-scratch
description: >
  Builds the complete security-gate sequence for a Kubernetes-targeted
  DevSecOps pipeline from scratch — SAST, SCA, container image scanning,
  a policy-as-code (OPA/Kyverno) admission gate placed before the GitOps
  handoff, and a secrets model where plaintext credentials never touch the
  pipeline because an External Secrets Operator pulls them cluster-side
  instead. Use when the user asks to "build a DevSecOps pipeline for
  Kubernetes from scratch," "add a policy gate before our GitOps commit,"
  "make sure secrets never touch CI for our K8s deploys," or "sequence
  SAST/SCA/image-scan/policy gates for a container pipeline end-to-end."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# Complete DevSecOps Pipeline Deployment for Kubernetes, From Scratch

## Purpose

A Kubernetes-targeted DevSecOps pipeline has a gate sequence with two
properties the serverless and VM variants of this skill don't share: a
**policy-as-code admission gate** (OPA/Kyverno) sits between the built
artifact and the GitOps handoff, checking the *manifests* themselves
(non-root, resource limits, approved registries, required labels) rather
than only the image contents — and **secrets never need to be present in
the pipeline at all**, because an External Secrets Operator running
in-cluster pulls them directly from a vault at deploy time, decoupled
entirely from CI. This is a materially different secrets model from
serverless (a managed secrets service the function's execution role reads
at invoke time) and VM-based (config-management-applied secrets baked in
at config-push time). This skill sequences SAST → SCA → image scan →
policy gate → GitOps handoff into one coherent walkthrough; each gate's
own mechanics are covered in depth by the linked skills.

## When to use

- A Kubernetes-targeted pipeline has individual security tools bolted on
  ad hoc, and the user wants the full gate sequence — including the
  policy-as-code admission check and the secrets-never-touch-CI model —
  designed coherently from scratch.
- The user is building a new containerized service's pipeline and wants
  security gates designed in from the start rather than retrofitted.
- The user wants to understand exactly where a Kubernetes-specific policy
  gate (OPA/Kyverno) fits relative to the GitOps handoff, and why
  Kubernetes's primary "last line of defense" gate is admission policy
  rather than IAM role scoping (the serverless variant's equivalent) or
  golden-image hardening (the VM variant's equivalent).
- Diagnosing why a hardened container image (per
  [container-image-hardening](../container-image-hardening/SKILL.md)) is
  still being deployed with `runAsUser: 0` or no resource limits in
  practice.

## Prerequisites & environment

- A working CI/CD pipeline that already builds and pushes a container
  image and hands off to GitOps — see
  [complete-cicd-pipeline-deployment-for-kubernetes-from-scratch](../../../cicd-tooling/skills/complete-cicd-pipeline-deployment-for-kubernetes-from-scratch/SKILL.md)
  for that base pipeline; this skill adds the security-gate layer onto it,
  not the build/deploy mechanics themselves.
- SAST, SCA, and container-scanning tools chosen per
  [sast-integration](../sast-integration/SKILL.md),
  [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md),
  and
  [container-image-hardening](../container-image-hardening/SKILL.md).
- An admission-policy engine installed in the target cluster — OPA
  Gatekeeper or Kyverno — per
  [policy-as-code-guardrails](../policy-as-code-guardrails/SKILL.md),
  [kyverno-policy-management](../../../policy-and-governance-tooling/skills/kyverno-policy-management/SKILL.md),
  or
  [opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md).
- External Secrets Operator (or an equivalent) installed in-cluster,
  configured against a backing vault (HashiCorp Vault, AWS Secrets
  Manager, Azure Key Vault) per
  [sealed-secrets-and-external-secrets-operator](../../../security-scanning-tooling/skills/sealed-secrets-and-external-secrets-operator/SKILL.md)
  and
  [secrets-management](../secrets-management/SKILL.md).
- A GitOps operator (Argo CD/Flux) already reconciling the target cluster
  — see the relevant `complete-gitops-argocd-deployment-on-*-from-scratch`
  skill if not yet set up.

## Step-by-step guidance

### Phase 1 — SAST on the diff (PR-time)

Per [sast-integration](../sast-integration/SKILL.md): diff-aware scanning,
blocking on new critical/high findings only, wired as a required PR
status check.

### Phase 2 — SCA on the dependency tree (PR-time)

Per [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md):
scan the lockfile, not just the manifest, blocking on fixed
critical/high findings.

### Phase 3 — Container image scan (post-build, on the actual digest)

Per [container-image-hardening](../container-image-hardening/SKILL.md)
and [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md)'s
image-scanning step, run Trivy against the *built* image, not just the
filesystem:
```yaml
  image-scan:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - run: trivy image --severity CRITICAL,HIGH --exit-code 1 ghcr.io/example/payments-api:${{ github.sha }}
```
This catches base-image OS-package CVEs the filesystem-level SCA scan in
Phase 2 can't see, since the base image's own layers aren't present until
the image is actually built.

### Phase 4 — Policy-as-code admission gate, before the GitOps handoff

This is the Kubernetes-specific gate with no direct equivalent in the
serverless or VM variants: check the **rendered Kubernetes manifests**
(not just the image) against an OPA/Conftest or Kyverno policy set in CI,
*before* they're committed to the GitOps config repo — catching a
violation (missing resource limits, `runAsUser: 0`, an unapproved
registry) at PR time on the manifests repo, in addition to the same
policy being enforced as a live admission webhook in-cluster:
```yaml
  manifest-policy-gate:
    needs: image-scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: kustomize build apps/payments-api/overlays/prod > rendered.yaml
      - run: conftest test rendered.yaml --policy policies/
```
```rego
# policies/no_root.rego
package main

deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.securityContext.runAsNonRoot
  msg := sprintf("container %s must set runAsNonRoot", [container.name])
}
```
The **same** policy set is also enforced live in-cluster via Kyverno/OPA
Gatekeeper admission control (per
[kyverno-policy-management](../../../policy-and-governance-tooling/skills/kyverno-policy-management/SKILL.md)/
[opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md))
— the CI check catches the violation early and cheaply on a PR; the
admission webhook is what actually guarantees it holds even if a manifest
somehow reaches the cluster through a path other than this pipeline (a
manual `kubectl apply`, a different pipeline). Neither one alone is
sufficient; see
[policy-as-code-guardrails](../policy-as-code-guardrails/SKILL.md) for
what each layer actually guarantees.

### Phase 5 — GitOps handoff (unchanged from the base CI/CD pipeline)

Only after Phase 4 passes does the pipeline commit the new image tag to
the manifests repo, per
[complete-cicd-pipeline-deployment-for-kubernetes-from-scratch](../../../cicd-tooling/skills/complete-cicd-pipeline-deployment-for-kubernetes-from-scratch/SKILL.md).

### Phase 6 — Secrets: never present in the pipeline at all

This is the Kubernetes-specific secrets model: the application's runtime
secrets (DB credentials, API keys) are **not** referenced anywhere in this
CI pipeline — not as CI secrets injected into a manifest, not baked into
the image. Instead, an `ExternalSecret` resource committed to the same
GitOps config repo declares *what* secret to sync and *where from*; the
in-cluster External Secrets Operator does the actual fetch from the vault
at reconcile time:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: payments-api-db-creds
  namespace: payments-prod
spec:
  secretStoreRef: { name: vault-backend, kind: ClusterSecretStore }
  target: { name: payments-api-db-creds }
  data:
    - secretKey: password
      remoteRef: { key: payments-api/prod/db, property: password }
```
CI's only involvement with this resource is committing it (a reference,
containing no secret value) to the manifests repo alongside the image-tag
bump in Phase 5 — the actual secret material never passes through a CI
runner, a build log, or an environment variable at any point.

### Phase 7 — Verify the full gate sequence and secrets model

```bash
kubectl get externalsecret payments-api-db-creds -n payments-prod -o jsonpath='{.status.conditions}'
kubectl get events -n payments-prod --field-selector reason=PolicyViolation
argocd app get payments-api-prod
```
Confirm the `ExternalSecret` shows a synced condition and that no
admission-policy violation events exist for the namespace, in addition to
the GitOps operator reporting `Synced`/`Healthy`.

## Best practices

- Enforce the same policy set in both CI (Phase 4, fast PR-time feedback)
  and cluster-side admission (a live webhook) — CI catches it cheaply;
  admission control is what actually guarantees the property holds
  regardless of how a manifest reaches the cluster.
- Never let the pipeline's own service account read the vault directly
  "to make it simpler" — the entire benefit of the External Secrets
  Operator model is that CI's compromise blast radius excludes runtime
  secrets entirely; keep that boundary intact even under deadline
  pressure.
- Order gates by cost: SAST/SCA (Phase 1/2, fast) before the image build,
  image scan (Phase 3) after build, policy gate (Phase 4) on the rendered
  manifests right before the GitOps commit — a policy violation caught
  after an expensive image build/push is still cheaper to fix than one
  caught only by admission rejection after the GitOps operator already
  tried to sync it.
- Start new policy rules in Kyverno/Gatekeeper's audit/report mode before
  flipping to enforcing/blocking, per
  [policy-as-code-guardrails](../policy-as-code-guardrails/SKILL.md) — the
  same audit-then-enforce rollout discipline applies to the CI-side
  `conftest` check.
- Keep the CI-side policy check and the in-cluster admission policy
  defined from the **same** source files (one `policies/` directory
  referenced by both the CI job and the Kyverno/Gatekeeper ConstraintTemplate
  sync), not two independently maintained copies that can drift apart.

## Common pitfalls

- **Symptom:** A manifest passes the CI policy gate (Phase 4) but is
  rejected by the in-cluster admission webhook when Argo CD tries to sync
  it, and the `Application` shows a confusing `SyncFailed` error.
  **Fix:** The CI-side `conftest` policies and the cluster's live
  Kyverno/Gatekeeper constraints have drifted apart (different rule
  versions, one updated without the other) — keep both driven from the
  same policy source, and treat this failure as a signal to reconcile
  them, not just a one-off manifest fix.

- **Symptom:** A team under deadline pressure adds the vault token
  directly as a CI secret "just to unblock this one deploy," bypassing the
  External Secrets Operator model entirely.
  **Fix:** This defeats the entire secrets-never-touch-CI design — any
  vault credential granted to CI reintroduces exactly the blast-radius
  risk the External Secrets Operator model exists to avoid. Fix the actual
  blocker (an `ExternalSecret` misconfiguration, a missing
  `ClusterSecretStore` binding) instead of routing around it with a
  pipeline-held credential, and treat any CI-held vault token as a finding
  to remove.

- **Symptom:** The image scan (Phase 3) passes clean, but a container
  later runs as root in production despite
  [container-image-hardening](../container-image-hardening/SKILL.md)'s
  Dockerfile setting `USER app`.
  **Fix:** A clean image scan says nothing about the *pod spec* deploying
  it — a Helm chart default or a manual override can set `runAsUser: 0` at
  the Kubernetes layer regardless of the image's own `USER` instruction.
  This is exactly what the Phase 4 policy gate (both CI-side and
  admission-side) exists to catch; if it's not catching this, the
  `runAsNonRoot` rule either isn't enabled or isn't enforcing yet.

- **Symptom:** The `ExternalSecret` shows `SecretSynced: True` in
  `kubectl describe`, but the application pod still fails to start,
  citing a missing environment variable.
  **Fix:** Confirm the `ExternalSecret`'s `target.name` actually matches
  what the Deployment's `envFrom`/`secretKeyRef` references — a
  successfully-synced secret under the wrong name looks identical to a
  missing one from the pod's perspective; this is a wiring mismatch
  between the GitOps-committed `ExternalSecret` and Deployment manifests,
  not an External Secrets Operator failure.

## Worked example

**Scenario:** `payments-api` gets its full DevSecOps gate sequence added:
SAST/SCA at PR time, an image scan post-build, an OPA policy gate on the
rendered prod overlay before the GitOps commit, and its database
credential delivered via External Secrets Operator instead of a CI secret.

```yaml
jobs:
  sast: { /* per sast-integration */ }
  sca: { /* per software-composition-analysis-sca */ }
  build-and-push: { needs: [sast, sca] /* per container-build-and-release */ }

  image-scan:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - run: trivy image --severity CRITICAL,HIGH --exit-code 1 ghcr.io/example/payments-api:${{ github.sha }}

  manifest-policy-gate:
    needs: image-scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: kustomize build apps/payments-api/overlays/prod > rendered.yaml
      - run: conftest test rendered.yaml --policy policies/

  update-manifests:
    needs: manifest-policy-gate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: |
          cd apps/payments-api/overlays/prod
          kustomize edit set image payments-api=ghcr.io/example/payments-api:${{ github.sha }}
          git commit -am "bump to ${{ github.sha }}" && git push
```
`apps/payments-api/overlays/prod` also carries the `ExternalSecret` from
Phase 6, committed once (not on every deploy) — Argo CD reconciles both
the Deployment's new image tag and the (unchanged) `ExternalSecret`
reference on each sync, while the External Secrets Operator's own
in-cluster reconcile loop independently keeps `payments-api-db-creds`
fresh from Vault, entirely outside this pipeline's reach.

## Cross-references

- [complete-cicd-pipeline-deployment-for-kubernetes-from-scratch](../../../cicd-tooling/skills/complete-cicd-pipeline-deployment-for-kubernetes-from-scratch/SKILL.md) — the base build/GitOps-handoff pipeline this skill adds security gates onto.
- [sast-integration](../sast-integration/SKILL.md), [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md), [container-image-hardening](../container-image-hardening/SKILL.md) — Phase 1-3 gate mechanics.
- [policy-as-code-guardrails](../policy-as-code-guardrails/SKILL.md), [kyverno-policy-management](../../../policy-and-governance-tooling/skills/kyverno-policy-management/SKILL.md), [opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md) — Phase 4's policy engine mechanics.
- [sealed-secrets-and-external-secrets-operator](../../../security-scanning-tooling/skills/sealed-secrets-and-external-secrets-operator/SKILL.md) and [secrets-management](../secrets-management/SKILL.md) — Phase 6's secrets model.
- [secure-cicd-gates](../secure-cicd-gates/SKILL.md) — the orchestration principles (severity thresholds, blocking vs. warn) this gate sequence follows.
- [complete-devsecops-pipeline-for-serverless-from-scratch](../complete-devsecops-pipeline-for-serverless-from-scratch/SKILL.md) and [complete-devsecops-pipeline-for-vm-based-workloads-from-scratch](../complete-devsecops-pipeline-for-vm-based-workloads-from-scratch/SKILL.md) — the same gate-sequencing goal with fundamentally different primary gates and secrets models.
