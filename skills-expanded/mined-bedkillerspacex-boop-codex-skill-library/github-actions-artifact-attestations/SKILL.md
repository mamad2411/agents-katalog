---
name: github-actions-artifact-attestations
description: >
  GitHub Actions artifact attestations and provenance (SLSA-oriented): generate
  attestations for build artifacts, verify with gh attestation, consume in deploy
  gates, and relate to Sigstore/OIDC identities. Use for owned repositories and
  release pipelines — not to forge trust for third-party unsigned malware.
---

# GitHub Actions Artifact Attestations

## Scope And Authorization

- **In scope:** Repositories and org policies you administer; verifying artifacts you deploy.
- **Out of scope:** Faking attestations to trick others; bypassing corporate verification controls.
- Attestations prove **claims about how an artifact was built**, not that code is free of bugs.
- Prefer OIDC-backed signing over long-lived signing keys in secrets.
- Pair with container scanning (`gcr-vulnerability-scanning`) and `code-quality-standards`.

## When To Use

- Producing provenance for release binaries, SBOM attachments, or container images.
- Enforcing “deploy only attested digests from this workflow/repo.”
- Migrating from ad-hoc checksum files to `actions/attest-*` / `gh attestation`.
- Preparing SLSA-style evidence for auditors.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Reusable workflow structure | `github-actions-reusable-workflows` |
| OIDC to cloud deploy | `github-actions-oidc-aws` / `gcp-workload-identity-federation` |
| Image CVE scanning | `gcr-vulnerability-scanning` |
| Environment protection rules | `github-actions-environment-gates` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| Attestation | Signed statement bound to subject digests (in-toto / Sigstore ecosystem) |
| Provenance | Who built what from which source/workflow |
| Subject | Artifact digest (sha256) being attested |
| `id-token: write` | OIDC token permission for signing |
| `attestations: write` | Permission to create GH attestations |
| Verification | `gh attestation verify` against repo/org trust roots |
| SLSA | Levels of supply-chain guarantees; attestations support evidence |

## Workflow

### 1. Confirm goals

1. List artifact types (binary, wheel, image), consumers (deploy, clients), authorization.
2. Success: every prod artifact has attestation; verify step fails on tampered file.

### 2. Minimal build + attest job

```yaml
name: release
on:
  push:
    tags: ["v*"]

permissions:
  contents: read
  id-token: write
  attestations: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: |
          go build -o dist/app ./cmd/app
          sha256sum dist/app
      - name: Attest
        uses: actions/attest-build-provenance@v2
        with:
          subject-path: dist/app
      - uses: actions/upload-artifact@v4
        with:
          name: app-bin
          path: dist/app
```

For multiple subjects, pass paths/digests per action docs for your version.

### 3. Container images

```yaml
# After build-push to registry with digest output:
# uses: actions/attest-build-provenance@v2
# with:
#   subject-name: ghcr.io/ORG/IMAGE
#   subject-digest: sha256:${{ steps.push.outputs.digest }}
#   push-to-registry: true
```

Ensure registry auth and permissions allow attestation storage/association.

### 4. Verify locally or in deploy

```bash
gh attestation verify ./app \
  --owner ORG \
  --repo ORG/REPO

# Or by digest / bundle as supported by gh version
gh attestation verify oci://ghcr.io/ORG/IMAGE@sha256:DIGEST --owner ORG
```

Deploy gate sketch:

```bash
set -euo pipefail
gh attestation verify "$ARTIFACT" --repo "$EXPECTED_REPO"
# also: pin expected workflow identity if policy requires
```

### 5. Org policy and consumers

| Control | Guidance |
| --- | --- |
| Required workflow | Attest step mandatory on release tags |
| Deploy environments | Job verifies attestation before promote (`github-actions-environment-gates`) |
| Trust root | Only accept attestations from listed repos/workflows |
| SBOM | Attach SBOM attestation separately if using `attest-sbom` actions |

### 6. Failure modes

| Symptom | Check |
| --- | --- |
| Permission denied creating attestation | `attestations: write`, `id-token: write` |
| Verify fails after re-download | File corrupted / wrong artifact |
| Verify wrong repo | Artifact built elsewhere or supply-chain attack |
| OCI verify issues | Digest vs tag mismatch; registry attest storage |

### 7. Hand off

- Document verify command for operators.
- Store policy: which workflows are trusted.
- Combine with signing for distribution (Sigstore) where customers verify offline.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Identity | OIDC ephemeral | Long-lived GPG key in `secrets` for everything |
| Subjects | Digest-pinned | Attest mutable `latest` only |
| Deploy | Verify before apply | Upload attestation but never check |
| Scope | Least permissions on workflow | `permissions: write-all` |
| Claims | Treat as build provenance | “Attested ⇒ secure from CVE” |

## Output Checklist

- [ ] Artifact types and trust policy recorded
- [ ] Workflow permissions minimal and correct
- [ ] Provenance attestation generated on release
- [ ] `gh attestation verify` succeeds on clean artifact
- [ ] Tamper test fails verification
- [ ] Deploy path enforces verify
- [ ] Docs for operators published
- [ ] Related scanning/OIDC skills linked
- [ ] `code-quality-standards` applied to workflow YAML

## Rules

- Only for pipelines you control; do not forge trust materials.
- Attestation ≠ vulnerability-free.
- Pin actions by SHA for high-security orgs when policy requires.
- Least-privilege `permissions:` blocks.
- Focus on GH artifact attestations; cloud OIDC deploy is adjacent.
