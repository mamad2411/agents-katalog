---
name: ai-pricing-psychology-consultant
description: "Design tiered pricing strategies with psychological anchoring, competitor analysis, and value-based packaging. Use when the user needs pricing optimization, discount framing, or willingness-to-pay research for SaaS, products, or services."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","GOOGLE_SEARCH_API_KEY","SERPER_API_KEY"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"💰"}}
---

## Overview

The **AI Pricing Psychology Consultant** analyzes your competitive landscape, customer psychology, and market positioning to generate data-driven pricing strategies that maximize revenue without triggering price sensitivity or commoditization.

This skill is designed for founders, product managers, and growth leaders who need to:
- **Analyze competitor pricing** across 10+ direct and indirect competitors
- **Model willingness-to-pay (WTP)** signals from customer research, surveys, and behavioral data
- **Design psychological anchoring tactics** using decoy pricing, charm pricing, and prestige framing
- **Generate tiered packaging** that segments customers by value perception
- **Frame discounts** to maintain perceived value during promotions
- **A/B test positioning** recommendations with supporting psychology research

The skill integrates with **WordPress pricing tables, Slack notifications for pricing alerts, Google Sheets for competitive tracking, Stripe for dynamic pricing testing, and HubSpot for customer segment analysis**.

---

## Quick Start

### Example 1: Analyze Competitor Pricing & Generate Tiered Strategy

```
Analyze pricing for a B2B project management SaaS competing with Asana, 
Monday.com, and Notion. Our current price is $99/month. 

Customers are:
- Freelancers (price-sensitive, $0-50/month budget)
- Small teams (5-20 people, value-driven, $100-300/month budget)
- Enterprise (100+ people, feature-driven, $1000+/month budget)

Generate a 3-tier pricing strategy with psychological anchoring, 
including anchor prices, decoy effects, and charm pricing recommendations.
```

### Example 2: Design Discount Framing to Preserve Perceived Value

```
We're running a Black Friday promotion: 30% off annual plans. 
Our standard price is $199/month.

Design 3 different discount frames that:
1. Preserve perceived value
2. Increase urgency without commoditizing
3. Appeal to different customer segments (budget-conscious vs. value-conscious)

Include specific copy recommendations and psychological principles for each frame.
```

### Example 3: Research Willingness-to-Pay & Market Positioning

```
I sell premium fitness coaching. My competitors range from $49-299/month.
I want to position at the premium end ($249/month) but need evidence 
of customer WTP.

Research willingness-to-pay signals from:
- Fitness industry benchmarks
- Premium coaching positioning
- Customer psychology research

Generate positioning language and pricing justification for $249/month tier.
```

---

## Capabilities

### 1. Competitive Pricing Analysis
- **Automated competitor discovery** via Google Search API + Serper API
- **Price tracking** across 10+ competitors (direct, indirect, adjacent categories)
- **Feature-to-price mapping** to identify pricing gaps and opportunities
- **Market positioning analysis** (budget, mid-market, premium, enterprise)
- **Pricing model comparison** (per-user, per-feature, usage-based, hybrid)

**Usage:** "Analyze pricing for [product category] in [industry]. Track [competitor names] and identify pricing white space."

### 2. Willingness-to-Pay (WTP) Research
- **Van Westendorp Price Sensitivity Meter** analysis
- **Conjoint analysis** for feature value weighting
- **Behavioral economics research** integration (anchoring, framing effects)
- **Customer segment WTP modeling** by persona, industry, company size
- **Price elasticity estimation** based on market research

**Usage:** "Model WTP for [customer segment]. Include elasticity analysis and segment-specific pricing recommendations."

### 3. Psychological Anchoring Strategy Design
- **Decoy pricing** (middle option bias exploitation)
- **Charm pricing** ($99 vs. $100, $49 vs. $50)
- **Prestige pricing** (premium tier positioning)
- **Bundle anchoring** (bundled vs. unbundled value perception)
- **Scarcity & urgency framing** (limited seats, time-based discounts)

**Usage:** "Design anchoring tactics for a 3-tier pricing model. Include decoy effect calculations and charm pricing recommendations."

### 4. Tiered Packaging & Value-Based Segmentation
- **Customer segment mapping** by WTP, use case, company size
- **Feature-to-tier allocation** (what features in each tier)
- **Value articulation** per tier with psychological framing
- **Upgrade path design** (friction points and incentives)
- **Packaging copy** optimized for conversion

**Usage:** "Create a 4-tier pricing structure for [product]. Map features to tiers based on value perception and willingness-to-pay."

### 5. Discount Frame Engineering
- **Loss aversion framing** ("Save $X" vs. "Get $X off")
- **Reference price anchoring** (original vs. discounted price visibility)
- **Urgency mechanisms** (countdown timers, limited seats, deadline framing)
- **Segment-specific discount positioning** (budget vs. value-conscious)
- **Perceived value preservation** during promotions

**Usage:** "Frame a 40% discount on annual plans. Preserve perceived value and maximize conversion without commoditizing."

### 6. A/B Testing Recommendations
- **Pricing page variant suggestions** (copy, anchors, framing)
- **Tier positioning tests** (3-tier vs. 4-tier, feature emphasis)
- **Discount frame testing** (% off vs. dollar amount vs. bundle savings)
- **Statistical power calculations** for pricing experiments
- **Sample size recommendations** by conversion rate

**Usage:** "Design A/B tests for our pricing page. Include variant copy, statistical requirements, and success metrics."

---

## Configuration

### Required Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # GPT-4 for strategy generation
export GOOGLE_SEARCH_API_KEY="AIza..."   # Google Custom Search for competitor research
export SERPER_API_KEY="..."              # Serper for real-time pricing data
```

### Optional Integrations

**Stripe** (for dynamic pricing testing):
```bash
export STRIPE_API_KEY="sk_live_..."
export STRIPE_PRODUCT_ID="prod_..."
```

**Google Sheets** (for competitive tracking):
```bash
export GOOGLE_SHEETS_ID="..."
export GOOGLE_SHEETS_CREDENTIALS="..."
```

**Slack** (for pricing alerts):
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
```

### Setup Instructions

1. **Enable APIs**: Activate Google Custom Search API and Serper API in your cloud console
2. **Create API keys**: Generate keys for OpenAI, Google Search, and Serper
3. **Set environment variables**: Export all required keys in your shell or `.env` file
4. **Test connectivity**: Run a sample competitor analysis to verify all APIs are accessible
5. **Customize industry benchmarks**: Update pricing psychology research data for your specific category

---

## Example Outputs

### Output 1: Competitor Pricing Analysis Report

```
COMPETITIVE PRICING ANALYSIS
Product: Project Management SaaS
Analysis Date: 2024-01-15

COMPETITOR LANDSCAPE:
┌─────────────────┬──────────────┬──────────────┬────────────┐
│ Competitor      │ Starter      │ Pro          │ Enterprise │
├─────────────────┼──────────────┼──────────────┼────────────┤
│ Asana           │ $10.99/mo    │ $24.99/mo    │ Custom     │
│ Monday.com      │ $9/mo        │ $49/mo       │ Custom     │
│ Notion          │ Free         │ $10/mo       │ Custom     │
│ Our Current     │ $29/mo       │ $99/mo       │ $299/mo    │
│ Market Average  │ $9.75/mo     │ $46/mo       │ $299/mo    │
└─────────────────┴──────────────┴──────────────┴────────────┘

PRICING GAPS IDENTIFIED:
• Starter tier: We're 3x higher than market average ($29 vs. $9.75)
  → Opportunity: Reposition at $14.99 or create freemium model
• Pro tier: We're 2.15x higher than market average ($99 vs. $46)
  → Opportunity: Add premium features to justify or segment differently
• Enterprise: Aligned with market ($299)

PSYCHOLOGICAL INSIGHTS:
✓ Charm pricing: All competitors use .99 endings (we use .00)
✓ Decoy effect: Notion's free tier creates anchoring pressure
✓ Prestige positioning: Enterprise tier at $299 is psychological threshold
```

### Output 2: Willingness-to-Pay Model

```
WILLINGNESS-TO-PAY ANALYSIS
Customer Segment: Small Teams (5-20 people)

VAN WESTENDORP PRICE SENSITIVITY METER:
Acceptable Price Range: $49 - $249/month
Optimal Price Point: $149/month
Indifference Price: $99/month

SEGMENT-SPECIFIC WTP:
├─ Budget-Conscious (40%): $49-99/month
├─ Value-Driven (45%): $99-199/month
└─ Premium/Feature-Driven (15%): $199-299/month

PRICE ELASTICITY:
At $99/month: Estimated conversion rate 8.2%
At $149/month: Estimated conversion rate 6.1% (-25.6%)
At $199/month: Estimated conversion rate 3.8% (-53.7%)

RECOMMENDATION: $149/month optimal for revenue maximization
Alternative: Use 3-tier (Pro $99, Premium $149, Elite $249) to serve all segments
```

### Output 3: Tiered Pricing Strategy with Anchoring

```
RECOMMENDED 3-TIER PRICING STRATEGY

TIER 1: STARTER - $49/month (Charm pricing)
├─ Anchor: "Most Popular" badge (middle option bias)
├─ Features: 3 projects, 5 team members, basic integrations
├─ Psychology: Entry point, low friction, upgrade path visible
└─ Copy: "Perfect for growing teams getting started with collaboration"

TIER 2: PROFESSIONAL - $149/month (Decoy effect)
├─ Anchor: Positioned as "best value" (anchors perception vs. $49 and $249)
├─ Features: Unlimited projects, 50 team members, advanced integrations
├─ Psychology: Perceived as "sweet spot," highest conversion expected
└─ Copy: "The complete toolkit for professional teams at scale"

TIER 3: ENTERPRISE - $299/month (Prestige pricing)
├─ Anchor: Premium positioning, custom features
├─ Features: Unlimited everything, dedicated support, SSO, custom contracts
├─ Psychology: Prestige tier, signals premium quality
└─ Copy: "Enterprise-grade collaboration with dedicated support"

DECOY EFFECT ANALYSIS:
Without $149 tier: 70% choose $49, 30% choose $299 (low revenue)
With $149 tier: 20% choose $49, 60% choose $149, 20% choose $299 (high revenue)
→ Expected revenue increase: +68% from decoy effect alone

CHARM PRICING IMPACT:
$49 vs. $50: +12-15% perceived value difference
$149 vs. $150: +8-10% perceived value difference
```

### Output 4: Discount Frame Recommendations

```
BLACK FRIDAY PROMOTION: 30% OFF ANNUAL PLANS

FRAME 1: LOSS AVERSION (Highest Conversion Expected)
Copy: "Save $537/year on Professional plan"
Mechanism: Dollar amount (loss aversion > percentage)
Psychology: Loss aversion is 2x stronger than gain attraction
Expected Lift: +18-22% conversion

FRAME 2: REFERENCE PRICE ANCHORING
Copy: "Professional: $1,788/year → $1,251/year"
Mechanism: Visual price comparison with strikethrough
Psychology: Anchors perception to higher original price
Expected Lift: +14-18% conversion

FRAME 3: SCARCITY + URGENCY (Budget-Conscious Segment)
Copy: "Limited: 100 annual seats at 30% off. Offer ends Sunday."
Mechanism: Artificial scarcity + deadline
Psychology: FOMO + loss aversion combined
Expected Lift: +22-28% conversion (budget-conscious only)

RECOMMENDED APPROACH:
Primary: Frame 1 (loss aversion) for general audience
Secondary: Frame 3 (scarcity) for budget-conscious segment via email
Preserve: Full-price tier visible (prevents commoditization)
```

---

## Tips & Best Practices

### 1. Anchor Pricing to Customer Value, Not Cost
- **Don't do:** Base pricing on development costs or competitor prices
- **Do this:** Price based on customer WTP and value delivered
- **Example:** If customers save 5 hours/week at $50/hour rate, anchor to $250/week value
- **Psychology:** Value-based pricing triggers prestige effect, not price sensitivity

### 2. Use Decoy Pricing to Guide Customer Segments
- **Strategy:** Create a middle tier that's slightly less attractive than the premium tier
- **Example:** If you want customers in the $149 tier, create $99 (too limited) and $249 (premium)
- **Result:** 60% of customers choose the $149 "sweet spot" instead of splitting between $99 and $249
- **Math:** Expected revenue increases 40-70% with proper decoy placement

### 3. Charm Pricing Works Better Than Prestige Pricing Alone
- **$99/month beats $100/month** by 12-15% in perceived value (irrationally)
- **Combine with anchoring:** Show original price at $100, discounted to $99 (double effect)
- **Warning:** Only use .99 endings for value tiers, not premium tiers (signals "discount")

### 4. Frame Discounts as Dollar Amounts, Not Percentages
- **"Save $537/year"** outperforms **"30% off"** by 18-22% in conversions
- **Psychology:** Loss aversion is 2x stronger than gain attraction
- **Exception:** Budget-conscious segments respond better to percentage discounts
- **Best practice:** Test both, segment by customer type

### 5. Keep Premium Tier Visible During Promotions
- **Discounting only lower tiers** signals value preservation
- **Hiding premium tier** during promotions triggers commoditization fears
- **Example:** Discount Starter and Pro, keep Enterprise full-price
- **Result:** Maintains prestige positioning while capturing price-sensitive customers

### 6. Test Pricing Incrementally
- **Don't:** Launch a completely new pricing structure without testing
- **Do this:** Test 2-3 price points via A/B testing with 1,000+ visitors each
- **Timeline:** Run for 2-4 weeks minimum to account for buying cycles
- **Metrics:** Track conversion rate, customer acquisition cost, and customer lifetime value

### 7. Segment Messaging by WTP
- **Budget-conscious:** Emphasize ROI, cost savings, efficiency
- **Value-driven:** Emphasize features, integrations, team collaboration
- **Premium:** Emphasize exclusivity, support, customization
- **Tactic:** Use same pricing page, different copy per segment via dynamic content

### 8. Research Customer WTP Before Launching
- **Survey:** Ask "What would you pay?" to 50+ customers/prospects
- **Behavioral:** Track which price points get most clicks/signups
- **Competitive:** Monitor competitor pricing changes monthly
- **Update:** Refresh WTP analysis quarterly as market evolves

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Illegal pricing practices:** This skill will not recommend price-fixing, predatory pricing, or collusion with competitors. All recommendations comply with antitrust laws (FTC, CMA guidelines).

❌ **Deceptive framing:** Will not create false scarcity ("Limited seats" when unlimited), fake urgency ("Offer ends today" when ongoing), or misleading anchors. All recommendations are transparent and ethical.

❌ **Predatory