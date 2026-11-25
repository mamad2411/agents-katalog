---
name: coml-cold-start-interview
version: 1.0.0
description: Interview a new team to capture the commercial-legal standards, playbook positions, risk tolerance, signing authority, and escalation triggers needed before any contract review can run.
author: matrixx0070
tags: [commercial-legal, intake, playbook, onboarding, interview]
capabilities: []
---

## When to use

Use this the first time the commercial-legal skills are set up for an organization, when no playbook exists yet. It gathers the raw material — standard positions, risk tolerance, and who decides what — so every later review measures against the company's own bar, not a generic one.

**Not for:** adjusting an existing playbook (use coml-customize), reviewing a specific contract (coml-review), or organizing an active matter (coml-matter-workspace).

## Method

1. Capture the basics: legal entity name, jurisdiction of incorporation, and preferred governing law and venue.
2. Elicit standard positions for the three contract families using the reference tables as a checklist — NDA term and residuals, SaaS liability cap and data ownership, vendor IP and insurance. Record the preferred and the fallback for each.
3. Probe risk tolerance: how much liability exposure is acceptable, appetite for one-sided terms, and any absolute red lines.
4. Define signing authority tiers: who can sign at what dollar value and which terms always require sign-off.
5. **Escalation gate — establish it now:** confirm who counsel is (internal or outside firm) and the triggers that route to them. If there is no counsel relationship, that gap is itself the first thing to escalate before any deal is signed.
6. Capture the renewal-notice process: who owns the calendar and how reminders are set.
7. Output a playbook stub that coml-customize can refine.

## Example

Interview of a 40-person SaaS company: entity Delaware C-corp, prefers Delaware law. NDA: mutual, 3-year, no residuals. SaaS-as-customer: 12-month cap, customer owns data, 60-day notice acceptable as fallback. Signing authority: founder any value; ops lead up to $25K non-gate terms. Counsel: outside firm, engaged for liability/IP/data terms. Renewal owner: ops lead. Gap found: no formal renewal calendar — flagged to stand up coml-renewal-tracker.

## Pitfalls

- Collecting preferred positions but not fallbacks, so reviewers have nothing to negotiate toward.
- Skipping signing authority, leaving it unclear who can actually agree to what.
- No named counsel or triggers, so escalation has nowhere to go.
- Treating the interview as one-time — capture enough that coml-customize can iterate.

## Output format

```
PLAYBOOK STUB — <company> | <date>
Entity: <name> · jurisdiction · preferred law/venue
Standard positions:
  - NDA: <term / mutuality / residuals — preferred | fallback>
  - SaaS/MSA: <cap / data / renewal — preferred | fallback>
  - Vendor: <IP / insurance / termination — preferred | fallback>
Risk tolerance: <appetite + red lines>
Signing authority: <tier → who / limit>
Counsel + escalation triggers: <who / when>
Renewal process: <owner / reminder cadence>
Gaps to close: <items>
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
