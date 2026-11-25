---
name: prioritization-frameworks
description: "Score and rank product initiatives using RICE, ICE, and value-effort frameworks. Makes prioritization transparent and defensible while acknowledging that math doesn't remove all judgment. Use when the backlog is growing, stakeholders disagree on priorities, or you need to justify decisions to leadership."
---

# Prioritization Frameworks

Decide what to build next with structured scoring, not gut feeling or politics.

## How to use

- `/prioritization-frameworks` Apply prioritization constraints to this conversation.
- `/prioritization-frameworks <backlog>` Score and rank a list of initiatives.

## Constraints

### RICE Scoring
- Reach: how many users affected in a given time period. MUST use specific numbers, not "all users."
- Impact: how much it moves the needle per user. Scale: 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal. Most features are 1 or 0.5.
- Confidence: how sure about Reach and Impact. 100% = strong data, 80% = good evidence, 50% = mixed, 20% = pure gut.
- Effort: person-months total. Include design, engineering, QA, docs, launch prep.
- Score = (Reach × Impact × Confidence) ÷ Effort
- BEST FOR: large backlogs needing rigorous comparison

### ICE Scoring
- Impact (1-10), Confidence (1-10), Ease (1-10 where 10 = easiest)
- Score = Impact × Confidence × Ease
- BEST FOR: quick ranking, small teams, limited reach data

### Value vs. Effort Matrix
- High value + low effort = Quick Wins (do first)
- High value + high effort = Big Bets (plan these)
- Low value + low effort = Fill-ins (maybe later)
- Low value + high effort = Money Pits (don't do)
- BEST FOR: executive communication and alignment meetings

### Scoring Rules
- MUST score in batches of 10-20 items, not individually. Relative comparison improves accuracy.
- Items within 10% of each other are effectively tied. Group into tiers, don't strict-rank.
- MUST re-score when context changes: competitive threats, customer feedback waves, churn signals.
- Separate scoring from deciding. Let the framework rank, then apply judgment. If #1 feels wrong, explore why.
- SHOULD allocate a fixed capacity percentage for strategic work (tech debt, experiments) that doesn't score well in feature-focused frameworks.

### Anti-Patterns
- HiPPO override: highest paid person always wins regardless of scores. Make scoring transparent.
- Urgency bias: whatever's loudest today jumps to the top. Separate urgent from important.
- Pet project inflation: someone inflates Impact to get their favorite ranked higher. Require evidence for Impact above 1.
- Analysis paralysis: spending more time scoring than building. Timebox to 5 minutes per item.
- Ignoring dependencies: Item A depends on Item B that scores lower. Group and score the bundle.
