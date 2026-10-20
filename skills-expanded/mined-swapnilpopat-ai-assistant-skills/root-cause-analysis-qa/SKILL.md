---
name: root-cause-analysis-qa
description: Perform blameless RCA on a defect or incident — timeline, contributing factors, root causes, lessons, actions — using 5 whys + fishbone + causal trees. Use after Sev-1/2 or recurring defects.
source: self
date_added: 2026-05-01
---

# Root Cause Analysis (QA)

RCA finds the **systemic causes** behind a failure so the same class can be prevented — not "who clicked what". This skill fuses 5 whys, fishbone, and causal trees with a strict blameless ethic.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Methods | 5 whys, Ishikawa fishbone, causal/fault trees, ATA (After-Action Review), ICS-style timeline |
| Format | Blameless postmortem template (Google/PagerDuty) |
| Output | Causal narrative + 1–5 owned actions + dissemination |
| Cadence | Within 5 business days of incident; quarterly aggregate |
| Storage | Repo `/postmortems/<date>-<title>.md`; cross-linked from defect & incident |

## When to Use

- Sev 1 / Sev 2 incident.
- Recurring defect class despite prior fixes.
- Customer-impacting near-miss.
- Audit-required RCA (regulated industries).
- Engineering retro requests deep-dive.

## Method

1. **Build a timeline** from logs, deploys, alerts, on-call notes — minute-precise. Include detection, mitigation, recovery, customer comms.
2. **Reproduce** the failure (or confirm reproduction is impossible and explain).
3. **5 whys** down the most directly-causal chain. Stop when:
   - You hit a systemic factor (process, tooling, design).
   - Or further "why" is speculative.
4. **Fishbone** to enumerate contributing factors across categories: People, Process, Tooling, Environment, Data, External.
5. **Causal tree** — multiple chains often combine; draw them so single-cause illusion doesn't dominate.
6. **Distinguish**: trigger (what set it off), conditions (what made it possible), absent defenses (what should have caught it).
7. **Write the narrative**: clear, blameless, evidence-cited.
8. **Derive actions**: each contributing factor → at most one preventive action; rank by impact × cost.
9. **Disseminate**: send summary to engineering; archive in postmortem index.

## Postmortem Template

```markdown
# Postmortem — <YYYY-MM-DD> — <one-line title>
- Status:           Final
- Author(s):        @name (lead) + reviewers
- Severity:         S1
- Detected by:      <alert / customer / synthetic>
- Customer impact:  <users, requests, revenue>
- Duration:         <DD/MM HH:MM> → <DD/MM HH:MM> (impact); detection at <HH:MM>; mitigation at <HH:MM>

## Summary (≤ 5 lines)
What happened, what users saw, what we did, current state.

## Timeline (UTC)
HH:MM — deploy of v3.13.4 (orders-api) started
HH:MM — error rate begins climbing
HH:MM — alert "ErrorRateHigh" fires (page #98712)
HH:MM — on-call ack; opens incident channel
HH:MM — rollback to v3.13.3 initiated
HH:MM — error rate returns to baseline
HH:MM — incident closed

## Impact
- 11 duplicate refunds, ~€420 over-refunded
- 3 customer tickets; refunded customers contacted
- SLO budget consumed: 0.6% (monthly budget 1%)

## Root cause analysis
Triggers:
  - Deploy of refund retry handler

Contributing factors (fishbone):
  People:      reviewer overlooked retry idempotency in PR #4821
  Process:     no idempotency contract test required for new POSTs
  Tooling:     PR template lacks idempotency checkbox
  Environment: canary too short (5 min) and traffic too low to surface 0.4% rate
  Data:        no shadow query for invariant (refund_count vs. order_count)
  External:    payment processor doesn't reject duplicate refund attempts within window

Absent defenses:
  - No contract test for idempotency
  - No invariant alert
  - Short canary

5 whys (deepest chain):
  Why duplicate refund? — Retry happened after 200 OK timeout
  Why was retry not idempotent? — Idempotency-Key not propagated by retry path
  Why not? — New retry handler bypassed shared client wrapper
  Why allowed? — No lint/test forced shared client usage
  Why not enforced? — Pattern existed but had no codified gate

## Lessons
- Idempotency belongs in the contract layer.
- Canary length must scale with low-rate failure modes.
- Shared infra wrappers must be enforced (lint or arch fitness function).

## Actions (owners, due, measurable)
- [ ] Pact contract: idempotent refund POST              | @sam   2026-05-05  | 100% POSTs covered
- [ ] Shadow query alert (refund vs order count)         | @sre   2026-05-04  | alert active
- [ ] Canary length: min 30 min for billing services     | @sre   2026-05-07  | rollout policy updated
- [ ] Lint rule: force use of `idempotentPost()`         | @plat  2026-05-15  | rule live, codemod merged
- [ ] PR template idempotency checkbox                   | @qa    2026-05-04  | template updated

## Detection / response evaluation
- Time-to-detect: 14 min  (target ≤ 5)  ⚠
- Time-to-mitigate: 28 min (target ≤ 30) ✅
- Comms: status page updated 12 min after detection

## What went well
- Clean rollback path; flag-protected feature unaffected
- Customer comms within 1 hour, refunds processed proactively
```

## Blameless Discipline

- Names appear only as authors, attendees, owners.
- Avoid evaluative language ("careless", "failed to"). Use mechanism language ("the gate did not require", "the alert lacked").
- Counterfactuals are speculation; surface them as actions, not blame.
- Reviewers reject drafts that name individuals as causes.

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Single cause illusion | Use fishbone + causal tree; multiple factors |
| Stopping at "human error" | Push down to absent defenses & systems |
| Vague actions ("be careful") | Owner + due + measurable outcome |
| Blame language | Reviewer enforces blameless edit |
| No follow-up | Quarterly action register review; old postmortems audited |
| Postmortem in private channel | Publish; cross-link to defect & incident |
| Action overload | Cap at 5; pick highest impact × lowest cost |
| Skipping near-misses | Run RCA on customer-visible near-misses too |

## Output Format

The template above; per-quarter aggregate of root-cause categories to spot patterns (links to defect-analysis ODC distribution).

## References

- Google SRE Book — *Postmortem Culture*
- John Allspaw — *Blameless PostMortems and a Just Culture*
- *The Field Guide to Understanding 'Human Error'* — S. Dekker
- PagerDuty Postmortems: <https://postmortems.pagerduty.com/>
- Cynefin & Etsy debriefing facilitation guide
