---
name: gcp-dataflow-flex-templates
description: >
  Build and run Dataflow Flex Templates: package launch container, template specs,
  parameters, staging/temp buckets, worker SA least privilege, and network/private
  Google access. Use when operationalizing owned Apache Beam pipelines on Dataflow
  with reusable flex templates.
---

# GCP Dataflow Flex Templates

## Scope And Authorization

- **In scope:** Dataflow jobs and templates in GCP projects you own.
- **Out of scope:** launching jobs against unauthorized data or foreign projects.
- Pipelines often touch sensitive data—control worker SA and logs.
- Redact template parameters that include secrets; use Secret Manager.
- Pair pipeline code with `code-quality-standards`.

## When To Use

- Packaging Beam pipelines as **Flex Templates** for repeated launches.
- Standardizing CI → Artifact Registry image → `gcloud dataflow flex-template run`.
- Replacing classic templates or ad-hoc `mvn/gradle` launch from laptops.
- Reviewing parameter injection and worker permissions.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Flink CDC/checkpoints | `flink-*` skills |
| BigQuery row security | `gcp-bigquery-row-access` |
| Cloud Run Jobs simple batch | `gcp-cloud-run-jobs` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Artifact | Role |
| --- | --- |
| Flex template image | Container with SDK + pipeline code |
| Template file (JSON/GCS) | Metadata and default parameters |
| Staging/temp buckets | Dataflow shuffle artifacts |
| Worker SA | Runtime data access |
| Parameters | Job-time inputs (paths, project, mode) |

## Workflow

### 1. Confirm scope and success criteria

1. Pipeline language (Java/Python/Go), region, data sources/sinks, budget.
2. Success: template builds in CI; launch with parameters works; SA cannot access unrelated buckets; secrets not in CLI history.
3. Idempotency/replay expectations documented.

### 2. Inventory

```bash
gcloud dataflow jobs list --project=PROJECT --region=REGION
gsutil ls gs://YOUR_TEMPLATES/
gcloud artifacts docker images list REGION-docker.pkg.dev/PROJECT/REPO
```

1. List worker SA roles.
2. Find hardcoded keys in pipeline options.

### 3. Build flex template container

```dockerfile
# Conceptual — use Google-published base images for Beam version you pin
# COPY pipeline code; define ENTRYPOINT for flex template launcher
```

```bash
# Build/push owned image
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT/REPO/pipeline:DIGEST
```

1. Pin Beam/Dataflow worker versions for reproducibility.
2. Non-root where feasible; minimal OS packages.

### 4. Build template spec and store

```bash
gcloud dataflow flex-template build gs://BUCKET/templates/pipeline.json \
  --image=REGION-docker.pkg.dev/PROJECT/REPO/pipeline:DIGEST \
  --sdk-language=PYTHON \
  --metadata-file=metadata.json
```

```json
{
  "name": "pipeline",
  "parameters": [
    {"name": "input", "label": "Input path", "isOptional": false},
    {"name": "output", "label": "Output table", "isOptional": false}
  ]
}
```

1. Validate parameter schema; reject unexpected params in code.
2. Do not pass passwords as plain parameters—use Secret Manager + code fetch with SA.

### 5. Launch with least privilege

```bash
gcloud dataflow flex-template run JOB_NAME \
  --template-file-gcs-location=gs://BUCKET/templates/pipeline.json \
  --region=REGION \
  --parameters=input=gs://in/...,output=project:dataset.table \
  --service-account-email=dataflow-worker@PROJECT.iam.gserviceaccount.com \
  --network=VPC \
  --subnetwork=regions/REGION/subnetworks/SUBNET \
  --disable-public-ips
```

1. Worker SA: specific `storage.objectAdmin` on needed buckets only; BQ dataset roles limited.
2. Staging/temp buckets: private; lifecycle delete.
3. Private Google Access / PSC as architecture requires.
4. Enable Dataflow Shuffle / Streaming Engine options intentionally for cost/security tradeoffs.

### 6. Verify with evidence

| Check | Expect |
| --- | --- |
| Launch | Job RUNNING→DONE |
| Wrong SA | Permission denied on data |
| Public IP disabled | Workers private |
| Parameter injection | Validated; no shell injection in options |

```bash
gcloud dataflow jobs describe JOB_ID --region=REGION
```

### 7. Observe and hand off

1. Alert on failed jobs and streaming backlog.
2. Version templates immutably (new GCS object / image digest per release).
3. Document parameters and SA matrix.
4. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Launch | Flex template + CI | Laptop-only Beam run to prod |
| SA | Narrow data access | Project editor worker |
| Secrets | Secret Manager | `--parameters=password=...` |
| Network | Private workers | Public IPs unnecessary |
| Versions | Digest pins | `:latest` template image |
| Buckets | Private + lifecycle | World-readable staging |

## Output Checklist

- [ ] Pipeline packaged as flex template image
- [ ] Template GCS location versioned
- [ ] Parameters documented and validated
- [ ] Worker SA least privilege evidenced
- [ ] Staging/temp buckets secured
- [ ] Private networking configured if required
- [ ] Job success + deny tests
- [ ] Monitoring for failures
- [ ] `code-quality-standards` applied

## Rules

- Owned data and projects only.
- Treat worker SA as highly privileged relative to data—minimize.
- Prefer immutable template versions.
- Never put long-lived credentials in template parameters or images.
