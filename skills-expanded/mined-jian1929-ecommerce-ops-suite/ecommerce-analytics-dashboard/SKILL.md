---
name: ecommerce_analytics_dashboard
description: Analyze e-commerce metrics and create actionable dashboards. Calculate KPIs, track trends, and generate insights from sales, traffic, and conversion data.
---

# E-Commerce Analytics Dashboard

Analyze e-commerce metrics and create actionable business insights.

## When to Use

Use this skill when the user wants to:
- Analyze sales and revenue data
- Calculate e-commerce KPIs (CAC, LTV, AOV, conversion rates)
- Create dashboard-style metric summaries
- Track trends over time periods
- Generate actionable insights from raw data

## Supported Platforms

- Google Analytics, Shopify Analytics, WooCommerce Reports
- Amazon Seller Central, Etsy Stats, eBay Seller Dashboard
- Custom CSV/Excel data import

## Workflow

### Step 1: Data Collection

Gather available metrics:

**Sales Metrics:**
- Total Revenue / GMV
- Number of Orders
- Average Order Value (AOV)
- Units per Transaction
- Return Rate

**Traffic Metrics:**
- Sessions / Visits
- Unique Visitors
- Page Views
- Bounce Rate
- Session Duration

**Conversion Metrics:**
- Conversion Rate (sessions to orders)
- Add-to-Cart Rate
- Checkout Started Rate
- Checkout Completed Rate

### Step 2: KPI Calculation

Calculate key performance indicators:

```markdown
## Core E-Commerce KPIs

### Revenue Metrics
| Metric | Formula | This Period |
|--------|---------|-------------|
| Average Order Value (AOV) | Revenue / Orders | $[X] |
| Revenue per Visitor (RPV) | Revenue / Visitors | $[X] |

### Conversion Metrics
| Metric | Formula | This Period |
|--------|---------|-------------|
| Conversion Rate | Orders / Sessions × 100 | X% |
| Cart Abandonment | 1 - (Checkouts/Add-to-Cart) | X% |
| Checkout Abandonment | 1 - (Purchases/Checkouts) | X% |

### Customer Metrics
| Metric | Formula | This Period |
|--------|---------|-------------|
| Customer Acquisition Cost (CAC) | Spend / New Customers | $[X] |
| Customer Lifetime Value (LTV) | AOV × Orders/Year × Retention Years | $[X] |
| LTV:CAC Ratio | LTV / CAC | X:1 |

### Marketing Metrics
| Metric | Formula | This Period |
|--------|---------|-------------|
| Return on Ad Spend (ROAS) | Revenue / Ad Spend | Xx |
| Marketing Efficiency Ratio | (Revenue - COGS - Ad Spend) / Ad Spend | X% |
```

### Step 3: Trend Analysis

Compare periods (Week-over-Week, Month-over-Month, Year-over-Year):

```markdown
## Trend Analysis

### Positive Trends
- [Metric] increased by [X]% (positive)
- [Explanation of driver]

### Negative Trends
- [Metric] decreased by [X]% (watch)
- [Root cause hypothesis]

### Flat Trends
- [Metric] flat (opportunity for improvement)
```

### Step 4: Dashboard Generation

Create visual-style text dashboards:

```markdown
## 📊 Performance Dashboard

### Revenue Summary
┌─────────────────────────────────────────┐
│ Total Revenue: $[XXX,XXX]  ▲ +XX%     │
│ Orders: [X,XXX]           ▲ +XX%      │
│ AOV: $[XX]               ▼ -X%       │
└─────────────────────────────────────────┘

### Funnel Performance
[████████████░░░░] Sessions: XXX,XXX
[██████░░░░░░░░░] Add to Cart: XX%
[███░░░░░░░░░░░░] Checkout: XX%
[█░░░░░░░░░░░░░░] Purchase: XX%

### Top 3 Insights
1. [Insight with metric]
2. [Insight with metric]
3. [Insight with metric]

### Recommended Actions
- [Priority action based on data]
- [Secondary action]
```

## Best Practices

1. **Context Matters**: Always compare to previous periods
2. **Segment When Possible**: By product, channel, customer type
3. **Explain the "Why"**: Don't just show numbers, explain drivers
4. **Prioritize Actions**: Focus on 3-5 actionable insights max
5. **Visualize Trends**: Use ASCII charts or trend indicators

## Benchmarks for E-Commerce

| Metric | Poor | Average | Good | Excellent |
|--------|------|---------|------|-----------|
| Conversion Rate | <1% | 1-2% | 2-4% | >4% |
| AOV | <$50 | $50-100 | $100-150 | >$150 |
| Cart Abandonment | >85% | 70-85% | 60-70% | <60% |
| LTV:CAC | <1:1 | 1:1-3:1 | 3:1-5:1 | >5:1 |
| ROAS | <1x | 1-3x | 3-5x | >5x |

## Example Prompts

- "Analyze last month's Shopify sales data"
- "Calculate our customer acquisition cost and LTV"
- "Create a dashboard comparing this quarter vs last"
- "Why did our conversion rate drop this week?"
- "What are our top performing products this month?"

## Advanced Use Cases

- **Cohort Analysis**: "Analyze customer retention by acquisition month"
- **Attribution Modeling**: "Which marketing channels drive the most conversions?"
- **Revenue Forecasting**: "Predict next month's revenue based on trends"
- **Unit Economics**: "Calculate our contribution margin per product"
