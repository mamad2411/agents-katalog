---
name: skill-incident-management
description: Incident response, postmortem facilitation, root cause analysis (RCA), blameless culture, incident timeline documentation, and incident classification. Use when responding to production incidents, writing incident reports, facilitating postmortems, or improving incident response processes.
version: 1.0.0
---

# Skill: Incident Management

Systematic incident response and postmortem process for production issues. Emphasizes speed (MTTR), clarity (timeline), and learning (blameless culture).

## Incident Classification (SEV Levels)

**SEV 1 (Critical)**
- Entire service down OR
- Core functionality unavailable AND
- Large user base affected AND
- Revenue/reputation impact
- MTTR target: < 30 minutes
- Declare: Immediately
- Escalation: Engineering Manager + Tech Lead + On-Call lead

**SEV 2 (High)**
- Partial degradation (slow, some users affected) OR
- Non-core features completely down
- MTTR target: < 2 hours
- Declare: Within 15 min
- Escalation: Tech Lead + Service Owner

**SEV 3 (Medium)**
- Non-critical feature broken OR
- Workaround exists AND
- Low user impact
- MTTR target: < 24 hours
- Declare: Next business day
- Escalation: Service Owner

**SEV 4 (Low)**
- Minor issue, cosmetic OR
- Zero user impact
- Can wait for next release
- Escalation: None (treat as bug)

## Incident Timeline Template

```
## Incident: [Title]

### Summary
- Service: [service-name]
- Duration: [start] - [end] (X minutes)
- Users affected: [X]%
- Severity: SEV [1-4]

### Timeline

| Time | Event | Owner |
|------|-------|-------|
| 14:32 UTC | ❌ Alert: API error rate > 10% | Monitoring |
| 14:33 UTC | 🟡 Incident declared (SEV 2) | On-Call |
| 14:35 UTC | 🔍 Root cause identified: DB connection pool exhausted | Backend lead |
| 14:37 UTC | 🔧 Mitigation: Increased pool size, restarted service | DevOps |
| 14:39 UTC | ✅ Incident resolved, metrics normal | Monitoring |
| 14:45 UTC | ✅ All systems nominal (monitoring for 10 min) | On-Call |

### Root Cause
Database connection pool was set to 50 but app scaled to 8 instances (50 x 8 = 400 connections but pool limit was 50). New deployment didn't adjust pool size.

### Contributing Factors
1. No automated pool size calculation (manual config)
2. Pre-deployment validation didn't catch pool exhaustion risk
3. Alerting was on error rate, not pool usage (too late)

### Resolution
1. Temporarily increased pool size from 50 to 200 (immediate)
2. Disabled auto-scaling during hot-fix (reduced concurrent instances)

### Monitoring During Incident
- API error rate: 8% → 0.2% after fix
- DB response time: 2s → 50ms after fix
- User-visible errors: Resolved

### Follow-up Actions
1. [Action] Implement auto-sizing of connection pool based on instance count
2. [Action] Add alert on pool usage % (critical at 80%+)
3. [Action] Add pre-deployment validation check for pool size
4. [Action] Document connection pool sizing in runbook
```

## Postmortem Process (Blameless)

### Before Postmortem
- Wait 24-48 hours (emotions settle, facts clear)
- Send survey to participants (get thoughts while fresh)
- Collect logs, metrics, alerts

### During Postmortem (60 min)

```
## Postmortem: [Service] incident on [Date]

### 1. Incident Summary (5 min)
[What happened, impact, duration]

### 2. Timeline (10 min)
[When did each major event occur? Focus on facts, not blame]

### 3. Root Cause Analysis (15 min)

**Ask "Why?" 5 times**:
1. Why did error rate spike?
   → Connection pool exhausted
2. Why was pool exhausted?
   → Pool size fixed at 50, scaled to 8 instances
3. Why wasn't pool size updated?
   → No automated calculation, manual config
4. Why wasn't this caught in testing?
   → Load tests didn't use production instance count
5. Why don't we catch this automatically?
   → Pre-deployment validation doesn't check pool usage

**Root cause**: No automated pool sizing based on instance count

### 4. Contributing Factors (not root causes)
- Alert on error rate was too late (pool full = errors immediate)
- No pre-deployment pool validation
- Runbook didn't document pool sizing

### 5. Action Items (10 min)
| Action | Owner | Deadline | Priority |
|--------|-------|----------|----------|
| Auto-size pool based on instances | Backend lead | 2 weeks | P0 |
| Add pool usage alert (80%+ critical) | Oncall | 1 week | P0 |
| Add pre-deploy validation check | DevOps | 1 week | P1 |
| Document pool sizing in runbook | Tech writer | 3 days | P1 |

### 6. Prevention Ideas (10 min)
[Brainstorm how to prevent similar incidents]

### 7. Blameless Check (5 min)
- Did we focus on facts/systems, not people? ✓
- Did we assume good intent? ✓
- Are all participants comfortable with the report? ✓
```

### After Postmortem
- Distribute report to all team (transparency)
- Track action items (check in 2 weeks)
- Close the loop (what did we learn?)

## RCA (Root Cause Analysis) Framework

**Don't stop at the symptom**:
```
❌ Root cause: Operator error
✓ Root cause: No automated validation → human forgot step

❌ Root cause: Connection pool too small
✓ Root cause: Pool size is manual config, no auto-sizing based on scale

❌ Root cause: Developer didn't check metrics
✓ Root cause: No alert on pool usage %, alert was on error rate too late
```

## Blameless Culture Principles

1. **Assume good intent** — Engineer did their best with information available
2. **Focus on systems** — What failed in the process/tooling/documentation?
3. **No "stupid" mistakes** — If someone made a mistake, how do we prevent it systematically?
4. **Psychological safety** — Team must feel safe to admit mistakes and learn
5. **Shared responsibility** — Incident is team's problem, not individual's
6. **Action items** — Every postmortem must end with concrete improvements

## Incident Communication

**During incident** (update every 5-10 minutes):
```
🟡 INCIDENT: API service degraded
Status: INVESTIGATING
Impact: Users may experience 50% error rate
Last update: 14:35 UTC
Next update: 14:40 UTC

https://status.example.com/incidents/[id]
```

**When resolved**:
```
✅ RESOLVED: API service
Status: RESOLVED (14:39 UTC)
Duration: 7 minutes
Impact: ~2000 users affected
Postmortem link: [link]

Thank you for your patience.
```

## Metrics to Track

- **MTTR** (Mean Time To Recovery): Target < 30 min SEV1
- **Detection time**: How fast did we notice?
- **Resolution time**: How fast did we fix?
- **Repeat incidents**: Same root cause within 6 months?
- **Postmortem quality**: All action items tracked?
- **Prevention success**: Did fixes prevent recurrence?

---

**Status**: Ready for production incident response  
**Best for**: Production incidents, postmortems, RCA, blameless culture
