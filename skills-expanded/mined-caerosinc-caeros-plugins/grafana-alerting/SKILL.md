---
name: grafana-alerting
description: Configure Grafana Alerting, including alert rules, contact points, notification policies, and silences. Use when creating alerts or wiring notifications to Slack, email, PagerDuty, or webhooks.
---

# Grafana Alerting

Grafana-managed alerting (unified alerting) evaluates queries on a schedule
and routes firing alerts through notification policies to contact points.

## Alert rules

A rule = one or more queries + expressions ending in a single condition,
evaluated every interval, firing after a pending period.

Typical shape:

- **A**: data query, e.g. PromQL
  `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`
- **B**: expression `Reduce` (last of A) when A returns a time series
- **C**: expression `Threshold` (B > 0.05), marked as the alert condition
- Evaluation: every `1m`, pending period (`for`) `5m` to suppress blips
- Labels: `severity=critical`, `team=payments` (drive routing)
- Annotations: `summary`, `description`, `runbook_url` (templated with
  `{{ $labels.route }}`, `{{ $values.B }}`)

Also configure no-data and error handling per rule (fire, OK, or keep last
state); silent no-data is a common way to miss dead exporters, so alert on it
for critical paths. Loki metric queries (`count_over_time`, `rate`) work the
same way for log-based alerts.

## Contact points

Where notifications go: Slack, email, PagerDuty, OpsGenie, webhook, Teams,
and more. One contact point can have multiple integrations. Message content
is customizable with notification templates (Go templating over `.Alerts`,
`.CommonLabels`).

## Notification policies

A tree of matchers routes alerts by label to contact points:

- Root policy: default contact point plus timings (`group_by`,
  `group_wait`, `group_interval`, `repeat_interval`).
- Child policies: e.g. `severity=critical` to the pager contact point,
  `team=payments` to that team's Slack channel; children can `continue` to
  let siblings also match.
- `group_by` labels collapse related alerts into one notification.

Mute timings suppress notifications on a schedule (deploy windows, nights
for non-critical); silences suppress by label match ad hoc during incidents.

## As code

Provision rules, contact points, and policies via YAML files
(`conf/provisioning/alerting/`), Terraform, or the alerting HTTP API; rules
export from the UI as provisioning-ready YAML/JSON. Keep alert definitions in
git next to the dashboards they watch.

## Practices

- Alert on symptoms (error ratio, p95 latency, saturation) with runbook
  links; keep cause-level alerts as warnings.
- Every rule gets `severity` and `team` labels or routing degrades into one
  noisy default channel.
- Test the full path: fire a synthetic alert and confirm delivery per
  contact point.
- The bundled mcp-grafana server can list and inspect alert rules and
  contact points on your instance.
