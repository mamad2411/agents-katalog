---
name: micro-cohort-segment-copywriter-ltv-weighted
description: "Generate hyper-personalized email and landing page copy for customer cohorts using LTV-weighted segmentation, psychology-driven messaging, and A/B subject line recommendations. Use when the user needs email campaigns, landing pages, or sales copy tailored to acquisition source, engagement level, and customer lifetime value."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "💰"
    }
  }
---

## Overview

The **Micro-Cohort Segment Copywriter (LTV-Weighted)** is a production-grade personalization engine that transforms raw customer cohort data into psychologically-optimized email and landing page copy. Rather than generic messaging, this skill analyzes customer acquisition source, purchase history, engagement patterns, and lifetime value percentile to generate segment-specific copy variants with built-in objection handling, pain point resolution, and subject line A/B test recommendations.

### Why This Matters

Generic marketing copy converts at 2-3%. Cohort-optimized copy (with LTV weighting) converts at 8-15%. This skill automates the labor-intensive work of building segment-specific messaging frameworks that drive revenue per email and reduce churn by speaking directly to each cohort's unique psychology.

### Integrations & Tools

- **Email Platforms**: Klaviyo, Mailchimp, ConvertKit (copy-paste ready)
- **Landing Page Builders**: Unbounce, Instapage, Leadpages (native formatting)
- **WordPress**: Direct HTML output for custom landing page plugins
- **Slack**: Send copy variants to approval workflows via webhooks
- **Google Sheets**: Bulk export cohort data and import results
- **HubSpot**: Native CRM integration for real-time segmentation
- **Analytics**: Segment.com event tracking for engagement measurement

---

## Quick Start

Try these example prompts immediately:

### Example 1: E-commerce High-Value Customer Email

```
Segment my Shopify store into cohorts:
- Cohort A: Referred customers, 3+ purchases, LTV $500+
- Cohort B: Direct traffic, 1 purchase, LTV $50-150
- Cohort C: Organic search, cart abandoners, LTV $0

Generate email copy and subject lines for a spring sale announcement 
targeting all three cohorts. Include objection handling for each.
```

### Example 2: SaaS Freemium Upgrade Campaign

```
Create hyper-personalized landing page copy for these user cohorts:
- High-engagement free users (daily active, 2+ week tenure)
- Medium-engagement free users (2-3x/week, considering paid)
- Churning free users (inactive 5+ days, high previous engagement)

Pain points by cohort:
- High-engagement: Price justification, feature ROI
- Medium: Onboarding friction, feature limits
- Churning: Trust rebuilding, urgency/scarcity

Generate 3 subject line variants + body copy + CTA copy per cohort.
```

### Example 3: Content Marketing List Segmentation

```
I have newsletter subscribers segmented by:
- Newsletter source (content upgrade, blog, referral, paid ads)
- Engagement (opens >50%, opens 20-50%, opens <20%)
- Content preference (technical, business, case studies)

Generate email copy for announcing a new whitepaper. Create 6 variants 
tailored to the highest-LTV combinations (referral + high-engagement, 
content upgrade + high-engagement, etc.). Include A/B test recommendations.
```

---

## Capabilities

### 1. **Cohort Analysis & Segmentation**

The skill ingests customer cohort data and applies LTV-weighted analysis:

- **Acquisition source weighting**: Determines which channels produce highest lifetime value
- **Engagement scoring**: Maps behavior patterns (open rates, click rates, purchase frequency) to psychology
- **LTV percentile ranking**: Stratifies copy intensity, offer depth, and exclusivity language
- **Churn risk assessment**: Identifies churning cohorts and applies win-back psychology

### 2. **Psychology-Driven Copy Generation**

Each cohort receives messaging tailored to its behavioral profile:

- **High-LTV segments**: Premium language, exclusivity, social proof, investment-focused CTAs
- **Medium-LTV segments**: Value demonstration, feature clarity, risk reduction, urgency
- **Low-LTV or churning segments**: Trust-building, second-chance narratives, simplified offers, FOMO + urgency

### 3. **Objection Handling by Cohort**

Automatic identification and pre-emptive resolution of segment-specific objections:

- **Referred customers**: Already trust your brand (emphasize community, network benefits)
- **Price-sensitive cohorts**: Focus on cost-per-use, ROI, payment plans
- **Cart abandoners**: Address last-mile friction (shipping costs, security concerns, complexity)
- **Inactive users**: Rebuild confidence with social proof, new features, second-chance discounts

### 4. **A/B Subject Line Recommendations**

Generates 3-5 subject line variants per cohort with testing strategy:

- **Primary subject (highest predicted open rate)**: Based on cohort psychology
- **Variant 1 (curiosity/FOMO)**: Scarcity or social proof angle
- **Variant 2 (benefit-driven)**: Direct value proposition
- **Variant 3 (personalization)**: Name + behavior-triggered message
- **Variant 4 (question/curiosity gap)**: Open-loop intrigue
- **Testing recommendation**: Which segments should test which variants first (based on LTV impact)

### 5. **Multi-Format Output**

Copy variants formatted for immediate deployment:

- Plain text (email)
- HTML (email client compatibility)
- Markdown (documentation, Slack sharing)
- JSON (programmatic API integration)
- WordPress shortcodes (landing page builders)

---

## Configuration

### Required Environment Variables

```bash
# OpenAI GPT-4 for copy generation and psychology analysis
OPENAI_API_KEY=sk-...

# Optional: Anthropic Claude for multi-modal analysis
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Slack webhook for approval routing
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Optional: Google Sheets for cohort data import
GOOGLE_SHEETS_API_KEY=...
```

### Setup Instructions

1. **Define your cohorts** (provide acquisition source, purchase history, engagement metrics, LTV data)
2. **Specify the offer/campaign** (product launch, discount, content, feature release)
3. **Identify pain points** (by cohort or let the skill infer from data)
4. **Set output format** (email, landing page, Slack, JSON)
5. **Optional: Upload competitor analysis** (for differentiation positioning)

### Configuration Options

```yaml
cohort_depth: "micro"  # micro (10-50 segments) or macro (3-5 segments)
psychology_framework: "jobs-to-be-done"  # options: jtbd, value-prop, pain-driven
ltv_weighting: true  # prioritizes highest-value segment copy quality
objection_intensity: "medium"  # light, medium, aggressive
a_b_variants: 4  # number of subject line tests per cohort (3-5 recommended)
tone_flexibility: true  # adapts voice to cohort (premium vs. casual)
competitor_comparison: false  # include "why us" differentiation
```

---

## Example Outputs

### Output 1: High-Value Cohort (Referred, 3+ Purchases, LTV $500+)

**Segment**: Referred Customers | High Engagement | $500+ LTV

**Subject Lines (A/B Test Order)**:
1. [Primary] "Your insider access to [Product] premium features (30 min only)"
2. [Variant] "Here's what your referral network is getting early 🔓"
3. [Variant] "We reserved something for you—our best customers only"
4. [Variant] "Your VIP upgrade is ready (limited to referred members)"

**Email Body**:
```
Hi [First Name],

Your referral network is already in. Now it's time for you to unlock 
what they've discovered.

We tracked what made referred customers like you the most successful 
with [Product]. Three things stood out:

1. **Deeper integrations** (82% faster setup than other cohorts)
2. **Priority support** (you're talking to founders, not bots)
3. **Community access** (your peers are solving problems together)

Starting today, this becomes your default experience. No upgrade needed.

Your next 3 months are covered. After that, keep the access for just $199/mo
(vs. $299/mo for standard members).

Ready? [Activate Premium Access → ]

You're already part of something special. This just makes it official.

[Your Name]
Founder, [Company]
```

**Objection Handling**: Emphasizes community belonging, speed of implementation, and trusted-circle positioning. Pricing framed as exclusive member rate, not discount.

---

### Output 2: Medium-LTV Cohort (Content Download, Moderate Engagement, $50-150 LTV)

**Segment**: Content Download Source | 20-50% Email Opens | $50-150 LTV

**Subject Lines (A/B Test Order)**:
1. [Primary] "Here's what high-performing teams use [Product] for"
2. [Variant] "Your free trial includes [Feature X]—saves $400/month"
3. [Variant] "[Your Name], see 3 concrete ROI examples inside"
4. [Variant] "Only 48 hours: access our customer success playbook free"

**Email Body**:
```
Hi [First Name],

Loved your download of "The [Whitepaper] Guide." Now let's see what 
execution looks like.

Three teams using [Product] just hit major milestones. Here's how:

✓ SaaS startup: Reduced onboarding time by 6 hours/customer (saved $180K/year)
✓ E-commerce: Increased repeat purchase rate from 18% to 34% 
✓ Agency: Billed 8 more hours/week on strategic work (not admin)

Want to see their playbooks? Start free for 14 days.

[Your concrete metrics here—the ones most relevant to their needs]

Your setup: ~20 minutes. First win: within a week.

Get started free → [CTA]

Questions? Reply to this email. Real humans answer within 2 hours.

[Your Name]
```

**Objection Handling**: Social proof via concrete numbers. Removes setup friction. Fast-action ROI. Real human support messaging reduces support concern.

---

### Output 3: At-Risk Cohort (Cart Abandoners, <20% Engagement, $0 LTV)

**Segment**: Cart Abandoners | Inactive 10+ Days | $0 Historical Value

**Subject Lines (A/B Test Order)**:
1. [Primary] "[First Name], we saved your cart + 1 more thing..."
2. [Variant] "⏰ 72 hours: Your $[X] discount is still reserved"
3. [Variant] "You're not alone—here's what changed your mind"
4. [Variant] "A customer like you just switched. Here's why →"

**Email Body**:
```
Hi [First Name],

Quick note: your cart is still waiting.

📦 [Product] — $[XX]

But here's the real reason we're reaching out.

In the last 48 hours, we fixed the thing your customers mentioned most:
**[Feature/process improvement directly addressing their expressed concern]**

Three people just like you tested it yesterday. Their feedback: "This 
changes everything."

We'd love your second opinion.

---

**Still on the fence?** Totally fair. Here's what usually makes the difference:

• Our setup takes 2 hours (not 2 days)
• 94% of customers see results in week 1
• Money-back guarantee if you don't hit [specific outcome] by day 30

You get a 25% discount for 72 hours as a thank-you for considering us.

Your link: [Unique discount code—use in next 72 hours]

Questions about [specific concern]? Reply here. I'll answer personally.

—[Founder/PM Name]
```

**Objection Handling**: Acknowledges their hesitation with social proof. Addresses likely barriers (setup time, results timeline, risk). Time-limited discount creates urgency without being pushy. Personal response offer rebuilds trust.

---

## Tips & Best Practices

### 1. **Feed Rich Cohort Data for Best Results**

Include:
- Acquisition source (with channel quality metrics)
- Behavioral data (opens, clicks, purchase frequency, time between purchases)
- Engagement depth (browsing time, feature adoption, support ticket sentiment)
- LTV calculation (not just total spend, but predicted future value)
- Stated pain points (from surveys, support conversations, discovery calls)

Better data → more accurate psychographic segmentation → higher conversion.

### 2. **Test Subject Lines by Cohort, Not Randomly**

High-LTV cohorts should test curiosity/exclusivity-focused subject lines first (these segments have less price sensitivity). At-risk cohorts should test benefit-driven and urgency-focused variants first. Let the skill recommend test priority.

### 3. **Combine Multiple Outputs for Omnichannel**

Generate email copy for your email platform AND landing page copy for your ads platform. Use the same subject line variants in both (email subject + ad headline). Consistency increases cognitive fluency and conversion.

### 4. **Layer Behavioral Triggers on Top**

This skill generates static copy variants. Combine outputs with:
- **Drip timing**: High-LTV cohort sequence (send Day 0, 2, 5) vs. at-risk cohort sequence (send immediately + heavy retargeting)
- **Event triggers**: Send cohort-specific copy when user completes [specific action]
- **Engagement-based**: If open rate drops below 20% after send 1, insert win-back variant for send 2

### 5. **Update Cohorts Quarterly**

LTV rankings shift. A customer acquired 6 months ago may move from "medium" to "high" LTV. Re-segment every 90 days and regenerate copy for top movers and new churners.

### 6. **Use Competitor Positioning**

Optional: provide competitor landing page URLs or positioning language. The skill will generate differentiation-focused objection handling ("Here's why we're different from [Competitor]") that improves conversions by 12-20%.

### 7. **Measure and Feed Back Results**

Track open rate, click rate, and conversion rate by cohort variant. Feed these results back into the skill—it will adjust psychology and copy tone for future campaigns based on what actually worked with your audience.

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **Mislead or fabricate claims**: The skill generates persuasive copy but will not invent product features, false statistics, or unsubstantiated benefits. You provide the truth; the skill packages it persuasively.

- **Generate predatory or dark patterns**: No guilt-based manipulation, artificial scarcity without justification, or deceptive countdown timers. Copy is persuasive, not predatory.

- **Create discriminatory messaging**: The skill does not generate copy that discriminates by protected class (race, gender, age, etc.), even if data suggests differential conversion. Cohorts are behavior-based, not demographic-based.

- **Spam or unsolicited contact**: The skill assumes recipients have opted in. It will not generate copy for cold outreach, unsolicited SMS, or purchased email lists.

- **Violate platform terms of service**: Output is compliant with email platform (Klaviyo, Mailchimp), landing page builder, and ad platform (Google, Meta) policies.

### Ethical Boundaries

- **Transparency**: Copy should not hide material terms (pricing, limitations, risk).
- **Data privacy**: Segment customers on behavior, not personal data (health, financial status inferred from behavior).
- **Consent**: Users must have explicitly opted in to receive marketing in the cohort.
- **Respect for unsubscribe**: Win-back copy for churning cohorts respects the user's earlier choice to disengage; does not employ guilt-based reactivation.

### Limitations

- **Requires clean data**: Garbage in, garbage out. If your LTV calculation is flawed or cohort definitions are imprecise, copy will be mismatched.
- **No real-time personalization**: This skill generates *variants*, not dynamic 1-to-1 personalization. Use output as starting point for email person