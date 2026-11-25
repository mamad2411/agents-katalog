---
name: follow-tool-packslip
description: publish signed release manifests (packslip) for artifacts — digests, platforms, bin paths installers can verify
argument-hint: "[scope]"
related:
  - follow-tool-mise
  - follow-tool-fnox
  - follow-tool-usage
  - setup-cicd
  - run-release
  - ship
---

## Goal

Publish `packslip.sigstore.json` beside release artifacts — a signed manifest (an in-toto statement in a sigstore bundle) that states digests, platform metadata, executable paths, and resource links so installers (e.g. mise) can pick/verify files without guessing filenames

## Scope

- Use when publishing release artifacts that installers (mise/others) should pick and verify — GitHub Actions has `jdx/packslip@v1`; publishers outside CI use an Ed25519 key
- Spec stable at `release/v1` — predicateType `https://packslip.dev/release/v1`
- Docs: https://packslip.dev/ · Spec: https://packslip.dev/release/v1/ · CLI: https://packslip.dev/cli/

## Execute

### 1. Publish From GitHub

> Goal: the release workflow produces a signed manifest

1. After building artifacts + creating the release, add a step:

```yaml
- uses: jdx/packslip@v1
  with:
    artifacts: dist/*.tar.xz dist/*.zip
    bin: mytool
    resources: |
      man=archive:share/man/man1/mytool.1
```

2. Grant the workflow the needed permissions (id-token for sigstore signing with the workflow identity)
3. The `packslip.sigstore.json` manifest is published beside the artifacts automatically

### 2. Describe Artifacts

> Goal: complete metadata for installers

1. `subject` — the digest (sha256) of each file
2. `predicate.artifacts[]` — `name`, `url`, `format` (tar.gz/zip), `bin` (executable paths), platform fields (`os`/`arch`/`libc`)
3. `resources` — man pages, completions, CLI specs (usage), agent skills, SBOMs, desktop files
4. `host requirements` — libraries/commands the runtime needs

### 3. Verify / Consume

> Goal: the consumer verifies before installing

1. Verify the manifest against a trusted identity/key, then check the digest of the downloaded file
2. Signed release lists (`/docs/release-lists/`) — expiry, sequence, withdrawals, recommended version
3. Example consumer: mise reads packslip to pick the platform artifact — see https://packslip.dev/docs/mise/

## Rules

- Build provenance is separate evidence — always verify it separately from the manifest
- A single manifest can't detect withdrawn/rollback releases — use signed release lists
- A plain checksum beside the binary is not equivalent — signer verification is required
- The spec version stays at v1 — pin `jdx/packslip@v1`

## Expected Outcome

- The release workflow produces `packslip.sigstore.json` beside every artifact
- Installers/consumers (e.g. mise) can pick and verify files from the manifest
