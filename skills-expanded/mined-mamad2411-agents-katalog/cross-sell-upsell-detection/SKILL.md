---
name: cross-sell-upsell-detection
description: When the user wants to build or improve a sales bot's ability to identify expansion opportunities with existing customers. Also use when the user mentions "cross-sell," "upsell," "expansion revenue," "customer growth," or "account expansion."
---

# Cross-Sell and Upsell Detection

You are an expert in building sales bots that identify expansion opportunities with existing customers. Your goal is to help developers create systems that recognize when customers might benefit from additional products, features, or capacity.

## Why Expansion Detection Matters

### The Expansion Opportunity
```
Customer acquisition cost: $500
Lifetime value (single product): $3,000
Lifetime value (with expansion): $10,000+

Expansion is:
- Higher margin (no acquisition cost)
- Higher close rate (they trust you)
- Better retention (more integrated)
```

### Detection Value
```
Without detection:
- Expansion happens opportunistically
- Customers outgrow without upgrading
- Cross-sell happens only when asked
- Revenue left on table

With detection:
- Proactive outreach at right moment
- Upgrade before they hit limits
- Cross-sell when need emerges
- Maximize customer value
```

## Upsell Signals

### Usage-Based Signals
```
Approaching limits:
- 80%+ of seat licenses used
- 90%+ of storage consumed
- API calls nearing cap
- Feature usage hitting tier limits

"You're at 45 of 50 users. As you grow,
want me to walk through the team plan?"
```

### Engagement Signals
```
Deep product adoption:
- Using advanced features
- Multiple active users
- High login frequency
- Long session times
- Feature requests for premium items

"Your team is using [feature] heavily.
The Pro tier adds [related capability]—
interested in seeing it?"
```

### Growth Signals
```
Company/team expansion:
- New users being added
- New departments onboarding
- Company hiring (external data)
- Funding announcement
- New locations

"Congrats on the growth! As you scale,
here's how other companies handle [challenge]."
```

### Friction Signals
```
Hitting product limits:
- Error messages about limits
- Workarounds being used
- Export/import patterns (working around system)
- Support tickets about capacity

"I noticed you hit the export limit a few times.
The Business tier has unlimited exports—worth
looking at?"
```

## Cross-Sell Signals

### Adjacent Need Signals
```
Using complementary features:
- CRM customer using lots of email → marketing automation
- Analytics user requesting data → data warehouse
- HR software user adding employees → payroll

"Given how much you use [current product] for
[use case], our [adjacent product] might help
with [related need]."
```

### Explicit Mentions
```
Customer mentions related challenges:

"I wish we had better reporting"
"We're looking for a solution to X"
"Do you integrate with Y?"
"We're evaluating [competitor product category]"

Listen for adjacent pain points.
```

### Workflow Expansion
```
Customer expanding use cases:

- Single department → multiple departments
- Single location → multiple locations
- Single brand → multiple brands
- Internal use → customer-facing

Each expansion may need more products.
```

### Integration Signals
```
Integration patterns suggesting needs:

- Integrating with [tool] suggests need for [our product]
- API usage patterns indicate workflow gaps
- Manual data transfer between systems

"I see you're moving data between [system] and us
manually. Our [product] automates that."
```

## Detection Implementation

### Signal Scoring System
```python
def calculate_expansion_score(customer):
    score = 0
    signals = []

    # Usage signals
    usage = get_usage_metrics(customer)
    if usage.seat_utilization > 0.8:
        score += 25
        signals.append("high_seat_usage")
    if usage.feature_utilization > 0.7:
        score += 20
        signals.append("high_feature_usage")
    if usage.at_limit_events > 5:
        score += 30
        signals.append("hitting_limits")

    # Engagement signals
    engagement = get_engagement_metrics(customer)
    if engagement.monthly_active_users_growth > 0.1:
        score += 20
        signals.append("user_growth")
    if engagement.advanced_feature_adoption:
        score += 15
        signals.append("advanced_usage")

    # External signals
    external = get_external_signals(customer)
    if external.recent_funding:
        score += 20
        signals.append("funding")
    if external.hiring_signal:
        score += 15
        signals.append("hiring")

    return {
        "score": min(score, 100),
        "signals": signals,
        "recommendation": get_expansion_recommendation(signals)
    }
```

### Trigger Events
```python
EXPANSION_TRIGGERS = [
    {
        "name": "seat_threshold",
        "condition": "seat_usage >= 80%",
        "action": "upsell_seats",
        "message_template": "seat_expansion_outreach"
    },
    {
        "name": "feature_ceiling",
        "condition": "premium_feature_attempt >= 3",
        "action": "upsell_tier",
        "message_template": "tier_upgrade_outreach"
    },
    {
        "name": "adjacent_need",
        "condition": "integration_with_competitor_product",
        "action": "cross_sell",
        "message_template": "cross_sell_replacement"
    },
    {
        "name": "company_growth",
        "condition": "company_raised_funding",
        "action": "expansion_conversation",
        "message_template": "growth_expansion"
    }
]
```

## Expansion Conversations

### Upsell Conversation Starters
```
Usage-based:

"Hey [Name], noticed your team has been growing—
you're at [X] of [Y] users. Want me to walk
through what the next tier offers so you're
ready when you need it?"

Feature-based:

"I saw your team tried [premium feature] a few
times. It's in our Pro tier, but I can set up
a trial if you want to test it properly."

Limit-based:

"You've bumped against the [limit] a couple times.
Rather than work around it, would upgrading make
sense? I can show you what that looks like."
```

### Cross-Sell Conversation Starters
```
Adjacent need:

"Given how much you've accomplished with [current
product], I'm curious—how are you handling [related
challenge]? We have something that complements
what you're doing."

Integration-based:

"I noticed you're using [competitor] for [function].
Just so you know, we have [our product] that
integrates natively—might simplify things."

Expansion-based:

"Now that you're using us for [use case], other
customers in your situation often add [product]
for [benefit]. Worth a look?"
```

### Timing the Conversation
```
Best times for expansion:
- After they've achieved a win
- At renewal discussions
- After positive support interaction
- When they mention growth/change
- At QBR/check-in meetings

Worst times:
- During active support issue
- When they've had problems
- At contract end (too transactional)
- Without any trigger signal
```

## Customer Success Integration

### Health Score Connection
```
Expansion should correlate with health:

High health score + expansion signals:
→ Proactive upsell/cross-sell

High health score + no signals:
→ Check-in, explore latent needs

Low health score + expansion signals:
→ Fix health first, then expand

Low health score + no signals:
→ Focus on retention, not expansion
```

### QBR Integration
```
Include expansion in regular reviews:

"Based on your usage this quarter:
• You're getting great value from [current]
• You might benefit from [expansion opportunity]
• Here's what other similar customers do..."

Natural context for expansion.
```

## Message Templates

### Seat Expansion
```
Subject: Your team is growing!

"Hi [Name],

Congrats on the growth—you're now at [X] users,
approaching your [Y] seat limit.

Before you need them, want me to walk through
what adding seats looks like? Some options:

• Add [N] seats: $[price]/month
• Upgrade to Team plan (unlimited): $[price]/month

Let me know what makes sense.

[Rep]"
```

### Tier Upgrade
```
Subject: Unlock [Feature] for your team

"Hi [Name],

I noticed your team has been trying to use
[premium feature]—it's available on our Pro tier.

Based on how you're using [current tier], Pro
would give you:
• [Feature 1] - [benefit relevant to them]
• [Feature 2] - [benefit relevant to them]

Want to try it free for 14 days?

[Rep]"
```

### Cross-Sell
```
Subject: Idea for [their challenge]

"Hi [Name],

I saw that you're using [current product] heavily
for [use case]—great to see!

Quick question: how are you handling [related
challenge]? We have [other product] that a lot
of our [current product] customers pair with it.

[Stat about customers who use both]

Worth a quick look?

[Rep]"
```

## Metrics

### Expansion Metrics
```
Track:
- Expansion revenue per customer
- Upsell conversion rate
- Cross-sell conversion rate
- Signal-to-opportunity conversion
- Time from signal to expansion

Optimize:
- Which signals predict expansion?
- What timing works best?
- Which messages convert?
```

### Signal Accuracy
```
Measure signal quality:

- True positive rate (signal + conversion)
- False positive rate (signal + no interest)
- Coverage (opportunities with signals)

Refine signals based on outcomes.
```

## Implementation

### Expansion Data Model
```json
{
  "customer_id": "12345",
  "expansion_profile": {
    "current_products": ["crm"],
    "current_tier": "professional",
    "expansion_score": 75,
    "active_signals": [
      {"type": "seat_usage", "value": 0.85},
      {"type": "premium_feature_attempt", "count": 5}
    ],
    "recommended_expansions": [
      {
        "type": "upsell",
        "target": "enterprise_tier",
        "confidence": 0.8,
        "trigger": "feature_ceiling"
      },
      {
        "type": "cross_sell",
        "target": "marketing_automation",
        "confidence": 0.6,
        "trigger": "adjacent_usage"
      }
    ],
    "last_expansion_conversation": "2024-01-01",
    "expansion_history": []
  }
}
```

### Detection Pipeline
```python
def expansion_detection_pipeline(customer):
    # Collect signals
    usage_signals = analyze_usage(customer)
    engagement_signals = analyze_engagement(customer)
    external_signals = fetch_external_signals(customer)

    # Score opportunity
    score = calculate_expansion_score(
        usage_signals,
        engagement_signals,
        external_signals
    )

    # Check health before recommending
    health = get_customer_health(customer)
    if health.score < HEALTH_THRESHOLD:
        return None  # Focus on retention first

    # Generate recommendations
    if score >= EXPANSION_THRESHOLD:
        recommendations = generate_recommendations(customer, signals)
        return create_expansion_opportunity(customer, recommendations)

    return None
```

