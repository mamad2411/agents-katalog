---
name: data-observability
description: |
  Specialized skill for establishing and monitoring data quality at the INFRASTRUCTURE level.
  Use when: setting up Great Expectations suites, Soda checks, custom SQL quality monitors, schema drift detection, or anomaly detection logic.
  Do NOT use for dbt-specific tests — use `testing-dbt-models` instead.
  Do NOT use for data freshness spot-checks — use `checking-freshness` instead.
metadata:
  author: dataops-agent
  version: "2.0.0"
---

# Data Observability

Infrastructure-level data quality monitoring. For dbt-specific tests, use `testing-dbt-models`. For quick freshness checks, use `checking-freshness`.

## When to Apply
Use this skill when:
- Implementing Great Expectations validation suites
- Setting up Soda data quality checks
- Building custom SQL anomaly detection (volume spikes, distribution shifts)
- Tracking and handling schema drift in source systems
- Establishing data quality SLAs and tiered alerting
- Monitoring data pipeline health metrics

## Scope Boundaries

| Task | Correct Skill |
|------|--------------|
| Add `not_null`, `unique` tests in schema.yml | `testing-dbt-models` |
| "Is this table fresh?" | `checking-freshness` |
| Set up Great Expectations suite | **this skill** ✅ |
| Build custom anomaly detection SQL | **this skill** ✅ |
| Schema drift monitoring | **this skill** ✅ |

## Best Practices
1. **Shift Left**: Implement quality checks as early as possible in the pipeline.
2. **Tiered Alerting**: Differentiate between "warning" anomalies and "critical" errors that should block the pipeline.
3. **Automated Profiling**: Use statistical methods to profile data and establish baseline metrics.
4. **Schema Evolution**: Implement robust schema handling for unexpected column drops/adds.

## Execution Pattern
1. Identify the critical data assets and their required SLAs/quality thresholds.
2. Generate the necessary testing logic (Great Expectations suites, Soda checks, or custom SQL quality monitors).
3. Provide recommendations on how to integrate the checks into the orchestrator.
