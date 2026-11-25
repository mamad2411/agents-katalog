---
name: cosign-sign-verify-ci
description: >
  Sign and verify container images with Cosign in CI using keyless OIDC (Sigstore)
  and policy gates on owned registries. Use when wiring GitHub Actions/GitLab CI
  cosign sign after build, cosign verify before deploy, provenance/identity binding,
  or retiring long-lived registry signing keys from pipelines.
---

# Cosign Sign Verify CI

## Scope And Authorization

- **In scope:** CI/CD pipelines, registries, and deploy gates for projects you own.
- **Out of scope:** Signing malware or tampering with third-party images; disabling org signature policy without approval.
- Prefer keyless OIDC over long-lived cosign.key in CI secrets.
- Redact OIDC tokens and registry passwords in logs.
- Pair verify-time identity rules with `cosign-keyless-verify`; code quality with `code-quality-standards`.

## When To Use

- Adding cosign to release workflows after `docker build` / `buildah` / `ko` / `jib`.
- Enforcing verify on deploy jobs or GitOps controllers.
- Migrating from static cosign private keys in CI secrets to Fulcio keyless.
- Multi-arch images: sign indexes/manifest lists correctly.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Verify-only identity hardening | `cosign-keyless-verify` |
| GitHub OIDC → AWS roles | `github-actions-oidc-aws` |
| General supply-chain SBOM | SBOM skills |
| KMS long-term signing keys as primary | org KMS signing runbooks |
| Implementation quality baseline | `code-quality-standards` |

## Pipeline pattern

```text
build → push by digest → cosign sign (keyless) → (optional SBOM attest) → verify in deploy job → promote
```

| Stage | Requirement |
| --- | --- |
| Build | Produce immutable digest |
| Sign | OIDC token permission; ambient credentials |
| Store | Signature in registry (cosign default) or bundle artifact |
| Verify | Same identity/issuer constraints as prod admission |
| Deploy | Refuse on verify fail |

## Workflow

### 1. Confirm scope and success criteria

1. Registry, image name, CI provider, environments (sign in release only vs every PR — usually **not** every fork PR).
2. Success: main/release pipeline signs; deploy verifies; fork PRs cannot mint trusted prod signatures without isolation.

### 2. CI OIDC permissions (GitHub Actions example)

```yaml
# permissions needed for keyless sign
permissions:
  id-token: write   # OIDC for Fulcio
  contents: read
  packages: write   # if pushing to ghcr.io
```

Guard release jobs with `if: github.ref == 'refs/heads/main'` or environment protection rules. Never publish prod signatures from untrusted `pull_request` on forks without isolated trust design.

### 3. Build and push by digest

```bash
IMAGE=ghcr.io/ORG/APP
docker build -t "$IMAGE:${GIT_SHA}" .
docker push "$IMAGE:${GIT_SHA}"
DIGEST=$(crane digest "$IMAGE:${GIT_SHA}")
REF="${IMAGE}@${DIGEST}"
echo "REF=$REF" >> "$GITHUB_ENV"
```

### 4. Sign (keyless)

```bash
# Cosign uses ambient OIDC in Actions when id-token: write
cosign sign --yes "$REF"
# Optional annotations
cosign sign --yes -a "git_sha=${GIT_SHA}" -a "repo=${GITHUB_REPOSITORY}" "$REF"
```

Notes:

1. Pin cosign version (binary or container digest).
2. For private Sigstore, configure rekor/fulcio URLs per enterprise docs.
3. Multi-arch: sign the index digest your deploy references.

### 5. Verify in the same or downstream pipeline

```bash
cosign verify \
  --certificate-identity "https://github.com/${GITHUB_REPOSITORY}/.github/workflows/release.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  "$REF"
```

Deploy job must use the **digest** ref, not a floating tag alone.

### 6. Example GitHub Actions job sketch

```yaml
jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: sigstore/cosign-installer@v3
      - name: Build push sign
        run: |
          # build/push omitted; assume REF set to image@sha256:...
          cosign sign --yes "$REF"
          cosign verify \
            --certificate-identity "https://github.com/${{ github.repository }}/.github/workflows/release.yml@refs/heads/main" \
            --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
            "$REF"
```

Pin third-party actions by digest in high-assurance orgs.

### 7. Operate and harden

1. Remove `COSIGN_PRIVATE_KEY` / password secrets after keyless migration; revoke old keys.
2. Registry permissions: who can push signatures vs overwrite tags.
3. Alert on verify failures in deploy.
4. Document break-glass: re-sign from protected environment only.
5. Align admission controller identity with CI identity strings exactly.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Trust | Keyless + protected env | Cosign key in repo |
| Refs | Sign/verify digest | Sign `:latest` only |
| PR builds | No prod identity from forks | Sign on `pull_request_target` carelessly |
| Verify | Deploy gate required | Sign but never verify |
| Pins | Cosign + actions pinned | `@main` installers |

## Output Checklist

- [ ] Registry and image naming scheme set
- [ ] OIDC `id-token: write` (or CI equivalent) configured
- [ ] Build pushes digest; REF is digest-based
- [ ] `cosign sign` in trusted release path only
- [ ] `cosign verify` with identity/issuer in deploy path
- [ ] Negative path tested (unsigned digest blocked)
- [ ] Old static keys removed/rotated
- [ ] Admission/GitOps identity aligned
- [ ] Action/binary pins documented
- [ ] Break-glass runbook with expiry

## Rules

- Signing without verification provides little assurance.
- Protect the OIDC identity: environment rules, branch protection, CODEOWNERS on workflows.
- Authorized registries and pipelines only.
- This skill owns **CI sign+verify wiring**; deep verify policy lives in `cosign-keyless-verify`.
