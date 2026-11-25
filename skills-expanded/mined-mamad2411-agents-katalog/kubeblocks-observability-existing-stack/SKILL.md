---
name: kubeblocks-observability-existing-stack
version: "0.1.0"
description: Integrate KubeBlocks database metrics into an existing Prometheus / Grafana stack. Use this when the monitoring base already exists and the remaining work is scrape configuration, dashboards, and alerting readiness.
---

# KubeBlocks Observability: Existing Stack

Use this path when Prometheus or Grafana already exists in the environment and the task is to **integrate** database metrics, not bootstrap a new monitoring stack.

## Output Contract

Always state which readiness level has been reached:

- `metrics-ready`
- `scrape-ready`
- `dashboard-ready`
- `alerting-ready`

Do not claim "monitoring is done" unless the achieved level matches the user's expectation.

## Workflow

```text
- [ ] Step 1: Confirm the existing monitoring stack
- [ ] Step 2: Verify exporter / metrics endpoints
- [ ] Step 3: Add scrape configuration
- [ ] Step 4: Confirm dashboards / alerts if requested
```

## Step 1: Confirm The Existing Stack

```bash
kubectl get pods -A | grep -E 'prometheus|grafana' || true
kubectl get servicemonitor,podmonitor -A 2>/dev/null || true
```

Answer:

- where Prometheus lives
- whether Grafana already exists
- whether the environment uses `ServiceMonitor` or `PodMonitor`

## Step 2: Verify Exporter / Metrics Endpoints

```bash
kubectl get pods -n <ns> -l app.kubernetes.io/managed-by=kubeblocks
kubectl describe pod -n <ns> <pod-name> | grep -A2 -E 'http-metrics|metrics' || true
```

If exporter pods or `http-metrics` endpoints do not exist, stop and say observability is not yet `metrics-ready`.

## Step 3: Add Scrape Configuration

For Prometheus Operator, prefer `ServiceMonitor` / `PodMonitor` aligned with the existing stack's label conventions.

Example `PodMonitor`:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kb-database-monitor
  namespace: monitoring
spec:
  namespaceSelector:
    matchNames:
      - <db-namespace>
  selector:
    matchLabels:
      app.kubernetes.io/managed-by: kubeblocks
  podMetricsEndpoints:
    - port: http-metrics
      path: /metrics
      interval: 30s
```

If scrape config exists and Prometheus targets are healthy, the result is at least `scrape-ready`.

## Step 4: Confirm Dashboards / Alerts

Only claim `dashboard-ready` when:

- Grafana exists
- the dashboard data source is wired correctly
- the user can actually open a dashboard for the database

Only claim `alerting-ready` when alert rules are configured and routed to a real notification path.
