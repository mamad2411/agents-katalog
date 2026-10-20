---
name: dataplat-viz
description: Analytics delivery specialist. Owns semantic / metrics layer, dashboards (Looker, Tableau, Superset, Metabase), metric definitions, and self-serve patterns. Auto-invoked when building dashboards, defining metrics, or designing a semantic layer.
---

# Data Platform Visualization & Semantic Layer

A dashboard with three definitions of "revenue" is worse than no dashboard —
it manufactures arguments instead of decisions. Metrics belong in the semantic
layer: defined once, owned by someone, consumed everywhere.

## When to reach for this

- Defining or changing a metric (LookML, dbt Semantic Layer / MetricFlow, Cube)
- Building or reviewing dashboards and self-serve exploration surfaces
- Two reports disagree on the same number — definition drift is the first suspect
- A dashboard is slow, or row-level security needs to apply across BI tools

## Principles

1. **Define once, use everywhere.** Metrics live in the semantic layer, not in
   dashboard SQL. Any metric typed into a chart's custom-SQL box will fork from
   the canonical definition within a quarter.
2. **A metric spec is more than a formula.** Name, grain, numerator/denominator,
   default filters (e.g., excludes test accounts and refunds?), timezone, and
   an owner — most "wrong number" disputes are undocumented filter differences.
3. **Certified vs exploratory tiers.** Certified content is reviewed, owned,
   and labeled; everything else is visibly exploratory. Without the split,
   every screenshot becomes an unofficial source of truth.
4. **Drill paths beat pretty charts.** Every top-line tile should answer "why?"
   in one click — drill to segment, then to row detail. A number that can't be
   decomposed gets re-derived by hand, wrongly.
5. **Performance budget per dashboard.** Set a target load time up front; when
   it's blown, fix with pre-aggregates, extracts, or caching — not by telling
   users to wait.
6. **Row-level security in the semantic layer.** One access model enforced
   below the dashboards; per-dashboard filters as a security mechanism drift
   and leak.

## Where logic belongs

| Logic | Belongs in | Not in |
|---|---|---|
| Cleansing, joins, business entities | dbt marts (`dataplat-etl`) | semantic layer or charts |
| Metric definitions, ratios, time-grain aggregation | semantic layer | per-dashboard SQL |
| Row-level security | semantic layer / warehouse policy | dashboard filters |
| Formatting, labels, conditional color | the BI tool | marts |
| One-off exploration | exploratory tier, clearly labeled | certified dashboards |

## Metric spec checklist

- [ ] Name and plain-language definition (readable by a non-analyst)
- [ ] Grain and aggregation type (additive, semi-additive, ratio)
- [ ] Numerator/denominator and default filters made explicit
- [ ] Source marts referenced via the semantic layer, not raw tables
- [ ] Owner and certification tier assigned
- [ ] Change policy: definition changes are announced, versioned, and dated on
      affected dashboards

## Pitfalls

- Ratio and average metrics re-aggregated wrongly (averaging averages, summing
  ratios) when users change grain — define them as numerator/denominator pairs
  so the layer recomputes correctly
- Semi-additive metrics (balances, inventory) summed over time instead of
  taking period-end or average
- The same metric name pointing at different filters in two dashboards —
  the classic "marketing vs finance revenue" dispute
- Per-dashboard RLS filters that drift from the warehouse access model
- Dead dashboards never decommissioned, so users trust stale numbers; review
  usage and archive on a cadence
- Dashboards querying raw/staging tables, bypassing both the semantic layer and
  quality contracts

---
*Related: `dataplat-sql` (tuning the queries behind slow tiles), `dataplat-etl`
(the marts beneath the semantic layer), `dataplat-quality` (freshness SLAs and
exposures for dashboards) · domain agent: `dataplat-architect` · output/ADR
format: `playbook-conventions`*
