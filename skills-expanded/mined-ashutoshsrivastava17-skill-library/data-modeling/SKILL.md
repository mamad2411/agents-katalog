---
name: data-modeling
description: >
  Design data models using dimensional modeling (star/snowflake schemas), entity-relationship diagrams,
  naming conventions, slowly changing dimensions, and comprehensive documentation standards.
  TRIGGER when: user says /data-modeling, "design data model", "star schema", "snowflake schema",
  "dimensional model", "entity relationship", "ERD", "data warehouse design", or "fact and dimension tables".
argument-hint: "[business_domain or use_case]"
user-invocable: true
---

# Data Modeling

You are an expert data architect and modeler. When the user asks you to design a data model, follow this structured process to deliver a robust, scalable, and well-documented model.

## Step 1: Requirements Gathering

Before modeling anything, understand the business and analytical needs:

| Requirement Area | Questions to Answer |
|------------------|---------------------|
| Business process | What process is being modeled (sales, marketing, support)? |
| Grain | What does one row in the fact table represent? |
| Analytical questions | What questions must the model answer? |
| Source systems | Where does the data originate? |
| Data volume | Expected row counts (initial and growth rate) |
| Query patterns | OLAP (aggregation-heavy) or OLTP (transactional)? |
| Users | Who will query this model (analysts, BI tools, ML pipelines)? |
| SLA | Freshness requirements and acceptable query latency |

## Step 2: Modeling Approach Selection

Choose the appropriate modeling paradigm:

| Approach | Best For | Trade-offs |
|----------|----------|------------|
| Star schema | BI/analytics, simple queries | Denormalized, redundancy acceptable |
| Snowflake schema | Complex hierarchies, storage-sensitive | More joins, normalized dimensions |
| Data Vault | Auditability, multiple source integration | Complex, requires automation |
| Wide/OBT (One Big Table) | Simple analytics, small teams | Limited flexibility, high redundancy |
| Normalized (3NF) | Transactional systems, OLTP | Slow for analytical queries |
| Activity schema | Event-driven analytics | Requires event tracking infrastructure |

### Star Schema Components

```
              ┌──────────────┐
              │ dim_date     │
              └──────┬───────┘
                     │
┌──────────────┐     │     ┌──────────────┐
│ dim_customer ├─────┼─────┤ dim_product  │
└──────────────┘     │     └──────────────┘
                     │
              ┌──────┴───────┐
              │ fact_orders  │
              └──────┬───────┘
                     │
              ┌──────┴───────┐
              │ dim_channel  │
              └──────────────┘
```

## Step 3: Dimension Design

Design dimension tables with best practices:

### Dimension Table Template

| Column | Type | Description |
|--------|------|-------------|
| `dim_[entity]_key` | BIGINT (surrogate) | Primary key, auto-generated |
| `[entity]_id` | VARCHAR | Natural/business key from source |
| `[entity]_name` | VARCHAR | Human-readable label |
| `[attribute]` | Varies | Descriptive attributes |
| `[hierarchy_level]` | VARCHAR | Hierarchy groupings |
| `is_current` | BOOLEAN | SCD Type 2 current flag |
| `valid_from` | TIMESTAMP | SCD Type 2 effective start |
| `valid_to` | TIMESTAMP | SCD Type 2 effective end |
| `_loaded_at` | TIMESTAMP | ETL load timestamp |
| `_source_system` | VARCHAR | Origin system identifier |

### Slowly Changing Dimensions (SCD)

| SCD Type | Behavior | When to Use | Implementation |
|----------|----------|-------------|----------------|
| Type 0 | Never changes | Reference data (country codes) | No update logic |
| Type 1 | Overwrite | Corrections, non-historical attributes | UPDATE in place |
| Type 2 | Add new row | Historical tracking required (customer tier) | Surrogate key, valid_from/to, is_current |
| Type 3 | Add column | Track previous value only | `current_value`, `previous_value` columns |
| Type 4 | Mini-dimension | Rapidly changing attributes | Separate fast-changing dimension table |
| Type 6 | Hybrid (1+2+3) | Full flexibility | Combines overwrite, history, and previous |

## Step 4: Fact Table Design

Design fact tables with proper grain and measures:

### Fact Table Types

| Type | Grain | Example | Characteristics |
|------|-------|---------|-----------------|
| Transaction | One row per event | `fact_orders` | Most common, finest grain |
| Periodic snapshot | One row per period | `fact_monthly_balance` | Regular intervals, cumulative |
| Accumulating snapshot | One row per lifecycle | `fact_order_fulfillment` | Milestones tracked across stages |
| Factless fact | Event occurrence only | `fact_student_attendance` | No numeric measures, tracks events |

### Fact Table Template

| Column | Type | Description |
|--------|------|-------------|
| `fact_[process]_key` | BIGINT | Surrogate primary key |
| `dim_date_key` | BIGINT (FK) | Date dimension foreign key |
| `dim_[entity]_key` | BIGINT (FK) | Dimension foreign keys |
| `[measure]_amount` | DECIMAL/NUMERIC | Additive measures |
| `[measure]_count` | INTEGER | Count measures |
| `[measure]_rate` | DECIMAL | Semi-additive or derived measures |
| `_loaded_at` | TIMESTAMP | ETL load timestamp |

### Measure Additivity

| Type | Definition | Aggregation | Example |
|------|-----------|-------------|---------|
| Additive | Sums across all dimensions | SUM | Revenue, quantity |
| Semi-additive | Sums across some dimensions | SUM (except time), use LAST/AVG for time | Account balance |
| Non-additive | Cannot be summed | AVG, RATIO, or recompute | Unit price, percentage |

## Step 5: Naming Conventions and Standards

Apply consistent naming across the model:

| Element | Convention | Example |
|---------|-----------|---------|
| Fact tables | `fact_[business_process]` | `fact_orders`, `fact_page_views` |
| Dimension tables | `dim_[entity]` | `dim_customer`, `dim_product` |
| Surrogate keys | `[table]_key` | `dim_customer_key` |
| Natural keys | `[entity]_id` | `customer_id` |
| Measures | `[measure]_[unit]` | `revenue_amount`, `order_count` |
| Dates | `[event]_date` or `[event]_at` | `order_date`, `created_at` |
| Booleans | `is_[condition]` or `has_[condition]` | `is_active`, `has_subscription` |
| Metadata | `_[purpose]` (underscore prefix) | `_loaded_at`, `_source_system` |

### General Rules

- Use `snake_case` for all object names
- Avoid abbreviations unless universally understood (e.g., `id`, `qty`)
- Pluralize table names if they represent collections (`dim_customers` or `dim_customer` — pick one and be consistent)
- Prefix staging tables with `stg_`, intermediate with `int_`
- Document every column with a description

## Step 6: Documentation and Validation

Produce comprehensive model documentation:

### Entity-Relationship Diagram

Generate or describe the ERD showing:
- All tables with their columns and types
- Primary keys and foreign key relationships
- Cardinality (1:1, 1:N, M:N)
- Relationship labels

### Data Dictionary

For each table and column, document:

| Field | Content |
|-------|---------|
| Table name | Physical table name |
| Column name | Physical column name |
| Data type | SQL data type with precision |
| Nullable | YES/NO |
| Default | Default value if any |
| Description | Business definition in plain language |
| Source | Source system and field mapping |
| Transformation | Any logic applied during ETL |
| Example values | 2-3 representative values |

## Output Format

Present the data model as:

1. **Model Summary** (business process, grain, approach chosen, key design decisions)
2. **Entity-Relationship Diagram** (ASCII or mermaid diagram)
3. **Fact Table Specifications** (columns, types, measures, grain statement)
4. **Dimension Table Specifications** (columns, types, SCD strategy, hierarchies)
5. **Naming Convention Reference** (applied standards)
6. **Data Dictionary** (full column-level documentation)
7. **Source-to-Target Mapping** (source system fields to model columns)
8. **Implementation Notes** (indexing, partitioning, materialization strategy)

## Quality Checklist

Before delivering the data model, verify:

- [ ] Grain is explicitly stated for every fact table
- [ ] All dimensions have surrogate keys
- [ ] SCD strategy is defined for every dimension
- [ ] Naming conventions are consistently applied
- [ ] Every table has a primary key
- [ ] Foreign key relationships are documented
- [ ] Measure additivity is classified for every measure
- [ ] A date dimension is included and conforms to the enterprise calendar
- [ ] Data dictionary is complete for all columns

## Edge Cases

- **Multiple time zones**: Store timestamps in UTC; provide a `dim_date` with local time attributes or use a timezone dimension
- **Many-to-many relationships**: Use a bridge/associative table (e.g., `bridge_customer_account`) rather than duplicating fact rows
- **Late-arriving dimensions**: Use a placeholder/unknown dimension row (key = -1) and update via SCD Type 2 when data arrives
- **Rapidly changing dimensions**: Use Type 4 mini-dimensions to avoid fact table explosion
- **Conformed dimensions**: Ensure shared dimensions (date, customer, product) use the same keys across all fact tables
- **Hybrid source systems**: Create a staging layer that normalizes disparate sources before loading into the dimensional model
