---
name: infra-prometheus-grafana
description: Use when building observability with Prometheus + Grafana — scrape configs, recording rules, alerting, dashboard provisioning as code.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [observability-essentials, infra-docker-compose, infra-docker-swarm]
---

# Infra Prometheus + Grafana

**Iron Law: dashboards are CODE in git, NEVER clicked in the UI. Apply RED for services, USE for resources. Every alert has a runbook URL and bounded cardinality — high-cardinality labels are how you DOS Prometheus.**

## What goes where

| Component        | Role                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| **Prometheus**   | pull-based metrics scrape, TSDB, recording rules, evaluates alert rules                           |
| **Alertmanager** | dedupes/routes/silences alerts; sends to PagerDuty/Slack/email                                    |
| **Grafana**      | dashboards on top of Prometheus (and other DS); provisioned from files                            |
| **Exporters**    | expose metrics for non-instrumented systems (node_exporter, postgres_exporter, blackbox_exporter) |
| **Push gateway** | for short-lived jobs only — NOT a general push endpoint                                           |

For push-based or high cardinality: VictoriaMetrics, Mimir, Thanos — same PromQL.

## prometheus.yml

```yaml
global:
  scrape_interval: 30s # 15-60s typical; lower = more storage
  evaluation_interval: 30s
  external_labels: { cluster: prod-eu, region: eu-west-1 }

rule_files:
  - /etc/prometheus/rules/*.yml

alerting:
  alertmanagers:
    - static_configs:
        - targets: [alertmanager:9093]

scrape_configs:
  - job_name: api
    metrics_path: /metrics
    static_configs:
      - targets: [api:8080]
        labels: { service: api, env: prod }

  - job_name: node
    static_configs:
      - targets: [node1:9100, node2:9100]

  - job_name: postgres
    static_configs:
      - targets: [pg_exporter:9187]

  # Service discovery — Docker Swarm
  # WARNING: mounting /var/run/docker.sock = root on the host (anyone with sock
  # access can `docker run --privileged`). Use a read-only socket proxy
  # (e.g. tecnativa/docker-socket-proxy with TASKS=1, SERVICES=1) instead of
  # the raw socket in any production deployment.
  - job_name: swarm
    dockerswarm_sd_configs:
      - host: tcp://docker-socket-proxy:2375 # not unix:///var/run/docker.sock
        role: tasks
    relabel_configs:
      - source_labels: [__meta_dockerswarm_task_desired_state]
        regex: running
        action: keep
```

Scrape endpoints exposing `/metrics` reveal internal topology, queue depths, latencies. Bind them to a non-public interface or require auth (`basic_auth: { username: prom, password_file: /etc/prometheus/scrape-token }` or `authorization: { type: Bearer, credentials_file: ... }`) when crossing trust boundaries.

`scrape_interval`: 30s default, 15s for hot services, 60s+ for batch.

## RED vs USE — which to apply where

| Method                           | What                                 | Use for                                |
| -------------------------------- | ------------------------------------ | -------------------------------------- |
| **RED**                          | Rate, Errors, Duration               | services (HTTP, gRPC, queue workers)   |
| **USE**                          | Utilization, Saturation, Errors      | resources (CPU, memory, disk, network) |
| Four golden signals (Google SRE) | latency, traffic, errors, saturation | same idea, slightly different framing  |

Per service: `http_requests_total{method, path, status}` + `http_request_duration_seconds_bucket` (histogram) + `http_inflight_requests`. Per host: `node_exporter` covers USE.

## Recording rules — pre-compute expensive queries

```yaml
groups:
  - name: api-red
    interval: 30s
    rules:
      - record: api:http_requests:rate5m
        expr: sum by (status, path) (rate(http_requests_total{service="api"}[5m]))

      - record: api:http_errors_ratio:rate5m
        expr: |
          sum by (path) (rate(http_requests_total{service="api",status=~"5.."}[5m]))
          /
          sum by (path) (rate(http_requests_total{service="api"}[5m]))

      - record: api:http_duration_p99:rate5m
        expr: histogram_quantile(0.99, sum by (le, path) (rate(http_request_duration_seconds_bucket{service="api"}[5m])))
        # Native histogram (Prom 2.40+, OTel default): drop `le`, target `..._seconds` not `..._bucket`
```

Naming convention: `<service>:<metric>:<window>` (same suffix everywhere). Dashboards + alerts query the recorded series — fast and consistent.

## Alerts — every one has a runbook

```yaml
groups:
  - name: api-alerts
    rules:
      - alert: APIHighErrorRate
        expr: api:http_errors_ratio:rate5m > 0.05
        for: 10m
        labels: { severity: page, team: platform }
        annotations:
          summary: "API 5xx ratio > 5% for 10m on {{ $labels.path }}"
          runbook_url: "https://runbooks.example.com/api/high-error-rate"
```

`for: 10m` prevents flap-pages. `severity` routes via Alertmanager. **No runbook = no alert.**

## Grafana — provisioned, not clicked

```yaml
# /etc/grafana/provisioning/datasources/prom.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090 # use https:// + tlsAuth across hosts; plain HTTP only safe over single-host Docker network
    access: proxy
    isDefault: true
```

```yaml
# /etc/grafana/provisioning/dashboards/dash.yml
apiVersion: 1
providers:
  - name: file
    type: file
    folder: Services
    updateIntervalSeconds: 30
    options:
      path: /etc/grafana/dashboards
```

Dashboards live as JSON in `/etc/grafana/dashboards/*.json` — committed to git. Built-in dashboards imported once, saved to the same path. Never edit-and-save in UI without committing the JSON back.

## Grafana variables

```jsonc
"templating": {
  "list": [
    { "name": "service", "datasource": "Prometheus", "query": "label_values(up, service)", "current": {...} },
    { "name": "env", "type": "constant", "current": {"value": "prod"} }
  ]
}
```

Variables drive `$service`, `$env` in panels. One dashboard, many slices.

## Cardinality — the killer

Every unique combination of label values = a new time series. `http_requests_total{user_id="123"}` × 10M users = OOM.

| Safe label (bounded)                                                  | Unsafe label (unbounded)                                                            |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `method`, `status`, `service`, `env`, `region`, `error_type` taxonomy | `user_id`, `request_id`, raw path (`/users/123`), session token, error message text |

Per-user data → logs, not metrics. Trace data → Tempo/Jaeger.

## Anti-patterns

- Dashboards clicked in UI, never exported (lost on Grafana reinstall)
- Alerts without `runbook_url`; `for: 0s` (flap-storms); no meta-monitoring on Prom itself
- High-cardinality labels (`user_id`, raw paths); `scrape_interval: 5s` everywhere (TSDB explodes)
- Push gateway for long-lived services (it's for short-lived batch only)
- Mixing recording-rule names with raw metric names — adopt `<service>:<metric>:<window>`
- Grafana panels with `$__interval` ignored at long ranges; one Alertmanager (cluster 2+)
- Mounting raw `/var/run/docker.sock` into Prometheus (use a socket proxy)

## Red flags

| Thought                                   | Reality                                                   |
| ----------------------------------------- | --------------------------------------------------------- |
| "I'll label by user_id, what's the harm?" | Cardinality explosion; Prom OOMs                          |
| "I saved the dashboard in Grafana"        | Not in git = not real                                     |
| "Our SLO is p99 < 100ms"                  | Without recording rules + wired alerts, it's aspirational |

## Hand-off

Instrumenting services (counters, histograms, OTel): `Skill(observability-essentials)`. Deploying this stack: `Skill(infra-docker-compose)` / `Skill(infra-docker-swarm)`. At-scale concerns — native histograms, `remote_write` to Mimir/Thanos, federation, Alertmanager routing, scrape-time cardinality dropping, PromQL traps: `references/prometheus-scale.md`.
