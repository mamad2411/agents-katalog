---
name: litig-portfolio-status
version: 1.0.0
description: Produce a portfolio-wide status across all active matters covering at-risk deadlines, next actions, resourcing, and escalations.
author: matrixx0070
tags: [litigation, portfolio, deadlines, resourcing, escalation]
capabilities: []
---

## When to use
Use this when you need a single view across every active matter — for a weekly case-team stand-up, a partner check-in, or when you are triaging where attention and staffing must go. It surfaces deadlines at risk, the next concrete action per matter, and anything that needs to be escalated now. Reach for it whenever the question is "across everything, what is on fire?"

**Not for:** deep single-matter work (use litig-claim-chart or litig-oc-status) or firm configuration (use litig-customize).

## Method
1. Enumerate every active matter with caption, court, phase, and lead attorney.
2. Pull the next three deadlines per matter and flag any within your risk window (default: 14 days) or already at risk of being missed.
3. State one next action per matter with an owner and date — no matter should have a blank next step.
4. Assess resourcing: which matters are under-staffed relative to upcoming load.
5. **Decision point:** if two hard deadlines collide for the same person, decide whether to reassign, seek an extension, or bring in support — and record which.
6. **Decision point:** if a deadline is genuinely at risk of being missed, escalate immediately rather than at the next scheduled review.
7. ATTORNEY-ESCALATION gate: route the deadline-risk list and any extension or reassignment decisions to the supervising/responsible attorney for review and sign-off.

## Example
> Smith v. Acme (N.D. Cal., discovery): next deadline expert disclosures 7/18 (7 days — AT RISK, expert not retained). Next action: retain expert, K. Lee, by 7/14. ESCALATE. Resourcing: Lee double-booked with Doe trial prep — reassign Doe research to associate.

## Pitfalls
- **Deadlines without owners.** Every at-risk date needs a named person, or it will be missed.
- **Averaging away the outlier.** One matter about to blow a deadline matters more than five that are calm.
- **Stale calendars.** Reconcile against the docket and calendaring system before every rollup; orders reset dates.
- **Silent resource conflicts.** Surface collisions early; they compound as trial dates approach.

## Output format
```
PORTFOLIO STATUS — as of <date>
| Matter | Court/Phase | Lead | Next Deadline (days) | Risk | Next Action (owner/date) |
AT-RISK / ESCALATIONS: <matter | issue | ask>
RESOURCING: <person | conflict | resolution>
```

## Reference
Deadline risk turns on the operative scheduling order (Fed. R. Civ. P. 16(b)), which controls discovery cutoffs, expert disclosures (Rule 26(a)(2), typically 90 days before trial absent a different order), dispositive-motion dates, and pretrial dates. Modifying a scheduling order requires "good cause" and the judge's consent (Rule 16(b)(4)) — a high bar, so treat set dates as firm. Always calendar from the order itself, not defaults; local rules, standing orders, and individual judges' practices vary. General guidance, not legal advice.
