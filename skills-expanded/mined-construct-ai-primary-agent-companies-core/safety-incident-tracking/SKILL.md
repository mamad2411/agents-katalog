---
title: Safety Incident Tracking
description: End-to-end tracking of safety incidents from initial report through investigation, corrective action, and final closure
frequency: Per incident report
success_rate: 98%
tags:
  - domainforge_ai
  - safety
  - incident-tracking
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02400_safety/agent-data/prompts/02400_AI-NATIVE-SAFETY-OPERATIONS-PROMPT.md
---

# Safety Incident Tracking

## Overview
End-to-end tracking of safety incidents from initial report through investigation, corrective action assignment, and final case closure. Primary agent: Incident Investigation Specialist.

## Triggers
- Incident reported on site (near-miss, injury, property damage, environmental)
- External authority reports incident
- Worker reports safety concern
- Automated system triggers (PPE-detection violation, hazard-detection alert)

## Prerequisites
- Incident report submitted via mobile app, phone, or in-person
- Initial information: who, what, where, when
- Incident severity level assigned

## Steps

### Step 1: Incident Registration
- Assign unique incident ID
- Record incident type (near-miss, medical treatment, lost-time, property damage, environmental)
- Assign severity level based on organisational matrix
- Record immediate actions taken
- Log report timestamp and reporter details

### Step 2: Initial Assessment
- Review incident details for accuracy and completeness
- Assign investigation priority based on severity and potential for recurrence
- Assign investigation team
- Determine if regulatory notification required

### Step 3: Investigation Assignment
- Assign lead investigator and team members
- Define investigation scope and timeline
- Allocate investigation resources
- Communicate investigation status to stakeholders

### Step 4: Investigation Tracking
- Monitor investigation progress against timeline
- Track evidence collection completion
- Record witness statement status
- Monitor root cause analysis milestone progress

### Step 5: Corrective Action Tracking
- Track corrective actions from investigation findings
- Monitor completion against due dates
- Escalate overdue items
- Verify action effectiveness upon completion

### Step 6: Incident Closure
- Verify all investigation steps completed
- Confirm all corrective actions closed
- Document lessons learned
- Archive incident record
- Share lessons learned with relevant stakeholders

## Success Criteria
- Incident registered within required reporting timeframe
- Investigation assigned and completed within timeline
- All corrective actions tracked to closure
- Lessons learned documented and shared

## Common Pitfalls
1. **Delayed reporting** → Incidents not reported immediately, losing critical evidence
2. **Incomplete initial data** → Missing who/where/what details delays investigation
3. **Investigation delays** → Resource conflicts, investigator availability
4. **Missing corrective actions** → Root causes not converted to corrective actions

## Cross-References
- `safety-RCA-analysis/SKILL.md` — Root cause analysis for investigation
- `safety-CAPA-management/SKILL.md` — Corrective action management