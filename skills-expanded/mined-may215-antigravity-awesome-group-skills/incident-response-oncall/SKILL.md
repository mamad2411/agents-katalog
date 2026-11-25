---
name: incident-response-oncall
description: "Group skill: Incident response/on-call — triage, diagnosis, tracing, logs, fix, verification, postmortem, and alerting."
risk: high
source: self
---

# 🔐 Incident Response / On-Call

> **Group Skill** — Orchestrates sub-skills for responding to production incidents.
> Activate by saying: "Respond to incident" or "production is down"

## When to Use

- Production is down or degraded
- Need to respond quickly to an incident
- Running postmortem and root cause analysis

## Step-by-Step Workflow

### Step 1: Triage
**Skill**: `incident-response-incident-response`
- Execute incident playbook
- Assess severity
- Notify stakeholders

### Step 2: Diagnose
**Skill**: `systematic-debugging` / `error-diagnostics-smart-debug`
- Find root cause
- Eliminate hypotheses
- Analyze error patterns

### Step 3: Trace
**Skill**: `distributed-tracing` / `distributed-debugging-debug-trace`
- Follow request flow
- Identify failure points
- Check service dependencies

### Step 4: Logs
**Skill**: `prometheus-configuration` / `grafana-dashboards`
- Analyze logs
- Check metrics
- Review dashboards

### Step 5: Fix
**Skill**: `debugger`
- Apply hotfix
- Minimize blast radius
- Test fix in staging

### Step 6: Verify
**Skill**: `test-automator` / `e2e-testing`
- Confirm fix works
- Run regression tests
- Monitor after deploy

### Step 7: Postmortem
**Skill**: `incident-runbook-templates` / `postmortem-writing`
- Document what happened
- Identify root cause
- Define prevention measures

### Step 8: Alert
**Skill**: `pagerduty-automation`
- Notify team
- Update status page
- Close incident

## Completion

Incident is resolved, documented, and prevention measures defined. 🔐

## Sub-Skills Referenced

1. `incident-response-incident-response`
2. `systematic-debugging`
3. `error-diagnostics-smart-debug`
4. `distributed-tracing`
5. `distributed-debugging-debug-trace`
6. `prometheus-configuration`
7. `grafana-dashboards`
8. `debugger`
9. `test-automator`
10. `e2e-testing`
11. `incident-runbook-templates`
12. `postmortem-writing`
13. `pagerduty-automation`
