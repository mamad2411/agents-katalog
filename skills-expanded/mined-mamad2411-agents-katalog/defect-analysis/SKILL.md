---
name: defect-analysis
description: Analyze defects systematically — classify per IEEE 1044, cluster by root cause, plot Pareto, derive trends, and feed back to design/test improvements. Use when defect data is plentiful but action is scarce.
source: self
date_added: 2026-05-01
---

# Defect Analysis

Counting bugs is not analysis. Analysis means **classifying**, **clustering**, **trending**, and **acting** so the same defects don't return. This skill applies IEEE 1044 + ODC + Pareto to turn the defect database into a continuous-improvement engine.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Standards | IEEE 1044 (anomaly classification), IBM ODC (Orthogonal Defect Classification), ISO 25010 (quality model) |
| Tracker | Jira / Linear / GitHub Issues with required fields for category, phase-injected, phase-found, root cause |
| Visualization | Grafana / Looker / Metabase: Pareto, trend, cohort, leakage |
| Analytics | Periodic SQL on tracker; quarterly summary; per-release diff |
| Adjacent | RCA (5 whys / fishbone), defect prevention skill |

## When to Use

- Many defects but no improvement loop.
- Releases keep producing similar bugs.
- Audit / compliance evidence (SOC 2, ISO).
- Prioritizing where to invest in tests, design, or process.

## Required Fields per Defect

To enable analysis, capture (don't make optional):

- **Severity** (S1–S4) and **Priority** (P1–P4)
- **Phase found** (unit / component / E2E / staging / canary / prod)
- **Phase injected** (req / design / code / config / data / 3rd-party)
- **Component / area** (orders, checkout, billing)
- **Defect type** (per ODC: function, interface, assignment, timing, algorithm, build/package, documentation)
- **Root cause** (filled at close)
- **Detection mechanism** (test type that found it, or "customer")
- **Time to detect / fix** (derived from timestamps)
- **Fix** (PR link)

CI bot can require these on close.

## Classification Frameworks

### IEEE 1044 (subset)

- **Symptom** — what the user observed
- **Type** — wrong/missing/extra/incorrect
- **Cause** — code, design, requirement, config, data, environment

### ODC (Orthogonal Defect Classification, IBM)

| ODC type | Trigger examples |
| --- | --- |
| Function | feature missing or wrong by spec |
| Interface | API contract mismatch |
| Assignment | wrong value to variable / config |
| Timing | concurrency, sequence, race |
| Algorithm | logic / math wrong |
| Build/Package | environment, deploy, dependency |
| Documentation | docs/runbook drift |

ODC enables **distribution analysis** ("60% of S1s are Timing → invest in concurrency tests").

## Analyses to Run Monthly

1. **Pareto by component** — 80% of defects from 20% of components.
2. **Pareto by ODC type** — focus tests on the dominant type.
3. **Phase-containment matrix** — % defects caught at each phase. Goal: shift left.
4. **Leakage trend** — defects found in prod / total per release.
5. **Aging** — open S1/S2 by age; SLA breaches.
6. **Reopen rate** — % defects reopened (signals weak fixes or testing).
7. **MTTR** by severity.

### SQL sample (Jira → warehouse)

```sql
SELECT component,
       odc_type,
       COUNT(*)                           AS defects,
       COUNT(*) FILTER (WHERE severity IN ('S1','S2'))  AS critical,
       AVG(EXTRACT(EPOCH FROM (resolved_at - created_at))/3600) AS avg_ttr_h
FROM jira_defects
WHERE created_at >= now() - interval '90 days'
GROUP BY 1, 2
ORDER BY defects DESC;
```

## Worked Example

```
Defect analysis — orders-api Q2 2026 (90d)
Total: 412 defects (S1: 6, S2: 41, S3: 244, S4: 121)

Pareto by component:
  refunds       128 (31%)
  cart           96 (23%)
  notifications  61 (15%)   --- top 3 cover 69%

ODC distribution (S1+S2):
  Timing      18 (38%)   ← invest in concurrency + idempotency tests
  Interface   12 (26%)   ← invest in contract tests for refunds API
  Assignment   8 (17%)
  Function     6 (13%)
  Algorithm    3 ( 6%)

Phase containment:
  caught in unit       46%
  component            18%
  E2E staging          14%
  canary                8%
  prod (leakage)       14%   ← target ≤10%; see escaped-defect-analysis

Trend (per release):
  Leakage 18% → 14% → 12% → 14% — flat last release; investigate
```

## Action Loops

For each top finding, produce 1 owned action:

- Top component → assign owner, deeper test design review.
- Top ODC type → invest in matching tests (Timing → concurrency/property tests; Interface → contract tests).
- Phase-containment regression → add gate at the upstream phase.
- High reopen rate → require RCA on close + reviewer.

Track actions in the QA retro register; close the loop next quarter.

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Only counting bugs | Classify and trend; counts ≠ insight |
| ODC fields optional | Bot blocks close when missing |
| Quarterly view only | Monthly cadence; per-release diff |
| Action items vague | One owned action per finding, measurable |
| "Just write more tests" | Write the **right** tests — the ones the dominant ODC type needs |
| Ignoring reopen rate | Symptom of weak fixes / weak tests on the fix |
| Small samples treated as trend | Annotate confidence; require N≥30 |

## Output Format

Above pattern: counts → Pareto → ODC → containment → trend → actions. Render as a one-pager dashboard + monthly Markdown summary.

## References

- IEEE 1044 — Standard Classification for Software Anomalies
- IBM Research — Orthogonal Defect Classification (Chillarege)
- ISO/IEC 25010 — Software product quality
- *Software Reliability Engineering* — Musa
- *Quality Software Project Management* — Futrell et al.
