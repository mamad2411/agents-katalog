---
name: coml-escalation-flagger
version: 1.0.0
description: Scan a contract or review output for terms that must go to an attorney before agreement, and produce a routed escalation packet with facts, the ask, and a deadline.
author: matrixx0070
tags: [commercial-legal, escalation, counsel, risk, routing]
capabilities: []
---

## When to use

Use this the moment a review surfaces a term you are not authorized to accept, or when you need a clean handoff to counsel that they can act on without a second round of questions. It converts a flagged issue into a decision-ready packet.

**Not for:** the substantive clause review itself (use the review skills), or summarizing an already-cleared contract for a business owner (coml-stakeholder-summary).

## Method

1. Run every candidate term against the escalation gate below. A term qualifies if it is uncapped/one-sided liability, shifts IP, creates indemnity for the vendor's product, touches data/privacy, uses non-standard law or arbitration, is irreversible for the business, or exceeds your signing authority.
2. For each qualifying term, quote the exact language and cite where it lives (section, document).
3. Separate fact from hypothesis: mark what the clause plainly says `[confirmed]` versus your read of its effect `[interpretation]`.
4. State the specific ask to counsel — a yes/no, a fallback to approve, or a redline to draft — and a deadline tied to the deal timeline.
5. Name the owner and the interim posture so the deal does not stall or advance past the gate.

## Example

> **[ESCALATE] Uncapped data-breach liability — MSA §11.3**
> `[confirmed]` breach liability is excluded from the cap, one direction (against us only).
> `[interpretation]` a single incident could exceed the contract value many times over.
> Ask: counsel to approve a mutual cap carve-out capped at 2x fees, or advise walk-away, by Thursday.
> Owner: @legal-ops · Interim: deal held at redline, not signed.

## Pitfalls

- Escalating a vague concern with no quoted language, forcing counsel to re-read the whole contract.
- Blending what the clause says with what you fear it means — mark them separately.
- No deadline, so the escalation sits while the deal clock runs.
- Letting the deal advance past the gate while the escalation is open.

## Output format

```
ESCALATION PACKET — <counterparty> | contract | date
Gate items:
  - [ESCALATE] <term> — <section>
    [confirmed] <what it says>
    [interpretation] <effect>
    Ask: <yes/no | fallback | redline> by <deadline>
Owner: @<name> · Interim posture: <held/other>
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
