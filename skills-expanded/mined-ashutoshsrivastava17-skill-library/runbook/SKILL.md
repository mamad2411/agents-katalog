---
name: runbook
description: >
  Create an operational runbook for a system, service, or process. Covers normal operations,
  incident response, troubleshooting decision trees, and maintenance procedures.
  TRIGGER when: user asks to create a runbook, document operational procedures,
  write on-call playbook, create incident response procedures, or document system operations.
argument-hint: "<system or service name>"
user-invocable: true
---

# Operational Runbook

You are a site reliability engineer and operations specialist. Create a comprehensive runbook that enables any on-call engineer to operate, monitor, troubleshoot, and recover the system or service.

## Discovery Questions

| Category | Questions |
|----------|-----------|
| **System** | What system or service is this for? What does it do? |
| **Architecture** | What are the components? What are the dependencies? |
| **Criticality** | What is the business impact of downtime? (Tier 1/2/3) |
| **Users** | Who uses this runbook? What is their expertise level? |
| **SLAs** | What are the uptime and response time commitments? |
| **On-call** | Who is on call? What is the escalation chain? |

## Output Format

### Runbook Header

| Field | Value |
|-------|-------|
| **Service Name** | [Name] |
| **Document ID** | RB-[SVC]-[NNN] |
| **Version** | 1.0 |
| **Last Updated** | [Date] |
| **Owner** | [Team / Individual] |
| **Criticality** | Tier 1 (Critical) / Tier 2 (Important) / Tier 3 (Standard) |
| **SLA** | [Uptime target, e.g., 99.9%] |

### 1. Service Overview

- **Purpose**: What the service does in 2-3 sentences
- **Users**: Who depends on this service
- **Business Impact**: What happens if this service is down
- **Architecture Diagram**: `[Diagram: high-level architecture]`

### 2. Key Information

| Item | Value |
|------|-------|
| **Production URL(s)** | ... |
| **Dashboard(s)** | ... |
| **Log Location** | ... |
| **Config Location** | ... |
| **Source Repository** | ... |
| **CI/CD Pipeline** | ... |
| **Infrastructure** | Cloud provider, region, account |
| **Database** | Type, host, connection details reference |
| **Message Queue** | Type, cluster details |
| **CDN / Load Balancer** | ... |

### 3. Contacts & Escalation

| Level | Contact | Method | Response Time |
|-------|---------|--------|--------------|
| **L1 - On Call** | [Rotation name] | PagerDuty / Slack #channel | 15 min |
| **L2 - Team Lead** | [Name] | Phone / Slack | 30 min |
| **L3 - Engineering Manager** | [Name] | Phone | 1 hour |
| **L4 - VP Engineering** | [Name] | Phone | As needed |
| **External - Vendor Support** | [Vendor] | Support portal / Phone | Per SLA |

### 4. Monitoring & Alerting

| Alert Name | Condition | Severity | Dashboard | Runbook Section |
|-----------|-----------|----------|-----------|----------------|
| High Error Rate | Error rate > 1% for 5 min | P1 | [Link] | 6.1 |
| High Latency | p99 > 2s for 5 min | P2 | [Link] | 6.2 |
| Low Throughput | QPS < X for 10 min | P2 | [Link] | 6.3 |
| Disk Usage High | > 85% | P3 | [Link] | 6.4 |
| Health Check Failing | 3 consecutive failures | P1 | [Link] | 6.5 |

### 5. Normal Operations

#### 5.1 Deployment

| Step | Action | Command / Procedure | Verification |
|------|--------|-------------------|-------------|
| 1 | Pre-deploy checks | `[command]` | All green |
| 2 | Deploy to staging | `[command]` | Smoke tests pass |
| 3 | Deploy to production | `[command]` | Health checks pass |
| 4 | Monitor | Check dashboard for 15 min | No anomalies |
| 5 | Rollback (if needed) | `[command]` | Previous version restored |

#### 5.2 Scaling

| Scenario | Action | Command | Limits |
|----------|--------|---------|--------|
| Scale up | Add instances | `[command]` | Max: X instances |
| Scale down | Remove instances | `[command]` | Min: Y instances |
| Auto-scaling | Adjust thresholds | `[command]` | CPU: 70%, Memory: 80% |

#### 5.3 Routine Maintenance

| Task | Frequency | Procedure | Estimated Duration |
|------|-----------|-----------|-------------------|
| Log rotation | Daily (automated) | Verify via `[command]` | N/A |
| Certificate renewal | 90 days | [Procedure] | 15 min |
| Dependency updates | Monthly | [Procedure] | 1-2 hours |
| Database maintenance | Weekly | [Procedure] | 30 min |
| Backup verification | Weekly | [Procedure] | 15 min |

### 6. Troubleshooting

For each common issue, provide a decision tree:

#### 6.1 High Error Rate

```
Is the error rate above threshold?
├── YES: Check recent deployments
│   ├── Recent deploy found → Rollback (Section 5.1, Step 5)
│   └── No recent deploy → Check dependencies
│       ├── Dependency down → See dependency runbook / Contact vendor
│       └── Dependencies healthy → Check application logs
│           ├── Known error pattern → Apply known fix (see table below)
│           └── Unknown error → Escalate to L2
└── NO: Monitor, likely transient
```

**Known Error Patterns**:

| Error | Cause | Fix | Prevention |
|-------|-------|-----|-----------|
| Connection timeout to DB | Connection pool exhausted | Restart pods / Increase pool | Tune pool size |
| OOM Kill | Memory leak or traffic spike | Restart + scale up | Set memory limits |
| 503 Service Unavailable | Upstream dependency failure | Check dependency status | Circuit breaker |

#### 6.2 High Latency

Provide similar decision tree format...

#### 6.3 Service Down

Provide similar decision tree format...

### 7. Incident Response

| Severity | Definition | Response Time | Communication |
|----------|-----------|--------------|---------------|
| **SEV-1** | Complete outage, all users affected | Immediate | Incident channel + status page |
| **SEV-2** | Degraded service, many users affected | 15 min | Incident channel |
| **SEV-3** | Minor issue, few users affected | 1 hour | Team channel |
| **SEV-4** | Cosmetic or low-impact issue | Next business day | Ticket |

**Incident Commander Checklist**:
- [ ] Acknowledge alert and join incident channel
- [ ] Assess severity and confirm or adjust
- [ ] Assign roles: IC, Communications, Technical Lead
- [ ] Start incident timeline documentation
- [ ] Communicate initial status to stakeholders
- [ ] Coordinate investigation and remediation
- [ ] Update stakeholders every 30 min (SEV-1) or 60 min (SEV-2)
- [ ] Confirm resolution and monitor for recurrence
- [ ] Schedule post-incident review within 48 hours

### 8. Disaster Recovery

| Scenario | RPO | RTO | Procedure |
|----------|-----|-----|-----------|
| Single instance failure | 0 | 5 min | Auto-healing / Replacement |
| AZ failure | 0 | 15 min | Failover to secondary AZ |
| Region failure | < 1 hour | < 4 hours | Failover to DR region |
| Data corruption | < 1 hour | < 2 hours | Restore from backup |
| Complete infrastructure loss | < 24 hours | < 8 hours | Rebuild from IaC |

### 9. Useful Commands

```
# Health check
[command]

# View recent logs
[command]

# Check resource usage
[command]

# Restart service
[command]

# Force failover
[command]

# Check database connectivity
[command]
```

## Quality Standards

- Every alert must have a corresponding troubleshooting section
- Commands must be copy-paste ready with placeholders clearly marked
- Decision trees must cover the common cases (80/20 rule)
- Escalation paths must be current and tested
- Runbook must be tested by someone who did NOT write it
- Update the runbook after every incident that reveals a gap
- Include "last verified" dates for procedures that can go stale

## Edge Cases

- **New service with no history**: Start with architecture-based risk analysis for troubleshooting
- **Multi-tenant services**: Include tenant-specific isolation and debugging procedures
- **Stateful services**: Emphasize data integrity checks and quorum requirements
- **Third-party services**: Include vendor contact, SLA, and known limitations
- **Deprecated services**: Include decommission timeline and migration guidance
- **Services with on-prem and cloud components**: Document both environments clearly
