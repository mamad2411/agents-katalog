---
name: conversion-rate-audit-specialist-by-traffic-source
description: "Analyze conversion funnels by traffic source (organic, paid, referral, direct) with drop-off identification, true CAC calculations including platform fees, and channel-specific optimization recommendations prioritized by revenue impact."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["GOOGLE_ANALYTICS_API_KEY","FACEBOOK_PIXEL_ID","SHOPIFY_API_TOKEN","STRIPE_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📊"}}
---

## Overview

The **Conversion Rate Audit Specialist by Traffic Source** is a comprehensive analytics automation skill designed for e-commerce teams and digital marketers who need to understand exactly where each traffic channel (organic, paid search, social, referral, direct) loses customers in the conversion funnel.

This skill goes beyond surface-level metrics. It:
- **Maps complete conversion journeys** by traffic source using Google Analytics 4 data
- **Identifies funnel drop-off points** at each stage (landing → product → cart → checkout → purchase)
- **Calculates true Customer Acquisition Cost (CAC)** including ad platform fees, landing page infrastructure, and attribution modeling
- **Generates channel-specific recommendations** based on data patterns (e.g., "Organic traffic bounces at product detail pages—improve reviews section")
- **Prioritizes improvements** by revenue impact and implementation effort
- **Integrates with Shopify, WooCommerce, Stripe, Google Analytics 4, Facebook Pixel, and Slack** for seamless workflows

Perfect for e-commerce stores with $10K–$10M annual revenue who want to stop wasting marketing budget on underperforming channels and instead optimize each source individually.

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Full Audit for Your Store
```
Audit conversion rates by traffic source for my Shopify store. 
I get ~5,000 visitors/month: 40% organic, 35% paid ads, 15% referral, 10% direct.
Organic converts at 2.5%, paid at 4.2%, referral at 6.1%, direct at 8%.
Show me where each source drops off and recommend 3 quick wins.
```

### Example 2: CAC Deep-Dive with Platform Fees
```
Calculate true CAC by traffic source including:
- Google Ads spend: $2,400/month (for organic-looking traffic)
- Facebook/Instagram spend: $1,800/month
- Affiliate commissions: 8% of referral sales
- Landing page hosting & tools: $150/month
- Attribution window: 30 days
Current monthly revenue: $28,000. Show CAC vs. AOV by channel.
```

### Example 3: Checkout Flow Analysis
```
My Shopify checkout abandonment is different by source:
- Organic: 68% abandon (often at payment info)
- Paid: 72% abandon (often at shipping cost reveal)
- Referral: 55% abandon (mostly complete checkout)
- Direct: 59% abandon (even across steps)
Tell me what's wrong with each funnel and what to A/B test first.
```

### Example 4: Optimization Roadmap
```
Create a 90-day optimization roadmap for my traffic sources.
Prioritize by revenue impact, not just conversion rate.
Include specific changes: landing page, product page, checkout flow.
Timeline: what should I do weeks 1-4, 5-8, 9-12?
```

---

## Capabilities

### 1. **Conversion Funnel Mapping by Source**
Automatically pulls data from Google Analytics 4 or your data warehouse and maps the complete conversion journey:
- Sessions → Landing page impression → Product view → Add to cart → Initiate checkout → Purchase
- Calculates conversion rate at each step **per traffic source**
- Identifies the single biggest drop-off point for each channel
- Example output: "Organic traffic: 2.1% loss at product page (reviews missing), 3.8% loss at checkout (shipping cost shock)"

### 2. **True CAC Calculation Engine**
Goes beyond "ad spend ÷ conversions" with complete cost visibility:
- **Direct platform costs**: Google Ads, Facebook, TikTok, LinkedIn spend
- **Platform fees**: 2.9% payment processing (Stripe/PayPal), affiliate commissions
- **Indirect costs**: Landing page builders, email tools, analytics platforms (allocated monthly)
- **Attribution modeling**: First-touch, last-touch, linear, time-decay options
- **Outputs**: CAC by source, CAC vs. Average Order Value, payback period per channel

### 3. **Drop-Off Analysis & Root Cause Detection**
Uses behavioral signals to identify *why* users leave:
- **Traffic source cohort behavior**: Paid users have different cart abandonment triggers than organic
- **Device/platform patterns**: Mobile vs. desktop drop-off differences by source
- **Time-on-page analysis**: Which pages are friction points for which channels
- **Comparison to benchmarks**: How you stack up vs. industry standards (Shopify, WooCommerce benchmarks)
- **Suggests interventions**: "Direct traffic drops at checkout—add guest checkout option" or "Organic bounces on landing—improve headline clarity for search intent"

### 4. **Channel-Specific Optimization Roadmap**
Prioritized recommendations tailored to each source:
- **Organic traffic**: Improve product reviews, internal linking, site speed, clear value proposition
- **Paid search (Google Ads)**: Optimize landing page for keyword intent, reduce form fields, improve ad relevance score
- **Social ads (Facebook/Instagram)**: Add urgency/scarcity, simplify checkout, retarget cart abandoners
- **Referral**: Improve affiliate creatives, add referral incentives, track partner performance
- **Direct**: Strengthen email nurturing, reduce checkout steps, improve email CTAs

### 5. **Revenue Impact Scoring**
Ranks improvements by estimated ROI:
- **Impact**: Revenue change × likelihood of success × months to full rollout
- **Effort**: Development hours, testing time, implementation complexity
- **Priority score**: Impact ÷ Effort (so you do high-leverage work first)
- Example: "Improving organic product page reviews: $4,200/month impact, 20 hours effort, priority score 8.8/10 ← DO FIRST"

### 6. **Slack & Email Integration**
Automatically delivers:
- Weekly conversion trend reports by source
- Alert when a channel's conversion rate drops >20%
- Monthly optimization recommendations
- A/B test result summaries

---

## Configuration

### Required Environment Variables
```bash
# Google Analytics 4
export GOOGLE_ANALYTICS_API_KEY="ya29.a0AfH6SMB..."
export GA4_PROPERTY_ID="properties/123456789"

# Shopify (if using Shopify store)
export SHOPIFY_API_TOKEN="shpat_abc123def456..."
export SHOPIFY_STORE_URL="your-store.myshopify.com"

# Stripe (for payment data)
export STRIPE_API_KEY="sk_live_abc123def456..."

# Facebook Pixel (optional, for pixel-based conversion tracking)
export FACEBOOK_PIXEL_ID="987654321"

# Slack Integration (optional, for alerts)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

### Setup Steps
1. **Grant API access**: Go to Google Analytics → Admin → API & Services, create a service account, download JSON key
2. **Connect Shopify**: Apps → Custom apps → Create app → Admin API scopes (read orders, read customers)
3. **Connect Stripe**: Account settings → API Keys → Copy secret key
4. **Configure date range**: Default is last 90 days; adjust with `--days 180` flag
5. **Set attribution window**: Default 30 days; change with `--attribution-window 14` for shorter windows

### Optional Configuration Files
Create `conversion_audit_config.json` to customize:
```json
{
  "traffic_sources": ["organic", "paid", "referral", "direct", "email"],
  "funnel_stages": ["landing", "product_view", "add_to_cart", "checkout_start", "purchase"],
  "benchmarks": "shopify",
  "attribution_model": "last_touch",
  "currency": "USD",
  "slack_enabled": true,
  "report_frequency": "weekly"
}
```

---

## Example Outputs

### Sample Audit Report
```
═══════════════════════════════════════════════════════════════
CONVERSION RATE AUDIT BY TRAFFIC SOURCE | Last 90 Days
═══════════════════════════════════════════════════════════════

📊 FUNNEL OVERVIEW
─────────────────────────────────────────────────────────────
                   Sessions  → Landing  → Product  → Cart    → Checkout → Purchase
Organic           2,847     → 2,798    → 1,889    → 284     → 86       → 76 (2.67%)
Paid Search       1,623     → 1,612    → 1,204    → 412     → 127      → 69 (4.25%)
Social Referral   745       → 741      → 612      → 215     → 142      → 89 (11.95%)
Direct            387       → 385      → 301      → 68      → 42       → 33 (8.53%)

💰 TRUE COST PER ACQUISITION (CAC)
─────────────────────────────────────────────────────────────
Organic:      $18.40  [Monthly site cost: $1,400 ÷ 76 conversions]
Paid Search:  $34.78  [Ad spend: $2,400 + fees ÷ 69 conversions]
Social Referral: $12.00 [Affiliate 8% commission only]
Direct:       $42.35  [No channel cost; attribution to existing brand]

🎯 BIGGEST DROP-OFF POINTS
─────────────────────────────────────────────────────────────
❌ Organic:     34% drop at product page (reviews section missing)
❌ Paid Search: 31% drop at checkout (shipping cost surprise)
❌ Social:      10% drop at checkout (payment options unclear)
❌ Direct:      22% drop at cart (price concerns + complexity)

✅ TOP 3 QUICK WINS (Ranked by Revenue Impact)
─────────────────────────────────────────────────────────────
1. Add 50+ star reviews to top 10 products (organic +$4,200/mo, 20h effort) → Priority 8.8
2. Show shipping cost BEFORE cart (paid -$2,800/mo abandonment, 8h effort) → Priority 7.2
3. Add guest checkout option (organic +$1,600/mo, 12h effort) → Priority 5.3
```

### 90-Day Optimization Roadmap
```
WEEKS 1-4: Foundation Fixes
├─ Add product reviews widget (1.5 weeks, +2.5% organic conversion)
├─ Implement pre-checkout shipping calculator (1 week, -$2,800/mo abandonment)
└─ Enable guest checkout (0.5 weeks, +1.2% all channels)

WEEKS 5-8: Channel Optimization
├─ Organic: Improve product descriptions + internal linking
├─ Paid: Redesign landing pages for keyword intent
└─ Social: Add urgency badges + testimonials

WEEKS 9-12: Testing & Refinement
├─ A/B test 3 checkout flows (highest impact first)
├─ Retargeting campaign for cart abandoners by source
└─ Analytics review + next quarter planning
```

---

## Tips & Best Practices

### 1. **Segment by Device & Geography**
Don't assume all organic traffic behaves the same. Mobile organic users may have different drop-off patterns than desktop. Add `--segment-by device,country` to your audit command.

### 2. **Use Cohort Analysis**
Compare new vs. returning users by traffic source. Paid traffic often converts better on first visit (high intent), while organic may convert better on repeat visits (high familiarity).

### 3. **Watch Your Attribution Window**
A 30-day attribution window works for fashion and impulse buys. B2B SaaS may need 90+ days. Use `--attribution-window 90` to match your sales cycle.

### 4. **Track UTM Parameters Consistently**
Ensure your paid ads always include `?utm_source=facebook&utm_medium=cpc&utm_campaign=summer-sale`. Without clean UTM data, the audit cannot accurately bucket conversions by source.

### 5. **Calculate Customer Lifetime Value (CLV) by Source**
Not all conversions are equal. A referred customer might have 2.3x lifetime value of a paid search customer. Ask the skill to calculate CLV-adjusted CAC with `--include-ltv`.

### 6. **Run Audits Monthly**
E-commerce seasonality, competitive changes, and platform algorithm shifts happen fast. Schedule monthly audits and compare trends quarter-over-quarter.

### 7. **Test One Variable at a Time**
Implement top recommendations in sequence, not all at once. Wait 2–4 weeks before measuring impact so you know which change drove improvement.

### 8. **Benchmark Against Your Historical Performance**
Compare this month's organic conversion rate to last month's, not to Shopify average. Your baseline matters more than industry standard.

---

## Safety & Guardrails

### What This Skill Will NOT Do
- **Make purchasing decisions for you.** Recommendations are data-driven suggestions, not guarantees. Always validate with your own business logic.
- **Guarantee conversion rate improvements.** Results depend on implementation quality, market conditions, and customer behavior—factors outside the skill's control.
- **Access customer personal data beyond aggregate metrics.** The skill only reads conversion funnel data, not individual customer records or PII.
- **Modify your store directly.** This is an analysis and recommendation tool, not an automation tool. You retain full control over what changes are implemented.
- **Work with incomplete data.** If you have <30 days of data or <50 conversions per source, the audit will flag results as unreliable.

### Data Privacy & Compliance
- GDPR compliant: Works only with anonymized, aggregated analytics data
- CCPA compliant: Does not access or store individual customer records
- SOC 2 ready: API keys are never logged or stored in plain text
- Supports anonymized Google Analytics 4 data by default

### Limitations
- **Requires GA4 or Shopify API access.** WooCommerce stores need manual data upload (CSV format)
- **Attribution is probabilistic, not deterministic.** Multi-touch attribution models are estimates based on historical patterns
- **Does not account for offline conversions** unless you manually import them
- **Requires minimum traffic volume.** Channels with <50 conversions/month may show unreliable conversion rates
- **Industry benchmarks are Shopify/WooCommerce focused.** If you're on a custom platform, bring your own benchmarks

---

## Troubleshooting

### Common Issues & Solutions

#### Q: "GA4 API returns 403 Forbidden"
**A:** Your service account doesn't have the right permissions.
- Go to Google Analytics → Admin → Property Access Management
- Add your service account email (`...-...-...@...iam.gserviceaccount.com`) as "Viewer"
- Wait 5 minutes for permissions to sync
- Regenerate your JSON key file

#### Q: "Conversion rates don't match my dashboard"
**A:** Attribution window mismatch.
- The skill defaults to 30-day last-touch attribution
- Your dashboard may use different settings (7-day, first-touch, 90-day window)
- Use `--attribution-window 7 --model first_touch` to match your dashboard
- Cross-check your date range (inclusive vs. exclusive of end date)

#### Q: "Paid search conversions seem low. Am I missing something?"
**A:** Verify your UTM parameters.
- Check a recent paid ad in your browser → right-click → View Page Source
- Search for `utm_source=` and `utm_campaign=`
- If missing, GA4 won't attribute that conversion to "Paid Search"; it'll go to "Direct"
- Update ad templates to always include UTMs

#### Q: "Shopify API token is valid, but skill won't connect"
**A:** Custom app scope issue.
- Go to Apps → Custom apps → [Your App] → Configuration
- Verify these Admin API scopes are enabled:
  - `read_orders`
  - `read_customers`
  - `read_products`
-