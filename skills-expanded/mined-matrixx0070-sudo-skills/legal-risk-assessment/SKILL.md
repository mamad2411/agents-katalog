---
name: legal-risk-assessment
version: 1.0.0
description: Size one legal risk by severity and likelihood, place it on a matrix, apply escalation criteria, and assign owned mitigations.
author: matrixx0070
tags: [legal, risk, assessment, matrix, escalation, mitigation]
capabilities: []
---

## When to use
Use this to size a specific legal risk — a contract term, a compliance gap, a potential dispute, a data exposure, an IP conflict — so stakeholders agree on how serious it is and who must act. It turns vague worry into a rated, owned item.

**Not for:** assessing many risks at once (run this per risk), a full contract review (use `legal-review-contract`), or deciding whether an action is lawful in the first place (use `legal-compliance-check`).

## Method
1. **Describe the risk as a scenario.** "If X happens, then Y consequence." One risk per assessment.
2. **Rate severity (1-5).** Weigh financial exposure, regulatory penalty, litigation, reputational and operational harm. State the driver of the score.
3. **Rate likelihood (1-5).** Base it on evidence and precedent, not gut feel. Note the basis.
4. **Plot severity × likelihood** and derive a tier: Low / Medium / High / Critical.
5. **Apply escalation criteria.** *Decision points:* Critical or any severity 5 → immediate counsel + leadership; High → counsel within the week; Medium → owner + tracked; Low → monitor.
6. **Define mitigation.** For each material risk, give an action that lowers severity or likelihood, with owner and date.
7. **Set a review trigger.** The event or date that forces re-assessment.

## Example
Scenario: "If the auto-renewal in the SaaS contract fires unnoticed, we're locked into another 12 months at $180k with no exit." Severity: 4 (financial lock-in, no operational harm). Likelihood: 3 (no calendar reminder exists; renewal is 60 days out). Tier: High → counsel within the week. Mitigation: file a 45-day-prior cancellation reminder and send notice of non-renewal (owner: Procurement, by next Friday). Residual: Low once notice is sent. Review trigger: renewal date, or any renegotiation.

## Pitfalls
- **Scoring on gut feel.** Likelihood without an evidence basis invites endless debate; cite precedent or data.
- **Bundling multiple risks.** One assessment per scenario, or the tier becomes meaningless.
- **Mitigations without an owner or date.** An unowned action is a wish, not a control.
- **No review trigger.** Risk ratings go stale; name the event that forces a re-look.

## Output format
```
Risk scenario: If <X>, then <Y>.
Severity: <1-5> — driver:
Likelihood: <1-5> — basis:
Tier: Low | Medium | High | Critical
Escalation: <who> by <when>
Mitigations: <action> — owner: <name> — by: <date>
Residual risk (post-mitigation):
Review trigger:
```

## Severity × likelihood matrix
Score every risk on two independent axes, then read the tier off the matrix. Anchor each score to a concrete threshold so two reviewers land in the same place.

**Severity scale**

| Score | Label | Financial | Regulatory / legal | Reputational / operational |
|-------|-------|-----------|--------------------|-----------------------------|
| 1 | Negligible | < $10k | None | No external notice; internal only |
| 2 | Minor | $10k–$100k | None | Internal only; no press |
| 3 | Moderate | $100k–$1M | Contained regulatory inquiry | Limited press; recoverable |
| 4 | Major | $1M–$10M | Regulatory penalty; litigation likely | Notable reputational hit |
| 5 | Severe | > $10M | Criminal/regulatory sanction; license loss | Existential; class action |

**Likelihood scale**

| Score | Label | Probability | Basis |
|-------|-------|-------------|-------|
| 1 | Rare | < 5% | No precedent; hypothetical |
| 2 | Unlikely | 5–25% | Conceivable, weak signal |
| 3 | Possible | 25–50% | Plausible; some indicators |
| 4 | Likely | 50–80% | Precedent exists; conditions present |
| 5 | Almost certain | > 80% | Already occurring or inevitable |

**Matrix (rows = severity 5→1, cols = likelihood 1→5)**

| Sev \ Like | 1 Rare | 2 Unlikely | 3 Possible | 4 Likely | 5 Almost certain |
|-----------|--------|-----------|-----------|----------|------------------|
| **5 Severe** | High | High | Critical | Critical | Critical |
| **4 Major** | Medium | High | High | Critical | Critical |
| **3 Moderate** | Low | Medium | Medium | High | High |
| **2 Minor** | Low | Low | Medium | Medium | High |
| **1 Negligible** | Low | Low | Low | Medium | Medium |

Reading rule: high severity **or** a high severity×likelihood product pushes the tier up. Any Severity-5 risk is **at least High**; Sev5 combined with Likelihood 3 or above is **Critical**.

## Escalation tiers

| Tier | Criteria | Action | SLA | Owner |
|------|----------|--------|-----|-------|
| Critical | Sev5×Like3+, or any cell marked Critical | Immediate counsel + leadership notification | Same day | Counsel + risk owner |
| High | High-tier cell; any Severity-5 | Counsel review; logged and tracked | Within the week | Risk owner + counsel |
| Medium | Medium-tier cell | Owner assigned; tracked in register | Monthly review | Risk owner |
| Low | Low-tier cell | Monitor only | Quarterly review | Register maintainer |

**Worked placements**

| Scenario | Severity | Likelihood | Tier |
|----------|----------|-----------|------|
| Auto-renewal lock-in, no reminder | 4 | 3 | High |
| Missing DPA with active PII flow | 5 | 4 | Critical |
| Ambiguous trademark similarity, no complaint | 3 | 2 | Medium |
| Expired insurance COI | 4 | 2 | Medium/High |

## Reference
**Mitigation levers.** Every mitigation should target one axis. To *reduce severity*: liability caps, indemnity carve-outs, insurance, data segregation, staged rollouts. To *reduce likelihood*: process controls, calendar reminders, monitoring/alerting, training, dual sign-off.

**Residual re-scoring.** After a mitigation is in place, re-score both axes and re-read the matrix — the residual tier, not the inherent tier, drives the escalation SLA. Only a mitigation that is actually owned and dated counts toward the residual score; a planned-but-unowned control leaves the inherent score standing.

**Review triggers.** Every rated risk carries a re-assessment trigger: a date (renewal, filing deadline), an event (new complaint, regulation change, incident), or a threshold breach. Without a trigger the rating silently goes stale. When the trigger fires, re-run severity and likelihood from scratch rather than nudging the old numbers.
