---
name: dbt-tests-and-docs
description: >
  Author dbt generic/singular tests and documentation for owned analytics
  projects: schema.yml tests, freshness, accepted values, relationships,
  doc blocks, and CI test gates. Use when hardening model quality and data
  contracts — pair with dbt-unit-testing for in-memory unit tests and
  dbt-exposures-lineage for consumer mapping.
---

# dbt Tests and Docs

## Scope And Authorization

- **In scope:** dbt projects and warehouses you are authorized to build/test.
- **Out of scope:** Running heavy full-refresh tests against production without approval; accessing unapproved data.
- Prefer CI on PR against dev schemas; limit warehouse cost.
- Pair with `dbt-unit-testing`, `dbt-exposures-lineage`, and `code-quality-standards`.

## When To Use

- Adding `unique`/`not_null`/relationships tests to marts.
- Documenting models/columns for self-serve analytics.
- Setting up `dbt test` in CI.
- Source freshness monitoring.
- Data contract style guarantees for stakeholders.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Unit tests without warehouse | `dbt-unit-testing` |
| Exposures/lineage | `dbt-exposures-lineage` |
| CDC ingestion | `debezium-cdc-postgres` |
| General SQL style | `sql-style-conventions` |
| Implementation quality baseline | `code-quality-standards` |

## Test types

| Kind | Mechanism | Use |
| --- | --- | --- |
| Generic | `unique`, `not_null`, `accepted_values`, `relationships` | Common column contracts |
| Singular | `tests/*.sql` returning failing rows | Custom business logic |
| Source freshness | `dbt source freshness` | Ingestion lag |
| Unit (dbt Core newer) | `unit_tests` YAML | See unit-testing skill |

## Workflow

### 1. Confirm scope and success criteria

1. Critical models (P0 marts) list.
2. Success: P0 models have primary key tests; docs for public columns; CI fails on test break; docs site published.

### 2. Document models

```yaml
version: 2

models:
  - name: fct_orders
    description: One row per completed order for analytics.
    columns:
      - name: order_id
        description: Surrogate key from billing system.
        tests:
          - unique
          - not_null
      - name: status
        description: Order lifecycle status.
        tests:
          - accepted_values:
              values: ['placed', 'paid', 'shipped', 'cancelled']
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

### 3. Doc blocks for reuse

```yaml
# models/_docs.yml
version: 2

docs:
  - name: order_id
    description: >
      Stable order identifier. Never reuse.
```

```yaml
columns:
  - name: order_id
    description: '{{ doc("order_id") }}'
```

### 4. Singular tests

```sql
-- tests/assert_order_totals_non_negative.sql
select order_id
from {{ ref('fct_orders') }}
where order_total < 0
```

Returns rows = failures.

### 5. Sources and freshness

```yaml
sources:
  - name: raw_billing
    database: raw
    schema: billing
    freshness:
      warn_after: {count: 6, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _loaded_at
    tables:
      - name: orders
        columns:
          - name: id
            tests: [not_null, unique]
```

### 6. CI

```bash
dbt deps
dbt parse
dbt build --select state:modified+ --defer --state path/to/prod-manifest  # if using slim CI
# or
dbt test --select fct_orders
dbt docs generate
```

Store `manifest.json`/`catalog.json` artifacts. Fail PR on test errors.

### 7. Operate

1. Triage flaky tests (late arrivals) with severity severity vs warn.
2. Own failures via model `meta.owner`.
3. Review test coverage quarterly on P0 nodes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| PK tests | unique+not_null on mart grains | No tests on revenue fact |
| Docs | Column meanings for consumers | Only model name |
| CI | Tests on modified+ downstream | Never test until prod break |
| Freshness | On raw sources | Only on final marts |
| Singular | Business invariants | Duplicate generic tests poorly |

## Output Checklist

- [ ] P0 models identified
- [ ] Grain tests (unique/not_null) applied
- [ ] Relationships where FKs matter
- [ ] accepted_values for enums
- [ ] Descriptions for public columns
- [ ] Source freshness configured
- [ ] Singular tests for key invariants
- [ ] CI runs dbt test/build
- [ ] Docs generated/published
- [ ] Owners on critical models

## Rules

- Tests encode contracts — treat failures as product bugs.
- Do not `dbt test` away without understanding cost on large tables (configure `where`/store failures carefully).
- Focus on **dbt tests and documentation**.
