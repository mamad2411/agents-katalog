---
name: pricing-psychology-optimizer
description: "Analyze and optimize pricing strategies using psychological principles like charm pricing, anchoring, and scarcity framing. Use when the user needs A/B test recommendations, pricing audits, or conversion lift predictions for SaaS, courses, and digital products."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "BROWSER_AUTOMATION_KEY"],
        "bins": ["curl", "node"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "💰"
    }
  }
---

# Pricing Psychology Optimizer

## Overview

The Pricing Psychology Optimizer is an expert-level pricing strategy analyzer that audits your product pages, landing pages, and checkout flows against proven psychological pricing principles. This skill helps SaaS companies, course creators, digital product businesses, and agencies discover hidden conversion lift opportunities by identifying suboptimal pricing presentation patterns.

**Why This Matters:** Research shows that 71% of purchasing decisions are influenced by perceived value and pricing presentation, not just price alone. Small changes to how you present pricing can yield 15-40% conversion improvements without discounting.

**What You Get:**
- **Comprehensive Pricing Audits** — Analyzes your current pricing pages against 12+ psychological pricing frameworks
- **Specific A/B Test Recommendations** — Ranked by predicted lift potential and implementation complexity
- **Competitive Benchmarking** — Compares your pricing presentation to industry leaders
- **Multi-Channel Integration** — Supports WordPress, Shopify, Stripe checkout flows, and custom landing pages
- **Priority Implementation Guide** — Quick wins first, then strategic optimizations
- **Conversion Lift Predictions** — Data-backed estimates for each recommendation

**Integrations:** WordPress, Stripe, Shopify, Webflow, ConvertKit, Gumroad, Slack (for reporting), Google Sheets (for tracking results)

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Basic SaaS Pricing Audit
```
Analyze my SaaS pricing page and audit it against pricing psychology principles.
My pricing page URL is: https://example.com/pricing
My current tiers are: Starter ($29/mo), Professional ($99/mo), Enterprise (custom)
What psychological pricing techniques am I missing?
```

### Example 2: Landing Page Conversion Optimization
```
I'm launching a digital course and need pricing psychology recommendations.
Landing page: https://example.com/course
Current price: $497 (one-time payment)
Target audience: Solopreneurs and small business owners
My main competitor charges $399 for a similar course.
Give me 5 A/B test recommendations ranked by predicted lift.
```

### Example 3: Checkout Flow Analysis with Competitive Comparison
```
Audit my Stripe checkout process for pricing psychology gaps.
Checkout URL: https://checkout.example.com/product
Current presentation: Single price $199, no payment plan option
Competitors: 3 similar products at $149, $199, $249
Generate specific A/B tests with implementation priority and predicted conversion lift.
```

### Example 4: Payment Plan Optimization
```
Help me optimize payment plans for my $2,997 course.
Current offer: $2,997 upfront only
Considering: 3x payment plan at $999/month
Analyze this against psychological anchoring and payment friction principles.
What specific messaging changes will maximize uptake?
```

---

## Capabilities

### 1. Psychological Pricing Principle Audits
The skill analyzes your pricing against these proven frameworks:

- **Charm Pricing** — Price endings (.99, .95) vs whole numbers for different segments
- **Anchoring Effect** — Using high reference prices to justify value
- **Decoy Pricing** — Three-tier strategy positioning (good/better/best)
- **Bundling Psychology** — Perceived value multiplication through bundling
- **Scarcity Framing** — Limited-time offers, stock indicators, urgency messaging
- **Payment Friction Reduction** — One-click checkout, saved payment methods, financing options
- **Social Proof Integration** — Customer count, testimonial placement, logo display
- **Loss Aversion Framing** — "Don't miss out" vs "Get access" messaging
- **Price-Value Alignment** — Feature-to-price ratio analysis
- **Comparison Optimization** — Feature comparison tables that drive selection
- **Risk Reversal** — Money-back guarantees, trial periods, satisfaction promises
- **Time-Limited Incentives** — Early-bird pricing, launch window scarcity

### 2. A/B Test Recommendation Engine
Generates prioritized test recommendations including:
- **Test Name & Hypothesis** — Clear, testable prediction
- **Implementation Complexity** — Low (1-2 hours), Medium (half-day), High (1-2 days)
- **Predicted Lift** — Estimated conversion improvement (15-40% typical range)
- **Sample Size & Duration** — Statistical significance requirements
- **Success Metrics** — What to measure and how to validate
- **Implementation Steps** — Exact CSS/copy changes needed

### 3. Multi-Page Analysis
Audit across your entire conversion funnel:
- Landing pages
- Product pages
- Pricing pages
- Checkout flows
- Payment confirmation pages
- Email sequences (opt-in to pricing communications)

### 4. Competitive Intelligence
```
Compare your pricing presentation to 3-5 direct competitors.
Provides: pricing strategy patterns, messaging frameworks, 
feature positioning, payment option differences
```

### 5. Conversion Lift Prediction Model
Generates estimated lift based on:
- Current conversion rate baseline
- Improvement magnitude of recommended change
- Industry benchmarks for your product category
- Statistical significance thresholds
- Time to implement vs. time to test

### 6. Batch Analysis & Reporting
Export full reports including:
- Priority matrix (quick wins vs. strategic plays)
- Implementation roadmap (Week 1, Month 1, Quarter 1)
- Slack notifications for completed audits
- Google Sheets tracking for A/B test results
- CSV export for team collaboration

---

## Configuration

### Environment Variables
```bash
# Required
export OPENAI_API_KEY="sk-..."           # For analysis and recommendations
export BROWSER_AUTOMATION_KEY="..."      # For capturing live pricing pages

# Optional
export STRIPE_API_KEY="sk_live_..."      # For checkout flow analysis
export WORDPRESS_API_TOKEN="..."         # For WordPress site audits
export SHOPIFY_API_TOKEN="..."           # For Shopify store analysis
export SLACK_WEBHOOK_URL="https://..."   # For report delivery
export GOOGLE_SHEETS_API_KEY="..."       # For tracking A/B test results
```

### Skill Options
```yaml
# pricing-psychology-optimizer.config.yml
analysis_depth: "comprehensive"  # Options: quick, standard, comprehensive
industry_type: "saas"            # saas, course, digital_product, agency
target_conversion_lift: "25%"     # Your goal for A/B testing
competitor_count: 3              # How many competitors to analyze
include_mobile_analysis: true    # Mobile checkout optimization
include_email_recommendations: true  # Pricing email sequences
confidence_threshold: 0.85       # Statistical significance for predictions
```

### Quick Setup
1. Clone/fork the skill to your OpenClaw workspace
2. Set required environment variables (OPENAI_API_KEY minimum)
3. Run `openclawctl skill:validate pricing-psychology-optimizer`
4. Test with Quick Start examples above
5. Integrate with Slack or Google Sheets (optional but recommended)

---

## Example Outputs

### Full Pricing Audit Report
```
PRICING PSYCHOLOGY AUDIT REPORT
Generated: 2024-01-15 | Analyzed URLs: 3

OVERALL SCORE: 6.2/10 (Below Industry Average)

KEY FINDINGS:
✗ No charm pricing ($99 vs $100) — Quick win
✗ Two-tier pricing vs three-tier decoy — Medium effort, high impact
✗ No payment plan option — High demand feature
✓ Good use of social proof (2,340+ users)
✓ Clear feature comparison table
✗ Missing scarcity messaging on limited tier
✗ No money-back guarantee visible

PRIORITY 1 - QUICK WINS (Implement This Week):
1. Charm Pricing on All Tiers
   • Change: $99→$99, $199→$199, $599→$599 to $99, $199, $597
   • Effort: 1 hour (CSS/copy update)
   • Predicted Lift: +8-12%
   • Rationale: Psychological research shows .99 endings reduce price perception by ~12%

2. Add Money-Back Guarantee
   • Copy: "30-day money-back guarantee. No questions asked."
   • Placement: Below pricing button
   • Effort: 2 hours (legal review + implementation)
   • Predicted Lift: +6-15%
   • Rationale: Risk reversal removes barrier for fence-sitters

PRIORITY 2 - MEDIUM IMPACT (Implement This Month):
3. Introduce Three-Tier Decoy Strategy
   • Add "Professional Plus" tier at $349 (between current $199 and $599)
   • Anchors perception toward $599 "Enterprise" tier
   • Increases perceived value of mid-tier by 23%
   • Effort: Half-day
   • Predicted Lift: +12-18%

4. Add Payment Plans
   • Offer: 3x payment plan at $199→$66/mo
   • Reduces payment friction for price-sensitive segment
   • Effort: 1 day (Stripe integration)
   • Predicted Lift: +10-20% (for mid/high tier)

5. Scarcity Messaging
   • Add: "Only 12 Professional seats available this month"
   • Update dynamic counter (hide at capacity)
   • Effort: 4 hours
   • Predicted Lift: +5-8%

PRIORITY 3 - STRATEGIC (Implement Next Quarter):
6. Pricing Email Sequence
   • 5-email nurture sequence for price objections
   • Social proof, success stories, value reinforcement
   • Effort: 1-2 days
   • Predicted Lift: +15-25%

COMPETITIVE ANALYSIS:
Your Pricing:     Competitor A:     Competitor B:
$99/mo            $95/mo            $99/mo
$199/mo           $199/mo           $189/mo
$599/mo           $599/mo           $499/mo

Insight: You're pricing inline with Competitor A, but Competitor B gets 18% 
higher conversion. Their difference: 2-tier vs 3-tier strategy + payment plans.

SAMPLE SIZE & DURATION FOR A/B TESTS:
Recommended: 2-week test windows for each change
Statistical significance: 500+ conversions per variant
Current monthly volume: 3,200 visitors, 2.1% conversion = 67 conversions
Estimated test duration: 2-3 weeks per test

PREDICTED CUMULATIVE LIFT:
Week 1 (Quick wins 1-2): +12-25%
Month 1 (All Priority 1-2): +35-60%
Quarter 1 (All recommendations): +65-95%

Conservative estimate: $180K → $255K annual ARR (from pricing changes alone)
```

### A/B Test Recommendation Card
```
TEST #3: Three-Tier Decoy Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hypothesis: Introducing a middle "Professional Plus" tier at $349 
will anchor perception upward and increase Enterprise ($599) conversions 
by 18%, while maintaining Professional ($199) sales.

Implementation: 4-6 hours
Complexity: MEDIUM

Current Pricing Table:
┌──────────────┬─────────┬──────────────┐
│ Starter      │ Prof    │ Enterprise   │
│ $99/mo       │ $199/mo │ $599/mo      │
└──────────────┴─────────┴──────────────┘

New Pricing Table (Control vs Treatment):
CONTROL (Current):           TREATMENT (Decoy):
Starter:    $99/mo           Starter:         $99/mo
Prof:       $199/mo          Prof:           $199/mo
Enterprise: $599/mo          Prof Plus:      $349/mo ← Decoy
                             Enterprise:     $599/mo

Success Metrics:
• Enterprise tier conversion rate: target +18%
• Professional tier: maintain within 5% of baseline
• Overall AOV (Average Order Value): +12-15%
• Variant selection distribution: 45% Starter, 35% Prof, 15% Prof Plus, 5% Enterprise

Statistical Requirement: 500 conversions per variant (approximately 3 weeks at current volume)

Measurement & Analysis:
Track in analytics: variant_selected, monthly_arr_impact, tier_distribution_shift
Analyze: Chi-square test for independence (tier selection difference)
Confidence threshold: 95% (p-value < 0.05)

Implementation Checklist:
☐ Design new tier in pricing table
☐ Add "Most Popular" badge to Prof Plus
☐ Update feature comparison
☐ Configure analytics tracking
☐ A/B test assignment logic
☐ Notify support team of new tier
☐ Monitor churn (ensure upsell, not just shift)
```

---

## Tips & Best Practices

### 1. Optimize for Your Industry
Different industries respond differently to pricing psychology:
- **SaaS**: Decoy pricing + payment plans most effective
- **Courses**: Payment plans + scarcity + social proof
- **Digital Products**: Charm pricing + bundling + urgency
- **Agencies**: Risk reversal + guarantee + case studies

### 2. Start with Quick Wins
Charm pricing and guarantees require minimal effort but yield 8-15% lift. Do these first to build momentum.

### 3. Test One Change at a Time
Multivariate testing introduces complexity. Test charm pricing alone, then add decoy pricing, then payment plans. This identifies which changes drive lift.

### 4. Measure Incrementally
Don't wait 3 months to see results. Run 2-week tests, analyze data, implement fast wins, then move to larger projects.

### 5. Mobile Matters
40%+ of traffic is mobile. Ensure your pricing page, checkout, and payment plans are mobile-optimized. Test mobile separately from desktop if volumes allow.

### 6. Track Downstream Metrics
A/B testing conversion rate is important, but also measure:
- Customer Lifetime Value (CLV)
- Churn rate by pricing tier
- Upgrade/downgrade patterns
- Support ticket volume by tier (proxy for satisfaction)

### 7. Segment by Buyer Persona
Price-sensitive buyers respond to payment plans. Value-driven buyers respond to guarantees and social proof. Use audience targeting to personalize pricing psychology tactics.

### 8. Document Your Assumptions
Before each test, write down your hypothesis and why you believe it will work. This trains your pricing intuition and creates institutional knowledge.

### 9. Competitive Monitoring
Revisit competitor pricing quarterly. This skill can track changes and alert you to new tactics you should test.

### 10. Email Sequences Drive Conversions
People often visit pricing pages but don't convert immediately. Follow up with value-focused emails (not discount-focused). This yields 15-25% incremental lift.

---

## Safety & Guardrails

### What This Skill Will NOT Do

**🚫 Unethical Pricing Tactics**
- Recommend deceptive dark patterns (hidden fees, misleading comparisons)
- Suggest aggressive scarcity tactics that aren't genuine
- Recommend predatory pricing for vulnerable populations
- Encourage price discrimination based on protected characteristics

**🚫 Competitor Espionage**
- This skill analyzes *publicly visible* pricing pages only
- Does NOT access private pricing data, secret databases, or protected URLs
- Does NOT scrape competitor data beyond what's visible to paying customers
- Does NOT recommend copying exact competitor copy (provides frameworks only)

**🚫 Compliance & Legal Issues**
- Does NOT generate legal guarantees or money-back promises (that's legal's job)
- Does NOT recommend pricing practices that violate regional regulations (e.g., GDPR pricing, consumer protection laws)
- Does NOT recommend bait-and-switch tactics
- Recommends involving legal/finance teams for warranty and guarantee language

**🚫 Data Privacy**
- Does NOT store or transmit customer pricing data
- Does NOT log pricing URLs without your explicit consent
- Does NOT create permanent records of your pricing strategy
- All analysis is real-time; reports are yours to keep/delete

**