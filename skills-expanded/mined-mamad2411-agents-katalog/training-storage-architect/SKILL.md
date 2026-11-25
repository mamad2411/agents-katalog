---
name: training-storage-architect
description: >-
  Architect secure, reproducible training and evaluation storage on Kubernetes,
  including lakehouse zones, Iceberg/Delta/Hudi selection, MinIO or S3 access
  controls, snapshot retention, immutable materialized-input manifests, and
  dataset-to-checkpoint lineage. Use for data lakes, table or file formats,
  medallion zones, time travel, eval isolation, byte-reproducible training
  inputs, Iceberg catalogs, Spark, Trino, or storage-design workshops.
---

# Training Storage Architect

## Purpose
Design the storage substrate that makes "which exact bytes trained this checkpoint?" answerable a year later. A lakehouse = cloud object storage + an open table format supplying ACID, schema evolution, and time travel + a catalog — warehouse-grade management on data-lake economics, which is the right shape for multi-TB versioned corpora feeding GPU jobs on a managed Kubernetes cluster. The deliverables are the zone layout, the table-format decision with rationale, the versioning/lineage scheme binding dataset snapshots to training runs, and the K8s/MinIO deployment plan. Reproducibility is the load-bearing requirement everything else serves. (Guarantees on top of this substrate — SLOs, contracts — route to the sibling `dataset-qos-slo-designer` and `data-contract-author` skills.)

## Core model to hold in your head

### Zones for research data (medallion, adapted)
| Zone | Contents | Rules |
|---|---|---|
| Landing (optional) | As-received drops from crawlers/vendors/streams | Decouples ingestion from processing; short retention |
| Raw (bronze) | Source data as-is (JSON/WARC/audio/images), foldered by source/table | No transformation; no tables needed on top; retain long (reprocessing, audit, license disputes); archive to cold tier post-processing |
| Cleansed (silver) | Validated, deduplicated, open-table-format data; level 1: 1:1 with raw post-quality-checks; level 2: integrated across sources by domain | Convert to the chosen table format here; valid and invalid data both kept — stewards triage invalid back to source; EDA and ad hoc SQL happen here |
| Curated (gold) | Training-ready corpora arranged per use (mixes, tokenized shards, filtered subsets) | Retain all historical versions; this is what training jobs pin |
| **Feature/training zone** (research addition) | Materialized training artifacts: tokenized/packed shards, embeddings, webdataset tars derived from curated snapshots | Every artifact set has an immutable manifest with object paths, content hashes, source snapshot, transform/image digest, loader version, ordering, and seed; regenerable, so retention can be shorter |
| **Eval zone** (research addition) | Frozen benchmark and eval sets | Physically separated prefix/bucket + distinct access policy; immutable after freeze; contamination gate between curated and eval is a publish-time check |
| Archive / Logs / Ad hoc | Cold copies; system logs (lifecycle-deleted); researcher scratch (write access only here) | Scratch is explicitly non-governed — exploration must stay cheap |

### Table format selection (Iceberg vs Delta vs Hudi)
All three give ACID on object storage, record-level update/delete, schema evolution, and time travel — the lakehouse baseline. Differentiate on the criteria that matter for training workloads:

| Criterion | Iceberg | Delta Lake | Hudi |
|---|---|---|---|
| Schema evolution | Full (add/drop/rename without rewrite) | Full + enforcement (reject nonconforming writes) | Full + enforcement |
| Partition evolution | **Unique**: repartition without rewriting data — valuable as corpora grow 10× | No (rewrite) | Clustering to adjust layout as data evolves |
| Time travel | Snapshot IDs + timestamps; snapshot-pinning is the reproducibility primitive | Versions + timestamps, audit log | Commit timeline; incremental queries from a commit |
| File formats under it | Parquet, ORC, Avro (only format supporting all three) | Parquet | Parquet, ORC |
| Incremental processing | Append-only incremental reads | Change data feed | **Strongest**: record-level indexes, upserts/deletes as change streams; CoW (read-fast) vs MoR (write-fast) tables |
| Engine/ecosystem | Spark, Trino, Flink, Dremio, Snowflake; REST catalog spec; broadly vendor-neutral | Spark-first (Databricks origin), Presto/Trino read | Spark/Flink-first, streaming-lake heritage |
| Catalog story | Iceberg catalog (REST/Hive/Glue/Nessie) points to metadata files | Transaction log in-table + external metastore | .hoodie metadata + metastore |

Decision rule for a research division on K8s/MinIO: **Iceberg by default** — partition evolution, tri-file-format support, vendor-neutral REST catalog, and first-class Trino/Spark support fit batch-heavy training pipelines and an open-standard posture. Choose **Hudi** where the workload is genuinely streaming/upsert-heavy (continuous feedback ingestion with record-level corrections); choose **Delta** when the org is committed to a Databricks-centric stack. Record the decision with the criteria table filled in for the org's actual workloads; don't mix formats within a zone without a stated reason.

File format beneath the table format is a separate, smaller decision: Parquet (columnar, default for curated analytics-and-training reads), ORC (columnar alternative), Avro (row-oriented; supports full schema evolution including column modification, so suited to landing/ingest streams). Parquet/ORC only support adding columns at the end — another reason schema changes route through the table format's evolution machinery, not raw file edits.

### Versioning and lineage-to-checkpoint (the reproducibility contract)
1. **Dataset version** = contract semver (human-meaningful) + table snapshot ID (logical table state), not a byte-exact training input by itself. A training config pins both: `dataset://curation/instr-tuning@2.1.0` and `snapshot=8412370493812`.
2. **Materialized-input manifest** pins the bytes actually consumed: ordered object paths and content hashes, source snapshot, transformation code revision, container image digest, tokenizer/dataloader version, shuffle/order policy, and random seed. Every training/eval run records the dataset/version/snapshot plus this manifest digest in the experiment tracker and lineage graph.
3. **Snapshot retention is an SLO**: time travel only reproduces runs while snapshots live; set retention (e.g., 12 months of snapshot history on curated; forever on frozen eval) deliberately and put it in the contract — vacuum/compaction jobs that expire snapshots are silently deleting reproducibility.
4. **Serving is immutable and append-only**: consumers never see update-in-place; corrections arrive as new snapshots/versions. Bitemporality (event time + processing time) on curated tables lets "as-of" questions survive backfills.
5. **Eval isolation**: eval snapshots are frozen at creation; the contamination scan runs before an eval snapshot is published; any breach is repaired by a new eval version, never by editing in place.

### Stakeholder design questionnaire (adapted from lakehouse practice)
Run in workshops; each answer maps to a design decision:

| Category | Ask | Drives |
|---|---|---|
| Existing system | What stores corpora today (buckets? NFS? laptops)? Top pain: findability, speed, reproducibility? | Which pains the zone/catalog design must visibly fix |
| Sources | Per collection pipeline: modality, batch or streaming, incremental capability, daily volume, license terms | Ingestion tooling; landing zone need; raw retention per license |
| Workloads | Pretraining bulk reads? Fine-tune mixes? Online eval? Streaming feedback? Concurrent jobs per day? | Table format choice; CoW vs MoR; throughput targets to GPU nodes |
| Users & agents | Personas (researchers, pipelines, ADP agents); concurrency; SQL vs dataloader access; self-service needs | Query engines (Trino for SQL, Spark for jobs); access paths; catalog surface |
| Data volumes | Historical volume to migrate; YoY growth; daily incremental | Capacity plan; erasure-coding vs replication in MinIO; partition strategy |
| Quality | Known issue classes? Business rules documented? Profiled sources? | Where cleansed-zone gates live; invalid-data handling |
| Sensitive data | PII in corpora (incidental web PII, annotator IDs)? Compliance constraints on raw storage? Joins on masked fields needed? | pii_attributes tagging, masking/anonymization step placement, per-zone access policy |
| Strategy | Approved tooling? Multi-cloud/on-prem posture? External data sharing planned? | Cloud-native vs cloud-agnostic (K8s + MinIO + Iceberg is the agnostic answer); sharing tech |

### Metadata and governance hooks at the storage layer
- **Metastore vs catalog**: the metastore physically stores metadata; the catalog is the access mechanism over it. Deploy one catalog surface over all zones so users and agents get a unified view — technical metadata (schemas, files, snapshots) auto-derived; business metadata (meaning, owners) added via contracts and the discovery layer.
- **pii_attributes tagging**: automate detection of sensitive attributes at metadata-ingestion time (alert on new PII-like columns), tag them (`pii_attributes`, sensitivity class), and drive masking + role-based access from tags, not from tribal knowledge. Lineage over tags answers "every table/report/model touching cust-identifier-class fields" — including which checkpoints trained on data containing them.
- **Role-based governance incl. AI assets**: treat models, features, and eval artifacts as governed assets with owners and access policy, same as tables; audit access logs for who reads PII-tagged attributes and prune standing access.

### K8s / MinIO / S3 deployment notes
- **Object store**: MinIO (or the cloud's S3) via its operator; erasure-coded pools; distinct buckets or prefixes per zone with per-zone lifecycle policies. Object-store IAM, bucket/prefix policies, and short-lived scoped credentials are the hard access boundary and must prevent direct catalog bypass. Catalog tags may drive policy generation and discovery filtering, but never replace storage enforcement.
- **Catalog service**: Iceberg REST catalog (or Nessie for git-like catalog branching of experimental table states) as a K8s deployment; back it with a small HA Postgres. This is a tier-1 service: if the catalog is down, the platform is down — HA and backups accordingly.
- **Compute**: Spark on K8s (operator) for curation jobs; Trino for interactive SQL over all zones; both read the same Iceberg tables — one copy of data, many engines.
- **Training data path**: GPU nodes read shards straight from the object store; budget aggregate read throughput against training-node fan-out (the Th SLO from the sibling QoS skill); consider node-local NVMe cache for hot shards; keep the feature zone's materialized shards in dataloader-native layouts (webdataset/tfrecord) generated from — and stamped with — curated snapshots.
- **Ops**: compaction and snapshot-expiry as scheduled jobs with retention SLOs encoded (never default settings); storage metrics (per-zone growth, small-file counts, snapshot counts) exported to the platform's Prometheus.

## Workflow
1. **Run the questionnaire** with producers, training consumers, and platform ops; write down volumes, workloads, and license/PII constraints.
2. **Draw the zone map** for this org (which optional zones exist, retention + access policy per zone, contamination gate placement).
3. **Select the table format** via the criteria table against the actual workload mix; record an ADR.
4. **Design the versioning scheme**: pinning convention, snapshot-retention SLOs, run-metadata emission, lineage events to the catalog.
5. **Specify the deployment**: operators, catalog HA, engines, throughput budget, lifecycle jobs — as manifests/Helm values lists, not prose.
6. **Validate with a golden-path test**: ingest → cleanse → curate snapshot → materialize and hash training shards → train from the pinned manifest → reproduce the exact ordered input bytes with the pinned image/transform/loader a week later → trace checkpoint back through lineage. The design passes when this runs unattended.

Reproducibility failure modes to test for explicitly in step 6:
- Snapshot expired by a default vacuum job → pinned read fails (retention SLO violated).
- Compaction rewrote table files while preserving the logical snapshot; the materialized-input manifest must still resolve its immutable objects and hashes.
- A backfill changed history → "as-of" query via bitemporal columns still returns the original view.
- Feature-zone shards regenerated from a *newer* curated snapshot while carrying an old stamp → lineage stamp must be write-once.
- Eval set edited in place instead of versioned → the immutability policy must make this impossible, not just discouraged.

## Output spec
Deliver: (a) zone map with per-zone retention/access/format rules; (b) table-format ADR with the filled criteria table; (c) versioning & lineage spec (pinning format, retention SLOs, event schema); (d) deployment plan (components, HA notes, throughput budget); (e) completed questionnaire with each answer's design consequence; (f) the golden-path test script description as acceptance criteria.

## Guardrails
- Never let snapshot expiry/vacuum defaults ship — reproducibility retention is an explicit, contracted decision.
- Eval data never shares a writable prefix with training data; freezes are new-version-only, no in-place edits.
- Raw zone is append-only and untransformed; "we cleaned it in place to save space" destroys audit and reprocessing — push back.
- One table format per zone unless a workload-based exception is documented; format sprawl multiplies engine and ops cost.
- Don't size from aspiration: capacity and throughput plans cite measured volumes and the questionnaire's growth numbers.
- The storage layer serves the catalog and contracts above it — no dataset lands in curated without an owner and at least discovery metadata (route to the sibling skills).

## Suggested effort
High — questionnaire workshops, format ADR, and deployment design are days of work each; the golden-path reproducibility test is non-negotiable before declaring the design done.
