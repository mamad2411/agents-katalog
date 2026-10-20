---
name: quality-dashboard
description: Build a quality dashboard that combines DORA, defect leakage, flake rate, coverage, performance, and security signals — a single page that drives action, not vanity. Use to give leaders and teams the same source of truth.
source: self
date_added: 2026-05-01
---

# Quality Dashboard

A quality dashboard exists to **drive decisions**: invest where, ship or not, intervene now or later. Vanity metrics (lines of code, test count) are forbidden; every panel maps to an action threshold.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Source data | Jira/Linear, GitHub, CI test runs (JUnit XML), Allure, k6 cloud, Sentry, Datadog/New Relic, OTel via Tempo/Jaeger |
| Pipeline | DBT models on warehouse (BigQuery / Snowflake / Redshift) |
| Visualization | Grafana 11, Looker, Metabase, Backstage SRE plugin |
| DORA tooling | LinearB, Sleuth, DX, in-house DBT models |
| Audience | Eng leadership (top page), team (drill-down per service) |
| Cadence | Real-time + weekly emailed summary |

## When to Use

- Multiple teams, no shared truth.
- Leadership relies on anecdote.
- Quality regressions surface late.
- Compliance evidence (SOC 2, ISO) needs a single source.

## Recommended Panels (with action thresholds)

### Top — Service-level scoreboard

| Metric | Target | Alert if |
| --- | --- | --- |
| Defect leakage % (prod / total) | ≤ 10% | > 15% |
| Open S1 / S2 | 0 / ≤ 2 | any S1; > 4 S2 |
| Change-failure rate (DORA) | ≤ 15% | > 25% |
| MTTR for S1 (DORA) | ≤ 1h | > 4h |
| Deployment frequency (DORA) | ≥ daily | < weekly |
| Lead time for change (DORA) | ≤ 1 day | > 1 week |

### Mid — Test signal

| Metric | Target | Alert if |
| --- | --- | --- |
| Flake rate (PR runs) | ≤ 1% | > 2% sustained |
| Suite duration p95 (PR) | ≤ 10 min | > 15 min |
| Coverage line / branch | floor 80 / 75 | drop > 2 pts |
| Mutation score (critical libs) | ≥ 80% | < 70% |
| Quarantined tests (count, max age) | ≤ 5 / ≤ 7d | any > 7d |

### Mid — Production health

| Metric | Target | Alert if |
| --- | --- | --- |
| Error rate (per service) | ≤ SLO | > SLO sustained |
| Latency p99 (per endpoint) | ≤ SLO | > SLO sustained |
| Incident count (Sev1/2) | trending ↓ | > 2 / month |
| Customer-reported bugs | trending ↓ | > prior month +20% |

### Bottom — Security & compliance

| Metric | Target | Alert if |
| --- | --- | --- |
| Open Critical/High vulns | 0 / 0 | any |
| Days since last DAST run | ≤ 7 | > 14 |
| % services with current threat model | 100% | < 95% |
| WCAG critical/serious axe violations | 0 | any (per surface) |

## Design Principles

1. **One page** for the org top-level. Drill-downs per team/service.
2. **Numbers + threshold + trend arrow + sparkline** — not just a number.
3. **Color discipline**: green within target, amber within tolerance, red over threshold + > 7 days.
4. **Every panel links to source** (a query, a test run, a Sentry issue).
5. **Owner per panel**; "no owner" is not allowed.
6. **No vanity** (LOC, test counts, story points) — only metrics that drive action.
7. **Short refresh windows** — yesterday's data hides today's regression.
8. **Annotated**: deploys and incidents marked on time series.

## Data Model (DBT excerpt)

```sql
-- mart_defect_leakage.sql
SELECT release_tag,
       COUNT(*) FILTER (WHERE phase_found = 'prod')                AS leaked,
       COUNT(*)                                                    AS total,
       SAFE_DIVIDE(COUNT(*) FILTER (WHERE phase_found = 'prod'), COUNT(*)) AS leakage_rate
FROM {{ ref('stg_defects') }}
GROUP BY release_tag
```

## Worked Example (top page)

```
Quality — orders-api  (period: rolling 28d)
  Leakage:    11%   ⚠ (above 10% target)
  S1 open:    0     ✅
  CFR:        12%   ✅
  MTTR S1:    42m   ✅
  Deploys/wk: 18    ✅
  Lead time:  6h    ✅

  Flake:      1.4%  ⚠
  Suite p95:  9m32s ✅
  Coverage:   86 / 78  ✅
  Mutation:   83% (billing) ✅
  Quarantine: 4 tests; oldest 6d ✅

  Error:      0.32% (SLO 0.5%) ✅
  p99:        416ms (SLO 600) ✅
  Sev1 28d:   0 ✅
  Customer:   12 → 9 ↓

  Security: 0 / 0 / DAST 4d / TM 100% ✅
  a11y: 0 / 0 ✅
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Counting tests, LOC, PRs | Drop vanity; show outcomes |
| Pretty dashboards no one reads | Wire alerts; share weekly TLDR |
| Numbers without thresholds | Every metric has target + alert level |
| Stale data | Refresh < 24h; freshness panel |
| One-size-fits-all | Top page for execs; service drill-down for teams |
| Drill-downs broken | Make panel-to-source links a CI check |
| No annotations | Mark deploys/incidents on time series |
| Owner: "the team" | Single owner per panel |

## Output Format

A single screenshotable page (above) plus a weekly summary email:

```
Quality TL;DR — week of 2026-04-28
  Reds:    flake rate 2.1% (action: quarantine/fix top 3)
  Ambers:  leakage 12% (driver: refunds idempotency — EDA #7421)
  Greens:  DORA all in elite/high; SLO compliance 100%
  Notable: 3 EDA actions closed; 1 carried
```

## References

- DORA — *State of DevOps* metrics
- Google SRE — *Practical Alerting from Time-Series Data*
- T. Wilkie — RED method
- B. Gregg — USE method
- *Accelerate* — Forsgren/Humble/Kim
- DX, LinearB, Sleuth blog series on engineering metrics
