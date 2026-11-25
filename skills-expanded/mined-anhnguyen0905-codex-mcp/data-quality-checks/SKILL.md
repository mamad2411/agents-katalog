---
name: data-quality-checks
description: Design and review data quality checks, validation rules and data tests for pipelines, ETL/ELT jobs and warehouse tables — completeness, uniqueness, validity and range checks, cross-source consistency, referential integrity, freshness and timeliness SLAs, distribution drift; row-count and sum reconciliation between source and destination, duplicate detection keys, null vs missing vs zero, timestamp ordering and timezone bugs, negative and impossible values, quarantine bad rows vs fail the pipeline, reporting what was checked and what was NOT.
---

# Data Quality Checks (assertions, reconciliation, honest reporting)

## The seven check families, as assertions

Every useful check is a predicate plus a threshold, evaluable automatically against a table:

```
Completeness   assert count(*) where required_col is null = 0
               assert count(distinct load_date) over window = expected_days  (partitions present)
Uniqueness     assert count(*) = count(distinct <business_key>)              (the declared grain)
Validity/range assert age between 0 and 120; status in (...); amount >= 0; format/length rules
Consistency    assert abs(sum(a.rev) - sum(b.rev)) / sum(b.rev) <= tol       (source vs source)
Referential    assert count(child left join parent where parent.id is null) = 0   (no orphans)
Timeliness     assert max(event_ts) >= now() - <SLA interval>                (freshness)
Drift          assert abs(mean_today - mean_baseline) <= k * stddev_baseline
               assert null_rate_today <= null_rate_baseline * (1 + tol)
```

Each assertion needs a grain, a severity (warn vs fail) and an owner. An unowned failing check gets
muted, which is worse than having no check at all.

## Reconciliation, source to destination

Row counts alone prove nothing — dedup, filtering and late arrivals legitimately change them.
Reconcile counts *and* sums per partition, every term measured rather than assumed:

```
source_rows - filtered_rows - deduped_rows = destination_rows
sum(source.amount) over the window = sum(dest.amount) ± rounding tolerance
per-key spot check: sample N business keys, compare field by field
```

Reconcile a closed window, never the currently-loading partition, and state the tolerance with its
cause (float rounding, FX conversion, timezone edge) instead of picking whatever makes it pass.

## Grain and duplicate keys

Use the business key that defines the grain, not the surrogate key — surrogates are unique by
construction and prove nothing. Typical real keys: `(event_id)`, `(user_id, event_ts, event_type)`,
`(order_id, line_no)`. Test near-duplicates too: same natural key with different surrogate ids (double
ingestion), same payload at different timestamps (retry storms). Document the resolution rule — keep
first, keep last by ingestion time, keep highest version — because `distinct` picks one silently.

## Null vs missing vs zero

```
NULL      value unknown / not captured   → excluded from AVG; must never become 0
MISSING   the row does not exist         → a completeness problem, invisible to column checks
ZERO      a measured value equal to zero → a real observation
EMPTY ''  usually an upstream bug posing as a value → test separately from NULL
```

Assert on both axes: column null rates *and* expected row presence per day and per entity. Never
`coalesce(x, 0)` on a metric before validation — that converts unknown into a measurement. Sentinels
(`-1`, `9999`, `'1970-01-01'`, `'N/A'`, `'unknown'`) are nulls in disguise: enumerate and test them.

## Time, and impossible values

Assert causal ordering (`created_at <= updated_at`, `start <= end`, `event_ts <= ingested_at`) and flag
future-dated events beyond a small clock-skew allowance. Store and compare in UTC with the offset
preserved. Classic bugs: a naive local timestamp compared against UTC, shifting rows across day
boundaries and breaking daily counts; DST duplicate or missing hours; timezone applied at query time in
one report and at load time in another. Assert one day-boundary definition across all aggregates.

Domain-impossible values are usually joins or units, not typing: negative quantities, prices or
durations; percentages outside 0-100; conversions exceeding sessions; end before start; children older
than parents; counts above a known population. Asserting `>= 0` on a never-negative column catches unit
errors, sign flips and fanned-out joins earlier than any dashboard will.

## Quarantine vs fail — and reporting

```
FAIL the run     the defect makes output untrustworthy or unfixable downstream: grain violated,
                 reconciliation outside tolerance, unexpected schema change, source empty.
QUARANTINE rows  defects are row-local and the rest is usable: write rejects WITH the failed rule,
                 raw payload and timestamp; emit reject count and rate; alert above a threshold.
```

Quarantine without a monitored reject rate and a replay path is silent data loss. Never drop bad rows
inline unrecorded, and never let a partial load overwrite a good partition — stage, validate, publish
atomically. Then report honestly: a report listing only passes manufactures false confidence. Per run,
publish the rules executed with thresholds and outcomes, rows checked and quarantined, and explicitly
the **unchecked surface** — columns with no assertions, tables with no freshness SLA, dimensions never
reconciled, checks skipped because a dependency was missing. Distinguish "passed" from "not evaluated";
a skipped check rendered green is the most expensive failure mode here.

## Failure modes

- Uniqueness asserted on the surrogate key, so real duplicates pass.
- Reconciling row counts only, so value corruption passes.
- Tolerances widened until the check stops alerting, with no record of why.
- `coalesce` before validation; sentinels treated as data.
- Reconciling the currently-loading partition and chasing phantom mismatches.
- Drift baselines that include the incident, normalising the bad state.
- Muted alerts with no owner; no quarantine replay, so rejects are never recovered.

## Reviewer checklist

- [ ] All seven families considered; gaps named deliberately, not silently omitted
- [ ] Every check is an executable assertion with grain, threshold, severity and owner
- [ ] Uniqueness asserted on the business key, not a surrogate id
- [ ] Reconciliation covers counts and sums per closed partition, tolerance justified
- [ ] Null / missing / zero / empty / sentinel handled distinctly; no pre-validation coalesce
- [ ] Timestamp ordering asserted; comparisons in UTC with one day-boundary definition
- [ ] Domain bounds asserted for impossible and negative values
- [ ] Quarantine records the failed rule and payload; reject rate monitored; replay path exists
- [ ] Fail-vs-quarantine stated per rule; publish is atomic after validation
- [ ] Report separates passed / failed / not evaluated and lists the unchecked surface

## Provenance

Standard data-engineering and data-observability practice (assertion-based testing, source-to-target
reconciliation, freshness SLAs, drift monitoring, quarantine patterns). The seven-family taxonomy and
the fail-vs-quarantine rule as stated here are **derived, unverified** working conventions, not a
citable standard, and the predicates above are illustrative pseudo-SQL. Every threshold, tolerance, SLA
interval, drift multiplier and reject-rate limit must be replaced with the project's own measured
values before being treated as a target.
