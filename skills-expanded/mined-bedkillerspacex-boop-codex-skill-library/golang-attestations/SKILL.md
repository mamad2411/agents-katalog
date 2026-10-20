---
name: golang-attestations
description: >
  Produce and verify build attestations for Go artifacts: SLSA provenance,
  cosign/sigstore signatures, SBOM attach, and admission verify. Use for owned
  supply chains under authorization.
---

# Golang Attestations

## Research grounding

Runbook for **signed attestations and provenance** of Go binaries and container
images—who built what from which commit. Skill id: `golang-attestations`.

## Scope And Authorization

- **In scope:** pipelines and registries you own.
- **Out of scope:** signing malware or spoofing others’ identity.
- Protect signing keys / OIDC identity; prefer keyless where appropriate.
- Pair with `golang-aqua-notes`, `golang-admission`, `code-quality-standards`.

## When To Use

- Requiring provenance before deploy of Go services.
- Implementing cosign sign/verify or GitHub artifact attestations.
- Attaching SBOM (CycloneDX/SPDX) to Go image digests.
- Focus tokens: **golang, attestations**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic container CVE gate | `golang-aqua-notes` |
| Module airgap | `golang-airgap` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Artifact | Attestation |
| --- | --- |
| Go binary | Provenance predicate + signature |
| Container image | cosign signature + SBOM attach |
| Source | Review requirements in SLSA levels |
| Verify | CI, admission controller, deploy job |
| Identity | OIDC to sigstore; or KMS keys |
| Pitfalls | Signing `latest` mutable tags; verify not enforced |

## Workflow

### 1. Confirm scope and success criteria

1. Artifacts in scope, SLSA target level, authorization.
2. Success: every prod digest signed; verify fails on unsigned; provenance has git sha.
3. Key custody or OIDC issuer allowlist.

### 2. Inventory

1. Build systems (GHA, GitLab, internal).
2. Registries and deploy paths.
3. Existing signatures (if any).

### 3. Baseline

1. Pick one Go service pilot.
2. Record image digest of last release.

### 4. Implement

```bash
# Build reproducible-ish Go binary
CGO_ENABLED=0 go build -trimpath -ldflags="-s -w -X main.sha=$GIT_SHA" -o dist/app ./cmd/app
go test ./... -count=1
govulncheck ./...

# SBOM example
# syft dir:. -o cyclonedx-json > sbom.json

# Sign image (illustrative cosign keyless)
# cosign sign registry.example/app@$DIGEST
# cosign attest --predicate provenance.json --type slsaprovenance registry.example/app@$DIGEST
# cosign verify registry.example/app@$DIGEST
```

1. Provenance must include: builder id, source repo, commit, materials (go.sum hash).
2. Prefer digest references in deploy manifests, not tags alone.
3. Admission/policy: deny unsigned in prod (`golang-admission` or policy engine).
4. Document key rotation / OIDC identity change procedure.

### 5. Verify with evidence

1. Tamper binary/image → verify fails.
2. Unsigned digest → deploy blocked.
3. Provenance commit matches git release tag.
4. Redact private key material from logs.

### 6. Observe and harden

1. Metrics: % prod images verified; verify failures.
2. Alert on deploy of unsigned (should be impossible—alert if bypass).
3. Raise SLSA level when builder hardening allows.

### 7. Hand off

1. Runbook for verify break-glass (dual control).
2. Developer docs: how local builds differ from release trust.
3. Link scanner gates separately from signatures (both needed).

## SLSA-oriented checklist

| Level idea | Control |
| --- | --- |
| Docs | Build script recorded |
| Hosted | Ephemeral builder, provenance |
| Hardened | Non-falsifiable provenance, isolation |
| Verify | Automated policy at deploy |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Ref | Digest pin | Tag only `latest` |
| Sign | OIDC/KMS | Shared password for cosign key |
| Enforce | Admission verify | Sign but never verify |
| Go build | trimpath + module pin | `go get` on prod host |
| Topic fidelity | Attestations for Go artifacts | Generic go test only |

## Output Checklist

- [ ] Artifact scope and trust root defined
- [ ] Sign/attest in release CI
- [ ] Verify enforced on prod deploy
- [ ] SBOM attached or stored
- [ ] Tamper test evidence
- [ ] Break-glass dual control
- [ ] `code-quality-standards` applied

## Rules

- Protect signing identity; authorized pipelines only.
- Focus on `golang-attestations`.
- Never commit private signing keys.
- Signature ≠ absence of vulns—still scan.
