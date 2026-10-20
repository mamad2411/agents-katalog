---
name: golang-aqua-notes
description: >
  Operational notes for container security platforms (Aqua-class) with Go
  workloads: image scanning gates, runtime policies, CI integration, and
  exception handling. Use for owned clusters under authorization.
---

# Golang Aqua Notes

## Research grounding

Runbook for integrating **container security platforms** (Aqua Security and
similar: scan + runtime + supply chain) with **Go** image pipelines and
Kubernetes runtimes. Product UIs change—capture durable controls. Skill id:
`golang-aqua-notes`.

## Scope And Authorization

- **In scope:** registries, clusters, and CI you own.
- **Out of scope:** scanning systems without authorization.
- Prefer audit/warn mode before enforce.
- Redact registry credentials and platform API keys.
- Pair with `golang-attestations`, `secure-sdlc-checklist`, `code-quality-standards`.

## When To Use

- Gating Go container images on CVE/severity policies before deploy.
- Runtime controls (drift, exec, network) on Go service pods.
- Wiring scanner CLI/API into Go service CI.
- Focus tokens: **golang, aqua, notes** (container security platform ops).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic vuln scanning of Go modules | `govulncheck` in `code-quality-standards` / SSDLC |
| Signed attestations design | `golang-attestations` |
| K8s admission webhooks you write | `golang-admission` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Guidance for Go images |
| --- | --- |
| Base image | Distroless/static where possible; pin digests |
| Scan gate | Block critical/high with fix available; exceptions expire |
| Language | Scanner should inventory Go modules in image |
| Secrets | Fail build if keys found in layers |
| Runtime | Read-only root FS; drop caps; no privileged |
| Drift | Alert on shell in distroless pods |
| CI | Scan after `docker build` of Go binary image |
| Pitfalls | Ignoring base OS CVEs; permanent suppressions |

## Workflow

### 1. Confirm scope and success criteria

1. Platform tenant, registries, clusters, authorization.
2. Success: CI fails on policy breach; prod runtime policy attached; exception process works.
3. Owners for suppressions.

### 2. Inventory

1. Go services images and base images.
2. Existing scan tools (Trivy/Grype/Aqua/etc.).
3. Runtime enforcer coverage (% nodes).

### 3. Baseline

1. Current critical CVE count on latest tags.
2. Runtime incidents last 90 days.
3. Export policy JSON/hash.

### 4. Integrate pipeline

```bash
# Build minimal Go image
CGO_ENABLED=0 go build -trimpath -o app ./cmd/app
# docker build -t registry.example/app:$GIT_SHA .

# Platform CLI pattern (illustrative name)
# aqua scan image registry.example/app:$GIT_SHA --fail-on high
# or trivy image --exit-code 1 --severity HIGH,CRITICAL registry.example/app:$GIT_SHA

go test ./... -count=1
govulncheck ./...
```

1. Scan **deployed digest**, not only `latest`.
2. Map results to ticket system; auto-open for new criticals.
3. Runtime: enforce non-root, read-only FS for Go static binaries.
4. Exceptions: CVE ID, image, owner, expiry ≤90 days, risk note.

### 5. Verify with evidence

1. PR with vulnerable base → CI red.
2. Clean image → CI green; admission allows digest.
3. Runtime: attempt `kubectl exec` if policy denies → denied (lab).
4. Redact platform tokens from logs.

### 6. Observe and harden

1. Dashboards: vulns by service, mean time to remediate, expired exceptions.
2. Alert on runtime blocks and on scanner outages (fail policy documented).
3. Rebuild Go images when base or Go toolchain patches.

### 7. Hand off

1. Runbook: exception request, false positive appeal.
2. Link SSDLC gates (`golang-asvs-gates` if used).
3. Quarterly policy review.

## Policy sketch

| Severity | CI | Prod deploy |
| --- | --- | --- |
| Critical fix available | Fail | Block |
| High | Fail or warn-by-service | Time-boxed |
| Medium | Ticket | Allow |
| Negligible | Report | Allow |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Gate | Digest-pinned scan | Scan ignored in CD |
| Exception | Expiry + owner | Forever suppress critical |
| Image | Static non-root | Fat image + shell as root |
| Go modules | govulncheck + image scan | Only one of them forever |
| Topic fidelity | Container platform + Go images | Generic go test only |

## Output Checklist

- [ ] Platform scope and owners set
- [ ] CI scan gate for Go images
- [ ] Runtime policies on target clusters
- [ ] Exception workflow with expiry
- [ ] Evidence of fail/pass cases
- [ ] MTTR metrics visible
- [ ] `code-quality-standards` applied to pipeline code

## Rules

- Authorized scanning only.
- Prefer warn→enforce rollouts.
- Focus on `golang-aqua-notes`.
- Never commit platform API keys.
