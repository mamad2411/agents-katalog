---
name: go-sumdb-verify
description: >
  Go module checksum database (sum.golang.org) verification: go.sum integrity,
  GOPROXY/GOSUMDB/GONOSUMDB/GOPRIVATE settings, go mod verify, offline/airgap
  patterns, and diagnosing checksum mismatches. Use for owned build pipelines
  securing module fetch supply chain.
---

# Go SumDB Verify

## Scope And Authorization

- **In scope:** Build systems and modules you control; configuring private module access.
- **Out of scope:** Bypassing checksum verification to install tampered public modules for others.
- Checksums protect **content integrity**, not license or vulnerability status.
- Pair with `go-module-hygiene`, `go-govulncheck-workflow`, and private module proxy docs.

## When To Use

- CI fails with `SECURITY ERROR` / checksum mismatch.
- Configuring private repos (`GOPRIVATE`) correctly so sumdb is skipped only where needed.
- Hardening corporate builds with `GOSUMDB` and locked proxies.
- Auditing that developers did not disable verification globally.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Module tidy/deps | `go-module-hygiene` |
| Publishing modules | `go-module-release-workflow` |
| Vuln scanning | `go-govulncheck-workflow` |
| Generic supply chain attestations | `github-actions-artifact-attestations` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Variable / tool | Role |
| --- | --- |
| `go.sum` | Local record of module version hashes |
| SumDB | Global transparency log of checksums (`sum.golang.org`) |
| `GOSUMDB` | Which sumdb to use (`sum.golang.org`, `off`, custom) |
| `GOPROXY` | Module fetch proxy list |
| `GOPRIVATE` / `GONOSUMDB` / `GONOPROXY` | Patterns for private modules |
| `go mod verify` | Re-hash cached modules vs go.sum |

### Trust flow (public modules)

```text
go get → proxy downloads zip → hash checked against go.sum
                            → sumdb consulted for unknown versions
```

Mismatch ⇒ refuse build (good).

## Workflow

### 1. Inspect environment

```bash
go env GOPROXY GOSUMDB GOPRIVATE GONOSUMDB GONOPROXY
go version
```

Healthy public open-source setup example:

```text
GOPROXY=https://proxy.golang.org,direct
GOSUMDB=sum.golang.org
```

### 2. Verify local module graph

```bash
go mod verify
go mod download
go mod verify
```

Any failure: do **not** blindly delete go.sum lines.

### 3. Diagnose checksum mismatch

| Cause | Action |
| --- | --- |
| Legitimate upstream re-tag (rare/bad) | Contact maintainer; pin other version; retract |
| Corrupt local cache | `go clean -modcache` then re-download |
| MITM / bad proxy | Change proxy; investigate network |
| Hand-edited go.sum | Restore from git; `go mod tidy` |
| Private module hitting sumdb | Set `GOPRIVATE=*.corp.example.com` |

```bash
# Compare after clean (authorized machine)
go clean -modcache
go mod download
go mod verify
```

### 4. Private modules

```bash
go env -w GOPRIVATE=github.com/my-org/*,gitlab.internal.example/*
# equivalent skip sumdb:
# GONOSUMDB=$GOPRIVATE
```

Ensure:

- Auth to private VCS (`GIT_CONFIG`, SSH, netrc, CI token).
- `GONOPROXY` if private must not go through public proxy.
- Do **not** set `GOSUMDB=off` globally unless offline policy reviewed.

### 5. Corporate / offline

| Mode | Pattern |
| --- | --- |
| Athens/Goproxy cache | `GOPROXY=https://proxy.corp,https://proxy.golang.org,direct` |
| Airgap | Vendor (`go mod vendor`) + `-mod=vendor`; sumdb off only with verified vendor |
| Custom sumdb | `GOSUMDB=sum.corp+key https://sum.corp` per Go docs |

Vendor workflow:

```bash
go mod vendor
go test -mod=vendor ./...
```

Commit vendor only if team policy requires (pros/cons documented).

### 6. CI hardening

```yaml
- name: Verify modules
  run: |
    go mod verify
    go mod tidy
    git diff --exit-code go.mod go.sum
  env:
    GOPROXY: https://proxy.golang.org,direct
    GOSUMDB: sum.golang.org
    GOPRIVATE: github.com/my-org/*
```

Fail if developers commit with `GOSUMDB=off` accidentally — document team go env.

### 7. What verification does not do

- Find CVEs → govulncheck
- Prove maintainer identity beyond sumdb transparency properties
- Replace code review of new dependencies

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Public deps | SumDB on | `GOSUMDB=off` always |
| Private | GOPRIVATE patterns | Public sumdb lookup for private 404 noise + leaks |
| Mismatch | Investigate root cause | Delete sum lines until builds |
| Offline | Vendor + verified mirror | Random zip from chat |
| CI | go mod verify | Trust laptop-only sums |

## Output Checklist

- [ ] `go env` documented for team/CI
- [ ] `go mod verify` clean
- [ ] GOPRIVATE set for private paths
- [ ] No unjustified GOSUMDB=off
- [ ] Mismatch incidents root-caused
- [ ] Proxy strategy recorded
- [ ] CI enforces verify + tidy
- [ ] Linked to module hygiene/vuln skills

## Rules

- Treat checksum errors as security-relevant until proven otherwise.
- Scope private exclusions narrowly.
- Do not “fix” sum by disabling verification casually.
- Integrity ≠ safety from vulns.
- Airgap needs explicit trusted cache/vendor process.
