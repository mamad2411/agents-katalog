# /project:monitoring

**Interactive Production Monitoring & Alert Configuration**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:monitoring AB#123
/project:monitoring AB#123 --service=signup-service
/project:monitoring AB#123 --setup-alerts
```

## What This Does

1. **Loads NFR targets** from story
2. **Configures monitoring** dashboards (CloudWatch, Datadog, etc.)
3. **Sets up alerts** for critical thresholds
4. **Creates runbooks** for common issues
5. **Validates telemetry** (logs, metrics, traces)
6. **Documents on-call procedures**

## Interactive Flow

```
User: /project:monitoring AB#123

Claude: 📊 Production Monitoring Setup

✅ STORY LOADED:
  Service: signup-service (v1.2.0)
  NFRs:
    • P95 latency: <200ms
    • Error rate: <0.1%
    • Availability: 99.9%

🎯 MONITORING DASHBOARD:

Create monitoring dashboard?
  [1] CloudWatch (AWS)
  [2] Datadog
  [3] Prometheus + Grafana
  [4] All of above

User: [1]

Creating CloudWatch dashboard...

Dashboard Widgets:
  ✓ Latency (p50, p95, p99) — line graph
  ✓ Error rate — area graph
  ✓ Throughput (RPS) — bar graph
  ✓ Availability — gauge
  ✓ Database latency — line graph
  ✓ Cache hit ratio — gauge
  ✓ Service replicas — metric
  ✓ Memory/CPU utilization — stacked area

Dashboard created: signup-service-monitoring

🚨 ALERT CONFIGURATION:

Configure critical alerts?
  [1] Yes, setup all alerts
  [2] Custom alert selection
  [3] Skip, configure manually later

User: [1]

Configuring alerts...

LATENCY ALERTS:
  ✓ P95 >200ms (5 min average) → CRITICAL
    Action: Page on-call engineer
  ✓ P99 >500ms (5 min average) → WARNING
    Action: Slack notification to #eng-alerts

ERROR RATE ALERTS:
  ✓ Error rate >0.1% (1 min) → CRITICAL
    Action: Page on-call engineer + create incident
  ✓ Error rate >0.05% (5 min) → WARNING
    Action: Slack notification

AVAILABILITY ALERTS:
  ✓ Availability <99.9% (1 hour) → CRITICAL
    Action: Page on-call engineer
  ✓ Service replicas <2 → CRITICAL
    Action: Auto-scale + page

DATABASE ALERTS:
  ✓ Connection pool exhaustion → WARNING
    Action: Slack + monitor closely
  ✓ Query latency >100ms → WARNING
    Action: Log and monitor

All alerts configured: ✓ 8 critical, 4 warning

📝 RUNBOOKS:

Create runbooks for common issues?
  [1] Yes, generate for all alerts
  [2] Select critical runbooks only
  [3] Skip for now

User: [2]

Generating critical runbooks...

RUNBOOK 1: High Latency (P95 >200ms)
  Trigger: P95 latency exceeds 200ms for 5 min
  Investigation:
    1. Check database query latency (should be <50ms)
    2. Check Twilio API response time
    3. Check service CPU/memory utilization
    4. Check cache hit ratio (should be >80%)
  
  Common causes:
    • Database slow queries (N+1)
    • Twilio API degradation
    • Memory leak (service pod restart)
    • Thundering herd (connection pool exhaustion)
  
  Resolution steps:
    1. If DB slow: Check slow query log, optimize query
    2. If Twilio: Monitor Twilio status, use fallback
    3. If memory: Restart pod (auto-heals in 90% of cases)
    4. If connection pool: Scale up Postgres connections
  
  Escalation: If issue persists >15 min, page on-call architect

RUNBOOK 2: High Error Rate (>0.1%)
  Trigger: Error rate exceeds 0.1% for 1 min
  Investigation:
    1. Check error type distribution (OtpExpired, PhoneInvalid, etc.)
    2. Check error logs for stack traces
    3. Check dependent services (Twilio, ID service)
  
  Common causes:
    • Twilio quota exhausted
    • Database constraint violation
    • Dependency service down
    • Invalid input validation error
  
  Resolution:
    1. Identify error type
    2. If Twilio: Check quota, escalate to Twilio support
    3. If DB: Check constraints, review recent migrations
    4. If external: Switch to fallback, notify user
  
  Escalation: If issue persists >10 min, create incident + page

RUNBOOK 3: Low Availability (<99.9%)
  Trigger: Availability drops below 99.9% for 1 hour
  Investigation:
    1. Check service health (pods, replicas)
    2. Check infrastructure (node failures)
    3. Check external dependencies
  
  Resolution:
    1. If pods unhealthy: Check logs, restart
    2. If nodes down: AWS auto-scaling handles (usually)
    3. If external: Implement graceful degradation
  
  Escalation: Requires management + customer communication

All runbooks created: ✓ 3 critical runbooks

📋 ON-CALL SETUP:

Configure on-call rotation?
  [1] Yes, setup PagerDuty integration
  [2] Slack notifications only
  [3] Skip, manual setup

User: [1]

Configuring PagerDuty...
  ✓ Created service: signup-service-prod
  ✓ Escalation policy: On-call engineer → On-call manager
  ✓ Alert routing configured
  ✓ Slack integration enabled

✅ MONITORING SETUP COMPLETE

Dashboard: CloudWatch (signup-service-monitoring)
Alerts: 12 configured (8 critical, 4 warning)
Runbooks: 3 critical runbooks created
On-call: PagerDuty + Slack configured
Telemetry: CloudWatch Logs, Container Insights, X-Ray tracing

Monitoring is LIVE and monitoring v1.2.0 in production.

NEXT STEP?
  [1] View live dashboard
  [2] Test alert configuration
  [3] Continue to incident response
  [4] Done

User: [3]

See `/project:incident-response` to prepare incident automation.
```

## CLI Mode

```bash
$ sdlc skill monitoring AB#123 --service=signup-service
$ sdlc skill monitoring AB#123 --setup-alerts --platform=cloudwatch
$ sdlc skill monitoring AB#123 --create-runbooks
```

## Outputs

- **Monitoring Dashboard**: Grafana/CloudWatch/Datadog
- **Alert Configuration**: Thresholds + escalation policies
- **Runbooks**: Troubleshooting guides for common issues
- **On-call Setup**: PagerDuty + Slack integration

## G12 Gate Clear Conditions

Gate G12 is CLEAR when:
- Monitoring dashboard created and verified
- All critical alerts configured
- Runbooks written (3+ common issues)
- On-call rotation configured
- Alert testing passed (test alert → on-call receives)

## Next Commands

- `/project:incident-response AB#123` - Incident response automation
- `/project:retrospective AB#123` - Post-release retrospective
- New features: Continue to next SDLC cycle

---

## Model & Token Budget
- **Model Tier:** Sonnet (runbook generation)
- Input: ~1.5K tokens (story + NFRs)
- Output: ~2K tokens (runbooks + alert config)

