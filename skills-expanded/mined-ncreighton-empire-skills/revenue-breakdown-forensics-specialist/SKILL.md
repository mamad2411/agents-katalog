---
name: revenue-breakdown-forensics-specialist
description: "Analyze Stripe, Shopify, and Gumroad transaction data to identify profitable products, customer cohorts, and traffic sources. Use when the user needs profitability analysis, SKU performance ranking, or revenue optimization recommendations."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["STRIPE_API_KEY", "SHOPIFY_API_TOKEN", "GUMROAD_API_TOKEN"],
        "bins": ["python3", "jq"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "💰"
    }
  }
---

# Revenue Breakdown Forensics Specialist

## Overview

The Revenue Breakdown Forensics Specialist is a business intelligence automation that transforms raw transaction data from **Stripe**, **Shopify**, and **Gumroad** into actionable profitability intelligence. While most business dashboards show *revenue*, this skill reveals *true profitability* by factoring in product costs, refunds, churn, support burden, and customer acquisition costs.

**Why this matters:**
- A $5,000/month SKU with 60% refund rate costs you money
- Your highest-revenue customer cohort may be your least profitable (high support tickets)
- Traffic sources that convert well may attract low-LTV customers who refund frequently
- Seasonal spikes mask year-round money-losers that should be sunset

**Integrations supported:**
- **Stripe** (SaaS, subscription, one-time payments)
- **Shopify** (e-commerce, physical products, variants)
- **Gumroad** (digital products, creator economy)
- **Google Analytics 4** (traffic source attribution)
- **Slack** (automated profitability alerts)
- **CSV/Excel** (manual data import for custom platforms)

This skill automates the forensic analysis that would take a financial analyst 40+ hours to complete manually.

---

## Quick Start

### Example 1: Analyze Stripe Revenue by Product & Refund Rate
```
Analyze my Stripe transactions from the last 90 days. 
Show me which products have the highest refund rates and which customers 
have requested support more than 5 times. Rank SKUs by actual profit 
(revenue minus refund impact). Include cohort analysis by customer signup date.
```

### Example 2: Identify Money-Losing Customer Segments
```
Pull my Shopify order data for 2024. Break down profitability by:
1. Traffic source (organic, paid ads, referral)
2. Customer lifetime value vs. support tickets opened
3. Product variant performance by margin

Tell me which traffic sources should be cut and which cohorts are over-indexed 
for refunds. What's our LTV:CAC ratio by channel?
```

### Example 3: Sunset Decision Framework
```
I sell 12 Gumroad products. Create a matrix showing:
- Revenue per product (last 6 months)
- Refund count and percentage
- Average time-to-refund
- Customer satisfaction scores (if available)

Which products should I consider discontinuing? Which ones should I raise 
prices on? Rank all 12 by profitability multiplier potential.
```

### Example 4: Cohort Profitability Deep Dive
```
Analyze Stripe data by customer cohort (signup month). For each cohort:
- Total revenue
- Total refunds
- Current churn rate
- Support tickets per customer
- LTV based on 12-month lookback

Which cohort is most profitable? Which should we stop acquiring?
```

---

## Capabilities

### 1. **Multi-Platform Data Aggregation**
- Connects to Stripe, Shopify, and Gumroad APIs simultaneously
- Normalizes transaction data across different schema formats
- Handles multi-currency conversions (USD-normalized)
- Retrieves 1–5 years of historical data (configurable)

### 2. **Profitability Forensics**
- **Refund analysis:** Rate, dollar amount, and time-to-refund by product
- **Product margin tracking:** Revenue minus COGS (if provided)
- **Support burden calculation:** Tickets per customer × estimated cost
- **Churn detection:** Customers who purchased once then churned
- **Lifetime value (LTV) modeling:** Cohort-based and individual customer

### 3. **Customer Cohort Segmentation**
- Automatic segmentation by: acquisition month, traffic source, product affinity, refund history
- Identifies high-churn, high-support-burden, and low-margin cohorts
- Calculates CAC payback period by cohort
- Flags "toxic" customers (high refund rate, low LTV, high tickets)

### 4. **Traffic Source Attribution**
- Links Stripe/Shopify orders to Google Analytics 4 source/medium
- Calculates LTV:CAC ratio by channel (organic, paid search, social, direct, etc.)
- Identifies underperforming acquisition channels
- ROI analysis for paid traffic

### 5. **SKU & Product Variant Analysis**
- Ranks products by: revenue, profit, refund rate, profit margin percentage
- Variant-level analysis (size, color, tier breakdowns)
- Identifies slow-moving, low-margin SKUs ripe for discontinuation
- Price optimization recommendations based on elasticity

### 6. **Automated Recommendations Engine**
Generates ranked list of revenue-multiplying actions:
- **Raise prices on:** High-demand, low-refund-rate products
- **Kill SKUs:** Products with >40% refund rate or <10% margin
- **Sunset channels:** Traffic sources with LTV:CAC < 3:1
- **Focus cohorts:** Customer segments with >3x average LTV
- **Reduce support burden:** Identify products with highest support:sales ratio

### 7. **Time-Series Profitability Trends**
- Monthly/quarterly profitability snapshots
- Seasonal pattern detection
- Anomaly flagging (sudden refund spikes, churn increases)
- Trend forecasting (simple linear regression)

---

## Configuration

### Required Environment Variables

```bash
# Stripe (OAuth or API Key)
export STRIPE_API_KEY="sk_live_..."
export STRIPE_ACCOUNT_ID="acct_..."  # If using Connect

# Shopify
export SHOPIFY_SHOP_URL="yourstore.myshopify.com"
export SHOPIFY_API_TOKEN="shpat_..."
export SHOPIFY_API_VERSION="2024-01"

# Gumroad
export GUMROAD_API_TOKEN="..."

# Optional: Google Analytics 4 (for traffic source attribution)
export GA4_PROPERTY_ID="1234567890"
export GA4_API_CREDENTIALS="path/to/service-account.json"

# Optional: Slack notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Optional: Cost data
export PRODUCT_COST_CSV="path/to/costs.csv"
export SUPPORT_HOURLY_RATE="50"  # $ per hour
```

### Setup Instructions

1. **Stripe:**
   - Navigate to [Stripe Dashboard > API Keys](https://dashboard.stripe.com/apikeys)
   - Copy your Secret Key (starts with `sk_live_`)
   - Verify you have read access to: Charges, Customers, Invoices, Refunds

2. **Shopify:**
   - Go to Settings > Apps and Integrations > API Credentials
   - Create a custom app with `read_orders` and `read_products` scopes
   - Copy the access token

3. **Gumroad:**
   - Visit [Gumroad Settings > API](https://gumroad.com/settings/api)
   - Generate an access token
   - Ensure you have creator/business account status

4. **Google Analytics 4 (Optional):**
   - Create a service account at [Google Cloud Console](https://console.cloud.google.com)
   - Download JSON credentials
   - Grant Editor access to your GA4 property

5. **Cost Data (Optional):**
   - Prepare CSV: `product_id,sku,cost_usd`
   - Pass via `PRODUCT_COST_CSV` env var for margin calculations

---

## Example Outputs

### Output 1: SKU Profitability Ranking
```
PRODUCT PROFITABILITY RANKING
═══════════════════════════════════════════════════════════════

Rank │ Product           │ Revenue │ Refunds │ Margin % │ LTV  │ Action
─────┼───────────────────┼─────────┼─────────┼──────────┼──────┼──────────────
  1  │ Pro Plan Annual   │ $24,500 │ 3.2%    │ 68%      │$156  │ RAISE PRICE
  2  │ Starter + Support │ $18,200 │ 5.1%    │ 52%      │$89   │ MAINTAIN
  3  │ Basic (Lifetime)  │ $12,100 │ 12.8%   │ 31%      │$34   │ SUNSET
  4  │ Premium Addon     │ $8,900  │ 48.2%   │ -5%      │-$12  │ KILL NOW
─────┴───────────────────┴─────────┴─────────┴──────────┴──────┴──────────────

RECOMMENDATION: Kill "Premium Addon" (negative margin). Raise prices on 
Pro Plan Annual by 15–20% (low refund rate = high elasticity). Sunset Basic 
(Lifetime) — refund rate is unsustainable.
```

### Output 2: Customer Cohort Analysis
```
COHORT PROFITABILITY MATRIX
═════════════════════════════════════════════════════════════════

Signup Month │ Customers │ Revenue │ LTV    │ Churn % │ Refund % │ ROI Status
─────────────┼───────────┼─────────┼────────┼─────────┼──────────┼──────────
Jan 2024     │ 234       │ $12,450 │ $53.21 │ 18%     │ 4.2%     │ 🟢 HEALTHY
Feb 2024     │ 189       │ $8,920  │ $47.20 │ 22%     │ 6.8%     │ 🟡 MONITOR
Mar 2024     │ 412       │ $18,560 │ $45.10 │ 28%     │ 11.3%    │ 🔴 AT RISK
Apr 2024     │ 156       │ $5,600  │ $35.90 │ 35%     │ 18.2%    │ 🔴 SHUT OFF

INSIGHT: Jan 2024 cohort is your profit engine (53% LTV, 4% churn). 
Mar & Apr cohorts are acquisition failures — high churn, high refunds. 
Stop all acquisition efforts targeting those cohort profiles.
```

### Output 3: Traffic Source Forensics
```
CHANNEL PROFITABILITY (LTV:CAC Analysis)
═══════════════════════════════════════════════════════════════

Source         │ Orders │ CAC    │ LTV    │ LTV:CAC │ Margin │ Action
───────────────┼────────┼────────┼────────┼─────────┼────────┼────────────
Organic        │ 1,240  │ $0     │ $92    │ ∞       │ 68%    │ SCALE UP
Direct         │ 890    │ $5     │ $78    │ 15.6:1  │ 62%    │ MAINTAIN
Google Ads     │ 340    │ $28    │ $51    │ 1.8:1   │ 45%    │ KILL NOW
Facebook Ads   │ 210    │ $42    │ $38    │ 0.9:1   │ 32%    │ KILL NOW
Affiliate      │ 125    │ $12    │ $128   │ 10.7:1  │ 71%    │ SCALE UP

RECOMMENDATION: Kill paid ads immediately (LTV:CAC < 3). Double down on 
organic and affiliate channels (highest ROI). Reallocate ad spend to content 
marketing to boost organic acquisition.
```

### Output 4: Refund Forensics Report
```
REFUND ANALYSIS BY PRODUCT
═════════════════════════════════════════════════════════════════

Product              │ Units Sold │ Refunds │ % Rate │ Avg Days │ Impact
─────────────────────┼────────────┼─────────┼────────┼──────────┼─────────
Premium + Setup      │ 45         │ 2       │ 4.4%   │ 18       │ Low
Starter Bundle       │ 289        │ 12      │ 4.2%   │ 22       │ Low
Mid-Tier Upgrade     │ 156        │ 28      │ 17.9%  │ 8        │ HIGH
Tier 3 (Annual)      │ 102        │ 51      │ 50.0%  │ 15       │ CRITICAL

TOP REFUND REASONS (unstructured feedback):
- Mid-Tier: "Not enough value for price" (60%)
- Tier 3: "Features not as described" (45%), "Customer changed mind" (35%)

ACTION: Rewrite Mid-Tier marketing copy. Audit Tier 3 feature parity 
vs. sales messaging. Lower Tier 3 price or add missing features.
```

---

## Tips & Best Practices

### 1. **Data Quality & Freshness**
- Ensure all transaction data includes: `customer_id`, `product_id`, `refund_status`, `refund_date`, `created_date`
- Run analysis weekly (not daily) to smooth out daily volatility
- Use a 90-day minimum lookback window for statistical significance
- Flag any refunds >30 days old as "delayed refunds" (often indicate dissatisfaction)

### 2. **Cost Data is Critical**
- Without COGS, "revenue" rankings are meaningless
- If exact costs unavailable, use industry benchmarks:
  - SaaS: 15–25% COGS (hosting, payment processing)
  - Digital products: 5–10% COGS (payment fees, delivery)
  - Physical: 40–60% COGS (typical retail)
- Update cost data monthly to track margin compression

### 3. **Customer Acquisition Cost (CAC) Context**
- Default CAC assumption: $0 for organic, estimate for paid
- If you have Google Analytics 4 linked, use actual CAC by channel
- Typical healthy LTV:CAC ratio: **3:1 or higher**
- Red flag: LTV:CAC < 1:1 (losing money on acquisition)

### 4. **Refund Rate Interpretation**
- **< 5%:** Excellent (low product-market fit issues)
- **5–15%:** Acceptable (normal for SaaS/digital)
- **15–30%:** Warning (quality or messaging problem)
- **> 30%:** Critical (product or fulfillment failure)

### 5. **Churn vs. One-Time Purchasers**
- Don't penalize one-time products (digital guides, courses)
- Focus churn analysis on subscription/recurring products
- Track "repeat purchase rate" (% who buy >1 product) as secondary metric

### 6. **Seasonal Adjustments**
- Expect 30–50% revenue variance month-to-month (B2B seasonality)
- Use 12-month rolling averages to smooth noise
- Flag anomalies only if >3 standard deviations from mean

### 7. **Price Optimization Window**
- Products with <5% refund rate + >50% margin: safe to raise prices 15–25%
- Test in 10% customer segment first, measure refund rate
- Avoid raising prices on products with >20% refund rate (signals issue)

### 8. **Integrate with Decision Workflows**
- Export recommendations to Slack (weekly alerts)
- Create Google Sheets dashboard (auto-update via API)
- Share SKU sunsets with product/ops teams 2 weeks in advance
- Use CAC findings