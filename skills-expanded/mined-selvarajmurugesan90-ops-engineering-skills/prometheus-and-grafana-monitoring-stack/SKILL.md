---
name: prometheus-and-grafana-monitoring-stack
description: >
  Guides standing up and operating the Prometheus + Grafana monitoring
  stack in Kubernetes and hybrid environments — scrape configuration and
  service discovery, writing PromQL for dashboards and alerts, defining
  Alertmanager routing/silencing, and provisioning Grafana datasources
  and dashboards as code. Use when a user asks to "scrape a new
  service", "write a PromQL query", "add an alerting rule", "configure
  Alertmanager routing/silences", "provision a Grafana dashboard", "debug
  a target showing as down", or "reduce alert noise/duplicate pages."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# Prometheus and Grafana Monitoring Stack

## Purpose

Prometheus and Grafana are the de facto open-source metrics stack for
Kubernetes and cloud-native workloads: Prometheus pulls (scrapes) metrics
on an interval, evaluates alerting rules against them, and hands firing
alerts to Alertmanager for routing/deduplication/silencing, while Grafana
turns the same time-series data into dashboards. The stack is simple to
install (kube-prometheus-stack Helm chart is a one-command bootstrap) but
easy to run badly: scrape configs that silently miss targets, PromQL
queries that are technically valid but semantically wrong (rate() over
too short a window, missing `by()` clauses that collapse dashboards to a
single line), alerting rules that page on transient blips, and
hand-edited Grafana dashboards that drift from what's checked into git.
This skill covers configuring scrape targets and service discovery
correctly, writing PromQL that means what you think it means, defining
alerting rules and Alertmanager routing that produce actionable pages
instead of noise, and provisioning Grafana as code so dashboards survive
a cluster rebuild.

## When to use

- Onboarding a new service/exporter so its metrics are actually scraped
  (adding a `ServiceMonitor`/`PodMonitor`, a static scrape config, or a
  Prometheus Operator CRD).
- Writing or debugging a PromQL query for a dashboard panel, a
  recording rule, or an alerting rule.
- Defining or tuning Prometheus alerting rules and Alertmanager
  routing trees, grouping, inhibition, and silences.
- Provisioning Grafana datasources and dashboards declaratively
  (as ConfigMaps/sidecars, Grafana provisioning YAML, or Terraform) so
  they are version-controlled rather than edited by hand in the UI.
- Investigating a target showing `up == 0` in Prometheus, a dashboard
  panel showing "No data", or an alert that fired but didn't page
  anyone (or paged everyone, repeatedly).
- Reducing alert fatigue — too many pages, duplicate pages across
  teams, or alerts with no clear owner/runbook.

## Prerequisites & environment

- Kubernetes cluster with the **kube-prometheus-stack** Helm chart
  (bundles Prometheus Operator, Prometheus, Alertmanager, Grafana, and
  the `node-exporter`/`kube-state-metrics` exporters) — version 55.x+
  tracks Prometheus 2.5x and Grafana 10.x/11.x at the time of writing;
  pin an exact chart version rather than tracking `latest` in
  production.
- Familiarity with the Prometheus Operator custom resources
  (`ServiceMonitor`, `PodMonitor`, `PrometheusRule`, `Probe`) if running
  on top of the Operator, versus hand-written `scrape_configs` in
  `prometheus.yml` if running vanilla Prometheus.
- Cluster RBAC allowing Prometheus's service account to `list`/`watch`
  `Endpoints`, `Service`, and `Pod` objects for Kubernetes service
  discovery (`kubernetes_sd_configs`) to function.
- A notification receiver already provisioned for Alertmanager
  (Slack webhook, PagerDuty integration key, Opsgenie API key, or
  generic webhook) stored as a Kubernetes `Secret` — never inline in the
  Alertmanager config.
- For Grafana provisioning as code: either the sidecar pattern
  (ConfigMaps labeled `grafana_dashboard: "1"` auto-loaded by a
  Grafana sidecar container) or the Grafana provisioning
  directory/Terraform provider, plus a git repo to store dashboard JSON.

## Step-by-step guidance

1. **Install the stack with an explicit, pinned chart version:**
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm upgrade --install kube-prom-stack prometheus-community/kube-prometheus-stack \
     --namespace monitoring --create-namespace \
     --version 65.5.0 \
     -f values-monitoring.yaml
   ```

2. **Add a scrape target for a new service.** Prefer the Prometheus
   Operator `ServiceMonitor` CRD over hand-editing `scrape_configs` —
   it's picked up automatically without a Prometheus reload/restart:
   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: payments-api
     namespace: monitoring
     labels:
       release: kube-prom-stack   # must match the Prometheus CR's serviceMonitorSelector
   spec:
     selector:
       matchLabels:
         app: payments-api        # matches the target Service's labels
     namespaceSelector:
       matchNames:
         - payments
     endpoints:
       - port: metrics            # named port on the Service, not a raw port number
         path: /metrics
         interval: 30s
         scrapeTimeout: 10s
   ```
   For non-Kubernetes targets (a VM, an on-prem host), use a static
   `scrape_configs` entry or `file_sd_configs` pointing at a JSON/YAML
   file so targets can be added without restarting Prometheus:
   ```yaml
   scrape_configs:
     - job_name: 'onprem-node-exporter'
       file_sd_configs:
         - files: ['/etc/prometheus/file_sd/onprem-nodes.json']
           refresh_interval: 5m
   ```

3. **Confirm the target is actually being scraped** before writing any
   dashboard or alert against it: check `Status > Targets` in the
   Prometheus UI (or `up{job="payments-api"}`) — a target that never
   appears usually means a label-selector mismatch, not a scrape
   failure (see Common pitfalls).

4. **Write PromQL against a rate, not a raw counter**, for anything
   that is a `_total` counter metric:
   ```promql
   # request rate over 5m, per service and status code
   sum by (service, status_code) (
     rate(http_requests_total[5m])
   )

   # error ratio (%) — guard the denominator so it doesn't divide by zero
   100 * sum(rate(http_requests_total{status_code=~"5.."}[5m]))
       / sum(rate(http_requests_total[5m]))

   # p99 latency from a histogram
   histogram_quantile(0.99,
     sum by (le, service) (rate(http_request_duration_seconds_bucket[5m]))
   )
   ```
   Use a rate window at least **4x the scrape interval** (e.g. `[5m]`
   for a 30s-60s scrape interval) so `rate()` always has enough samples
   to extrapolate correctly.

5. **Add recording rules for anything queried repeatedly** (dashboards,
   alerts) to precompute expensive aggregations rather than recomputing
   them on every dashboard refresh:
   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: PrometheusRule
   metadata:
     name: payments-api-recording-rules
     namespace: monitoring
     labels:
       release: kube-prom-stack
   spec:
     groups:
       - name: payments-api.rules
         interval: 30s
         rules:
           - record: job:http_requests:rate5m
             expr: sum by (job) (rate(http_requests_total[5m]))
   ```

6. **Write alerting rules with a `for:` duration** to suppress
   flapping/transient blips, and attach severity + runbook labels so
   routing and on-call response are automatic:
   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: PrometheusRule
   metadata:
     name: payments-api-alerts
     namespace: monitoring
     labels:
       release: kube-prom-stack
   spec:
     groups:
       - name: payments-api.alerts
         rules:
           - alert: PaymentsAPIHighErrorRate
             expr: |
               100 * sum(rate(http_requests_total{job="payments-api",status_code=~"5.."}[5m]))
                   / sum(rate(http_requests_total{job="payments-api"}[5m])) > 5
             for: 10m
             labels:
               severity: critical
               team: payments
             annotations:
               summary: "Payments API error rate above 5% for 10m"
               runbook_url: "https://runbooks.internal/payments-api-error-rate"

           - alert: PrometheusTargetDown
             expr: up{job="payments-api"} == 0
             for: 5m
             labels:
               severity: warning
               team: payments
             annotations:
               summary: "Payments API target down for 5m"
   ```

7. **Configure Alertmanager routing** so alerts reach the right team
   without duplicate pages, using label matching, grouping, and
   inhibition:
   ```yaml
   route:
     receiver: default-slack
     group_by: ['alertname', 'team']
     group_wait: 30s
     group_interval: 5m
     repeat_interval: 4h
     routes:
       - matchers:
           - severity = "critical"
           - team = "payments"
         receiver: payments-pagerduty
         continue: false
       - matchers:
           - severity = "warning"
         receiver: default-slack

   inhibit_rules:
     # a firing critical alert suppresses a lower-severity alert for the same target
     - source_matchers: [severity = "critical"]
       target_matchers: [severity = "warning"]
       equal: ['alertname', 'job']

   receivers:
     - name: default-slack
       slack_configs:
         - api_url: '${SLACK_WEBHOOK_URL}'
           channel: '#alerts-platform'
     - name: payments-pagerduty
       pagerduty_configs:
         - routing_key: '${PAGERDUTY_ROUTING_KEY}'
   ```
   Store `SLACK_WEBHOOK_URL`/`PAGERDUTY_ROUTING_KEY` in a Kubernetes
   `Secret` referenced via `alertmanagerConfigSecret`/`envFrom`, never
   inline.

8. **Provision Grafana datasources and dashboards as code**, not
   through the UI, using the sidecar pattern:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: payments-api-dashboard
     namespace: monitoring
     labels:
       grafana_dashboard: "1"   # auto-discovered by the Grafana sidecar
   data:
     payments-api.json: |
       { "title": "Payments API", "panels": [ ... ] }
   ```
   and a datasource provisioned once at install time:
   ```yaml
   apiVersion: 1
   datasources:
     - name: Prometheus
       type: prometheus
       access: proxy
       url: http://kube-prom-stack-prometheus.monitoring:9090
       isDefault: true
       jsonData:
         timeInterval: 30s
   ```
   Export dashboard JSON from the Grafana UI only as a starting point,
   then check it into git and let the sidecar/provisioning pipeline own
   it going forward.

9. **Validate rule syntax before applying** with `promtool` in CI:
   ```bash
   promtool check rules payments-api-alerts.yaml
   promtool test rules payments-api-alerts_test.yaml
   ```

## Best practices

- **Use `ServiceMonitor`/`PodMonitor` CRDs over hand-edited
  `scrape_configs`** when running the Prometheus Operator — they're
  reconciled automatically and don't require a Prometheus restart/reload.
- **Every alert must have `severity` and `team` (or equivalent
  ownership) labels** and a `runbook_url` annotation — an alert with no
  clear owner and no runbook is a page nobody knows how to act on.
- **Set `for:` on every alerting rule** long enough to ride out normal
  noise (typically 5-15 minutes for error-rate/latency alerts, shorter
  for hard down/crash-loop conditions) — alerts without a `for:` fire on
  a single bad scrape.
- **Precompute expensive/frequently-used aggregations as recording
  rules** rather than repeating heavy PromQL in every dashboard panel —
  keeps dashboard load fast and query cost predictable.
- **Alert on symptoms (error rate, latency, saturation), not on every
  possible cause** — a smaller set of well-tuned symptom-based alerts
  produces far less noise than alerting on every internal metric.
- **Use inhibition rules to suppress redundant lower-severity alerts**
  when a related critical alert is already firing for the same target,
  instead of paging on every layer of a cascading failure.
- **Set retention and remote-write/long-term-storage deliberately** —
  local Prometheus TSDB retention (commonly 15-30 days) is for
  operational queries; use Thanos, Cortex, or Mimir (or a managed
  remote-write target) if you need long-term retention for capacity
  planning or compliance.
- **Version-control Grafana dashboards and Alertmanager config** in the
  same repo/pipeline as the rest of the platform config — dashboards
  edited only in the UI are lost on the next cluster rebuild.

## Common pitfalls

- **Symptom:** A `ServiceMonitor` is applied but the target never shows
  up under `Status > Targets` in Prometheus.
  **Fix:** The `ServiceMonitor`'s `labels` don't match the Prometheus
  custom resource's `serviceMonitorSelector` (commonly `release:
  <helm-release-name>`), or the `endpoints.port` name doesn't match a
  named port on the target `Service`. Check
  `kubectl get prometheus -o yaml` for the selector and confirm the
  Service exposes a **named** port, not just a numeric one.

- **Symptom:** A dashboard panel using `rate(http_requests_total[1m])`
  shows a flat line or gaps even though traffic is steady.
  **Fix:** The rate window is too close to (or shorter than) the scrape
  interval, so `rate()` doesn't have enough samples to extrapolate.
  Use a window at least 4x the scrape interval (`[5m]` for a 30-60s
  scrape interval).

- **Symptom:** An alert fires and pages on-call, but investigation shows
  it was a single transient blip that self-resolved seconds later.
  **Fix:** No `for:` duration was set (or it was too short). Add a
  `for:` clause matched to the metric's natural noise level so the
  condition must hold for the full duration before firing.

- **Symptom:** The same underlying incident produces five separate
  pages across four different teams within two minutes.
  **Fix:** No `inhibit_rules` or `group_by` tuning in Alertmanager — every
  downstream symptom alert fired independently. Group alerts by
  `alertname`/`team`/shared label, and add inhibition rules so a firing
  root-cause alert suppresses its known downstream symptoms.

- **Symptom:** A hand-edited Grafana dashboard that took hours to build
  disappears after a Helm upgrade or cluster rebuild.
  **Fix:** The dashboard was only ever saved through the Grafana UI,
  not provisioned via a ConfigMap/sidecar or the Terraform Grafana
  provider. Export it to JSON, check it into git, and load it through
  provisioning so it's rebuilt automatically.

- **Symptom:** Prometheus disk fills up and the pod starts
  crash-looping (`OOMKilled` or `no space left on device`).
  **Fix:** Retention (`--storage.tsdb.retention.time`/`.size`) wasn't
  bounded relative to actual disk size, or high-cardinality labels
  (e.g. a label containing a raw user ID or full URL path) blew up
  the number of time series. Bound retention explicitly, and audit
  metrics/labels for unbounded cardinality before scraping them at
  scale.

## Worked example

**Scenario:** The `payments-api` team ships a new service. It exposes
Prometheus metrics on `/metrics` but is invisible in Prometheus, has no
dashboard, and no alerting — the team wants to be paged only on genuine
customer-impacting error rates, not on every blip.

1. Confirm the Service exposes a named metrics port:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: payments-api
     namespace: payments
     labels:
       app: payments-api
   spec:
     ports:
       - name: metrics
         port: 9100
         targetPort: 9100
   ```
2. Apply the `ServiceMonitor` (step 2 above) with `release:
   kube-prom-stack` matching the Prometheus selector, and confirm
   `up{job="payments-api"}` returns `1` in the Prometheus UI within one
   scrape interval.
3. Add a recording rule for request rate/error rate (step 5) so the
   dashboard and alert both reference the same precomputed series.
4. Add the `PaymentsAPIHighErrorRate` alert (step 6) with `for: 10m`,
   `severity: critical`, `team: payments`, and a `runbook_url`.
5. Route `severity="critical", team="payments"` to a PagerDuty
   receiver and everything else to the team's Slack channel (step 7),
   with an inhibition rule so a firing `PaymentsAPIHighErrorRate`
   suppresses the lower-severity `PrometheusTargetDown` warning for
   the same job if both trip during the same incident.
6. Provision a Grafana dashboard (request rate, error rate, p99 latency
   panels backed by the recording rule and histogram query from step 4)
   as a labeled ConfigMap, checked into the team's platform-config repo
   alongside the `ServiceMonitor` and `PrometheusRule` manifests.
7. Run `promtool check rules` and `promtool test rules` in CI against
   the alerting rule file before merging, catching a typo'd metric name
   before it reaches production.

## Cross-references

- [kubecost-cost-visibility](../kubecost-cost-visibility/SKILL.md)
- [karpenter-cluster-autoscaling](../karpenter-cluster-autoscaling/SKILL.md)
- [kubernetes-network-policy-zero-trust](../kubernetes-network-policy-zero-trust/SKILL.md)
