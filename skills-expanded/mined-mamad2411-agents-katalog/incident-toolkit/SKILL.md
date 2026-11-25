---
name: incident-toolkit
description: Consolidated toolkit for incident. Covers incident-runbook-templates, incident-response-smart-fix, incident-response-incident-response, incident-responder
---
# Incident Toolkit

## Use this skill when
- Building service-specific runbooks
- Creating incident response procedures
- Documenting recovery procedures
- Establishing escalation paths
- Needing guidance, best practices, or checklists for incident responder
- Needing guidance, best practices, or checklists for incident response incident response
- Needing guidance, best practices, or checklists for intelligent issue resolution with multi-agent orchestration
- Onboarding on-call engineers
- Responding to active incidents
- Working on incident responder tasks or workflows
- Working on incident response incident response tasks or workflows
- Working on intelligent issue resolution with multi-agent orchestration tasks or workflows

## Do not use this skill when
- The task is unrelated to incident responder
- The task is unrelated to incident response incident response
- The task is unrelated to incident runbook templates
- The task is unrelated to intelligent issue resolution with multi-agent orchestration
- You need a different domain or tool outside this scope

## Core Capabilities
# Incident Toolkit

# Incident Runbook Templates

Production-ready templates for incident response runbooks covering detection, triage, mitigation, resolution, and communication.

## Core Concepts

### 1. Incident Severity Levels

| Severity | Impact | Response Time | Example |
|----------|--------|---------------|---------|
| **SEV1** | Complete outage, data loss | 15 min | Production down |
| **SEV2** | Major degradation | 30 min | Critical feature broken |
| **SEV3** | Minor impact | 2 hours | Non-critical bug |
| **SEV4** | Minimal impact | Next business day | Cosmetic issue |

### 2. Runbook Structure

```
1. Overview & Impact
2. Detection & Alerts
3. Initial Triage
4. Mitigation Steps
5. Root Cause Investigation
6. Resolution Procedures
7. Verification & Rollback
8. Communication Templates
9. Escalation Matrix
```

## Runbook Templates

### Template 1: Service Outage Runbook

```markdown
# [Service Name] Outage Runbook

## Overview
**Service**: Payment Processing Service
**Owner**: Platform Team
**Slack**: #payments-incidents
**PagerDuty**: payments-oncall

## Impact Assessment
- [ ] Which customers are affected?
- [ ] What percentage of traffic is impacted?
- [ ] Are there financial implications?
- [ ] What's the blast radius?

## Detection
### Alerts
- `payment_error_rate > 5%` (PagerDuty)
- `payment_latency_p99 > 2s` (Slack)
- `payment_success_rate < 95%` (PagerDuty)

### Dashboards
- [Payment Service Dashboard](https://grafana/d/payments)
- [Error Tracking](https://sentry.io/payments)
- [Dependency Status](https://status.stripe.com)

## Initial Triage (First 5 Minutes)

### 1. Assess Scope
```bash
# Check service health
kubectl get pods -n payments -l app=payment-service

# Check recent deployments
kubectl rollout history deployment/payment-service -n payments

# Check error rates
curl -s "http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total{status=~'5..'}[5m]))"
```

### 2. Quick Health Checks
- [ ] Can you reach the service? `curl -I https://api.company.com/payments/health`
- [ ] Database connectivity? Check connection pool metrics
- [ ] External dependencies? Check Stripe, bank API status
- [ ] Recent changes? Check deploy history

### 3. Initial Classification
| Symptom | Likely Cause | Go To Section |
|---------|--------------|---------------|
| All requests failing | Service down | Section 4.1 |
| High latency | Database/dependency | Section 4.2 |
| Partial failures | Code bug | Section 4.3 |
| Spike in errors | Traffic surge | Section 4.4 |

## Mitigation Procedures

### 4.1 Service Completely Down
```bash
# Step 1: Check pod status
kubectl get pods -n payments

# Step 2: If pods are crash-looping, check logs
kubectl logs -n payments -l app=payment-service --tail=100

# Step 3: Check recent deployments
kubectl rollout history deployment/payment-service -n payments

# Step 4: ROLLBACK if recent deploy is suspect
kubectl rollout undo deployment/payment-service -n payments

# Step 5: Scale up if resource constrained
kubectl scale deployment/payment-service -n payments --replicas=10

# Step 6: Verify recovery
kubectl rollout status deployment/payment-service -n payments
```

### 4.2 High Latency
```bash
# Step 1: Check database connections
kubectl exec -n payments deploy/payment-service -- \
  curl localhost:8080/metrics | grep db_pool

# Step 2: Check slow queries (if DB issue)
psql -h $DB_HOST -U $DB_USER -c "
  SELECT pid, now() - query_start AS duration, query
  FROM pg_stat_activity
  WHERE state = 'active' AND duration > interval '5 seconds'
  ORDER BY duration DESC;"

# Step 3: Kill long-running queries if needed
psql -h $DB_HOST -U $DB_USER -c "SELECT pg_terminate_backend(pid);"

# Step 4: Check external dependency latency
curl -w "@curl-format.txt" -o /dev/null -s https://api.stripe.com/v1/health

# Step 5: Enable circuit breaker if dependency is slow
kubectl set env deployment/payment-service \
  STRIPE_CIRCUIT_BREAKER_ENABLED=true -n payments
```

### 4.3 Partial Failures (Specific Errors)
```bash
# Step 1: Identify error pattern
kubectl logs -n payments -l app=payment-service --tail=500 | \
  grep -i error | sort | uniq -c | sort -rn | head -20

# Step 2: Check error tracking
# Go to Sentry: https://sentry.io/payments

# Step 3: If specific endpoint, enable feature flag to disable
curl -X POST https://api.company.com/internal/feature-flags \
  -d '{"flag": "DISABLE_PROBLEMATIC_FEATURE", "enabled": true}'

# Step 4: If data issue, check recent data changes
psql -h $DB_HOST -c "
  SELECT * FROM audit_log
  WHERE table_name = 'payment_methods'
  AND created_at > now() - interval '1 hour';"
```

### 4.4 Traffic Surge
```bash
# Step 1: Check current request rate
kubectl top pods -n payments

# Step 2: Scale horizontally
kubectl scale deployment/payment-service -n payments --replicas=20

# Step 3: Enable rate limiting
kubectl set env deployment/payment-service \
  RATE_LIMIT_ENABLED=true \
  RATE_LIMIT_RPS=1000 -n payments

# Step 4: If attack, block suspicious IPs
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-suspicious
  namespace: payments
spec:
  podSelector:
    matchLabels:
      app: payment-service
  ingress:
  - from:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 192.168.1.0/24  # Suspicious range
EOF
```

## Verification Steps
```bash
# Verify service is healthy
curl -s https://api.company.com/payments/health | jq

# Verify error rate is back to normal
curl -s "http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total{status=~'5..'}[5m]))" | jq '.data.result[0].value[1]'

# Verify latency is acceptable
curl -s "http://prometheus:9090/api/v1/query?query=histogram_quantile(0.99,sum(rate(http_request_duration_seconds_bucket[5m]))by(le))" | jq

# Smoke test critical flows
./scripts/smoke-test-payments.sh
```

## Rollback Procedures
```bash
# Rollback Kubernetes deployment
kubectl rollout undo deployment/payment-service -n payments

# Rollback database migration (if applicable)
./scripts/db-rollback.sh $MIGRATION_VERSION

# Rollback feature flag
curl -X POST https://api.company.com/internal/feature-flags \
  -d '{"flag": "NEW_PAYMENT_FLOW", "enabled": false}'
```

## Escalation Matrix

| Condition | Escalate To | Contact |
|-----------|-------------|---------|
| > 15 min unresolved SEV1 | Engineering Manager | @manager (Slack) |
| Data breach suspected | Security Team | #security-incidents |
| Financial impact > $10k | Finance + Legal | @finance-oncall |
| Customer communication needed | Support Lead | @support-lead |

## Communication Templates

### Initial Notification (Internal)
```
🚨 INCIDENT: Payment Service Degradation

Severity: SEV2
Status: Investigating
Impact: ~20% of payment requests failing
Start Time: [TIME]
Incident Commander: [NAME]

Current Actions:
- Investigating root cause
- Scaling up service
- Monitoring dashboards

Updates in #payments-incidents
```

### Status Update
```
📊 UPDATE: Payment Service Incident

Status: Mitigating
Impact: Reduced to ~5% failure rate
Duration: 25 minutes

Actions Taken:
- Rolled back deployment v2.3.4 → v2.3.3
- Scaled service from 5 → 10 replicas

Next Steps:
- Continuing to monitor
- Root cause analysis in progress

ETA to Resolution: ~15 minutes
```

### Resolution Notification
```
✅ RESOLVED: Payment Service Incident

Duration: 45 minutes
Impact: ~5,000 affected transactions
Root Cause: Memory leak in v2.3.4

Resolution:
- Rolled back to v2.3.3
- Transactions auto-retried successfully

Follow-up:
- Postmortem scheduled for [DATE]
- Bug fix in progress
```
```

### Template 2: Database Incident Runbook

```markdown
# Database Incident Runbook

## Quick Reference
| Issue | Command |
|-------|---------|
| Check connections | `SELECT count(*) FROM pg_stat_activity;` |
| Kill query | `SELECT pg_terminate_backend(pid);` |
| Check replication lag | `SELECT extract(epoch from (now() - pg_last_xact_replay_timestamp()));` |
| Check locks | `SELECT * FROM pg_locks WHERE NOT granted;` |

## Connection Pool Exhaustion
```sql
-- Check current connections
SELECT datname, usename, state, count(*)
FROM pg_stat_activity
GROUP BY datname, usename, state
ORDER BY count(*) DESC;

-- Identify long-running connections
SELECT pid, usename, datname, state, query_start, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- Terminate idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND query_start < now() - interval '10 minutes';
```

## Replication Lag
```sql
-- Check lag on replica
SELECT
  CASE
    WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() THEN 0
    ELSE extract(epoch from now() - pg_last_xact_replay_timestamp())
  END AS lag_seconds;

-- If lag > 60s, consider:
-- 1. Check network between primary/replica
-- 2. Check replica disk I/O
-- 3. Consider failover if unrecoverable
```

## Disk Space Critical
```bash
# Check disk usage
df -h /var/lib/postgresql/data

# Find large tables
psql -c "SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;"

# VACUUM to reclaim space
psql -c "VACUUM FULL large_table;"

# If emergency, delete old data or expand disk
```
```

## Best Practices

### Do's
- **Keep runbooks updated** - Review after every incident
- **Test runbooks regularly** - Game days, chaos engineering
- **Include rollback steps** - Always have an escape hatch
- **Document assumptions** - What must be true for steps to work
- **Link to dashboards** - Quick access during stress

### Don'ts
- **Don't assume knowledge** - Write for 3 AM brain
- **Don't skip verification** - Confirm each step worked
- **Don't forget communication** - Keep stakeholders informed
- **Don't work alone** - Escalate early
- **Don't skip postmortems** - Learn from every incident

## Resources

- [Google SRE Book - Incident Management](https://sre.google/sre-book/managing-incidents/)
- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Atlassian Incident Management](https://www.atlassian.com/incident-management)

---

# Intelligent Issue Resolution with Multi-Agent Orchestration

[Extended thinking: This workflow implements a sophisticated debugging and resolution pipeline that leverages AI-assisted debugging tools and observability platforms to systematically diagnose and resolve production issues. The intelligent debugging strategy combines automated root cause analysis with human expertise, using modern 2024/2025 practices including AI code assistants (GitHub Copilot, Claude Code), observability platforms (Sentry, DataDog, OpenTelemetry), git bisect automation for regression tracking, and production-safe debugging techniques like distributed tracing and structured logging. The process follows a rigorous four-phase approach: (1) Issue Analysis Phase - error-detective and debugger agents analyze error traces, logs, reproduction steps, and observability data to understand the full context of the failure including upstream/downstream impacts, (2) Root Cause Investigation Phase - debugger and code-reviewer agents perform deep code analysis, automated git bisect to identify introducing commit, dependency compatibility checks, and state inspection to isolate the exact failure mechanism, (3) Fix Implementation Phase - domain-specific agents (python-pro, typescript-pro, rust-expert, etc.) implement minimal fixes with comprehensive test coverage including unit, integration, and edge case tests while following production-safe practices, (4) Verification Phase - test-automator and performance-engineer agents run regression suites, performance benchmarks, security scans, and verify no new issues are introduced. Complex issues spanning multiple systems require orchestrated coordination between specialist agents (database-optimizer → performance-engineer → devops-troubleshooter) with explicit context passing and state sharing. The workflow emphasizes understanding root causes over treating symptoms, implementing lasting architectural improvements, automating detection through enhanced monitoring and alerting, and preventing future occurrences through type system enhancements, static analysis rules, and improved error handling patterns. Success is measured not just by issue resolution but by reduced mean time to recovery (MTTR), prevention of similar issues, and improved system resilience.]

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

---

## Configuration

### Severity Levels
- **P0/SEV-1**: Complete outage, security breach, data loss - immediate all-hands response
- **P1/SEV-2**: Major degradation, significant user impact - rapid response required
- **P2/SEV-3**: Minor degradation, limited impact - standard response
- **P3/SEV-4**: Cosmetic issues, no user impact - scheduled resolution

### Incident Types
- Performance degradation
- Service outage
- Security incident
- Data integrity issue
- Infrastructure failure
- Third-party service disruption

## Phase 1: Detection & Triage

### 1. Incident Detection and Classification
- Use Task tool with subagent_type="incident-responder"
- Prompt: "URGENT: Detect and classify incident: $ARGUMENTS. Analyze alerts from PagerDuty/Opsgenie/monitoring. Determine: 1) Incident severity (P0-P3), 2) Affected services and dependencies, 3) User impact and business risk, 4) Initial incident command structure needed. Check error budgets and SLO violations."
- Output: Severity classification, impact assessment, incident command assignments, SLO status
- Context: Initial alerts, monitoring dashboards, recent changes

### 2. Observability Analysis
- Use Task tool with subagent_type="observability-monitoring::observability-engineer"
- Prompt: "Perform rapid observability sweep for incident: $ARGUMENTS. Query: 1) Distributed tracing (OpenTelemetry/Jaeger), 2) Metrics correlation (Prometheus/Grafana/DataDog), 3) Log aggregation (ELK/Splunk), 4) APM data, 5) Real User Monitoring. Identify anomalies, error patterns, and service degradation points."
- Output: Observability findings, anomaly detection, service health matrix, trace analysis
- Context: Severity level from step 1, affected services

### 3. Initial Mitigation
- Use Task tool with subagent_type="incident-responder"
- Prompt: "Implement immediate mitigation for P$SEVERITY incident: $ARGUMENTS. Actions: 1) Traffic throttling/rerouting if needed, 2) Feature flag disabling for affected features, 3) Circuit breaker activation, 4) Rollback assessment for recent deployments, 5) Scale resources if capacity-related. Prioritize user experience restoration."
- Output: Mitigation actions taken, temporary fixes applied, rollback decisions
- Context: Observability findings, severity classification

## Phase 2: Investigation & Root Cause Analysis

### 4. Deep System Debugging
- Use Task tool with subagent_type="error-debugging::debugger"
- Prompt: "Conduct deep debugging for incident: $ARGUMENTS using observability data. Investigate: 1) Stack traces and error logs, 2) Database query performance and locks, 3) Network latency and timeouts, 4) Memory leaks and CPU spikes, 5) Dependency failures and cascading errors. Apply Five Whys analysis."
- Output: Root cause identification, contributing factors, dependency impact map
- Context: Observability analysis, mitigation status

### 5. Security Assessment
- Use Task tool with subagent_type="security-scanning::security-auditor"
- Prompt: "Assess security implications of incident: $ARGUMENTS. Check: 1) DDoS attack indicators, 2) Authentication/authorization failures, 3) Data exposure risks, 4) Certificate issues, 5) Suspicious access patterns. Review WAF logs, security groups, and audit trails."
- Output: Security assessment, breach analysis, vulnerability identification
- Context: Root cause findings, system logs

### 6. Performance Engineering Analysis
- Use Task tool with subagent_type="application-performance::performance-engineer"
- Prompt: "Analyze performance aspects of incident: $ARGUMENTS. Examine: 1) Resource utilization patterns, 2) Query optimization opportunities, 3) Caching effectiveness, 4) Load balancer health, 5) CDN performance, 6) Autoscaling triggers. Identify bottlenecks and capacity issues."
- Output: Performance bottlenecks, resource recommendations, optimization opportunities
- Context: Debug findings, current mitigation state

## Phase 3: Resolution & Recovery

### 7. Fix Implementation
- Use Task tool with subagent_type="backend-development::backend-architect"
- Prompt: "Design and implement production fix for incident: $ARGUMENTS based on root cause. Requirements: 1) Minimal viable fix for rapid deployment, 2) Risk assessment and rollback capability, 3) Staged rollout plan with monitoring, 4) Validation criteria and health checks. Consider both immediate fix and long-term solution."
- Output: Fix implementation, deployment strategy, validation plan, rollback procedures
- Context: Root cause analysis, performance findings, security assessment

### 8. Deployment and Validation
- Use Task tool with subagent_type="deployment-strategies::deployment-engineer"
- Prompt: "Execute emergency deployment for incident fix: $ARGUMENTS. Process: 1) Blue-green or canary deployment, 2) Progressive rollout with monitoring, 3) Health check validation at each stage, 4) Rollback triggers configured, 5) Real-time monitoring during deployment. Coordinate with incident command."
- Output: Deployment status, validation results, monitoring dashboard, rollback readiness
- Context: Fix implementation, current system state

## Phase 4: Communication & Coordination

### 9. Stakeholder Communication
- Use Task tool with subagent_type="content-marketing::content-marketer"
- Prompt: "Manage incident communication for: $ARGUMENTS. Create: 1) Status page updates (public-facing), 2) Internal engineering updates (technical details), 3) Executive summary (business impact/ETA), 4) Customer support briefing (talking points), 5) Timeline documentation with key decisions. Update every 15-30 minutes based on severity."
- Output: Communication artifacts, status updates, stakeholder briefings, timeline log
- Context: All previous phases, current resolution status

### 10. Customer Impact Assessment
- Use Task tool with subagent_type="incident-responder"
- Prompt: "Assess and document customer impact for incident: $ARGUMENTS. Analyze: 1) Affected user segments and geography, 2) Failed transactions or data loss, 3) SLA violations and contractual implications, 4) Customer support ticket volume, 5) Revenue impact estimation. Prepare proactive customer outreach list."
- Output: Customer impact report, SLA analysis, outreach recommendations
- Context: Resolution progress, communication status

## Phase 5: Postmortem & Prevention

### 11. Blameless Postmortem
- Use Task tool with subagent_type="documentation-generation::docs-architect"
- Prompt: "Conduct blameless postmortem for incident: $ARGUMENTS. Document: 1) Complete incident timeline with decisions, 2) Root cause and contributing factors (systems focus), 3) What went well in response, 4) What could improve, 5) Action items with owners and deadlines, 6) Lessons learned for team education. Follow SRE postmortem best practices."
- Output: Postmortem document, action items list, process improvements, training needs
- Context: Complete incident history, all agent outputs

### 12. Monitoring and Alert Enhancement
- Use Task tool with subagent_type="observability-monitoring::observability-engineer"
- Prompt: "Enhance monitoring to prevent recurrence of: $ARGUMENTS. Implement: 1) New alerts for early detection, 2) SLI/SLO adjustments if needed, 3) Dashboard improvements for visibility, 4) Runbook automation opportunities, 5) Chaos engineering scenarios for testing. Ensure alerts are actionable and reduce noise."
- Output: New monitoring configuration, alert rules, dashboard updates, runbook automation
- Context: Postmortem findings, root cause analysis

### 13. System Hardening
- Use Task tool with subagent_type="backend-development::backend-architect"
- Prompt: "Design system improvements to prevent incident: $ARGUMENTS. Propose: 1) Architecture changes for resilience (circuit breakers, bulkheads), 2) Graceful degradation strategies, 3) Capacity planning adjustments, 4) Technical debt prioritization, 5) Dependency reduction opportunities. Create implementation roadmap."
- Output: Architecture improvements, resilience patterns, technical debt items, roadmap
- Context: Postmortem action items, performance analysis

## Success Criteria

### Immediate Success (During Incident)
- Service restoration within SLA targets
- Accurate severity classification within 5 minutes
- Stakeholder communication every 15-30 minutes
- No cascading failures or incident escalation
- Clear incident command structure maintained

### Long-term Success (Post-Incident)
- Comprehensive postmortem within 48 hours
- All action items assigned with deadlines
- Monitoring improvements deployed within 1 week
- Runbook updates completed
- Team training conducted on lessons learned
- Error budget impact assessed and communicated

## Coordination Protocols

### Incident Command Structure
- **Incident Commander**: Decision authority, coordination
- **Technical Lead**: Technical investigation and resolution
- **Communications Lead**: Stakeholder updates
- **Subject Matter Experts**: Specific system expertise

### Communication Channels
- War room (Slack/Teams channel or Zoom)
- Status page updates (StatusPage, Statusly)
- PagerDuty/Opsgenie for alerting
- Confluence/Notion for documentation

### Handoff Requirements
- Each phase provides clear context to the next
- All findings documented in shared incident doc
- Decision rationale recorded for postmortem
- Timestamp all significant events

Production incident requiring immediate response: $ARGUMENTS

---

## Purpose
Expert incident responder with deep knowledge of SRE principles, modern observability, and incident management frameworks. Masters rapid problem resolution, effective communication, and comprehensive post-incident analysis. Specializes in building resilient systems and improving organizational incident response capabilities.

## Immediate Actions (First 5 minutes)

### 1. Assess Severity & Impact
- **User impact**: Affected user count, geographic distribution, user journey disruption
- **Business impact**: Revenue loss, SLA violations, customer experience degradation
- **System scope**: Services affected, dependencies, blast radius assessment
- **External factors**: Peak usage times, scheduled events, regulatory implications

### 2. Establish Incident Command
- **Incident Commander**: Single decision-maker, coordinates response
- **Communication Lead**: Manages stakeholder updates and external communication
- **Technical Lead**: Coordinates technical investigation and resolution
- **War room setup**: Communication channels, video calls, shared documents

### 3. Immediate Stabilization
- **Quick wins**: Traffic throttling, feature flags, circuit breakers
- **Rollback assessment**: Recent deployments, configuration changes, infrastructure changes
- **Resource scaling**: Auto-scaling triggers, manual scaling, load redistribution
- **Communication**: Initial status page update, internal notifications

## Modern Investigation Protocol

### Observability-Driven Investigation
- **Distributed tracing**: OpenTelemetry, Jaeger, Zipkin for request flow analysis
- **Metrics correlation**: Prometheus, Grafana, DataDog for pattern identification
- **Log aggregation**: ELK, Splunk, Loki for error pattern analysis
- **APM analysis**: Application performance monitoring for bottleneck identification
- **Real User Monitoring**: User experience impact assessment

### SRE Investigation Techniques
- **Error budgets**: SLI/SLO violation analysis, burn rate assessment
- **Change correlation**: Deployment timeline, configuration changes, infrastructure modifications
- **Dependency mapping**: Service mesh analysis, upstream/downstream impact assessment
- **Cascading failure analysis**: Circuit breaker states, retry storms, thundering herds
- **Capacity analysis**: Resource utilization, scaling limits, quota exhaustion

### Advanced Troubleshooting
- **Chaos engineering insights**: Previous resilience testing results
- **A/B test correlation**: Feature flag impacts, canary deployment issues
- **Database analysis**: Query performance, connection pools, replication lag
- **Network analysis**: DNS issues, load balancer health, CDN problems
- **Security correlation**: DDoS attacks, authentication issues, certificate problems

## Communication Strategy

### Internal Communication
- **Status updates**: Every 15 minutes during active incident
- **Technical details**: For engineering teams, detailed technical analysis
- **Executive updates**: Business impact, ETA, resource requirements
- **Cross-team coordination**: Dependencies, resource sharing, expertise needed

### External Communication
- **Status page updates**: Customer-facing incident status
- **Support team briefing**: Customer service talking points
- **Customer communication**: Proactive outreach for major customers
- **Regulatory notification**: If required by compliance frameworks

### Documentation Standards
- **Incident timeline**: Detailed chronology with timestamps
- **Decision rationale**: Why specific actions were taken
- **Impact metrics**: User impact, business metrics, SLA violations
- **Communication log**: All stakeholder communications

## Resolution & Recovery

### Fix Implementation
1. **Minimal viable fix**: Fastest path to service restoration
2. **Risk assessment**: Potential side effects, rollback capability
3. **Staged rollout**: Gradual fix deployment with monitoring
4. **Validation**: Service health checks, user experience validation
5. **Monitoring**: Enhanced monitoring during recovery phase

### Recovery Validation
- **Service health**: All SLIs back to normal thresholds
- **User experience**: Real user monitoring validation
- **Performance metrics**: Response times, throughput, error rates
- **Dependency health**: Upstream and downstream service validation
- **Capacity headroom**: Sufficient capacity for normal operations

## Post-Incident Process

### Immediate Post-Incident (24 hours)
- **Service stability**: Continued monitoring, alerting adjustments
- **Communication**: Resolution announcement, customer updates
- **Data collection**: Metrics export, log retention, timeline documentation
- **Team debrief**: Initial lessons learned, emotional support

### Blameless Post-Mortem
- **Timeline analysis**: Detailed incident timeline with contributing factors
- **Root cause analysis**: Five whys, fishbone diagrams, systems thinking
- **Contributing factors**: Human factors, process gaps, technical debt
- **Action items**: Prevention measures, detection improvements, response enhancements
- **Follow-up tracking**: Action item completion, effectiveness measurement

### System Improvements
- **Monitoring enhancements**: New alerts, dashboard improvements, SLI adjustments
- **Automation opportunities**: Runbook automation, self-healing systems
- **Architecture improvements**: Resilience patterns, redundancy, graceful degradation
- **Process improvements**: Response procedures, communication templates, training
- **Knowledge sharing**: Incident learnings, updated documentation, team training

## Modern Severity Classification

### P0 - Critical (SEV-1)
- **Impact**: Complete service outage or security breach
- **Response**: Immediate, 24/7 escalation
- **SLA**: < 15 minutes acknowledgment, < 1 hour resolution
- **Communication**: Every 15 minutes, executive notification

### P1 - High (SEV-2)
- **Impact**: Major functionality degraded, significant user impact
- **Response**: < 1 hour acknowledgment
- **SLA**: < 4 hours resolution
- **Communication**: Hourly updates, status page update

### P2 - Medium (SEV-3)
- **Impact**: Minor functionality affected, limited user impact
- **Response**: < 4 hours acknowledgment
- **SLA**: < 24 hours resolution
- **Communication**: As needed, internal updates

### P3 - Low (SEV-4)
- **Impact**: Cosmetic issues, no user impact
- **Response**: Next business day
- **SLA**: < 72 hours resolution
- **Communication**: Standard ticketing process

## SRE Best Practices

### Error Budget Management
- **Burn rate analysis**: Current error budget consumption
- **Policy enforcement**: Feature freeze triggers, reliability focus
- **Trade-off decisions**: Reliability vs. velocity, resource allocation

### Reliability Patterns
- **Circuit breakers**: Automatic failure detection and isolation
- **Bulkhead pattern**: Resource isolation to prevent cascading failures
- **Graceful degradation**: Core functionality preservation during failures
- **Retry policies**: Exponential backoff, jitter, circuit breaking

### Continuous Improvement
- **Incident metrics**: MTTR, MTTD, incident frequency, user impact
- **Learning culture**: Blameless culture, psychological safety
- **Investment prioritization**: Reliability work, technical debt, tooling
- **Training programs**: Incident response, on-call best practices

## Modern Tools & Integration

### Incident Management Platforms
- **PagerDuty**: Alerting, escalation, response coordination
- **Opsgenie**: Incident management, on-call scheduling
- **ServiceNow**: ITSM integration, change management correlation
- **Slack/Teams**: Communication, chatops, automated updates

### Observability Integration
- **Unified dashboards**: Single pane of glass during incidents
- **Alert correlation**: Intelligent alerting, noise reduction
- **Automated diagnostics**: Runbook automation, self-service debugging
- **Incident replay**: Time-travel debugging, historical analysis

## Behavioral Traits
- Acts with urgency while maintaining precision and systematic approach
- Prioritizes service restoration over root cause analysis during active incidents
- Communicates clearly and frequently with appropriate technical depth for audience
- Documents everything for learning and continuous improvement
- Follows blameless culture principles focusing on systems and processes
- Makes data-driven decisions based on observability and metrics
- Considers both immediate fixes and long-term system improvements
- Coordinates effectively across teams and maintains incident command structure
- Learns from every incident to improve system reliability and response processes

## Response Principles
- **Speed matters, but accuracy matters more**: A wrong fix can exponentially worsen the situation
- **Communication is critical**: Stakeholders need regular updates with appropriate detail
- **Fix first, understand later**: Focus on service restoration before root cause analysis
- **Document everything**: Timeline, decisions, and lessons learned are invaluable
- **Learn and improve**: Every incident is an opportunity to build better systems

Remember: Excellence in incident response comes from preparation, practice, and continuous improvement of both technical systems and human processes.

---
