---
name: feature-store-design
description: >
  Guides designing and operating a feature store (offline + online layers)
  for ML, covering feature definitions, point-in-time-correct training data
  generation, entity keys, and low-latency online serving. Use when the user
  asks to "design a feature store", "avoid feature leakage", set up
  Feast/Tecton/Databricks Feature Store/Vertex AI Feature Store, backfill
  features, or ensure training/serving parity for feature values.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Feature Store Design

## Purpose

Most production ML bugs are not model bugs — they are feature bugs: a
feature computed one way for training and a subtly different way for serving,
or a feature that accidentally uses information from the future relative to
the label it's predicting. A feature store solves this by making feature
definitions a first-class, versioned artifact with two consistent
materializations — an offline store for point-in-time-correct training data
and an online store for low-latency inference — computed from the *same*
feature definition. Getting this right is what prevents training/serving skew
and label leakage, two of the most expensive classes of ML production bugs to
diagnose after the fact.

## When to use

- The user is designing feature definitions, entity keys, or a feature schema
  for a new ML use case.
- The user wants to set up or evaluate a feature store platform (Feast,
  Tecton, Databricks Feature Store, Vertex AI Feature Store, SageMaker
  Feature Store) or a homegrown offline/online split.
- The user needs point-in-time-correct joins for training data ("as-of"
  joins) to avoid label leakage.
- The user is debugging a training/serving skew issue where offline metrics
  don't match online model behavior.
- The user needs to backfill historical feature values for a newly added
  feature.
- The user asks about feature versioning, feature ownership, or feature
  reuse across teams/models.

## Prerequisites & environment

- A feature store platform or the intent to build a minimal one: Feast ≥ 0.30
  (open source, supports point-in-time joins natively), Tecton, Databricks
  Feature Store, or a custom design over a data warehouse (BigQuery,
  Snowflake, Redshift) plus a low-latency KV store (Redis, DynamoDB,
  Bigtable) for online serving.
- A batch/streaming compute layer to materialize features (Spark, Flink,
  dbt, or warehouse-native SQL/scheduled queries).
- Clear entity definitions (e.g. `user_id`, `merchant_id`, `session_id`) that
  features are keyed on.
- Event-time timestamps on source data — point-in-time correctness is
  impossible without a reliable "when did this fact become true" timestamp,
  distinct from "when was this row loaded."
- Access to the training pipeline and serving pipeline codebases, since the
  feature store's value depends on both consuming it identically (see
  [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)).

## Step-by-step guidance

1. **Define entities and feature views explicitly.** An entity is the join
   key (e.g. `driver_id`); a feature view is a named, versioned group of
   features tied to that entity with a defined source and freshness.
   ```python
   # Feast example: feature_repo/driver_features.py
   from feast import Entity, FeatureView, Field, FileSource
   from feast.types import Float32, Int64
   from datetime import timedelta

   driver = Entity(name="driver_id", join_keys=["driver_id"])

   driver_stats_source = FileSource(
       path="s3://feature-lake/driver_stats/",
       timestamp_field="event_timestamp",
       created_timestamp_column="created_timestamp",
   )

   driver_stats_fv = FeatureView(
       name="driver_stats",
       entities=[driver],
       ttl=timedelta(days=3),
       schema=[
           Field(name="trips_last_7d", dtype=Int64),
           Field(name="avg_rating_30d", dtype=Float32),
           Field(name="acceptance_rate_30d", dtype=Float32),
       ],
       source=driver_stats_source,
   )
   ```
2. **Build point-in-time-correct training datasets** by joining the label
   timestamps against feature history "as of" that timestamp — never a naive
   join against the latest feature value:
   ```python
   from feast import FeatureStore

   store = FeatureStore(repo_path="feature_repo/")

   # entity_df has driver_id + event_timestamp = the moment the label occurred
   training_df = store.get_historical_features(
       entity_df=entity_df,
       features=[
           "driver_stats:trips_last_7d",
           "driver_stats:avg_rating_30d",
           "driver_stats:acceptance_rate_30d",
       ],
   ).to_df()
   ```
   Concretely: if a ride's label ("driver accepted", yes/no) was recorded at
   `2026-06-14 09:03:00`, the join must use `avg_rating_30d` as it was
   *computed as of* `2026-06-14 09:03:00` — not the value as of today, which
   would leak information from rides that happened after the label event.
3. **Materialize the online store** for the same feature views so inference
   reads the latest values with low latency:
   ```bash
   feast materialize-incremental $(date -u +%Y-%m-%dT%H:%M:%S)
   ```
4. **Serve features online** using the identical feature view definition
   used in training:
   ```python
   online_features = store.get_online_features(
       features=[
           "driver_stats:trips_last_7d",
           "driver_stats:avg_rating_30d",
           "driver_stats:acceptance_rate_30d",
       ],
       entity_rows=[{"driver_id": 4521}],
   ).to_dict()
   ```
5. **Version feature definitions** alongside a schema/semver similar to model
   versioning (see
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)):
   changing a feature's computation logic (e.g. window from 7d to 14d) should
   bump a feature view version and be tracked so historical training runs
   remain reproducible against the definition they were trained with.
6. **Register lineage** from raw source tables → feature view → training
   dataset → model version, so a drift alert or a bad prediction can be
   traced back to the exact feature definition and source data involved (see
   [data-and-model-lineage](../data-and-model-lineage/SKILL.md)).
7. **Backfill new features carefully**: when adding a feature to an
   existing feature view, run a backfill job over historical source data
   before enabling it for training, and validate the backfilled values
   against a small manually-computed sample before trusting the bulk backfill.
8. **Monitor feature freshness and null rates** in both stores — a stale
   online store (e.g. a materialization job silently failing) causes serving
   to use outdated features while nothing else in the system errors, which
   is a common source of silent degradation (see
   [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)).

## Best practices

- Always derive online-store values and training-store values from the same
  feature view definition — never maintain two separate implementations
  (e.g. a SQL query for training and hand-written application code for
  serving) of the same logical feature.
- Use `event_timestamp` (when the fact became true) strictly separately from
  `created_timestamp`/ingestion time — point-in-time joins must use the
  former.
- Default new feature views to a conservative TTL and document staleness
  tolerance per feature; not all features need sub-second freshness, and
  treating all features as "always fresh" adds unnecessary infra cost and
  failure surface.
- Give every feature an owning team and a description in the feature store's
  metadata/registry so feature reuse doesn't turn into an undocumented,
  duplicated mess across models.
- Prefer wide, reusable feature views over ad hoc per-model feature pipelines
  — this reduces both compute duplication and the number of places skew can
  creep in.
- Write automated tests that assert a feature's value computed via the
  offline path matches the value computed via the online path for a sample
  of entities, on a schedule — this is the single highest-leverage test for
  catching training/serving skew before it reaches production.

## Common pitfalls

- **Symptom:** A fraud model performs excellently offline (AUC 0.95+) but is
  much worse in production — classic label leakage from a feature that
  includes information not actually available at prediction time (e.g. a
  "total lifetime chargebacks" feature computed using all data including
  events after the prediction timestamp).
  **Fix:** Enforce point-in-time joins for every training dataset build (no
  naive `latest value` joins), and add a leakage check that verifies no
  feature's `event_timestamp` is later than the corresponding label's
  timestamp.

- **Symptom:** A model's online predictions differ from what offline batch
  scoring would produce for the same entity at the same time (training/serving
  skew), traced to the online store returning slightly stale values because a
  materialization job has been silently failing for two days.
  **Fix:** Monitor feature freshness explicitly (max age since last
  materialization per feature view) with alerting, not just pipeline
  success/failure status — a "successful" job that ran 0 rows still shows
  green in most schedulers.

- **Symptom:** Two teams independently build near-identical features (e.g.
  `user_avg_order_value_30d` computed two slightly different ways) and models
  trained on each disagree in ways that are hard to debug.
  **Fix:** Maintain a searchable feature registry with ownership and
  definitions before allowing new feature views to be created; require a
  quick check for existing similar features as part of onboarding a new
  feature.

- **Symptom:** A backfill for a newly added feature silently produces nulls
  for a large fraction of historical rows because the backfill job's date
  range didn't cover the full window the feature's rolling aggregation needs
  (e.g. a 90-day rolling feature backfilled only 30 days back).
  **Fix:** Validate backfill completeness with a null-rate check per time
  bucket before enabling the feature for training, and always backfill with
  lookback margin equal to the feature's full aggregation window plus one
  period.

## Worked example

A ride-hailing company builds a feature store for a driver-acceptance model.

1. Entity: `driver_id`. Feature view `driver_stats` includes
   `trips_last_7d`, `avg_rating_30d`, `acceptance_rate_30d`, each computed
   nightly from an event stream with `event_timestamp` set to when the
   underlying trip/rating event actually occurred.
2. For a new label dataset covering rides from June 1–14, 2026, the training
   job builds `entity_df` with one row per ride: `driver_id`,
   `event_timestamp` = the ride's request time, `label` = accepted/declined.
3. `get_historical_features` performs a point-in-time join: for the ride at
   `2026-06-14 09:03:00`, it returns `avg_rating_30d` as computed from
   ratings received strictly before that timestamp — not the driver's
   current rating as of today.
4. The resulting training dataframe trains a gradient-boosted classifier;
   the run and its resolved feature view versions are logged (see
   [experiment-tracking](../experiment-tracking/SKILL.md)).
5. In production, the same `driver_stats` feature view is materialized to a
   Redis-backed online store every 15 minutes. At inference time, the
   serving layer calls `get_online_features` for the incoming
   `driver_id`, retrieving the latest materialized values — the identical
   feature definitions used in training, just read from the online store
   instead of the offline store.
6. Three weeks later, a freshness monitor alerts that `driver_stats`
   materialization has been failing for six hours due to a schema change
   upstream; on-call fixes the pipeline and backfills the missed window
   before the online store's staleness affects live predictions materially.

## Cross-references

- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)
- [data-and-model-lineage](../data-and-model-lineage/SKILL.md)
- [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)
- [experiment-tracking](../experiment-tracking/SKILL.md)
