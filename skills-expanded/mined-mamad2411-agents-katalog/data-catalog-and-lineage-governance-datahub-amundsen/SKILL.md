---
name: data-catalog-and-lineage-governance-datahub-amundsen
description: >
  Guides deploying and operating enterprise data catalog and governance
  tooling — DataHub or Amundsen — for discovering, tagging, classifying,
  and owning datasets, features, and models across an organization,
  including deprecation workflows that must check downstream consumers
  before deletion. Use when the user asks to "set up a data catalog", "make
  datasets/models searchable and discoverable", "tag PII/sensitive data",
  assign data ownership, install or configure DataHub or Amundsen, write an
  ingestion recipe, or safely deprecate/delete an old dataset or model
  artifact without breaking a consumer.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Data Catalog And Lineage Governance (DataHub / Amundsen)

## Purpose

[data-and-model-lineage](../data-and-model-lineage/SKILL.md) covers
building the lineage *graph* — which node derives from which — for
root-cause and impact analysis. This skill covers the broader enterprise
governance layer on top of that graph: a searchable **catalog** (DataHub or
Amundsen) where every dataset, feature table, and model has an owner, a
description, classification tags (PII, confidential, public), a glossary
term, and a documented deprecation status, so that "who owns this," "is
this safe to use," and "is anything still depending on this" are answerable
by search rather than by asking around. The catalog and the lineage graph
are complementary — DataHub in particular models lineage as part of its
metadata graph — but this skill's focus is the governance surface:
ownership, discoverability, classification, and the deprecation/deletion
workflow that has to check the lineage graph before removing anything,
rather than the graph-construction mechanics themselves.

## When to use

- Standing up DataHub or Amundsen as an organization-wide data/ML catalog,
  or evaluating which fits the organization's stack.
- Writing or debugging an ingestion recipe/connector that pulls metadata
  from a source system (warehouse, dbt, MLflow, Feast, S3) into the
  catalog.
- Setting ownership, tags, glossary terms, or domains on datasets, feature
  tables, or registered models so they're governed and discoverable rather
  than undocumented.
- Setting up or enforcing PII/sensitive-data classification tags as part of
  a compliance program.
- **Deciding whether it's safe to deprecate or delete an "old" dataset,
  feature table, or model artifact** — this must go through impact
  analysis against the catalog's lineage view first, not be based on file
  age or a naming convention alone.
- Auditing catalog freshness (stale ingestion, orphaned entities with no
  owner) as part of a data governance review.

## Prerequisites & environment

- **DataHub**: a running GMS (metadata service) backend with Elasticsearch
  (search index), Kafka (metadata change event bus), and a storage backend
  (MySQL/Postgres or Cassandra) — deployable via the `datahub` CLI's
  `docker quickstart` for evaluation or the official Helm charts for
  production. **Amundsen**: separate metadata, search, and frontend
  services, typically backed by Neo4j or Atlas for the metadata graph and
  Elasticsearch for search.
- The `acryl-datahub` Python CLI/SDK (for DataHub) or Amundsen's
  `databuilder` library, for writing and running ingestion recipes.
- Read access (credentials scoped to metadata only, not data content where
  avoidable) to every source system to be cataloged: data warehouse system
  tables, dbt manifest/catalog JSON, MLflow tracking server API, Feast
  registry, object storage bucket listings.
- An identifier (URN in DataHub's model) scheme agreed upon *before* mass
  ingestion — inconsistent naming across sources is the leading cause of
  duplicate or orphaned catalog entities.
- For enforcement (not just documentation) of classification policies,
  integration with an access-control or policy engine — DataHub's own
  policy framework, or an external OPA-based check — since catalog tags
  alone are metadata, not access enforcement.

## Step-by-step guidance

1. **Choose and deploy the catalog platform.** DataHub's push-based
   ingestion model (metadata change events over Kafka) suits environments
   wanting near-real-time catalog updates and rich ML-specific entity types
   (`MLModel`, `MLModelGroup`, `MLFeatureTable`) out of the box; Amundsen's
   simpler pull-based batch ingestion (via `databuilder` extractors) suits
   teams wanting a lighter-weight search-first catalog without the Kafka
   dependency. Deploy DataHub for evaluation with:
   ```bash
   pip install acryl-datahub
   datahub docker quickstart
   ```
   For production, use the DataHub Helm chart with externally-managed
   Kafka/Elasticsearch/MySQL rather than the quickstart's bundled
   containers.

2. **Write ingestion recipes per source system**, defining what metadata
   gets pulled and how often — a DataHub recipe for an MLflow model
   registry and a dbt project:
   ```yaml
   # mlflow_ingestion.yaml
   source:
     type: mlflow
     config:
       tracking_uri: "https://mlflow.internal"
   sink:
     type: datahub-rest
     config:
       server: "https://datahub-gms.internal:8080"
   ```
   ```yaml
   # dbt_ingestion.yaml
   source:
     type: dbt
     config:
       manifest_path: "./target/manifest.json"
       catalog_path: "./target/catalog.json"
       target_platform: snowflake
   sink:
     type: datahub-rest
     config:
       server: "https://datahub-gms.internal:8080"
   ```
   ```bash
   datahub ingest -c mlflow_ingestion.yaml
   datahub ingest -c dbt_ingestion.yaml
   ```

3. **Model ML-specific entities explicitly**, not just generic tables —
   DataHub's ML entity model (`MLFeatureTable`, `MLModel`, `MLModelGroup`,
   `MLFeature`) lets a registered model's catalog entry link directly to
   the feature tables and training run it depends on, tying together with
   the lineage graph from
   [data-and-model-lineage](../data-and-model-lineage/SKILL.md):
   ```python
   from datahub.emitter.rest_emitter import DatahubRestEmitter
   from datahub.metadata.schema_classes import MLModelPropertiesClass, MLModelLineageInfoClass

   emitter = DatahubRestEmitter("https://datahub-gms.internal:8080")
   model_urn = "urn:li:mlModel:(urn:li:dataPlatform:mlflow,fraud-scorer,PROD)"
   props = MLModelPropertiesClass(
       description="Fraud transaction scoring model, gradient-boosted trees",
       version="v14",
       trainingMetrics=[{"name": "auc", "value": "0.94"}],
   )
   # emit as a metadata change proposal against model_urn
   ```

4. **Set ownership, tags, and glossary terms** so every cataloged entity
   answers "who owns this" and "what is this" without asking around:
   ```bash
   datahub put --urn "urn:li:dataset:(urn:li:dataPlatform:snowflake,fraud.transactions_clean,PROD)" \
     --aspect ownership \
     --json '{"owners": [{"owner": "urn:li:corpGroup:fraud-team", "type": "DATAOWNER"}]}'

   datahub put --urn "urn:li:dataset:(urn:li:dataPlatform:snowflake,fraud.transactions_clean,PROD)" \
     --aspect globalTags \
     --json '{"tags": [{"tag": "urn:li:tag:PII"}, {"tag": "urn:li:tag:Tier1"}]}'
   ```
   Enforce a minimum-metadata policy (every dataset must have an owner and
   at least one classification tag) as part of the ingestion pipeline or a
   scheduled audit, rather than treating tagging as optional best-effort
   documentation.

5. **Classify sensitive data explicitly and treat the tag as
   policy-relevant, not just descriptive.** A `PII` tag in the catalog is
   metadata only — it does nothing on its own to restrict access. Pair it
   with an actual access-control or policy-engine check (DataHub's native
   policy framework, or an external OPA/Gatekeeper-based check on
   pipelines/services that read tagged datasets) so classification
   actually gates behavior:
   ```json
   {
     "policyType": "METADATA",
     "resources": {"filter": {"criteria": [{"field": "TAG", "value": "urn:li:tag:PII"}]}},
     "privileges": ["VIEW_DATASET_DATA"],
     "actors": {"groups": ["urn:li:corpGroup:fraud-team", "urn:li:corpGroup:data-governance"]}
   }
   ```

6. **Schedule ingestion to run continuously**, not as a one-time import —
   run recipes via Airflow, a cron job, or DataHub's own ingestion
   scheduler UI so the catalog reflects the current state of source
   systems, not a snapshot from initial setup:
   ```yaml
   # Airflow DAG snippet scheduling the recipes from step 2
   ingest_mlflow = BashOperator(task_id="ingest_mlflow", bash_command="datahub ingest -c mlflow_ingestion.yaml")
   ingest_dbt = BashOperator(task_id="ingest_dbt", bash_command="datahub ingest -c dbt_ingestion.yaml")
   ```

7. **Run impact analysis before deprecating or deleting anything**,
   using the catalog's lineage/dependency view to enumerate every
   downstream consumer, and mark the entity `Deprecated` with a
   grace-period date before actual deletion:
   ```bash
   # Query DataHub for downstream consumers of a dataset before deletion
   datahub get --urn "urn:li:dataset:(urn:li:dataPlatform:s3,ml-artifacts/fraud-scorer/v11,PROD)" --aspect upstreamLineage
   ```
   ```python
   # Mark deprecated with a grace period rather than deleting immediately
   from datahub.metadata.schema_classes import DeprecationClass
   deprecation = DeprecationClass(
       deprecated=True,
       note="Superseded by v14; scheduled for deletion 2026-09-01 pending consumer migration.",
       decommissionTime=1767225600000,  # epoch ms
   )
   ```

## Best practices

- **Never delete a dataset or model artifact solely because it looks
  "old" by name or timestamp** — a version that looks stale (`v11` when
  `v14` is current) may still be the active rollback target for a deployed
  model, referenced by a scheduled batch job, or held for a
  compliance-mandated retention period. Query the catalog's
  lineage/dependency view for downstream consumers first, every time,
  before deletion — this is the single highest-consequence mistake this
  skill exists to prevent.
- Treat classification tags (PII, confidential) as inputs to an actual
  policy/access-control decision, not documentation — a tag nobody
  enforces gives a false sense of governance.
- Require an owner on every cataloged entity as an ingestion or CI-time
  check, not a best-effort convention — an orphaned dataset with no owner
  is one nobody will notice going stale or one nobody can approve a change
  to.
- Keep ingestion recipes scheduled and monitored for failure — a catalog
  fed by a broken ingestion job silently drifts out of sync with reality,
  and stale catalog data is worse than no catalog for trust in the tool.
- Agree on a stable identifier/URN scheme before mass-ingesting from
  multiple sources — reconciling duplicate entities for the same logical
  dataset discovered under two different names after the fact is far more
  work than establishing the convention up front.
- Use the deprecation workflow (mark deprecated with a grace period and
  documented replacement, notify owners of downstream consumers, then
  delete after the grace period) as the default path for removing
  anything, never a direct delete.

## Common pitfalls

- **Symptom:** An "old" model artifact or dataset version is deleted to
  free up storage, and a production model deployment or scheduled batch
  job that was still silently pointing at it starts failing (or, worse,
  serving from a fallback/cached copy with no one aware the real source
  is gone).
  **Warning:** This is exactly the dangerous action this skill's impact
  analysis step exists to prevent — a deployed model's rollback target
  (see
  [production-model-rollback-procedure](../production-model-rollback-procedure/SKILL.md))
  or an infrequently-run batch job can both depend on an artifact that
  looks unused by recent-activity metrics alone.
  **Fix:** Always run the catalog's downstream-lineage query (step 7)
  before deleting anything, mark entities `Deprecated` with a grace period
  first, and require an explicit sign-off from every listed owner of a
  downstream consumer before the actual deletion proceeds.

- **Symptom:** The catalog shows a dataset as actively used with a recent
  timestamp, but the ingestion job that populates it has actually been
  failing silently for weeks, and the catalog is serving stale metadata
  that nobody has corrected.
  **Fix:** Monitor ingestion job success/failure explicitly (alert on a
  scheduled recipe run failing, not just on the catalog UI looking
  populated), and surface a "metadata last refreshed" timestamp
  prominently in the catalog entity view so staleness is visible to users,
  not just to whoever owns the ingestion pipeline.

- **Symptom:** The same logical dataset appears as two or three separate
  entities in the catalog (e.g. ingested once via a warehouse connector and
  again via a dbt connector with a slightly different name), fragmenting
  ownership, tags, and lineage across duplicates.
  **Fix:** Standardize the URN/identifier scheme across all ingestion
  sources before onboarding new connectors — for DataHub this typically
  means aligning `platform` and `name` fields consistently — and run a
  deduplication pass on existing entities rather than allowing duplicates
  to accumulate silently.

- **Symptom:** A dataset is tagged `PII` in the catalog, but a downstream
  ML pipeline reads it unrestricted anyway, because the tag was applied for
  documentation purposes with no actual access-control policy attached.
  **Fix:** Treat this as a real governance gap, not a catalog bug — wire
  the classification tag into an enforced policy (DataHub's native policy
  engine, or an external check on pipelines reading tagged sources) so
  `PII` actually restricts read access to authorized groups instead of
  only appearing in search results.

- **Symptom:** After a large-scale onboarding of source systems, the
  catalog fills with hundreds of entities that have no assigned owner,
  and nobody can say who to ask about a specific dataset months later.
  **Fix:** Enforce ownership assignment as a required step of the
  ingestion or onboarding process (a CI check against the ingestion recipe
  or a scheduled audit query for entities with an empty `ownership`
  aspect), rather than treating owner assignment as an optional follow-up
  that competes with other priorities and never happens.

## Worked example

**Scenario:** A platform team onboards their MLflow model registry and a
Snowflake warehouse (via dbt) into DataHub, tags sensitive tables, and
needs to safely retire an old model artifact version.

Ingestion (scheduled daily via Airflow, from step 2/6):
```yaml
# snowflake_dbt_ingestion.yaml
source:
  type: dbt
  config:
    manifest_path: "s3://dbt-artifacts/latest/manifest.json"
    catalog_path: "s3://dbt-artifacts/latest/catalog.json"
    target_platform: snowflake
sink: {type: datahub-rest, config: {server: "https://datahub-gms.internal:8080"}}
```

Tagging the raw transactions table as PII, owned by the fraud team:
```bash
datahub put --urn "urn:li:dataset:(urn:li:dataPlatform:snowflake,fraud.raw_transactions,PROD)" \
  --aspect globalTags --json '{"tags": [{"tag": "urn:li:tag:PII"}]}'
datahub put --urn "urn:li:dataset:(urn:li:dataPlatform:snowflake,fraud.raw_transactions,PROD)" \
  --aspect ownership --json '{"owners": [{"owner": "urn:li:corpGroup:fraud-team", "type": "DATAOWNER"}]}'
```

Retiring `fraud-scorer` model version `v11` (superseded by `v14`):
```bash
# 1. Impact analysis first — who/what still depends on v11?
datahub get --urn "urn:li:mlModel:(urn:li:dataPlatform:mlflow,fraud-scorer-v11,PROD)" --aspect upstreamLineage
# Result: no active serving deployment references v11, but the
# production-model-rollback-procedure runbook lists v11 as the last
# known-good rollback target for v12's incident two months ago.
```
Given that finding, the artifact is marked deprecated with a grace period
rather than deleted immediately:
```python
deprecation = DeprecationClass(
    deprecated=True,
    note="Superseded by v14. Retained as rollback reference per incident INC-2026-0512; delete after 2026-10-01 once v14 has one full quarter of stable production history.",
    decommissionTime=1759276800000,
)
```
This keeps the artifact available for the rollback procedure's
schema-compatibility check for one more quarter instead of freeing storage
immediately at the cost of removing a legitimate incident-response option.

## Cross-references

- [data-and-model-lineage](../data-and-model-lineage/SKILL.md) — the lineage-graph construction and root-cause/impact-analysis concepts this skill's catalog layers governance (ownership, classification, deprecation workflow) on top of.
- [feature-store-design](../feature-store-design/SKILL.md) — feature definitions that should be cataloged as `MLFeatureTable`/`MLFeature` entities alongside the datasets and models covered here.
- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md) — the registry versioning scheme whose entries this skill catalogs and governs.
- [production-model-rollback-procedure](../production-model-rollback-procedure/SKILL.md) — why an "old" model version may still be a required rollback target, directly relevant to the deprecation/deletion warning above.
- [security-compliance-mapping-soc2-iso-pci-nist](../../../standards-and-compliance-frameworks/skills/security-compliance-mapping-soc2-iso-pci-nist/SKILL.md) — the compliance frameworks that typically require the ownership/classification/audit trail this catalog layer provides evidence for.
