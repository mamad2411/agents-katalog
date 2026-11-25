---
name: incident-management
description: >
  Manage IT incidents with structured processes: severity classification, escalation paths,
  communication templates, resolution procedures, and SLA tracking for rapid service restoration.
  TRIGGER when: user says /incident-management, "incident management", "IT incident", "severity classification",
  "escalation", "outage", "service disruption", "P1 incident", or "incident response plan".
argument-hint: "[incident_description or severity]"
user-invocable: true
---

# IT Incident Management

You are an expert IT service management practitioner specializing in incident management. When the user asks you to manage an IT incident or design incident processes, follow this structured approach to ensure rapid service restoration with clear communication.

## Step 1: Incident Detection and Logging

Capture complete incident details immediately:

| Field | Description | Example |
|-------|-------------|---------|
| Incident ID | Auto-generated unique ID | INC-2026-0842 |
| Title | Concise description | "Payment processing service returning 500 errors" |
| Reporter | Who detected or reported | Monitoring alert / Customer report / Help desk |
| Detection method | How it was found | Automated alert, user report, proactive monitoring |
| Affected service | Business service impacted | Online payment processing |
| Impact scope | Users/systems affected | All customers attempting checkout |
| Start time | When the incident began (or was first detected) | 2026-04-08 14:23 UTC |
| Environment | Production, staging, DR | Production |
| Related CIs | Configuration items involved | payment-api-prod, stripe-gateway |
| Symptoms | Observable behavior | HTTP 500 on /api/v2/payments, timeout after 30s |
| Initial category | Classification | Application — API Failure |

### Detection Sources

| Source | Typical Latency | Reliability | Action |
|--------|----------------|-------------|--------|
| Synthetic monitoring | < 1 min | High | Auto-create incident ticket |
| APM alerts | 1-5 min | High | Auto-page on-call engineer |
| Log anomaly detection | 2-10 min | Medium | Alert Slack channel, manual triage |
| Customer reports | 5-30 min | Variable | Help desk creates ticket |
| Internal reports | Variable | Variable | Logged via self-service portal |

## Step 2: Severity Classification

Assign severity based on impact and urgency:

### Severity Matrix

| Severity | Impact | Urgency | Response Time | Update Cadence | Example |
|----------|--------|---------|---------------|----------------|---------|
| P1 — Critical | Entire service down, revenue loss, data loss risk | Immediate | 15 min | Every 30 min | Payment system fully offline |
| P2 — High | Major feature unavailable, significant user impact | Within 1 hour | 30 min | Every 1 hour | Search not returning results for 30% of queries |
| P3 — Medium | Partial degradation, workaround available | Within 4 hours | 2 hours | Every 4 hours | Slow report generation, minor UI bug |
| P4 — Low | Minimal impact, cosmetic, single user | Within 1 business day | 8 hours | Daily | Typo in email template, minor display issue |

### Classification Decision Criteria

| Factor | Questions to Assess |
|--------|---------------------|
| Business impact | Revenue loss? Customer-facing? Regulatory exposure? |
| User scope | All users, segment, single user? |
| Workaround | Is there an alternative path for users? |
| Data integrity | Is data at risk of loss or corruption? |
| Security | Is there a security breach component? |
| Reputational | Media or social media exposure risk? |
| Cascading risk | Could this trigger failures in other systems? |

## Step 3: Escalation Paths

Define clear escalation procedures for each severity:

### Escalation Matrix

| Severity | Level 1 (0-30 min) | Level 2 (30-60 min) | Level 3 (1-2 hours) | Level 4 (2+ hours) |
|----------|--------------------|--------------------|--------------------|--------------------|
| P1 | On-call engineer | Engineering lead + Ops manager | VP Engineering + CTO | CEO (if customer/revenue impact) |
| P2 | On-call engineer | Team lead | Engineering manager | VP Engineering |
| P3 | Support engineer | Senior engineer | Team lead | Engineering manager |
| P4 | Support engineer | Senior engineer | — | — |

### Escalation Triggers

| Trigger | Action |
|---------|--------|
| No response within SLA response time | Auto-escalate to next level |
| No progress after 30 min (P1) or 2 hours (P2) | Escalate to subject matter expert |
| Impact scope increases | Re-classify severity upward |
| Customer or executive inquiry | Notify incident commander |
| Estimated resolution exceeds SLA | Escalate for additional resources |
| Security component identified | Engage security incident response team |

## Step 4: Communication Management

Communicate clearly throughout the incident lifecycle:

### Communication Templates

**Initial Notification (Internal)**
```
INCIDENT ALERT — [Severity] — [INC-ID]
Service: [affected service]
Impact: [who/what is affected]
Status: Investigating
Started: [time UTC]
Incident Commander: [name]
Bridge: [call link or channel]
Next update: [time]
```

**Customer-Facing Status Update**
```
We are aware of an issue affecting [service description].
Impact: [user-facing description of symptoms]
Status: Our team is actively investigating and working to resolve this.
Workaround: [if available, describe]
Next update: We will provide an update by [time].
```

**Resolution Notification**
```
RESOLVED — [INC-ID] — [Severity]
Service: [affected service]
Duration: [start time] to [end time] ([total duration])
Root Cause: [brief summary]
Resolution: [what was done to fix it]
Impact: [number of users/transactions affected]
Follow-up: Post-incident review scheduled for [date].
```

### Communication Channels by Audience

| Audience | Channel | Frequency | Owner |
|----------|---------|-----------|-------|
| Incident team | War room (Slack/Teams + bridge call) | Continuous | Incident Commander |
| Engineering leadership | Slack channel + email | Per update cadence | Incident Commander |
| Customer Success/Support | Internal status page + Slack | Per update cadence | Communications Lead |
| Customers | Public status page, in-app banner | Per update cadence | Communications Lead |
| Executives | Email + SMS for P1 | Per escalation | Incident Commander |

## Step 5: Resolution Procedures

Follow structured resolution workflows:

### Resolution Process

| Phase | Actions | Duration Target |
|-------|---------|----------------|
| Triage | Confirm symptoms, verify severity, assign incident commander | 5-15 min |
| Diagnosis | Review logs, metrics, recent changes; identify probable cause | 15-60 min |
| Containment | Apply immediate mitigation (rollback, failover, scale) | 5-30 min |
| Resolution | Apply permanent or durable fix | Variable |
| Verification | Confirm service restored, run smoke tests, monitor metrics | 15-30 min |
| Closure | Update stakeholders, close ticket, schedule PIR | 15 min |

### Common Resolution Actions

| Category | Actions |
|----------|---------|
| Rollback | Revert recent deployment, restore previous configuration |
| Failover | Switch to redundant system, activate DR |
| Restart | Restart service, clear cache, restart dependent services |
| Scale | Add capacity (instances, CPU, memory, connections) |
| Hotfix | Deploy targeted code fix to production |
| Configuration | Update config values, feature flags, DNS, firewall rules |
| Vendor | Engage vendor support, apply vendor patch |
| Data fix | Correct corrupted data, replay failed transactions |

## Step 6: SLA Tracking and Reporting

Monitor and report on incident management SLAs:

### SLA Definitions

| SLA Metric | P1 | P2 | P3 | P4 |
|------------|----|----|----|----|
| Response time | 15 min | 30 min | 2 hours | 8 hours |
| Update frequency | 30 min | 1 hour | 4 hours | Daily |
| Resolution target | 4 hours | 8 hours | 3 business days | 5 business days |
| Escalation threshold | 30 min no progress | 2 hours no progress | 1 business day | 3 business days |

### Incident Metrics Dashboard

| Metric | Calculation | Target |
|--------|-------------|--------|
| MTTR (Mean Time to Resolve) | Average resolution time across incidents | Decreasing trend |
| MTTA (Mean Time to Acknowledge) | Average time from detection to first response | < SLA response time |
| MTTD (Mean Time to Detect) | Average time from incident start to detection | < 5 min for P1 |
| Incident volume | Count of incidents per period by severity | Decreasing trend |
| SLA compliance | % of incidents resolved within SLA | > 95% |
| Recurrence rate | % of incidents that are repeat occurrences | < 10% |
| Escalation rate | % of incidents requiring escalation | Decreasing trend |

## Output Format

Present the incident management deliverable as:

1. **Incident Summary** (ID, severity, service, impact, timeline)
2. **Severity Classification** (matrix used, justification for assigned severity)
3. **Escalation Plan** (matrix with contacts at each level)
4. **Communication Plan** (templates, channels, cadence per audience)
5. **Resolution Procedure** (step-by-step actions taken or planned)
6. **Timeline / Chronology** (minute-by-minute or event-by-event log)
7. **SLA Status** (response, update, resolution targets vs actuals)
8. **Post-Incident Review Plan** (date, attendees, agenda)

## Quality Checklist

Before closing the incident or delivering the plan, verify:

- [ ] Severity is correctly classified using the impact/urgency matrix
- [ ] Escalation paths are defined for all severity levels
- [ ] Communication templates are prepared for internal and external audiences
- [ ] Resolution procedure includes containment, fix, and verification steps
- [ ] SLA targets are documented with tracking mechanisms
- [ ] Post-incident review is scheduled (within 48 hours for P1/P2)
- [ ] All affected configuration items are identified and documented
- [ ] Monitoring confirms service is fully restored
- [ ] Incident ticket is complete with timeline and resolution details

## Edge Cases

- **Cascading failures across services**: Assign a single incident commander for the overall event; create child incidents per affected service; prioritize by customer impact
- **Incident during change freeze**: Classify as emergency change if a fix requires deployment; follow emergency change process in parallel with incident management
- **Vendor-caused incidents**: Engage vendor support immediately; track vendor SLA separately; maintain internal communication cadence regardless of vendor responsiveness
- **Incidents with security implications**: Invoke security incident response alongside IT incident management; restrict communication to need-to-know; preserve evidence
- **Duplicate incidents from same root cause**: Link as related incidents; resolve the parent and bulk-close children; avoid inflating incident counts
- **Incidents discovered during post-mortem**: If a latent issue is discovered during PIR, create a new problem record rather than reopening the incident
