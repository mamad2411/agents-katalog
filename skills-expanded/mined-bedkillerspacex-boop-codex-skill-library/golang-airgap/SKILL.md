---
name: golang-airgap
description: >
  Build, vendor, and deploy Go modules and toolchains in air-gapped environments:
  module proxies, zip mirrors, hermetic builds, and verification. Use for owned
  air-gapped networks under authorization.
---

# Golang Airgap

## Research grounding

Runbook for **air-gapped Go development and delivery**: no direct Internet from
build/run networks; controlled promotion of modules, toolchains, and container
images. Skill id: `golang-airgap`.

## Scope And Authorization

- **In scope:** owned air-gapped labs/prod and the connected staging used to stage artifacts.
- **Out of scope:** bypassing someone else’s network controls without authorization.
- Document transfer paths (diode, sneakernet, approved proxy).
- Redact internal registry URLs only if classified; never embed credentials.
- Pair with `code-quality-standards`.

## When To Use

- `GOPROXY=off` / no sumdb reachability in secure networks.
- Creating an internal module proxy or vendored release bundles for Go.
- Hermetic CI for Go inside the gap.
- Focus tokens: **golang, airgap**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Air-gapped **backups** specifically | `golang-airgap-backup` |
| Container signing / attestations | `golang-attestations` |
| General secrets hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Toolchain | Copy official Go tarball + checksum; verify signature/hash before install |
| Modules | `GOPROXY=file:///...` or Athens/Goproxy binary cache; `GOSUMDB=off` only if sums mirrored |
| Vendor | `go mod vendor` for app builds; commit or ship vendor tarball per policy |
| Sums | Mirror sumdb or use `GONOSUMDB` carefully for private modules only |
| Images | Internal registry mirror; cosign verify inside gap if policy requires |
| Transfer | Manifest of versions + sha256; write-once media or one-way diode |
| Pitfalls | Building with laptop module cache polluted; unchecked `GOSUMDB=off` |

## Workflow

### 1. Confirm scope and success criteria

1. Gap boundary diagram, transfer approval process, owners, authorization.
2. Success: clean build with network denied; versions pinned; hashes recorded.
3. Rollback: previous toolchain + module bundle retained.

### 2. Inventory

1. Go version(s), base images, private modules, CGO deps (lib versions).
2. CI runners’ egress rules; existing proxies.
3. License constraints for redistributing modules.

### 3. Baseline (connected side)

1. From a clean machine: `go mod download` / `go mod vendor` at locked versions.
2. Record `go.mod`, `go.sum`, and `go version`.
3. Export module cache or proxy snapshot.

### 4. Stage artifacts into the gap

```bash
# Connected staging (authorized)
go version
go env GOPATH GOMODCACHE
go mod download
go mod verify
go mod vendor

# Pack reproducible bundle
tar -czf go-mod-bundle.tgz "$(go env GOMODCACHE)" go.mod go.sum vendor
sha256sum go-mod-bundle.tgz go*.tar.gz > SHA256SUMS

# Inside airgap after transfer
export GOPROXY=file:///media/airgap/modcache
export GOSUMDB=off   # only if you verified sums on connected side and policy allows
go build -mod=readonly ./...
# or
go build -mod=vendor ./...
```

1. Install Go from verified tarball (compare SHA256 to published).
2. Prefer internal Athens/proxy serving only approved modules.
3. For private VCS: pre-export git bundles or use `replace` + vendor.

### 5. Verify with evidence

```bash
# Network should fail (prove hermeticity)
# curl https://proxy.golang.org || true

go test ./... -count=1
go vet ./...
go mod verify
# staticcheck/govulncheck: run on connected side on the same go.sum if gap cannot update DB
```

1. Build twice → identical binary hashes if reproducible flags used (`-trimpath`, ldflags).
2. Document any `GOSUMDB=off` residual risk.
3. Keep transfer ticket IDs with SHA256SUMS.

### 6. Observe and harden

1. Process for vulnerability refresh: rebuild bundle on connected side with `govulncheck`.
2. Age-out old module caches; prevent unapproved module adds without review.
3. Monitor for accidental egress enablement on runners.

### 7. Hand off

1. Runbook: how to bump Go version and modules through the gap.
2. Owners for proxy and transfer.
3. Apply `code-quality-standards` to build scripts.

## Env reference

| Variable | Airgap note |
| --- | --- |
| `GOPROXY` | Internal URL or `file://` |
| `GOSUMDB` | Mirror or justified off + external verify |
| `GOPRIVATE` | Private prefixes |
| `GOFLAGS` | `-mod=readonly` in CI |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Integrity | SHA256 + go.sum verify | USB copy with no hashes |
| Builds | `-mod=vendor` or readonly proxy | `go get` latest inside gap via hidden proxy |
| Toolchain | Pinned Go version | Random laptop Go |
| Vulns | Connected govulncheck on same sum | Never refresh modules |
| Topic fidelity | Module/toolchain airgap | Generic go test only |

## Output Checklist

- [ ] Gap boundary and transfer path documented
- [ ] Go toolchain verified and pinned
- [ ] Module proxy or vendor bundle created with hashes
- [ ] Hermetic build proven (no required egress)
- [ ] go.mod/go.sum policy clear
- [ ] Vuln refresh process defined
- [ ] `code-quality-standards` applied to automation

## Rules

- Authorized networks only; do not smuggle unapproved code.
- Prefer verified sums over permanent `GOSUMDB=off`.
- Focus on `golang-airgap`; backups → `golang-airgap-backup`.
- Never embed registry passwords in scripts committed to git.
