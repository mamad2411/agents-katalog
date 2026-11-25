---
name: cosign-keyless-verify
description: >
  Verify Cosign keyless (Sigstore Fulcio/Rekor) signatures on container images and
  artifacts with tight certificate identity and OIDC issuer allowlists. Use for
  cosign verify, --certificate-identity / --certificate-identity-regexp,
  --certificate-oidc-issuer, Rekor checks, signed digests in admission or CI, or
  offline bundle verify — not long-lived PEM key signing as the primary mode.
---

# Cosign Keyless Verify

## Scope And Authorization

- **In scope:** Verifying signatures on images/artifacts for registries and repos you own or are authorized to enforce policy on.
- **Out of scope:** Bypassing signature gates on production clusters without change control; forging identities against public Sigstore for abuse.
- Prefer digest references (`@sha256:…`) over mutable tags.
- Redact registry credentials; identity emails/repos in logs may still be sensitive — follow org policy.
- Pair CI wiring with `cosign-sign-verify-ci` and `code-quality-standards`.

## When To Use

- Enforcing keyless Sigstore verification in CI, GitOps, or admission (Kyverno/Gatekeeper/Connaisseur/Ratify).
- Tightening overly broad `--certificate-identity-regexp` (e.g. any GitHub Actions).
- Offline/air-gapped verify with bundles attached to the image.
- Investigating “signature present but wrong identity” failures.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| CI sign + verify pipeline end-to-end | `cosign-sign-verify-ci` |
| Long-lived cosign key pairs / KMS keys | container-image-signing or org KMS signing skill |
| SBOM generation only | SBOM skills |
| Cluster admission policy authoring broadly | policy engine skill |
| Implementation quality baseline | `code-quality-standards` |

## Keyless model (topic map)

| Component | Role |
| --- | --- |
| OIDC token (CI/user) | Proves identity to Fulcio |
| Fulcio | Issues short-lived code-signing cert |
| Cosign | Signs image digest; records to Rekor (default) |
| Rekor | Transparency log entry |
| Verifier | Checks sig + cert + identity/issuer + (optional) Rekor |

Verification without identity constraints is **insufficient** — any Fulcio-issued cert that signed the digest would pass.

## Workflow

### 1. Confirm scope and success criteria

1. Image refs (registry/repo), expected OIDC issuer (e.g. `https://token.actions.githubusercontent.com`), expected identity (workflow ref, `subject` SAN pattern).
2. Success: only images signed by that identity verify; others fail closed; digests pinned in deploy manifests.

### 2. Inventory how images are signed today

```bash
cosign version
# Discover signatures (registry must be reachable)
cosign tree ghcr.io/ORG/APP:TAG
# Or inspect digest
crane digest ghcr.io/ORG/APP:TAG
```

Collect sample good image digest and a known-unsigned or wrong-identity image for negative tests.

### 3. Baseline verify (tight claims)

```bash
IMAGE='ghcr.io/ORG/APP@sha256:DIGEST'

# Exact identity (example: GitHub Actions workflow)
cosign verify \
  --certificate-identity 'https://github.com/ORG/REPO/.github/workflows/release.yml@refs/heads/main' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  "$IMAGE"

# Or regexp when multiple workflows are intentional (keep tight)
cosign verify \
  --certificate-identity-regexp '^https://github.com/ORG/REPO/\.github/workflows/release\.yml@refs/heads/main$' \
  --certificate-oidc-issuer-regexp '^https://token\.actions\.githubusercontent\.com$' \
  "$IMAGE"
```

Optional:

```bash
# Require transparency log presence (default behavior varies by version/flags — pin cosign version)
cosign verify ... "$IMAGE"
# Offline / bundle (when sigs attached as bundle)
cosign verify --offline --bundle path/to/bundle.json "$IMAGE"
```

### 4. Negative tests (must fail)

```bash
# Wrong issuer or identity must non-zero exit
cosign verify \
  --certificate-identity 'https://github.com/EVIL/REPO/.github/workflows/x.yml@refs/heads/main' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  "$IMAGE" && echo 'UNEXPECTED PASS' || echo 'fail closed OK'
```

### 5. Wire policy (admission / CI)

1. CI gate: verify before deploy job promotes digest.
2. Cluster: policy engine verifies digest on admit; block tags without digest when possible.
3. Store expected identity/issuer in config reviewed by security; avoid `.*` regex.
4. Prefer repository + workflow + ref binding for GitHub Actions subject.

### 6. Private Sigstore / air-gap notes

1. Enterprise may run private Fulcio/Rekor — point cosign via env (`SIGSTORE_*`) or flags per your distribution docs.
2. Offline verify needs bundles and trusted roots distributed out-of-band — document trust root updates.
3. Do not disable Rekor checks in production without compensating controls and written exception.

### 7. Hand off

1. Signing side pipeline → `cosign-sign-verify-ci`.
2. Document break-glass unsigned rollback (time-limited).
3. Monitor verify failures as potential supply-chain or mis-sign events.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Identity | Workflow + ref exact or tight regexp | `.*github.com.*` |
| Image ref | Digest | `:latest` only |
| Trust | Pinned cosign version + trusted root process | Random cosign from unpinned action |
| Negative test | Wrong identity fails CI | Only happy-path verify |
| Exceptions | Ticketed unsigned break-glass | Permanent `--insecure` |

## Output Checklist

- [ ] Digests and registry scope recorded
- [ ] Expected OIDC issuer + identity documented
- [ ] `cosign verify` success on golden image
- [ ] Negative verify fails
- [ ] CI and/or admission enforcement path defined
- [ ] Regexes reviewed for overbreadth
- [ ] Offline/private Sigstore needs documented if any
- [ ] Break-glass process with expiry
- [ ] Cosign version pinned
- [ ] Residual risks (tag mutability, registry auth) noted

## Rules

- Fail closed: missing or wrong identity is a deploy blocker unless break-glass.
- Keyless verify without identity allowlists is theater.
- Authorized registries and clusters only.
- Keep focus on **verification** of keyless signatures; signing pipeline is the sibling skill.
