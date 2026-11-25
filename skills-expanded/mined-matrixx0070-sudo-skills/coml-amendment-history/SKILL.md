---
name: coml-amendment-history
version: 1.0.0
description: Build and maintain the amendment and version history of a contract — what changed, when, why, and the current effective terms across the base agreement and all amendments.
author: matrixx0070
tags: [commercial-legal, amendments, versioning, tracking, terms]
capabilities: []
---

## When to use

Use this when a contract has been amended one or more times and you need a single reliable view of what the terms actually are today. It reconstructs the chain from base agreement through every amendment, order form, and SOW so nobody negotiates against a superseded clause.

**Not for:** the substantive review of any single document (use the review skills), or tracking renewal deadlines (coml-renewal-tracker). It records changes; it does not judge them.

## Method

1. Assemble the full document set in date order: base agreement, then each amendment, addendum, order form, and SOW.
2. For each amendment, record the date, the sections it touches, what changed (old → new), and the stated reason if given.
3. Resolve conflicts using the ordering rules: later amendments override earlier ones; check whether order forms or the master agreement control when they disagree.
4. Compile the current effective terms — the net result after all amendments — so the live position is unambiguous.
5. **Escalation gate:** if an amendment quietly shifted a gate term (liability, IP, indemnity, data), or if the controlling-document order is unclear, flag it to counsel.
6. Note any gaps: missing signatures, undated amendments, or referenced documents you do not have.

## Example

Base MSA (2024) liability cap = 12 mo fees. Amendment 1 (2025) raised cap to 24 mo, reason "expanded scope". Amendment 2 (2026) added a data-processing addendum. Current effective terms: cap 24 mo fees; DPA in force. Conflict check: Order Form #7 restated a 12-mo cap — superseded by Amendment 1 per the "latest controls" rule; flagged to counsel to confirm the order form did not intend to re-lower it.

## Pitfalls

- Reading the base agreement as current when a later amendment already changed the clause.
- Missing which document controls when an order form and the master agreement conflict.
- Undated or unsigned amendments treated as effective without confirmation.
- Losing referenced side letters or addenda that alter the terms.

## Output format

```
AMENDMENT HISTORY — <contract> | as of <date>
Chain:
  - <date> <doc> — <sections> — <old → new> — reason: <...>
Controlling-document order: <rule applied>
Current effective terms:
  - <clause>: <live position>
Conflicts / gaps: <items>
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
