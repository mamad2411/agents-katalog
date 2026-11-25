---
name: coml-stakeholder-summary
version: 1.0.0
description: Translate a contract review into a plain-language summary for a business stakeholder — key risks, the recommendation, and the exact decision they need to make.
author: matrixx0070
tags: [commercial-legal, summary, communication, stakeholder, decision]
capabilities: []
---

## When to use

Use this after a review is done, when a non-lawyer decision-maker needs to understand what they are signing and what to decide. It strips the legal detail down to money, risk, and the one decision in front of them.

**Not for:** the review analysis itself (use the review skills), a formal escalation to counsel (coml-escalation-flagger), or a full legal memo. Keep it to what a busy owner reads in two minutes.

## Method

1. Lead with the decision: what you need from them (sign, approve a fallback, hold) and by when.
2. State the deal in one line: counterparty, what it is, value, and term.
3. Give the top three to five risks in plain language — no clause numbers, just the business consequence and how likely it is.
4. Give your recommendation and the reasoning, plus the trade-offs of the alternatives.
5. Separate what is decided from what is still with counsel, so they know what is theirs to call.
6. **Escalation gate:** never present a gate item (uncapped liability, IP shift, data exposure) as a routine sign-off — mark it as counsel-dependent and do not imply it is cleared when it is not.

## Example

> **Decision needed: approve signing the Acme SaaS deal by Friday.**
> Deal: Acme analytics platform, $80K/yr, 1-year term.
> Risks: (1) their liability is capped low, so if they cause a data problem our recovery is limited — medium likelihood; (2) price can rise up to 5% at renewal — low impact; (3) we can exit for convenience with 60 days' notice — low risk.
> Recommendation: sign. The low cap is the main concession; counsel accepted it given the mutual carve-out we negotiated.
> Still with counsel: none — cleared. Your call: the commercial terms.

## Pitfalls

- Burying the decision under legal detail the stakeholder cannot act on.
- Using clause numbers and jargon instead of the business consequence.
- Implying a term is cleared when it is still open with counsel.
- Listing every deviation instead of the few that actually change the decision.

## Output format

```
STAKEHOLDER SUMMARY — <deal> | for: <name> | decision by <date>
Decision needed: <sign / approve fallback / hold>
The deal: <counterparty · what · value · term>
Top risks (plain language):
  - <risk> — impact <low/med/high>, likelihood <low/med/high>
Recommendation: <verdict> — <why>
Still with counsel: <items or none>
Your call: <the specific decision>
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
