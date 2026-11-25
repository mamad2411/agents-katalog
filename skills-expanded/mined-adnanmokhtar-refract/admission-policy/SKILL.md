---
name: admission-policy
description: Generates fail-closed Kubernetes admission policy for the cluster's engine (Kyverno / Sigstore policy-controller / Gatekeeper / native ValidatingAdmissionPolicy) — cosign image-signature verification, restricted Pod Security Standards, a provenance gate, and default-deny egress. Run when standing up a cluster's security baseline, or once `release-security` starts signing so the signatures are actually verified. Not a posture report — `k8s-audit` reports drift and `k8s-generate` sets defaults; this enforces at admission so neither can be bypassed.
kind: skill
pack: infrastructure
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: admission-policy

## Premise

Signing an image (devops `release-security`) means nothing until the cluster **refuses to run anything unsigned or CVE-failing**. Admission control is the enforcement point — a policy that runs at `kubectl apply` time and *rejects* a workload that violates it. The pack sets secure defaults *when it generates* a manifest (`k8s-generate`), but nothing stops a hand-written or third-party manifest that skips them. This skill generates the admission policy that makes the security posture non-bypassable — closing the "admission control is mentioned but never generated" gap and giving `release-security`'s `cosign sign` a verifier.

**Every generated policy cites what it enforces + the failure message a rejected workload gets.** Generate policy that fails closed; a policy in `Audit`/`warn` mode that never blocks is theater — default to `Enforce`.

## Adapt to the codebase

Detect the admission engine in use (or recommend one) and generate for it:

| Engine | Best for | Image-signature verification |
|---|---|---|
| **Kyverno** | most teams — YAML policies, good UX | `verifyImages` rule with `keyless` (cosign OIDC) |
| **Sigstore policy-controller** | signature-first shops | `ClusterImagePolicy` (native cosign/Fulcio/Rekor) |
| **OPA Gatekeeper** | Rego-standardized orgs | constraint templates (+ a verifier such as `ratify` for signatures) |
| **Native ValidatingAdmissionPolicy** | no extra controller wanted | CEL expressions — pod-security shape only; **image signatures still need a controller**, VAP cannot reach a registry |

Mirror the cluster's existing engine; only introduce one if none exists (recommend Kyverno). Native `ValidatingAdmissionPolicy` reached GA in Kubernetes 1.30, so it is available on every currently-supported minor (https://kubernetes.io/releases/) — confirm with `kubectl --context=<ctx> api-resources --api-group=admissionregistration.k8s.io` on a context the user confirmed in this session (or on the scratch cluster below) rather than assuming.

**Resolve the engine's own API shape before generating.** Policy-engine CRDs deprecate fields on their own schedule, independently of Kubernetes. `kubectl --context=<ctx> explain <kind>.<field>` against the installed engine (read-only, a context the user confirmed; or the scratch kind cluster with the engine installed at the cluster's pinned chart version) prints the DEPRECATED marker when there is one; a generated policy that sets a deprecated field still applies today and stops applying at the next engine upgrade. The current live example is `validationFailureAction` (below).

## Generates

### 1. Image-signature verification (the release-security counterpart)

Only images signed by the CI's OIDC identity admit — keyless, no key to distribute:

```yaml
# Kyverno
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: verify-image-signatures }
spec:
  rules:
    - name: check-cosign-signature
      match: { any: [{ resources: { kinds: [Pod] } }] }
      verifyImages:
        - imageReferences: ["<registry>/*"]
          attestors:
            - entries:
                - keyless:
                    issuer: "https://token.actions.githubusercontent.com"   # your CI OIDC issuer
                    subject: "https://github.com/<org>/<repo>/.github/workflows/*"
```
Optionally also require the SBOM / SLSA-provenance attestation (`attestations:`) that `release-security` produced.

**Enforce vs Audit is a PER-RULE field, not a spec-level one.** Kyverno's own API type marks the spec-level field deprecated — *"Deprecated, use validationFailureAction under the validate rule instead"* (https://raw.githubusercontent.com/kyverno/kyverno/main/api/kyverno/v1/spec_types.go) — so `spec.validationFailureAction` (and `spec.validationFailureActionOverrides`) belong to the removal path. Set it on the rule instead:

```yaml
  rules:
    - name: require-digest
      match: { any: [{ resources: { kinds: [Pod] } }] }
      validate:
        failureAction: Enforce         # per-rule; the spec-level field is deprecated
        message: "images must be referenced by digest, not a mutable tag"
        pattern: { spec: { containers: [{ image: "*@sha256:*" }] }}
```

Confirm the shape against the engine actually installed before generating — `kubectl explain clusterpolicy.spec.validationFailureAction` prints the deprecation marker on versions that carry it, and `kubectl explain clusterpolicy.spec.rules.validate.failureAction` confirms the replacement exists. Generating for the wrong one produces a policy that either fails schema validation or silently does not enforce.

### 2. Pod Security Standards (restricted) — enforced, not just defaulted

Reject `privileged`, `hostNetwork`/`hostPID`/`hostIPC`, `allowPrivilegeEscalation: true`, missing `runAsNonRoot`, un-dropped capabilities, writable root FS, and no `seccompProfile: RuntimeDefault`. Prefer the built-in **Pod Security Admission** label (`pod-security.kubernetes.io/enforce: restricted`) on the namespace + a Kyverno/VAP backstop for the specifics.

### 3. Supply-chain + provenance gate

Reject images by mutable tag (`:latest` / no digest); require the digest form so the signature binds. Optionally require the CVE-scan attestation to be present and passing.

### 4. Egress / network default-deny reference

Point at `k8s-generate`'s default-deny `NetworkPolicy` (blocks pod→metadata `169.254.169.254`) — the runtime belt to the code-level SSRF suspenders (`security/skills/ssrf-scan/SKILL.md`).

## Output

```
admission-policy — <cluster/namespace>   (engine: Kyverno)

Generated:
  policies/verify-image-signatures.yaml   Enforce — keyless cosign, issuer=<ci>, subject=<repo>
  policies/pod-security-restricted.yaml    Enforce — non-root, no-priv, drop-caps, RO-rootfs, seccomp
  policies/require-digest.yaml             Enforce — reject mutable :tag, require @sha256

Verify (scratch kind cluster, engine at the cluster's pinned version — never the user's cluster):
  KUBECONFIG="$SCAN/kind.kubeconfig" kubectl apply -f policies/
  KUBECONFIG="$SCAN/kind.kubeconfig" kubectl apply --dry-run=server -f unsigned-pod.yaml → REJECTED with the policy message
  offline cross-check: kyverno apply policies/ --resource unsigned-pod.yaml → fail
```

## False positives / gotchas

- **Roll out in `Audit` first, then flip to `Enforce`** — an Enforce policy on an existing cluster can block system workloads (kube-system, the ingress controller). Scope exclusions explicitly, then enforce.
- **Keyless subject/issuer must match your CI exactly** — a wrong `subject` regex fails every deploy (or, worse, an over-broad one verifies nothing). Pin to your repo's workflow identity.
- **Signature verify needs registry reachability + Rekor** — air-gapped clusters need a mirrored transparency log.
- **Pod Security Admission ≠ signature verification** — PSA covers the securityContext; images still need Kyverno/policy-controller. Use both.

## When to run

- When standing up a cluster's security baseline, or after devops `release-security` starts signing (so the signatures get verified).
- Alongside `k8s-generate` (which sets the defaults) + `k8s-audit` (which reports drift) — this is the *enforcement* layer between them.

## Halt conditions

- **Context halt (2026-10-10 rule).** Never rely on the default or current kube context. A read (`kubectl explain`, `api-resources`, `get` of the installed engine) names its context and runs with `--context=<ctx>` only after the user confirms that context in this session. Every dry-run and every policy apply for proof goes to a scratch kind cluster through an explicit `KUBECONFIG="$SCAN/kind.kubeconfig"` (or `--kubeconfig`) on the same command line, never to the user's cluster: `--dry-run=server` still sends the request to the API server and its admission webhooks (precedents § 56). Applying the generated policies to a real cluster is the user's step, through their pipeline.

- Halt on a generated policy left in `Audit`/`warn` when the intent is enforcement — say so explicitly and require the operator to opt into Audit.
- Halt on any policy field written from memory. Confirm each against the installed engine (`kubectl explain <kind>.<field>`); a deprecated field applies today and stops applying at the next engine upgrade, which is the worst possible failure shape for a control that fails closed.
- Do not generate a signature policy with a placeholder/over-broad `subject` — it must bind to the project's real CI identity or it verifies nothing.
- Do not claim "images verified" without a policy that actually rejects an unsigned image (the scratch-cluster dry-run proof in the output, with its kubeconfig named). No docker for kind → the proof is `blocked (no scratch cluster)` with the commands written out, and the claim stays Unconfirmed.

## Related

- `devops/skills/release-security/SKILL.md` — the producer (signs + attests); this is the verifier that enforces it. Together they close the sign→verify loop.
- `k8s-generate` — sets secure defaults on generated manifests; `k8s-audit` — reports posture drift; this **enforces** at admission so nothing bypasses.
- `security/agents/security-auditor.md` — A03 Supply-Chain + A02 Misconfiguration dispatch here for the admission-enforcement check.
- `security/skills/ssrf-scan/SKILL.md` — the code-level SSRF detector this pack's egress NetworkPolicy backstops.
