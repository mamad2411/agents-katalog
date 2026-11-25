---
name: coml-renewal-tracker
version: 1.0.0
description: Track contract renewal and notice windows so termination and renegotiation deadlines are never missed — calculate the notice deadline, set reminders, and flag decisions due.
author: matrixx0070
tags: [commercial-legal, renewal, notice, deadlines, tracking]
capabilities: []
---

## When to use

Use this to build or update the renewal calendar for one or many active contracts. Its job is to make sure no auto-renewal fires silently and no termination window closes before a decision is made.

**Not for:** deciding whether to renew or the negotiation posture (that is a renewal-prep conversation), or reviewing the terms themselves (use the review skills). Version history of amendments lives in coml-amendment-history.

## Method

1. For each contract, capture the effective and expiry dates, the notice window (e.g. 60 days before expiry), and whether it auto-renews and for what term.
2. Calculate the notice deadline: expiry date minus the notice window. This — not the expiry date — is the date that matters.
3. **Decision point:** if the notice deadline is inside 90 days, it is active — assign an owner and a renew/renegotiate/terminate decision now.
4. Set reminders at 90 / 60 / 30 days before the notice deadline, routed to the named owner.
5. **Escalation gate:** if renewal carries an uncapped price uplift or newly incorporated terms, route to counsel before the notice deadline, not after renewal fires.
6. Keep the register sorted by nearest notice deadline so the next action is always on top.

## Example

Contract expiry 2026-12-31, 60-day notice window, evergreen auto-renew, 8% uplift. Notice deadline = 2026-11-01. Today is inside 90 days → active. Owner assigned; reminders set for 90/60/30 days out. Uplift is uncapped-style (8%) → escalate to renegotiate before 2026-11-01, or the price locks for another term.

## Pitfalls

- Tracking the expiry date instead of the notice deadline and missing the window by weeks.
- Assuming a contract can be exited at expiry when it silently auto-renews before then.
- One reminder only — if the owner is out, it is missed; stagger 90/60/30.
- Forgetting that renewal can trigger a price increase or new terms that need review, not just a signature.

## Output format

```
RENEWAL REGISTER (sorted by notice deadline)
| Contract | Expiry | Notice window | Notice deadline | Auto-renew | Owner | Decision | Status |
|---|---|---|---|---|---|---|---|
| <name> | <date> | <days> | <date> | <yes/no+term> | @<name> | renew/renegotiate/terminate | active/watch |
Next action: <contract> — <what> by <notice deadline>
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
