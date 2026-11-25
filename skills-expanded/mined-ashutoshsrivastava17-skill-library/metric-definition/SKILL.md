---
name: metric-definition
description: >
  Define business and product metrics with precise calculations, data sources,
  dimensions, and ownership. Create metric dictionaries and glossaries to
  ensure consistent measurement.
  TRIGGER when: user says /metric-definition, "define metric", "metric definition",
  "KPI definition", "metric dictionary", or "measurement spec".
argument-hint: "[metric name or domain]"
user-invocable: true
---

# Metric Definition

You are a data analyst creating precise, unambiguous metric definitions. Produce metric specifications that ensure everyone in the organization calculates and interprets metrics the same way, eliminating discrepancies between dashboards, reports, and analyses.

## Process

### Step 1: Understand the Metric Need

Gather context about what needs to be measured:

| Question | Purpose |
|----------|---------|
| What business question does this metric answer? | Ensures the metric is tied to a real decision |
| Who will use this metric and how? | Determines granularity, refresh cadence, and access needs |
| What decisions will this metric inform? | Guards against vanity metrics |
| Does a similar metric already exist? | Prevents duplication and conflicting definitions |
| What is the expected range or benchmark? | Provides sanity-check context |

### Step 2: Core Metric Specification

Define the metric precisely:

| Attribute | Definition |
|-----------|------------|
| **Metric name** | Clear, unambiguous name following naming conventions |
| **Business definition** | Plain-language description a non-technical stakeholder can understand |
| **Technical definition** | Precise formula or calculation logic |
| **Formula** | `metric = numerator / denominator` or equivalent expression |
| **Unit** | Percentage, count, currency, ratio, duration, etc. |
| **Direction** | Higher is better / Lower is better / Target range |
| **Granularity** | Per user, per transaction, per day, per cohort |
| **Time window** | Point-in-time, trailing 7-day, monthly, quarterly |
| **Aggregation method** | SUM, AVG, COUNT, MEDIAN, P95, weighted average |

### Step 3: Data Source Specification

Document where the data comes from:

| Attribute | Details |
|-----------|---------|
| Primary source table(s) | Database, schema, and table names |
| Key columns | Columns used in the calculation |
| Join logic | How tables are joined (keys, conditions) |
| Filters | Exclusions applied (e.g., test accounts, internal traffic, bots) |
| Data freshness | How frequently source data updates |
| Data lag | Expected delay between event and data availability |
| Backfill policy | Can the metric be recalculated historically? Limitations? |

Example SQL or pseudocode for the metric calculation:

```sql
SELECT
    date_trunc('day', event_timestamp) AS metric_date,
    COUNT(DISTINCT user_id) AS metric_value
FROM schema.table
WHERE event_type = 'target_event'
  AND is_test_account = FALSE
GROUP BY 1
```

### Step 4: Dimensions and Segments

Define how the metric can be sliced:

| Dimension | Source Column | Values | Purpose |
|-----------|-------------|--------|---------|
| *e.g., Platform* | `device_type` | iOS, Android, Web | Compare metric across platforms |
| *e.g., Region* | `country_code` | US, EU, APAC | Geographic performance |
| *e.g., Customer tier* | `plan_type` | Free, Pro, Enterprise | Segment by customer value |
| *e.g., Cohort* | `signup_month` | YYYY-MM | Track metric evolution by cohort |

### Step 5: Thresholds and Targets

Set performance thresholds:

| Level | Value | Response |
|-------|-------|----------|
| **Target** | *goal value* | On track; no action needed |
| **Warning** | *threshold* | Investigate; may need intervention |
| **Critical** | *threshold* | Immediate action required; escalate |

Include seasonality notes -- e.g., metric typically drops 15% in Q4 due to holidays.

### Step 6: Ownership and Governance

| Attribute | Details |
|-----------|---------|
| Metric owner | Person or team accountable for the metric definition |
| Data owner | Team responsible for data quality of the source |
| Review cadence | How often the definition is reviewed (quarterly recommended) |
| Change process | How to propose changes to the metric definition |
| Approved consumers | Which dashboards, reports, and systems use this metric |
| Version | Current version number of the definition |

## Output Format

Present the metric definition as a structured specification:

1. **Summary** -- metric name, one-line description, owner, and status (draft / approved / deprecated)
2. **Business Context** -- what question it answers and what decisions it informs
3. **Core Specification** -- formula, unit, direction, granularity, and time window
4. **Data Source** -- tables, columns, filters, and example query
5. **Dimensions** -- available slices with values and purpose
6. **Thresholds** -- target, warning, and critical levels
7. **Governance** -- ownership, review cadence, and change process
8. **Known Limitations** -- caveats, edge cases, and what the metric does NOT measure

## Quality Checklist

- [ ] Metric has a single, unambiguous formula
- [ ] Business definition is understandable by non-technical stakeholders
- [ ] Technical definition is reproducible by any analyst given the same data
- [ ] Filters and exclusions are explicitly documented (not assumed)
- [ ] Dimensions are defined with allowed values
- [ ] Thresholds are set with clear response actions
- [ ] An owner is assigned and has accepted responsibility
- [ ] The metric has been validated against a known baseline or benchmark
- [ ] Known limitations and caveats are documented

## Edge Cases

- **Metrics with multiple valid calculations**: Document each variant, name them distinctly, and specify which is the canonical version (e.g., "Revenue (booked)" vs. "Revenue (recognized)")
- **Metrics requiring data from external systems**: Document the integration point, data freshness, and fallback behavior if the external source is unavailable
- **Metrics affected by product changes**: Note when definition changes are needed due to feature launches or deprecations; maintain a version history
- **Leading vs. lagging indicators**: Clearly label the metric type and document the expected lag between action and metric movement
- **Composite metrics (ratios, indexes)**: Define each component metric independently before defining the composite; ensure component metrics are also tracked
