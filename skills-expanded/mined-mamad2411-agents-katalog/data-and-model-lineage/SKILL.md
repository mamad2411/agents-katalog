---
name: data-and-model-lineage
description: >
  Guides tracking end-to-end lineage from raw data sources through feature
  computation, training runs, and model versions, to enable root-cause
  tracing, impact analysis, and compliance/audit answers. Use when the user
  asks to "trace where a feature/model came from", set up data/model lineage
  tracking, do impact analysis before changing an upstream table, answer an
  audit/compliance question about a model's training data, or debug a bad
  prediction back to its source.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Data And Model Lineage

## Purpose

Every model in production is the end of a long chain: raw data sources feed
transformations, transformations feed feature computations, features feed
training runs, training runs produce model versions, and model versions serve
predictions that drive business decisions. When something goes wrong at any
point — a bad prediction, a compliance question, an upstream schema change —
the operational question is always "what does this actually depend on, and
what depends on it." Data and model lineage makes that chain an explicit,
queryable graph instead of tribal knowledge scattered across Slack threads
and the memories of whoever built the pipeline. This is what makes root-cause
analysis, impact analysis before a risky change, and audit/compliance answers
tractable instead of an archaeology project.

## When to use

- The user wants to set up lineage tracking across a data/ML platform (e.g.
  OpenLineage, Marquez, DataHub, Amundsen, or a cloud-native lineage feature
  in Databricks Unity Catalog / dbt / a warehouse's built-in lineage).
- The user needs to trace a bad prediction or a drift alert back to the
  specific data snapshot, feature definition, and training run that produced
  the currently-serving model (tie-in with
  [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)).
- The user is planning a change to an upstream table/source and wants impact
  analysis — which features, training pipelines, and models depend on it.
- The user needs to answer a compliance/audit question: "what data was this
  model trained on," "who has access to the data that feeds this model,"
  "can we prove this model didn't train on data we didn't have rights to."
- The user wants to wire lineage metadata into feature store or experiment
  tracking systems rather than maintaining it as separate documentation.

## Prerequisites & environment

- A lineage-capable metadata platform or a plan to construct a minimal
  graph: OpenLineage (an open specification with integrations for Airflow,
  Spark, dbt), Marquez (reference OpenLineage backend), DataHub, Amundsen,
  or a cloud-native catalog (Unity Catalog, AWS Glue Data Catalog with
  lineage, Vertex AI Metadata).
- Instrumented pipelines that emit lineage events at each transformation
  step — this usually means integrating the orchestrator (Airflow, dbt,
  Spark) with the lineage platform's event API rather than bolting lineage
  on after the fact.
- Consistent, stable identifiers for datasets, feature views, experiment
  runs, and model versions across all the systems being linked (see
  [feature-store-design](../feature-store-design/SKILL.md),
  [experiment-tracking](../experiment-tracking/SKILL.md), and
  [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)
  for where these identifiers originate).
- Buy-in to instrument lineage emission at pipeline-build time, since
  retrofitting lineage onto years of undocumented pipelines is a
  significant, usually incremental, effort.

## Step-by-step guidance

1. **Model the lineage graph explicitly** before picking a tool: nodes are
   datasets/tables, feature views, training runs, and model versions; edges
   are "derived from" relationships. Sketch the shape for a typical use
   case:
   ```
   raw_transactions_table
        │  (derived from)
        ▼
   cleaned_transactions_table  (dbt model)
        │
        ▼
   driver_stats feature view  (Feast materialization)
        │
        ▼
   training_dataset_run-8841  (point-in-time join output)
        │
        ▼
   experiment_run-8841  (training run, logged params/metrics)
        │
        ▼
   fraud-scorer_v14  (registered model version)
        │
        ▼
   production_predictions_2026-07-28  (serving logs)
   ```
2. **Emit lineage events from each stage's orchestrator**, using an open
   standard where possible so tools interoperate. OpenLineage example event
   shape emitted by an Airflow task on completion:
   ```json
   {
     "eventType": "COMPLETE",
     "job": {"namespace": "fraud-ml", "name": "compute_driver_stats"},
     "run": {"runId": "8841-compute-features"},
     "inputs": [{"namespace": "warehouse", "name": "cleaned_transactions_table"}],
     "outputs": [{"namespace": "feature_store", "name": "driver_stats_v3"}],
     "producer": "airflow-openlineage-provider"
   }
   ```
3. **Propagate identifiers forward, not just names.** Each stage's output
   should carry the specific version/snapshot identifier of everything it
   consumed (e.g. the training dataset build should record the exact
   feature view version and data snapshot ID it read, not just "driver_stats
   as of whenever this ran").
4. **Link experiment tracking and model registry records into the same
   graph** rather than treating them as separate systems: an experiment
   run's logged `data_snapshot` and `git_sha` tags (see
   [experiment-tracking](../experiment-tracking/SKILL.md)) and a registered
   model version's lineage tags (see
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md))
   should resolve to the same node identifiers used in the lineage graph.
5. **Support two query directions**: backward ("what produced this model
   version / this prediction") for root-cause analysis, and forward ("what
   depends on this table / this feature") for impact analysis before a
   risky upstream change.
6. **Run impact analysis before any upstream schema or semantics change** —
   query the lineage graph for all downstream feature views, training
   pipelines, and production models that depend on the table being changed,
   and notify/coordinate with their owners before the change ships.
7. **Retain lineage records at least as long as the models/predictions they
   describe remain relevant to compliance or audit needs** — a lineage
   record for a model that's still influencing live decisions (even an
   older, archived version still consulted for past-decision audits) should
   not be purged on a generic retention timer without checking active
   relevance.
8. **Expose lineage queries to the people who need them** (ML engineers
   during incident response, compliance/legal during audits) via a UI or a
   simple query API — a lineage graph that only the platform team knows how
   to query loses most of its operational value.

## Best practices

- Treat lineage identifiers (dataset snapshot IDs, feature view versions,
  run IDs, model version IDs) as a shared vocabulary across teams and
  systems — inconsistent IDs across the feature store, experiment tracker,
  and model registry silently break the graph's usefulness.
- Instrument lineage emission as part of building a new pipeline stage, not
  as a follow-up task — it is far cheaper to emit lineage events at
  creation time than to reconstruct history later.
- Use an open standard (OpenLineage) over a fully proprietary format where
  feasible, so lineage data isn't locked into one vendor's tool as the
  platform evolves.
- Make lineage queryable both forward and backward — teams tend to only
  build the backward ("where did this come from") direction and then
  struggle when they need impact analysis ("what breaks if I change this")
  before a migration.
- Pair lineage with data/model retention and access-control policy — lineage
  tells you what a model depends on, which is exactly the information needed
  to answer "did this model train on data subject to a deletion request" or
  "does this model depend on data outside our licensed usage."
- Review lineage completeness periodically (spot-check that a recently
  registered model's lineage chain is fully resolvable back to raw source
  data) rather than assuming instrumentation stays correct indefinitely as
  pipelines evolve.

## Common pitfalls

- **Symptom:** A drift alert or a bad-prediction report comes in, and
  tracing it back to the responsible data source and training run takes
  days of manual Slack archaeology because no lineage was captured at
  pipeline-build time.
  **Fix:** Instrument lineage emission into orchestrators from the start of
  a new pipeline's life (Airflow/dbt/Spark integrations with OpenLineage or
  an equivalent), so backward tracing is a graph query, not an
  investigation.

- **Symptom:** A team changes an upstream table's schema (e.g. drops a
  column, changes a type) without realizing three downstream feature views
  and two production models depend on it, causing multiple pipeline
  failures simultaneously.
  **Fix:** Require a forward impact-analysis query against the lineage
  graph before any upstream schema or semantics change to a shared
  table/source, and notify the owners of everything found downstream before
  the change ships.

- **Symptom:** Compliance asks "what data was model X trained on" during an
  audit, and the honest answer is "we're not entirely sure — the training
  script pointed at 'the latest data' rather than a specific pinned
  snapshot," which is not an acceptable audit answer.
  **Fix:** Always pin training runs to immutable, specific data snapshot
  identifiers (not "latest") and record them in both experiment tracking and
  the lineage graph, so the exact training data for any model version is
  retrievable on demand.

- **Symptom:** A well-intentioned data-retention cleanup deletes a "stale"
  raw data snapshot that turns out to still be referenced by the lineage
  chain of a model version that is archived but still consulted for
  historical-decision audits, breaking the ability to answer future audit
  questions about decisions that model made.
  **Fix:** Before deleting any data snapshot or pipeline artifact, query the
  lineage graph for active references (including archived-but-still-audited
  model versions) rather than relying on a generic time-based retention
  rule; treat deletion of anything with unresolved downstream references as
  requiring explicit review, not automatic execution.

## Worked example

Compliance asks the ML platform team to prove what data trained the
currently-deployed `fraud-scorer` model, following a customer data-subject
access request.

1. The team looks up `fraud-scorer` version 14 in the model registry (see
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)),
   which carries a `run_id=run-8841` lineage tag.
2. Following `run-8841` into the experiment tracker (see
   [experiment-tracking](../experiment-tracking/SKILL.md)) surfaces the
   logged `data_snapshot=s3://data-lake/fraud/training/run-8841/` and
   `feature_view_version=driver_stats_v3` tags.
3. Querying the lineage graph backward from `driver_stats_v3` (see
   [feature-store-design](../feature-store-design/SKILL.md)) resolves to its
   source table, `cleaned_transactions_table`, and further back to
   `raw_transactions_table`, with the exact ingestion job run that populated
   it on 2026-07-19.
4. The team confirms the specific customer's records were present in
   `raw_transactions_table` as of that ingestion run, and — since the
   customer has since requested deletion — runs a forward impact-analysis
   query to identify every downstream artifact (feature views, training
   datasets, and model versions) derived from data including that customer's
   records, to plan a compliant remediation (e.g. scheduling a retrain
   excluding the deleted data, per the deletion policy) rather than guessing
   at what's affected.
5. The full chain — raw table → transformation → feature view → training
   dataset → experiment run → model version — is produced as a lineage
   report for the audit, generated directly from the graph rather than
   reconstructed manually.

## Cross-references

- [feature-store-design](../feature-store-design/SKILL.md)
- [experiment-tracking](../experiment-tracking/SKILL.md)
- [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)
- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)
