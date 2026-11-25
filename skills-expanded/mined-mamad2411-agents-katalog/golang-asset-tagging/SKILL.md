---
name: golang-asset-tagging
description: >
  Standardize asset tagging for Go services and cloud resources: required keys,
  ownership, data class, propagation from code to runtime, and compliance.
  Use for owned inventories under authorization.
---

# Golang Asset Tagging

## Research grounding

Runbook for **consistent tagging/labeling** of services, cloud resources, images,
and repos that implement or host Go workloads—so ASM, cost, and security can
route ownership. Skill id: `golang-asset-tagging`.

## Scope And Authorization

- **In scope:** cloud accounts, clusters, and repos you administer.
- **Out of scope:** modifying third-party account tags without permission.
- Prefer policy-as-code enforcement; allow exceptions with expiry.
- Pair with `golang-asm-surface`, FinOps practices, `code-quality-standards`.

## When To Use

- Defining org tag taxonomy and applying to Go service deploy pipelines.
- Fixing unowned resources discovered by ASM/cost tools.
- Propagating labels from Go Helm/K8s manifests and AWS resources.
- Focus tokens: **golang, asset, tagging**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Attack surface discovery | `golang-asm-surface` |
| Access reviews of people | `golang-access-reviews` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Tag key (example) | Purpose |
| --- | --- |
| `owner` / `team` | Page routing, cost |
| `service` | Correlate logs/metrics/AMIs |
| `env` | prod/stage/dev |
| `data-class` | public/internal/confidential |
| `repo` | source mapping |
| `go-version` or `runtime` | patch campaigns |
| `cost-center` | finance |
| Pitfalls | Free-text drift; PII in tags; missing on ephemeral resources |

## Workflow

### 1. Confirm scope and success criteria

1. Org units, clouds, authorization.
2. Success: ≥95% of prod resources have required tags; CI blocks missing tags.
3. Approved key list published.

### 2. Inventory

1. Existing tag keys (cardinality explosion?).
2. Go deploy paths: Terraform, Helm, ECS task defs, Lambda.
3. Orphan resources without `owner`.

### 3. Baseline

1. Compliance % report snapshot.
2. Agree required vs optional tags.

### 4. Implement standards

**K8s labels for Go apps:**

```yaml
metadata:
  labels:
    app.kubernetes.io/name: payments-api
    app.kubernetes.io/part-of: checkout
    owner: team-payments
    env: prod
    data-class: confidential
```

**AWS tags via IaC (illustrative):**

```hcl
tags = {
  owner       = "team-payments"
  service     = "payments-api"
  env         = "prod"
  data-class  = "confidential"
  repo        = "github.com/org/payments-api"
}
```

**Go metrics/log fields:** align `service` label with tag value for join.

1. Pipeline injects tags from single service catalog YAML.
2. OPA/admission or cloud policy denies missing required tags in prod.
3. Normalize case (`env=prod` not `Prod`).
4. Ban tags containing emails/secrets.

### 5. Verify with evidence

```bash
go test ./... -count=1
# terraform validate / conftest / opa test on policies
# kubectl get deploy -A -o json | jq '...' # required labels present
```

1. New Go service pipeline fails without tags.
2. Backfill script dry-run then apply for orphans.
3. ASM inventory shows owner populated.

### 6. Observe and harden

1. Weekly noncompliant resource report to teams.
2. Auto-remediate safe defaults only where policy allows.
3. Review taxonomy annually; retire unused keys.

### 7. Hand off

1. Publish tag dictionary with examples.
2. Service catalog owns canonical `service` names.
3. Link on-call mapping from `owner` tag.

## Required tag matrix (example)

| Resource | owner | service | env | data-class |
| --- | --- | --- | --- | --- |
| EKS Deployment | req | req | req | req |
| AMI | req | req | opt | opt |
| S3 bucket | req | req | req | req |
| ECR image | req | req | opt | opt |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Source of truth | Catalog → pipeline | Hand-typed per console |
| Enforcement | Policy deny in prod | Optional guidelines only |
| Values | Enumerated env | Typos galore |
| Privacy | No PII in tags | `owner=jane@corp` everywhere |
| Topic fidelity | Tagging standards for Go estates | Generic go test only |

## Output Checklist

- [ ] Tag dictionary published
- [ ] Required keys agreed
- [ ] Pipelines inject tags for Go services
- [ ] Policy enforcement in prod
- [ ] Backfill plan for orphans
- [ ] Compliance metrics visible
- [ ] `code-quality-standards` applied to policy code

## Rules

- Consistent, minimal, non-secret tags.
- Focus on `golang-asset-tagging`.
- Authorized account changes only.
- Do not encode credentials in tags.
