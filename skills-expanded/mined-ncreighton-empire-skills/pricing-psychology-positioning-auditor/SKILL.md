---
name: pricing-psychology-positioning-auditor
description: "Audit competitor pricing, positioning, and willingness-to-pay signals to recommend tier structures, psychological price anchoring, and bundling strategies. Use when the user needs revenue optimization, pricing research, or A/B test frameworks."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "GOOGLE_SHEETS_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "💰"
    }
  }
---

## Overview

The **Pricing Psychology & Positioning Auditor** is a comprehensive analysis skill that transforms pricing decisions from guesswork into data-driven strategy. It systematically reviews competitor pricing pages, your current positioning, customer behavior signals (support tickets, refund reasons, feature requests), and market benchmarks to recommend actionable changes.

### Why This Matters

Pricing is the easiest lever to pull for revenue growth—a 1% price increase often yields 7-25% profit increase. Yet most companies make pricing decisions based on gut feel or cost-plus formulas. This skill eliminates that risk by surfacing:

- **Willingness-to-pay** signals hidden in customer support data
- **Psychological price anchoring** tactics competitors use
- **Tier structure inefficiencies** that leave money on the table
- **Bundling opportunities** that increase average order value
- **Churn risk factors** from price sensitivity analysis

It integrates with Stripe, Intercom, Zendesk, Google Sheets, and Slack to pull real data about your customers, then synthesizes competitive intelligence (via web_search) and behavioral economics frameworks to generate A/B test templates and price recommendations you can execute immediately.

---

## Quick Start

Try these prompts to get immediate value:

### Prompt 1: Basic Competitor Pricing Audit
```
Analyze the pricing pages of HubSpot, Pipedrive, and Close CRM. 
Compare their tier names, positioning language, anchoring tactics, 
and bundling strategies. What psychological principles does each use? 
Output a comparison table with recommendations for my B2B SaaS pricing.
```

### Prompt 2: Customer Willingness-to-Pay Analysis
```
I'll share my last 50 Zendesk support tickets and 30 refund reasons. 
Identify patterns in price sensitivity, feature requests tied to tier limits, 
and willingness-to-pay signals. Recommend tier structure changes and 
price point adjustments that reduce churn without sacrificing MRR.
```

### Prompt 3: A/B Test Design Framework
```
Generate a 4-week A/B test framework for my SaaS pricing. 
Include: (1) null/alternative hypotheses, (2) segment targeting, 
(3) control vs. test pricing variants, (4) success metrics, 
(5) statistical significance thresholds, (6) Slack alerts for 
real-time monitoring. Format for Optimizely and Google Analytics.
```

### Prompt 4: Psychological Anchoring Strategy
```
My current pricing is $99/$299/$999/month. Redesign tier positioning 
using: charm pricing, left-digit anchoring, decoy pricing, and bundling 
psychology. Show before/after positioning language, visual hierarchy, 
and expected impact on conversion rate and average revenue per user.
```

---

## Capabilities

### 1. Competitor Pricing Intelligence
- **Automated web scraping** of competitor pricing pages (up to 10 competitors)
- **Tier extraction**: Names, features, price points, annual discounts
- **Psychological tactic identification**: Anchoring, scarcity, social proof language
- **Bundling analysis**: Feature combinations, add-on pricing, package deals
- **Output**: Competitive pricing matrix with benchmark percentiles

**Example:**
```
Competitor: Salesforce
- Tier 1: "Starter" ($25/user/mo) — anchors low, positions for entry
- Tier 2: "Professional" ($75/user/mo) — most popular (70% of seats)
- Tier 3: "Enterprise" (custom) — anchors with exclusivity
- Anchoring tactic: Uses "Industry Standard" language on Professional tier
- Bundling: All tiers include email, calls, forecast (basic features)
  Enterprise adds Einstein AI (premium signal)
- Recommended action: Your Tier 2 is underpriced vs. Salesforce Professional
```

### 2. Willingness-to-Pay Signal Detection
- **Support ticket analysis**: Extracts price objections, feature requests, upgrade blockers
- **Refund reason mining**: Identifies price sensitivity vs. feature fit issues
- **Feature request correlation**: Links feature requests to tier levels (can you increase price by adding this feature?)
- **Churn prediction signals**: Detects early warning signs (support volume spikes, downgrade requests)
- **Integration**: Connects to Zendesk, Intercom, HubSpot Service Hub via API

**Example:**
```
Analysis of 50 refund requests:
- 24% cite "price too high relative to value" (price sensitivity)
- 18% request missing features in their tier (upgrade opportunity)
- 12% cite competitor switching (competitive risk)
- 8% cite lack of integrations (bundling gap)

Willingness-to-pay insight: Moving "API access" from Enterprise to 
Professional tier would unlock $12K/month ARR (based on 40 churned 
customers who requested it). Risk: Tier cannibalization <2% based on 
adoption patterns.
```

### 3. Market Benchmark Analysis
- **Industry pricing ranges** for your product category (SaaS, e-commerce, marketplaces, etc.)
- **Price-to-value positioning**: Where you sit vs. premium/budget competitors
- **Elasticity modeling**: Estimates revenue impact of ±5%, ±10%, ±20% price changes
- **Segment pricing**: Per-industry, per-company-size, per-geography recommendations
- **Data source**: Combines G2, Capterra, public filings, industry reports

**Example:**
```
Your category: Project Management SaaS
- Market average: $45-$120/user/month
- Your current: $99/user/month (68th percentile)
- Premium tier average: $400-$600/month flat
- Your premium positioning: Weak (priced like competitor, no differentiation)

Recommendation: Increase Professional tier to $149 (matches Asana, 
positions as premium). Impact model: 8% conversion rate decrease, 
but 50% price increase = +38% revenue growth. Churn risk: <1% based 
on competitor switching patterns.
```

### 4. Tier Structure & Bundling Optimization
- **Feature matrix analysis**: Which features drive upgrades vs. which are table-stakes?
- **Bundling recommendations**: What features should be packaged together?
- **Tier naming psychology**: Reframe names using aspiration/status language
- **Price point optimization**: Recommend specific numbers using charm pricing and anchoring
- **Decoy pricing strategy**: When to add a strategic "bad deal" tier to drive conversions to target tier

**Example Output:**
```
BEFORE:
Tier 1: Free ($0) — Too much free value
Tier 2: Pro ($99) — Name is generic
Tier 3: Enterprise ($999) — Price jump is too high

AFTER:
Tier 1: Starter ($0 → $29/mo) — Convert free users, anchors to paid
Tier 2: Pro ($99 → $149/mo) — Reposition as "Scale" (aspiration language)
Tier 3: Enterprise ($999 → $399/mo) — Reduce jump, add "Teams" positioning
Tier 4: [NEW] Premium ($249/mo) — Decoy tier drives conversions to Scale

Expected impact: +28% revenue (price + tier migration), +12% conversion rate
```

### 5. A/B Test Framework Generation
- **Hypothesis formulation**: Pre-formatted null/alternative hypotheses
- **Segment targeting**: Who to test with (new vs. existing, by company size, by product usage)
- **Variant design**: Control vs. 2-4 test variants (price, tier names, positioning language)
- **Metrics specification**: Primary (conversion rate, ARR), secondary (churn, feature adoption)
- **Statistical power calculation**: Sample size needed, duration, significance threshold
- **Integration templates**: Ready-to-deploy configs for Optimizely, Google Optimize, VWO, or custom scripts
- **Monitoring setup**: Slack alerts for statistical significance, alerts for anomalies

**Example:**
```
TEST: Charm Pricing vs. Round Pricing
Hypothesis: $149/mo (charm) drives higher conversion than $150/mo
Control: $150/month tier
Variant: $149/month tier (same features)

Segment: New sign-ups only (avoiding existing customer bias)
Duration: 2 weeks minimum (target 500 conversions per variant)
Primary metric: Conversion rate (trials to paid)
Secondary metrics: Churn rate (30-day), NPS, feature adoption

Slack alert: 
- Trigger when p-value <0.05
- Alert if conversion rate <3% (technical issue)
- Daily digest of conversion rates by variant

Expected result: 0.5-2% conversion lift from charm pricing
(based on behavioral econ literature for B2B SaaS)
```

### 6. Psychological Price Anchoring Tactics
Recommends specific, evidence-based tactics:

- **Left-digit anchoring**: "From $1/mo" vs. "$10/mo" impacts perception
- **Decoy pricing**: Add a bad-value tier to make target tier look better
- **Charm pricing**: $99 vs. $100 (tested in B2B, 1-2% lift typical)
- **Prestige pricing**: Higher price for premium tier signals quality
- **Bundling illusion**: Combine features to increase perceived value
- **Annual discount positioning**: Show as "40% savings" not "65% yearly price"
- **Social proof anchoring**: "Join 5,000+ companies using our Pro tier"

**Example:**
```
Your current positioning: "Pro Plan - $99/month"

Reframed with anchoring:
"Pro Plan — From $99/month — Join 4,200+ growing companies"
(left-digit anchor + social proof + aspiration)

Landing page changes:
- Highlight savings: "Save 40% annually" (not "$1,188/year")
- Feature positioning: "Everything in Starter, plus:"
- Decoy tier: Add $199 "Pro+" (slight increase) to make Pro look better
- Social proof: Customer logos on pricing page (48% conversion lift)

Expected lift: 8-15% conversion rate improvement from framing alone
```

---

## Configuration

### Required Environment Variables
```bash
# OpenAI API for analysis and recommendations
export OPENAI_API_KEY="sk-..."

# Google Sheets API for storing analysis results and benchmarks
export GOOGLE_SHEETS_API_KEY="AIza..."

# Optional integrations (for data pulling)
export STRIPE_API_KEY="sk_live_..."
export ZENDESK_API_KEY="your_api_key"
export INTERCOM_API_KEY="dG9rOmFkZGNk..."
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T00000/B00000/..."
```

### Setup Steps

1. **Create a Google Sheet** for results storage (templates provided):
   - Competitor Pricing Matrix
   - Willingness-to-Pay Analysis
   - A/B Test Results Tracker
   - Pricing Recommendation Roadmap

2. **Connect your data sources**:
   - Export Zendesk tickets as CSV (last 30-90 days)
   - Pull refund reasons from Stripe dashboard
   - Provide your current pricing page URL

3. **Set analysis scope**:
   - Number of competitors to analyze (2-10 recommended)
   - Customer data time window (30/60/90 days)
   - Analysis depth (quick/standard/comprehensive)

---

## Example Outputs

### Output 1: Competitor Pricing Matrix
```
┌─────────────┬──────────┬──────────┬──────────┬──────────────┐
│ Competitor  │ Tier 1   │ Tier 2   │ Tier 3   │ Anchoring    │
├─────────────┼──────────┼──────────┼──────────┼──────────────┤
│ HubSpot     │ $0       │ $50/mo   │ $120/mo  │ Free trial   │
│ Pipedrive   │ $14/mo   │ $39/mo   │ $99/mo   │ Low anchor   │
│ Close       │ $29/mo   │ $59/mo   │ $99/mo   │ Charm prices │
│ Your SaaS   │ $0       │ $99/mo   │ $999/mo  │ High jump    │
│ Benchmark   │ $0-15    │ $40-80   │ $150+    │ [See gaps]   │
└─────────────┴──────────┴──────────┴──────────┴──────────────┘

Recommendation: Your Tier 1 → Tier 2 jump is too large (4.9x). 
Competitors average 2.8x. Add mid-tier or reduce Tier 2 to $59/mo.
```

### Output 2: Willingness-to-Pay Report
```
CUSTOMER BEHAVIOR SIGNALS (Last 60 days)

Price Objection Rate: 24% of refunds
- Trend: +8% vs. previous quarter
- Risk level: MEDIUM (indicates market saturation or feature gap)

Feature Request Patterns:
- API access (12 requests, 30% from Enterprise tier) → Upsell opportunity
- SSO/SAML (8 requests, 50% from Mid-market) → Premium feature candidate
- Custom workflows (15 requests, 40% churn) → Add to Pro tier

Churn Prediction:
- Support ticket spike 3 weeks before churn (90% accuracy)
- Price objections + feature requests = 2.5x churn likelihood
- At-risk accounts: 7 (estimated $8.4K ARR exposure)

Recommended Actions (Priority Order):
1. Add API access to Pro tier → Expected recovery: $12K ARR, churn reduction: 3%
2. Increase Professional tier pricing to $149 → Revenue lift: +23%, churn risk: <1%
3. Create "Enterprise+" tier at $499/mo for teams tier → New segment: $15K+ ARR
```

### Output 3: A/B Test Design (Ready-to-Deploy)
```yaml
test_name: "Professional Tier Pricing Optimization"
hypothesis: "Increasing Professional tier from $99 to $149/mo 
  (with benefit reframing) will increase conversion rate by 8-12% 
  while reducing churn by <1%."

variants:
  control:
    price: "$99/month"
    name: "Professional"
    tagline: "For growing teams"
  test_a:
    price: "$149/month"
    name: "Scale"
    tagline: "For teams ready to grow"
    change: "Rename tier, reposition as aspiration tier"
  test_b:
    price: "$149/month"
    name: "Professional Plus"
    tagline: "Everything in Starter, plus Advanced Analytics"
    change: "Add feature anchoring to justify price"

targeting:
  segment: "New sign-ups only"
  traffic_allocation: "33% control / 33% test_a / 34% test_b"
  minimum_duration: "14 days"
  sample_size_per_variant: "500 conversions"

success_metrics:
  primary:
    - name: "Conversion Rate (Trial to Paid)"
      expected_lift: "8-12%"
      minimum_acceptable_change: "3%"
      statistical_significance: "p < 0.05"
  secondary:
    - name: "30-day Churn Rate"
      acceptable_increase: "<1%"
    - name: "Pro tier adoption rate"
      baseline: "35%"

monitoring:
  slack_webhook: "https://hooks.slack.com/services/..."
  daily_report: true
  alert_on: 
    - "p-value crossing 0.05 threshold"
    - "conversion rate <3% (tech issue)"
    - "any variant with churn >8%"

deployment:
  platform: "Optimizely"
  pages: ["pricing", "checkout