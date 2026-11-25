---
name: kpi-dashboard
description: "Sets up KPI tracking dashboards in Notion with metrics, targets, status indicators, and trend tracking for any business type. Use when a user wants to track business performance, needs a visual dashboard for key metrics, or wants to replace scattered spreadsheets with a centralized KPI view."
---

# KPI Dashboard Builder

## When to Use This Skill

- Business metrics are scattered across multiple tools and spreadsheets
- Want a single view of business health updated weekly or monthly
- Setting quarterly OKRs and need to track progress
- Onboarding a team member who needs visibility into performance
- Preparing for a board meeting or investor update

## Core Principle

**A DASHBOARD THAT TRACKS EVERYTHING TRACKS NOTHING. Limit to 5-8 KPIs that directly reflect business health.**

## Workflow

### Step 1: Identify Key Metrics

Ask the user:
1. What type of business? (e-commerce, SaaS, service, content creator)
2. What are you trying to improve right now? (revenue, growth, efficiency, retention)
3. How often will you review this? (weekly, monthly, quarterly)
4. Who else will see this dashboard? (just you, team, investors)

**Minimum needed: question 1.**

### Step 2: Select KPIs by Business Type

**E-commerce:**
| KPI | Formula | Target Example | Frequency |
|-----|---------|---------------|-----------|
| Revenue | Total sales | $25,000/mo | Weekly |
| Average Order Value | Revenue / Orders | $58 | Weekly |
| Conversion Rate | Orders / Visitors | 2.5% | Weekly |
| Customer Acquisition Cost | Ad Spend / New Customers | < $25 | Monthly |
| Return Rate | Returns / Orders | < 5% | Monthly |

**SaaS / Subscription:**
| KPI | Formula | Target Example | Frequency |
|-----|---------|---------------|-----------|
| MRR | Sum of active subscriptions | $15,000 | Weekly |
| Churn Rate | Lost customers / Total customers | < 5%/mo | Monthly |
| LTV | Avg revenue per customer × avg lifespan | > $500 | Quarterly |
| CAC | Sales + Marketing spend / New customers | < $100 | Monthly |
| LTV:CAC Ratio | LTV / CAC | > 3:1 | Quarterly |

**Service Business / Freelance:**
| KPI | Formula | Target Example | Frequency |
|-----|---------|---------------|-----------|
| Revenue | Invoiced amount | $12,000/mo | Monthly |
| Utilization Rate | Billable hours / Available hours | > 70% | Weekly |
| Pipeline Value | Sum of proposal values | $50,000 | Weekly |
| Close Rate | Won proposals / Total proposals | > 40% | Monthly |
| Client Retention | Returning clients / Total clients | > 80% | Quarterly |

**Content Creator:**
| KPI | Formula | Target Example | Frequency |
|-----|---------|---------------|-----------|
| Revenue | Sponsorships + Products + Affiliate | $8,000/mo | Monthly |
| Email List Size | Total subscribers | 10,000 | Weekly |
| Email Open Rate | Opens / Delivered | > 40% | Weekly |
| Engagement Rate | (Likes + Comments) / Followers | > 3% | Weekly |
| Content Published | Posts/videos/episodes produced | 12/mo | Weekly |

### Step 3: Build the Notion Dashboard

Create a Notion database with these properties:

- **KPI Name** (Title)
- **Current Value** (Number)
- **Target** (Number)
- **Status** (Select: On Track / At Risk / Off Track)
- **Trend** (Select: Up / Flat / Down)
- **Period** (Select: This Week / This Month / This Quarter)
- **Category** (Select: Revenue / Growth / Efficiency / Retention)
- **Last Updated** (Date)
- **Notes** (Rich text — for context on changes)

Add a **formula property** for % of Target: `(Current Value / Target) × 100`

Set status rules:
- **On Track:** ≥ 90% of target
- **At Risk:** 70-89% of target
- **Off Track:** < 70% of target

### Step 4: Create Dashboard Views

1. **Summary View** — Gallery view showing all KPIs with status color-coding
2. **Weekly Review** — Table filtered to weekly KPIs, sorted by status
3. **Trend View** — Board view grouped by trend (Up / Flat / Down)
4. **Category View** — Board view grouped by category

### Step 5: Set Up Review Rhythm

Provide a review checklist:
- **Weekly (15 min):** Update all weekly KPIs, flag anything Off Track
- **Monthly (30 min):** Update all KPIs, compare to previous month, adjust targets if needed
- **Quarterly (60 min):** Full review, set new targets, add/remove KPIs

## Examples

### Example 1: E-commerce Store Dashboard

**Notion Database Setup:**

| KPI | Current | Target | Status | Trend |
|-----|---------|--------|--------|-------|
| Monthly Revenue | $22,400 | $25,000 | At Risk | Up |
| Average Order Value | $62 | $58 | On Track | Up |
| Conversion Rate | 1.8% | 2.5% | Off Track | Flat |
| New Customers | 180 | 200 | At Risk | Up |
| Return Rate | 3.2% | < 5% | On Track | Down |
| Email List Growth | +340 | +500 | At Risk | Flat |
| Ad ROAS | 3.2x | 3.0x | On Track | Up |

**Weekly Review Notes:**
> Revenue trending up but still below target — conversion rate is the bottleneck. AOV is strong (above target), so traffic quality may be the issue. Action: Review ad targeting this week, check landing page bounce rate.

### Example 2: Freelance Consultant Dashboard

| KPI | Current | Target | Status | Trend |
|-----|---------|--------|--------|-------|
| Monthly Revenue | $9,800 | $12,000 | At Risk | Flat |
| Utilization Rate | 58% | 70% | Off Track | Down |
| Pipeline Value | $42,000 | $50,000 | At Risk | Up |
| Active Clients | 3 | 4 | At Risk | Flat |
| Close Rate | 45% | 40% | On Track | Up |
| Avg Project Value | $4,200 | $4,000 | On Track | Up |

**Insight:** Close rate is strong but pipeline is light. The constraint isn't converting leads — it's generating them. Recommendation: Increase outreach or referral activity before optimizing anything else.

## Recovery & Fallbacks

- **User doesn't know what to track:** Start with revenue + one growth metric + one efficiency metric. Three KPIs beats zero KPIs. Expand after the first month of tracking.
- **User wants to track 20+ metrics:** Push back. A dashboard with 20 metrics is a spreadsheet, not a dashboard. Force-rank and pick the top 5-8.
- **User doesn't use Notion:** Adapt the dashboard to a Google Sheet or Airtable. The structure is the same — only the tool changes.
- **Metrics aren't improving:** Dashboards show problems; they don't fix them. When a KPI is Off Track for 3+ periods, it needs an action plan, not more tracking.

## Constraints

- **NEVER include more than 8 KPIs** on the primary dashboard — create a secondary "detail" view for nice-to-haves
- Every KPI must have a defined target — a metric without a target is just a number
- Include status indicators (On Track / At Risk / Off Track) for at-a-glance reading
- Always include a "Last Updated" field to prevent stale data from looking current
- Provide the review rhythm — a dashboard nobody looks at is useless
