---
name: build-data-pipeline
description: Design and implement transactional lakehouse pipelines (Iceberg v3/Delta 4.4), enforce ODCS v3.2.0 data contracts, execute Write-Audit-Publish (WAP) on isolated snapshot branches, route malformed records to DLQ with circuit breaker wired to contract SLA fields, enforce S3 prefix hashing, implement Iceberg REST protocol (scan planning, ETag, Idempotency-Key, credential vending), native table encryption (KMS), and OpenLineage explicit lineage. Use when building or maintaining reliable, contract-governed lakehouse data pipelines.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, query_db, read_database, run_tests]
---

# Build Data Pipeline

Use this skill when building or maintaining transactional lakehouse infrastructure: ingestion pipelines, table formats, schema contracts, Write-Audit-Publish (WAP) validation, dead-letter quarantine (DLQ), and orchestration. For one-off exploratory queries, use `analyze-data` instead.

## When to Use

- implementing transactional lakehouse pipelines with Apache Iceberg v3 (metadata-only restructuring, Variant type) or Delta Lake 4.4 UniForm
- enforcing Open Data Contract Standard (ODCS v3.2.0) at producer boundaries before ingestion
- staging writes to isolated snapshot branches (`wap_audit_<run_id>`) for atomic Write-Audit-Publish (WAP)
- auditing branch data in-process via DuckDB zero-copy Arrow memory before publishing to `main`
- routing poisoned or non-conforming records into Dead-Letter Queue (DLQ) quarantine with circuit breaker **wired to contract SLA fields**
- enforcing deterministic upsert `MERGE INTO` with composite SHA-256 cryptographic natural keys
- configuring S3 object storage prefix hashing (`write.object-storage.enabled = true`) to prevent 503 throttling
- executing automated table maintenance: 256MB bin-pack compaction, 7-day snapshot expiration, 72h vacuum
- implementing Iceberg REST Catalog protocol: scan planning, ETag-based freshness validation, Idempotency-Key commits, credential vending
- mandating native table encryption (KMS) for all Iceberg and Delta Lake tables
- emitting OpenLineage explicit lineage facets for end-to-end pipeline traceability

## Core Rules

- **Read-Only Sources**: treat all source inputs as read-only; never mutate upstream source files or CDC logs.
- **ODCS v3.2.0 Contract Verification**: validate raw payloads against version-controlled ODCS v3.2.0 schemas at producer boundaries before ingestion; reject uncontracted schema drift.
- **Modern Lakehouse Table Formats**:
  - standardize on **Apache Iceberg v3** (1.11+/1.12 implementation line) with metadata-only restructuring (never data rewrites for schema/partition evolution), Puffin RoaringBitmap Deletion Vectors (DVs), and integer `spec-id` partition evolution; avoid legacy position deletes; treat the unratified Iceberg v4 spec strictly as roadmap.
  - support **Delta Lake 4.4 UniForm** for universal Iceberg metadata compatibility and Liquid Clustering.
  - **Variant as Canonical Semi-Structured Path**: adopt `VARIANT` type for schemaless JSON payloads, eliminating `string` blob anti-patterns and enabling pushdown predicate evaluation on nested fields.
  - coordinate catalog metadata through REST Catalogs (Polaris, Unity Catalog OSS, Lakekeeper) with short-lived STS tokens.
- **Iceberg REST Catalog Protocol**: implement scan planning (`POST /v1/oauth/tokens`, `POST /v1/namespaces/{ns}/tables`), ETag-based freshness validation (`If-None-Match`), Idempotency-Key commits for exactly-once writes, and dynamic credential vending (`GET /v1/credentials`).
- **S3 Object Storage Prefix Hashing**: set table property `write.object-storage.enabled = true` on high-throughput Iceberg tables to distribute Parquet files across hashed S3 prefixes, preventing AWS S3 503 Slow Down errors.
- **Write-Audit-Publish (WAP) Protocol**:
  1. *Write*: validate contracts and quarantine non-compliant records to DLQ; stage only compliant, deduplicated Parquet batches to an isolated Iceberg snapshot branch (`wap_audit_<run_id>`).
  2. *Audit*: execute automated contract assertions in-process via DuckDB over zero-copy Apache Arrow memory (`SET max_memory = '4GB';`). If circuit breaker $Q_r > 2.0\%$ ($N \ge 50$) trips or audits fail, abort without publishing.
  3. *Publish*: atomically fast-forward the `main` branch pointer to the audited snapshot; prune temporary branches.
- **DLQ Envelopes & Mathematical Circuit Breaker**:
  - quarantine non-conforming rows into a structured DLQ table with diagnostic JSON envelopes (`quarantine_id`, `source_system`, `batch_id`, `trace_id`, `payload_raw`, `error_code`, `violated_rule`, `diagnostic_context`).
  - calculate quarantine ratio: $Q_r = (N_{\text{quarantined}} / N_{\text{total}}) \times 100%$.
  - trip circuit breaker and halt pipeline if $Q_r > 2.0%$ with minimum sample size floor $N \ge 50$.
  - **wire DLQ to contract SLA fields**: map DLQ metrics to ODCS freshness and quality SLA thresholds for automated alerting.
- **Deterministic Upsert MERGE**:
  - generate composite SHA-256 cryptographic natural keys: `SHA256(col1 || '|' || col2 || '|' || col3)`.
  - apply intra-batch window deduplication (`ROW_NUMBER() OVER (PARTITION BY natural_key ORDER BY event_ts DESC) = 1`).
  - execute atomic `MERGE INTO` with watermark check (`source.event_ts >= target.event_ts`); never use non-idempotent appends.
- **Lakehouse Maintenance Lifecycle**:
  - bin-pack compaction (`rewrite_data_files`) merging Deletion Vectors to target 256MB Parquet blocks.
  - manifest rewriting (`rewrite_manifests`), 7-day TTL snapshot expiration with 50-snapshot floor, 72-hour orphan vacuuming.
- **Native Table Encryption (KMS)**: mandate AES-256 encryption at rest via cloud KMS (AWS KMS, GCP CMEK, Azure Key Vault) for all Iceberg and Delta Lake tables; manage encryption keys through catalog-integrated key management.
- **OpenLineage Explicit Lineage**: emit column-level lineage events for all pipeline stages (extraction, transformation, load) to enable end-to-end traceability and impact analysis.
- **Zero-Trust & PII Governance**: mask or hash PII per `data-classification.yaml`; enforce Column-Level Security (CLS) and Row-Level Security (RLS); sanitize RAG vector inputs per OWASP ASI06.
- detailed specifications are maintained in [`references/producer-contracts-and-lakehouse.md`](references/producer-contracts-and-lakehouse.md) and [`references/quality-gates-dlq-and-replayability.md`](references/quality-gates-dlq-and-replayability.md).

## Suggested Process

### 1. Ingest & Verify Producer Contract
Validate incoming batch or streaming event schemas against the ODCS v3.2.0 contract in producer CI/CD before persisting to storage.

### 2. Contract Validation, DLQ Quarantine & WAP Branch Staging
Validate incoming batch records against the ODCS contract. Route non-compliant records to the DLQ with structured envelopes. Calculate quarantine ratio $Q_r = (N_{\text{quarantined}} / N_{\text{total}}) \times 100\%$. Write and stage only compliant, deduplicated records to an isolated Iceberg snapshot branch (`wap_audit_<run_id>`) with `write.object-storage.enabled = true`.

### 3. Zero-Copy In-Process Arrow Audit
Run in-process DuckDB zero-copy Arrow memory audits (`SET max_memory = '4GB';`) against the staged data on the isolated branch. Execute assertion queries checking nullability, value ranges, distribution drift, and foreign keys.

### 4. Circuit Breaker & Audit Verification Gate
Evaluate audit query results and quarantine rate. If circuit breaker $Q_r > 2.0\%$ ($N \ge 50$) tripped, or if any DuckDB audit query fails, abort the transaction without publishing, drop the temporary audit branch, and alert.

### 5. Atomic Upsert MERGE & Fast-Forward Publish
Execute atomic `MERGE INTO` using composite SHA-256 natural keys. Fast-forward the `main` branch pointer to the validated branch snapshot knowing that uncontracted and defective data was already isolated in DLQ, then prune temporary audit branch metadata.

### 6. Iceberg REST Catalog Operations
Execute scan planning via REST API, validate ETag freshness, commit with Idempotency-Key for exactly-once semantics, and fetch short-lived credentials from catalog credential vending endpoint.

### 7. Native Encryption & OpenLineage Emission
Apply KMS-managed AES-256 encryption at rest. Emit OpenLineage column-level lineage events for extraction, transformation, and load stages.

### 8. Emit Pipeline Spec & FinOps Tags
Validate outputs against `contracts/schemas/data-pipeline-spec.json`. Tag maintenance metadata with `CostCenter`, `Environment`, and `TableOwner`.

## Checklist

- [ ] upstream source files and streaming CDC logs treated as strictly read-only
- [ ] ODCS v3.2.0 producer contracts validated at perimeter before storage persistence
- [ ] Iceberg v3 / Delta 4.4 UniForm configured with Puffin RoaringBitmap DVs and `spec-id` partition evolution
- [ ] **Variant type adopted for semi-structured JSON payloads** (canonical path)
- [ ] table property `write.object-storage.enabled = true` active to prevent AWS S3 503 Slow Down throttling
- [ ] **Iceberg REST Catalog protocol implemented**: scan planning, ETag freshness, Idempotency-Key commits, credential vending
- [ ] Write-Audit-Publish (WAP) staged on isolated branch (`wap_audit_<run_id>`) with in-process DuckDB Arrow audit
- [ ] non-conforming rows routed to DLQ quarantine with structured diagnostic JSON payload envelopes
- [ ] circuit breaker halts pipeline if quarantine ratio $Q_r > 2.0%$ with sample floor $N \ge 50$
- [ ] **DLQ wired to contract SLA fields** for automated alerting on freshness/quality threshold breaches
- [ ] deterministic upsert `MERGE INTO` enforced using composite SHA-256 natural keys and window deduplication
- [ ] lakehouse maintenance scheduled: 256MB bin-pack compaction, manifest rewriting, 7-day expiration (50-snapshot floor), 72h vacuum
- [ ] **Native table encryption (KMS)**: AES-256 at rest via AWS KMS / GCP CMEK / Azure Key Vault
- [ ] **OpenLineage explicit lineage** emitted for all pipeline stages (extraction, transformation, load)
- [ ] customer PII masked or hashed per `data-classification.yaml`; CLS/RLS policies active
- [ ] pipeline specifications emitted and validated against `contracts/schemas/data-pipeline-spec.json`

## Related Skills

- **analyze-data**: Query and explore conformed datasets without owning production pipeline infrastructure
- **database-maintenance**: Operational lakehouse maintenance, 256MB bin-pack compaction, and snapshot expiration
- **create-migration**: Manage relational database DDL schema migrations and rollback scripts
- **security-audit**: Audit pipeline data flow for PII leakage, zero-trust controls, and access boundaries
- **write-documentation**: Document pipeline runbooks, ODCS contracts, and data dictionaries
- **commit-code**: Safely commit pipeline definitions and transformation models to version control

## Output Contracts

When emitting pipeline specifications for downstream consumers, orchestrators, or cross-role handoffs, emit:

- `contracts/schemas/data-pipeline-spec.json` — complete pipeline definition, ODCS contract version, table format properties, WAP configuration, circuit breaker thresholds, FinOps metadata, **Iceberg REST protocol config, KMS encryption config, OpenLineage facets**.
- `contracts/schemas/data-analysis-report.json` — summary of ingested row counts, validation metrics, and data quality results when cross-role handoff to Data Analyst is required.

## Failure Modes

- **Silent schema poisoning**: unannounced upstream schema changes corrupt lakehouse tables. Mitigation: enforce ODCS v3.2.0 pre-ingestion validation; route non-conforming payloads to DLQ quarantine.
- **S3 partition throttling storm**: high-volume writes hit single S3 prefix limits causing 503 Slow Down errors. Mitigation: set table property `write.object-storage.enabled = true` for prefix hashing.
- **Direct write corruption**: unvalidated rows written directly to `main`. Mitigation: mandate Write-Audit-Publish (WAP) isolated snapshot branches (`wap_audit_<run_id>`).
- **DLQ poison overflow**: high-volume bad data floods quarantine silently. Mitigation: enforce circuit breaker halting ingestion when $Q_r > 2.0%$ ($N \ge 50$).
- **Non-idempotent replay duplication**: retrying a pipeline run creates duplicate records. Mitigation: require idempotent `MERGE INTO` operations on composite SHA-256 natural keys.
- **Unencrypted data at rest**: lakehouse tables lack native AES-256 encryption via KMS. Mitigation: enforce native table encryption (KMS) for all Iceberg and Delta Lake tables.
- **Missing lineage traceability**: pipeline stages do not emit OpenLineage events, breaking impact analysis. Mitigation: enforce OpenLineage explicit lineage emission for all stages.
- **Iceberg REST protocol bypass**: direct catalog access bypassing REST API scan planning, ETag, Idempotency-Key, and credential vending. Mitigation: enforce REST Catalog protocol for all catalog operations.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: classify PII with `data-classification.yaml`; enforce short-lived STS tokens via REST Catalog.
- **ASI04 Agentic Supply Chain**: validate connectors, dbt packages, and Iceberg catalog drivers against approved manifests.
- **ASI05 Unexpected Code Execution**: parameterize all dynamic SQL and partition paths; prohibit raw string interpolation.
- **ASI06 Memory & Context Poisoning**: sanitize and provenance-tag document chunks before RAG vector ingestion.
- **ASI07 Insecure Inter-Agent Communication**: emit structured `data-pipeline-spec.json` contracts for downstream agents.
- **ASI09 Human-Agent Trust Exploitation**: disclose residual ingestion risks, SLA deviations, and quality validation metrics truthfully.
- **NATIVE-ENCRYPTION-LOCK**: all Iceberg and Delta Lake tables must enforce AES-256 encryption at rest via cloud KMS; encryption keys managed through catalog-integrated key management.
- **OPENLINEAGE-LOCK**: all pipeline stages must emit column-level OpenLineage events for end-to-end traceability and impact analysis.
- **ICEBERG-REST-PROTOCOL-LOCK**: REST Catalog operations must use Iceberg REST protocol (scan planning, ETag freshness validation, Idempotency-Key commits, credential vending); direct catalog access bypassing REST is prohibited.
