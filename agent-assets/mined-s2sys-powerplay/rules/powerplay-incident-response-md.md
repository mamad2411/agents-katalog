---
name: incident-response
description: Incident response & post-mortems — IR playbooks, detection, response, communication, forensics, post-incident reviews
globs: ["**/*.md", "**/*.yaml", "**/*.yml", "**/*.tf"]
alwaysApply: false
---

# Incident Response & Post-Mortems

Security incidents are inevitable. Respond quickly, communicate clearly, investigate thoroughly, and improve continuously. A good IR playbook separates minor outages from major breaches.

---

## Incident Response Playbook

**ALWAYS**:
- Document all incidents (no matter severity)
- Follow IR playbook (don't improvise)
- Establish incident command (single decision maker)
- Set up war room (real-time communication)
- Gather evidence (preserve chain of custody)
- Communicate status regularly (internal + external)
- Isolate affected systems (prevent spread)
- Keep timeline of events (for post-mortem)

**NEVER**:
- Panic or make hasty decisions
- Delete logs (destroy evidence)
- Communicate before internal agreement
- Blame individuals (focus on systems)
- Downplay severity (be honest with stakeholders)

### ✅ GOOD Incident Response Playbook

```yaml
# Incident Response Playbook Structure

incident_response:
  severity_levels:
    # Severity 1: System-wide outage, data breach, RCE
    severity_1:
      response_time: "15 minutes"
      escalation: "CEO, CISO, Legal, Comms"
      actions:
        - "Declare incident (Slack #incident, PagerDuty)"
        - "Activate war room (Zoom call, Slack thread)"
        - "Establish incident commander (authority to make decisions)"
        - "Identify stakeholders (affected teams)"
        - "Begin evidence collection (logs, system state)"
        - "Assess: Is system still under attack?"
        - "Isolate if necessary (disconnect from internet)"
        - "Notify legal/compliance (required for data breach)"
      communication:
        - "Internal: Real-time Slack updates every 30 minutes"
        - "External: Status page update within 1 hour"
        - "Customer: Email within 2 hours (if data breach)"
      sla: "Declare resolved or escalate within 24 hours"
    
    # Severity 2: Major service degradation, unauthorized access
    severity_2:
      response_time: "1 hour"
      escalation: "VP Engineering, Security Lead"
      actions:
        - "Declare incident (Slack, page oncall)"
        - "Start war room"
        - "Assign incident commander"
        - "Begin diagnostics"
        - "Gather logs (immediate, full retention)"
      communication:
        - "Internal: Slack updates every 2 hours"
        - "External: Status page within 2 hours"
      sla: "Resolved or escalated within 8 hours"
    
    # Severity 3: Minor issues, limited impact
    severity_3:
      response_time: "4 hours"
      escalation: "Team lead"
      actions:
        - "Log incident (Slack thread)"
        - "Diagnose root cause"
        - "Implement fix"
      communication:
        - "Internal: Daily standup update"
        - "Status page: Daily"
      sla: "Resolved within 48 hours"

  incident_command_structure:
    incident_commander: "Single decision maker, has authority to override"
    communications_lead: "Internal updates, external messaging approval"
    technical_lead: "Diagnosis, mitigation, recovery"
    operations_lead: "System isolation, failover, resource allocation"
    legal_lead: "Compliance, breach notification, regulatory reporting"

  war_room_setup:
    communication: "Slack #incident + Zoom call"
    frequency: "Sync every 15 min (severity 1), hourly (severity 2)"
    documentation: "Live Google Doc with timeline, decisions, actions"
    roles: "Assigned at incident start, not during firefighting"
```

---

## Detection & Triage

**ALWAYS**:
- Monitor for anomalies (unusual traffic, error spikes, latency)
- Alert on thresholds (setup alerts before they trigger)
- Triage quickly (is this a real incident?)
- Classify severity (use playbook levels)
- Gather context (recent changes, deployments?)

**NEVER**:
- Ignore alerts (investigate every one)
- Escalate without context (know what you're escalating)
- Assume it's DNS (investigate fully)

### ✅ GOOD Incident Detection Setup

```yaml
# Monitoring & Alert Configuration (Prometheus + Alertmanager)

alert_rules:
  high_error_rate:
    expr: 'rate(http_requests_total{status=~"5.."}[5m]) > 0.05'
    for: '5m'
    labels:
      severity: 'critical'
    annotations:
      summary: 'High error rate: {{ $value | humanizePercentage }}'
      description: 'Service {{ $labels.service }} has error rate > 5% for 5 minutes'
      action: 'Check application logs, recent deployments, database connectivity'

  database_connection_failure:
    expr: 'pg_up == 0'
    for: '1m'
    labels:
      severity: 'critical'
    annotations:
      summary: 'Database unreachable'
      description: 'Cannot connect to {{ $labels.instance }}'
      action: 'Check database status, network connectivity, credentials'

  disk_space_low:
    expr: '(node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1'
    for: '10m'
    labels:
      severity: 'high'
    annotations:
      summary: 'Disk space low: {{ $value | humanizePercentage }} remaining'
      action: 'Expand disk, cleanup old logs/temp files'

  certificate_expiration:
    expr: 'ssl_certificate_expires_in_seconds < 604800'  # < 7 days
    labels:
      severity: 'high'
    annotations:
      summary: 'SSL certificate expires in {{ $value | humanizeDuration }}'
      action: 'Renew certificate immediately'

  unusual_api_pattern:
    expr: 'rate(api_requests_total[1m]) > 2 * avg_over_time(rate(api_requests_total[1m])[1d])'
    for: '10m'
    labels:
      severity: 'high'
    annotations:
      summary: 'Unusual API traffic pattern'
      description: 'Current request rate 2x higher than daily average'
      action: 'Check for DDoS, malicious bots, viral content, cache miss'

  unauthorized_access_attempts:
    expr: 'rate(auth_failed_total[5m]) > 100'
    for: '2m'
    labels:
      severity: 'critical'
    annotations:
      summary: 'High failed authentication rate'
      description: '{{ $value }} failed logins/sec'
      action: 'Check for credential stuffing, compromised password, API key leak'

  data_exfiltration_suspect:
    expr: 'rate(data_exported_bytes[5m]) > 1073741824'  # > 1GB/min
    for: '2m'
    labels:
      severity: 'critical'
    annotations:
      summary: 'Unusual data export volume'
      description: '{{ humanize $value }} bytes exported per second'
      action: 'Investigate who exported what data, check audit logs'
```

---

## Incident Response Steps

**ALWAYS**:
- **Detect** — Monitoring alerts fire
- **Declare** — Severity assigned, incident commander appointed
- **Diagnose** — Root cause investigation begins
- **Mitigate** — Temporary fix to restore service
- **Recover** — Permanent fix, full restoration
- **Communicate** — Stakeholder updates throughout
- **Document** — Timeline of events preserved
- **Review** — Post-mortem analysis completed

**NEVER**:
- Skip steps (follow process every time)
- Make decisions without incident commander
- Forget to communicate

### ✅ GOOD Incident Response Flow

```csharp
// Incident Response Orchestration
public class IncidentResponseService
{
    private readonly IIncidentStore _incidentStore;
    private readonly INotificationService _notificationService;
    private readonly ILoggingService _loggingService;
    
    public async Task DeclareIncidentAsync(
        IncidentSeverity severity,
        string title,
        string description)
    {
        // Step 1: Create incident record
        var incident = new SecurityIncident
        {
            Id = Guid.NewGuid().ToString(),
            Title = title,
            Description = description,
            Severity = severity,
            DeclaredAt = DateTime.UtcNow,
            Status = IncidentStatus.Active,
            Timeline = new List<IncidentEvent>
            {
                new IncidentEvent
                {
                    Time = DateTime.UtcNow,
                    Action = "Incident declared",
                    Details = description,
                    Actor = GetCurrentUser()
                }
            }
        };
        
        await _incidentStore.CreateAsync(incident);
        
        // Step 2: Assign incident commander
        var commander = severity switch
        {
            IncidentSeverity.Critical => await _assignmentService.GetOnCallCSOAsync(),
            IncidentSeverity.High => await _assignmentService.GetSecurityLeadAsync(),
            _ => await _assignmentService.GetTeamLeadAsync()
        };
        
        incident.CommanderId = commander.Id;
        
        // Step 3: Page oncall team
        var escalationContacts = severity switch
        {
            IncidentSeverity.Critical => new[] 
            { 
                commander,
                await _assignmentService.GetCEOAsync(),
                await _assignmentService.GetCFOAsync(),
                await _assignmentService.GetLegalLeadAsync()
            },
            IncidentSeverity.High => new[]
            {
                commander,
                await _assignmentService.GetVPEngineeringAsync(),
                await _assignmentService.GetSecurityLeadAsync()
            },
            _ => new[] { commander }
        };
        
        foreach (var contact in escalationContacts)
        {
            await _notificationService.PageAsync(
                contact,
                $"INCIDENT: {severity}\n{title}\n{description}\n" +
                $"Command: {commander.Name}\n" +
                $"War Room: https://zoom.us/j/incident\n" +
                $"Details: {GetIncidentDashboardUrl(incident.Id)}"
            );
        }
        
        // Step 4: Create incident channel
        var slackChannel = await _slackService.CreateChannelAsync(
            $"incident-{incident.Id}",
            $"Incident: {title}"
        );
        
        incident.SlackChannelId = slackChannel.Id;
        
        // Step 5: Post initial summary
        await _slackService.PostMessageAsync(slackChannel.Id,
            $"""
            🚨 **INCIDENT DECLARED**
            **Severity**: {incident.Severity}
            **Title**: {incident.Title}
            **Status**: Active
            **Commander**: {commander.Name}
            **Started**: {incident.DeclaredAt:yyyy-MM-dd HH:mm:ss} UTC
            
            📋 **What to do**:
            1. Join Zoom: https://zoom.us/j/incident
            2. Check: {GetIncidentDashboardUrl(incident.Id)}
            3. Update progress here
            4. Do NOT communicate externally yet
            """
        );
        
        // Step 6: Preserve evidence immediately
        await _loggingService.LockLogsAsync(
            DateTime.UtcNow.AddHours(-4),  // Last 4 hours
            incident.Id
        );
    }
    
    public async Task UpdateIncidentAsync(
        string incidentId,
        string action,
        string details)
    {
        var incident = await _incidentStore.GetAsync(incidentId);
        
        // Add to timeline
        incident.Timeline.Add(new IncidentEvent
        {
            Time = DateTime.UtcNow,
            Action = action,
            Details = details,
            Actor = GetCurrentUser()
        });
        
        await _incidentStore.UpdateAsync(incident);
        
        // Post to Slack (all war room participants see update)
        await _slackService.PostMessageAsync(incident.SlackChannelId,
            $"**[{DateTime.UtcNow:HH:mm:ss}]** {action}\n{details}"
        );
        
        // Alert if status changed
        if (action.Contains("resolved") || action.Contains("contained"))
        {
            await _notificationService.NotifyIncidentTeamAsync(
                incident,
                $"Incident update: {action}"
            );
        }
    }
    
    public async Task ResolveIncidentAsync(
        string incidentId,
        string resolutionDetails)
    {
        var incident = await _incidentStore.GetAsync(incidentId);
        incident.Status = IncidentStatus.Resolved;
        incident.ResolvedAt = DateTime.UtcNow;
        incident.ResolutionDetails = resolutionDetails;
        
        await _incidentStore.UpdateAsync(incident);
        
        // Schedule post-mortem
        var postMortemDate = incident.DeclaredAt.AddDays(3);  // 3 days later
        await _calendarService.SchedulePostMortemAsync(
            incident.Id,
            postMortemDate,
            incident.CommanderId,
            $"Post-mortem: {incident.Title}"
        );
        
        // Notify stakeholders
        await _notificationService.NotifyIncidentTeamAsync(
            incident,
            $"Incident {incident.Id} marked RESOLVED. Post-mortem scheduled: {postMortemDate:yyyy-MM-dd HH:mm}"
        );
    }
}
```

---

## Post-Incident Reviews (Blameless Post-Mortems)

**ALWAYS**:
- Schedule within 48 hours (while fresh)
- Focus on systems, not blame
- Document root cause (not just symptom)
- Identify contributing factors
- Create action items (prevent recurrence)
- Assign owners & deadlines
- Share findings widely (learn as organization)

**NEVER**:
- Blame individuals
- Skip the post-mortem (normalize learning)
- Ignore systemic problems

### ✅ GOOD Post-Mortem Template

```markdown
# Post-Mortem: [Incident Title]

**Date**: 2026-04-09
**Duration**: 45 minutes (09:00-09:45 UTC)
**Severity**: Critical
**Incident ID**: INC-2026-0042

---

## Participants

- **Incident Commander**: Alice Chen (VP Security)
- **Technical Lead**: Bob Martinez (Backend Lead)
- **Operations Lead**: Carol Singh (DevOps)
- **Communications Lead**: David Wong (Communications)

---

## Timeline

| Time | Event |
|------|-------|
| 08:15 | Monitoring alert: Database connection failures (5% error rate) |
| 08:16 | On-call engineer investigates, notifies team |
| 08:18 | Incident declared (Severity 1) |
| 08:22 | War room activated, investigation begins |
| 08:35 | Root cause identified: Database certificate expired |
| 08:40 | Certificate renewed via AWS CLI |
| 08:42 | Connections restored, error rate normal |
| 08:45 | Incident resolved |
| 08:50 | Status page updated (customer impact: 30 minutes) |

---

## Root Cause Analysis (5 Whys)

1. **Why did database connections fail?**
   → SSL certificate expired at 08:15 UTC

2. **Why wasn't certificate renewed before expiration?**
   → Certificate was scheduled to renew but renewal script failed silently

3. **Why did renewal script fail silently?**
   → No error logging or alerting for renewal failures (only success was logged)

4. **Why wasn't the lack of renewal detected?**
   → No monitoring for certificate expiration; only noticed when connections failed

5. **Why was there no certificate expiration monitoring?**
   → Process gap: Certificate renewal was manual, not automated; monitoring was assumed but never implemented

---

## Contributing Factors

1. **Manual process** — Certificate renewal was not fully automated
2. **Silent failures** — No alerting on renewal script errors
3. **Lack of monitoring** — No alert on low certificate lifetime
4. **No runbook** — Team didn't know immediate recovery procedure
5. **No testing** — Renewal process was never tested in advance

---

## Impact Assessment

**User Impact**:
- Duration: 30 minutes (08:15-08:45 UTC)
- Affected: All customers using database-dependent features
- Severity: Complete service unavailability for 30 minutes
- Downstream: 10% request failure rate during incident

**Financial Impact**:
- Estimated revenue loss: $50,000 (based on SLA penalties)
- Additional: Customer support escalations, PR management costs

---

## Action Items

| Action | Owner | Deadline | Priority |
|--------|-------|----------|----------|
| **Automate certificate renewal** | Carol Singh | 2026-04-16 | Critical |
| **Add certificate expiration monitoring** (7-day alert) | Bob Martinez | 2026-04-13 | Critical |
| **Alert on cert renewal failures** | Carol Singh | 2026-04-13 | High |
| **Document certificate renewal runbook** | David Wong | 2026-04-11 | High |
| **Test certificate renewal process** (monthly) | Carol Singh | 2026-04-20 | High |
| **Review all cert infrastructure** (audit remaining certs) | Alice Chen | 2026-04-15 | Medium |

---

## Prevention Measures

### Immediate (24 hours)
- [✅] Manually renew all certificates
- [✅] Verify all services using SSL/TLS
- [✅] Document current certificate inventory

### Short-term (1 week)
- [ ] Implement automated renewal (AWS Lambda + EventBridge)
- [ ] Add monitoring alerts (7, 14, 30 days before expiration)
- [ ] Create runbook for manual renewal (as backup)
- [ ] Test renewal process end-to-end

### Long-term (4 weeks)
- [ ] Regular certificate audits (monthly)
- [ ] Certificate lifecycle training for team
- [ ] Automated notifications to Slack (#ops-alerts)
- [ ] Integrate with certificate provider's automated renewal API

---

## Lessons Learned

| Lesson | Impact |
|--------|--------|
| **"Assume managed services still need monitoring"** | Even "automatic" renewals can fail silently |
| **"Silent failures hide problems"** | Must log and alert on script errors, not just success |
| **"Monitoring !== Alerting"** | Seeing the metric isn't enough; must alert before impact |
| **"Manual processes don't scale"** | This won't be the last cert that expires; automate everywhere |
| **"Runbooks save lives"** | Team reacted quickly because procedures were clear |

---

## Follow-up

- **Post-Mortem Review**: Schedule 1 week after (2026-04-16) to confirm action items completed
- **Broader Team Sharing**: Post findings to #engineering Slack (learn from incident)
- **CEO Communication**: Update executive team (SLA impact, remediation plan, prevention)
- **Customer Communication**: Send summary to affected customers (what happened, what we did, how we prevent)

---

## Metrics

- **MTTR** (Mean Time To Resolution): 30 minutes
- **MTPD** (Mean Time to Problem Detection): 1 minute
- **Action Items**: 6 created
- **Critical Items**: 2
- **Estimated Prevention Benefit**: Prevent this class of incident 99.9% (automated renewal)
```

---

## Incident Response Checklist

- [ ] IR playbook documented (with severity levels)
- [ ] Incident commander role defined (authority, escalation)
- [ ] War room process established (communication, updates, roles)
- [ ] Monitoring alerts configured (detect incidents early)
- [ ] Alert thresholds tuned (avoid noise, catch real issues)
- [ ] Evidence preservation automated (logs, system state)
- [ ] Triage process defined (severity classification)
- [ ] Communication templates ready (internal, customer, regulatory)
- [ ] Escalation contacts identified (CEO, legal, compliance)
- [ ] Post-mortem template created (blameless, action items)
- [ ] Incident tracking system in place (timeline, audit trail)
- [ ] Regular IR drills conducted (test procedures quarterly)

---

## Summary

Good incident response:
1. **Prepare beforehand** — Playbook, contacts, automation
2. **Detect quickly** — Monitoring, alerts, thresholds
3. **Declare clearly** — Severity, commander, team activation
4. **Diagnose thoroughly** — Evidence preservation, root cause analysis
5. **Mitigate immediately** — Temporary fix to restore service
6. **Communicate constantly** — Internal & external, no surprises
7. **Review blameless** — Focus on systems, not individuals
8. **Improve continuously** — Action items, follow-up, prevention

Incidents are learning opportunities—treat them as such.
