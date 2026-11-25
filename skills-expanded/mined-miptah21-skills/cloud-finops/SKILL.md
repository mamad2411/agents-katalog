---
name: cloud-finops
description: |
  Specialized skill for optimizing cloud data INFRASTRUCTURE costs and resource utilization at the platform level.
  Use when: rightsizing warehouses, configuring auto-suspend policies, optimizing storage formats, setting budget alerts, or forecasting cloud spend.
  Do NOT use for query-level cost analysis — use `finding-expensive-queries` instead.
  Do NOT use for optimizing individual SQL queries — use `optimizing-query-text` or `optimizing-query-by-id` instead.
metadata:
  author: dataops-agent
  version: "2.0.0"
---

# Cloud FinOps for Data Infrastructure

Platform-level cost optimization. For query-level cost analysis, use `finding-expensive-queries`. For SQL optimization, use `optimizing-query-text`.

## When to Apply
Use this skill when:
- Rightsizing Snowflake warehouses (XS → XL) and scaling policies
- Configuring auto-suspend/auto-resume policies
- Evaluating storage formats (Parquet, Iceberg, Delta) for cost impact
- Setting up budget alerts and cost anomaly detection
- Forecasting cloud spend for data platforms
- Comparing pricing models (on-demand vs reserved, standard vs enterprise)
- Implementing resource tagging/attribution for cost allocation

## Scope Boundaries

| Task | Correct Skill |
|------|--------------|
| "Find our most expensive queries" | `finding-expensive-queries` |
| "Optimize this slow query" | `optimizing-query-text` |
| "Our warehouse costs are too high" | **this skill** ✅ |
| "Should we upsize the warehouse?" | **this skill** ✅ |
| "Set up budget alerts" | **this skill** ✅ |

## Best Practices
1. **Attribution**: Ensure all resources are tagged to attribute costs to teams/products.
2. **Warehouse Suspend/Resume**: Configure aggressive auto-suspend policies for unused compute.
3. **Storage vs. Compute**: Optimize data formats and partitioning to reduce bytes scanned.
4. **Continuous Monitoring**: Set budget alerts and threshold limits.

## Execution Pattern
1. Analyze the infrastructure configuration or query cost patterns.
2. Identify wasted resources or inefficient scaling policies.
3. Provide actionable recommendations and configuration code to reduce costs.
