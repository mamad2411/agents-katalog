---
name: de-data-quality
version: 1.0.0
description: Define data-quality checks and a monitoring and alerting plan across a pipeline.
author: matrixx0070
tags: [data-engineering, data-quality, monitoring, alerting, observability]
capabilities: []
---

# de-data-quality

## When to use

Use this when you need to guarantee that data flowing through a pipeline is correct and to know — before stakeholders do — when it is not. Covers what to check, where to check it, and how to alert.

**Not for:** writing model-level dbt tests as part of building models (use de-dbt-transform), designing the pipeline itself (use de-pipeline-design), or investigating a specific number's correctness (use data-analyze).

## Method

1. **Map checks to the six dimensions:** completeness (row counts, no missing partitions), uniqueness (no dup keys), validity (types, ranges, enums), consistency (cross-table referential integrity), timeliness (freshness vs SLA), accuracy (reconcile to a trusted total).
2. **Place checks at the right gate:** at ingestion (schema/contract), post-transform (business rules), and pre-consumption (freshness + reconciliation). Decision point: block-on-fail at ingestion (circuit-break bad data); warn-and-alert on downstream anomalies.
3. **Classify each check as blocking or non-blocking.** Blocking checks halt the pipeline and page. Non-blocking checks log a warning and notify. Never block on a soft anomaly-detection signal.
4. **Set thresholds from history, not guesses.** Use rolling baselines for volume/freshness; static rules for hard constraints (a key is unique, always).
5. **Route alerts by severity.** Critical → page/on-call; warning → team channel; info → dashboard only. Every alert names the table, the check, the observed vs expected value, and a runbook link.
6. **Track SLIs over time** (freshness, pass rate, incident count) so quality is measurable, not anecdotal.

## Example

```sql
-- Freshness check (blocking, pre-consumption)
select max(ordered_at) as latest,
       timestampdiff(hour, max(ordered_at), now()) as lag_hours
from marts.fct_orders
having lag_hours > 2;     -- SLA: < 2h; non-empty result = FAIL → page

-- Volume anomaly (non-blocking): today's rows vs 28-day median
-- alert if todays_rows < 0.5 * median OR > 2 * median
```

Reconciliation: nightly, `sum(amount)` in `fct_orders` must equal the source ledger total within 0.1% — a break pages the on-call before the morning dashboards refresh.

## Pitfalls

- Alerting on everything, training the team to ignore alerts (alert fatigue).
- Static thresholds that break on legitimate growth, or none at all.
- Checking only at the end, so bad source data has already contaminated marts.
- Alerts with no context or runbook, so the responder starts every incident from zero.

## Output format

```
Check:     <name> | dimension: <completeness|uniqueness|validity|consistency|timeliness|accuracy>
Table:     <target> | gate: ingest|post-transform|pre-consume
Rule:      <expected> vs <observed>  | threshold: <static|rolling baseline>
Mode:      blocking (halt+page) | non-blocking (warn)
Alert:     severity <critical|warning|info> → <channel> | runbook: <link>
SLI:       track <freshness | pass-rate | MTTR>
```
