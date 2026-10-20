---
name: alerting-engineering
description: Design alerting that gets paged for the right reasons. Use when
  defining alert rules and policies.
metadata:
  tags: alerting, engineering
---

# Alerting Engineering

## Use this skill when
- Turning SLOs and metrics into alerts
- Setting severity, escalation, and routing
- Reducing alert noise

## Do not use this skill when
- Building dashboards
- Debugging a system (incident playbook)

## Instructions
1. Alert on user impact symptoms and SLO burn, not every dip.
2. Set paging thresholds so real incidents page; everything else goes to an issue.
3. Include runbook links, severity, and owner in every alert.
4. Use alerting on rate/trend, not raw thresholds alone.
5. Keep a max alerts-per-person budget; retire noise.
6. Escalate on silence or repetition.
7. Post-incident, tune alerts as follow-up.

## Checklist
- Every alert links a runbook
- No on-call fatigue from noise
- SLO burn alerts present

## Output Format
- Alert | condition | severity | owner | runbook | frequency

## Common Mistakes
- Paging from a dashboard graph
- Threshold alerts that always fire
- No retirement of stale alerts
