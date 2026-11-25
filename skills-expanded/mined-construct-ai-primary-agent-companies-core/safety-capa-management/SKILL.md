---
title: CAPA Management
description: Management of corrective and preventive action tracking including assignment, due date monitoring, effectiveness verification, and closure for the ConstructAI HSE system
frequency: Per corrective/preventive action
success_rate: 95%
tags:
  - domainforge_ai
  - safety
  - CAPA-management
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02400_safety/agent-data/prompts/02400_AI-NATIVE-SAFETY-OPERATIONS-PROMPT.md
---

# CAPA Management

## Overview
Management of corrective and preventive actions (CAPA) tracking including generation from incident findings or audit results, assignment, due date monitoring, effectiveness verification, and closure. Primary agent: Incident Investigation Specialist.

## Triggers
- Root cause analysis completed with corrective action recommendations
- Audit findings generated requiring corrective action
- Inspection findings requiring corrective action
- Management review identifying improvement opportunities
- Regulatory finding requiring corrective action

## Prerequisites
- Root cause or finding documented
- Corrective actions identified and prioritised
- Responsible persons and timeline defined
- Resources allocated for implementation

## Steps

### Step 1: CAPA Registration
- Assign unique CAPA ID
- Record source (incident, audit, inspection, management review)
- Classify corrective vs preventive action
- Assign severity/priority
- Record due date and responsible person

### Step 2: CAPA Assignment
- Assign to responsible person or department
- Communicate CAPA requirements and timeline
- Ensure resource availability
- Confirm acceptance of assignment

### Step 3: CAPA Implementation Tracking
- Monitor progress against implementation plan
- Track milestone completion
- Record status updates
- Flag at-risk items (approaching due date, resource constraints)
- Escalate overdue items

### Step 4: Effectiveness Verification
- Verify corrective action has been implemented as planned
- Assess effectiveness in addressing root cause
- Collect evidence of sustained improvement
- Document verification results
- Identify any need for additional actions

### Step 5: CAPA Closure
- Verify all evidence collected and documented
- Confirm root cause addressed
- Update source record (incident, audit) with CAPA closure
- Record lessons learned
- Share improvements with relevant stakeholders

## Success Criteria
- All CAPAs assigned with clear responsibility and due dates
- Implementation tracked with regular status updates
- Effectiveness verified before closure
- All CAPAs closed within required timeframes

## Common Pitfalls
1. **Vague corrective actions** → Actions not specific enough to address root cause
2. **Unrealistic timeframes** → Due dates set without resource confirmation
3. **Missing effectiveness verification** → Actions completed but root cause still present
4. **No escalation** → Overdue CAPAs not escalated to management

## Cross-References
- `safety-RCA-analysis/SKILL.md` — Root cause analysis source
- `safety-incident-tracking/SKILL.md` — Incident closure verification