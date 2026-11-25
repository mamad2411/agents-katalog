---
name: dbt-exposures-lineage
description: >
  Document and use dbt exposures and lineage for owned analytics projects:
  declare BI dashboards/ML pipelines as exposures, generate docs/lineage graphs,
  impact analysis before model changes, and freshness contracts. Use when
  improving dbt governance, not for unauthorized access to warehouses.
---

# dbt Exposures and Lineage

## Scope And Authorization

- **In scope:** dbt projects and warehouses your org owns.
- **Out of scope:** Querying production warehouses without access approval; modifying others' dbt Cloud without permission.
- Prefer documented exposures over tribal knowledge of “who uses this model.”
- Pair with `dbt-tests-and-docs`, `dbt-unit-testing`, and `code-quality-standards`.

## When To Use

- Mapping dashboards, reverse ETL, and ML features to upstream models.
- Impact analysis before renaming/dropping columns.
- dbt docs site / Catalog lineage navigation.
- Establishing ownership for critical data products.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| dbt tests & docs broadly | `dbt-tests-and-docs` |
| dbt unit tests | `dbt-unit-testing` |
| Warehouse access control | data platform security skills |
| CDC into warehouse | `debezium-cdc-postgres` |
| Implementation quality baseline | `code-quality-standards` |

## Concepts

| Term | Role |
| --- | --- |
| Model/source | Nodes in lineage graph |
| Exposure | Downstream consumer (dashboard, app, ML) declared in YAML |
| Parent/child | DAG edges from `ref()` / `source()` |
| Impact analysis | Who breaks if node changes |
| Freshness | Source freshness SLA |

## Workflow

### 1. Confirm scope and success criteria

1. Critical dashboards and data products list.
2. Success: top consumers declared as exposures; owners set; docs generated; change process uses lineage.

### 2. Inventory consumers

Interview BI/ML/app teams:

| Consumer | Type | Owner | Upstream models (known) |
| --- | --- | --- | --- |
| Exec revenue board | dashboard | finance-bi | `fct_revenue` |
| Churn model | ml | ds-platform | `mart_users` |

### 3. Declare exposures

```yaml
# models/exposures.yml
version: 2

exposures:
  - name: exec_revenue_dashboard
    label: Exec Revenue Dashboard
    type: dashboard
    maturity: high
    url: https://bi.example.corp/dashboards/revenue
    description: Weekly executive revenue view
    depends_on:
      - ref('fct_revenue')
      - ref('dim_accounts')
    owner:
      name: Finance BI
      email: finance-bi@example.com
    tags: ['p0', 'finance']
```

Types commonly: `dashboard`, `notebook`, `analysis`, `ml`, `application`.

### 4. Generate and publish lineage

```bash
dbt deps
dbt parse
dbt docs generate
dbt docs serve  # or publish to dbt Cloud/Catalog
```

Navigate model → dependents/exposures. Ensure CI runs `dbt parse` on PRs.

### 5. Use lineage in change management

Before dropping/renaming:

```bash
# Find refs
rg -n "ref\\('fct_revenue'\\)" models/
# Review exposure dependents in docs UI
```

PR template checklist:

- [ ] Lineage dependents reviewed
- [ ] Exposures owners notified
- [ ] Column-level contracts/tests updated

### 6. Source freshness + exposure criticality

```yaml
sources:
  - name: raw_billing
    freshness:
      warn_after: {count: 6, period: hour}
      error_after: {count: 12, period: hour}
    tables:
      - name: invoices
```

```bash
dbt source freshness
```

P0 exposures should map to freshness alerts on their upstream sources.

### 7. Govern drift

1. Quarterly review: exposures still valid URLs/owners?
2. Block merge of model deletion if exposures depend on it (policy/manual).
3. Prefer semantic layer / metrics tooling integration when available.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Exposures | Owned + URL + depends_on | Empty YAML theater |
| Changes | Notify exposure owners | Silent breaking rename |
| Docs | Generated in CI artifact | Only on laptops |
| Freshness | Alert P0 paths | All sources same lazy SLA |
| Lineage | From `ref` integrity | Hardcoded table names bypassing dbt |

## Output Checklist

- [ ] Critical consumers listed
- [ ] Exposures YAML committed
- [ ] Owners and maturity set
- [ ] `dbt docs generate` in CI/publish path
- [ ] Impact analysis process documented
- [ ] Freshness on key sources
- [ ] PR checklist includes lineage
- [ ] Quarterly exposure audit scheduled
- [ ] Tags for P0 data products
- [ ] Residual unknown consumers noted

## Rules

- Lineage is only as good as `ref`/`source` discipline and exposure honesty.
- Notify humans behind exposures before breaking changes.
- Focus on **dbt exposures and lineage governance**.
