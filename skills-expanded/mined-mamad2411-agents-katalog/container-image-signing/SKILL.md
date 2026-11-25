---
name: container-image-signing
description: >
  Sign and verify container images with Cosign and Sigstore: keyless OIDC, long-lived
  keys, and admission or policy enforcement by digest. Use when cosign sign/verify,
  Fulcio/Rekor, keyless OIDC image signing, Kyverno/Gatekeeper/policy-controller image
  checks, or OCI signature enforcement on deploy. Hand SBOM gates to sbom-ci-enforcement;
  git commit signatures to signed-commits-basics.
---

# Container Image Signing

## Scope And Authorization

- **In scope:** registries, CI, and clusters you own.
- **Out of scope:** signing malware images; bypassing others’ admission controls without authorization.
- Protect signing keys; prefer keyless OIDC where org allows.
- Deploy by **digest**, not mutable tags alone.
- Pair with supply-chain/SBOM skills and `code-quality-standards` for policy code.

## When To Use

- Implementing Cosign sign in CI and verify on admit/deploy.
- Migrating from optional verify to enforce.
- Tokens: cosign, Sigstore, Fulcio, Rekor, keyless, image digest, admission policy.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SBOM generate/CI gate | `sbom-ci-enforcement` (or catalog SBOM skill) |
| Git commit signing | signed-commits skill |
| Container escape testing | `container-escape-techniques` |
| Registry auth basics | registry/platform docs |

## Signing Modes

| Mode | Pros | Cons |
| --- | --- | --- |
| Keyless OIDC (Fulcio) | No long-lived key in CI if OIDC solid | Needs identity issuer trust policy |
| Cosign key pair | Offline/airgap friendly | Key custody hard |
| KMS-backed key | HSM/cloud KMS control | Setup cost |

## Workflow

### 1. Confirm scope and success

1. Registry, CI identity (GitHub Actions OIDC etc.), cluster admission stack.
2. Success: only signed digests run in prod; unsigned rejected; signatures verifiable.
3. Rollback: policy warn mode before deny.

### 2. Inventory images and deploy path

```bash
# Images currently deployed (example)
kubectl get pods -A -o jsonpath='{range .items[*]}{.spec.containers[*].image}{"\n"}{end}' | sort -u
```

1. Find who can push to prod repos.
2. Note tag mutability (`:latest` risk).

### 3. Sign in CI

```bash
# After build & push digest
cosign version
# Keyless example (CI with OIDC)
cosign sign --yes "$IMAGE@$DIGEST"
# Key pair example
cosign sign --key cosign.key "$IMAGE@$DIGEST"
```

1. Sign the **digest** reference.
2. Store key material in KMS/secret store if not keyless.
3. Optional: attach SBOM attestations (`cosign attest`) — coordinate SBOM skill.

### 4. Verify

```bash
cosign verify "$IMAGE@$DIGEST"
# With identity flags for keyless, e.g. certificate identity/reged issuer matching your CI
cosign verify --certificate-identity-regexp '...' --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' "$IMAGE@$DIGEST"
```

1. Negative test: unsigned image must fail verify.
2. Record trusted identities (repo workflow refs).

### 5. Enforce at admission

| Tool | Role |
| --- | --- |
| Kyverno / Gatekeeper / Sigstore policy-controller | Cluster admit verify |
| CI deploy job | Pre-check before kubectl |
| Registry replication rules | Optional defense in depth |

1. Start `audit/warn`, measure failures, then `enforce`.
2. Allowlist break-glass images with ticket + expiry only.

### 6. Operate

1. Rotate keys / update OIDC subject patterns when CI paths change.
2. Monitor admit denials.
3. Forbid `:latest` in prod manifests; pin digests.

### 7. Hand off

1. Document verify command and trusted identities.
2. Runbook: signature missing after rebuild; emergency unsigned path (highly controlled).
3. Link SBOM and vulnerability scan gates as separate controls.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Reference | Sign/verify digest | Sign only `:latest` |
| Trust | CI identity allowlist | Any signature from anywhere |
| Enforce | Gradual warn→deny | Instant deny without inventory |
| Keys | KMS/keyless | Cosign key in git |
| Deploy | Digest in manifests | Mutable tag trust |

## Output Checklist

- [ ] Image inventory and push paths mapped
- [ ] CI signing implemented on digests
- [ ] Verify works; unsigned fails
- [ ] Admission/policy enforce plan executed
- [ ] Trusted OIDC/key identities documented
- [ ] Prod manifests pin digests
- [ ] Break-glass exceptions ticketed
- [ ] Residual risks (mirror unsigned) noted

## Rules

- Owned registries/clusters only.
- Prefer digest + identity-bound keyless or KMS.
- Evidence: verify output + denied admit.
- Focus on **image signing/verification**; SBOM and git signing are siblings.
