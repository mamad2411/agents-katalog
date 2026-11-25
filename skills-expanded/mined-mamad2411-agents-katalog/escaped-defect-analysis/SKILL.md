---
name: escaped-defect-analysis
description: Analyze defects that escaped to production — calculate leakage, identify the gate that should have caught them, and feed actions back to tests and process. Use after every prod-detected defect.
source: self
date_added: 2026-05-01
---

# Escaped Defect Analysis (EDA)

Every defect found in prod is a failure of one or more upstream gates. EDA names the gate that should have caught it, asks why it didn't, and produces a specific test or process improvement so the next instance is caught.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Trigger | Any S1/S2 defect found in prod or by customer; sampled S3/S4 |
| Output | EDA record per defect + monthly aggregate |
| Cadence | Per defect (within 5 days); monthly review of patterns |
| Adjacent | Defect analysis (clustering), defect prevention, blameless postmortem |
| Storage | EDA report attached to defect; aggregated in quality dashboard |

## When to Use

- Sev-1/Sev-2 defects post-deploy.
- Customer-reported defect that automated tests should have caught.
- Recurring defect patterns — EDA on each forces a structural fix.
- Compliance / SOX / SOC 2 audit trail.

## Method

1. **Reproduce locally / staging**. Without a clean repro, you don't have a defect; you have a guess.
2. **Identify phase injected** (requirement / design / code / config / data / 3rd-party).
3. **Walk every gate** the change passed through — for each, ask:
   - Was this defect class **in scope** for this gate?
   - Was a relevant test **present**?
   - Did a relevant test **execute**?
   - Did a relevant test **assert** the failing behavior?
4. **Identify the gap**: missing test, missing oracle, wrong env, untested config, dataset gap, flag combination, time/concurrency, locale, scale.
5. **Propose the cheapest reliable prevention** (per defect-prevention skill).
6. **Implement** the test/gate **before closing** the EDA.
7. **Track recurrence** — if same root cause returns, escalate to design fix.

## EDA Record Template

```markdown
# EDA — DEF-7421 — Duplicate refund on retry
- Severity / Priority: S1 / P1
- Detected: 2026-04-30 14:18 UTC by @support (customer ticket #98234)
- Service / version: orders-api v3.13.4
- Phase injected: code (commit 9f1c2 — refund retry)
- Customer impact: 11 duplicate refunds, ~€420 over-refunded; tickets 98234, 98261, 98290
- Repro: documented at <link> (deterministic)

## Gate analysis
| Gate                | In scope? | Present? | Executed? | Asserted? | Outcome |
| --- | :-: | :-: | :-: | :-: | --- |
| Unit                | Y | Partial | Y | N | Tested success path; not retry-after-success |
| Component (Pact)    | Y | N | — | — | No idempotency contract |
| Integration         | Y | N | — | — | No retry simulation |
| E2E                 | Y | N | — | — | Single-shot only |
| Manual exploratory  | Y | N | — | — | Not in last bug-bash |
| Canary              | Y | Y | Y | N | Low traffic; signal didn't surface |
| Monitoring alert    | Y | Y | Y | N | No alert on duplicate refund |

## Why it escaped
- No idempotency contract test for refund POST.
- Retry handler added without negative-path test.
- Canary too short / traffic too low to surface 0.4% duplicate rate.

## Prevention (filed before close)
- [x] Add Pact contract: refund POST must be idempotent on Idempotency-Key
- [x] Add property-based test: any sequence of N retries → exactly 1 effect
- [x] Add monitoring: alert when |refund_count - order_count| in 1h > threshold
- [x] Update PR template: "Idempotency considered for new POSTs?"
- [x] Add to release readiness checklist

## Owner / due
- Tests: @sam by 2026-05-05
- Alert: @sre by 2026-05-04
- Process: @qa-lead by 2026-05-07

## Recurrence check
- Search for similar pattern across services: refunds, cancellations, exports
- 2 candidates flagged → DEF-7430, DEF-7431

## Lessons
- Idempotency belongs in **contract** layer, not unit
- Canary must include a **shadow query** for invariants, not just SLOs
```

## Aggregate Metrics

```sql
-- Leakage rate per release
SELECT release_tag,
       COUNT(*) FILTER (WHERE phase_found = 'prod') AS leaked,
       COUNT(*)                                     AS total,
       ROUND(100.0 * COUNT(*) FILTER (WHERE phase_found = 'prod') / COUNT(*), 1) AS leakage_pct
FROM jira_defects
GROUP BY release_tag
ORDER BY release_tag DESC;
```

Track:

- **Leakage rate** (target ≤ 10%; tier-1 ≤ 5%)
- **Repeat-offender modules** (which keep escaping)
- **Gate where caught vs. where should-have-been-caught** matrix
- **Time-to-detect-in-prod** (MTTD post-deploy)

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Closing the defect without an EDA | Make EDA mandatory for S1/S2 in tracker workflow |
| Generic prevention ("add more tests") | Name the test; commit before closing EDA |
| Blame culture | Blameless EDA; focus on gates and systems |
| EDA only after exec sees the bug | Trigger automatically on prod severity threshold |
| Recurrences accepted as "rare" | Same root cause twice = mandatory design fix |
| EDA quality varies | Use the template; require gate analysis table |
| Aggregates ignored | Monthly leakage trend on the dashboard |

## Output Format

Per defect: the record above attached to the defect ticket.

Monthly aggregate:

```
EDA — April 2026
  Releases: 6
  Defects in prod: 14 (S1: 1, S2: 4, S3: 9)
  Leakage rate: 11% (target 10%)  ⚠
  Top offending modules: refunds (4), notifications (3)
  Top gate gap: contract tests (5), monitoring alerts (3)
  Actions completed: 11 / 12 prevention items closed
  Recurrences: 1 (DEF-7421 family) — escalate to design fix
```

## References

- IEEE 1044 — Anomaly classification
- IBM ODC — Phase containment analysis
- Google SRE Workbook — Postmortem culture
- *Continuous Delivery* — Humble & Farley (deployment pipeline gates)
- Atlassian Incident Handbook
