---
name: log-patterns
description: "Log management patterns: a Fluent Bit DaemonSet for Kubernetes, the Loki stack with Helm, LogQL queries, OpenSearch index templates, Grafana alerts from Loki logs, and log sampling with Vector. Use when building log collection, retention, or log-based alerting."
---

# Log Management Patterns

Structured log formats, collection pipelines, retention policies, and log-based alerting.

## Fluent Bit DaemonSet for Kubernetes

```yaml
# fluent-bit-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
  namespace: logging
spec:
  selector:
    matchLabels: {app: fluent-bit}
  template:
    metadata:
      labels: {app: fluent-bit}
      annotations:
        # Prometheus scrape
        prometheus.io/scrape: "true"
        prometheus.io/port: "2020"
        prometheus.io/path: "/api/v1/metrics/prometheus"
    spec:
      serviceAccountName: fluent-bit
      tolerations:
        - key: node-role.kubernetes.io/control-plane
          effect: NoSchedule
      containers:
        - name: fluent-bit
          image: fluent/fluent-bit:3.1
          resources:
            requests: {cpu: 50m, memory: 50Mi}
            limits: {cpu: 200m, memory: 200Mi}
          ports:
            - containerPort: 2020  # Metrics
          volumeMounts:
            - name: varlog
              mountPath: /var/log
            - name: config
              mountPath: /fluent-bit/etc/
          env:
            - name: OPENSEARCH_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: opensearch-credentials
                  key: password
      volumes:
        - name: varlog
          hostPath: {path: /var/log}
        - name: config
          configMap: {name: fluent-bit-config}

---
# RBAC for Kubernetes metadata enrichment
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fluent-bit
rules:
  - apiGroups: [""]
    resources: [pods, namespaces]
    verbs: [get, list, watch]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: fluent-bit
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: fluent-bit
subjects:
  - kind: ServiceAccount
    name: fluent-bit
    namespace: logging
```

## Loki Stack with Helm

```bash
# Install Loki stack (Loki + Promtail + Grafana)
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install loki-stack grafana/loki-stack \
  --namespace monitoring \
  --create-namespace \
  --set loki.enabled=true \
  --set promtail.enabled=true \
  --set grafana.enabled=false \  # Use existing Grafana
  --values - << 'EOF'
loki:
  storage:
    type: s3
    s3:
      endpoint: s3.us-east-1.amazonaws.com
      bucketnames: loki-chunks-prod
      region: us-east-1
      s3forcepathstyle: false
  serviceAccount:
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT:role/loki-s3-role
  config:
    limits_config:
      retention_period: 30d
      ingestion_rate_mb: 32
      ingestion_burst_size_mb: 64
      max_query_series: 500

promtail:
  config:
    clients:
      - url: http://loki-stack:3100/loki/api/v1/push
    snippets:
      extraRelabelConfigs:
        - source_labels: [__meta_kubernetes_pod_annotation_fluentbit_io_exclude]
          action: drop
          regex: "true"
EOF
```

## LogQL Queries (Loki)

```logql
# All error logs from payment service in last 15m
{app="payment-api", namespace="production"} |= "ERROR"

# Parse JSON and filter by HTTP status
{app="api", namespace="production"}
  | json
  | http_status >= 500
  | line_format "{{.level}} {{.message}} status={{.http_status}}"

# Count error rate per service (metric query)
sum by (app) (
  rate({namespace="production"} |= "ERROR" [5m])
)

# P99 request duration from structured logs
quantile_over_time(0.99,
  {app="api"} | json | unwrap duration_ms [5m]
) by (app)

# Find slow queries (>1s)
{app="api"} | json | duration_ms > 1000

# Log-based alert: >5 errors/min triggers alert
sum(rate({app="payment-api", namespace="production"} |= "ERROR" [1m])) > 5
```

## OpenSearch Index Template

```bash
# Index template for log indices
curl -X PUT "https://opensearch:9200/_index_template/logs" \
  -H "Content-Type: application/json" -d '
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-policy",
      "index.codec": "best_compression",
      "index.refresh_interval": "30s"
    },
    "mappings": {
      "dynamic_templates": [
        {
          "strings_as_keyword": {
            "match_mapping_type": "string",
            "mapping": {"type": "keyword", "ignore_above": 256}
          }
        }
      ],
      "properties": {
        "@timestamp": {"type": "date"},
        "message": {"type": "text"},
        "level": {"type": "keyword"},
        "service": {"type": "keyword"},
        "trace_id": {"type": "keyword"},
        "span_id": {"type": "keyword"},
        "duration_ms": {"type": "long"},
        "http": {
          "type": "object",
          "properties": {
            "status": {"type": "short"},
            "method": {"type": "keyword"},
            "path": {"type": "keyword"}
          }
        }
      }
    }
  }
}'
```

## Grafana Alert from Loki Logs

```yaml
# Grafana alert rule (via Terraform)
resource "grafana_rule_group" "log_alerts" {
  name             = "log-error-alerts"
  folder_uid       = grafana_folder.alerts.uid
  interval_seconds = 60

  rule {
    name      = "High Error Rate"
    condition = "C"

    data {
      ref_id = "A"
      datasource_uid = "loki-uid"
      model = jsonencode({
        expr = "sum(rate({app=\"payment-api\",namespace=\"production\"} |= \"ERROR\" [5m]))"
      })
    }

    data {
      ref_id     = "C"
      datasource_uid = "__expr__"
      model = jsonencode({
        type       = "threshold"
        conditions = [{evaluator = {params = [0.1], type = "gt"}}]
      })
    }

    annotations = {
      summary     = "High error rate in {{ $labels.app }}"
      description = "Error rate: {{ $values.A.Value | humanize }} errors/sec"
      runbook_url = "https://wiki.example.com/runbooks/high-error-rate"
    }

    no_data_state  = "NoData"
    exec_err_state = "Error"
    for            = "5m"
  }
}
```

## Log Sampling with Vector

```toml
# vector.toml: sample debug logs, keep all errors
[transforms.level_router]
type = "route"
inputs = ["kubernetes"]
[transforms.level_router.route]
  debug = '.level == "debug" || .level == "trace"'
  important = '.level == "error" || .level == "warn" || .level == "info"'

[transforms.sample_debug]
type = "sample"
inputs = ["level_router.debug"]
rate = 20   # Keep 1 in 20 debug/trace logs

[sinks.loki]
type = "loki"
inputs = ["sample_debug", "level_router.important"]
endpoint = "http://loki:3100"
[sinks.loki.labels]
  app = "{{ kubernetes.pod_labels.app }}"
  namespace = "{{ kubernetes.pod_namespace }}"
  level = "{{ level }}"
```
