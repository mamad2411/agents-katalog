---
name: fivetran-transform-notes
description: >
  Govern Fivetran transformations (dbt Core/Cloud integration, Quickstart data models,
  scheduled transforms): permissions, secrets, warehouse write scope, model review,
  PII handling, and failure observability. Use when operating owned Fivetran ELT
  pipelines, reviewing who can change transforms, or hardening post-load SQL/dbt runs.
---

# Fivetran Transform Notes

## Scope And Authorization

- **In scope:** Fivetran accounts, destinations, and warehouses you own; authorized analytics reviews.
- **Out of scope:** accessing another org’s Fivetran tenant or warehouse data without permission.
- Prefer non-prod destinations for experiments; mask PII in dev.
- Redact warehouse credentials and personal data from tickets.
- Pair SQL/dbt changes with `code-quality-standards` and `sql-style-conventions` as applicable.

## When To Use

- Enabling or reviewing **Fivetran transformations** (dbt integration, transformation runs).
- Controlling which service accounts can run models that write curated schemas.
- Preventing unreviewed SQL from productionizing sensitive marts.
- Operational notes: scheduling, retries, run logs, cost controls.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic dbt project structure alone | dbt/data skills in catalog if present |
| Warehouse secrets program | `secrets-management-hygiene` |
| BigQuery row access policies | `gcp-bigquery-row-access` |
| Database migration safety | `database-migration-safety` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Fivetran role | ELT extract/load; transforms shape curated data after load |
| Transform types | Integrated dbt, Quickstart models, custom | 
| Risk | Over-privileged destination creds; PII expansion; silent model drift |
| Controls | RBAC in Fivetran + warehouse grants; PR review for dbt; separate write schemas |
| Observe | Transform run history, freshness, test failures |

## Trust boundaries

| Boundary | Question |
| --- | --- |
| Fivetran → warehouse | What roles can CREATE/INSERT in prod marts? |
| Engineer → Fivetran | Who can edit connections/transforms? |
| dbt code → runtime | Are models reviewed and versioned? |
| Output → BI | Are grants on marts least privilege? |

## Workflow

### 1. Confirm scope and success criteria

1. Account, destinations, transformation feature set, dbt connection mode.
2. Success: only approved identities alter transforms; prod writes scoped; tests gate deploys; PII columns documented.
3. Cost/runtime budgets for transform schedules.

### 2. Inventory

```text
Connections → destination schemas (raw) → transform jobs → curated schemas → BI users
```

1. List users/roles in Fivetran with transform edit rights.
2. List warehouse role used by Fivetran destination and by dbt runner.
3. Locate dbt project repo and CI.

```sql
-- Warehouse examples (adapt): who has write on curated schema?
-- SHOW GRANTS ON SCHEMA curated_finance;
```

### 3. Baseline risks

1. Destination credentials with `ACCOUNTADMIN`/owner-equivalent.
2. Transforms selecting `select *` from raw PII into broadly shared marts.
3. No `dbt test` / schema tests on critical models.
4. Shared dev/prod destinations.

### 4. Apply governance

1. **Separate schemas:** `raw_*` (Fivetran write), `stg_*` / `mart_*` (transform write), BI read-only on marts.
2. **Least privilege:** Fivetran role write raw only; transform role write curated only; no DROP on unrelated DBs.
3. **Code review:** dbt models via PR; protect main branch; required CI `dbt build` on sample/dev target.
4. **Secrets:** OAuth/keypair in secret manager; rotate; no keys in dbt `profiles.yml` committed.
5. **PII:** column-level tagging; limit who can add raw PII to wide marts; consider dynamic masking/RLS skills.
6. **Scheduling:** off-peak heavy models; dependency awareness after Fivetran sync success.
7. **Quickstart models:** review generated SQL before prod; pin versions.

```yaml
# Conceptual CI gates
# - dbt parse
# - dbt build --select state:modified+
# - SQLFluff / warehouse policy checks
```

### 5. Verify with evidence

| Check | Evidence |
| --- | --- |
| Transform editor RBAC | Screenshot/export of Fivetran permissions |
| Warehouse grants | Query grants; no superuser for connector |
| Failed bad model | CI red on breaking change |
| PII mart access | Unauthorized BI user denied |

```bash
# Example dbt (owned project)
dbt deps
dbt build --target dev
```

### 6. Observe and harden

1. Monitor transform failures and row count anomalies.
2. Alert when grants change on Fivetran service roles.
3. Quarterly access review for Fivetran users and warehouse roles.

### 7. Hand off

1. Diagram raw→transform→mart; owners for each layer.
2. Runbook for failed transforms (rerun, partial, data freeze).
3. Apply code quality/SQL style to models shipped.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Creds | Scoped roles per layer | One god warehouse user |
| Models | PR + CI tests | Edit SQL live in prod UI only |
| PII | Tagged + restricted marts | `SELECT *` raw into public schema |
| Env | Dev destination | All transforms hit prod |
| Secrets | Managed, rotated | Key in git `profiles.yml` |
| Failures | Alert + data freshness SLA | Silent stale dashboards |

## Output Checklist

- [ ] Fivetran account/destination/transform inventory
- [ ] RBAC for who edits transforms
- [ ] Warehouse grants least privilege evidenced
- [ ] dbt/SQL review and CI gates
- [ ] PII handling documented
- [ ] Schedule and dependency on sync defined
- [ ] Monitoring for transform failures
- [ ] Runbook and owners
- [ ] `code-quality-standards` applied

## Rules

- Owned tenants and warehouses only.
- Transforms can expand blast radius of raw data—treat as production code.
- Prefer schema separation and PR review over unrestricted UI SQL.
- Route pure warehouse RLS or secrets programs to neighbor skills.
