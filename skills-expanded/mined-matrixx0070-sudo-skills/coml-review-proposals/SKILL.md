---
name: coml-review-proposals
version: 1.0.0
description: Review a vendor proposal, quote, SOW, or order form for commercial and legal traps before it converts into a binding order.
author: matrixx0070
tags: [commercial-legal, proposal, sow, order-form, review, escalation]
capabilities: []
---

## When to use

Use this for the pre-contract paper — a vendor proposal, quote, statement of work, or order form — before it is countersigned and becomes binding. These documents look informal but often carry pricing, term, and incorporated legal terms that lock you in.

**Not for:** the master agreement the order form rides on (use coml-saas-msa-review), a standalone services contract (coml-vendor-agreement-review), or turning your own review findings into redlines (that is the drafting step inside each review skill).

## Method

1. Read what the document actually commits you to: total value, term length, quantity, and start date — not just the headline price.
2. Hunt for hidden bindings: auto-renewal, minimum commitments, incorporated-by-reference terms, and "acceptance of quote constitutes agreement" language.
3. Check pricing mechanics: one-time vs recurring, price-increase caps, overage rates, and payment terms against the vendor and SaaS tables.
4. Verify scope precision so it cannot drift into change orders later.
5. **Escalation gate:** if the proposal incorporates unseen terms, waives your standard protections, or exceeds your signing authority, route to counsel before anyone signs or clicks accept.
6. Return a proceed / clarify / reject verdict with the specific items to fix before signature.

## Example

SaaS order form, $40K/yr, "3-year term, auto-renews, governed by vendor's online MSA." Traps: 3-year lock (clarify — expected 1 year), evergreen auto-renew (fix), online MSA not reviewed (escalate — incorporated terms unseen), net-15 payment (fallback). Verdict: clarify + escalate. Fix before signature: pull and review the online MSA; convert to 1-year term with opt-in renewal.

## Pitfalls

- Treating a quote as non-binding when it says acceptance forms the contract.
- Signing an order form that incorporates an online MSA nobody has read.
- Anchoring on the discounted year-one price while missing the uncapped renewal uplift.
- Vague SOW scope that becomes a change-order fight after work starts.

## Output format

```
PROPOSAL REVIEW — <vendor> | doc: <quote/SOW/order form> | value
Commits you to: <term / quantity / total>
Hidden bindings: <auto-renew / minimums / incorporated terms>
Pricing: <recurring? cap? overage? payment>
Verdict: PROCEED | CLARIFY | REJECT
Fix before signature: <items>
Escalated to counsel: <items or none>
```

## Reference

**Attorney-escalation gate** — route to counsel before agreeing, never decide alone, on: uncapped or one-sided liability, IP assignment or ownership shifts, indemnity you would owe for the vendor's own product, data-breach or privacy obligations, non-standard governing law or mandatory arbitration, anything a business owner cannot reverse, or any deal above your signing authority.

### NDA clauses
| Clause | Standard | Fallback | Walk-away |
|---|---|---|---|
| Term | 2-3 yr (trade secrets survive longer) | up to 5 yr | perpetual on ordinary CI |
| Mutuality | mutual | one-way when we only disclose | one-way binding us as recipient |
| CI definition | marked or reasonably identifiable | all disclosed | "anything discussed", no carve-outs |
| Carve-outs | public / independently developed / rightfully received / compelled | narrowed set | none |
| Residuals | none | narrow, memory-only | broad reuse license |
| Remedies / law | mutual injunctive, our or neutral law | neutral law, no bond | one-sided + liquidated damages |

### SaaS / MSA clauses
| Clause | Standard | Fallback | Walk-away |
|---|---|---|---|
| Liability cap | 12 mo fees | 24 mo fees | uncapped for us / their cap ≤3 mo |
| Cap carve-outs | IP, confidentiality, data breach | + willful misconduct | breach uncapped against us only |
| Indemnity | mutual IP; vendor covers data breach | mutual | we indemnify their product |
| Data | customer owns; export on exit | customer owns | vendor licenses or resells data |
| Security / SLA | SOC 2 + 99.9% + credits | 99.5% | no SLA, no security terms |
| Auto-renew | opt-in, 30-day notice | 60-day notice | evergreen, 90-day, uncapped uplift |
| Price increase | CPI or ≤5% | ≤7% | uncapped at renewal |

### Vendor / services clauses
| Clause | Standard | Fallback | Walk-away |
|---|---|---|---|
| Payment | net-30 / net-45 | net-15 | full prepay, no milestones |
| IP in deliverables | work-for-hire to us | perpetual license to us | vendor retains |
| Insurance | ≥$1M GL + cyber | $500K | none |
| Termination | for cause + convenience, 30-day | for cause only | locked full term, no exit |
| Audit / compliance | annual audit right | on cause | none |

### Renewal-notice tracking
| Field | Capture |
|---|---|
| Effective / expiry date | contract dates |
| Notice window | e.g. 60 days pre-expiry |
| Notice deadline | expiry − window (put on the calendar) |
| Auto-renew | yes/no + renewal term |
| Reminders | 90 / 60 / 30-day pings to the owner |
