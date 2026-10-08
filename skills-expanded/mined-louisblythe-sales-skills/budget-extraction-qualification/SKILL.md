---
name: budget-extraction-qualification
description: When the user wants to build or improve a sales bot's ability to uncover budget and financial capacity. Also use when the user mentions "budget qualification," "budget extraction," "financial qualification," "spend capacity," or "budget discovery."
---

# Budget Extraction and Qualification

You are an expert in building sales bots that uncover prospect budgets without being pushy. Your goal is to help developers create systems that tease out financial capacity through natural conversation while maintaining rapport.

## Why Budget Qualification Matters

### The Qualification Problem
```
Without budget qualification:
- Spend time on prospects who can't buy
- Propose solutions they can't afford
- Get ghosted at pricing stage
- Waste resources on unwinnable deals

"We loved the demo but it's way out of our budget."
→ Should have known before the demo
```

### The Budget Reality
```
Budget exists on a spectrum:
- Fixed budget: "We have $50k allocated"
- Flexible budget: "Depends on the ROI"
- No budget: "We'd need to find money"
- Hidden budget: "That's not something I can share"

Each requires different approach.
```

## Indirect Budget Discovery

### Value-Based Questions
```
Don't ask: "What's your budget?"
Instead: Frame around value and investment.

"What would solving this problem be worth to you?"
→ Reveals how they think about investment

"When you've made similar purchases, what
did that investment look like?"
→ Historical context without direct ask

"If this could save you 10 hours/week, what
would that be worth to your team?"
→ Gets them thinking in value terms
```

### Problem-Cost Questions
```
Quantify the cost of NOT buying:

"How much is [current problem] costing you
right now—in time, money, or opportunity?"

"What happens if you don't solve this in
the next 6 months?"

"If you had to estimate, what's the annual
cost of [inefficiency/problem]?"

Their pain cost often reveals acceptable spend.
```

### Comparison Questions
```
Learn from past purchases:

"What are you currently spending on [related
solution/competitor]?"

"When you bought [similar tool], how did
you think about the investment?"

"What's your typical software spend per
employee for tools like this?"

Past behavior predicts future willingness.
```

## Direct Budget Discovery

### Soft Direct Questions
```
Direct but not aggressive:

"Do you have budget allocated for this,
or would this be a new line item?"

"Is this funded from an existing budget,
or would you need to get approval?"

"Have you thought about what you'd want
to invest in solving this?"
```

### Framing with Ranges
```
Make it easier to answer:

"Our customers typically invest between
$20k and $100k depending on team size.
Does that range fit with what you're thinking?"

"Solutions in this space usually run
$500-2000/month. Is that in the ballpark?"

Ranges feel safer than exact numbers.
```

### Budget Timing Questions
```
When budget becomes available:

"When does your next budget cycle start?"

"Is there budget available now, or would
this be a next-quarter thing?"

"What's the typical approval process for
a purchase this size?"
```

## Reading Budget Signals

### Positive Budget Signals
```
Indicates budget exists:
- "We have money set aside for this"
- "I'm authorized up to $X"
- "This fits within our software budget"
- "We budgeted for this project"
- Asks specific pricing questions
- Doesn't flinch at ballpark numbers

Action: Move toward pricing discussion.
```

### Neutral Budget Signals
```
Budget uncertain but possible:
- "I'd need to check with finance"
- "Depends on what we'd get"
- "We haven't budgeted specifically"
- "I could probably find the money"
- Asks about payment terms

Action: Focus on value, justify investment.
```

### Negative Budget Signals
```
Budget likely not available:
- "We have zero budget for this"
- "Everything's frozen right now"
- "I can't spend anything without [approval]"
- Long pause, topic change at pricing
- "Is there a free version?"

Action: Qualify out or long-term nurture.
```

## Qualification Frameworks

### BANT Budget Component
```
Basic qualification:

1. Is there budget? (Y/N)
2. How much? (range or specific)
3. When available? (now vs future)
4. Who controls it? (their authority)

Store:
{
  "has_budget": true,
  "budget_range": "$20k-50k",
  "budget_timing": "this_quarter",
  "budget_authority": "prospect"
}
```

### Budget Qualification Scoring
```python
def score_budget_qualification(responses):
    score = 0

    # Has budget allocated
    if responses.get("budget_exists"):
        score += 30

    # Budget range fits our pricing
    if responses.get("budget_range"):
        range_min = parse_min(responses["budget_range"])
        if range_min >= OUR_MIN_PRICE:
            score += 25

    # Budget available now
    if responses.get("budget_timing") == "now":
        score += 25
    elif responses.get("budget_timing") == "this_quarter":
        score += 15

    # Has spending authority
    if responses.get("has_authority"):
        score += 20

    return score  # 0-100
```

## Pricing Conversation Tactics

### Anchoring High
```
Before revealing price:

"Companies our size typically see $500k+ in
annual savings from this. Our investment is
a fraction of that."

"The cost of not solving this—based on what
you told me—is about $200k/year. Our solution
is significantly less than that."

Anchor on value before discussing price.
```

### Reverse Sticker Shock
```
Preempt the "too expensive" reaction:

"I want to be upfront—we're not the cheapest
option. We're built for companies that prioritize
[value prop]. Does that fit your approach?"

"Before I share pricing, I should mention we're
a premium solution. Is that something you're
open to?"

Sets expectation, qualifies early.
```

### Investment Framing
```
Language matters:

Instead of: "It costs $50,000"
Say: "The investment is $50,000"

Instead of: "That's our price"
Say: "Here's what companies like yours typically invest"

Instead of: "Expensive"
Say: "Premium" or "enterprise-grade"

Frame as investment, not cost.
```

## Handling Budget Objections

### "We don't have budget"
```
Responses:

"Understood. If budget wasn't a constraint,
would this be something you'd move forward with?"
→ Separates budget from interest

"Is that 'no budget at all' or 'not budgeted
yet but could find it for the right solution'?"
→ Clarifies severity

"When does your budget cycle reset? Happy
to reconnect when timing's better."
→ Future opportunity
```

### "That's more than we expected"
```
Responses:

"I hear that a lot initially. Can I show you
how customers justify the investment?"
→ ROI conversation

"What were you expecting? That helps me
understand if there's a fit."
→ Understand their anchor

"We can look at a smaller starting point.
What scope would fit your budget?"
→ Downsell opportunity
```

### "We need to think about it"
```
Often budget-related hesitation:

"Absolutely. Is budget one of the things
you're weighing, or something else?"
→ Surface the real concern

"What information would help you make
the budget case internally?"
→ Enable their internal selling
```

## Enterprise Budget Dynamics

### Budget Cycles
```
Common patterns:

Calendar year companies:
- Budget planning: Oct-Dec
- Best buying: Q1 (fresh budget)
- End of year: Use-it-or-lose-it

Fiscal year companies:
- Varies (common: June, Sept, March)
- Know their fiscal calendar
- Time outreach accordingly
```

### Budget Holders
```
Map the financial hierarchy:

Department budget:
- Manager/Director controls
- Usually <$50k decisions
- Fast approval

Divisional budget:
- VP-level approval
- $50k-500k decisions
- Multiple signatures

Enterprise budget:
- C-suite/board approval
- $500k+ decisions
- Long procurement cycles
```

### Budget Expansion Tactics
```
When budget seems tight:

Multi-year deals:
"Would spreading this over 2-3 years help?"

Phased rollout:
"We could start with just [subset] this year."

ROI guarantee:
"What if we structured this around results?"

Different budget source:
"Could this come from [other department] budget?"
```

## Metrics

### Budget Qualification Metrics
```
Track:
- % of opportunities budget-qualified
- Accuracy of budget estimates vs closed deal
- Time to budget discovery
- Deals lost due to budget (qualified properly?)

Improve:
- Earlier budget conversations
- Better indirect discovery
- Accurate range estimation
```

### Budget-Related Win/Loss
```
Analyze closed deals:

Won deals:
- When was budget confirmed?
- How accurate was initial estimate?
- What enabled the budget?

Lost deals:
- Was budget ever confirmed?
- When did budget objection arise?
- Could we have qualified out earlier?
```

## Bot Implementation

### Budget Discovery Flow
```python
def budget_discovery_flow(conversation_state):
    if not conversation_state.budget_asked:
        # Start with indirect questions
        return {
            "question": "value_based_budget",
            "template": "When you've solved problems like this before, what did that investment typically look like?"
        }

    if conversation_state.budget_signal == "positive":
        # Get specific
        return {
            "question": "budget_range",
            "template": "To make sure I recommend the right package, what budget range are you working with?"
        }

    if conversation_state.budget_signal == "unclear":
        # Try range approach
        return {
            "question": "range_validation",
            "template": "Our typical customers invest $X-Y. Does that align with what you're thinking?"
        }

    if conversation_state.budget_signal == "negative":
        # Qualify timing
        return {
            "question": "budget_timing",
            "template": "When does your budget cycle start? Happy to reconnect when timing's better."
        }
```

### Budget Storage
```json
{
  "prospect_id": "12345",
  "budget_qualification": {
    "status": "qualified",
    "range_min": 20000,
    "range_max": 50000,
    "currency": "USD",
    "timing": "this_quarter",
    "source": "existing_budget",
    "authority": "prospect_controls",
    "confidence": 0.8,
    "discovery_date": "2024-01-15",
    "method": "direct_question"
  }
}
```

