---
name: golang-bi-access
description: >
  Control access to BI/analytics stacks fed by Go services: warehouse roles,
  row-level security, service accounts, and export governance. Use for owned
  data platforms under authorization.
---

# Golang BI Access

## Research grounding

Runbook for **Business Intelligence access control** when data is produced or
exported by Go pipelines—warehouses, semantic layers, dashboards. Skill id:
`golang-bi-access`.

## Scope And Authorization

- **In scope:** BI tools and warehouses you own; authorized data use.
- **Out of scope:** granting yourself access to data outside policy.
- Prefer least privilege and audited exports.
- Pair with `golang-access-reviews`, `golang-anonymize`, `code-quality-standards`.

## When To Use

- Go ETL loads warehouses consumed by Looker/Metabase/etc.
- Defining roles for analysts vs PII-restricted views.
- Securing Go-built metric APIs that power internal BI.
- Focus tokens: **golang, bi, access**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| App RBAC for product APIs | `golang-access-control` |
| Anonymized extracts | `golang-anonymize` |
| Access review campaigns | `golang-access-reviews` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Layer | Control |
| --- | --- |
| Ingestion (Go) | Job SA can write only target schemas |
| Warehouse | Roles, RLS/CLS, masking policies |
| BI tool | Group→role mapping; no shared admin |
| Exports | DLP review; row limits; watermark |
| Semantic | Certified datasets vs raw tables |
| Pitfalls | Analyst role SELECT on raw PII; Go job with superuser |

## Workflow

### 1. Confirm scope and success criteria

1. Data domains, tools, authorization, compliance class.
2. Success: matrix of groups→datasets; PII paths restricted; reviews scheduled.
3. Break-glass BI admin dual control.

### 2. Inventory

1. Go pipelines and destination schemas.
2. Dashboards with external shares.
3. Service accounts and personal credentials in use.

### 3. Baseline

1. Who can query PII today (export inventory).
2. Shadow IT extracts.

### 4. Implement controls

```go
// Go loader uses restricted SA
// DSN user: etl_loader — INSERT on analytics.staging only
```

1. Separate raw landing vs curated marts; BI users hit marts only.
2. Row-level security by region/tenant for multi-tenant data.
3. Column masking for email/phone in analyst roles.
4. Go metric APIs: OIDC + group claims; audit queries (`golang-audit-logging`).
5. Disable public link sharing or require allowlist domains.
6. Schedule access reviews for BI groups quarterly.

### 5. Verify with evidence

```bash
go test ./internal/etl/... -count=1
# Warehouse: role A cannot SELECT raw.pii_table
# BI: user without group cannot open restricted explore
```

1. Attempt over-privileged SA → denied.
2. Export path logged.

### 6. Observe and harden

1. Alert on grants to PII schemas; alert on new public dashboards.
2. Query audit logs sampling.
3. Rotate BI service tokens.

### 7. Hand off

1. Publish data access matrix.
2. Onboarding path for analysts (request → approve → group).
3. Link anonymize for external shares.

## Access matrix sketch

| Role | Raw PII | Curated marts | Exports |
| --- | --- | --- | --- |
| ETL SA | write landing | write | no |
| Analyst | no | yes (masked) | limited |
| Data sci (approved) | project-scoped | yes | approved |
| Exec dashboard | no | KPI only | no |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| SA | Least privilege schema | Superuser ETL |
| Share | Domain-restricted | Public web link to customer data |
| Review | Quarterly | Never |
| Topic fidelity | BI access + Go pipelines | Generic go test only |

## Output Checklist

- [ ] Tools and data domains inventoried
- [ ] Role matrix published
- [ ] Go pipeline SAs scoped
- [ ] RLS/masking verified
- [ ] Export governance in place
- [ ] Access reviews scheduled
- [ ] `code-quality-standards` applied to ETL code

## Rules

- Least privilege and auditability.
- Focus on `golang-bi-access`.
- Authorized data access only.
- No shared personal logins for admin.
