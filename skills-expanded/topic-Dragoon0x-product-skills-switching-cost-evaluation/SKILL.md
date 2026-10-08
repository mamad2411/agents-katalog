---
name: switching-cost-evaluation
description: "Analyze the real cost of switching between products — financial, technical, operational, political, and emotional. Use when trying to win customers from competitors, worried about churn to alternatives, designing migration tools, or setting pricing relative to switching friction."
---

# Switching Cost Evaluation

Understand the real cost of switching — it's never just money.

## How to use

- `/switching-cost-evaluation` Apply switching cost constraints to this conversation.
- `/switching-cost-evaluation <from> <to>` Evaluate switching costs between two specific products.

## Constraints

### Five Types of Switching Costs
MUST assess all five. Most teams only think about the first.

1. Financial: remaining contracts, migration costs, duplicate subscriptions during transition
2. Technical: data migration, integration rewiring, custom config loss, API changes, learning curve
3. Operational: team retraining, process changes, productivity dip, documentation updates
4. Political: who championed the current tool, executive approval needed, blame risk if switch fails
5. Emotional: familiarity, identity ("we're a Slack company"), fear of the unknown, vendor relationships

### Scoring
- Rate each type 1-5 (1 = negligible, 5 = could prevent the switch)
- Total score out of 25
- 5-10: low. Compete on product merit. Easy to win, easy to lose.
- 11-17: moderate. Need clear ROI story and migration support.
- 18-25: high. Need a compelling event (contract renewal, failure, leadership change) to create an opening.

### Offensive Strategy (Winning Switchers)
- SHOULD offer free migration tools or import-from-competitor features
- SHOULD time outreach around contract renewals and competitor price increases
- MUST build a clear ROI case: (new product value - current value) > total switching cost
- NEVER assume product quality alone overcomes high switching costs

### Defensive Strategy (Keeping Customers)
- SHOULD increase healthy switching costs through deep workflow integration, historical data, and team expertise
- NEVER increase switching costs through toxic lock-in (hard-to-export data, hidden cancellation, contract handcuffs)
- Goal: be hard to leave because you're valuable, not because you've trapped them

### Anti-Patterns
- Only evaluating financial costs and ignoring the other four
- Assuming switching cost is zero because your product is better
- Using lock-in tactics that breed resentment and eventually backfire
- Ignoring political dynamics — the person who championed the old tool has veto power
