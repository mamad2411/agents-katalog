---
name: test-metrics-framework
description: Define a balanced set of test metrics — outcome, signal, and effort — anchored to GQM and ISO 25023. Use when building or auditing a metrics program for QA.
source: self
date_added: 2026-05-01
---

# Test Metrics Framework

Most metrics programs collect what's easy and ignore what matters. This skill defines a small, balanced set anchored to **Goals → Questions → Metrics** so each number drives a decision.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Method | Goal-Question-Metric (GQM) — Basili; OKRs upstream |
| Standards | ISO/IEC 25023 (measurement of system quality), DORA, SPACE framework |
| Storage | Warehouse + DBT models; surfaced via quality dashboard |
| Cadence | Real-time alerts; weekly TLDR; quarterly trend |

## When to Use

- Standing up a QA metrics program.
- Replacing a vanity-metric scorecard.
- Aligning teams on what "quality" means.
- Compliance evidence (ISO 25010/25023, SOC 2).

## Three Metric Categories (balanced)

| Category | Question it answers | Examples |
| --- | --- | --- |
| **Outcome** | Did the user / business benefit? | Defect leakage, customer-reported issues, MTTR, change-failure rate, SLO compliance |
| **Signal** | How sharp is our quality signal? | Test effectiveness (DDP, mutation), coverage floor, flake rate, suite duration |
| **Effort** | What did it cost? | Test maintenance %, CI minutes, perf-test cost, manual testing hours |

Imbalance is a red flag: outcome-only hides flaky tools; signal-only hides escapes; effort-only encourages cheap-but-blind suites.

## GQM Worksheet

For each goal, derive questions and the smallest set of metrics that answer them.

```
Goal:      Reduce production defects without slowing releases
Questions:
  Q1 — Are escapes decreasing?
  Q2 — Is the test signal getting sharper?
  Q3 — Are we still shipping at our deploy frequency?
Metrics:
  Q1 → leakage_rate (per release, 28d trailing)
  Q2 → mutation_score on critical libs; DDP at unit/integ; flake_rate
  Q3 → DORA: deploy_frequency, lead_time, change_failure_rate, MTTR
Targets:
  leakage ≤ 10%; mutation_score ≥ 80% billing; flake ≤ 1%; DORA elite/high
```

## Recommended Core Set (start here)

### Outcome (DORA + escape)

- Deployment frequency
- Lead time for change
- Change-failure rate
- MTTR (Sev 1/2)
- Defect leakage rate
- Customer-reported issues / week

### Signal (test effectiveness)

- DDP per phase
- Mutation score on critical modules
- Coverage line / branch (floor)
- Flake rate (PR runs)
- Suite duration p95
- Quarantine count + max age

### Effort (cost & sustainability)

- Test maintenance % of capacity
- CI minutes per PR
- Manual testing hours per release
- Perf testing $ per release
- Tooling licenses cost (FinOps tag)

## Anti-Metrics (don't track as KPI)

- Number of test cases / lines of test code
- Number of bugs filed
- Story points / velocity
- Hours spent testing
- "% automation" without context

These either drive perverse incentives or lack signal.

## Targets vs. Floors

- **Targets** for outcome metrics (leakage ≤ 10%).
- **Floors** for signal metrics (coverage ≥ 80%, mutation ≥ 80%) — going *above* doesn't earn credit; going below alerts.
- **Budgets** for effort (maintenance ≤ 20% capacity).

## Reporting Cadence

- **Real-time**: alert on threshold breach (e.g., flake > 2% sustained).
- **Weekly TLDR**: 5-bullet summary, deltas vs. last week.
- **Per release**: leakage, DORA snapshot, EDA roll-up.
- **Quarterly**: trend, action review, GQM refresh.

## Worked Example (TLDR)

```
QA Metrics — week 2026-W18
Outcome:
  Deployments: 27 (4.5/day) ✅
  Lead time:   6h ✅
  CFR:         12% ✅
  MTTR S1:     38m ✅
  Leakage:     11% ⚠ (target 10%)
  Customer issues: 9 (-3 vs. last) ✅

Signal:
  DDP unit:    74% ✅
  Mutation (billing): 82% ✅
  Flake:       1.4% ⚠
  Suite p95:   9m32s ✅

Effort:
  Maintenance: 17% capacity ✅
  CI mins/PR:  18 ✅
  Manual hrs/rel: 6 ✅

Themes: 1 leakage above target (refunds idempotency) — EDA #7421
Asks:   investment for refunds contract tests (≤ 1 sprint)
```

## CI / Warehouse Sketch

```sql
-- weekly outcome snapshot
SELECT date_trunc('week', d.detected_at) AS wk,
       AVG(CASE WHEN d.phase_found='prod' THEN 1 ELSE 0 END) AS leakage_rate,
       SUM(CASE WHEN d.severity IN ('S1','S2') AND d.phase_found='prod' THEN 1 ELSE 0 END) AS critical_escapes
FROM   defects d
WHERE  d.detected_at >= now() - interval '90 days'
GROUP  BY 1 ORDER BY 1;
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Vanity metrics dominate | Apply GQM; drop metrics with no decision |
| Only signal, no outcome | Add DORA + leakage |
| Only outcome, no effort | Add maintenance % so unsustainable wins are visible |
| Targets without owners | Each metric has owner + on-call for breach |
| Over-collecting | Start with ≤ 12 metrics; add only when a question demands |
| Quarterly only | Weekly cadence keeps it actionable |
| No baseline / definition drift | Document each metric's SQL/source/owner |

## Output Format

A repo `docs/qa/metrics.md` listing each metric (definition, source, owner, target/floor/budget) plus the dashboard URL. Weekly TLDR template above.

## References

- V. Basili — *The Goal Question Metric Approach*
- DORA — *State of DevOps* metrics
- SPACE framework — Forsgren, Storey, Maddila, Zimmermann
- ISO/IEC 25023 — Measurement of system quality
- *Accelerate* — Forsgren/Humble/Kim
- Microsoft DX engineering metrics blog series
