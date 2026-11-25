---
name: funnel-leak-detector-attribution-mapper
description: "Analyze complete sales funnels to identify drop-off points, traffic source attribution, and conversion leaks. Use when the user needs CRO audits, funnel optimization, or revenue recovery strategies."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["GOOGLE_ANALYTICS_API_KEY", "FACEBOOK_PIXEL_ID", "SLACK_WEBHOOK_URL"],
        "bins": ["python3", "curl"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🔍"
    }
  }
---

# Funnel Leak Detector & Attribution Mapper

## Overview

This expert-level skill performs comprehensive sales funnel audits across your entire customer journey—from first touch (landing page) through checkout to post-purchase. It identifies exactly where leads abandon, quantifies the revenue impact, diagnoses root causes (form friction, messaging misalignment, trust gaps, poor mobile UX), and generates a prioritized action plan with estimated recovery revenue per fix.

**Why This Matters:**
- Average e-commerce funnels leak 50-75% of traffic at each stage
- A 2% improvement in conversion rate = 20-40% revenue increase (without scaling traffic)
- Most businesses optimize blindly without attribution; this skill connects traffic source → conversion rate → revenue impact
- Delivers ROI on fixes within 2-4 weeks typically

**Integrations & Data Sources:**
- Google Analytics 4 / Universal Analytics
- Facebook Pixel & Conversions API
- Shopify / WooCommerce / custom checkout endpoints
- Slack (for alerts on critical leaks)
- Segment / mParticle (optional data warehouse connections)
- Hotjar / Session Recording APIs (for friction detection)
- Typeform / Gravity Forms (form abandonment data)

---

## Quick Start

Try these prompts immediately:

### Example 1: E-Commerce Funnel Audit
```
Analyze my Shopify funnel from landing page to order confirmation.
Traffic sources: Google Ads, Facebook, organic search.
Last 30 days. Identify where most leads drop. What's the revenue impact 
if I fix the top 3 leaks?
```

### Example 2: SaaS Free Trial Leak Detection
```
My funnel: marketing site → pricing page → signup form → trial onboarding.
Users are abandoning at form. Use form analytics (Typeform API) to show 
which fields cause drop-off. Estimate impact of removing 2-3 fields.
```

### Example 3: Multi-Touch Attribution Analysis
```
Show me which traffic sources (Google Ads vs. organic vs. email) have 
lowest conversion rates at each funnel stage. Which channel should I 
deprioritize? Which has best ROAS potential if optimized?
```

### Example 4: Mobile vs. Desktop Breakdown
```
Funnel audit: separate mobile and desktop conversion paths. Which device 
type leaks more leads? Where specifically (form, checkout, trust signals)?
Recovery strategy with estimated revenue.
```

---

## Capabilities

### 1. **Funnel Stage Mapping & Leak Detection**
- Automatically identifies funnel stages (awareness → consideration → decision → purchase)
- Calculates drop-off rate per stage using GA4, FB Pixel, or custom event data
- Flags statistically significant leaks (>10% unexpected drop)
- **Example Output:**
  ```
  Stage: Landing Page → Product Page
  Drop-off: 45% (industry avg 30%)
  Estimated leak: 1,500 leads/month
  Primary cause: Slow page load (3.2s), high bounce rate on mobile
  ```

### 2. **Traffic Source Attribution & Channel Performance**
- Ingests multi-touch attribution (first-click, last-click, linear, time-decay models)
- Compares conversion rates by source (Google Ads, Facebook, organic, email, referral)
- Identifies underperforming channels with highest traffic spend
- Shows cost-per-conversion by source and stage
- **Example Output:**
  ```
  Channel: Facebook Ads
  Total traffic: 12,000 / month
  Landing page CR: 8% (vs. 12% organic avg)
  Estimated lost revenue: $18K/month
  Root cause: Audience targeting too broad, message mismatch
  ```

### 3. **Root Cause Diagnosis**
- **Form Friction:** Field count, required vs. optional, error messaging, mobile responsiveness
- **Messaging Misalignment:** Landing page promise vs. product page reality (headline, CTA, imagery)
- **Trust Gaps:** Missing reviews, security badges, testimonials, guarantees, creator credibility
- **Technical Issues:** Page speed, broken links, 404s, mobile layout problems
- **Psychological Blockers:** Price shock, unclear value prop, objection handling, urgency/scarcity

### 4. **Revenue Impact Quantification**
- Calculates current conversion funnel revenue
- Estimates revenue recovery per fix based on industry benchmarks
- Prioritizes fixes by impact (highest ROI first)
- **Example:**
  ```
  Fix #1: Reduce form fields from 8 to 4 (est. +3% signup CR)
  Potential recovery: $12K/month
  Effort: 2 hours
  
  Fix #2: Add 3 customer testimonials above CTA button (est. +2% conversion)
  Potential recovery: $8K/month
  Effort: 1 week
  ```

### 5. **Device/Segment Breakdown**
- Mobile vs. desktop conversion comparison
- Geographic performance (if available)
- Device type (iOS, Android, Chrome, Safari)
- Browser compatibility issues
- Screen size-specific friction points

### 6. **Post-Purchase Funnel Analysis**
- Abandoned cart recovery opportunities
- Post-purchase email engagement
- Customer lifetime value by acquisition source
- Repeat purchase rates by traffic source
- Refund/churn risk analysis

---

## Configuration

### Environment Variables (Required)

```bash
# Google Analytics 4
export GOOGLE_ANALYTICS_PROPERTY_ID="12345678"
export GOOGLE_ANALYTICS_API_KEY="your_service_account_key.json"

# Facebook Pixel & Conversions API
export FACEBOOK_PIXEL_ID="123456789"
export FACEBOOK_ACCESS_TOKEN="your_token_here"

# Shopify (if applicable)
export SHOPIFY_STORE_URL="https://yourstore.myshopify.com"
export SHOPIFY_API_TOKEN="your_token"
export SHOPIFY_API_KEY="your_key"

# Session Recording / Heatmap (optional)
export HOTJAR_SITE_ID="your_id"
export HOTJAR_API_TOKEN="your_token"

# Slack Notifications (optional)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Date range & timezone
export FUNNEL_START_DATE="2024-01-01"
export FUNNEL_END_DATE="2024-01-31"
export TIMEZONE="America/New_York"
```

### Setup Instructions

1. **Create GA4 Service Account:**
   - Go to Google Cloud Console → Create service account
   - Download JSON key, set as `GOOGLE_ANALYTICS_API_KEY`
   - Grant "Editor" role on GA4 property

2. **Get Facebook Pixel Data:**
   - Retrieve Pixel ID from Business Manager
   - Generate access token with `ads_management` scope
   - Ensure conversion tracking is enabled

3. **Connect Checkout Data:**
   - For Shopify: Generate private app with order/product read permissions
   - For WooCommerce: Install WooCommerce REST API, enable custom headers
   - For custom funnel: Provide webhook endpoint that logs funnel events

4. **Enable Enhanced Ecommerce Tracking (GA4):**
   - Ensure purchase, add_to_cart, view_item events are firing
   - Include item_id, item_name, item_category, price, quantity in events

---

## Example Outputs

### Full Funnel Audit Report

```json
{
  "funnel_analysis": {
    "report_date": "2024-01-15",
    "date_range": "2024-01-01 to 2024-01-31",
    "total_users": 45230,
    "revenue": "$187,500",
    "conversion_rate": "2.1%",
    "stages": [
      {
        "name": "Landing Page",
        "users": 45230,
        "dropoff_rate": "28%",
        "next_stage_users": 32566,
        "severity": "HIGH",
        "root_cause": "Mobile UX issue - form field errors on iOS Safari"
      },
      {
        "name": "Product Page",
        "users": 32566,
        "dropoff_rate": "35%",
        "next_stage_users": 21168,
        "severity": "CRITICAL",
        "root_cause": "Price objection - $49/month feels high vs. competitors. Missing ROI calculator."
      },
      {
        "name": "Checkout Page",
        "users": 21168,
        "dropoff_rate": "15%",
        "next_stage_users": 17993,
        "severity": "MEDIUM",
        "root_cause": "3-step checkout process. Shipping cost reveal shock at step 2."
      },
      {
        "name": "Order Confirmation",
        "users": 17993,
        "conversion": "Yes"
      }
    ]
  },
  "attribution_by_source": [
    {
      "source": "Google Ads",
      "traffic": 18500,
      "landing_page_cr": "42%",
      "product_page_cr": "61%",
      "checkout_cr": "82%",
      "overall_conversion": "2.8%",
      "cost_per_conversion": "$28",
      "status": "HEALTHY"
    },
    {
      "source": "Facebook Ads",
      "traffic": 15200,
      "landing_page_cr": "31%",
      "product_page_cr": "45%",
      "checkout_cr": "75%",
      "overall_conversion": "1.1%",
      "cost_per_conversion": "$62",
      "status": "UNDERPERFORMING",
      "recommendation": "Audience targeting too broad. Narrow by purchase intent keyword interest."
    },
    {
      "source": "Organic Search",
      "traffic": 9800,
      "landing_page_cr": "78%",
      "product_page_cr": "71%",
      "checkout_cr": "88%",
      "overall_conversion": "4.9%",
      "cost_per_conversion": "$0",
      "status": "BEST_PERFORMER"
    }
  ],
  "revenue_recovery_plan": [
    {
      "rank": 1,
      "fix": "Optimize mobile checkout - remove optional fields",
      "current_impact": "35% checkout drop-off on mobile (9K users/month)",
      "estimated_improvement": "+8% checkout CR",
      "potential_revenue_recovery": "$18400/month",
      "effort": "8 hours engineering",
      "timeline": "5 days"
    },
    {
      "rank": 2,
      "fix": "Add ROI calculator to product page",
      "current_impact": "35% product page drop-off",
      "estimated_improvement": "+6% product page CR",
      "potential_revenue_recovery": "$12600/month",
      "effort": "3 days dev + 2 days copy",
      "timeline": "14 days"
    },
    {
      "rank": 3,
      "fix": "Retarget Facebook traffic with price-justified messaging",
      "current_impact": "Facebook only 1.1% conversion vs. 2.8% Google Ads",
      "estimated_improvement": "+1.5% conversion on 15K FB traffic",
      "potential_revenue_recovery": "$8250/month",
      "effort": "4 hours copywriting + 2 hours ad setup",
      "timeline": "3 days"
    }
  ],
  "total_estimated_recovery": "$39,250/month",
  "implementation_cost": "~$2,000-3,000 (dev + tools)",
  "roi": "13x within 30 days"
}
```

---

## Tips & Best Practices

### 1. **Set Baseline Metrics First**
Before making changes, document current funnel health in a spreadsheet:
- Conversion rate per stage
- Drop-off rate per source
- Cost per acquisition
- Customer lifetime value
This creates a control to measure impact post-fix.

### 2. **Test One Change at a Time**
Don't optimize everything simultaneously. Use A/B testing:
- Control: existing funnel
- Variant: single change (e.g., reduced form fields OR new messaging)
- Sample size: 500+ conversions per variant minimum
- Duration: minimum 2 weeks (avoid day-of-week bias)

### 3. **Prioritize by Impact × Effort**
Use the 2×2 matrix:
- **Quick wins** (high impact, low effort): forms, copy, trust signals → do first
- **Strategic projects** (high impact, high effort): checkout redesign, new feature → do second
- **Low priority** (low impact, high effort): vanity improvements → skip

### 4. **Segment Your Audience**
- New vs. returning visitors behave differently
- Mobile-first users need different UX than desktop
- B2B (long consideration) vs. B2C (impulse) have different drop-off points
- Geographic markets (US, EU, APAC) have different trust markers

### 5. **Use Micro-Conversions**
Track leading indicators before final purchase:
- Email signup
- Demo request
- Free trial activation
- Add to cart
- Wishlist save
These predict purchase; optimize them first.

### 6. **Implement Event Tracking Properly**
Ensure your funnel data is clean:
```javascript
// Good event structure
gtag('event', 'add_to_cart', {
  currency: "USD",
  value: 49.99,
  items: [{
    item_id: "prod_123",
    item_name: "Premium Plan",
    item_category: "subscription"
  }]
});

// Bad (insufficient data)
gtag('event', 'purchase');
```

### 7. **Monitor Attribution Decay**
- First-click attribution gives credit to initial awareness (good for top-of-funnel fixes)
- Last-click attribution credits final touchpoint (good for bottom-of-funnel optimization)
- Use **time-decay model** (30-day window, exponential weight to recent touches) for most realistic view

---

## Safety & Guardrails

### This Skill WILL NOT:

- **Bypass user privacy/compliance** — Does not extract PII or violate GDPR/CCPA. Only aggregated, anonymized funnel data.
- **Make unilateral changes to your funnel** — Generates recommendations only. All implementation requires your approval and testing.
- **Guarantee results** — Provides estimates based on industry benchmarks and your data. Actual results depend on execution quality, market conditions, and external factors.
- **Recommend unethical tactics** — Will not suggest dark patterns (fake urgency, misleading claims, hidden fees), cookie walls, or predatory practices.
- **Assume causation from correlation** — May identify correlation between messaging and drop-off but requires your domain expertise to confirm root cause.

### Limitations:

- **Attribution window** — Limited to 30-day lookback default (configurable). Long sales cycles (>30 days) require custom model.
- **Data quality dependency** — Garbage in, garbage out. Requires proper event tracking implementation; misconfigured pixels = unreliable results.
- **API rate limits** — GA4 API has quota limits (~10K requests/day). Large funnels may require overnight batch processing.
- **Platform-specific blind spots** — Cross-device tracking (user on phone initially, converts on desktop) often missed by standard attribution.
- **External factors** — Cannot account for seasonality, competitor launches, PR events, or major product changes without manual context.

---

## Troubleshooting

### Q: "My conversion data looks wrong. Audit shows 0 purchases."
**A:** Likely cause: purchase event not implemented in GA4 or Facebook Pixel. Verify:
```javascript
// GA4 purchase event (required)
gtag('event',