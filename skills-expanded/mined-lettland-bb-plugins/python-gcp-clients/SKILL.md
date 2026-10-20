---
name: python-gcp-clients
description: Use when using google-cloud-* clients in Python — auth (ADC, SA keys, workload identity), GCS object ops, BigQuery query/load patterns, cost guardrails.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [python]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [python-essentials, python-django, python-data-pipeline, security, observability-essentials]
---

# Python GCP Clients

**Iron Law: never ship a service-account JSON key into a container if you can avoid it. ADC + workload identity is the default; a key on disk is an auditable liability. Always set a max-bytes-billed guard on every BigQuery query — one missing `WHERE` clause on a partitioned table is a five-figure invoice.**

**Versions:** google-cloud-storage `2.18+` · google-cloud-bigquery `3.27+` · google-auth `2.35+` — _Both clients moved to gRPC-first; HTTP fallback still works. `google-cloud-bigquery-storage` is the fast read path (Arrow batches) — install it alongside `google-cloud-bigquery[bqstorage,pandas]`._

## Auth — precedence and pick-list

ADC (Application Default Credentials) resolves in this order — the first hit wins:

| #   | Source                                                                      | Use case                                           |
| --- | --------------------------------------------------------------------------- | -------------------------------------------------- |
| 1   | `GOOGLE_APPLICATION_CREDENTIALS` env var → file path                        | Legacy SA JSON key — **avoid for prod**            |
| 2   | gcloud user creds (`~/.config/gcloud/application_default_credentials.json`) | Local dev: `gcloud auth application-default login` |
| 3   | GCE/GKE/Cloud Run metadata server                                           | **The right answer in prod** — no keys on disk     |
| 4   | Workload Identity Federation (external OIDC, e.g., GitHub Actions, AWS)     | Cross-cloud / CI without SA keys                   |

```python
from google.cloud import storage, bigquery
# No args = ADC. Project picked from env (GOOGLE_CLOUD_PROJECT) or metadata server.
gcs = storage.Client()
bq  = bigquery.Client(project="my-proj", location="EU")
```

**Workload identity in GKE**: bind a Kubernetes SA to a Google SA via `iam.workloadIdentityUser`. Pods inherit the GSA; no key file. In Cloud Run / Cloud Functions: the runtime SA is automatic — just grant it the IAM roles it needs.

**If you must ship a key** (third-party hosts, restricted environments):

- Store in a secret manager (GCP Secret Manager, Vault, 1Password CLI), never in the image.
- Mount at runtime to a tmpfs path; never bake into a layer.
- Rotate on a schedule (`iam.serviceAccountKeys.create` + delete the old one).
- Scope the SA to one project, minimum roles, deny `iam.serviceAccountTokenCreator` unless explicitly needed.

See `Skill(devkit:security)` for secret handling rules.

## GCS — Cloud Storage patterns

```python
from google.cloud import storage
from datetime import timedelta

gcs = storage.Client()
bucket = gcs.bucket("my-bucket")

# Resumable upload — auto-chunked, retries; default for files > 8 MiB
blob = bucket.blob("uploads/big.parquet")
blob.upload_from_filename("local/big.parquet", timeout=300)        # resumable by default

# Streaming download with chunked iteration
blob = bucket.blob("uploads/big.parquet")
with blob.open("rb") as f:
    for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
        process(chunk)

# Signed URL for time-limited download (V4 signing — required after 2025)
url = blob.generate_signed_url(
    version="v4",
    expiration=timedelta(minutes=15),
    method="GET",
    response_disposition='attachment; filename="report.pdf"',      # force download
)

# Set Content-Disposition / Content-Type at upload (matters for browser handling)
blob.upload_from_string(
    pdf_bytes,
    content_type="application/pdf",
)
blob.content_disposition = 'attachment; filename="report.pdf"'
blob.patch()
```

**Lifecycle rules** (set once on the bucket, run forever — no Python needed at runtime):

```python
bucket.lifecycle_rules = [
    {"action": {"type": "Delete"}, "condition": {"age": 30, "matchesPrefix": ["tmp/"]}},
    {"action": {"type": "SetStorageClass", "storageClass": "NEARLINE"}, "condition": {"age": 90}},
]
bucket.patch()
```

**Composite ops**: use `gcs.batch()` context manager for ≤ 100 metadata operations in one round-trip. Composing > 100 objects (`compose()`) hits the 32-object limit per call — chain multiple compose calls.

**Resumable upload session URLs** (browser-direct uploads): create on the server with `blob.create_resumable_upload_session()`, hand the URL to the client. The client PUTs directly to GCS — your service never sees the bytes. Pair with object-level CORS.

## BigQuery — query, load, stream

```python
from google.cloud import bigquery
bq = bigquery.Client(location="EU")

# Parameterized query — ALWAYS use this, NEVER f-string SQL
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("user_id", "INT64", 42),
        bigquery.ScalarQueryParameter("since",   "TIMESTAMP", since_ts),
    ],
    use_query_cache=True,
    maximum_bytes_billed=10 * 10**9,       # 10 GB hard cap — refuse query if it would scan more
)
rows = bq.query("""
    SELECT order_id, total FROM `proj.ds.orders`
    WHERE user_id = @user_id AND created_at >= @since
""", job_config=job_config).result()
```

**Cost guardrails — apply every time**:

| Guard                              | How                                                                                                                         |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Dry run** before unknown queries | `job_config.dry_run = True; job_config.use_query_cache = False` — `query.total_bytes_processed` tells you the bill          |
| **`maximum_bytes_billed`**         | Job fails if it would scan more — set per-query or per-client                                                               |
| **Partition filter**               | `WHERE _PARTITIONTIME >= TIMESTAMP("...")` on partitioned tables — required if `require_partition_filter=TRUE` on the table |
| **Cluster keys**                   | Cluster on common filter columns; reduces bytes scanned dramatically                                                        |
| **`SELECT *` is banned**           | Project explicit columns — column-store charges per column scanned                                                          |
| **Slot reservations**              | Predictable spend on flat-rate ($2k+/mo minimum) — only worth it for sustained > 1 TB/day                                   |

```python
# Load from GCS — parquet preferred (typed, columnar, no schema autodetect lottery)
job = bq.load_table_from_uri(
    "gs://my-bucket/exports/orders/*.parquet",
    "proj.ds.orders",
    job_config=bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        time_partitioning=bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY, field="created_at",
        ),
        clustering_fields=["user_id", "status"],
    ),
)
job.result()                                # blocks; raises on failure
```

**Streaming inserts** (`insert_rows_json`) are now legacy. **Use the Storage Write API** (`google-cloud-bigquery-storage`) for high-throughput append-only ingest: exactly-once semantics, lower cost, schema validation. Streaming inserts are still fine for low-volume use.

**Reading large results into a DataFrame**: install the `bqstorage` extra and use `to_arrow(bqstorage_client=...)` or `to_dataframe(bqstorage_client=...)` — the BigQuery Storage Read API is 5–10× faster than the standard REST iterator on multi-million-row results.

## IAM tips

- Grant on the **resource** (dataset, bucket), not on the project, when possible.
- `roles/storage.objectAdmin` is too broad — use `roles/storage.objectViewer` + `roles/storage.objectCreator` if writes are append-only.
- BigQuery: `roles/bigquery.dataViewer` + `roles/bigquery.jobUser` is the minimum for "can run queries against this dataset". `roles/bigquery.user` includes job creation across the project — broader than needed.
- Audit with `gcloud asset analyze-iam-policy` quarterly; revoke unused bindings.
- IAM Conditions can restrict by request time / resource tag — useful for temporary access.

## Emulators (for tests)

| Service   | Emulator                                                                                                                                        | Pin                                                   |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| GCS       | `fsouza/fake-gcs-server`                                                                                                                        | docker image; point client at `STORAGE_EMULATOR_HOST` |
| BigQuery  | **no official emulator** — use a separate sandbox dataset with lifecycle expiration, or `goccy/bigquery-emulator` (community, partial coverage) |
| Pub/Sub   | `gcr.io/google.com/cloudsdktool/cloud-sdk` includes a Pub/Sub emulator                                                                          |
| Firestore | `firebase-tools` / `gcloud` emulator                                                                                                            |

```python
# Client pointed at the GCS emulator
import os
os.environ["STORAGE_EMULATOR_HOST"] = "http://localhost:4443"
gcs = storage.Client(project="test", credentials=AnonymousCredentials())
```

For BigQuery in tests: prefer integration tests against a real sandbox dataset (`test_*` prefix, 1-day partition expiration) over the community emulator — query syntax compatibility drifts.

## Anti-patterns

- SA JSON key baked into a container image or committed to a repo — rotate now
- `SELECT *` on a wide table for a one-row preview — use `LIMIT 0` schema + sample
- f-string SQL (`f"SELECT ... WHERE id = {uid}"`) — SQL injection in BQ too; use query params
- Calling `insert_rows_json` for high throughput — use Storage Write API
- No `maximum_bytes_billed` on user-controlled queries — one runaway scan = real money
- Downloading 10 GB blobs with `download_as_bytes()` — use streaming `blob.open("rb")`
- Granting `roles/owner` to a service account "just to unblock" — irreversibly broad audit problem
- Forgetting to set `version="v4"` on signed URLs — v2 signing is deprecated
- Not setting a partition filter requirement on big partitioned tables (`require_partition_filter=TRUE`) — invites accidental full-table scans

## Red flags

| Thought                                   | Reality                                                                   |
| ----------------------------------------- | ------------------------------------------------------------------------- |
| "I'll just mount the SA key into the pod" | Workload identity is the prod path. Keys are a finding waiting to happen. |
| "Dry-runs slow things down"               | Saves orders of magnitude more than it costs. Always dry-run unknowns.    |
| "Streaming inserts are fine"              | Storage Write API is cheaper, faster, and supports schema enforcement.    |
| "Lifecycle can wait"                      | It can't. GCS bills for what you don't delete, forever.                   |
| "I'll add the partition filter later"     | The bill comes first. Add `require_partition_filter` on the table.        |
| "ADC just works locally"                  | Until CI runs without `gcloud auth`. Use WIF for CI from day one.         |

## Hand-off

For broader Python rules: `Skill(devkit:python-essentials)`. For Django integration (model fields backed by GCS): `Skill(devkit:python-django)`. For pulling BigQuery results into polars/pandas: `Skill(devkit:python-data-pipeline)`. For secret handling and IAM hygiene: `Skill(devkit:security)`. For tracing slow GCP calls: `Skill(devkit:observability-essentials)`.
