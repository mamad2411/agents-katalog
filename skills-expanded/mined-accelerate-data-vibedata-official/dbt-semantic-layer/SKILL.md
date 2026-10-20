---
name: dbt-semantic-layer
description: >
  Define semantic models and MetricFlow metrics in dbt on Microsoft Fabric.
  Use when creating semantic model YAML, defining entities, dimensions, and
  measures, or configuring metric types. Also use when choosing between
  denormalized marts and semantic layer queries.
tools: Read, Write, Edit, Glob, Grep, Bash
type: platform
domain: dbt Semantic Layer on Fabric
version: 1.0.0
---

# dbt Semantic Layer on Fabric

Practitioner patterns for defining semantic models and MetricFlow metrics in dbt on Microsoft Fabric. Focuses on what LLMs consistently get wrong: entity type selection, metric type decisions, join path design, and the semantic layer vs denormalized mart trade-off.

## Quick Reference

### When semantic layer vs denormalized mart

This is not "it depends." Use these concrete criteria:

| Signal | Use semantic layer | Use denormalized mart |
|---|---|---|
| Metric consumed by 3+ tools (BI, notebooks, APIs) | Yes -- single definition, multiple consumers | No |
| Metric needs flexible dimensionality (different group-bys per consumer) | Yes -- MetricFlow composes joins dynamically | No |
| One dashboard with fixed dimensions | No -- overkill | Yes -- simpler, faster |
| Metric requires cross-model joins (orders + customers + products) | Yes -- MetricFlow handles join paths | Possible but creates wide, fragile tables |
| Team has no dbt Cloud (SL API requires Cloud) | Partial -- `dbt sl query` works locally, no API | Yes -- only option for ad-hoc BI |
| Source models change schema frequently | Yes -- metric definitions absorb changes | No -- every mart must be updated |
| Need percentile/median aggregations on Fabric | No -- see Fabric limitations below | Yes -- compute in the mart SQL directly |

**Default rule**: If the metric is consumed in more than one place, define it in the semantic layer. If it's a one-off dashboard column, a mart is fine.

### Star schema preservation principle

Keep marts normalized (separate `fct_` and `dim_` tables). Let MetricFlow denormalize dynamically at query time. This:
- Eliminates redundant wide tables that duplicate dimension columns across facts
- Lets MetricFlow pick optimal join paths per query
- Reduces storage and maintenance (one `dim_customers` instead of customer columns copied into every fact)

**Anti-pattern**: Building `fct_orders_with_customers_and_products` as a pre-joined wide mart when you also have semantic models. This creates two sources of truth.

### Entity type decision

| Entity type | Guarantees | Use when |
|---|---|---|
| `primary` | Exactly one row per value, no nulls | The column is the grain of the model (e.g., `order_id` in `fct_orders`) |
| `unique` | At most one row per value, nulls allowed | The column uniquely identifies rows but may have nulls (e.g., `email` in `dim_customers`) |
| `foreign` | Multiple rows per value allowed | The column references a primary/unique entity in another model (e.g., `customer_id` in `fct_orders`) |
| `natural` | No uniqueness guarantee | Shared business concept without enforced cardinality (rarely used -- prefer foreign + primary pair) |

**Common mistake**: Using `primary` for a foreign key column. If `customer_id` appears in `fct_orders` (many orders per customer), it must be `foreign`, not `primary`. MetricFlow uses entity types to determine join cardinality -- wrong types produce incorrect joins or fan-out errors.

### Semantic model YAML structure

Every semantic model needs these four sections:

```yaml
semantic_models:
  - name: orders                    # Must match a dbt model
    description: "Order fact table. Grain: one row per order."
    model: ref('fct_orders')        # Points to the dbt model
    defaults:
      agg_time_dimension: order_date  # Required -- MetricFlow needs a time spine

    entities:
      - name: order_id
        type: primary               # Grain of this model
      - name: customer_id
        type: foreign               # FK to dim_customers
        expr: customer_id           # Optional if name matches column

    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day      # Controls minimum query grain
      - name: order_status
        type: categorical

    measures:
      - name: order_total
        description: "Sum of order amounts"
        agg: sum
        expr: amount                 # SQL expression or column name
      - name: order_count
        agg: sum
        expr: "1"                    # Count pattern: sum of literal 1
```

**Key rules**:
- `defaults.agg_time_dimension` is required. Without it, MetricFlow cannot place metrics on a time axis.
- Every semantic model must have exactly one `primary` entity.
- `expr` on measures accepts any valid SQL expression, including `CASE WHEN` for conditional aggregations.
- Dimension names must not collide across semantic models that share an entity -- MetricFlow uses `entity__dimension` syntax to disambiguate.

### Aggregation types available

| Aggregation | T-SQL compatible | Notes |
|---|---|---|
| `sum` | Yes | Most common |
| `average` / `avg` | Yes | |
| `count_distinct` | Yes | |
| `min` / `max` | Yes | |
| `sum_boolean` | Yes | Sums a boolean/bit column |
| `count` | Yes | Counts non-null values |
| `percentile` | **No on Fabric** | Requires `PERCENTILE_CONT` -- see Fabric limitations |
| `median` | **No on Fabric** | Syntactic sugar for 50th percentile |

### Fabric-specific limitations

The dbt Semantic Layer (via dbt Cloud API) does **not** officially support Fabric as a query platform. However, you can still define semantic models and metrics in a dbt-fabric project and query them locally via `dbt sl query`. Limitations:

1. **No hosted Semantic Layer API**: Fabric is not a supported platform for the dbt Semantic Layer cloud service. Metrics are queryable only via `dbt sl query` (CLI) or by materializing via saved query exports.
2. **Percentile/median aggregations**: MetricFlow generates `PERCENTILE_CONT` SQL, which Fabric's T-SQL does not support. Use a measure with `expr` containing a manual workaround or compute percentiles in the mart model instead.
3. **No `QUALIFY`**: MetricFlow may generate `QUALIFY` clauses for certain filter operations. Fabric does not support `QUALIFY` -- if you hit this, file a bug or restructure the metric to avoid the pattern.
4. **Boolean type**: T-SQL has no native boolean. `sum_boolean` measures should reference `BIT` columns (0/1), not `TRUE`/`FALSE` literals.
5. **String functions in `expr`**: Use T-SQL syntax (`LEN()`, `CHARINDEX()`, `ISNULL()`) not Postgres/Snowflake syntax (`LENGTH()`, `POSITION()`, `COALESCE()` for two-arg).
6. **Saved query exports**: You can materialize metrics as tables/views via exports. On Fabric, export to the warehouse endpoint (not the SQL analytics endpoint, which is read-only).

### Saved query exports -- materializing metrics

When the Semantic Layer API is not available (Fabric), use saved query exports to materialize metrics as tables:

```yaml
saved_queries:
  - name: monthly_revenue_by_customer
    description: "Revenue metrics grouped by customer and month"
    query_params:
      metrics:
        - revenue
        - order_count
      group_by:
        - TimeDimension('metric_time', 'month')
        - Dimension('customer__customer_segment')
      where:
        - "{{ TimeDimension('metric_time', 'month') }} >= '2024-01-01'"
    exports:
      - name: monthly_revenue_export
        config:
          export_as: table            # or 'view'
          schema: gold                # Target schema on Fabric
```

Run with `dbt build --select saved_queries` to materialize. This bridges the gap when the full Semantic Layer API is unavailable.

## Anti-patterns

What LLMs consistently get wrong with dbt semantic models and metrics:

- **Defining metrics on staging models** -- Semantic models should point to marts (`fct_`/`dim_`), not `stg_` models. Staging models are 1:1 with sources and lack business logic.
- **Wrong entity type on foreign keys** -- Using `primary` on a column that has many rows per value. MetricFlow will reject the join or produce incorrect results.
- **Duplicate metric definitions** -- Defining the same metric as both a measure with `create_metric: true` AND a separate metric block. Pick one.
- **Missing `agg_time_dimension`** -- Every semantic model needs a default time dimension. Without it, time-series queries fail.
- **Over-denormalized marts alongside semantic layer** -- Building wide pre-joined tables when MetricFlow can compose the same joins dynamically. Creates maintenance burden and metric drift.
- **Using `natural` entity type by default** -- Natural entities provide no join guarantees. Use `foreign` + `primary` pairs for predictable joins.
- **Postgres/Snowflake SQL in `expr`** -- Using `||` for concatenation, `INTERVAL` for date math, or `::` for casting in measure/dimension expressions. These fail on Fabric.
- **Conversion metrics without proper entity alignment** -- The `entity` in a conversion metric must exist in both the base and conversion semantic models. Mismatched entities produce empty results.

## Reference Files

For deeper guidance on specific patterns:

- **[references/semantic-models.md](references/semantic-models.md)** -- Entity relationship configuration, join paths, multi-hop joins, dimension types, measure expressions, and semantic model design patterns.
- **[references/metric-patterns.md](references/metric-patterns.md)** -- MetricFlow metric types (simple, ratio, derived, cumulative, conversion), decision framework for selecting types, filters, and advanced patterns.
- **[references/evaluations.md](references/evaluations.md)** -- Evaluation scenarios for testing skill effectiveness.
