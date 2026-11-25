---
name: Salary Negotiator
description: Build a salary negotiation strategy with market data, counter-offer scripts, and fallback plans. Use this skill when someone wants to negotiate a job offer, prepare a counter-offer, understand total compensation, research market rates, or navigate salary discussions. Trigger for "negotiate salary", "counter offer", "how much should I ask for", "is this offer fair", "compensation package", or any mention of negotiating pay, equity, bonus, or benefits.
---

# Salary Negotiator

Build a negotiation plan that maximizes total compensation while maintaining the relationship.

## Research Phase

Before any negotiation, establish the market range using at least two of these sources: Levels.fyi (tech), Glassdoor, LinkedIn Salary, PayScale, Salary.com, H1B salary database (public data for US roles), or direct information from recruiters or peers.

Build a four-point range:
- Floor: 25th percentile (your walk-away point)
- Target: 50th-60th percentile (your realistic ask)
- Ambitious: 75th percentile (your opening number)
- Ceiling: 90th percentile (only with exceptional leverage)

## Total Compensation Breakdown

Never evaluate an offer on base salary alone. Calculate total annual compensation:

```
Base salary
+ Target bonus (as percentage of base)
+ Equity (total grant / vesting years, at current valuation)
+ 401k or pension match (employer contribution)
+ Health insurance (employer-paid portion)
+ Other benefits (HSA contribution, commuter, education)
= Total annual compensation
```

For year-one calculations, add signing bonus separately since it is non-recurring.

## Counter-Offer Strategy

### Timing
1. Receive verbal offer: express enthusiasm, ask for written details
2. Receive written offer: thank them, ask for 48-72 hours to review
3. Research and prepare: build your case
4. Deliver counter: email or call, depending on relationship

### Counter-Offer Structure

Whether by email or call, follow this sequence:
1. Express genuine enthusiasm for the role (be specific about what excites you)
2. Reinforce your value (cite one achievement relevant to their needs)
3. State your ask with a specific number (not a range -- ranges get anchored at the bottom)
4. Justify briefly (market data, competing offer, or scope of role)
5. Signal flexibility ("I am open to discussing the full package")

### When Base Is Firm

Negotiate other elements in this priority order:
1. Signing bonus (one-time cost, easier to approve)
2. Additional equity
3. Earlier performance review (accelerates first raise)
4. Extra PTO days
5. Remote work flexibility
6. Professional development budget
7. Title adjustment
8. Start date flexibility

## Scripts

**Email counter:**
"Thank you for the offer to join [Company] as [Title]. I am genuinely excited about [specific aspect]. After reviewing the details and researching market rates for this role, I would like to discuss a base salary of $[X]. This reflects [brief justification]. I am flexible and happy to discuss the overall package. Would you have time for a quick call this week?"

**When asked for expectations first:**
"I am focused on finding the right role and am flexible on compensation. What is the range budgeted for this position?"

**When they will not budge:**
"I understand the base is set. Could we explore a signing bonus of $[X] to bridge the difference?"

**When you have competing offers:**
"I want to be transparent: I have another offer at $[X]. [Your company] is my preference because [genuine reason], and I am hoping we can find a competitive package."

## Output Format

```
NEGOTIATION PLAN

MARKET DATA
Role: [title], Location: [city/remote], Experience: [years]
Market range: $[floor] - $[ceiling]
Sources: [list]

CURRENT OFFER
Base: $X | Bonus: X% | Equity: $X/yr | Signing: $X | Benefits: ~$X
Year 1 Total: $X
Ongoing Total: $X

COUNTER PROPOSAL
Ask: $[specific number]
Justification: [1-2 sentences]
Fallback elements: [list in priority order]
Walk-away point: $[minimum acceptable total comp]

SCRIPTS
[Counter email or call script customized to the situation]
[Pushback response if they say no to base]
```
