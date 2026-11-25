---
name: logging-monitoring
description: "Configure observability on GCP using Cloud Logging, Cloud Monitoring, Cloud Trace, and Cloud Profiler. Covers log sinks, log-based metrics, alerting policies, dashboards, and uptime checks. Owns the operational readiness evidence for gcp-ops. Use when the user mentions: logging setup, monitoring setup, alerting policy, dashboard GCP, error reporting, SLO monitoring. Use this to configure the observability resources themselves; use gcp-ops instead for SLO targets, runbooks and release gating."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "cloud logging, cloud monitoring, logging setup, monitoring setup, alerting policy, log sink, dashboard GCP, uptime check, cloud trace, error reporting, log-based metric, SLO monitoring"
  "googlecloud-plugin/required-scopes": "logging.sinks.create, logging.sinks.get, logging.logMetrics.create, monitoring.alertPolicies.create, monitoring.dashboards.create, monitoring.uptimeCheckConfigs.create"
  "googlecloud-plugin/mcp-servers": "google-logging, google-monitoring"
---

# Logging + Monitoring

Full observability stack for GCP workloads: Cloud Logging, Cloud Monitoring, Cloud Trace, and Cloud Profiler.

## Core Patterns

### Create a log sink (export to BigQuery for long-term retention)

```bash
gcloud logging sinks create SINK_NAME \
  bigquery.googleapis.com/projects/PROJECT_ID/datasets/DATASET \
  --log-filter='resource.type="cloud_run_revision"' \
  --project=PROJECT_ID
```

### Create a log-based metric (count errors)

```bash
gcloud logging metrics create error-rate \
  --description="Count of ERROR log entries" \
  --log-filter='severity=ERROR' \
  --project=PROJECT_ID
```

### Create an alerting policy (notify on error spike)

```bash
# Best done via Terraform or Console for complex conditions
# CLI example for uptime check failure:
gcloud alpha monitoring policies create \
  --policy-from-file=alerting-policy.json \
  --project=PROJECT_ID
```

### Uptime check

```bash
gcloud monitoring uptime create \
  --display-name="Service Health Check" \
  --resource-type=uptime-url \
  --hostname=SERVICE_URL \
  --path=/ \
  --project=PROJECT_ID
```

## Golden Signal Queries (Cloud Logging)

```
# 5xx errors on Cloud Run
resource.type="cloud_run_revision"
severity=ERROR

# Latency > 2s (requires structured logging with latency field)
resource.type="cloud_run_revision"
httpRequest.latency>"2s"

# GKE OOMKilled events
resource.type="k8s_container"
jsonPayload.reason="OOMKilling"
```

## Safety Rules

- **Log sinks can incur cost.** Exporting logs to BigQuery, Cloud Storage, or Pub/Sub bills for storage and, in BigQuery's case, for queries over the exported data. Scope every sink with a tight `--log-filter` — never export `severity>=DEFAULT` (i.e. everything) to a billable destination without intent.
- **Scope log filters narrowly.** Broad filters (no `resource.type`, no `severity`) match high-volume logs and drive both ingestion and export cost. Always pin `resource.type` and the minimum `severity` you need.
- **Exclusion filters reduce ingestion cost.** Use log exclusions to drop high-volume, low-value logs (e.g. health-check 200s) before they are ingested and billed.
- **Never log secrets.** Application logs routed to Cloud Logging are readable by anyone with `roles/logging.viewer`. Redact tokens, keys, and PII at the source; do not rely on downstream filtering.
- **Retention has a cost curve.** Default retention is free to a point; extended retention on `_Default`/custom buckets bills per GB. Set retention deliberately per bucket.

## References

- [Cloud Logging Overview](https://cloud.google.com/logging/docs/overview)
- [Cloud Monitoring Overview](https://cloud.google.com/monitoring/docs/monitoring-overview)
- [Cloud Trace Overview](https://cloud.google.com/trace/docs/overview)
- [Log-based Metrics](https://cloud.google.com/logging/docs/logs-based-metrics)
- [Error Reporting](https://cloud.google.com/error-reporting/docs)
