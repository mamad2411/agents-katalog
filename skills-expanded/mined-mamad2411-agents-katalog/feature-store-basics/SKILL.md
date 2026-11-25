---
name: feature-store-basics
description: >
  Design and operate a feature store safely for owned ML systems: train/serve
  parity, point-in-time correctness, entity keys, offline/online stores, access
  control, PII features, and monitoring. Use when Feast/Tecton-like platforms,
  feature views, materialization, or online feature retrieval.
---

# Feature Store Basics

## Scope And Authorization

- **In scope:** Feature platforms and data for ML systems you own.
- **Out of scope:** Pulling features/PII from data lakes without authorization.
- Features may contain sensitive attributes—apply access control and retention.
- Prefer non-prod for schema experiments; materialization can be expensive.
- Pair with `embedding-model-choice` when features are vectors; `code-quality-standards` for pipelines.

## When To Use

- Introducing Feast/Tecton/vertex feature store or similar.
- Debugging train/serve skew.
- Defining entities, feature views, and TTL for online store.
- Point-in-time joins for training datasets.
- Governing who can publish/consume features.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Embedding model selection | `embedding-model-choice` |
| Embedding drift monitors | `embedding-drift-monitoring` |
| Generic data warehouse design | data platform skills |
| Secrets for service creds | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Entity | Stable keys (user_id, driver_id)—not mutable emails alone |
| Offline | Historical correctness with event timestamps |
| Online | Low-latency materialization; TTLs |
| Parity | Same transformation logic train vs serve |
| Time | Point-in-time join prevents leakage |
| Governance | Owners, schemas, PII tags, access |

## Workflow

### 1. Confirm scope and success criteria

1. Models, entities, latency SLO for online retrieval, data domains.
2. Success: PIT-correct training set; online retrieval p99 within SLO; documented owners.

### 2. Inventory current features

1. Ad-hoc SQL in training notebooks vs production services.
2. Duplicated transforms between offline ETL and online services.
3. Sensitive fields (SSN, health, precise location).

### 3. Model entities and feature views

```python
# Conceptual Feast-like sketch
driver = Entity(name="driver_id", join_keys=["driver_id"])

driver_stats = FeatureView(
    name="driver_stats",
    entities=[driver],
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
    ],
    source=source,
    ttl=timedelta(hours=24),
)
```

1. Define event_timestamp and created timestamp semantics.
2. Version feature views on breaking transform changes.
3. Document aggregation windows (1h/24h) explicitly.

### 4. Point-in-time correctness

1. Training retrieval uses as-of timestamps—no future data.
2. Validate with known leakage tests (label time vs feature time).
3. Reject joins that silently use latest features for historical labels.

### 5. Online materialization and serve

1. Materialize schedule aligned to model freshness needs.
2. Online store auth (IAM); network private.
3. Serving API: batch get by entity keys; timeouts; metrics.
4. Train/serve parity tests: same inputs → close enough values.

### 6. Security and privacy

1. Tag PII features; restrict consumers; prefer hashed/tokenized IDs.
2. Audit who reads online features.
3. Retention: expire online keys; lifecycle offline tables.
4. No secrets as “features.”

### 7. Verify and hand off

```bash
# Example checks (tool-specific)
# feast apply / materialize-incremental
# integration test: training row matches online get at timestamp t
```

1. Monitoring: materialization lag, null rates, distribution drift, serve errors.
2. On-call runbook for stale online features.
3. Registry of feature views with owners.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Time | PIT joins | Latest features for past labels |
| Transforms | Shared definitions | Notebook SQL ≠ prod Java |
| Keys | Stable entity ids | Fuzzy name matching as entity |
| PII | Tagged + restricted | Raw SSN as open feature |
| Lag | Monitored materialization | Silent days-old online data |

## Output Checklist

- [ ] Entities and feature views defined with owners
- [ ] Offline PIT correctness validated
- [ ] Online materialization + TTL set
- [ ] Train/serve parity tests
- [ ] Access control and PII tags applied
- [ ] Lag/null/error monitoring
- [ ] Runbook for stale features
- [ ] Residual risk noted

## Rules

- Authorized data only; minimize PII features.
- Prevent label leakage with PIT discipline.
- Prefer shared transforms over duplicated logic.
- Monitor freshness—stale features are silent failures.
- Vectors/embeddings may need embedding skills alongside.
