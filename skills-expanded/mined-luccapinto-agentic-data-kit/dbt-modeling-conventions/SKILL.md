---
name: dbt-modeling-conventions
description: Applies the organization's dbt modeling conventions. Use when the user writes, reviews, or renames dbt models, mentions dbt, staging, marts, fct_ or dim_ tables, schema.yml, surrogate keys, model naming, CTE structure, or dimensional modeling (star schema) with dbt.
---

# Skill: dbt-modeling-conventions

Org conventions only — the model already knows generic SQL and dbt. Apply these to every model
you write or review.

## CTE structure
- `import` CTEs on top (one per `ref()`/`source()`, `select` only the needed columns).
- `logical` CTEs in the middle (joins, filters, calculations — one step each).
- One `final` CTE at the bottom; the model ends with `select * from final`.

## Naming
| Prefix | Layer |
|---|---|
| `stg_` | Staging: 1:1 with a source table, rename/cast only |
| `dim_` | Dimension |
| `fct_` | Fact |
| `mart_` | Business-facing mart built on dims/facts |

## Keys and grain
- Every dimension has a surrogate key `sk_<entity>`: a hash of the natural key.
- One grain per fact table; state it in the model description ("one row per order line").
- Build dimensions before facts.

## Tests and docs
Every model has a `schema.yml` entry with a description and `unique` + `not_null` on its
primary key.

## Example

```sql
-- models/marts/dim_customer.sql
with stg_customers as (
    select * from {{ ref('stg_crm__customers') }}
),
customers_keyed as (
    select
        {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as sk_customer,
        customer_id,
        customer_name,
        country
    from stg_customers
),
final as (
    select * from customers_keyed
)
select * from final
```

```yaml
# models/marts/schema.yml
models:
  - name: dim_customer
    description: One row per customer.
    columns:
      - name: sk_customer
        description: Surrogate key, hash of customer_id.
        tests: [unique, not_null]
```
