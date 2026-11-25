---
name: loki-log-aggregation-configuration
description: >
  Configures Grafana Loki as a log aggregation backend — ingestion
  limits, label/cardinality design, retention periods, index/chunk
  schema config, and object-storage backends (S3/GCS/Azure Blob or
  filesystem for small setups), plus single-binary vs. simple-scalable
  vs. microservices deployment modes. Use when the user asks to "stand
  up Loki," "set Loki log retention," "configure Loki's storage
  backend," "design labels for Loki ingestion," "scale Loki for higher
  log volume," or "Loki is rejecting/dropping logs at ingestion."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# Loki Log Aggregation Configuration

## Purpose

Loki indexes only a small label set per log stream and stores the log
content itself as compressed chunks in object storage — a deliberate
design trade-off (cheap to run at scale, versus Elasticsearch's
full-text index) that only pays off if labels are chosen with
cardinality discipline and ingestion limits/retention are configured for
real volume, not left at chart defaults. This skill covers configuring
Loki itself as the aggregation backend: label/cardinality design,
`limits_config` ingestion controls, the schema/chunk store config that
determines the index format and storage backend, retention, and
deployment-mode selection — not the queries run against it (see
[logql-query-authoring](../logql-query-authoring/SKILL.md)) and not
pre-deploy config validation (see
[loki-configuration-validation](../loki-configuration-validation/SKILL.md)),
which is a distinct, narrower concern from standing up Loki in the first
place.

## When to use

- Standing up a new Loki instance/cluster for log aggregation, choosing
  a deployment mode and storage backend.
- Designing which fields become indexed stream labels versus staying as
  unindexed log content/parsed fields.
- Setting or revising retention (how long logs are kept, and per-tenant
  overrides).
- Loki is rejecting logs at ingestion (`429`/`entry too far behind`/
  `per-stream rate limit exceeded`) or silently dropping expected log
  volume.
- Scaling Loki from a single-binary/small setup to handle materially
  higher log volume, and deciding on simple-scalable vs. microservices
  deployment mode.
- Migrating or configuring the object-storage backend (S3/GCS/Azure Blob)
  and the index/chunk schema version that governs it.

## Prerequisites & environment

- Loki 2.9+ assumed (TSDB index format, the current recommended schema,
  became stable/default-recommended from 2.9; earlier `boltdb-shipper`
  schema configs still work but TSDB is preferred for new deployments).
- A deployment target: Kubernetes (via the `loki` or
  `loki-distributed`/`loki-simple-scalable` Helm charts) or bare
  VMs/containers running the Loki binary directly.
- An object storage backend for anything beyond a small/test setup —
  filesystem storage is fine for a single-node evaluation but is not
  durable or horizontally scalable; S3/GCS/Azure Blob (or an S3-compatible
  store like MinIO) is expected for production.
- A log shipper already forwarding logs into Loki's push API (Promtail,
  the Grafana Agent, or Fluent Bit — see
  [fluent-bit-log-forwarding-configuration](../fluent-bit-log-forwarding-configuration/SKILL.md)
  for configuring Fluent Bit specifically as that shipper) so there's
  something to ingest while tuning limits.
- For multi-tenant setups: `auth_enabled: true` and a clear tenant-ID
  (`X-Scope-OrgID`) scheme agreed with whatever is pushing logs.

## Step-by-step guidance

1. **Choose a deployment mode deliberately, by volume, not by default.**
   - **Single binary (`-target=all`):** simplest, fine for low volume/dev/
     small production. All components (distributor, ingester, querier,
     etc.) run in one process.
   - **Simple scalable (`-target=read` / `-target=write` / `-target=backend`):**
     splits the read and write paths into independently scaled
     deployments — the right default for most production Kubernetes
     setups once volume grows past what single-binary comfortably
     handles.
   - **Microservices:** every Loki component (distributor, ingester,
     querier, query-frontend, compactor, etc.) scaled independently —
     reserve for genuinely large multi-team/high-volume deployments; it's
     meaningfully more operational surface area than most teams need.

2. **Design labels for cardinality, not convenience, before ingesting
   anything at volume.** Every distinct combination of label values
   creates a separate stream, and Loki's index grows with the number of
   streams, not the number of log lines:
   ```yaml
   # GOOD: bounded, small label set
   labels:
     app: payments-api
     namespace: payments
     env: production
     level: error   # small enumerated set (debug/info/warn/error)

   # BAD: unbounded/high-cardinality labels — never do this
   labels:
     app: payments-api
     request_id: "a1b2c3..."     # unique per request — unbounded
     user_id: "48213"            # unbounded
     pod_ip: "10.2.3.41"         # high cardinality, churns on every restart
   ```
   > **Warning — unbounded cardinality:** a label like `request_id`,
   > `user_id`, `trace_id`, or a raw pod IP explodes the number of
   > streams Loki has to track, degrading ingestion and query performance
   > cluster-wide, not just for whoever added the label. Fields like
   > these belong in the log line content (extracted at query time via
   > `| json`/`| logfmt` — see
   > [logql-query-authoring](../logql-query-authoring/SKILL.md)), never
   > as indexed labels. If unsure whether a label is safe, check its
   > cardinality before it ships broadly (see
   > [loki-configuration-validation](../loki-configuration-validation/SKILL.md)
   > for pre-deploy checks).

3. **Configure ingestion limits in `limits_config` to protect the
   cluster from a runaway/misbehaving shipper**, rather than leaving
   defaults that either reject legitimate traffic or let one bad actor
   overwhelm shared infrastructure:
   ```yaml
   limits_config:
     ingestion_rate_mb: 10          # sustained MB/s per tenant
     ingestion_burst_size_mb: 20    # short burst allowance above the rate
     per_stream_rate_limit: 5MB     # per-stream ingestion rate ceiling
     per_stream_rate_limit_burst: 15MB
     max_streams_per_user: 10000    # hard ceiling on distinct streams per tenant
     max_line_size: 256KB
     reject_old_samples: true
     reject_old_samples_max_age: 168h   # 7 days
   ```
   `max_streams_per_user` is the single most important cardinality
   backstop — set it deliberately based on expected label cardinality
   times expected app/namespace count, not left unbounded.

4. **Set retention explicitly, per tenant if multi-tenant, via the
   compactor** — Loki does not delete old chunks on its own without a
   configured retention policy:
   ```yaml
   compactor:
     working_directory: /loki/compactor
     retention_enabled: true
     delete_request_store: s3

   limits_config:
     retention_period: 720h   # 30 days, cluster default

   # per-tenant override (in runtime overrides config, not limits_config)
   overrides:
     "tenant-payments":
       retention_period: 2160h   # 90 days for a tenant needing longer retention
   ```
   Retention is enforced by the **compactor** component — it must be
   running (and `retention_enabled: true` set) for old chunks to actually
   be deleted; setting `retention_period` alone with the compactor
   disabled leaves chunks accumulating indefinitely in object storage.

5. **Configure the schema and storage backend together** — the schema
   config determines the index format (TSDB is current-recommended) and
   is versioned by date so you can roll forward without rewriting
   historical data:
   ```yaml
   schema_config:
     configs:
       - from: 2024-01-01
         store: tsdb
         object_store: s3
         schema: v13
         index:
           prefix: loki_index_
           period: 24h

   storage_config:
     tsdb_shipper:
       active_index_directory: /loki/tsdb-index
       cache_location: /loki/tsdb-cache
     aws:
       s3: s3://<AWS_REGION>/<S3_BUCKET_NAME>
       s3forcepathstyle: false
   ```
   Adding a new `schema_config.configs` entry with a future `from:` date
   is how you change schema/store version going forward without
   rewriting already-ingested data under the old schema — never edit an
   existing entry's `from:` date retroactively.

6. **Size the ingester's replication and WAL settings for durability**
   in a scaled (non-single-binary) deployment:
   ```yaml
   ingester:
     wal:
       enabled: true
       dir: /loki/wal
     lifecycler:
       ring:
         replication_factor: 3
     chunk_idle_period: 30m
     chunk_target_size: 1572864   # ~1.5MB compressed target per chunk
     max_chunk_age: 2h
   ```
   `replication_factor: 3` (typical) means each stream's data is written
   to 3 ingesters before being acknowledged, so a single ingester pod
   loss doesn't lose in-flight (not-yet-flushed-to-storage) log data;
   the WAL protects against loss during ingester restarts specifically.

7. **Confirm ingestion is actually flowing and within limits** after
   deploying:
   ```bash
   curl -s http://<LOKI>/ready
   curl -s http://<LOKI>/metrics | grep -E 'loki_ingester_streams_created_total|loki_discarded_samples_total'
   ```
   A rising `loki_discarded_samples_total` counter (with a `reason`
   label such as `rate_limited`, `stream_limit`, or `line_too_long`)
   means logs are being silently dropped at ingestion — check that
   reason against the `limits_config` values in step 3 before assuming
   the shipper is misbehaving.

## Best practices

- Treat label design as a schema decision made once, deliberately, up
  front — retrofitting a high-cardinality label out of an already-large
  deployment means a slow migration, not a quick config edit.
- Set `max_streams_per_user` and per-stream rate limits explicitly rather
  than relying on defaults meant for evaluation-scale deployments —
  defaults that are too generous let one misbehaving app degrade the
  shared cluster for everyone.
- Enable the compactor with `retention_enabled: true` from day one, even
  if the initial retention period is generous — discovering retention
  was never actually enforced after months of unbounded storage growth
  is an expensive mistake to unwind.
- Prefer TSDB over the older `boltdb-shipper` index store for any new
  deployment — it has better query performance and is the schema Loki
  development is focused on going forward.
- Choose simple-scalable mode as the default production target on
  Kubernetes rather than jumping straight to full microservices mode —
  most teams never need the extra operational surface area
  microservices mode adds.
- Monitor `loki_discarded_samples_total` by `reason` as a standing
  dashboard panel/alert, not just when someone reports missing logs —
  silent ingestion drops are otherwise invisible until someone notices
  gaps during an actual investigation.
- Validate any schema/limits/label change against
  [loki-configuration-validation](../loki-configuration-validation/SKILL.md)
  before deploying — a bad schema config or an overly permissive limit
  is much cheaper to catch pre-deploy than to unwind after ingestion has
  already been running against it.

## Common pitfalls

- **Symptom:** Loki's storage (object storage bucket, or local disk in a
  small deployment) grows without bound despite a `retention_period`
  being set in config.
  **Fix:** `retention_period` alone does nothing without the compactor
  running with `retention_enabled: true` and `delete_request_store`
  configured — confirm the compactor component is actually deployed and
  its logs show retention sweeps running, not just that the config value
  exists.

- **Symptom:** A specific application's logs start being rejected with
  `429`/`per-stream rate limit exceeded` shortly after a deploy, even
  though overall log volume looks normal.
  **Fix:** That app likely just started emitting a new high-cardinality
  label (a new field promoted to a label, or a bug causing a unique value
  per pod/request), pushing one stream's rate past
  `per_stream_rate_limit`. Check `loki_discarded_samples_total{reason=
  "per_stream_rate_limit"}` and the app's label set — fix the label
  design at the source rather than raising the limit to accommodate
  runaway cardinality.

- **Symptom:** Loki ingesters intermittently lose recent (not-yet-
  flushed) log data during pod restarts/rolling upgrades.
  **Fix:** The write-ahead log (WAL) wasn't enabled, or its volume isn't
  actually persistent (e.g. backed by ephemeral storage in Kubernetes
  instead of a PersistentVolume). Enable `ingester.wal.enabled: true`
  with a real persistent volume backing `wal.dir`, and confirm
  `replication_factor` is set high enough that a single ingester's loss
  doesn't lose data outright.

- **Symptom:** Query performance degrades badly over time as log volume
  grows, even though ingestion itself keeps up fine.
  **Fix:** Often an artifact of the older `boltdb-shipper` index store
  under sustained high stream counts, or `max_streams_per_user` being set
  far higher than the label design actually needs. Migrate to TSDB via a
  new `schema_config` entry (never edit the old one) and re-audit label
  cardinality.

- **Symptom:** After adding S3 as the storage backend, existing
  historical logs ingested under the previous (e.g. filesystem or GCS)
  backend become unqueryable.
  **Fix:** A `storage_config`/`object_store` change was made by editing
  the existing `schema_config.configs` entry in place instead of adding a
  new entry with a future `from:` date. Add the new backend as a new
  dated schema config entry so historical data continues to be read from
  its original store while new data lands in the new one.

- **Symptom:** A single noisy tenant/team in a multi-tenant Loki cluster
  degrades query latency for every other tenant.
  **Fix:** Per-tenant `limits_config` overrides weren't set, so one
  tenant's oversized queries/high stream count consume shared querier
  resources. Set per-tenant overrides (query concurrency, max streams,
  ingestion rate) in the runtime overrides config rather than a single
  global limit meant to be "generous enough for everyone."

## Worked example

**Scenario:** Standing up Loki on Kubernetes in simple-scalable mode for
a multi-team platform, backed by S3, with a 30-day default retention and
a stricter cardinality ceiling after an earlier incident where a team's
new field caused stream-count explosion.

```yaml
# values.yaml (loki-simple-scalable Helm chart, excerpted)
loki:
  auth_enabled: true
  commonConfig:
    replication_factor: 3
  schemaConfig:
    configs:
      - from: 2026-01-01
        store: tsdb
        object_store: s3
        schema: v13
        index:
          prefix: loki_index_
          period: 24h
  storageConfig:
    aws:
      region: <AWS_REGION>
      bucketnames: <S3_BUCKET_NAME>
  limits_config:
    ingestion_rate_mb: 15
    ingestion_burst_size_mb: 30
    per_stream_rate_limit: 5MB
    per_stream_rate_limit_burst: 15MB
    max_streams_per_user: 5000
    retention_period: 720h
  compactor:
    retention_enabled: true
    delete_request_store: s3

write:
  replicas: 3
read:
  replicas: 3
```

Runtime overrides give the `payments` tenant a longer retention window
for compliance without changing the cluster-wide default:

```yaml
overrides:
  "payments":
    retention_period: 2160h
```

After rollout, `loki_discarded_samples_total{reason="per_stream_rate_
limit"}` is added as a standing Grafana panel per team namespace so a
repeat of the earlier cardinality incident surfaces immediately instead
of being discovered days later during a query-performance complaint.

## Cross-references

- [loki-configuration-validation](../loki-configuration-validation/SKILL.md) — validating this exact config (limits, schema) before deploying, to catch ingestion-rejecting mistakes pre-rollout.
- [logql-query-authoring](../logql-query-authoring/SKILL.md) — writing queries against logs ingested here; label design decisions made in this skill directly determine what's cheap versus expensive to query.
- [fluent-bit-log-forwarding-configuration](../fluent-bit-log-forwarding-configuration/SKILL.md) — configuring a shipper to push logs into this Loki instance's ingestion API.
- [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md) — provisioning the Grafana datasource this Loki instance is queried through, and where `loki_discarded_samples_total` alerting rules would be wired.
