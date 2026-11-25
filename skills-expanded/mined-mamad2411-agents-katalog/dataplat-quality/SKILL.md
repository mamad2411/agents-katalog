---
name: dataplat-quality
description: Data quality and contracts specialist. Owns data contracts, expectation testing (Great Expectations, dbt tests, Soda), lineage, freshness SLAs, and incident response for bad data. Auto-invoked when adding or tightening quality rules, or when a downstream consumer reports bad data.
---

# Data Platform Quality & Contracts

Silent data corruption is the most expensive failure mode in analytics — by the
time a consumer notices, the bad numbers have already driven decisions. Every
mart that feeds a decision needs a contract, a freshness SLA, and a human owner.

## When to reach for this

- A downstream consumer reports wrong or stale numbers
- Adding or tightening dbt tests, Great Expectations suites, or Soda checks
- Defining a contract between a producer team and its consumers
- A schema change is proposed and the blast radius is unknown

## Principles

1. **Contracts at domain boundaries, not every table.** Contract the tables
   that feed decisions, ML, or other teams; testing everything equally buries
   the signal.
2. **Severity tiers decide pipeline behavior.** Critical checks (`error`) block
   the run; advisory checks (`warn`) page nobody but trend on a dashboard. A
   suite that is 100% warn protects nothing.
3. **Test at the source of truth.** Uniqueness, not-null, and referential
   integrity belong at the staging layer — by the marts, corruption has already
   propagated and the failing test points at the wrong place.
4. **Freshness is about the data, not the table.** Assert on the max event
   timestamp against the SLA, not on "table was written recently" — a pipeline
   that loads zero new rows still updates the table.
5. **Lineage before change.** No schema change ships without an impact radius
   from lineage (dbt exposures, OpenLineage, catalog) and notice to affected
   consumers.
6. **Runbook every alert.** An alert without an owner and a response plan is
   noise; noise trains people to ignore the alert that matters.

## Baseline check tiers

| Tier | Checks | Severity | Where |
|---|---|---|---|
| Structural | unique key, not-null on keys, accepted values, referential | error (block) | staging |
| Freshness | max event timestamp within SLA per contracted table | error on 2× SLA, warn on 1× | marts |
| Volume | row count vs trailing window (flag swings beyond expected band) | warn, error on zero rows | staging + marts |
| Distribution | null-rate, distinct-count, numeric-range drift | warn | marts |
| Reconciliation | totals vs source system (counts, sums) | error beyond tolerance | marts |

## Contract spec checklist

- [ ] Columns: name, type, nullability, semantics (units, timezone, enum values)
- [ ] Grain stated explicitly ("one row per order per day")
- [ ] Freshness SLA and delivery schedule
- [ ] Named producer owner and consumer list
- [ ] Change policy: notice period, deprecation path for breaking changes
- [ ] Enforcement wired: tests in CI/pipeline mapped to each clause

## Pitfalls

- Tests only on marts, so failures fire far from the defect and triage starts
  at the wrong layer
- Freshness checks on load time instead of event time — stale-source incidents
  sail through green
- Volume checks with static thresholds that false-alarm every Monday and
  holiday (compare against same-day-of-week history)
- Schema "additive" changes that still break `SELECT *` consumers and BI extracts
- Bad-data incidents fixed in place with no backfill of the already-served
  wrong numbers, and no post-incident test added

---
*Related: `dataplat-etl` (the pipelines under contract), `dataplat-sql`
(diagnostic queries), `dataplat-viz` (exposures and metric consumers),
`dataplat-privacy` (classification tags carried in contracts) · domain agent:
`dataplat-architect` · output/ADR format: `playbook-conventions`*
