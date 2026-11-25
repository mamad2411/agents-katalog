---
name: privl-dpa-review
version: 1.0.0
description: Review a Data Processing Agreement for the mandatory controller-processor clauses, transfer mechanisms, sub-processor terms, and liability gaps before signature.
author: matrixx0070
tags: [privacy, legal, dpa, contract, processor, gdpr-art28, sccs]
capabilities: []
---

## When to use

Use this when a vendor, sub-processor, or customer sends a DPA (or its DPA is missing) and you must check it covers the legally required terms before signing or onboarding. It is a clause-completeness and risk review, not contract negotiation authority.

**Not for:** deciding whether to use the vendor at all (privl-use-case-triage), assessing your own processing (privl-pia-generation), or drafting the whole master agreement. If there is no DPA at all and personal data will flow, that is a blocker — flag it, do not paper over it.

## Method

1. Fix the roles: are you controller, processor, or joint controller, and what is the counterparty? The required clauses follow from this.
2. Check the **Art. 28(3) mandatory clauses**: processing only on documented instructions; confidentiality obligations on staff; security measures (Art. 32); sub-processor authorization + flow-down; assistance with data-subject rights; assistance with Art. 32-36 duties; deletion/return at end; audit/inspection rights and information duty; breach notification (with timeline).
3. Check **international transfers**: if data leaves the EEA/UK, is there a valid mechanism (adequacy, SCCs with the correct modules, UK IDTA/Addendum, DPF certification)? Confirm a transfer impact assessment is contemplated.
4. Review sub-processor terms: general vs specific authorization, change-notice period, objection right, and equivalent-terms flow-down.
5. Check liability, indemnity, breach-notice timing, and audit practicality against your risk posture.
6. **Decision point:** list missing/weak clauses as must-fix vs. negotiable.
7. **Attorney-escalation gate:** missing Art. 28 terms, an unmechanized transfer, uncapped/imbalanced liability, or joint-controller ambiguity → route to counsel before signature.

## Example

> **DPA:** analytics vendor, you = controller.
> **Findings:** instructions + security + deletion present; **missing** breach-notice timeline; sub-processor change gives no objection right; US transfer cites SCCs but no module specified.
> **Verdict:** three must-fix; transfer module + breach timeline routed to counsel; do not sign as-is.

## Pitfalls

- Assuming a "DPA" heading means the Art. 28 terms are actually present — check each clause.
- Accepting "we use SCCs" without confirming the correct module and a transfer assessment.
- Ignoring silent breach-notification timing — "without undue delay" with no hours is weak.
- Treating unlimited sub-processor swaps with no notice as acceptable.

## Output format

```
DPA REVIEW — <counterparty> | roles: <controller/processor>
Art. 28 clauses: <present / missing per item>
Transfers: <mechanism + gap>
Sub-processors: <authorization type + objection right>
Liability/breach-notice: <finding>
Must-fix: <list> | Negotiable: <list>
For counsel: <items> | Sign-ready: <y/n>
```

## Reference

- **GDPR Art. 28(3)(a)-(h)** the eight mandatory processor-contract terms; **Art. 28(2)/(4)** sub-processor rules.
- **Art. 32** security of processing; **Chapter V / Art. 46** transfer mechanisms (SCCs), UK IDTA/Addendum, EU-US DPF.
- **CCPA §1798.140** service-provider vs. contractor vs. third-party contract terms.
- Escalate missing Art. 28 terms, unmechanized transfers, and liability imbalance to an attorney.
