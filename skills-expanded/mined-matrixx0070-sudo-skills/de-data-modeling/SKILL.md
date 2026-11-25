---
name: de-data-modeling
version: 1.0.0
description: Model a warehouse schema — choose star vs snowflake, declare grain, and design slowly-changing dimensions.
author: matrixx0070
tags: [data-engineering, data-modeling, warehouse, dimensional, scd]
capabilities: []
---

# de-data-modeling

## When to use

Use this when designing the analytical schema of a warehouse: which tables are facts, which are dimensions, what one row means, and how history is tracked. Do this before writing marts.

**Not for:** designing the ingestion pipeline (use de-pipeline-design), implementing the models in dbt (use de-dbt-transform), OLTP/normalized app schemas, or ad-hoc analysis (use data-analyze).

## Method

1. **Identify the business process** the fact table records (an order, a shipment, a page view). One process per fact table.
2. **Declare the grain in one sentence** — "one row per order line item." Everything downstream is checked against this. Decision point: if two metrics need different grains, they need two fact tables.
3. **Choose measures and dimensions.** Measures are the numeric, additive facts. Dimensions are the descriptive context (who/what/when/where) you filter and group by.
4. **Star vs snowflake.** Default to star (denormalized dimensions) for query simplicity and BI-tool friendliness. Snowflake (normalized dimension hierarchies) only when a dimension is huge, shared, and its attributes churn independently.
5. **Design each dimension's history strategy (SCD):** Type 1 (overwrite, no history), Type 2 (new row per change with valid_from/valid_to + is_current), or Type 3 (previous-value column). Decision point: if analysts must reproduce "state as of the transaction date," use Type 2.
6. **Add surrogate keys** on dimensions (a warehouse-generated integer/hash), and reference them from facts — never join on mutable natural keys, especially with Type 2.

## Example

Grain: one row per order line item.

```
fact_order_line (
  order_line_sk,        -- surrogate PK
  customer_sk,          -- FK → dim_customer (SCD2)
  product_sk,           -- FK → dim_product  (SCD1)
  date_sk,              -- FK → dim_date
  quantity, unit_price, line_amount   -- additive measures
)

dim_customer (         -- SCD Type 2
  customer_sk PK, customer_id,        -- natural key
  segment, region,
  valid_from, valid_to, is_current
)
```

A customer moving from SMB to Enterprise gets a new `customer_sk` row; old order lines still point at the SMB version, so history is preserved.

## Pitfalls

- Mixed grain: stuffing order-level and line-level measures in one fact, so sums double-count.
- Joining facts on natural keys, which breaks the moment a dimension goes SCD2.
- Type-1 overwriting a dimension analysts need history on, silently rewriting the past.
- Over-snowflaking every dimension, forcing 6-way joins for a simple report.

## Output format

```
Process:   <business event>
Grain:     one row per <...>
Fact:      <fact_name> — measures: <...> | dims (FKs): <...>
Dimensions:<dim_name> — SCD Type <1|2|3> — key: <surrogate + natural>
Shape:     star | snowflake  (+ why)
Notes:     conformed dims shared across facts: <...>
```
