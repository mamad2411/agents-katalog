---
name: golang-asm-surface
description: >
  Attack surface management for Go services: inventory listeners, deps, cloud
  exposures, continuous discovery, and reduction tracking. Use for owned estates
  under authorization.
---

# Golang ASM Surface

## Research grounding

Runbook for **Attack Surface Management (ASM)** focused on organizations that
run **Go services**—discovering what is exposed and shrinking it. Skill id:
`golang-asm-surface`.

## Scope And Authorization

- **In scope:** assets you own; authorized ASM tooling and scanning.
- **Out of scope:** scanning third-party ranges without permission.
- Prefer passive DNS/cert transparency first; active scan only in scope.
- Redact customer hostnames if required; no full exploit in ASM notes.
- Pair with `recon-and-methodology`, `golang-api-surface`, `code-quality-standards`.

## When To Use

- Building or operating continuous external/internal exposure inventory.
- Mapping Go services’ ports, domains, and admin UIs.
- Tracking “shadow” APIs and forgotten staging endpoints.
- Focus tokens: **golang, asm, surface** (attack surface management).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| API design minimization | `golang-api-surface` |
| Deep vuln exploitation | authorized pentest skills per finding class |
| Asset tagging taxonomy only | `golang-asset-tagging` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Surface type | Go-relevant examples |
| --- | --- |
| Network | Public LB → Go `:8080`; accidental `:6060` pprof |
| Identity | Callback URLs, device code flows |
| Software | Exposed gRPC reflection; debug routes |
| Cloud | Public buckets with Go build artifacts |
| CI | Workflow dispatch endpoints; open runners |
| Dependencies | Old Go modules with known CVEs on edge |

## Workflow

### 1. Confirm scope and success criteria

1. Domains, IP ranges, clouds, authorization letter.
2. Success: inventory freshness ≤7d; critical exposures ticketed SLA; trend down.
3. Define severity model for exposures.

### 2. Discover

1. Cert transparency, DNS, cloud inventory APIs, k8s ingress list, API gateways.
2. From code: extract listen addresses and route mounts.

```bash
rg -n "ListenAndServe|Listen\(|:6060|pprof|grpc\.NewServer" --glob '*.go'
rg -n "Reflection|EnableReflection" --glob '*.go'
```

3. Merge into asset DB with owner tags (`golang-asset-tagging`).

### 3. Baseline

1. Snapshot current public endpoints and open security groups.
2. Mark known-good vs unknown.

### 4. Reduce surface

1. Remove public admin/debug; bind metrics to internal only.
2. Close orphan DNS; expire old staging.
3. Require auth on all external Go routes; gateway front door.
4. Disable gRPC reflection in prod.
5. Track each reduction with before/after evidence.

### 5. Verify with evidence

```bash
go test ./... -count=1
# Authorized external checks against own assets only
# nmap/httpx only on scoped targets
```

1. Re-scan after change; exposure closed.
2. Confirm monitoring still works via internal path.
3. Owner assigned for residual accepted risks.

### 6. Observe and harden

1. Continuous ASM alerts on new public assets.
2. Weekly new-asset owner notification.
3. Tie deploys to inventory updates (service catalog).

### 7. Hand off

1. Dashboard of open exposures by severity.
2. Quarterly reduction goals.
3. Link findings to fix skills (auth, surface design).

## Exposure severity sketch

| Finding | Severity |
| --- | --- |
| Unauth admin/debug on Internet | Critical |
| Forgotten staging with prod data | High |
| Public metrics with sensitive labels | Medium |
| Documented public marketing API | Info (track) |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Written ranges | Whole Internet scans |
| Discovery | Multi-source merge | Single nmap once a year |
| Fix | Close + verify | Ticket forever open |
| Go specifics | pprof/reflection/listen audit | Ignore code inventory |
| Topic fidelity | ASM for Go estates | Generic go test only |

## Output Checklist

- [ ] Authorized scope recorded
- [ ] Discovery sources connected
- [ ] Go listeners/routes inventoried
- [ ] Critical exposures remediated or accepted
- [ ] Continuous detection of new assets
- [ ] Owners and tags applied
- [ ] Trend metrics reviewed
- [ ] `code-quality-standards` applied to any tooling

## Rules

- Authorized scanning only; evidence over guesses.
- Prefer reduction over endless finding collection.
- Focus on `golang-asm-surface`.
- Do not store full exploit PoCs in ASM tickets for prod.
