---
name: kpi-definition
description: >
  Define KPIs with structured methodology: metric selection, leading vs lagging indicators, target setting,
  measurement methodology, data sources, and governance frameworks for consistent organizational alignment.
  TRIGGER when: user says /kpi-definition, "define KPIs", "key performance indicators", "metric selection",
  "set targets", "measurement framework", "KPI governance", or "what should we measure".
argument-hint: "[business_area or objective]"
user-invocable: true
---

# KPI Definition

You are an expert analytics strategist. When the user asks you to define KPIs, follow this structured process to deliver a comprehensive, measurable, and actionable KPI framework.

## Step 1: Business Context Discovery

Before defining any metrics, understand the strategic landscape:

| Discovery Area | Questions to Answer |
|----------------|---------------------|
| Business objective | What is the primary goal this KPI supports? |
| Stakeholders | Who will consume and act on this metric? |
| Decision context | What decisions will this KPI inform? |
| Time horizon | Short-term (weekly), medium (monthly), or long-term (quarterly/annual)? |
| Current state | Are there existing metrics? What is being tracked today? |
| Maturity level | Does the org have data infrastructure and reporting culture? |

## Step 2: Metric Selection and Classification

Categorize each proposed KPI systematically:

### Leading vs Lagging Indicators

| Type | Definition | Example | Use Case |
|------|-----------|---------|----------|
| Leading | Predictive, forward-looking | Pipeline velocity, feature adoption rate | Early warning, proactive action |
| Lagging | Outcome-based, backward-looking | Revenue, churn rate, NPS | Performance validation, reporting |
| Coincident | Real-time operational | Active users, server uptime | Monitoring, immediate response |

### Metric Quality Assessment

For each candidate KPI, evaluate:

- **Specific**: Does it measure exactly one thing?
- **Measurable**: Can it be quantified with available data?
- **Actionable**: Can the team influence this metric?
- **Relevant**: Does it connect to the stated objective?
- **Time-bound**: Is there a defined measurement period?
- **Comparable**: Can it be benchmarked against peers or past performance?

## Step 3: Target Setting

Define targets using a structured framework:

| Target Component | Description |
|------------------|-------------|
| Baseline | Current performance level (last 3-6 months average) |
| Benchmark | Industry or peer comparison |
| Stretch target | Ambitious but achievable (top quartile) |
| Minimum threshold | Below this triggers escalation or review |
| Target | Expected performance (50th-75th percentile improvement) |
| Cadence | How often the target is evaluated and reset |

### Target-Setting Methods

- **Historical trending**: Extrapolate from past performance with improvement factor
- **Benchmarking**: Use industry standards (e.g., SaaS benchmarks for churn, CAC)
- **Top-down allocation**: Break company goals into team-level targets
- **Bottom-up modeling**: Aggregate team capacity into achievable targets
- **OKR alignment**: Derive from quarterly Objectives and Key Results

## Step 4: Measurement Methodology

Document how each KPI is calculated:

```
KPI Name: [Name]
Formula: [Numerator] / [Denominator] * [Multiplier if %]
Data Source(s): [System(s) of record]
Granularity: [Daily / Weekly / Monthly]
Segmentation: [By region, product, team, cohort]
Filters/Exclusions: [What is excluded and why]
Refresh Frequency: [Real-time / Daily / Weekly]
Owner: [Team or individual responsible]
```

### Common Pitfalls to Avoid

- Vanity metrics that look good but do not drive action
- Metrics that can be gamed without improving outcomes
- Too many KPIs (recommend 5-7 per team/domain)
- Metrics without clear ownership
- Lagging-only frameworks with no leading indicators

## Step 5: Data Source Mapping

Identify and validate data sources for each KPI:

| Data Layer | Examples | Considerations |
|------------|----------|----------------|
| Source systems | CRM, ERP, product analytics, billing | Data freshness, API availability |
| Data warehouse | Snowflake, BigQuery, Redshift | Transformation logic, latency |
| Semantic layer | Looker, dbt metrics, Cube.js | Consistent definitions, version control |
| Presentation | Dashboard tool, spreadsheet, API | Access controls, refresh cadence |

## Step 6: Governance Framework

Establish ongoing KPI management:

| Governance Element | Detail |
|--------------------|--------|
| Definition owner | Who maintains the metric definition |
| Data steward | Who ensures data quality |
| Review cadence | Quarterly KPI review and pruning |
| Change process | How KPI definitions are updated |
| Documentation | Central metric dictionary location |
| Audit trail | Version history of definition changes |
| Retirement criteria | When and how to sunset a KPI |

## Output Format

Present the KPI framework as:

1. **Executive Summary** (objective, audience, time horizon)
2. **KPI Inventory Table** (name, type, formula, target, owner, data source)
3. **Leading/Lagging Balance Map** (visual or tabular representation)
4. **Target Summary** (baseline, target, stretch, threshold per KPI)
5. **Measurement Specifications** (detailed calculation for each KPI)
6. **Data Source Architecture** (source-to-dashboard lineage)
7. **Governance Plan** (ownership, review cadence, change process)
8. **Implementation Roadmap** (phased rollout with dependencies)

## Quality Checklist

Before delivering the KPI framework, verify:

- [ ] Each KPI ties directly to a stated business objective
- [ ] Mix of leading and lagging indicators is present
- [ ] Targets have baselines and are grounded in data
- [ ] Formulas are unambiguous and reproducible
- [ ] Data sources are identified and accessible
- [ ] No more than 7 KPIs per team or domain
- [ ] Every KPI has a named owner
- [ ] Governance and review cadence is defined
- [ ] Edge cases and exclusions are documented

## Edge Cases

- **New business with no baseline**: Use industry benchmarks; set 90-day data collection phase before finalizing targets
- **Cross-functional KPIs**: Assign a single accountable owner even when multiple teams contribute
- **Conflicting metrics**: Surface trade-offs explicitly (e.g., speed vs quality) and establish priority
- **Data not yet available**: Mark as "aspirational KPI" with a data infrastructure prerequisite
- **Seasonal businesses**: Use year-over-year comparisons rather than month-over-month
- **Acquired companies**: Reconcile metric definitions before merging KPI frameworks
