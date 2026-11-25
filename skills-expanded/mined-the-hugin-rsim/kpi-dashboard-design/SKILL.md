---
name: kpi-dashboard-design
description: KPI framework for business dashboards — metric selection, hierarchy (strategic/tactical/operational), SQL templates for MRR/retention, Streamlit examples. Use when designing or reviewing business dashboards and metrics.
group: domain
triggers:
  - "KPI дашборд"
  - "метрики бизнеса"
  - "MRR"
  - "дашборд метрики"
  - "бизнес аналитика дашборд"
output: "KPI framework, metric definitions, SQL queries, dashboard layout recommendations"
calls: []
---

# KPI Dashboard Design

Framework for building effective business dashboards that drive decisions.

## When to Activate

- Designing or reviewing business dashboards
- Selecting KPIs for a product/department
- Writing SQL for business metrics (MRR, churn, retention)
- Creating Streamlit/data visualization dashboards

## Core Principle: SMART KPIs

Metrics must be **Specific, Measurable, Achievable, Relevant, Time-bound**.

**Limit: 5–7 KPIs per dashboard.** More = noise.

## Dashboard Hierarchy

| Level | Audience | Cadence | Focus |
|---|---|---|---|
| Strategic | C-level | Monthly/Quarterly | ARR, NPS, gross margin |
| Tactical | Managers | Weekly/Monthly | CAC, conversion, churn |
| Operational | Teams | Real-time/Daily | DAU, error rate, queue depth |

## KPIs by Department

### Sales
- MRR / ARR (absolute + growth rate)
- Win rate, average deal size
- Sales cycle length
- Pipeline coverage ratio

### Marketing
- Customer Acquisition Cost (CAC)
- Lead → MQL → SQL → Close conversion funnel
- Channel attribution (by revenue)
- Payback period

### Product
- DAU / MAU (and DAU/MAU ratio)
- Feature adoption rate
- NPS / CSAT
- Churn rate (user-level and revenue-level)

### Finance
- Gross margin %
- Operating expense ratio
- Cash runway
- LTV:CAC ratio

## SQL Templates

### MRR Calculation

```sql
WITH monthly_revenue AS (
  SELECT
    DATE_TRUNC('month', subscription_start) AS month,
    SUM(monthly_amount) AS mrr
  FROM subscriptions
  WHERE status = 'active'
  GROUP BY 1
)
SELECT
  month,
  mrr,
  mrr - LAG(mrr) OVER (ORDER BY month) AS mrr_change,
  ROUND(100.0 * (mrr - LAG(mrr) OVER (ORDER BY month)) / NULLIF(LAG(mrr) OVER (ORDER BY month), 0), 1) AS mrr_growth_pct
FROM monthly_revenue
ORDER BY month DESC;
```

### Cohort Retention

```sql
WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('month', first_active_date) AS cohort_month
  FROM users
),
activity AS (
  SELECT DISTINCT
    user_id,
    DATE_TRUNC('month', event_date) AS activity_month
  FROM events
)
SELECT
  c.cohort_month,
  COUNT(DISTINCT c.user_id) AS cohort_size,
  COUNT(DISTINCT a.user_id) AS retained,
  ROUND(100.0 * COUNT(DISTINCT a.user_id) / COUNT(DISTINCT c.user_id), 1) AS retention_pct,
  EXTRACT(MONTH FROM AGE(a.activity_month, c.cohort_month)) AS months_since_join
FROM cohorts c
LEFT JOIN activity a ON c.user_id = a.user_id
GROUP BY 1, 5
ORDER BY 1, 5;
```

### Churn Rate

```sql
SELECT
  DATE_TRUNC('month', cancelled_at) AS month,
  COUNT(*) AS churned,
  ROUND(100.0 * COUNT(*) / (
    SELECT COUNT(*) FROM subscriptions
    WHERE status = 'active'
      AND created_at < DATE_TRUNC('month', s.cancelled_at)
  ), 2) AS churn_rate_pct
FROM subscriptions s
WHERE cancelled_at IS NOT NULL
GROUP BY 1
ORDER BY 1 DESC;
```

## Dashboard Layout Templates

### Executive Summary (4–6 KPIs)

```
┌─────────────────────────────────────────────────────────┐
│  MRR: $124K  ↑8%  │  Churn: 2.1%  ↓0.3%  │  NPS: 62  │
│  CAC: $420   ↑5%  │  LTV:CAC: 4.2x        │           │
├─────────────────────────────────────────────────────────┤
│  [MRR trend 12m]        │  [Cohort retention heatmap]  │
└─────────────────────────────────────────────────────────┘
```

### Streamlit Metric Card Example

```python
import streamlit as st
import pandas as pd

def metric_card(label: str, value: str, delta: str, delta_color: str = "normal"):
    st.metric(label=label, value=value, delta=delta, delta_color=delta_color)

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("MRR", "$124K", "+8% MoM")
with col2:
    metric_card("Churn Rate", "2.1%", "-0.3%", delta_color="inverse")
with col3:
    metric_card("CAC", "$420", "+5%", delta_color="inverse")
with col4:
    metric_card("NPS", "62", "+4pts")

# Trend chart
st.line_chart(df.set_index('month')[['mrr']])

# Retention heatmap
import plotly.graph_objects as go
fig = go.Figure(data=go.Heatmap(z=retention_matrix, colorscale='Blues'))
st.plotly_chart(fig)
```

## Best Practices

| Do | Don't |
|---|---|
| Show trend + absolute value | Show absolute value alone |
| Compare to target or prior period | Show raw numbers without context |
| Enable drilldown (summary → detail) | Cram 15 KPIs on one screen |
| Use consistent color conventions (red=bad) | Use 3D pie charts |
| Document metric definitions | Leave ambiguous calculations |
| Highlight anomalies automatically | Rely on users to spot outliers |
