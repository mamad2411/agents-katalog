---
name: "dbt"
description: "dbt models, sources, tests, macros, incremental models, documentation, CI integration, Jinja patterns"
---

# dbt Data Pipelines Skill

## When to activate
- Writing dbt models (staging, intermediate, mart layers)
- Configuring dbt sources, refs, and dependencies
- Writing dbt tests (schema tests, singular tests, custom generic tests)
- Setting up dbt project structure for a new data warehouse
- Writing dbt macros for reusable SQL logic
- Configuring dbt documentation and freshness checks
- Debugging dbt compilation errors or failed model runs
- Setting up dbt with BigQuery, Snowflake, Redshift, or DuckDB

## When NOT to use
- Raw ETL pipelines without a warehouse (use Airflow, Prefect, or Dagster instead)
- Real-time streaming data (dbt is batch-only)
- Pandas/Polars in-memory transformations (use the pandas-polars skill)
- Data ingestion (dbt transforms, it doesn't ingest)

## Instructions

### Project layer architecture
Always separate models into three layers:
```
models/
├── staging/          ← 1:1 with source tables. Light cleaning only. No joins.
│   ├── stg_orders.sql
│   └── stg_customers.sql
├── intermediate/     ← Business logic. Joins allowed. Not exposed to BI tools.
│   └── int_orders_with_customers.sql
└── marts/            ← Final business entities. Exposed to BI. Aggregations live here.
    ├── finance/
    │   └── fct_revenue.sql
    └── marketing/
        └── dim_customers.sql
```

**Staging rules:**
- Rename columns to project conventions (snake_case)
- Cast types explicitly
- No business logic — no joins, no aggregations
- Prefix with `stg_`

**Mart rules:**
- `fct_` prefix for fact tables (events, transactions)
- `dim_` prefix for dimension tables (customers, products)
- Always document in schema.yml

### Model configuration
```sql
-- models/marts/finance/fct_revenue.sql
{{
  config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail'
  )
}}

with orders as (
    select * from {{ ref('int_orders_with_customers') }}
    {% if is_incremental() %}
    where created_at > (select max(created_at) from {{ this }})
    {% endif %}
)

select
    order_id,
    customer_id,
    amount,
    created_at
from orders
```

**Materialization choices:**
- `view`: default — good for staging and intermediate models
- `table`: for expensive queries queried frequently
- `incremental`: for large fact tables that grow over time
- `ephemeral`: CTEs, not materialized — use for simple transformations called once

### Testing — required on every mart model
```yaml
# models/marts/finance/schema.yml
version: 2

models:
  - name: fct_revenue
    description: "One row per completed order"
    columns:
      - name: order_id
        description: "Primary key"
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

Minimum tests on every mart model: `unique` + `not_null` on primary key, `not_null` on critical foreign keys.

### Sources configuration
```yaml
# models/staging/sources.yml
version: 2

sources:
  - name: raw_stripe
    database: raw
    schema: stripe
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _ingested_at
    tables:
      - name: charges
        description: "Raw Stripe charges from Fivetran"
```

Always set `freshness` on sources — stale source data is a silent failure.

### Macros for reusable logic
```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name) %}
    ({{ column_name }} / 100.0)::numeric(10, 2)
{% endmacro %}

-- Usage in model
select
    {{ cents_to_dollars('amount_cents') }} as amount_dollars
from orders
```

## Example

**User:** Create staging and mart models for Stripe payments data (charges, refunds) with tests and freshness checks.

**Expected output:**
- `models/staging/stripe/sources.yml` — source with freshness check on `_ingested_at`
- `models/staging/stripe/stg_stripe_charges.sql` — rename, cast, no joins
- `models/staging/stripe/stg_stripe_refunds.sql` — same pattern
- `models/marts/finance/fct_payments.sql` — join charges + refunds, net amount, incremental materialization
- `models/marts/finance/schema.yml` — `unique` + `not_null` on `charge_id`, relationship test on `customer_id`

---
