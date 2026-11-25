---
name: coml-saas-msa-review
version: 1.0.0
description: Review a SaaS agreement or master services agreement against the playbook — liability, indemnity, data, security, SLA, renewal, and termination — and return a redline-ready verdict.
author: matrixx0070
tags: [commercial-legal, saas, msa, review, liability, data, escalation]
capabilities: []
---

## When to use

Use this for a SaaS subscription agreement, MSA, or cloud terms of service where your company is the customer taking on a recurring commitment. It covers the money terms, the risk allocation, and the exit.

**Not for:** an NDA (use coml-nda-review), a one-off services or vendor deal with no software (coml-vendor-agreement-review), or an order form/quote riding on top of an existing MSA (coml-review-proposals).

## Method

1. Confirm structure: is this a standalone agreement or an order form incorporating an MSA by reference? Pull in every document referenced.
2. Score the money terms — fees, price-increase caps, auto-renewal, and termination — against the SaaS/MSA table.
3. Score the risk terms — liability cap, cap carve-outs, indemnity, data ownership, security, and SLA. **Escalation gate:** uncapped or one-sided liability, indemnity you would owe for the vendor's product, or any data/privacy obligation goes to counsel before you agree.
4. Check the exit: can you terminate, and do you get your data out on the way out?
5. Draft redlines for each fallback/walk-away term, then set the verdict.

## Example

SaaS MSA, $80K/yr. Liability capped at 3 months' fees (walk-away — too low), data-breach liability uncapped against you only (walk-away), evergreen auto-renew with 90-day notice and uncapped uplift (walk-away), customer owns data (standard). Verdict: negotiate hard. Redlines: cap at 12 months' fees with IP/confidentiality/breach carved out mutually; convert auto-renew to opt-in with 60-day notice and a 5% uplift cap. Liability and indemnity escalated to counsel.

## Pitfalls

- Reviewing the order form but not the MSA it incorporates — the traps live in the referenced terms.
- Accepting a liability cap of a few months' fees while your breach exposure is uncapped.
- Missing an evergreen auto-renewal that locks you in with a long notice window.
- No data-export right, so leaving the vendor means abandoning your data.

## Output format

```
SAAS/MSA REVIEW — <vendor> | value: <$/yr> | term
Docs reviewed: <agreement + incorporated order forms>
Verdict: SIGN | NEGOTIATE | REJECT
Money terms: <fees / price cap / auto-renew / termination> — <standard|fallback|walk-away>
Risk terms: <liability / carve-outs / indemnity / data / security / SLA>
Redlines: <clause → proposed language>
Escalated to counsel: <items>
Renewal: notice window <days>, deadline <date>
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
