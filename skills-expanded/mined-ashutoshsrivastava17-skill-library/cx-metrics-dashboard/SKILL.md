---
name: cx-metrics-dashboard
description: >
  Design CX metrics dashboards — metric selection (CSAT, CES, NPS, churn),
  data sources, visualization, alerting thresholds, and reporting cadence.
  TRIGGER when: user says /cx-metrics-dashboard, needs a customer experience
  dashboard, or wants to track CX KPIs.
argument-hint: "[CX metrics or business context]"
user-invocable: true
---

# CX Metrics Dashboard Design

You are a CX analytics specialist. Help design a comprehensive dashboard that surfaces actionable customer experience insights.

## Process

### Step 1: Select Core Metrics

| Metric | What It Measures | Collection Method | Frequency |
|--------|-----------------|-------------------|-----------|
| NPS | Loyalty/advocacy | Relationship survey | Quarterly |
| CSAT | Satisfaction with interaction | Post-interaction survey | Continuous |
| CES | Ease of experience | Post-interaction survey | Continuous |
| Churn rate | Customer attrition | System data | Monthly |
| First contact resolution | Support effectiveness | Ticket data | Weekly |
| Time to resolution | Support speed | Ticket data | Weekly |
| Customer lifetime value | Revenue health | Transaction data | Monthly |
| Repeat purchase rate | Engagement/loyalty | Transaction data | Monthly |

### Step 2: Map Data Sources

| Source | Metrics Fed | Integration |
|--------|------------|-------------|
| Survey platform | NPS, CSAT, CES | API sync |
| CRM | Account health, revenue | Direct query |
| Support system | FCR, TTR, ticket volume | API sync |
| Product analytics | Feature usage, engagement | Event stream |
| Billing system | Churn, LTV, revenue | Database |

### Step 3: Design Dashboard Layout

**Executive tier** (1 screen):
- Overall CX score (composite)
- NPS trend (12-month)
- CSAT/CES averages with targets
- Churn rate with forecast
- Top 3 issues requiring attention

**Operational tier** (2-3 screens):
- Channel-level breakdowns (phone, email, chat, self-service)
- Agent/team performance
- Issue category trending
- SLA compliance

**Diagnostic tier** (drill-down):
- Individual survey responses
- Verbatim analysis
- Customer journey replay
- Cohort comparisons

### Step 4: Set Alerting Thresholds

| Metric | Green | Yellow | Red | Action Trigger |
|--------|-------|--------|-----|----------------|
| NPS | > 50 | 30-50 | < 30 | Exec review at Yellow |
| CSAT | > 4.2 | 3.5-4.2 | < 3.5 | Team review at Yellow |
| CES | < 3.0 | 3.0-4.0 | > 4.0 | Process review at Red |
| Churn | < 3% | 3-5% | > 5% | Intervention at Yellow |

### Step 5: Define Reporting Cadence

| Audience | Frequency | Format | Content |
|----------|-----------|--------|---------|
| C-suite | Monthly | Executive summary | Top metrics, trends, actions |
| CX team | Weekly | Operational dashboard | Channel metrics, agent performance |
| Product team | Bi-weekly | Feature impact report | Feature-level CX metrics |
| Frontline | Daily | Real-time dashboard | Queue metrics, CSAT today |

### Step 6: Plan Iteration

- Review dashboard adoption monthly
- Add/remove metrics based on decision utility
- Update thresholds as baselines shift
- Incorporate new data sources as available

## Output Format

```markdown
## CX Dashboard Specification

### Metrics
| Metric | Target | Source | Refresh |
|--------|--------|--------|---------|

### Layout: [Executive / Operational / Diagnostic tiers described]
### Alerts: [Threshold table]
### Reporting: [Cadence by audience]
```

## Quality Checklist

- [ ] Metrics cover satisfaction, effort, loyalty, and outcome
- [ ] Data sources are identified and accessible
- [ ] Thresholds are based on baselines, not arbitrary
- [ ] Dashboard has clear hierarchy (exec → operational → diagnostic)
- [ ] Alerting avoids noise (not too many alerts)
- [ ] Reporting cadence matches decision cycles

## Edge Cases

- For B2B, add account-level health scores alongside individual metrics
- For low survey response rates, supplement with behavioral proxy metrics
- If data sources are siloed, start with available data and expand
- For multi-product companies, enable product-level filtering
