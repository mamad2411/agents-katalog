---
name: ai-customer-churn-prediction-and-win-back-strategist
description: "Predict at-risk customers and generate personalized win-back strategies using behavioral signals. Use when the user needs churn prevention, customer retention campaigns, or re-engagement offers ranked by urgency."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","CUSTOMER_DATA_SOURCE"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🎯"}}
---

# AI Customer Churn Prediction & Win-Back Strategist

## Overview

This skill analyzes customer behavioral signals in real-time to identify at-risk customers **before they churn**, then generates hyper-personalized retention strategies and intervention recommendations. It integrates with your CRM, analytics platform, or customer database to surface declining engagement patterns, support ticket escalations, purchase frequency drops, and engagement decay—then automatically ranks customers by churn urgency and prescribes targeted win-back tactics.

**Why This Matters:**
- Acquiring new customers costs 5-25x more than retaining existing ones
- Early intervention can recover 30-50% of at-risk customers with the right offer
- Personalized retention messaging increases response rates by 3-4x vs. generic campaigns

**Integrations Supported:**
- **Stripe** (payment decline patterns, subscription churn)
- **Salesforce CRM** (opportunity pipeline, engagement scoring)
- **HubSpot** (contact activity, email engagement, deal stage)
- **Slack** (alert notifications for high-risk customers)
- **Google Analytics 4** (session frequency, scroll depth, time-on-site)
- **Intercom/Zendesk** (support ticket sentiment, response time)
- **WordPress/WooCommerce** (purchase history, cart abandonment)
- **Mailchimp/Klaviyo** (email open rates, unsubscribe patterns)

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Analyze a Single At-Risk Customer
```
Analyze this customer for churn risk:
- Name: Sarah Chen
- Signup: 18 months ago
- Last purchase: 47 days ago (was every 14 days)
- Support tickets (last 30 days): 3 (all unresolved)
- Email open rate: 12% (down from 45%)
- Subscription tier: Premium ($199/mo)
- Product usage: Logged in 2x in last 30 days (was 15x/month)

Generate a win-back strategy with specific offers and messaging.
```

### Example 2: Batch Churn Analysis from CSV
```
Import customer data from our Stripe export and:
1. Score all customers (0-100 churn risk)
2. Identify top 20 at-risk customers
3. For each, recommend ONE personalized intervention
4. Rank by revenue impact (highest LTV at risk first)
5. Generate a Slack notification template for our retention team

CSV columns: customer_id, email, ltv, days_since_purchase, support_tickets, engagement_score
```

### Example 3: Win-Back Campaign Builder
```
Create a 3-email win-back sequence for customers who:
- Haven't purchased in 60+ days
- Were previously high-engagement (>$500 LTV)
- Are in our SaaS product category

Include:
- Subject lines (A/B variants)
- Personalization tokens (first name, last product used)
- Specific re-engagement offers (discount %, free trial extension, feature unlock)
- Success metrics to track
- Send timing recommendations
```

---

## Capabilities

### 1. **Churn Risk Scoring**
Analyzes 15+ behavioral signals to assign a churn probability score (0-100):
- **Engagement decay**: Login frequency, feature usage, session duration
- **Purchase velocity**: Days since last order, order frequency trend, AOV decline
- **Support friction**: Unresolved tickets, response time, sentiment analysis
- **Email engagement**: Open rates, click rates, unsubscribe signals
- **Account health**: Subscription downgrades, payment method changes, API failures
- **Competitive signals**: Industry benchmarks, seasonal patterns, cohort trends

**Example Usage:**
```
Score these customers for churn risk:
Customer IDs: [1023, 4567, 8901, 12345]
Data source: Salesforce
Include engagement metrics from: last 90 days
Weight factors: Purchase recency (40%), Support tickets (25%), Email engagement (20%), Feature usage (15%)
Output format: JSON with risk score, primary risk factor, confidence level
```

### 2. **Personalized Retention Strategies**
Generates customized intervention plans based on churn root cause:

| Churn Signal | Recommended Action | Example Offer |
|---|---|---|
| High support friction | Dedicated support + training | Free premium support for 30 days |
| Price sensitivity | Targeted discount | 20% off for 3 months (auto-renew at full price) |
| Feature underutilization | Onboarding + feature unlock | Free advanced features demo + training |
| Competitive pressure | Value reinforcement | Exclusive loyalty reward + upgrade discount |
| Payment issues | Payment retry + assistance | Payment plan option + $25 credit |
| Engagement decay | Re-engagement sequence | "We miss you" campaign + limited-time bonus |

### 3. **Outreach Message Generation**
Creates subject lines, email copy, and messaging frameworks optimized for conversion:
- **A/B variants** for subject lines (curiosity vs. benefit-driven)
- **Personalization tokens** (name, product, last purchase, discount code)
- **Urgency signals** (limited-time offer, exclusive access, deadline)
- **Social proof** (testimonials, success stories, user count)
- **CTA optimization** (single clear action, benefit-focused button copy)

### 4. **Intervention Ranking by Urgency**
Prioritizes customers by revenue impact and intervention success likelihood:
```
Priority = (Customer LTV × Churn Probability × Intervention Success Rate) / Implementation Cost
```
Outputs a ranked action list so your team focuses on highest-ROI customers first.

### 5. **Campaign Automation Templates**
Generates ready-to-deploy templates for:
- Email sequences (1-7 touches)
- SMS/push notification scripts
- In-app messaging copy
- Slack/Teams alerts for your team
- Salesforce workflow rules
- HubSpot automation workflows

---

## Configuration

### Required Environment Variables
```bash
# OpenAI API for analysis and content generation
OPENAI_API_KEY=sk-...

# Your primary customer data source (choose one)
CUSTOMER_DATA_SOURCE=stripe|salesforce|hubspot|custom_api

# API credentials for your data source
STRIPE_API_KEY=sk_live_...
SALESFORCE_ORG_ID=00D...
HUBSPOT_API_KEY=pat-...
CUSTOM_API_URL=https://api.yourcompany.com/customers

# Optional: Slack alerts for high-risk customers
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Optional: Email provider for campaign deployment
MAILCHIMP_API_KEY=...
KLAVIYO_API_KEY=...
```

### Configuration Options
```yaml
churn_analysis:
  lookback_period_days: 90        # Analyze last 90 days of behavior
  risk_score_threshold: 65        # Flag customers scoring 65+
  min_customer_ltv: 100           # Only analyze customers worth $100+
  
retention_strategy:
  intervention_types:
    - email_sequence
    - discount_offer
    - feature_unlock
    - support_upgrade
    - loyalty_reward
  
  personalization_depth: high     # Use behavioral data for customization
  
output:
  format: json|csv|slack_message
  include_confidence_scores: true
  rank_by: revenue_impact|churn_probability|success_likelihood
```

---

## Example Outputs

### Output 1: Individual Customer Risk Assessment
```json
{
  "customer_id": "cus_K8x9Y2p1Q",
  "email": "sarah.chen@example.com",
  "name": "Sarah Chen",
  "churn_risk_score": 78,
  "churn_probability": "HIGH (78% likely to churn in next 60 days)",
  "primary_risk_factors": [
    {
      "factor": "Purchase frequency decline",
      "severity": "CRITICAL",
      "detail": "Last purchase 47 days ago (was every 14 days)",
      "weight": "40%"
    },
    {
      "factor": "Support ticket backlog",
      "severity": "HIGH",
      "detail": "3 unresolved tickets in last 30 days, avg resolution 8 days",
      "weight": "25%"
    },
    {
      "factor": "Email disengagement",
      "severity": "MEDIUM",
      "detail": "Open rate 12% (down from 45%), last click 23 days ago",
      "weight": "20%"
    }
  ],
  "customer_ltv": "$2,847",
  "revenue_at_risk": "$2,847",
  "recommended_intervention": {
    "type": "support_upgrade + limited_discount",
    "offer": "Free premium support for 30 days + 15% off next order",
    "expected_recovery_rate": "42%",
    "success_confidence": "HIGH",
    "implementation_cost": "Low (email + support ticket routing)",
    "estimated_roi": "6.2x"
  },
  "outreach_template": {
    "subject_line": "Sarah, we're here to help—and we have something special for you",
    "preview_text": "Your dedicated support hero + 15% off. Let's get you back on track.",
    "send_channel": "email",
    "send_timing": "Tuesday 10am (optimal for this segment)",
    "followup_cadence": "Email 1 (Day 0), SMS (Day 3), Email 2 (Day 7)"
  }
}
```

### Output 2: Batch Churn Report (Top 10 At-Risk)
```
CHURN RISK REPORT — Generated 2024-01-15
============================================

Cohort: All active customers (n=4,230)
Analysis Period: Last 90 days
High-Risk Customers (score 65+): 287 (6.8%)
Total Revenue at Risk: $412,847

TOP 10 HIGHEST-PRIORITY INTERVENTIONS:
Rank | Customer | LTV | Risk | Primary Factor | Recommended Action | Est. Recovery
-----|----------|-----|------|----------------|-------------------|---------------
1    | cus_K8x9 | $2,847 | 78% | Support friction | Premium support + 15% off | 42%
2    | cus_M2p3 | $1,923 | 76% | Price sensitivity | 20% discount (3mo) | 38%
3    | cus_Q5r8 | $5,120 | 74% | Feature underuse | Advanced features + training | 51%
4    | cus_L9t2 | $847 | 72% | Engagement decay | Re-engagement sequence | 35%
5    | cus_P1v4 | $3,456 | 71% | Competitive pressure | Loyalty upgrade + bonus | 44%
...
```

### Output 3: Win-Back Email Sequence
```
SUBJECT: Sarah, we're here to help—and we have something special for you

EMAIL 1 (Day 0 — Hook):
---
Hi Sarah,

We noticed you haven't placed an order in a while, and we wanted to check in.

Our support team saw you had a few questions recently, and we want to make 
sure you're getting the most out of your Premium plan. You deserve it.

**Here's what we're offering:**
→ 30 days of FREE premium support (dedicated to you)
→ 15% off your next order (code: COMEBACK15)
→ Free 1-on-1 onboarding session with our product specialist

Your account is too valuable to lose. Let's get you back to winning.

[BUTTON: Claim My Support + Discount]

Best,
The [Company] Team

---

EMAIL 2 (Day 3 — Follow-up via SMS):
"Hi Sarah—did you see our offer? 30 days free support + 15% off. 
Reply YES to claim it, or click: [link]"

EMAIL 3 (Day 7 — Final push):
Subject: Sarah, your 15% offer expires in 48 hours

---

SUCCESS METRICS TO TRACK:
- Email open rate (target: 35%+)
- Click-through rate (target: 8%+)
- Discount redemption rate (target: 15%+)
- Reactivation rate (target: 40%+)
- Revenue recovered (target: $427+)
```

---

## Tips & Best Practices

### 1. **Data Quality is Critical**
- Ensure your CRM/database timestamps are accurate (last_purchase, last_login, etc.)
- Sync customer data at least weekly (ideally daily)
- Include all behavioral data: support tickets, email engagement, feature usage
- **Tip**: Run a data audit before your first analysis to identify gaps

### 2. **Segment Before You Segment**
- Analyze churn patterns by customer segment (industry, product tier, cohort)
- Different segments have different churn drivers
- **Example**: SaaS customers churn on feature gaps; e-commerce on price/shipping
- Create segment-specific intervention strategies rather than one-size-fits-all

### 3. **Timing is Everything**
- Intervene at the **earliest** churn signal (don't wait for cancellation notice)
- Best engagement windows: Tuesday-Thursday, 9-11am or 6-8pm
- **Avoid**: Mondays (low engagement), weekends (lower conversion)
- Use historical data to find YOUR audience's optimal send time

### 4. **Personalization > Generics**
- Generic "we miss you" emails have <5% conversion
- Personalized offers based on churn cause have 20-40% conversion
- Reference specific product usage or purchase history
- **Example**: "You loved our Premium Analytics feature—here's an exclusive upgrade"

### 5. **Test and Iterate**
- A/B test subject lines (curiosity vs. benefit-driven)
- Test discount levels (15% vs. 20% vs. free shipping)
- Test channels (email vs. SMS vs. in-app)
- Track what works and double down

### 6. **Combine with Proactive Support**
- Don't just send offers—fix underlying issues
- If support friction is the driver, assign a dedicated support person
- If feature underutilization is the issue, offer training
- **Offers without solutions = wasted marketing spend**

### 7. **Monitor Post-Intervention**
- Track reactivation for 30-60 days after intervention
- Measure repeat purchase rate (not just initial recovery)
- Calculate true ROI: (Revenue recovered - Campaign cost) / Campaign cost
- Use learnings to refine future campaigns

---

## Safety & Guardrails

### What This Skill WILL NOT Do

❌ **Make final business decisions** — Recommendations are data-informed suggestions, not guarantees. Your team must validate strategy before deployment.

❌ **Guarantee customer recovery** — Churn prediction is probabilistic, not deterministic. External factors (competitor acquisition, budget cuts, company pivots) can override recommendations.

❌ **Access customer data without permission** — You must have explicit access to customer data and comply with GDPR, CCPA, and regional privacy laws.

❌ **Override customer preferences** — Respects unsubscribe lists, do-not-contact flags, and communication preferences. Will NOT send unsolicited messages.

❌ **Make promises on behalf of your company** — Generated messaging must be reviewed by your team before deployment. Ensure offers are valid and legally binding.

❌ **Discriminate or profile** — Will not make recommendations based on protected characteristics (race, gender, religion, etc.). Focuses solely on behavioral and transactional signals.

### Limitations & Boundaries

⚠️ **Data freshness**: Churn predictions degrade over time. Refresh analysis weekly for optimal accuracy.

⚠️ **Segment size**: Requires minimum 50 customers per segment for statistically significant patterns.

⚠️ **Historical bias**: Model learns from past churn patterns. If your company recently changed pricing/product, historical data may not reflect current churn drivers.

⚠️ **External factors**: Cannot account for market