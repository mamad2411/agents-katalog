---
name: alerting-rules
description: Design alerting rules for production monitoring with Prometheus, Grafana, PagerDuty. Outputs alert definitions, severity levels, escalation policies, and runbooks.
argument-hint: [service SLAs, team size, on-call rotation]
allowed-tools: Read, Write, Bash
---

# Alerting Rules

Design production alerting rules that wake the right people for the right problems. Not alert fatigue — symptom-based alerts with severity levels, escalation, and runbooks.

## Process

1. **Define SLOs.** Service Level Objectives (99.9% uptime, p95 < 200ms).
2. **Identify symptoms.** Customer-facing issues (slow responses, errors, downtime).
3. **Write alert rules.** Prometheus alerting rules,  thresholds, duration.
4. **Set severity levels.** Critical (page), warning (ticket), info (log).
5. **Configure routing.** Who gets notified, when, via what channel.
6. **Write runbooks.** Debugging steps for each alert.
7. **Track metrics.** Alert frequency, time to resolution, false positive rate.

## Output Format

### Alerting Configuration: [Service]

**Tool:** Prometheus + Alertmanager  
**Alert Rules:** 25 defined  
**Severity Levels:** Critical (5), Warning (15), Info (5)  
**Routing:** PagerDuty (critical), Slack (warning), email (info)  
**Runbooks:** 25 documented

---

## Alert Severity Levels

### Critical (Page On-Call)
```
Customer impact: YES
Response time: < 5 minutes
Examples:
- Service down (> 1 minute)
- Error rate > 5%
- Database unreachable
- Payment processing failing
```

### Warning (Create Ticket)
```
Customer impact: Potential
Response time: < 1 hour
Examples:
- High latency (p95 > 500ms)
- Disk space < 20%
- Cache hit rate dropping
- API rate limit approaching
```

### Info (Log/Dashboard)
```
Customer impact: None
Response time: Next business day
Examples:
- Deployment succeeded
- Auto-scaling triggered
- Backup completed
- Certificate renewed
```

---

## Prometheus Alert Rules

```yaml
# /etc/prometheus/alerts.yml
groups:
  - name: service_alerts
    interval: 30s
    rules:
      # Critical: Service Down
      - alert: ServiceDown
        expr: up{job="api"} == 0
        for: 1m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "Service {{ $labels.instance }} is down"
          description: "{{ $labels.job }} on {{ $labels.instance }} has been down for 1 minute"
          runbook: "https://runbooks.example.com/service-down"
      
      # Critical: High Error Rate
      - alert: HighErrorRate
        expr: |
          (
            rate(http_requests_total{status=~"5.."}[5m]) /
            rate(http_requests_total[5m])
          ) > 0.05
        for: 5m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High error rate on {{ $labels.instance }}"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook: "https://runbooks.example.com/high-error-rate"
      
      # Critical: Database Connection Pool Exhausted
      - alert: DatabaseConnectionPoolExhausted
        expr: |
          (
            db_connections_active / db_connections_max
          ) > 0.95
        for: 2m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "Database connection pool exhausted"
          description: "{{ $value | humanizePercentage }} of connections in use"
      
      # Warning: High Latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 0.5
        for: 10m
        labels:
          severity: warning
          team: backend
        annotations:
          summary: "High latency on {{ $labels.route }}"
          description: "p95 latency is {{ $value }}s"
      
      # Warning: Disk Space Low
      - alert: DiskSpaceLow
        expr: |
          (
            node_filesystem_avail_bytes{mountpoint="/"} /
            node_filesystem_size_bytes{mountpoint="/"}
          ) < 0.2
        for: 5m
        labels:
          severity: warning
          team: sre
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} remaining"
      
      # Warning: High Memory Usage
      - alert: HighMemoryUsage
        expr: |
          (
            node_memory_MemAvailable_bytes /
            node_memory_MemTotal_bytes
          ) < 0.1
        for: 5m
        labels:
          severity: warning
          team: sre
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} memory available"
      
      # Info: Deployment
      - alert: DeploymentCompleted
        expr: deployment_status{status="success"} == 1
        labels:
          severity: info
          team: backend
        annotations:
          summary: "Deployment completed"
          description: "Version {{ $labels.version }} deployed to {{ $labels.environment }}"
```

---

## Alertmanager Configuration

```yaml
# /etc/alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m
  pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'
  slack_api_url: 'https://hooks.slack.com/services/...'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s       # Wait 10s to batch alerts
  group_interval: 10s   # Send batch every 10s
  repeat_interval: 12h  # Repeat every 12h if not resolved
  receiver: 'team-notifications'
  
  routes:
    # Critical alerts to PagerDuty
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      group_wait: 0s      # Immediate
      repeat_interval: 5m # Repeat every 5min
      continue: true      # Also send to Slack
    
    - match:
        severity: critical
      receiver: 'slack-critical'
      group_wait: 0s
    
    # Warning alerts to Slack
    - match:
        severity: warning
      receiver: 'slack-warnings'
    
    # Info alerts to email
    - match:
        severity: info
      receiver: 'email-info'

receivers:
  - name: 'team-notifications'
    email_configs:
      - to: 'team@example.com'
  
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<pagerduty-integration-key>'
        description: '{{ .CommonAnnotations.summary }}'
        details:
          firing: '{{ .Alerts.Firing | len }}'
          num_firing: '{{ .Alerts.Firing | len }}'
          num_resolved: '{{ .Alerts.Resolved | len }}'
          resolved: '{{ .Alerts.Resolved | len }}'
        client: 'Prometheus'
        client_url: '{{ template "pagerduty.default.clientURL" . }}'
  
  - name: 'slack-critical'
    slack_configs:
      - channel: '#incidents'
        title: '🚨 {{ .CommonAnnotations.summary }}'
        text: |
          {{ range .Alerts }}
          *Alert:* {{ .Labels.alertname }}
          *Severity:* {{ .Labels.severity }}
          *Description:* {{ .Annotations.description }}
          *Runbook:* {{ .Annotations.runbook }}
          {{ end }}
        color: 'danger'
  
  - name: 'slack-warnings'
    slack_configs:
      - channel: '#alerts'
        title: '⚠️ {{ .CommonAnnotations.summary }}'
        text: '{{ .CommonAnnotations.description }}'
        color: 'warning'
  
  - name: 'email-info'
    email_configs:
      - to: 'team@example.com'
        headers:
          Subject: '[Info] {{ .CommonAnnotations.summary }}'

inhibit_rules:
  # Don't alert on instance down if whole cluster down
  - source_match:
      alertname: 'ClusterDown'
    target_match:
      alertname: 'ServiceDown'
    equal: ['cluster']
  
  # Don't alert on high latency if service down
  - source_match:
      alertname: 'ServiceDown'
    target_match:
      alertname: 'HighLatency'
    equal: ['instance']
```

---

## Escalation Policies

```yaml
# PagerDuty escalation policy
escalation_policy:
  name: "Backend On-Call"
  escalation_rules:
    # Level 1: Primary on-call
    - escalation_delay_in_minutes: 0
      targets:
        - type: schedule
          id: primary_schedule
    
    # Level 2: Secondary after 15 min
    - escalation_delay_in_minutes: 15
      targets:
        - type: schedule
          id: secondary_schedule
    
    # Level 3: Manager after 30 min
    - escalation_delay_in_minutes: 30
      targets:
        - type: user
          id: engineering_manager
```

---

## Alert Routing by Team

```yaml
route:
  routes:
    # Backend team alerts
    - match:
        team: backend
      receiver: 'backend-team'
      routes:
        - match:
            severity: critical
          receiver: 'backend-pagerduty'
    
    # Frontend team alerts
    - match:
        team: frontend
      receiver: 'frontend-team'
    
    # SRE team alerts (infrastructure)
    - match:
        team: sre
      receiver: 'sre-team'
      routes:
        - match:
            severity: critical
          receiver: 'sre-pagerduty'
```

---

## Runbook Template

```markdown
# Runbook: High Error Rate

**Alert Name:** HighErrorRate  
**Severity:** Critical  
**Team:** Backend

## Symptoms
- Error rate > 5% for 5 minutes
- Users seeing 500 errors
- May impact payments, orders, or login

## Impact
- **Users:** Cannot complete transactions
- **Revenue:** Lost sales during incident
- **SLA:** Violates 99.9% availability

## Diagnosis Steps

### 1. Check error distribution
```bash
# View error breakdown by endpoint
curl -s prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~"5.."}[5m]) | jq
```

### 2. Check recent deployments
```bash
# Last 5 deployments
kubectl rollout history deployment/api
```

### 3. Check database
```bash
# Database connections
psql -c "SELECT count(*) FROM pg_stat_activity;"

# Slow queries
psql -c "SELECT query, query_start FROM pg_stat_activity WHERE state='active' AND query_start < now() - interval '10 seconds';"
```

### 4. Check external dependencies
```bash
# Ping payment provider
curl -I https://api.stripe.com/v1/charges

# Check DNS
dig api.partner.com
```

## Common Causes
1. **Recent deployment** → Rollback
2. **Database connection pool exhausted** → Scale DB or app
3. **External API down** → Enable circuit breaker
4. **Memory leak** → Restart pods
5. **Rate limiting** → Increase limits or reduce traffic

## Resolution

### If caused by deployment (most common):
```bash
# Rollback last deployment
kubectl rollout undo deployment/api

# Wait 2 minutes, check error rate
watch -n 10 'curl -s prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~"5.."}[5m])'
```

### If caused by database:
```bash
# Scale up database
aws rds modify-db-instance --db-instance-identifier prod-db --db-instance-class db.m5.large

# Or scale app to reduce DB load
kubectl scale deployment/api --replicas=3
```

### If caused by external API:
```python
# Enable circuit breaker
curl -X POST https://api.example.com/circuit-breaker/stripe/open
```

## Escalation
- If error rate > 10% for 10 minutes: Page SRE lead
- If unable to resolve in 30 minutes: Page engineering manager
- If revenue-impacting: Notify COO

## Post-Incident
- File incident report
- Review deployment process
- Add monitoring for root cause
- Update runbook with learnings
```

---

## Alert Tuning

### Avoid Alert Fatigue
```yaml
# Bad: Alert on every error
- alert: AnyError
  expr: rate(errors[1m]) > 0  # Too sensitive!
  
# Good: Alert on sustained error rate
- alert: HighErrorRate
  expr: rate(errors[5m]) > 0.05  # 5% error rate
  for: 5m  # Sustained for 5 minutes
```

### Use Percentiles, Not Averages
```yaml
# Bad: Average latency (hides outliers)
- alert: HighLatency
  expr: avg(http_request_duration_seconds) > 1
  
# Good: p95 latency (catches tail latency)
- alert: HighLatency
  expr: histogram_quantile(0.95, http_request_duration_seconds_bucket) > 0.5
```

### Burn Rate Alerting (SLO-based)
```yaml
# Alert if burning error budget too fast
- alert: ErrorBudgetBurnRate
  expr: |
    (
      1 - (
        sum(rate(http_requests_total{status!~"5.."}[1h])) /
        sum(rate(http_requests_total[1h]))
      )
    ) > (14.4 * 0.001)  # 99.9% SLO, 14.4x burn rate
  for: 5m
  annotations:
    summary: "Burning error budget 14.4x faster than allowed"
    description: "At current rate, will exhaust monthly budget in 2 days"
```

---

## Alert Silence

```bash
# Silence alert during maintenance
amtool silence add \
  alertname=ServiceDown \
  instance=api-1 \
  --duration=2h \
  --comment="Planned maintenance"

# Silence all alerts for service
amtool silence add \
  service=api \
  --duration=1h \
  --comment="Emergency fix deployment"

# List active silences
amtool silence query

# Expire silence early
amtool silence expire <silence-id>
```

---

## Alert Testing

```yaml
# Test alert fires at threshold
- name: test_high_error_rate_alert
  interval: 1m
  input_series:
    - series: 'http_requests_total{status="500"}'
      values: '0+10x10'  # 0, 10, 20, ..., 100
    - series: 'http_requests_total{status="200"}'
      values: '0+100x10'  # 0, 100, 200, ..., 1000
  
  alert_rule_test:
    - eval_time: 5m
      alertname: HighErrorRate
      exp_alerts:
        - exp_labels:
            severity: critical
          exp_annotations:
            summary: "High error rate"
```

```bash
# Run alert tests
promtool test rules alert_test.yml
```

---

## Metrics to Track

```python
from prometheus_client import Counter, Histogram

# Alert metrics
alerts_fired = Counter('alerts_fired_total', 'Alerts fired', ['alertname', 'severity'])
alerts_resolved = Counter('alerts_resolved_total', 'Alerts resolved', ['alertname'])
alert_duration = Histogram('alert_duration_seconds', 'Time to resolve', ['alertname'])

# Track in Alertmanager webhook
@app.route('/alert-webhook', methods=['POST'])
def alert_webhook():
    data = request.json
    
    for alert in data['alerts']:
        if alert['status'] == 'firing':
            alerts_fired.labels(
                alertname=alert['labels']['alertname'],
                severity=alert['labels']['severity']
            ).inc()
        elif alert['status'] == 'resolved':
            alerts_resolved.labels(
                alertname=alert['labels']['alertname']
            ).inc()
            
            # Calculate duration
            start = parse_time(alert['startsAt'])
            end = parse_time(alert['endsAt'])
            duration = (end - start).total_seconds()
            
            alert_duration.labels(
                alertname=alert['labels']['alertname']
            ).observe(duration)
    
    return '', 200
```

## Rules

- Alert on symptoms, not causes — alert on "high error rate" not "database slow query".
- Page only for customer-impacting issues — false pages destroy on-call quality of life.
- Every alert needs a runbook — on-call shouldn't have to guess how to fix.
- Use `for` duration to reduce noise — transient blips shouldn't wake people.
- Set inhibit rules to prevent cascades — don't alert on 50 instances if cluster is down.
- Test alerts in staging — verify threshold fires before production deployment.
- Track alert metrics — false positive rate, time to resolution, alert frequency.
- Review and tune quarterly — prune low-signal alerts, adjust thresholds.
- Silence during deployments — known downtime shouldn't trigger pages.
- SLO-based alerting preferred over threshold — burn rate indicates customer impact.
