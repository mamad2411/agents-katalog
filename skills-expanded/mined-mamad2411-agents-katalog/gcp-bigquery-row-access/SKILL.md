---
name: gcp-bigquery-row-access
description: >
  Implement and review BigQuery row-level security (row access policies) and related
  column security: filter predicates, principals, authorized views alternatives, and
  testing deny paths. Use when restricting which rows principals can query in owned
  BigQuery datasets—not for bypassing another tenant’s policies.
---

# GCP BigQuery Row Access

## Scope And Authorization

- **In scope:** BigQuery datasets/tables in projects you own or are authorized to secure.
- **Out of scope:** escalating privileges in foreign GCP orgs or exfiltrating restricted rows without authorization.
- Test with least-privilege test users; never use production data copies without policy.
- Redact row filter examples if they reveal sensitive business logic.
- Pair SQL with `sql-style-conventions` and `code-quality-standards`.

## When To Use

- Multi-tenant or multi-region tables needing **row access policies**.
- Restricting analysts to `customer_id = SESSION_USER()` style predicates (or attribute tables).
- Comparing row policies vs authorized views vs separate tables.
- Auditing whether filters can be bypassed via wildcards, scripts, or JOINs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Feature store Feast auth | `feature-store-feast-auth` |
| General IAM secrets | `secrets-management-hygiene` |
| Dataflow pipelines | `gcp-dataflow-flex-templates` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Role |
| --- | --- |
| Row access policy | Server-enforced predicate per principal set |
| Column security | Policy tags / restricted columns (pair as needed) |
| Authorized view | Share subset via view with owner’s rights carefully |
| Table ACL | Dataset/table IAM still required |
| True/False filters | `TRUE` for admins; fine-grained for analysts |

## Workflow

### 1. Confirm scope and success criteria

1. Tables, sensitivity, identity model (Google groups, workforce ID).
2. Success: unauthorized user cannot see others’ rows via console/API/Jobs; performance acceptable; admin break-glass documented.
3. Define attributes (tenant_id, region, clearance).

### 2. Inventory

```bash
bq ls project:dataset
bq show --format=prettyjson project:dataset.table
# List row access policies (API/gcloud as available)
```

```sql
-- Who has dataset access?
-- Review IAM in console or via gcloud asset / IAM policy export
```

1. Note ETL writers that must bypass or use elevated SA.
2. Find BI tools using shared service accounts (anti-pattern for RLS).

### 3. Design predicates

```sql
-- Conceptual row access policy filter
-- SESSION_USER() email matches owner column OR group-based access via access map table
-- Example sketch:
-- customer_id IN (
--   SELECT customer_id FROM access_map WHERE user_email = SESSION_USER()
-- )
```

1. Prefer immutable tenant keys on each row.
2. Avoid filters that reference non-deterministic functions incorrectly.
3. Document admin policy with broader filter and dual control.

### 4. Apply policies

```bash
# Illustrative — use current bq/API syntax for create row access policy
# bq mk --row_access_policy --policy_id=tenant_isolation ...
```

```sql
-- Grant table metadata/data access as needed; row policy further filters rows
```

1. Combine with **column-level** restrictions for PII columns.
2. Replace shared “analyst SA” with user OAuth or per-team SAs mapped in access tables.
3. For complex logic, authorized views may complement—but prevent view shopping that escapes filters.

### 5. Verify with evidence

| Test user | Query | Expect |
| --- | --- | --- |
| Tenant A user | `SELECT * FROM t` | Only A rows |
| Tenant B user | same | Only B rows |
| No policy principal | | Denied or empty per design |
| Job via API | same filters | Cannot bypass via `bq query` |

```sql
-- As restricted user
SELECT COUNT(*), tenant_id FROM project.dataset.t GROUP BY tenant_id;
```

1. Try `CREATE TABLE AS SELECT` copy—ensure permissions don’t allow unrestricted export if policy requires.
2. Test JOINs to unrestricted tables for leakage patterns; fix with careful design.

### 6. Observe and harden

1. Audit logs for BigQuery data access.
2. Alert on policy removal events.
3. CI: policy definitions as code reviewed.

### 7. Hand off

1. Policy catalog: id, filter summary, principals, owner.
2. Break-glass procedure.
3. Apply `code-quality-standards` for IaC/SQL.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Identity | End-user credentials | One SA for all BI users |
| Filter | Tenant key + map table | Client-side filter only |
| Admin | Dual control | Everyone TRUE policy |
| Export | Controlled | CTAS to open dataset |
| Evidence | Two-user deny proof | “Policy created” screenshot only |
| Evolution | Versioned SQL | ClickOps drift |

## Output Checklist

- [ ] Tables and identity model documented
- [ ] Row policies defined as code
- [ ] Column security considered
- [ ] Cross-tenant deny evidenced
- [ ] ETL/admin paths documented
- [ ] Audit logging enabled/reviewed
- [ ] BI tool identity fixed if shared SA
- [ ] `code-quality-standards` applied

## Rules

- Owned datasets; authorized tests only.
- Row policies are not a substitute for dataset IAM least privilege.
- Prove deny paths with real principals.
- Keep filter logic simple enough to audit.
