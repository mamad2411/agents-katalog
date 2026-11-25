---
name: observability-patterns
description: "Observability patterns: kube-prometheus-stack install, OpenTelemetry Collector configuration, Thanos sidecar and query for multi-cluster long-term storage, Grafana dashboard provisioning, and SLO error budget tracking. Use when setting up monitoring or defining SLOs."
---

# Observability Patterns

Prometheus stack, SLO alerting, OpenTelemetry collector, Grafana dashboards, and Thanos for long-term storage.

## kube-prometheus-stack Helm Install

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --values - << 'EOF'
prometheus:
  prometheusSpec:
    retention: 15d
    retentionSize: "50GB"
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: gp3
          resources:
            requests:
              storage: 100Gi
    # Scrape custom PodMonitors/ServiceMonitors from all namespaces
    podMonitorSelectorNilUsesHelmValues: false
    serviceMonitorSelectorNilUsesHelmValues: false
    ruleSelectorNilUsesHelmValues: false
    # Resource limits
    resources:
      requests: {cpu: 500m, memory: 2Gi}
      limits: {cpu: 2, memory: 8Gi}

grafana:
  adminPassword: "${GRAFANA_PASSWORD}"
  persistence:
    enabled: true
    size: 10Gi
  grafana.ini:
    server:
      root_url: https://grafana.example.com
    auth.github:
      enabled: true
      allow_sign_up: true
      client_id: "${GITHUB_CLIENT_ID}"
      client_secret: "${GITHUB_CLIENT_SECRET}"
      allowed_organizations: my-org

alertmanager:
  config:
    global:
      slack_api_url: "${SLACK_WEBHOOK_URL}"
    route:
      group_by: [alertname, cluster, service]
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 12h
      receiver: slack-critical
      routes:
        - match: {severity: warning}
          receiver: slack-warning
        - match: {severity: critical}
          receiver: pagerduty
    receivers:
      - name: slack-critical
        slack_configs:
          - channel: "#alerts-critical"
            title: '{{ .GroupLabels.alertname }}'
            text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
      - name: pagerduty
        pagerduty_configs:
          - service_key: "${PAGERDUTY_SERVICE_KEY}"
EOF
```

## OpenTelemetry Collector

```yaml
# otel-collector-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
  namespace: monitoring
data:
  config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
      # Scrape Prometheus metrics from collector itself
      prometheus:
        config:
          scrape_configs:
            - job_name: otel-collector
              scrape_interval: 30s
              static_configs:
                - targets: [localhost:8888]

    processors:
      batch:
        timeout: 10s
        send_batch_size: 1000
      memory_limiter:
        limit_percentage: 75
        check_interval: 1s
      # Add Kubernetes attributes to all signals
      k8sattributes:
        auth_type: serviceAccount
        extract:
          metadata: [k8s.namespace.name, k8s.pod.name, k8s.deployment.name]
          labels:
            - tag_name: app
              key: app
      # Sample: keep 10% of debug-level traces
      tail_sampling:
        decision_wait: 10s
        policies:
          - name: errors-always
            type: status_code
            status_code: {status_codes: [ERROR]}
          - name: slow-traces
            type: latency
            latency: {threshold_ms: 1000}
          - name: probabilistic-sample
            type: probabilistic
            probabilistic: {sampling_percentage: 10}

    exporters:
      otlp/tempo:
        endpoint: http://tempo:4317
        tls: {insecure: true}
      prometheus:
        endpoint: 0.0.0.0:8889
      loki:
        endpoint: http://loki:3100/loki/api/v1/push

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, k8sattributes, tail_sampling, batch]
          exporters: [otlp/tempo]
        metrics:
          receivers: [otlp, prometheus]
          processors: [memory_limiter, k8sattributes, batch]
          exporters: [prometheus]
        logs:
          receivers: [otlp]
          processors: [memory_limiter, k8sattributes, batch]
          exporters: [loki]
```

## Thanos Sidecar + Query (Multi-cluster Long-term Storage)

```yaml
# prometheus-with-thanos-sidecar.yaml (add to Prometheus StatefulSet)
containers:
  - name: prometheus
    image: prom/prometheus:v2.51.0
    args:
      - --config.file=/etc/prometheus/prometheus.yml
      - --storage.tsdb.path=/prometheus
      - --storage.tsdb.min-block-duration=2h    # Required for Thanos
      - --storage.tsdb.max-block-duration=2h    # Required for Thanos
      - --web.enable-lifecycle

  - name: thanos-sidecar
    image: quay.io/thanos/thanos:v0.35.0
    args:
      - sidecar
      - --prometheus.url=http://localhost:9090
      - --tsdb.path=/prometheus
      - --grpc-address=0.0.0.0:10901
      - --http-address=0.0.0.0:10902
      - --objstore.config-file=/etc/thanos/objstore.yaml
    volumeMounts:
      - name: prometheus-data
        mountPath: /prometheus
      - name: thanos-config
        mountPath: /etc/thanos

---
# Thanos object store config
apiVersion: v1
kind: Secret
metadata:
  name: thanos-objstore-config
type: Opaque
stringData:
  objstore.yaml: |
    type: S3
    config:
      bucket: thanos-metrics-prod
      endpoint: s3.us-east-1.amazonaws.com
      region: us-east-1
      sse_config:
        type: SSE-S3

---
# Thanos Query (unified query across clusters)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: thanos-query
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: thanos-query
          image: quay.io/thanos/thanos:v0.35.0
          args:
            - query
            - --http-address=0.0.0.0:10902
            - --store=thanos-sidecar-cluster1:10901
            - --store=thanos-sidecar-cluster2:10901
            - --store=thanos-store-gateway:10901
            - --query.replica-label=prometheus_replica
            - --query.auto-downsampling
```

## Grafana Dashboard Provisioning

```yaml
# grafana-dashboards-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards
  namespace: monitoring
  labels:
    grafana_dashboard: "1"  # Label picked up by Grafana sidecar
data:
  golden-signals.json: |
    {
      "title": "Golden Signals",
      "uid": "golden-signals",
      "panels": [
        {
          "title": "Request Rate",
          "type": "stat",
          "targets": [{
            "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[5m]))",
            "legendFormat": "req/s"
          }]
        },
        {
          "title": "Error Rate",
          "type": "timeseries",
          "targets": [{
            "expr": "sum(rate(http_requests_total{status=~\"5..\",namespace=\"$namespace\"}[5m])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[5m]))",
            "legendFormat": "error rate"
          }]
        },
        {
          "title": "P99 Latency",
          "type": "timeseries",
          "targets": [{
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[5m])) by (le))",
            "legendFormat": "p99"
          }]
        }
      ]
    }
```

## SLO Error Budget Tracking

```promql
# Remaining error budget (30d window, 99.9% SLO)
# 1 = full budget remaining, 0 = exhausted
1 - (
  sum(increase(http_requests_total{job="myapp", status=~"5.."}[30d]))
  /
  (sum(increase(http_requests_total{job="myapp"}[30d])) * 0.001)
)

# Budget burn rate (current consumption rate relative to target)
# 1.0 = burning at exactly the rate to exhaust budget in 30d
# 14.4 = would exhaust in 50h (Google's 5% in 1h threshold)
(
  sum(rate(http_requests_total{job="myapp", status=~"5.."}[1h]))
  /
  sum(rate(http_requests_total{job="myapp"}[1h]))
) / 0.001
```
