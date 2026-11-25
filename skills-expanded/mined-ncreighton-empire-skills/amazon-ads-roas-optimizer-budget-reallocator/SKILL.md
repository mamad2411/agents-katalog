---
name: amazon-ads-roas-optimizer-budget-reallocator
description: "Analyze Amazon PPC campaigns in real-time, identify underperformers, calculate true ROAS with organic lift, and reallocate budgets across campaigns. Use when the user needs campaign optimization, keyword analysis, budget recommendations, or A/B testing strategies."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["AMAZON_ADS_CLIENT_ID","AMAZON_ADS_CLIENT_SECRET","AMAZON_ADS_REFRESH_TOKEN","AWS_REGION"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📊"}}
---

## Overview

The **Amazon Ads ROAS Optimizer & Budget Reallocator** is a production-grade skill that transforms raw Amazon PPC data into actionable optimization strategies. This skill connects directly to the Amazon Advertising API to pull real-time campaign metrics, applies proprietary ROAS calculations (including organic lift attribution), and generates data-driven budget reallocation recommendations.

### Why This Matters

Amazon sellers lose an estimated **$47,000 annually** through suboptimal campaign budgeting and keyword underutilization. This skill eliminates guesswork by:

- **Real-time analysis** of campaign performance across 50+ metrics
- **Organic lift attribution** — calculates true profitability by factoring in organic sales influenced by paid campaigns
- **Automated underperformer detection** — identifies ASINs and keywords destroying ROI
- **Intelligent budget reallocation** — recommends specific dollar amounts to move between campaigns
- **A/B test frameworks** — suggests statistically valid experiments to improve conversion rates
- **Multi-channel reporting** — exports to Slack, Google Sheets, or your CRM

**Integrations:** Amazon Advertising API, Google Sheets, Slack, Salesforce, HubSpot, WordPress (via REST), S3 storage for historical analysis.

---

## Quick Start

### Example 1: Analyze Campaign Performance & Get Budget Recommendations

```
Analyze my Amazon PPC campaigns for the last 30 days. Calculate ROAS 
including organic lift. Identify campaigns with ROAS below 1.5x and 
recommend how much budget to reallocate to top performers. Include 
keyword-level analysis for the top 10 underperformers by ACoS.
```

### Example 2: A/B Test Recommendation Framework

```
Generate A/B test recommendations for my "Winter Boots" campaign. 
Suggest variations for ad copy, bid strategy, and targeting. Which 
keywords show the highest conversion rate variance? What's the 
minimum sample size needed to achieve 95% confidence?
```

### Example 3: Weekly Optimization Report with Slack Alert

```
Create a weekly ROAS optimization report for all my campaigns. 
Flag any campaign that dropped more than 10% in ROAS since last week. 
Calculate budget reallocation from bottom 20% to top 20%. Send summary 
to Slack #amazon-ppc and export detailed CSV to Google Drive.
```

### Example 4: Organic Lift Attribution & True Profitability

```
Calculate true ROAS for my campaigns by including organic lift. 
Show me which campaigns are driving organic sales at 2x+ the direct 
paid conversion rate. Recommend pausing low organic-lift campaigns 
and scaling high organic-lift ones.
```

---

## Capabilities

### 1. Real-Time Campaign Analysis
Connects to **Amazon Advertising API v3** to pull:
- Campaign-level metrics: spend, impressions, clicks, conversions, revenue
- Keyword performance: CTR, conversion rate, ACoS, CPC trends
- ASIN-level data: returns, damaged units, refund rates
- Portfolio performance: budget utilization, daily spend variance

**Usage:**
```
Get detailed performance metrics for campaigns containing "premium" 
in the name. Show 14-day trailing metrics with trend comparison 
to the 14 days prior. Flag any metric with >20% variance.
```

### 2. ROAS Calculation with Organic Lift Attribution
Proprietary algorithm that:
- Isolates direct paid conversions from organic conversions
- Uses **cohort analysis** to attribute organic sales to paid campaigns (30-day lookback window)
- Calculates **incremental ROAS** by measuring sales attributed to campaigns vs. baseline organic rate
- Adjusts for seasonality and day-of-week effects
- Produces confidence intervals for statistical validity

**Output Example:**
```
Campaign: "Summer Dresses"
Direct ROAS: 2.3x
Organic Lift ROAS: 1.8x (estimated from 12% of organic revenue)
True ROAS: 4.1x (direct + organic lift combined)
Recommendation: Increase daily budget by $200 (high confidence)
```

### 3. Underperformer Identification
Automated detection using:
- **ACoS threshold analysis** — flags keywords with ACoS >50% of target
- **Conversion velocity** — identifies keywords with <2 conversions/week
- **Impression-to-conversion ratio** — spots keywords wasting impressions
- **Return rate analysis** — catches ASINs with >15% return rates
- **Bid efficiency scoring** — measures cost-per-conversion trend

**Usage:**
```
Identify the bottom 50 keywords by ROAS across all campaigns. 
Show why each is underperforming (high ACoS, low CTR, etc.). 
Recommend bid adjustments or pause thresholds for each.
```

### 4. Budget Reallocation Engine
Calculates optimal budget distribution using:
- **Marginal ROAS curves** — models diminishing returns at scale
- **Capacity constraints** — respects max daily budget limits per campaign
- **Seasonal adjustments** — factors in upcoming demand surges
- **Risk minimization** — gradual reallocation to prevent volatility shocks

**Output:**
```
Current Budget Allocation: Campaign A $500, Campaign B $300, Campaign C $200
Recommended: Campaign A $450, Campaign B $380, Campaign C $270
Expected ROAS Improvement: +0.6x (from 2.1x to 2.7x)
Migration Timeline: Implement over 5 days (gradual 10% daily shift)
```

### 5. A/B Test Design & Statistical Power Analysis
Generates test frameworks with:
- **Hypothesis formulation** — suggests directional tests based on data gaps
- **Sample size calculator** — determines weeks needed to reach 95% confidence
- **Control/treatment design** — recommends keyword groupings or bid variations
- **Expected outcome ranges** — confidence intervals for each variant
- **Statistical significance checker** — validates completed tests

**Usage:**
```
Design an A/B test to improve conversion rate on my "running shoes" 
keyword cluster. What's the best lever to test (bid strategy, targeting 
type, or ad copy)? How long will the test take if I keep current volume?
```

### 6. Multi-Channel Reporting & Export
Automated delivery to:
- **Google Sheets** — auto-updated dashboard with charts and pivots
- **Slack** — daily/weekly summaries with alerts for >10% variance
- **Salesforce/HubSpot** — sync ROAS data to lead records
- **AWS S3** — archive historical data for machine learning models
- **Email** — PDF reports with executive summaries
- **WordPress** — publish performance insights to blog (for agencies)

---

## Configuration

### Required Environment Variables

```bash
# Amazon Advertising API credentials (obtain from Advertising Console)
export AMAZON_ADS_CLIENT_ID="your-client-id"
export AMAZON_ADS_CLIENT_SECRET="your-client-secret"
export AMAZON_ADS_REFRESH_TOKEN="your-refresh-token"
export AWS_REGION="us-east-1"  # or your region: eu-west-1, ap-northeast-1

# Optional: For Slack alerts
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Optional: For Google Sheets integration
export GOOGLE_SHEETS_API_KEY="your-api-key"

# Optional: Salesforce/HubSpot sync
export SALESFORCE_CLIENT_ID="your-sf-id"
export HUBSPOT_API_TOKEN="your-hubspot-token"
```

### Setup Instructions

1. **Create Amazon Ads API Application:**
   - Go to [Amazon Seller Central → Developer Console](https://developer.amazon.com)
   - Register an application and generate OAuth credentials
   - Authorize access to Advertising data
   - Whitelist your IP address in security settings

2. **Initialize the Skill:**
   ```bash
   openclaw configure amazon-ads-roas-optimizer-budget-reallocator
   # Paste credentials when prompted
   # Test connection: openclaw test amazon-ads-roas-optimizer
   ```

3. **Set Analysis Preferences:**
   - ROAS target threshold (default: 1.5x)
   - ACoS maximum acceptable (default: 40%)
   - Organic lift lookback window (default: 30 days)
   - Budget reallocation step size (default: 10% per migration day)

---

## Example Outputs

### Output 1: Campaign Performance Dashboard

```
╔════════════════════════════════════════════════════════════════════════════╗
║                    AMAZON PPC OPTIMIZATION REPORT                          ║
║                          Week of Nov 18-24, 2024                           ║
╚════════════════════════════════════════════════════════════════════════════╝

PORTFOLIO SUMMARY
─────────────────────────────────────────────────────────────────────────────
Total Spend:           $4,250         Direct Revenue:        $12,340
Avg ROAS (Direct):     2.1x           Avg ROAS (w/ Organic):  3.8x
Avg ACoS:              48%            Portfolio Efficiency:  -5% vs prior week
Top Campaign:          Winter Boots   Bottom Campaign:       Summer Dresses

UNDERPERFORMER ALERTS (Bottom 5 by ROAS)
─────────────────────────────────────────────────────────────────────────────
Campaign: Summer Dresses
├─ Direct ROAS: 1.2x ❌ (Target: 1.5x)
├─ ACoS: 82% (43% above target)
├─ Issue: High CPC ($0.68), Low CTR (0.8%)
├─ Action: Reduce bids by 15%, test negative keywords
└─ Impact: Potential +$340/week revenue if optimized

Campaign: Casual Wear - Budget
├─ Direct ROAS: 1.4x ⚠️  (Target: 1.5x)
├─ ACoS: 71%
├─ Issue: Organic lift is strong (2.6x) but paid is weak
├─ Action: Increase daily budget to $150, focus on brand keywords
└─ Impact: Organic lift could generate additional $1,200/month

BUDGET REALLOCATION RECOMMENDATION
─────────────────────────────────────────────────────────────────────────────
Action: Move $300/week from underperformers to top 3 campaigns
Timeline: 5-day gradual migration (minimize volatility)

FROM:                              TO:
Summer Dresses      -$150    ──→  Winter Boots       +$100
Casual Wear Misc    -$150    ──→  Premium Shoes      +$120
                                  Activewear         +$80

Expected Outcome: ROAS +0.4x (3.8x → 4.2x), Spend unchanged
Confidence Level: 92%

A/B TEST RECOMMENDATIONS
─────────────────────────────────────────────────────────────────────────────
Test 1: Winter Boots - Bid Strategy Optimization
├─ Control: Dynamic bids (down only)
├─ Treatment: Fixed bids at $0.55 (current avg: $0.62)
├─ Expected Outcome: -5% conversions, -12% ACoS (net +0.3x ROAS)
├─ Duration: 14 days at current volume
└─ Sample Size: 340 conversions needed

Test 2: Summer Dresses - Targeting Refinement
├─ Control: Broad match keywords
├─ Treatment: Phrase + exact match only
├─ Expected Outcome: -20% impressions, +35% conversion rate
├─ Duration: 21 days
└─ Sample Size: 280 conversions needed
```

### Output 2: Organic Lift Attribution Report

```
CAMPAIGN: Premium Shoes (30-day analysis)
─────────────────────────────────────────────────────────────────────────────
Direct Paid Conversions:        847
Direct Paid Revenue:            $19,854
Direct ROAS:                    2.1x

Organic Sales Analysis:
├─ Total Organic Conversions:   324
├─ Baseline Organic Rate:       2.1% (historical avg without paid)
├─ Organic Conversions w/ Paid: 2.8%
├─ Lift Attribution:            (+0.7%) = ~101 organic conversions
├─ Organic Revenue Lift:        $2,367
└─ Organic Lift ROAS:           1.18x

True ROAS (Combined Impact):    3.28x ✓ EXCELLENT
Recommendation: Scale budget by 25%
```

### Output 3: Slack Alert Format

```
📊 Amazon PPC Daily Alert — Nov 24, 2024

⚠️  PORTFOLIO ROAS DOWN 8% → 3.2x (Target: 3.8x)

🔴 3 Campaigns Need Attention:
   • Summer Dresses: ROAS 1.2x (down from 1.5x)
   • Casual Misc: ACoS at 71% (vs 60% target)
   • Accessories: CTR dropped 12%

✅ 2 Campaigns Excelling:
   • Winter Boots: ROAS 4.8x (up 0.6x)
   • Premium Shoes: +14% conversions

💰 Recommended Action: Reallocate $200 from Dresses to Winter Boots
→ Open detailed report: [link]
→ Apply recommendations: [button]
```

---

## Tips & Best Practices

### 1. Optimize Organic Lift Attribution
- **Check lookback window:** Shorter windows (14 days) work better for seasonal products; longer (60 days) for evergreen
- **Validate baseline rates:** Analyze 90 days of historical data before campaigns to establish true organic conversion baseline
- **Account for new ASINs:** Disable organic lift calculation for products <30 days old; ramp to full attribution gradually
- **Monitor external factors:** Adjust for reviews, pricing changes, or competitor activity that affect organic sales

### 2. Budget Reallocation Strategy
- **Migrate gradually:** Move budget in 10% daily increments to avoid shocking the algorithm and triggering learning resets
- **Respect daily minimums:** Keep all campaigns at least $20/day to maintain statistical significance
- **Use seasonal lens:** Scale up 3 weeks before peak season (Thanksgiving, Christmas, Prime Day) and reduce immediately after
- **Test before scaling:** Run A/B tests on reallocation decisions before implementing full portfolio changes

### 3. A/B Testing Rigor
- **Calculate sample size upfront:** Use the built-in calculator; underpowered tests waste time
- **Run control/treatment in parallel:** Never pause control campaigns mid-test; use campaign splitting instead
- **Wait for statistical significance:** Don't declare winners until 95% confidence is achieved (typical: 14-21 days)
- **Document all tests:** Create a test registry to avoid conflicting hypotheses and learn from past results

### 4. Campaign Structure for Optimization
- **Segment by intent:** Separate branded, category, and competitor keywords into distinct campaigns for surgical budget allocation
- **Group by product type:** Create 1 campaign per product category to isolate underperformers
- **Monitor portfolio structure:** If campaigns become imbalanced (one >50% of spend), rebalance quarterly
- **Use negative keywords aggressively:** Block non-converting search terms weekly to improve ACoS

### 5. Real-Time Monitoring
- **Set up Slack alerts:** Get daily notifications for ROAS variance >10%, spend anomalies, or underperformer detection
- **Review top 20 keywords daily:** Identify trending winners and adjust bids within 24 hours
- **Check organic lift weekly:** Compare organic conversion rate to baseline; if it spikes, increase paid budgets
- **Audit placements monthly:** Review top of search vs. product page placement performance; adjust bid modifiers

### 6. Data Quality