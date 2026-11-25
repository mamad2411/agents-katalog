---
name: golang-alerting
description: >
  Design actionable alerts for Go services: SLO-based rules, PromQL patterns,
  Alertmanager routing, runbooks, and instrumentation. Use for owned systems
  under authorization.
---

# Golang Alerting

## Research grounding

Runbook for **creating and operating alerts** on Go services—metrics via
prometheus client libraries, rules, routing, and runbook quality. Skill id:
`golang-alerting`.

## Scope And Authorization

- **In scope:** owned services and observability stacks.
- **Out of scope:** paging third parties or abusing notification APIs.
- Prefer staging rule deploy; production pages affect humans—change carefully.
- Redact secrets and PII from annotations.
- Pair with `code-quality-standards`; noise reduction → `golang-alert-fatigue`.

## When To Use

- Adding first-class monitoring for a new Go service or critical path.
- Defining SEV levels, routes, and on-call handoff for Go microservices.
- Writing PromQL/Logs-based alerts tied to Go metrics names.
- Focus tokens: **golang, alerting**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Reducing existing noise | `golang-alert-fatigue` |
| Anomaly ML tuning | `golang-anomaly-tuning` |
| Metrics/tracing standards | `observability-metrics-tracing` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Golden signals | Latency, traffic, errors, saturation (+ business KPIs) |
| SLO alerts | Multi-window multi-burn-rate (MWMBR) preferred over raw thresholds |
| Go metrics | `prometheus/client_golang`; consistent prefix `namespace_subsystem_` |
| Logs | Structured (`slog`/zap); alert on rates not single lines when possible |
| Routing | severity → pager vs ticket vs Slack |
| Runbooks | Every page alert has `runbook_url` annotation |
| Pitfalls | Alerting on causes only; no owner; high cardinality labels |

## Workflow

### 1. Confirm scope and success criteria

1. Service, SLOs, on-call rotation, authorization.
2. Success: critical user journeys covered; test page received; runbooks linked.
3. Define what is **not** paged (info metrics).

### 2. Inventory

1. Existing dashboards, metrics, and dead alerts.
2. Dependencies (DB, queues, IdP) and their alerts.
3. Label taxonomy (`service`, `env`, `region`).

### 3. Baseline

1. Current error rate/latency for SLOs.
2. Decide SLI measurement from Go handlers (histograms, counters).

### 4. Instrument and define alerts

```go
var (
	httpRequests = promauto.NewCounterVec(prometheus.CounterOpts{
		Name: "myapp_http_requests_total",
		Help: "HTTP requests",
	}, []string{"route", "code_class"})
	httpDuration = promauto.NewHistogramVec(prometheus.HistogramOpts{
		Name:    "myapp_http_request_duration_seconds",
		Help:    "HTTP duration",
		Buckets: prometheus.DefBuckets,
	}, []string{"route"})
)
```

Example rule ideas (illustrative):

```yaml
groups:
  - name: myapp
    rules:
      - alert: MyappHighErrorRate
        expr: |
          sum(rate(myapp_http_requests_total{code_class="5xx"}[5m]))
          /
          sum(rate(myapp_http_requests_total[5m])) > 0.05
        for: 10m
        labels:
          severity: page
          service: myapp
        annotations:
          summary: "High 5xx rate on myapp"
          runbook_url: "https://runbooks.example/myapp/high-5xx"
      - alert: MyappDown
        expr: up{job="myapp"} == 0
        for: 2m
        labels:
          severity: page
          service: myapp
```

1. Page on **symptoms** users feel; ticket on capacity trends.
2. Include dependency alerts but inhibit children when parent is down.
3. Test alert pipeline end-to-end (staging sink).

### 5. Verify with evidence

```bash
promtool check rules rules/myapp.yml
promtool test rules rules/myapp_test.yml
go test ./... -count=1
```

1. Fault inject in staging: kill pod → `MyappDown` fires → page/route correct.
2. Confirm labels allow grouping without storms.
3. Runbook steps validated by someone other than author.

### 6. Observe and harden

1. Track false positives; feed `golang-alert-fatigue`.
2. Review alerts after each SEV-1 (missing or noisy).
3. Keep alert-as-code in git with review.

### 7. Hand off

1. On-call training; escalation policy documented.
2. Dashboard links in annotations.
3. Apply `code-quality-standards` to metrics middleware.

## Severity guide

| Severity | Channel | Example |
| --- | --- | --- |
| page | Pager | SLO burn, total outage |
| ticket | Issue tracker | Disk 80%, cert 14d |
| info | Chat only | Deploy finished |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Expr | Burn rate / rate() | single datapoint without `for` |
| Labels | service, severity | user_id |
| Runbook | Linked + tested | empty annotation |
| Ownership | team label + schedule | nobody |
| Topic fidelity | Go metrics + alert design | Generic go test only |

## Output Checklist

- [ ] SLOs/SLIs defined for Go service
- [ ] Metrics instrumented with bounded labels
- [ ] Rules checked with promtool
- [ ] Routing/severity correct
- [ ] Runbooks linked and reviewed
- [ ] Staging fire test evidence
- [ ] GitOps ownership for rules
- [ ] `code-quality-standards` applied

## Rules

- Page only actionable, user-impacting conditions by default.
- Never put secrets in alert annotations.
- Focus on `golang-alerting`; noise → `golang-alert-fatigue`.
- Authorized notification endpoints only.
