---
name: prodl-customize
version: 1.0.0
description: Tune the product-legal review skills to your company's risk tolerance, jurisdictions, product type, and escalation chain before running them.
author: matrixx0070
tags: [product-legal, configuration, risk-tolerance, jurisdiction, escalation, policy]
capabilities: []
---

## When to use
Use this once per company (and revisit quarterly) to set the parameters the other product-legal skills assume: your risk appetite, the markets you sell in, your product category, and who counsel is. A review calibrated to a seed-stage consumer app differs from one for a regulated fintech; this makes that difference explicit and repeatable.

**Not for:** reviewing a specific launch (use `prodl-launch-review`), spotting one issue (use `prodl-is-this-a-problem`), or a general intake (use `prodl-cold-start-interview`).

## Method
1. **Set risk tolerance.** Conservative, moderate, or aggressive — this shifts where the launch-risk rubric trips from "proceed" to "hold".
2. **Declare jurisdictions.** Where do you market and sell? Each adds rules (EU GDPR/UCPD, CA CCPA/CPRA, UK, minors regimes).
3. **Pick product category.** Consumer, B2B SaaS, health/wellness, fintech, kids — category sets the default sensitivity floor.
4. **Define the escalation chain.** Name the internal reviewer, then the attorney (in-house or outside counsel) and the trigger for reaching each.
5. **List standing prohibitions.** Claims or practices you never ship (e.g., "guaranteed returns", dark-pattern renewals).
6. **Write the config record.** Store it as the profile every downstream skill reads first.

## Example
A moderate-tolerance B2B SaaS company selling in the US and EU sets: sensitivity floor = standard; standing prohibition on unsubstantiated uptime SLAs; escalation = PM reviews, Legal Ops triages, outside counsel for any EU data-transfer or health-adjacent claim. A later launch touting "99.99% uptime" now auto-trips the standing-prohibition check unless an SLA report backs it.

## Pitfalls
- **Copying another company's profile.** Risk tolerance is a leadership decision, not a template default.
- **Forgetting a live market.** An undeclared jurisdiction means its rules go unchecked.
- **No named attorney.** An escalation chain that ends nowhere fails at the moment it matters.
- **Set-and-forget.** New markets, products, or regulations invalidate the profile; re-run it.

## Output format
```
Company / profile date:
Risk tolerance: conservative | moderate | aggressive
Jurisdictions:
Product category / sensitivity floor:
Escalation chain: reviewer -> triager -> attorney (trigger)
Standing prohibitions:
Review cadence for this profile:
```

## Reference
**FTC substantiation baseline.** Regardless of tolerance, the "reasonable basis before dissemination" standard is not tunable — you cannot configure it away. Aggressive tolerance widens what you attempt, never what evidence a claim requires.

**Launch-risk rubric calibration.** The rubric's proceed/hold thresholds shift with tolerance, but audience-vulnerability (minors, health, finance) and legally mandated disclosures stay fixed at conservative regardless of the profile.

**When to escalate to counsel.** Configuration itself is a legal-policy act: have counsel approve the risk-tolerance and standing-prohibition settings. This skill records a policy; it does not create one, and it is not legal advice. Any profile touching regulated categories should be signed off by an attorney.
