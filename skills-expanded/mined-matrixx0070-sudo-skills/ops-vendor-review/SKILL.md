---
name: ops-vendor-review
version: 1.0.0
description: Evaluate a vendor on capability fit, total cost of ownership, and risk, ending in a defensible choose/negotiate/reject verdict.
author: matrixx0070
tags: [operations, vendor, procurement, tco, risk, scorecard]
capabilities: []
---

# Vendor Review

## When to use
Use this to evaluate a prospective or incumbent vendor before purchase, renewal, or replacement, when comparing shortlisted options, or when a spend needs a defensible recommendation for approval.

**Not for:** deep security due diligence alone (use ops-risk-assessment for that dimension), or negotiating price once the vendor is already chosen. This produces the *decision*, not the contract.

## Method
1. **Frame the decision.** State the need the vendor fills, the alternatives (including build and do-nothing), and the decision deadline.
2. **Score capability fit.** Rate how well the offering meets must-have and nice-to-have requirements; note gaps. *Decision:* any unmet must-have is disqualifying regardless of price — flag it before scoring further.
3. **Compute TCO.** Sum all costs over the horizon: license/subscription, implementation, integration, training, support, and exit/migration. Do not stop at sticker price.
4. **Assess risk.** Evaluate financial stability, security/compliance posture, lock-in and data portability, SLA strength, and support responsiveness.
5. **Weigh trade-offs.** Build a weighted scorecard across cost, fit, risk, and support; compute a total per option.
6. **Recommend.** Give a clear choose / negotiate / reject verdict with reasoning and the conditions or contract terms to secure.
7. **Plan the exit.** Note how to leave if it fails — data export and switching cost.

## Example
Comparing Vendor A ($40k/yr sticker) vs. Vendor B ($55k/yr). TCO over 3 years: A = $180k (heavy integration + no bulk export), B = $175k (turnkey, clean export API). A fails the must-have "SSO" gap. Weighted scorecard (fit 40%, TCO 30%, risk 20%, support 10%): B wins 8.1 vs. 6.2. **Verdict: choose B**; negotiate a 3-year price lock and a data-export SLA. **Exit:** B's export API keeps switching cost low.

## Pitfalls
- **Anchoring on sticker price.** Implementation, integration, and exit costs often dwarf the license; TCO is the real number.
- **Ignoring lock-in.** A cheap vendor you can't leave is expensive later — always price the exit.
- **Scoring without weights.** Equal-weighting a nice-to-have against a must-have produces a wrong winner; weight deliberately.
- **No do-nothing baseline.** Without the build/status-quo alternative, every vendor looks justified.

## Output format
```
Need:        problem + alternatives (incl. build / do-nothing) + deadline
Capability:  requirement | must/nice | met? | notes
TCO table:   cost line | year 1 | ongoing | total over horizon
Risk:        dimension | rating | notes
Scorecard:   criterion | weight | score per option | totals
Recommendation: verdict (choose/negotiate/reject) | rationale | terms
Exit plan:   data export | switching cost
```
