---
name: csm-renewal-prep
version: 1.0.0
description: Prepare an account renewal with a value recap, risk assessment, and a clear negotiation posture.
author: matrixx0070
tags: [customer-success, renewal, retention, negotiation, value]
capabilities: []
---

## When to use

Use this when a contract renewal is approaching and you need to enter it prepared: value proven, risks known, and a posture set. Reach for it 90-120 days before the renewal date, or whenever renewal strategy must be locked before commercial conversations begin.

**Not for:** an account already signaling churn (run csm-churn-save first, then return here); growing an account beyond its current contract (see csm-expansion-play); the periodic value review itself (see csm-qbr, which often feeds this).

## Method

1. Build the value recap: what the customer bought it for, what was delivered, and the dollarized/quantified impact. Decision point: if value is weak or unproven, that is the renewal risk — address it before the commercial ask.
2. Score renewal risk across sponsor stability, adoption trend, competitive pressure, budget climate, and open escalations. Assign a likelihood: safe / at-risk / uncertain.
3. Confirm the decision process: who signs, budget cycle, procurement steps, and lead time. Decision point: if procurement is involved, start early — legal/security reviews sink on-time renewals.
4. Set your posture based on risk and value: strong value + safe → hold or raise price and seek expansion; weak value or at-risk → protect the base, minimize concessions, secure a quick win first.
5. Prepare for likely objections (price, ROI doubt, competitor) with evidence-based responses, not discounts.
6. Define your concession ladder and walk-away in advance — know what you'll trade (term length, case study, reference) for what.
7. Line up the sponsor as an internal advocate and confirm the timeline to signature.

## Example

Account renewing in 90 days, ARR $120K. Value recap: automated onboarding cut their new-hire ramp from 6 weeks to 3, ~$200K saved annually. Risk: safe (sponsor stable, adoption up, no competitor). Decision: VP signs, budget locked in Q3, light procurement. Posture: hold price, propose 5% uplift, seed a seat expansion. Objection prep: if price pushback, lead with the $200K saved. Concession ladder: trade a 2-year term for flat pricing; walk-away = no discount below current price without term extension.

## Pitfalls

- **Starting too late.** Procurement and security reviews need runway; a great value story dies on a missed deadline.
- **Discount-first negotiation.** Opening with a concession forfeits value you've earned and anchors the customer low.
- **No documented value.** Walking in without proof turns renewal into a price defense you'll lose.
- **Assuming the sponsor equals the signer.** The person who loves you may not control the budget.

## Output format

```
RENEWAL PREP — <account> | ARR: <$> | renewal date: <date>
Value recap: <bought for> → <delivered> → <$ impact>
Risk: <safe|at-risk|uncertain> — drivers: <sponsor/adoption/competitor/budget/escalations>
Decision process: signer <name> | budget cycle <when> | procurement <yes/no + lead time>
Posture: <hold/raise/protect> — target: <price/term outcome>
Objection prep: <objection → evidence response>
Concession ladder: <trade → for> | Walk-away: <line>
Sponsor advocacy: <name> | Timeline to signature: <dates>
```
