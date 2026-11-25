---
name: coml-matter-workspace
version: 1.0.0
description: Set up and maintain a tracking workspace for a single contract matter — parties, key dates, documents, review status, and open items with owners.
author: matrixx0070
tags: [commercial-legal, matter, workspace, tracking, organization]
capabilities: []
---

## When to use

Use this to organize an active contract matter from first draft through signature so nothing is lost across drafts, reviewers, and negotiation rounds. It is the container the review, escalation, renewal, and amendment skills feed into.

**Not for:** the substantive review of a document (use the review skills), configuring the org's playbook (coml-cold-start-interview, coml-customize), or a lightweight one-off NDA you will sign the same day.

## Method

1. Open the matter record: counterparty, contract type, business owner, deal value, target signature date, and current status.
2. Register every document with its version and date; mark which is the current draft so reviewers never work off a stale copy.
3. Link the working artifacts: the review verdict, any escalation packet, the renewal-tracker entry, and the amendment history once signed.
4. Maintain an open-items log — each item with an owner, a due date, and whether it blocks signature.
5. **Escalation gate:** track counsel-dependent items separately and keep the matter status at "held" until they clear; never let it move to "ready to sign" with an open gate item.
6. Advance the status through a defined pipeline (intake → review → negotiation → counsel → ready → signed) so the next action is always visible.

## Example

Matter: Acme MSA renewal, owner @jordan, value $80K, target signature 2026-08-15. Documents: MSA v3 (current), Order Form #7, DPA draft. Links: SaaS review verdict = negotiate; escalation packet open on liability cap; renewal-tracker deadline 2026-11-01. Open items: liability cap (counsel, blocks signature), DPA sign-off (@security, due 08-08). Status: counsel (held).

## Pitfalls

- Reviewers working off an old draft because the current version was not marked.
- Open items with no owner or due date, so they never close.
- Marking a matter ready to sign while a counsel item is still open.
- Losing the thread between the review, the escalation, and the renewal entry because they live in separate places.

## Output format

```
MATTER — <counterparty> <type> | owner: @<name> | value | target sign: <date>
Status: intake | review | negotiation | counsel | ready | signed
Documents:
  - <doc> v<n> (<date>) [current?]
Linked artifacts: review · escalation · renewal · amendments
Open items:
  - <item> — owner @<name> — due <date> — blocks signature: <y/n>
Counsel-dependent (held): <items or none>
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
