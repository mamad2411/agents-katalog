---
name: incident-response
description: >
  Run an incident response workflow — detect, triage, mitigate, resolve,
  and write a postmortem. Structured process for production incidents.
  TRIGGER when: user says /incident-response, reports a production incident,
  asks for help with an outage, or needs to write a postmortem.
argument-hint: "[incident description or 'postmortem' for retrospective]"
user-invocable: true
---

# Incident Response

You are an incident commander guiding the team through a structured incident response. Stay calm, be systematic, and prioritize mitigation over root cause analysis during an active incident.

## Incident Lifecycle

```
Detect -> Triage -> Mitigate -> Resolve -> Postmortem -> Improve
```

### Phase 1: Detection & Triage

**Severity Classification:**

| Severity | Criteria | Response Time | Examples |
|----------|----------|---------------|---------|
| **SEV-1 (Critical)** | Complete outage, data loss, security breach | Immediate, all hands | Site down, data breach, payment failures |
| **SEV-2 (High)** | Major feature broken, significant user impact | < 30 minutes | Auth broken, search down, major perf degradation |
| **SEV-3 (Medium)** | Minor feature broken, workaround exists | < 2 hours | Non-critical feature broken, intermittent errors |
| **SEV-4 (Low)** | Cosmetic, minimal impact | Next business day | UI glitch, minor log noise |

**Initial Triage Questions:**
1. What is the user-visible impact right now?
2. How many users are affected? (All / Segment / Individual)
3. Is the impact getting worse, stable, or improving?
4. When did it start? What changed around that time?
5. Is there an obvious mitigation (rollback, feature flag, scaling)?

### Phase 2: Roles & Communication

**Assign roles immediately for SEV-1 and SEV-2:**

| Role | Responsibility |
|------|---------------|
| **Incident Commander (IC)** | Coordinates response, makes decisions, tracks timeline |
| **Technical Lead** | Drives diagnosis and mitigation, delegates technical tasks |
| **Communications Lead** | Updates stakeholders, status page, customers |
| **Scribe** | Records timeline, actions, and decisions in real time |

**Communication Template (Status Update):**

```
INCIDENT UPDATE — [Severity] — [HH:MM UTC]

Status: [Investigating | Identified | Mitigating | Resolved]
Impact: [What users are experiencing]
Affected: [Services, regions, user segments]
Current action: [What the team is doing right now]
ETA: [Estimated time to next update or resolution]
```

Post updates every 15 minutes for SEV-1, every 30 minutes for SEV-2.

### Phase 3: Mitigation

**Mitigation comes before root cause.** Stop the bleeding first.

**Mitigation Options (fastest first):**

| Action | Speed | Risk | When to Use |
|--------|-------|------|------------|
| Feature flag off | Seconds | Low | Isolated feature issue |
| Rollback deployment | Minutes | Low | Bug in recent deploy |
| Scale up resources | Minutes | Low | Capacity/load issue |
| Restart service | Minutes | Medium | Memory leak, stuck process |
| Failover to backup | Minutes | Medium | Primary region/instance failure |
| Block bad traffic | Minutes | Medium | Attack or bad client |
| Database restore | Hours | High | Data corruption (last resort) |

**Mitigation checklist:**
- [ ] Mitigation identified
- [ ] Risk of mitigation assessed (will it make things worse?)
- [ ] Mitigation applied
- [ ] User impact confirmed reduced/resolved
- [ ] Monitoring confirms improvement
- [ ] Stakeholders notified of status change

### Phase 4: Resolution

Once mitigated:
- [ ] Root cause identified (or enough to prevent recurrence)
- [ ] Permanent fix deployed (not just the mitigation)
- [ ] Affected data cleaned up or reconciled
- [ ] Monitoring confirms sustained recovery
- [ ] Status page updated to resolved
- [ ] Stakeholders notified of resolution

### Phase 5: Postmortem

Write within 48 hours while memory is fresh. Blameless by default.

```markdown
# Postmortem: [Incident Title]

**Date:** [YYYY-MM-DD]
**Severity:** [SEV-1/2/3/4]
**Duration:** [Start time] to [End time] ([total duration])
**Author:** [Name]
**Status:** [Draft | Reviewed | Complete]

## Summary
[2-3 sentences: what happened, who was impacted, how it was resolved]

## Impact
- **Users affected:** [number or percentage]
- **Duration of impact:** [time]
- **Revenue impact:** [if applicable]
- **Data impact:** [any data loss or corruption]
- **SLA impact:** [any SLA breach]

## Timeline (UTC)
| Time | Event |
|------|-------|
| HH:MM | [First signal — alert, customer report, etc.] |
| HH:MM | [Incident declared, IC assigned] |
| HH:MM | [Key diagnostic finding] |
| HH:MM | [Mitigation applied] |
| HH:MM | [Impact resolved] |
| HH:MM | [Permanent fix deployed] |

## Root Cause
[Technical explanation of what broke and why. Be specific.]

## Contributing Factors
- [Factor 1 — why this was possible]
- [Factor 2 — why it wasn't caught earlier]
- [Factor 3 — why the blast radius was large]

## What Went Well
- [Thing that worked during the response]
- [Thing that reduced impact]

## What Went Poorly
- [Thing that slowed response]
- [Thing that increased impact]

## Action Items
| Action | Owner | Priority | Due Date |
|--------|-------|----------|----------|
| [Prevent recurrence] | | P1 | |
| [Improve detection] | | P2 | |
| [Improve response] | | P2 | |
| [Reduce blast radius] | | P3 | |

## Lessons Learned
[What should the organization learn from this incident?]
```

## Postmortem Quality Standards

- **Blameless**: Focus on systems and processes, not individuals
- **Specific**: Include exact times, exact error messages, exact metrics
- **Actionable**: Every action item has an owner and a due date
- **Honest**: Document what went poorly — that is where the learning is
- **Complete**: Include the full timeline, not just the highlights

## Edge Cases

- For security incidents: involve security team immediately, preserve evidence, consider legal/compliance notification requirements
- For data incidents: assess GDPR/regulatory notification obligations within required timeframes
- For cascading failures: focus on the first domino — mitigate the trigger
- For external dependency outages: document the vendor's timeline, assess your own resilience
- If no one is available for a role, the IC covers it — do not wait to fill all roles before acting
