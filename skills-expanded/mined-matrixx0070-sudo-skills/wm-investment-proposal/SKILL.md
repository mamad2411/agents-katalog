---
name: wm-investment-proposal
version: 1.0.0
description: Structure an investment proposal — objective, risk profile, proposed allocation, rationale, costs, and suitability notes — as advisory support for client review.
author: matrixx0070
tags: [wealth-management, investment-proposal, allocation, suitability, risk-profile, advisory]
capabilities: []
---

## When to use

Reach for this when you are an advisor drafting a proposed portfolio or strategy for a client to consider — mapping their objective and risk tolerance to a target allocation with clear rationale and disclosed costs. Use it to organize the argument for a strategy before a client conversation.

**Not for:** executing or trimming an existing book to targets (that is wm-portfolio-rebalance) or the full plan (wm-financial-plan). It does not constitute personalized investment advice or a recommendation to buy any specific security; it is educational and advisory-support. Route the decision to a licensed advisor.

## Method

1. **State the objective and constraints** — return objective, time horizon, liquidity needs, income requirements, and any constraints (ESG screens, concentrated positions, tax lots to avoid).
2. **Establish the risk profile** — document risk tolerance and risk capacity separately; the lower of the two governs. Decision point: if tolerance and capacity conflict, propose to the more conservative and note the tension.
3. **Propose the allocation** — target weights by asset class, then representative vehicles. Justify each sleeve against the objective, not against recent performance.
4. **Show cost and tax friction** — weighted expense ratio, any transaction or advisory costs, and expected tax impact of implementing from the current state.
5. **Compare to a baseline** — proposed vs. current (or vs. a simple index blend) on expected return, risk, and cost so the client sees the marginal case.
6. **Add suitability and disclosures** — why the proposal fits the documented profile, key risks, and standard disclosures. Present as an option for discussion.

## Example

A client with a 15-year horizon but low stated risk tolerance asks for "growth." Weak: propose 90% equities because the horizon is long. Strong: "Your capacity supports more equity, but your tolerance is moderate — the lower governs, so I'm proposing 60/40. Expected return ~5.8% vs. your current ~5.2%, weighted expense 0.11% vs. 0.34%, and moving to it realizes ~$3,100 in gains. Here's the trade-off if you wanted to lean more aggressive." The conservative constraint wins and the marginal case is quantified.

## Pitfalls

- Proposing off recent performance instead of the client's objective and profile.
- Conflating risk capacity with risk tolerance; document both, let the lower govern.
- Ignoring the tax cost of moving from the current portfolio into the proposal.
- Framing the proposal as a directive; keep it an option and route the decision to a licensed advisor.

## Output format

```
Client: [name] | Proposal date:
Objective: [return goal, horizon, income/liquidity needs, constraints]
Risk profile: tolerance [level] | capacity [level] | governing [lower]
Proposed allocation: [asset class | target % | representative vehicle | rationale]
Cost & tax: weighted expense [%], transaction/advisory [$], est. tax to implement [$]
Comparison: proposed vs. current — expected return / risk / cost
Suitability: why it fits the documented profile | key risks
Disclosures: not a recommendation to buy any specific security; discuss with a licensed advisor
```

## Reference

Suitability and best-interest frameworks (e.g., Reg BI / fiduciary standards) and modern-portfolio-theory allocation principles. Confirm firm suitability documentation before presenting.
