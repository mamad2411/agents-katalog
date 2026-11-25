---
name: bi-semantic-layer-metric-trees
description: "Define normalized metric logic in headless semantic layers (Cube, dbt Semantic Layer, MetricFlow) and decompose North Star metrics into hierarchical driver trees."
category: business-intelligence
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - business-intelligence
  - semantic-layer
  - dbt
  - metric-trees
  - data-governance
---

# Metric Trees and Headless Semantic Layer Engineering

## Overview & Core Principles
Define normalized metric logic in headless semantic layers (Cube, dbt Semantic Layer, MetricFlow) and decompose North Star metrics into hierarchical driver trees.

### Metric Tree Architecture & YAML Specification
1. **Mathematical Decomposition**:
   - Top Level: ARR = Total Active Subscriptions * ARPU.
   - Tier 2 Drivers: ARPU = Base Tier Price + Expansion Revenue per Account.
   - Churn Metric: Net Revenue Retention (NRR) = (Beginning ARR + Expansion - Downgrades - Churn) / Beginning ARR.
2. **MetricFlow Semantic Manifest**:
```yaml
semantic_models:
  - name: orders
    model: ref('fct_orders')
    dimensions:
      - name: ordered_at
        type: time
        type_params:
          time_granularity: day
      - name: customer_country
        type: categorical
    measures:
      - name: gross_order_value
        agg: sum
        expr: line_total_cents / 100.0

metrics:
  - name: revenue
    type: simple
    type_params:
      measure: gross_order_value
```
3. **Consistency Verification**:
   - Metric definitions are source-controlled in Git, tested with CI assertions, and queried uniformly by BI tools and reverse-ETL.
