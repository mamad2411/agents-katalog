---
name: operations-playbook
description: "When to activate: SOPs, runbooks, escalation matrices, on-call rotations, operational reviews, capacity planning, ops documentation, incident management, business operations"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: business-ops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Operations Playbook

## SOP (Standard Operating Procedure) Standard

### SOP Template
```
---
Title: [Process Name]
SOP ID: OPS-[NNN]
Version: 1.x
Owner: [Name / Role]
Approver: [Name / Role]
Effective date: YYYY-MM-DD
Next review: YYYY-MM-DD
---

## 1. Purpose
[One paragraph: what this process accomplishes and why it exists.]

## 2. Scope
**Applies to:** [teams, roles, geographies]
**Excludes:** [explicit exclusions]

## 3. Prerequisites
- [Access, tool, or knowledge required before starting]
- [System access: link to access request process]

## 4. Procedure

Step 1: [Action title]
  Actor: [Role]
  Action: [What to do — imperative, specific]
  Tool/system: [Where to do it]
  Output: [What is produced or recorded]
  If error: [What to do if something goes wrong]

Step 2: [Action title]
  [Same structure]

[Decision point — if applicable]
  IF [condition] → proceed to Step X
  IF [other condition] → escalate to [Role] via [channel]

## 5. Exceptions
[Known edge cases and how to handle each]

## 6. Verification
[How to confirm the process completed correctly]

## 7. Related documents
- [Upstream SOP]: [link]
- [Downstream SOP]: [link]
- [Policy reference]: [link]

## 8. Change history
| Version | Date | Author | Change summary |
|---------|------|--------|---------------|
| 1.0 | YYYY-MM-DD | [Name] | Initial version |
```

---

## Runbook Template (Technical Operations)

```
---
Runbook: [System / Incident Type]
ID: RB-[NNN]
Severity: P1 / P2 / P3
Last tested: YYYY-MM-DD
---

## Symptoms
- [Observable indicator that triggers this runbook]
- [Alert name / threshold that fires]

## Impact
- [Who is affected]
- [What is degraded or unavailable]
- [Revenue / customer impact estimate]

## Immediate actions (first 5 minutes)
1. [Action] — [command or link]
2. [Action]
3. Notify [channel] with: "Investigating [issue] — ETA for update: 15 min"

## Diagnosis steps
1. Check [dashboard / log / metric]: [link]
   Expected: [normal range]
   If abnormal: → go to section [X]
2. Run: [command]
   Expected output: [example]
3. Check [upstream dependency]: [link]

## Mitigation options

### Option A — [Quick fix, lower risk]
1. [Steps]
2. [Verification]
Expected recovery time: X minutes

### Option B — [More complete fix, higher effort]
1. [Steps]
Expected recovery time: X minutes

## Rollback procedure
1. [Steps to undo mitigation if it worsens the situation]

## Escalation
- If not resolved in 30 min: page [on-call lead] via [PagerDuty / Slack]
- If customer data impact: notify [DPO / Legal] immediately
- Exec notification threshold: [criteria]

## Post-incident
- File incident report within 24h
- Schedule post-mortem within 5 business days
- Update this runbook with findings
```

---

## Escalation Matrix

### Severity Definitions
| Severity | Customer impact | Response SLA | Who is paged |
|----------|----------------|--------------|-------------|
| P0 / Critical | All customers affected / data loss | 15 min | On-call eng + eng lead + exec |
| P1 / High | Major feature down for subset of customers | 30 min | On-call eng + eng lead |
| P2 / Medium | Feature degraded, workaround exists | 2 hours | On-call eng |
| P3 / Low | Minor issue, no workaround needed immediately | Next business day | Ticket queue |

### Escalation Path Template
```
P0 Escalation:
  1. On-call engineer (immediate)
  2. Engineering lead — if not resolved in 15 min
  3. VP Engineering — if not resolved in 30 min
  4. CEO + CTO — if revenue impact > $X or data breach suspected
  5. Customer communications — if > N customers affected

Internal communication: #incidents Slack channel
Customer communication: Status page + email to affected accounts
```

---

## On-Call Rotation Design

### Rotation Structure
| Parameter | Recommendation |
|-----------|---------------|
| Rotation length | 1 week (Mon–Sun) |
| Primary + secondary | Always two people covering |
| Minimum rest | 8h between pages (don't page same person twice in 8h) |
| Handoff | Sync call Mondays: open incidents, known risks this week |
| Compensation | On-call pay / TOIL policy must be documented in HR system |

### On-Call Handbook Contents
1. How to be paged (tools: PagerDuty, OpsGenie, etc.)
2. What to do in first 5 minutes of any alert
3. Runbook library location
4. Escalation contacts (updated every rotation)
5. How to declare incident and open war room
6. Communication templates (internal + external)
7. How to request backup

### On-Call Health Metrics
| Metric | Target | Action if exceeded |
|--------|--------|-------------------|
| Pages per week per engineer | < 5 | Investigate and fix alert noisiness |
| Median time to acknowledge | < 5 min | Improve paging / rotation coverage |
| Incident MTTR | < 60 min (P1) | Post-mortem + runbook improvement |
| Repeat incidents | 0 for same root cause | Post-mortem action item tracking |

---

## Operational Review Cadences

### Weekly Ops Review (30 min)
```
Agenda:
1. Open incidents / active issues (5 min)
2. Key metrics vs. targets — RED / YELLOW / GREEN (10 min)
3. Top operational risk this week (5 min)
4. Action items from last week — status (5 min)
5. New action items (5 min)
```

### Monthly Business Review (60 min)
```
Agenda:
1. Financial performance: revenue, burn, cash (15 min)
2. Operational metrics by function (15 min)
3. OKR progress — on track / at risk / off track (15 min)
4. Risks and mitigation plans (10 min)
5. Cross-functional dependencies and blockers (5 min)
```

### Quarterly Business Review (3 hours)
```
Agenda:
1. Prior quarter results vs. plan (45 min)
2. Market and competitive update (30 min)
3. Product roadmap and delivery status (30 min)
4. People and org health (30 min)
5. Next quarter plan and commitments (30 min)
6. Strategic discussion — one deep topic (15 min)
```

---

## Capacity Planning

### Headcount Planning Framework
```
Step 1: Translate business goals to output targets
  - Revenue target → sales quota per rep → # reps needed
  - Product roadmap → engineering throughput needed → # engineers needed
  - Support ticket volume → tickets per agent → # agents needed

Step 2: Model current capacity
  - Headcount today × productivity per person = current output
  - Account for: ramp time, attrition, PTOs, meetings overhead

Step 3: Identify gap
  Gap = target output - current capacity
  
Step 4: Close gap options
  - Hire (slowest, highest cost)
  - Increase productivity (tooling, automation, process)
  - Reduce scope (what can we not do?)
  - Outsource (faster ramp, lower fixed cost)
```

### Capacity Model Inputs
| Input | Source | Refresh cadence |
|-------|--------|-----------------|
| Revenue/ARR plan | Finance | Quarterly |
| Headcount by function | HR / finance | Monthly |
| Attrition rate | HR | Rolling 12-month |
| Ramp time by role | HR / managers | Annual calibration |
| Productivity metrics | BizOps | Monthly |

---

## Operations Documentation Index

Maintain a living index of all operational documents:

```
Operations Wiki — Top-level Index

/Processes
  /Sales: [list of SOPs]
  /Engineering: [list of runbooks]
  /Support: [list of SOPs]
  /Finance: [list of SOPs]
  /HR: [list of SOPs]

/Escalation Paths
  Incident severity matrix
  On-call contacts (refreshed weekly)
  Executive escalation protocol

/Templates
  Incident report template
  Post-mortem template
  Business review deck template
  Budget request template

/Dashboards
  [Links to live operational dashboards by function]
```

### Document Ownership Rule
Every document must have a named owner (person, not team). Owner is responsible for:
- Accuracy (update when process changes)
- Review cadence (quarterly minimum)
- Archiving superseded versions
