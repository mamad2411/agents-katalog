---
name: managed-ingestion-service
description: >
  Ingest documents at scale into Amazon OpenSearch using OpenSearch Ingestion
  Service (OSIS) pipelines. Upload pre-generated JSONL chunks to S3 and OSIS
  indexes them — optionally using semantic_enrichment in the sink to create the
  index with ASE automatically. Cloud ingestion — uploading raw PDF/DOCX and
  letting document_extractor parse them in the cloud — is available via private
  beta. Use this skill when the user wants to ingest documents into a cloud
  OpenSearch domain or collection, process documents at full volume beyond local
  limits, or set up an OSIS pipeline. Activate even if the user says OSIS,
  ingestion pipeline, document extraction, S3 ingestion, managed ingestion,
  or cloud processing.
compatibility: >
  Requires AWS credentials, an ACTIVE Amazon OpenSearch Service domain (v2.19+)
  or Serverless collection endpoint, and an S3 bucket for source documents or chunks.
metadata:
  author: opensearch-project
  version: "3.0"
---

# Managed Ingestion Service

## Overview

Ingest documents into Amazon OpenSearch at scale via OSIS pipelines. Supports both
Amazon OpenSearch Service (AOS) domains and Amazon OpenSearch Serverless (AOSS) collections.

## When to Use

- User has an OpenSearch domain or AOSS collection and wants to ingest documents at scale
- User wants to move from local development to cloud ingestion
- User mentions OSIS, S3 ingestion, cloud processing, managed ingestion

## Ingestion Paths

| Path | Upload to S3 | OSIS Processor | Status | Best for |
|------|--------------|----------------|--------|----------|
| **Local processing** | JSONL chunks (from local Docling) | `parse_json` (pass-through) | **Available now** | Validated locally, deploy at scale |
| **Cloud ingestion** | Raw PDF/DOCX/PPTX/XLSX | `document_extractor` | **Private beta** | Full cloud processing, no local compute |

Both paths support the same sink options — the only difference is source content and processor.

## Key Constraints

- AWS credentials must be configured; check first and stop if missing
- **AOS domains:** must be running OpenSearch 2.19+ for ASE; public domains only (no VPC)
- **AOSS collections:** must be in ACTIVE state before creating the pipeline
- The IAM role (`sts_role_arn`) must have S3 read + OpenSearch write permissions
- When using `semantic_enrichment`: it creates the index automatically — do NOT create it manually
- `parse_json` is the OSIS **processor** (parses JSONL lines); `semantic_enrichment` is in the **sink** (applies embeddings when writing) — they are independent
- Save generated YAML to `.opensearch/pipelines/<pipeline-name>.yaml`

---

## Entry Point

### Step 1: Validate credentials

```bash
aws sts get-caller-identity
```

If this fails, stop and ask the user to configure credentials.

### Step 2: Determine the deploy target

**Ask:** "Are you ingesting into an Amazon OpenSearch Service (AOS) domain or an OpenSearch Serverless (AOSS) collection?"

**AOS domain:**
- Must be running OpenSearch 2.19+ for semantic_enrichment
- Verify the domain exists and is in ACTIVE state:
  ```bash
  aws opensearch describe-domain --domain-name <domain-name> --region <region>
  ```

**AOSS collection:**
- Verify it's ACTIVE:
  ```bash
  aws opensearchserverless batch-get-collection \
    --ids <collection-id> --region <region>
  ```

If the user needs a new domain/collection, provision one using the
[aws-setup](../../cloud/aws-setup/SKILL.md) skill. Wait until ACTIVE, then continue here.

### Step 3: Determine the data source

**Ask:** "Do you already have JSONL chunks, or do you have raw documents (PDF/DOCX) that need processing?"

**If the user already has JSONL chunks:**
- Validate the JSONL format: each line must be valid JSON with text fields that can be enriched.
- Proceed to Step 4.

**If the user has raw documents (PDF/DOCX/etc.):**

Present both options to the user:

> I see you have raw PDF documents. There are two ways to process them for ingestion:
>
> **Option A — Cloud ingestion (recommended for scale)**
> Upload your PDFs directly to S3 and let the cloud handle parsing, chunking, and indexing with ASE (automatic sparse embeddings) — no local compute needed. This is currently in private beta.
>
> 👉 To get access, email **opensearch-agent-skills-interests@amazon.com** with your AWS account ID and region.
>
> **Option B — Local processing (available now)**
> Process your PDFs locally with Docling to produce JSONL chunks, then upload those to S3 for cloud ingestion. Gives you full control over chunk quality.
>
> Which would you prefer? (Or if you'd like to get started immediately, I'll go with Option B while you wait for beta access.)

- If the user chooses **Option A**: confirm they should email opensearch-agent-skills-interests@amazon.com, and offer to proceed with Option B in the meantime.
- If the user chooses **Option B**: proceed with [document_processing_guide.md](../../ingest/document-processing/document_processing_guide.md). Once chunks are ready at `.opensearch/chunks/<index>/`, return here and continue to Step 4.

### Step 4: Gather parameters

Collect from the user (one at a time):
1. **Deploy target** — AOS domain endpoint or AOSS collection endpoint
2. **S3 bucket name** — where chunks will be uploaded
3. **S3 prefix** — key prefix for source files (e.g., `chunks/input`)
4. **Target index name** — will be created by `semantic_enrichment` if new; or an existing index
5. **IAM role ARN** — for OSIS pipeline (or offer to create one)
6. **Network policy name** — (AOSS only) network policy allowing OSIS access
7. **Region** — AWS region

### Step 5: Determine the sink mode

**Ask:** "Do you already have an existing index to ingest into, or should I create a new one with automatic semantic enrichment (ASE)?"

**Path A — Existing index (no semantic_enrichment):**
- The user already has an index with mappings configured.
- Use the plain opensearch sink (no `semantic_enrichment` block).
- Documents are written directly without automatic embedding.
- Proceed with Pipeline YAML — Existing Index.

**Path B — New index (with semantic_enrichment / ASE):**
- OSIS creates the index automatically with ASE.
- **Ask:** "Which text fields in your chunks should have semantic enrichment (sparse embeddings)?"
- The user should specify the field names from their JSONL that contain natural language text
  (e.g., `text`, `title`, `description`, `summary`).
- Each field is enriched independently — ASE generates sparse vectors for each specified field.
- Proceed with Pipeline YAML — New Index with Semantic Enrichment.

> **Note:** `semantic_enrichment` is about which text fields get sparse embeddings — it is
> not tied to any particular "search strategy." Any text field that contains natural language
> and should be semantically searchable should be listed.

### Step 6: Upload to S3

Upload your locally-prepared chunks:
```bash
aws s3 cp .opensearch/chunks/<index>/<file>.jsonl s3://<bucket>/<prefix>/
```

For multiple files:
```bash
aws s3 cp .opensearch/chunks/<index>/ s3://<bucket>/<prefix>/ --recursive
```

### Step 7: Create OSIS pipeline

Generate the YAML based on the selected path and sink mode, save to
`.opensearch/pipelines/<pipeline-name>.yaml`, then create:

```bash
aws osis create-pipeline \
  --pipeline-name <pipeline-name> \
  --min-units 1 \
  --max-units 1 \
  --pipeline-configuration-body file://.opensearch/pipelines/<pipeline-name>.yaml \
  --region <region>
```

### Step 8: Verify

Poll until ACTIVE:
```bash
aws osis get-pipeline \
  --pipeline-name <pipeline-name> \
  --region <region> \
  --query 'Pipeline.Status' --output text
```

Then verify documents are indexed (check doc count, test a `match` query — if ASE is
configured, it rewrites match queries to neural sparse automatically).

---

## Pipeline YAML — Local Chunking + New Index (AOSS with semantic_enrichment)

```yaml
version: "2"
<pipeline-name>:
  source:
    s3:
      codec:
        newline:
      compression: "none"
      aws:
        region: "<region>"
        sts_role_arn: "<iam-role-arn>"
      acknowledgments: true
      scan:
        scheduling:
          interval: PT30S
        buckets:
          - bucket:
              name: "<s3-bucket-name>"
              filter:
                include_prefix:
                  - <s3-prefix>
  processor:
    - parse_json:
    - delete_entries:
        with_keys: [ "s3" ]
  sink:
    - opensearch:
        hosts: [ "<aoss-collection-endpoint>" ]
        aws:
          region: "<region>"
          sts_role_arn: "<iam-role-arn>"
          semantic_enrichment:
            fields:
              - name: "<text-field-name>"
                language: "english"
          serverless: true
          serverless_options:
            network_policy_name: "<network-policy-name>"
        index: "<index-name>"
        index_type: custom
```

---

## Pipeline YAML — Local Chunking + New Index (AOS domain with semantic_enrichment)

```yaml
version: "2"
<pipeline-name>:
  source:
    s3:
      codec:
        newline:
      compression: "none"
      aws:
        region: "<region>"
        sts_role_arn: "<iam-role-arn>"
      acknowledgments: true
      scan:
        scheduling:
          interval: PT30S
        buckets:
          - bucket:
              name: "<s3-bucket-name>"
              filter:
                include_prefix:
                  - <s3-prefix>
  processor:
    - parse_json:
    - delete_entries:
        with_keys: [ "s3" ]
  sink:
    - opensearch:
        hosts: [ "<aos-domain-endpoint>" ]
        aws:
          region: "<region>"
          sts_role_arn: "<iam-role-arn>"
          semantic_enrichment:
            fields:
              - name: "<text-field-name>"
                language: "english"
        index: "<index-name>"
        index_type: custom
```

Key difference from AOSS: no `serverless: true` or `serverless_options` block.

---

## Pipeline YAML — Existing Index (no semantic_enrichment)

Use this when the user already has an index with mappings configured.

**For AOSS:**
```yaml
version: "2"
<pipeline-name>:
  source:
    s3:
      codec:
        newline:
      compression: "none"
      aws:
        region: "<region>"
        sts_role_arn: "<iam-role-arn>"
      acknowledgments: true
      scan:
        scheduling:
          interval: PT30S
        buckets:
          - bucket:
              name: "<s3-bucket-name>"
              filter:
                include_prefix:
                  - <s3-prefix>
  processor:
    - parse_json:
    - delete_entries:
        with_keys: [ "s3" ]
  sink:
    - opensearch:
        hosts: [ "<aoss-collection-endpoint>" ]
        aws:
          region: "<region>"
          sts_role_arn: "<iam-role-arn>"
          serverless: true
          serverless_options:
            network_policy_name: "<network-policy-name>"
        index: "<index-name>"
        index_type: custom
```

**For AOS:**
```yaml
version: "2"
<pipeline-name>:
  source:
    s3:
      codec:
        newline:
      compression: "none"
      aws:
        region: "<region>"
        sts_role_arn: "<iam-role-arn>"
      acknowledgments: true
      scan:
        scheduling:
          interval: PT30S
        buckets:
          - bucket:
              name: "<s3-bucket-name>"
              filter:
                include_prefix:
                  - <s3-prefix>
  processor:
    - parse_json:
    - delete_entries:
        with_keys: [ "s3" ]
  sink:
    - opensearch:
        hosts: [ "<aos-domain-endpoint>" ]
        aws:
          region: "<region>"
          sts_role_arn: "<iam-role-arn>"
        index: "<index-name>"
        index_type: custom
```

Key points:
- No `semantic_enrichment` — the index already exists with its own mappings
- Documents are written directly without automatic embedding
- Use this when the user manages their own index lifecycle

---

## Cloud Ingestion (private beta)

> **Private beta.** Cloud ingestion lets you upload raw documents (PDF/DOCX) directly to S3
> and have the OSIS pipeline handle parsing, chunking, and indexing end-to-end — no local
> compute needed. Contact **opensearch-agent-skills-interests@amazon.com** to onboard.
> Pipeline YAML will be provided during onboarding.

---

## Key Concepts

### parse_json vs semantic_enrichment

These are **independent** components at different stages of the pipeline:

| Component | Stage | Purpose |
|-----------|-------|---------|
| `parse_json` | **Processor** | Parses each JSONL line into a structured JSON document |
| `semantic_enrichment` | **Sink** | Applies sparse embeddings to specified text fields when writing to the index |

You can use `parse_json` without `semantic_enrichment` (existing index) or with it (new index + ASE).

### semantic_enrichment field selection

`semantic_enrichment` is about **which text fields get sparse vector embeddings**. It is NOT
tied to any search strategy (hybrid, semantic, agentic). Any text field containing natural
language that you want to be semantically searchable should be listed:

```yaml
semantic_enrichment:
  fields:
    - name: "text"
      language: "english"
    - name: "title"
      language: "english"
```

Ask the user: "Which fields in your chunks contain natural language text that should be
semantically searchable?" — then list those fields.

---
## IAM Role Setup (if needed)

See [iam-setup.md](iam-setup.md) for full IAM role creation, S3/AOSS/AOS permissions,
and data access policy configuration. The IAM role is a prerequisite — without it the
pipeline will fail with permission errors on every retry.


## Parameters Reference

| Parameter | Description | Example |
|-----------|-------------|---------|
| `region` | AWS region for S3 and OpenSearch | `us-west-2` |
| `iam-role-arn` | IAM role with S3 read + OpenSearch write | `arn:aws:iam::123456789012:role/osis-role` |
| `s3-bucket-name` | S3 bucket for source files | `my-docs-bucket` |
| `s3-prefix` | Key prefix to filter source files | `chunks/input` |
| `aos-domain-endpoint` | AOS domain endpoint (v2.19+) | `https://my-domain.us-west-2.es.amazonaws.com` |
| `aoss-collection-endpoint` | AOSS endpoint (must be ACTIVE) | `https://abc123.us-west-2.aoss.amazonaws.com` |
| `network-policy-name` | AOSS network policy name (AOSS only) | `my-net-policy` |
| `index-name` | Target index (created by semantic_enrichment, or existing) | `my-docs-index` |
| `text-field-name` | Field(s) to apply semantic enrichment to | `text`, `title`, `description` |
