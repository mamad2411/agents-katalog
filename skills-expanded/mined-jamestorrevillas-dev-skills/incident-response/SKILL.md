---
name: incident-response
description: Use this skill when handling production incidents, outages, or critical bugs — from initial detection through resolution and post-mortem. Trigger on keywords: incident, outage, production down, on-call, P1, P2, critical bug, postmortem, root cause analysis, runbook, service disruption.
---

# Incident Response

## The Five Phases

```
DETECT → ASSESS → RESPOND → RESOLVE → LEARN
```

Every incident touches all five. Never skip LEARN — it's the only one that prevents recurrence.

---

## Phase 1: Detect & Assess (First 5 Minutes)

```
1. What is broken? (specific service, feature, endpoint)
2. Who is affected? (all users, subset, specific region)
3. What is the impact? (data loss? revenue? user-facing?)
4. When did it start? (correlate with recent deploys/changes)
5. Severity: P1 (all users, data loss) / P2 (major feature) / P3 (minor)
```

**Communicate immediately** — even if you don't know the cause yet:
```
"We're investigating an issue with [service]. 
Impact: [who is affected]. 
We'll update in 15 minutes."
```

---

## Phase 2: Respond (During Incident)

### Incident Roles
- **Incident Commander** — coordinates, communicates, makes calls
- **Technical Lead** — investigates and fixes
- **Communicator** — updates stakeholders

### Response Checklist
- [ ] Create incident channel/ticket
- [ ] Assign IC and Technical Lead
- [ ] Begin investigation (check logs, metrics, recent changes)
- [ ] Post status updates every 15-30 minutes
- [ ] Consider rollback if recent deploy is suspect
- [ ] Escalate if not resolved in [your SLA]

### Rollback Decision Criteria
Roll back immediately if:
- Root cause is a recent deploy (< 24h)
- Fix is not immediately obvious
- User impact is severe

---

## Phase 3: Resolve

Document as you go:
```
Timeline:
[time] - Incident detected: [symptom]
[time] - Identified probable cause: [cause]
[time] - Applied fix: [action taken]
[time] - Monitoring for stability
[time] - Incident resolved
```

---

## Phase 4: Post-Mortem (Within 48h)

### Post-Mortem Template
```markdown
## Incident: [title]
**Date:** | **Duration:** | **Severity:**

### Summary
[2-3 sentences: what happened and impact]

### Timeline
[Chronological events from detection to resolution]

### Root Cause
[The actual cause — not the symptom]

### Contributing Factors
[Conditions that allowed this to happen]

### What Went Well
[Things that helped during response]

### Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| [preventive fix] | [name] | [date] |
| [monitoring improvement] | [name] | [date] |
```

### Blameless Post-Mortems
- Focus on systems and processes, not people
- "The deploy process didn't have a rollback check" not "James forgot to test"
- Every person did their best with the information they had
- Action items fix systems, not punish individuals

---

## Runbook Template

For recurring incident types, create a runbook:
```markdown
## Runbook: [incident type]

### Symptoms
[How to recognize this incident]

### Immediate Actions
1. [First thing to check/do]
2. [Second thing]

### Investigation Steps
1. Check [X] for [Y]
2. Run [command] to verify [Z]

### Resolution
[Steps to fix]

### Escalation
If not resolved in [time]: escalate to [person/team]
```
