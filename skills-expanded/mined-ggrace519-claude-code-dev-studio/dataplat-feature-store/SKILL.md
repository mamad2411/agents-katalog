---
name: dataplat-feature-store
description: Feature store / ML data ops specialist. Owns feature definitions, online / offline parity, point-in-time correctness, materialization, and feature serving latency. Auto-invoked when building, debugging, or extending feature pipelines for ML.
---

# Feature Store / ML Data Ops

Training-serving skew silently kills models: offline metrics look fine while
production predictions degrade. Features need one definition, point-in-time
correct training data, and proven parity between the offline and online paths.

## When to reach for this

- Defining new features or standing up a registry (Feast, Tecton, Featureform, native)
- Building training sets — any join between labels and feature history
- Wiring or tuning online serving (Redis, DynamoDB, Cassandra) and materialization jobs
- A model performs well offline but badly in production — skew is the first suspect

## Principles

1. **One definition, two surfaces.** The same feature computation feeds both the
   offline store (warehouse) and the online store. Hand-reimplementing a feature
   in serving code is how skew is born.
2. **Point-in-time joins, always.** Training rows join features *as of the label
   event's timestamp* (as-of join), never the current value — using current
   values is label leakage and inflates offline metrics.
3. **Event time, not processing time.** Feature timestamps record when the fact
   became true, not when the pipeline ran; otherwise backfilled history leaks
   the future.
4. **Freshness SLA per feature group.** Most features tolerate hourly or daily
   materialization; pay the streaming cost only where the SLA demands it, and
   alert when materialization lag exceeds the SLA.
5. **Parity tests in CI.** For a sample of entity keys, the online-store value
   must equal the offline value at the same timestamp; run on every feature
   definition change.
6. **Publish a latency budget.** Each feature group declares a P99 retrieval
   target; the serving path (store choice, batching, caching) is designed
   against it, not discovered after launch.

## New-feature checklist

- [ ] Registered: entity, name, dtype, owner, freshness SLA, description
- [ ] Computation lives in one place referenced by both offline and online paths
- [ ] Timestamp column is event time; verified against a known historical fact
- [ ] Training-set query uses an as-of join (no `latest value` shortcut)
- [ ] Materialization job scheduled; lag alert wired to the freshness SLA
- [ ] Online TTL ≥ materialization interval (no blackout window between refreshes)
- [ ] Parity test added: sampled keys, offline vs online, tolerance for floats
- [ ] Backfill produced history for training without overwriting event times

## Pitfalls

- Training on current feature values instead of as-of values — the classic
  leakage that shows up as an offline/online metric gap
- Entity-key mismatches between stores (string vs int IDs, casing, zero-padding)
  causing silent null features in serving
- Online TTL shorter than the materialization cadence, so features expire and
  serve nulls between refreshes
- Defaults/imputation differing between training (e.g., mean-fill) and serving
  (e.g., zero-fill)
- Backfills that stamp rows with the backfill run time, corrupting every future
  point-in-time join

---
*Related: `dataplat-etl` (the pipelines feeding the offline store),
`dataplat-quality` (contracts on feature source tables), `dataplat-streaming`
(real-time feature ingestion), `dataplat-privacy` (PII in features) · domain
agent: `dataplat-architect` · output/ADR format: `playbook-conventions`*
