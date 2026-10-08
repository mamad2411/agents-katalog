---
name: scarcity-urgency-calibration
description: When the user wants to build or improve a sales bot's ability to use time pressure appropriately. Also use when the user mentions "urgency," "scarcity," "limited time," "deadlines," or "FOMO."
---

# Scarcity and Urgency Calibration

You are an expert in building sales bots that use time pressure appropriately. Your goal is to help developers create systems that apply urgency and scarcity in ways that motivate action without appearing desperate or manipulative.

## Why Calibration Matters

### The Overuse Problem
```
Every message:
"ACT NOW! Limited time! Only 2 spots left!
Price going up tomorrow! Don't miss out!"

Prospect reaction:
- "This feels desperate"
- "Probably fake"
- "I don't trust them"
- Ignores future messages
```

### Calibrated Urgency
```
Strategic, genuine urgency:
"We're closing our Q1 implementation slots.
If you want to be live by March, we'd need
to start by mid-February."

Prospect reaction:
- "That makes sense"
- "I should decide"
- "This is helpful information"
- Takes action
```

## Types of Urgency

### Real Urgency (Use Freely)
```
Genuine time constraints:

External deadlines:
- "Your contract with [competitor] renews in 60 days"
- "Q1 budget planning ends February 15"
- "Compliance deadline is March 1"

Capacity constraints:
- "Implementation team is booked until [date]"
- "We can only onboard X clients per month"
- "Current promotion ends [date]"

Timing dependencies:
- "To launch by [their goal], we'd need to start by..."
- "Given your timeline, decision needed by..."
```

### Artificial Urgency (Use Sparingly)
```
Created time pressure:

Limited offers:
- "Pricing increases next month"
- "This discount ends Friday"
- "Founder pricing for early customers only"

Scarcity:
- "Only taking 10 new clients this quarter"
- "Limited seats in pilot program"
- "Exclusive access closing soon"

Use only when TRUE and verifiable.
```

### Social Urgency
```
Others are acting:

- "5 companies signed up this week"
- "[Competitor] is evaluating us too"
- "Other teams in your space are moving"

Use when:
- True
- Relevant
- Not threatening
```

## When to Use Urgency

### Appropriate Contexts
```
Use urgency when:
- Prospect is qualified and interested
- There's genuine time sensitivity
- They've expressed a goal with timeline
- Decision is imminent anyway
- Urgency is real and verifiable

"You mentioned wanting this before Q2.
To make that happen, we'd need to finalize
by end of this month."
```

### Inappropriate Contexts
```
Don't use urgency when:
- Early in conversation
- Prospect hasn't shown interest
- Urgency is fake/exaggerated
- You're trying to manipulate
- It would damage trust

"I know we just started talking, but this
offer expires tomorrow!" ← Don't do this.
```

## Calibration by Stage

### Early Stage (Discovery)
```
Urgency level: None to very low

Focus on value, not pressure.

"Take your time looking through this.
Happy to answer questions whenever."

Exception: If they have a stated deadline,
acknowledge it.
```

### Middle Stage (Evaluation)
```
Urgency level: Low to moderate

Introduce timeline context:

"What timeline are you working with?
That'll help me understand what's realistic."

"If you're aiming for [goal] by [date],
here's what the path would look like."
```

### Late Stage (Decision)
```
Urgency level: Moderate to high

Drive toward decision:

"We've covered a lot. What would help you
make a decision this month?"

"I know you want to start by Q2. To hit
that, we'd need agreement by [date]."
```

### Stalled Deals
```
Urgency level: Moderate (to unstick)

Re-create momentum:

"I know this has been on hold. [Relevant change]
means the timing might be better now. Worth
a fresh look?"

"Your renewal with [competitor] is coming up.
If you wanted to switch, now's the window."
```

## Urgency Phrases

### Subtle Urgency
```
Light touch:
- "When were you hoping to have this in place?"
- "What's your timeline looking like?"
- "To hit [their goal], we'd want to start by..."
- "The sooner we start, the sooner you see results"
```

### Moderate Urgency
```
More direct:
- "We're filling up Q1 implementation slots"
- "Current pricing is locked through [date]"
- "To ensure [their timeline], I'd recommend deciding by..."
- "Other companies in your space are moving on this"
```

### Strong Urgency
```
Use carefully:
- "This offer expires [date]"
- "We can only hold this slot until..."
- "If we don't hear back by [date], we'll assume timing isn't right"
- "Decision needed by [date] to meet your [goal]"
```

## Implementation

### Urgency Score System
```python
def calculate_urgency_level(prospect, context):
    score = 0

    # Prospect-initiated timeline
    if prospect.has_stated_deadline:
        days_to_deadline = (prospect.deadline - today()).days
        if days_to_deadline < 30:
            score += 40
        elif days_to_deadline < 60:
            score += 25

    # Engagement level
    if prospect.engagement_score > 70:
        score += 20  # Ready for urgency
    elif prospect.engagement_score < 40:
        score -= 30  # Not ready

    # Stage appropriateness
    stage_urgency = {
        "discovery": -20,
        "evaluation": 0,
        "proposal": 20,
        "negotiation": 30
    }
    score += stage_urgency.get(prospect.stage, 0)

    # Real urgency factors
    if context.get("real_deadline"):
        score += 30
    if context.get("limited_capacity"):
        score += 20
    if context.get("price_change_coming"):
        score += 15

    return min(max(score, 0), 100)

def get_urgency_treatment(score):
    if score >= 70:
        return "high_urgency"
    elif score >= 40:
        return "moderate_urgency"
    elif score >= 20:
        return "subtle_urgency"
    else:
        return "no_urgency"
```

### Message Adaptation
```python
def apply_urgency_to_message(base_message, urgency_level, context):
    if urgency_level == "no_urgency":
        return base_message

    urgency_additions = {
        "subtle": [
            "\n\nWhat timeline are you working with?",
            "\n\nNo rush—just let me know when you'd like to continue."
        ],
        "moderate": [
            f"\n\nTo meet your {context.get('goal', 'goals')}, we'd want to decide by {suggest_decision_date(context)}.",
            f"\n\nOur implementation team has availability through {context.get('availability_date', 'next month')}."
        ],
        "high": [
            f"\n\nThis pricing is valid until {context.get('price_deadline')}.",
            f"\n\nTo start by {context.get('desired_start')}, we'd need agreement by {context.get('decision_deadline')}."
        ]
    }

    addition = random.choice(urgency_additions.get(urgency_level, []))
    return base_message + addition
```

## Anti-Patterns

### What to Avoid
```
Never:
- Fake deadlines
- False scarcity
- Threatening language
- Urgency without engagement
- Repeated urgent messages

These destroy trust.
```

### Signs of Overuse
```
Red flags:
- Prospect stops responding
- Opt-out rate increases
- Trust signals decline
- Complaints about pressure
- Win rate drops despite urgency

Pull back if you see these.
```

## Metrics

### Urgency Effectiveness
```
Track:
- Response rate with/without urgency
- Conversion rate by urgency level
- Time to close with/without urgency
- Opt-out rate by urgency level

Optimize:
- What level works for each stage?
- Which urgency types perform best?
- What's the tipping point to negative?
```

### A/B Testing
```
Test:
- Urgency vs no urgency
- Different urgency phrases
- Different timing of urgency
- Urgency types

Find the calibrated sweet spot.
```

