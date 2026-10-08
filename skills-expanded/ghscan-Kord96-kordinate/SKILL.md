---
name: design-monitoring
description: >
  Implement monitoring for a project by consuming augur's monitoring-spec.yaml.
  Produces Grafana dashboard JSON, Prometheus alert rules, and validates that
  the running service emits the expected metrics. Aligns with the infra-atlas
  new_workload_contract for observability.
argument-hint: "<project> [--scope full|dashboards|alerts|validate] [--dry-run]"
---

Implement a monitoring system for a project from augur's monitoring spec. Augur designs the spec (metrics, alerts, dashboards); sauron implements it as concrete Grafana JSON, Prometheus rules, and validates live metric emission.

## Arguments

`$ARGUMENTS` — Required: `<project>`. Optional:
- `--scope full|dashboards|alerts|validate` — focus on a specific area (default: full)
- `--dry-run` — generate configs but do not push to Grafana or apply alert rules

## Input: Augur's monitoring-spec.yaml

This skill consumes the monitoring spec that augur produces during `/design --approve`.
The spec follows this schema:

```yaml
version: "1"
project: <name>
generated_from: design-atlas.json
metrics:
  - name: <metric_name>
    type: counter|gauge|histogram
    labels: [<labels>]
    source_pattern: <pattern-name>
    description: <what it measures>
alerts:
  - name: <alert_name>
    condition: <PromQL expression>
    severity: critical|warning
    source_pattern: <pattern-name>
dashboards:
  - name: <dashboard_name>
    panels: [<metric references>]
```

### How to locate the spec

The daemon injects artifact paths into the job prompt. Look for:

```
[Artifacts] monitoring-spec: <path>
```

Resolution order:
1. **Artifact path** — if the prompt contains `[Artifacts] monitoring-spec:`, read the file at that path. This is the primary mechanism when augur delegates to sauron after `/design --approve`.
2. **Augur project memory** — if no artifact path, read from `/kord/agents/augur/memory/projects/<project>/monitoring-spec.yaml`.
3. **Fail** — if neither exists, report that no monitoring spec is available and ask the user to run `augur /design <project> --approve` first.

## Dependencies

1. **Augur** — provides monitoring-spec.yaml (input) and atlas.json (architectural context).
   - Atlas at `/kord/agents/augur/memory/projects/<project>/atlas.json` provides: components, flows, failure modes, external dependencies.
   - If atlas exists, use it to enrich dashboard panels and alert annotations.

2. **Charon/Alfred** — cluster access for live validation:
   ```
   /kord alfred get config <cluster>
   ```
   Provides: Tailscale IPs, namespaces, service ports, kubeconfig context.

3. **Infra-atlas contract** — read from `$AGENT_PROJECT_DIR/memory/global/infra-atlas.json` (if available). The `new_workload_contract` section defines observability requirements all workloads must satisfy:
   - `health`: readiness and liveness endpoints (`GET /health`)
   - `metrics`: Prometheus endpoint (`/metrics`, prometheus format)
   - `logging`: stdout, JSON format
   - `labels`: `app: <name>` on all pods
   All generated configs must align with these contract requirements.

4. **Sauron monitoring model** — follow the two-layer model from `memory/monitoring.md`:
   - **Alloy layer**: pod-level collection (infra metrics via cAdvisor, app metrics via `/metrics` scrape, logs via stdout)
   - **Vitals layer**: app-level health evaluation (health gauges: 0=FAIL/1=WARNING/2=OK, derived metrics)
   Generated dashboards and alerts must target the correct layer.

## Procedure

### Step 1 — Load the monitoring spec

Parse the monitoring-spec.yaml using the resolution order above. Validate:
- `version` is `"1"`
- `metrics` array is non-empty
- Each metric has `name`, `type`, and `description`
- Each alert has `name`, `condition`, and `severity`

Also load:
- Atlas (`/kord/agents/augur/memory/projects/<project>/atlas.json`) for component context
- Infra-atlas (`$AGENT_PROJECT_DIR/memory/global/infra-atlas.json`) for contract requirements
- Existing observability catalog (`$MEM/observability-catalog.yaml`) from a previous `/monitor` scan, if available

### Step 2 — Generate Grafana dashboard JSON

For each dashboard entry in the spec, produce a complete Grafana dashboard JSON file.

**Overview dashboard** (always generated):
- Title: `<project> Overview`
- Rows: one per component group (from atlas groups, or one row per spec dashboard)
- Panels per row:
  - Request rate (counter metrics with `rate()`)
  - Error rate (counter metrics filtered by error status)
  - Latency (histogram metrics with `histogram_quantile()`)
  - Saturation (gauge metrics for resource utilization)
- Variables: `$namespace`, `$app` (pre-filled from project name)
- Datasource: `Prometheus` (uid: use cluster default)

**Vitals dashboard** (generated if vitals metrics are in the spec):
- Title: `<project> Vitals`
- Health gauge panels: stat panels showing 0/1/2 state with value mappings (FAIL/WARNING/OK)
- Derived metric panels: time series for throughput, latency, lag

**Dashboard JSON structure**:
```json
{
  "title": "<project> Overview",
  "uid": "<project>-overview",
  "tags": ["<project>", "generated"],
  "templating": { "list": [/* $namespace, $app */] },
  "panels": [/* generated from spec metrics */],
  "time": { "from": "now-1h", "to": "now" },
  "refresh": "30s"
}
```

Each panel must reference specific metrics from the spec by name and include proper PromQL queries. Use `app="<project>"` label selector to align with the infra-atlas contract `app` label requirement.

Write dashboard files to: `$MEM/dashboards/<project>-overview.json`, `$MEM/dashboards/<project>-vitals.json`

### Step 3 — Generate Prometheus alert rules

For each alert in the spec, produce a Prometheus alerting rule in the standard format:

```yaml
groups:
  - name: <project>
    rules:
      - alert: <alert_name>
        expr: <condition from spec>
        for: 5m
        labels:
          severity: <severity from spec>
          app: <project>
        annotations:
          summary: "<description>"
          source_pattern: "<pattern that motivated this alert>"
          runbook_url: "<if failure mode has recovery steps in atlas>"
```

**Required meta-alert** (always generated):
```yaml
- alert: <project>VitalsMissing
  expr: absent(vitals_process{app="<project>"})
  for: 5m
  labels:
    severity: critical
    app: <project>
  annotations:
    summary: "Vitals pod for <project> is not reporting. Health visibility lost."
```

**Severity routing** (document in annotations):
- `critical` — pages on-call (PagerDuty)
- `warning` — Slack notification

Write alert rules to: `$MEM/alerts/<project>-rules.yaml`

### Step 4 — Validate live metric emission

If the service is running (cluster access available), verify that the expected metrics are actually being emitted:

1. **Get pod endpoint** — use cluster config to find the service's metrics endpoint:
   ```bash
   kubectl get pods -n <namespace> -l app=<project> -o jsonpath='{.items[0].status.podIP}'
   ```

2. **Scrape metrics** — hit the `/metrics` endpoint:
   ```bash
   curl -s http://<pod-ip>:<metrics-port>/metrics
   ```

3. **Check each spec metric** — for every metric in monitoring-spec.yaml:
   - Does a metric with this name appear in the scrape output?
   - Does it have the expected type (counter/gauge/histogram)?
   - Are the expected labels present?

4. **Check contract compliance** — verify infra-atlas requirements:
   - Pod has `app: <project>` label
   - Pod has `prometheus.io/scrape: "true"` annotation
   - Health endpoint responds at `/health`
   - Logs are JSON on stdout (check recent logs via `kubectl logs`)

5. **Classify results**:
   - `PASS` — metric exists with correct type and labels
   - `MISSING` — metric not found in scrape output (not yet instrumented)
   - `TYPE_MISMATCH` — metric exists but wrong type
   - `LABELS_MISSING` — metric exists but missing expected labels
   - `CONTRACT_VIOLATION` — infra-atlas requirement not met

If cluster access is unavailable, skip this step and note it in the report.

### Step 5 — Write to sauron project memory

Write all generated configs to sauron's project memory:

```
$MEM/
  dashboards/
    <project>-overview.json      # Grafana overview dashboard
    <project>-vitals.json        # Grafana vitals dashboard (if applicable)
  alerts/
    <project>-rules.yaml         # Prometheus alert rules
  validation-report.yaml         # Metric emission validation results
  implementation-status.yaml     # What was created, what needs work
```

The `$MEM` path is the project memory directory injected by the daemon:
`/kord/agents/sauron/memory/projects/<project>/`

`implementation-status.yaml` tracks:
```yaml
project: <name>
generated: <timestamp>
source_spec: <path to monitoring-spec.yaml used>
dashboards:
  - file: <project>-overview.json
    status: generated|pushed
    panels: <count>
  - file: <project>-vitals.json
    status: generated|pushed
    panels: <count>
alerts:
  - file: <project>-rules.yaml
    status: generated|applied
    rules: <count>
validation:
  total_metrics: <count>
  pass: <count>
  missing: <count>
  type_mismatch: <count>
  labels_missing: <count>
  contract_violations: [<list>]
```

### Step 6 — Deploy (unless --dry-run)

If not `--dry-run`:

1. **Push dashboards to Grafana** — use the Grafana API (see `grafana_api.py`):
   ```python
   push_dashboard("<project>-overview.json", folder_uid="<project>")
   ```

2. **Apply alert rules** — deploy as ConfigMap for Prometheus to pick up:
   ```bash
   kubectl create configmap <project>-alerts -n monitor \
     --from-file=alerts/ --dry-run=client -o yaml | kubectl apply --server-side -f -
   ```

3. **Provision dashboards** — deploy as ConfigMap for Grafana:
   ```bash
   kubectl create configmap <project>-dashboards -n monitor \
     --from-file=dashboards/ --dry-run=client -o yaml | kubectl apply --server-side -f -
   ```

If `--dry-run`, write the files but do not push or apply. Note in the report.

## Report

```
## Monitoring Implementation: <project>

**Source spec**: <path to monitoring-spec.yaml>
**Generated from**: <spec.generated_from>

### Dashboards
| Dashboard | Panels | Status |
|-----------|--------|--------|
| <project>-overview | N | pushed / generated (dry-run) |
| <project>-vitals | N | pushed / generated (dry-run) |

Written to: $MEM/dashboards/

### Alert Rules
| Alert | Severity | Source Pattern | Status |
|-------|----------|----------------|--------|
| <alert_name> | critical/warning | <pattern> | applied / generated (dry-run) |
| <project>VitalsMissing | critical | meta-alert | applied / generated (dry-run) |

Written to: $MEM/alerts/<project>-rules.yaml
Rules: N (N critical, N warning)

### Metric Validation
| Metric | Type | Status |
|--------|------|--------|
| <metric_name> | counter | PASS / MISSING / TYPE_MISMATCH |

Summary: N/N metrics validated, N missing, N contract violations
(or: "Skipped — cluster access unavailable")

### Contract Compliance (infra-atlas)
- [x] app label present
- [x] prometheus.io/scrape annotation
- [x] /health endpoint responds
- [x] JSON logs on stdout
(or [ ] with explanation for failures)

### Files written
- $MEM/dashboards/<project>-overview.json
- $MEM/dashboards/<project>-vitals.json
- $MEM/alerts/<project>-rules.yaml
- $MEM/validation-report.yaml
- $MEM/implementation-status.yaml
```
