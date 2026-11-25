---
name: kpi-design
description: "When to activate: KPI, metrics, OKR, dashboard, leading indicator, lagging indicator, measurement framework, performance tracking, north star metric"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: business-ops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# KPI Design

## KPI Selection Framework

### The 5-Question Test for Each KPI
```
1. Does it measure progress toward a specific goal?
2. Can we collect the data reliably and consistently?
3. Can the team take action based on this number?
4. Does it avoid perverse incentives (Goodhart's Law)?
5. Is it understood the same way by everyone who reads it?

Reject any KPI that fails 2+ of these tests.
```

### North Star Metric
```
One metric that best captures the core value delivered to customers.

Examples by business type:
  SaaS productivity:    Weekly Active Teams
  Marketplace:          Gross Merchandise Value
  Social platform:      Daily Active Users
  Developer tools:      Repositories with ≥1 CI run/week
  E-commerce:           Monthly Orders from Returning Customers
  Consumer subscription: Paid Subscribers Retained ≥ 90 Days

Criteria for North Star:
  ✓ Correlates with long-term revenue
  ✓ Reflects customer value (not just internal activity)
  ✓ Can be influenced by multiple teams
  ✓ Simple enough to be memorized
```

---

## KPI Hierarchy (Three Levels)

```
Level 1: Company KPIs (CEO/Board)
  → North Star, ARR, Gross Margin, EBITDA, NPS

Level 2: Functional KPIs (VP/Director)
  → Sales: Pipeline, Win Rate, ACV, Cycle Time
  → Marketing: MQLs, CPL, MQL→SQL, CAC
  → Product: DAU/MAU, Feature Adoption, TTFV
  → CS: NRR, GRR, Churn Rate, CSAT

Level 3: Team KPIs (Manager/Individual)
  → AE: Quota Attainment, Activities, Pipeline Coverage
  → SDR: Meetings Booked, Connect Rate, Sequences
  → Engineer: Deployment Frequency, PR Cycle Time
```

---

## Leading vs Lagging Indicators

```
Function    | Lagging (outcome)        | Leading (predictor)
------------|--------------------------|---------------------------
Sales       | Revenue closed           | Pipeline created, Activities
Marketing   | CAC, Revenue influenced  | MQLs, Website traffic, ICP fit
CS          | Churn, NRR               | Health score, Logins, CSAT
Product     | MAU, Retention           | Feature adoption rate, D7 retention
Engineering | Bug rate, Uptime         | Code review cycle time, Test coverage
Finance     | Cash balance, Burn       | Bookings, AR aging, Invoice backlog
```

**Rule**: Track 2–3 leading indicators per lagging indicator. Lagging tells you what happened; leading tells you where you're heading.

---

## KPI Tree

### Revenue KPI Tree (SaaS)
```
ARR
├── New ARR
│   ├── Leads Generated
│   │   ├── Inbound (content, SEO, brand)
│   │   └── Outbound (sequences, events)
│   ├── MQL → SQL Conversion Rate
│   ├── SQL → Opportunity Rate
│   ├── Win Rate
│   └── Average Contract Value (ACV)
│
└── Net Revenue Retention
    ├── Gross Revenue Retention
    │   ├── Logo Churn Rate
    │   └── Revenue per churned customer
    └── Expansion Revenue
        ├── Upsell Rate
        └── Cross-sell Rate
```

---

## Dashboard Design Principles

### Layout Rules
```
Top Row: 3–4 headline numbers (North Star + primary KPIs)
Middle: Trend charts (12-month history + target line)
Bottom: Drill-down tables or segment breakdowns

Color coding:
  Green  = At or above target
  Yellow = 90–99% of target
  Red    = Below 90% of target
  Grey   = Not yet measurable (new KPI)
```

### Refresh Cadence
```
Real-time:    Operational alerts (uptime, error rates, support queue)
Daily:        Activity metrics (logins, tickets, tasks)
Weekly:       Progress metrics (pipeline, MQLs, feature adoption)
Monthly:      Business metrics (ARR, churn, CAC, NRR)
Quarterly:    Strategic metrics (NPS, competitive position, market share)
```

---

## Target-Setting Methods

### Top-Down (Investor / Board driven)
```
Start with: Growth rate required for next fundraise
Work back:  ARR target → Win rate required → Pipeline needed → Leads needed
Risk:       May be disconnected from operational reality
Fix:        Validate bottleneck-by-bottleneck with team
```

### Bottom-Up (Team driven)
```
Start with: Capacity (headcount, budget, tools)
Build up:   Activities → Conversion rates → Outcomes
Risk:       May sandbag; anchors to past performance
Fix:        Apply 20–30% stretch; benchmark against industry peers
```

### Benchmark-Based
```
Industry benchmarks (SaaS, 2024):
  Outbound connect rate:     8–12%
  MQL → SQL conversion:      20–30%
  Demo → Opportunity:        50–70%
  Win rate (enterprise):     25–35%
  Win rate (SMB):            15–25%
  Support CSAT:              90–95%
  NPS (software):            30–50
  Annual churn (SMB SaaS):   10–20%

Source: SaaStr, ChartMogul, Gainsight benchmarks
```

---

## Data Availability Assessment

Before committing to a KPI, answer:
```
1. Where does this data live? (CRM, database, analytics tool, spreadsheet)
2. How is it captured? (automatic vs manual)
3. How often is it updated? (real-time, daily, weekly, manual)
4. Who owns the data quality? (named person)
5. Are there definition inconsistencies? (e.g., is "active user" defined identically across teams?)
6. What is the latency? (time between event and data availability)
7. What's the error rate? (estimated % of incorrect records)

Only publish a KPI on a dashboard if: 1–4 are answered, 5–6 are documented.
```

---

## Review Cadence Template

### Weekly KPI Review (30 min, team)
```
Agenda:
  1. Review dashboard (10 min) — what changed vs last week
  2. Anomalies and root cause (10 min) — anything unexpected?
  3. Forecast update (5 min) — are we on track for monthly target?
  4. Actions (5 min) — specific changes to make this week

No reporting theater: if everything is green, end in 15 minutes.
```

### Monthly Business Review (MBR)
```
1. Prior month actuals vs targets (with variance explanation)
2. Rolling 3-month trends by function
3. Year-to-date vs annual plan
4. Forecast for next 30/60/90 days
5. Top 3 issues + owners + resolution dates
6. Top 3 wins + what caused them
```

---

## KPI Definition Template

```yaml
KPI: Net Revenue Retention (NRR)

Definition: Percentage of recurring revenue retained from existing customers
  including expansion, contraction, and churn over a 12-month period.

Formula: (Beginning ARR + Expansion ARR - Churned ARR - Contracted ARR)
  / Beginning ARR × 100

Included: All ARR from customers active at start of period
Excluded: New logo revenue; one-time fees; professional services

Owner: VP Customer Success
Data Source: Salesforce (subscription objects) + ChartMogul
Refresh: Monthly, within 5 business days of month close
Target: ≥ 115% (FY2025)
Reported to: Board, CEO, all VPs

Calculation notes:
  - Use beginning-of-period ARR (Jan 1 for annual)
  - Expansion = upsell + cross-sell signed in period
  - Churn = cancellations effective in period
  - Contraction = downgrade ARR effective in period
```
