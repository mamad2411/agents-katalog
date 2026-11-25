---
name: incident-response
description: Run blameless post-mortems, define incident severity levels, maintain runbooks, and prepare on-call readiness. Includes templates for post-mortem documents, runbooks, and severity classification.
invoke_when: Use when setting up incident response processes, writing a post-mortem, defining severity levels, creating runbooks, preparing on-call rotations, or discussing incident management.
---

# Incident Response

## Core Principle

Incidents are inevitable. The goal is not to prevent all incidents but to detect them fast, resolve them fast, and learn from them. Blamelessness is non-negotiable -- people make better decisions when they are not afraid of punishment.

---

## 1. Incident Severity Levels

| Severity | Impact | Response Time | Examples |
|---|---|---|---|
| **SEV1 -- Critical** | Complete service outage affecting all users. Revenue loss active. Data integrity risk. | Respond within 15 minutes. All-hands incident response. | Site is down. Payment processing is broken. Data breach detected. |
| **SEV2 -- Major** | Significant degradation affecting many users. Major feature is broken. | Respond within 30 minutes. Dedicated incident commander + on-call. | Checkout flow broken for 50%+ users. Login failures spiking. API latency > 10x normal. |
| **SEV3 -- Minor** | Partial degradation affecting some users. Workaround exists. | Respond within 2 hours. On-call engineer handles. | One region degraded. Non-critical feature broken. Elevated error rate for one endpoint. |
| **SEV4 -- Low** | Cosmetic issue or minor bug with minimal user impact. | Respond next business day. Tracked as a bug ticket. | UI rendering glitch. Incorrect error message. Slow non-critical background job. |

### Escalation Rules

- Any on-call engineer can declare a SEV1 or SEV2. Do not wait for manager approval.
- SEV1 automatically pages the engineering manager and VP of Engineering.
- SEV2 automatically pages the team lead.
- If an incident is not resolved within 1 hour, escalate severity by one level.
- When in doubt, escalate. It is always better to over-communicate.

---

## 2. Blameless Post-Mortem Template

Write a post-mortem for every SEV1 and SEV2 incident within 72 hours. SEV3 incidents get a post-mortem if the team decides it warrants one.

```markdown
# Post-Mortem: [Incident Title]

**Date:** [YYYY-MM-DD]
**Severity:** [SEV1 / SEV2 / SEV3]
**Duration:** [Start time - End time, total duration]
**Author:** [Name]
**Reviewers:** [Names of people who reviewed this document]

---

## Summary

[2-3 sentences describing what happened, what the user impact was, and how it was resolved.
Example: "On 2025-06-15, the checkout service became unavailable for 47 minutes due to a
database connection pool exhaustion caused by a missing index on the orders table. Approximately
12,000 users were unable to complete purchases, resulting in an estimated $85,000 in lost revenue.
The issue was resolved by adding the missing index and increasing the connection pool size."]

---

## Impact

- **Users affected:** [Number or percentage]
- **Duration of impact:** [Minutes/hours]
- **Revenue impact:** [Estimated $, if applicable]
- **Data impact:** [Any data loss or corruption? If so, describe.]
- **SLO impact:** [How much error budget was consumed?]

---

## Timeline (all times in UTC)

| Time | Event |
|---|---|
| 14:00 | Deployment of v2.3.1 to production |
| 14:12 | Monitoring alert fires: "High error rate on /api/checkout" |
| 14:15 | On-call engineer acknowledges alert |
| 14:18 | Incident declared as SEV2, Slack channel created |
| 14:25 | Root cause identified: database connection pool exhaustion |
| 14:30 | Mitigation applied: increased connection pool from 20 to 50 |
| 14:35 | Error rate returns to normal |
| 14:45 | Incident resolved, monitoring confirms recovery |
| 14:50 | Severity downgraded, incident closed |

---

## Root Cause

[Detailed technical explanation of what caused the incident. Be specific.
Example: "The v2.3.1 deployment added a new query to the checkout flow that joins the orders
and order_items tables. This query lacks an index on order_items.order_id, causing a full
table scan on every checkout request. Under production load (500 req/s), this query consumed
all 20 database connections within 12 minutes, causing subsequent requests to fail with
connection timeout errors."]

---

## Contributing Factors

[Factors that made the incident more likely or made it harder to detect/resolve. These are NOT
the root cause but contributed to the severity or duration.]

- [ ] The query was not load-tested before deployment.
- [ ] The connection pool size (20) was too small for the traffic volume.
- [ ] The staging environment has 1/100th the data volume, so the missing index was not noticeable.
- [ ] The deployment happened on a Friday afternoon with reduced staffing.

---

## Detection

- **How was the incident detected?** [Monitoring alert / Customer report / Engineer noticed]
- **Time to detect:** [Minutes from start of impact to first alert]
- **Was the alert actionable?** [Yes/No -- did the alert message point to the problem?]
- **What would have detected this faster?** [e.g., "A query latency alert on p99 > 1s would have
  fired 5 minutes earlier than the error rate alert."]

---

## Resolution

[What was done to resolve the incident? Be specific about the steps taken.]

1. Increased database connection pool from 20 to 50 (immediate mitigation).
2. Added index on `order_items.order_id` (root cause fix).
3. Deployed v2.3.2 with the index migration.

---

## Action Items

| Action | Owner | Priority | Due Date | Status |
|---|---|---|---|---|
| Add index on order_items.order_id | @alice | P0 | 2025-06-16 | Done |
| Add query latency alert (p99 > 1s) | @bob | P1 | 2025-06-20 | In Progress |
| Add slow query logging (> 500ms) | @alice | P1 | 2025-06-20 | To Do |
| Add load test for checkout flow with production data volume | @charlie | P2 | 2025-06-30 | To Do |
| Review connection pool sizing for all services | @bob | P2 | 2025-07-01 | To Do |
| No Friday deployments policy for critical services | @team-lead | P2 | 2025-06-20 | To Do |

---

## Lessons Learned

**What went well:**
- Alert fired within 12 minutes of the issue starting.
- On-call engineer responded within 3 minutes of the alert.
- Root cause was identified quickly (10 minutes).

**What could be improved:**
- Staging environment data volume should match production for performance testing.
- Connection pool sizes should be reviewed as traffic grows.
- Deploy-time checks should verify that new queries have appropriate indexes.

---

## Appendix

[Include relevant graphs, logs, or links to dashboards that illustrate the incident.]
```

**Key blamelessness rules:**
- Never use a person's name in the root cause section. Describe what happened, not who did it.
- Frame contributing factors as systemic issues: "The system allowed X" not "Person Y did X."
- Action items improve the system, not the person.

---

## 3. Runbook Template for Services

Every production service must have a runbook. The on-call engineer should be able to follow the runbook without prior knowledge of the service.

```markdown
# Runbook: [Service Name]

**Owner Team:** [Team Name]
**Slack Channel:** [#service-name-oncall]
**PagerDuty Service:** [Link]
**Dashboard:** [Grafana/Datadog link]
**Repository:** [GitHub link]

---

## Service Overview

**Purpose:** [One sentence describing what this service does]
**Dependencies:** [List upstream and downstream services]
**Data stores:** [Databases, caches, queues]
**SLO:** [Availability target and latency target]

---

## Health Check

- **Liveness:** `GET /healthz` -- returns 200 if the process is running.
- **Readiness:** `GET /readyz` -- returns 200 if the service can handle requests (DB connected, cache warm).

---

## Common Alerts and Responses

### Alert: High Error Rate (>1% 5xx)

**Possible causes:**
1. Downstream service is down -- check [dependency dashboard link].
2. Bad deployment -- check recent deployments in [CI/CD link].
3. Database connection issues -- check [RDS dashboard link].

**Steps to investigate:**
1. Check the error logs: `kubectl logs -l app=service-name --tail=100`
2. Check if a deployment happened in the last 30 minutes.
3. Check downstream service health.

**Mitigation:**
- If caused by bad deployment: rollback with `kubectl rollout undo deployment/service-name`
- If caused by downstream: enable circuit breaker override in [flag dashboard]
- If caused by database: check connection pool metrics, restart pods if connection leak suspected.

### Alert: High Latency (p99 > 500ms)

**Possible causes:**
1. Database slow queries.
2. Increased traffic volume.
3. Resource contention (CPU/memory).

**Steps to investigate:**
1. Check slow query logs.
2. Check pod resource utilization: `kubectl top pods -l app=service-name`
3. Check if autoscaler is active.

**Mitigation:**
- Scale up: `kubectl scale deployment/service-name --replicas=10`
- If database: kill long-running queries, add indexes.

### Alert: Pod Crash Loop

**Steps to investigate:**
1. Check pod status: `kubectl get pods -l app=service-name`
2. Check logs of crashing pod: `kubectl logs <pod-name> --previous`
3. Check events: `kubectl describe pod <pod-name>`

**Mitigation:**
- If OOM: increase memory limits in deployment manifest.
- If config error: check ConfigMap/Secrets for missing values.
- If dependency unavailable: check dependency health, circuit breakers.

---

## Operational Procedures

### Scaling

- Minimum replicas: 3
- Maximum replicas: 20
- Scale manually: `kubectl scale deployment/service-name --replicas=N`

### Rollback

- Rollback to previous version: `kubectl rollout undo deployment/service-name`
- Rollback to specific version: `kubectl rollout undo deployment/service-name --to-revision=N`

### Database Access

- Read replica: [connection details or SSM parameter path]
- Never run write queries against production without approval from [team lead].

---

## Contacts

| Role | Name | Slack Handle |
|---|---|---|
| Primary on-call | [Rotation schedule link] | - |
| Team lead | [Name] | @handle |
| Database admin | [Name] | @handle |
```

---

## 4. On-Call Readiness Checklist

### Before Going On-Call

- [ ] I have access to PagerDuty and can receive pages on my phone.
- [ ] I have access to the production Kubernetes cluster.
- [ ] I have access to the logging system (Datadog/Splunk/CloudWatch).
- [ ] I have read the runbooks for all services I am on-call for.
- [ ] I know the escalation path (who to page if I need help).
- [ ] I have tested VPN access from my on-call location.
- [ ] I have a laptop with me and reliable internet access.
- [ ] I know how to rollback a deployment.
- [ ] I know where the kill switches are for each service.

### During an Incident

- [ ] Acknowledge the page within 5 minutes.
- [ ] Open the relevant dashboard and check the alert details.
- [ ] If SEV1/SEV2: create an incident Slack channel (#incident-YYYY-MM-DD-brief-description).
- [ ] Post a brief status update every 15 minutes in the incident channel.
- [ ] Focus on mitigation first (stop the bleeding), root cause second.
- [ ] If you cannot mitigate within 30 minutes, escalate.
- [ ] Document your actions and findings in the incident channel as you go.

### After an Incident

- [ ] Write a brief incident summary in the incident channel.
- [ ] Create a post-mortem document (for SEV1 and SEV2).
- [ ] Schedule a post-mortem review meeting within 72 hours.
- [ ] Create action items with owners and due dates.
- [ ] Update the runbook if you discovered missing information.

---

## Incident Communication Templates

### Initial Status Update (post within 15 minutes of detection)

```
**Incident: [Brief description]**
**Severity:** SEV[1/2/3]
**Status:** Investigating
**Impact:** [What users are experiencing]
**Started:** [Time UTC]
**Incident Commander:** [Name]

We are aware of [description of issue] and are actively investigating.
Next update in 15 minutes.
```

### Follow-Up Status Update (every 15 minutes)

```
**Incident Update: [Brief description]**
**Status:** [Investigating / Identified / Monitoring / Resolved]
**Impact:** [Current user impact]
**Update:** [What we have learned since last update, what we are doing next]

Next update in 15 minutes.
```

### Resolution Update

```
**Incident Resolved: [Brief description]**
**Duration:** [Total duration]
**Root Cause:** [One sentence]
**Resolution:** [What was done to fix it]
**Impact:** [Summary of user impact]

A post-mortem will be published within 72 hours.
```
