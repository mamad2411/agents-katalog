---
name: risk-assessment
description: Identifies, assesses, and plans mitigations for OPERATIONAL risks — system outages, vendor failures, capacity shortfalls, process breakdowns, security incidents, single-point-of-failure dependencies, and execution risk on projects. Make sure to use this skill whenever the user says what could go wrong with [project/system/vendor], assess the operational risks of [initiative], build a risk register, identify single points of failure, evaluate vendor/third-party risk, or analyze the execution risk of a launch/migration/change. Produces a structured risk register with likelihood × impact scoring and concrete mitigation owners. Do NOT use for: legal liability, contractual exposure, regulatory consequence, IP, privacy, employment claims, or litigation risk (use legal:legal-risk-assessment) — that skill handles legal risk and this one handles operational risk. They are intentionally separate by domain.
---

# Risk Assessment (Operational)

Structured identification, scoring, and mitigation planning for operational risks.

## Scope: OPERATIONAL risks only

This skill handles operational exposure: system reliability, vendor/third-party failure, capacity, process and execution risk, security incidents (the operational side, not the legal/regulatory side), single points of failure, dependency risk.

For legal exposure (contract risk, regulatory liability, privacy obligations, IP, litigation, employment claims) → use `legal:legal-risk-assessment`.

The two skills are intentionally separate. Operational risk needs eng/ops/security stakeholders and SRE/incident-response frameworks. Legal risk needs counsel and legal-classification frameworks. Mixing them creates muddled output and unclear ownership.

## Framework

Every operational risk gets classified on two axes:

**Likelihood (probability over a defined window — usually 90 days or 1 year):**
- **5 — Near-certain:** Will happen if no action taken
- **4 — Probable:** More likely than not
- **3 — Possible:** Realistic chance, unclear timing
- **2 — Unlikely:** Would require unusual circumstances
- **1 — Rare:** Theoretical, no recent precedent

**Impact (consequence if it occurs):**
- **5 — Severe:** Multi-day outage, primary revenue loss, significant data loss, irrecoverable customer churn
- **4 — Major:** Hours-long outage of critical system, single-day revenue impact, significant customer escalation
- **3 — Moderate:** Hours of degradation, contained impact, recoverable
- **2 — Minor:** Brief disruption, single-team or single-customer impact
- **1 — Negligible:** Noticed but not impactful

## Risk score = Likelihood × Impact (1–25)

| Score | Action | Owner |
|---|---|---|
| 20–25 | **Critical** — Mitigate before next deploy. Halt deployment if mitigation isn't ready. | Eng/Ops Director |
| 12–19 | **High** — Mitigation plan within 30 days. Weekly status. | Risk owner + manager |
| 6–11 | **Medium** — Quarterly mitigation. Monitor leading indicators. | Risk owner |
| 3–5 | **Low** — Accept and monitor. Quarterly review. | Auto |
| 1–2 | **Negligible** — Document only. | Auto |

## Risk register structure

Every register entry includes:

| Field | Content |
|---|---|
| **ID** | RISK-2026-NNN |
| **Title** | Short noun phrase ("Single primary database with no read replica") |
| **Category** | Infrastructure / Vendor / Process / Security / Capacity / Dependency |
| **Description** | The trigger condition and the failure mode (2-3 sentences) |
| **Likelihood** | 1-5 with rationale (cite evidence — past incidents, leading indicators) |
| **Impact** | 1-5 with rationale (which system, how many customers, what duration) |
| **Risk score** | Likelihood × Impact |
| **Owner** | Named individual (not "the team") |
| **Mitigation status** | Planned / In progress / Implemented / Accepted |
| **Mitigation actions** | Bullet list with target dates |
| **Residual risk** | Score after mitigation (often 4-9 for Highs that get mitigated) |
| **Last reviewed** | Date |
| **Next review** | Date based on score (Highs monthly, Mediums quarterly) |

## Common operational risks (quick-reference for cybersec/infra contexts)

- **No tested backup restoration** → Likelihood 4, Impact 5 = 20 → critical
- **Single primary DB without read replica** → L4 × I5 = 20 → critical
- **Vendor lock-in for critical service with <30 day exit cost estimate** → L3 × I4 = 12 → high
- **Capacity headroom <20% on production traffic** → L4 × I4 = 16 → high
- **Single-point-of-failure on someone's laptop** (deploy keys, undocumented script) → L3 × I5 = 15 → high
- **MFA not enforced on admin access** → L4 × I5 = 20 → critical, also a security finding
- **No on-call rotation for critical service** → L3 × I4 = 12 → high
- **Untested incident response runbook** → L3 × I4 = 12 → high
- **Vendor SOC 2 expired/missing for production data processor** → L2 × I5 = 10 → medium (and triggers a `legal:legal-risk-assessment` for the regulatory angle)

## Mitigation strategy categories

When proposing mitigation, name the strategy:

1. **Avoid** — Don't take the risk (kill the project, refuse the vendor)
2. **Reduce likelihood** — Make failure less likely (add monitoring, redundancy, automated tests)
3. **Reduce impact** — Make failure less painful (backups, failover, blast-radius reduction)
4. **Transfer** — Move risk to insurance, vendor SLA, contractor
5. **Accept** — Document and live with it (only valid for Low/Negligible)

## When to chain to legal-risk-assessment

If the operational risk has legal/regulatory consequences (data breach exposure, SLA penalty, regulatory reporting obligation triggered) — also run `legal:legal-risk-assessment` on the legal aspects. The two assessments together form the complete picture.

## Output

Every assessment produces:
1. Risk register entry (or update) in the structure above
2. Recommended mitigation strategy with owner and dates
3. Leading indicators to monitor (so likelihood changes are detected early)
4. Trigger for re-assessment (what would change the score)
5. Cross-reference to legal risk register if applicable
