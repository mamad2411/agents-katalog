---
name: golang-blast-radius
description: >
  Analyze and reduce blast radius for Go systems: trust boundaries, tenancy
  isolation, permission scopes, deploy topology, and failure containment.
  Use for owned architectures under authorization.
---

# Golang Blast Radius

## Research grounding

Runbook for **blast radius analysis**—how far a compromise or bug in a Go
component can spread—and techniques to shrink it. Skill id: `golang-blast-radius`.

## Scope And Authorization

- **In scope:** systems you own; authorized chaos/failure tests.
- **Out of scope:** expanding damage on systems without permission.
- Prefer tabletop + controlled experiments in staging.
- Pair with `golang-authz-design`, `golang-active-passive`, `golang-attack-trees`.

## When To Use

- Design reviews for multi-tenant Go SaaS.
- After incidents: quantify and reduce spread paths.
- CI/CD permission scoping for Go deploy roles.
- Focus tokens: **golang, blast, radius**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AuthZ implementation | `golang-access-control` |
| Attack trees | `golang-attack-trees` |
| Backup immutability | `golang-backup-immutable` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Dimension | Reduce radius by |
| --- | --- |
| Identity | Short-lived creds; per-service SA; no shared god tokens |
| Tenancy | Hard tenant isolation in data + authz |
| Network | Segment prod; mesh policies; no flat VPC trust |
| Deploy | Separate pipelines; environment isolation |
| Data | Encrypt; minimize replicas of PII |
| Dependencies | Bulkheads; timeouts (`golang-backpressure`) |
| Humans | Tiered admin (`golang-ad-tiering` analogy for cloud) |
| Pitfalls | One Kubernetes cluster admin = all apps; one DB user for all services |

## Workflow

### 1. Confirm scope and success criteria

1. Component under analysis, threat (compromise of service X), authorization.
2. Success: diagram of reachable assets; mitigations cut top paths; residual accepted.
3. Metrics: max tenants impacted, max data classes, max accounts.

### 2. Inventory trust

1. Credentials the Go service holds (DB, cloud, JWT signing).
2. Network paths and admin APIs.
3. Shared platforms (cluster, monorepo CI OIDC).

### 3. Baseline radius

1. Assume full RCE as service identity—what can it read/write?
2. Assume stolen deploy role—what can it ship?
3. Assume one tenant malicious—can they touch others?

### 4. Reduce

```go
// Per-tenant DB credentials or forced tenant_id predicate
// Prefer: SET app.tenant = $id + RLS over superuser app role
```

1. Split shared god SA into per-service roles with least privilege.
2. Separate signing keys per env; deny prod keys in staging.
3. Cell-based or shard isolation for high-risk tenants if needed.
4. CI: environment-scoped OIDC; require reviews for prod.
5. Feature: disable dangerous admin bulk APIs or dual-control them.
6. Rate limit and authz on export endpoints.

### 5. Verify with evidence

```bash
go test ./internal/tenancy/... -count=1
# IAM policy simulator: service role cannot iam:* or s3:* all
# Cross-tenant integration tests deny
```

1. Recompute radius metrics after changes.
2. Chaos: kill dependency—failure contained (errors not cascade wipe).

### 6. Observe and harden

1. Continuous cloud IAM lint for privilege creep.
2. Attack mapping updates when radius changes.
3. Review monorepo CI permissions quarterly.

### 7. Hand off

1. Architecture decision records for isolation choices.
2. Residual radius statement for risk committee.
3. Link runbooks for containment during incidents.

## Scoring sketch

| Score | Meaning |
| --- | --- |
| R1 | Single tenant / single host |
| R2 | Single service multi-tenant |
| R3 | Multi-service same account |
| R4 | Org-wide cloud admin impact |

Aim to lower score for tier-0 services.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Creds | Per-service short-lived | One long-lived admin key in all pods |
| Tenant | RLS + tests | `WHERE` filter forgotten |
| CI | Env-scoped OIDC | `write-all` to prod from PR |
| Topic fidelity | Blast radius analysis | Generic go test only |

## Output Checklist

- [ ] Component and threat framed
- [ ] Credential/network inventory done
- [ ] Baseline radius scored
- [ ] Mitigations applied
- [ ] Cross-tenant and IAM evidence
- [ ] Residual risk documented
- [ ] Review date set

## Rules

- Prefer isolation over perfect detection.
- Focus on `golang-blast-radius`.
- Authorized tests only.
- Measure before/after.
