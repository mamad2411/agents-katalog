---
name: financial-dashboard
description: Creates a financial KPI tracking dashboard structure with revenue, expenses, margins, runway, and trend analysis. Use this skill when a business owner wants a single view of their financial health, needs to set up KPI tracking, or wants to monitor financial metrics consistently.
allowed-tools: Read Write Bash(ls)
---

# Financial Dashboard

## When to Use This Skill

- User wants a single-view financial dashboard for their business
- User needs to track revenue, expenses, and margins over time
- User wants to set up KPI tracking for financial health
- User is growing and needs visibility into burn rate or runway
- User wants to compare financial performance across months or quarters

## Core Principle

A DASHBOARD THAT TRACKS EVERYTHING TRACKS NOTHING — LIMIT TO 8-12 KPIS THAT DIRECTLY ANSWER "AM I MAKING MONEY AND WILL I KEEP MAKING MONEY?"

## Financial Disclaimer

**IMPORTANT: This dashboard is for internal tracking and planning purposes only. It does not constitute audited financial reporting. Always consult a qualified accountant for official financial statements, tax filings, and compliance. Accuracy depends on the data entered by the user.**

## Workflow

### Phase 1: Define the Business Model

1. Confirm the business type to select relevant KPIs:
   - **Service business** (freelancer, consultant, agency): Focus on revenue per client, utilization rate, project margin
   - **E-commerce**: Focus on AOV, COGS, gross margin, customer acquisition cost
   - **Digital products/SaaS**: Focus on MRR, churn, LTV, CAC
   - **Hybrid**: Combine relevant metrics from above
2. Determine tracking frequency: monthly (default) or weekly
3. Identify data sources (bank account, Stripe, PayPal, QuickBooks, spreadsheet)

### Phase 2: Select KPIs

4. Choose 8-12 KPIs from the master list below. Default selections are marked.

**Revenue KPIs:**

| KPI | Formula | Default For |
|-----|---------|-------------|
| Total Revenue | Sum of all income | All businesses |
| Monthly Recurring Revenue (MRR) | Recurring subscriptions/retainers | SaaS, memberships |
| Revenue by Source | Revenue broken down by channel/product | All businesses |
| Average Order Value (AOV) | Revenue / Number of orders | E-commerce |
| Revenue per Client | Revenue / Active clients | Service businesses |

**Profitability KPIs:**

| KPI | Formula | Default For |
|-----|---------|-------------|
| Gross Profit | Revenue - COGS | All businesses |
| Gross Margin % | (Gross Profit / Revenue) x 100 | All businesses |
| Net Profit | Revenue - All Expenses | All businesses |
| Net Margin % | (Net Profit / Revenue) x 100 | All businesses |
| Operating Expense Ratio | Operating Expenses / Revenue | All businesses |

**Growth & Health KPIs:**

| KPI | Formula | Default For |
|-----|---------|-------------|
| Month-over-Month Growth | (This Month - Last Month) / Last Month x 100 | All businesses |
| Cash Runway | Cash on Hand / Monthly Burn Rate | Startups, new businesses |
| Customer Acquisition Cost (CAC) | Marketing Spend / New Customers | E-commerce, SaaS |
| Customer Lifetime Value (LTV) | Avg Revenue per Customer x Avg Retention (months) | SaaS, memberships |
| Accounts Receivable Aging | Outstanding invoices by days overdue | Service businesses |

### Phase 3: Build the Dashboard Structure

5. Create the dashboard layout with these sections:

```
╔══════════════════════════════════════════════════════════╗
║              FINANCIAL DASHBOARD — [MONTH YEAR]         ║
║              [Business Name]                            ║
╠══════════════════════════════════════════════════════════╣
║                                                         ║
║  SNAPSHOT (Top-line numbers)                            ║
║  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  ║
║  │ Revenue  │ │ Expenses │ │Net Profit│ │Net Margin│  ║
║  │ $XX,XXX  │ │ $XX,XXX  │ │ $X,XXX  │ │  XX.X%   │  ║
║  │ ▲ +12%   │ │ ▲ +5%    │ │ ▲ +22%  │ │ ▲ +3.1pp │  ║
║  └──────────┘ └──────────┘ └──────────┘ └──────────┘  ║
║                                                         ║
║  REVENUE BREAKDOWN                                      ║
║  [Revenue by source — bar chart or table]              ║
║                                                         ║
║  EXPENSE BREAKDOWN                                      ║
║  [Top 5 expense categories — bar chart or table]       ║
║                                                         ║
║  TREND (Last 6 months)                                  ║
║  [Revenue, Expenses, Net Profit line over time]        ║
║                                                         ║
║  HEALTH INDICATORS                                      ║
║  [CAC, LTV, Runway, AR Aging — as applicable]          ║
║                                                         ║
╚══════════════════════════════════════════════════════════╝
```

6. For each KPI, define:
   - Green/Yellow/Red thresholds (what's healthy, warning, critical)
   - Data source (where the number comes from)
   - Update frequency

### Phase 4: Populate with Data

7. If the user provides financial data, populate the dashboard with real numbers
8. Calculate all derived metrics (margins, ratios, growth rates)
9. Flag any KPIs in the red zone with specific commentary

### Phase 5: Deliver

10. Output the complete dashboard structure
11. Output a data collection template (what to track and where to enter it)
12. Provide threshold definitions so the user knows what green/yellow/red means

## Example 1: Freelance Copywriter Dashboard

**Context:** Solo copywriter earning $6,000-$9,000/month from retainer clients and one-off projects. Wants to track if the business is healthy.

**Selected KPIs (8):** Total Revenue, Revenue per Client, Gross Margin, Net Profit, Net Margin, MoM Growth, Operating Expense Ratio, Accounts Receivable

```
╔══════════════════════════════════════════════════════════╗
║         FINANCIAL DASHBOARD — JANUARY 2026              ║
║         Cole Bradley Copywriting                        ║
╠══════════════════════════════════════════════════════════╣
║                                                         ║
║  SNAPSHOT                                               ║
║  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  ║
║  │ Revenue  │ │ Expenses │ │Net Profit│ │Net Margin│  ║
║  │ $8,200   │ │ $1,340   │ │ $6,860  │ │  83.7%   │  ║
║  │ ▲ +8.6%  │ │ ▼ -2.1%  │ │ ▲ +11.4%│ │ ▲ +2.1pp │  ║
║  │ 🟢 GOOD  │ │ 🟢 GOOD  │ │ 🟢 GOOD │ │ 🟢 GOOD  │  ║
║  └──────────┘ └──────────┘ └──────────┘ └──────────┘  ║
║                                                         ║
║  REVENUE BREAKDOWN                                      ║
║  Retainer Clients (3)              $6,000    73.2%     ║
║    - Greenline Marketing           $2,500              ║
║    - FreshPress Juicery            $2,000              ║
║    - Oakmont Financial             $1,500              ║
║  One-Off Projects (2)              $2,200    26.8%     ║
║    - Website copy (Bloom Yoga)     $1,400              ║
║    - Email sequence (indie author)   $800              ║
║                                                         ║
║  Revenue per Client: $1,640                            ║
║                                                         ║
║  EXPENSE BREAKDOWN                                      ║
║  Software & Tools        $144    10.7%                 ║
║    Jasper AI $49, Grammarly $30, ConvertKit $29,       ║
║    Google Workspace $12, Notion $8, Zoom $16           ║
║  Marketing               $450    33.6%                 ║
║    LinkedIn ads $300, portfolio hosting $50,            ║
║    networking event $100                                ║
║  Contractor               $400    29.9%                ║
║    VA (16 hrs x $25)                                   ║
║  Professional Services    $150    11.2%                 ║
║    Bookkeeper                                          ║
║  Office & Operations      $145    10.8%                ║
║    Co-working $120, supplies $25                       ║
║  Education                 $51     3.8%                ║
║    Newsletter subscription                             ║
║                                                         ║
║  TREND (Last 6 months)                                  ║
║  Aug   $5,800  ████████████                            ║
║  Sep   $6,400  █████████████                           ║
║  Oct   $7,100  ██████████████                          ║
║  Nov   $7,550  ███████████████                         ║
║  Dec   $7,550  ███████████████                         ║
║  Jan   $8,200  ████████████████                        ║
║  MoM Growth: +8.6% (6-mo avg: +7.2%)                  ║
║                                                         ║
║  HEALTH INDICATORS                                      ║
║  Operating Expense Ratio: 16.3% 🟢 (target: <30%)     ║
║  Accounts Receivable: $1,400 🟡                        ║
║    - Bloom Yoga: $1,400 outstanding (22 days)          ║
║    - All retainers: paid current                       ║
║                                                         ║
╚══════════════════════════════════════════════════════════╝
```

**Threshold Definitions:**

| KPI | Green | Yellow | Red |
|-----|-------|--------|-----|
| Net Margin | >60% | 40-60% | <40% |
| MoM Growth | >5% | 0-5% | Negative |
| OpEx Ratio | <30% | 30-50% | >50% |
| AR Aging | <30 days | 30-60 days | >60 days |

**Action item:** Follow up with Bloom Yoga on the $1,400 outstanding invoice — approaching 30-day threshold.

## Example 2: E-Commerce Skincare Brand Dashboard

**Context:** Small skincare brand selling through Shopify, $15K-$22K/month revenue, 3 product lines.

**Selected KPIs (10):** Total Revenue, AOV, Gross Profit, Gross Margin, Net Profit, Net Margin, MoM Growth, CAC, Revenue by Product Line, Cash Runway

```
╔══════════════════════════════════════════════════════════╗
║         FINANCIAL DASHBOARD — JANUARY 2026              ║
║         GlowRoot Botanicals                             ║
╠══════════════════════════════════════════════════════════╣
║                                                         ║
║  SNAPSHOT                                               ║
║  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  ║
║  │ Revenue  │ │Gross Mrgn│ │Net Profit│ │   AOV    │  ║
║  │ $19,400  │ │  68.2%   │ │ $7,180  │ │  $54.20  │  ║
║  │ ▲ +6.0%  │ │ ▼ -1.3pp │ │ ▲ +4.2% │ │ ▲ +$2.40 │  ║
║  │ 🟢 GOOD  │ │ 🟢 GOOD  │ │ 🟢 GOOD │ │ 🟢 GOOD  │  ║
║  └──────────┘ └──────────┘ └──────────┘ └──────────┘  ║
║                                                         ║
║  REVENUE BY PRODUCT LINE                                ║
║  Serums               $9,800     50.5%   ▲ +12%       ║
║  Cleansers            $5,600     28.9%   ▼ -3%        ║
║  Moisturizers         $4,000     20.6%   ▲ +8%        ║
║                                                         ║
║  EXPENSE SUMMARY                                        ║
║  COGS                 $6,168     31.8%                 ║
║  Marketing            $3,200     16.5%                 ║
║  Fulfillment          $1,450      7.5%                 ║
║  Software               $372      1.9%                 ║
║  Contractors            $600      3.1%                 ║
║  Other OpEx             $430      2.2%                 ║
║  Total Expenses      $12,220     63.0%                 ║
║                                                         ║
║  GROWTH METRICS                                         ║
║  New Customers: 142    CAC: $22.54                     ║
║  Repeat Customers: 86  Repeat Rate: 37.7%             ║
║  CAC Trend: $22.54 🟢 (target: <$30)                  ║
║                                                         ║
║  TREND (Last 6 months)                                  ║
║  Aug   $14,200  ████████████                           ║
║  Sep   $15,800  █████████████                          ║
║  Oct   $17,600  ██████████████                         ║
║  Nov   $21,300  █████████████████                      ║
║  Dec   $18,300  ███████████████                        ║
║  Jan   $19,400  ████████████████                       ║
║                                                         ║
║  CASH POSITION                                          ║
║  Cash on hand: $28,500                                 ║
║  Monthly burn: $12,220                                 ║
║  Runway: 2.3 months (at zero revenue) 🟡               ║
║  Note: Runway is conservative — assumes no income       ║
║                                                         ║
╚══════════════════════════════════════════════════════════╝
```

**Threshold Definitions for E-Commerce:**

| KPI | Green | Yellow | Red |
|-----|-------|--------|-----|
| Gross Margin | >50% | 30-50% | <30% |
| Net Margin | >20% | 10-20% | <10% |
| CAC | <$30 | $30-$50 | >$50 |
| Cash Runway | >3 months | 1-3 months | <1 month |
| AOV | >$45 | $30-$45 | <$30 |

**Data Collection Template:**

Track these numbers weekly, compile monthly:
1. **Revenue**: Export from Shopify Admin > Analytics > Sales by product
2. **COGS**: Track per-unit costs in a spreadsheet, multiply by units sold
3. **Marketing spend**: Sum of ad platform dashboards (Meta, Google) + any other promo costs
4. **New vs. repeat customers**: Shopify Admin > Customers > filter by "First order this month"
5. **Cash on hand**: Business checking account balance on the last day of the month

## Recovery and Fallback

- If the user has no historical data, set up the dashboard structure with empty fields and help them start tracking from the current month
- If the user uses multiple payment processors, help them consolidate by listing all sources and suggesting a monthly reconciliation process
- If a KPI is in the red zone, provide one specific action to address it (not a list of 10 options)
- If the user finds the full dashboard overwhelming, start with the 4-metric snapshot only (Revenue, Expenses, Net Profit, Net Margin) and add KPIs over time

## Constraints

- **Always include the financial disclaimer**
- Limit to 12 KPIs maximum — more than that reduces usability
- Do not include vanity metrics (social followers, website visits) in a financial dashboard
- Do not calculate or estimate tax liability
- Cash runway calculation assumes zero revenue as worst-case — always note this
- Thresholds are guidelines, not rules — they vary by industry and business stage
- Do not recommend specific accounting software unless the user asks
- All financial data must come from the user — do not estimate or fabricate numbers
