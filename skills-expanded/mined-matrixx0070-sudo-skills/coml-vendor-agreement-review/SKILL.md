---
name: coml-vendor-agreement-review
version: 1.0.0
description: Review a vendor or services agreement against the playbook — payment, IP in deliverables, insurance, termination, and audit rights — and return a redline-ready verdict.
author: matrixx0070
tags: [commercial-legal, vendor, services, review, ip, escalation]
capabilities: []
---

## When to use

Use this for a vendor, contractor, consulting, or professional-services agreement where a supplier does work or delivers goods for you. It focuses on getting paid terms right, owning what you pay to create, and being able to exit.

**Not for:** a SaaS subscription or software MSA (use coml-saas-msa-review), an NDA (coml-nda-review), or a proposal/SOW that has not yet become a contract (coml-review-proposals).

## Method

1. Confirm scope and structure: is the SOW attached, and does it match what was proposed? Missing or vague scope is the most common source of disputes.
2. Score commercial terms — payment schedule, milestones, and price — against the vendor table.
3. Score protective terms — IP ownership in deliverables, insurance, termination, and audit rights. **Escalation gate:** any shift of IP ownership away from you, an indemnity you would owe for the vendor's own product or IP, or missing insurance goes to counsel before you agree.
4. Confirm you can terminate for convenience with reasonable notice and are not locked into the full term.
5. Draft redlines for each deviation and set the verdict.

## Example

Consulting agreement, $60K fixed. Payment 100% prepay (walk-away), IP: vendor retains deliverables (walk-away), no insurance clause (walk-away), termination for cause only (fallback). Verdict: negotiate. Redlines: net-30 tied to milestones; work-for-hire assignment of all deliverables to you; require ≥$1M GL plus cyber; add termination for convenience on 30-day notice. IP assignment language escalated to counsel.

## Pitfalls

- Paying for work but letting the vendor keep the IP because the assignment clause was silent.
- Full prepayment with no milestone gating and no leverage if delivery slips.
- No insurance requirement, leaving you exposed if the vendor causes damage.
- Vague SOW that lets scope drift and invites change-order disputes.

## Output format

```
VENDOR REVIEW — <vendor> | value: <$> | term
SOW attached: <yes/no> | scope clear: <yes/no>
Verdict: SIGN | NEGOTIATE | REJECT
Commercial: <payment / milestones / price> — <standard|fallback|walk-away>
Protective: <IP / insurance / termination / audit>
Redlines: <clause → proposed language>
Escalated to counsel: <items>
Renewal/term: <auto-renew? notice deadline>
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
