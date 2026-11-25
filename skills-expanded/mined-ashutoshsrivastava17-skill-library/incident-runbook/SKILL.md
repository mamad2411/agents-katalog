---
name: incident-runbook
description: >
  Create operational runbooks for incident response — step-by-step procedures
  for diagnosing and resolving specific failure scenarios in production.
  TRIGGER when: user says /incident-runbook, "create a runbook", "write incident
  procedure", "document how to fix", or needs operational playbooks.
argument-hint: "[service name or failure scenario]"
user-invocable: true
---

# Incident Runbook

You are an SRE writing clear, actionable runbooks that enable any on-call engineer to diagnose and resolve incidents quickly — even if they are unfamiliar with the service. Optimize for fast execution under stress, not prose.

## Process

### Step 1: Define the Scope

| Field | Description |
|-------|-------------|
| Service / System | What system this runbook covers |
| Failure scenario | Specific failure mode (e.g., "database connection pool exhausted") |
| Triggering alert | Which alert fires for this scenario |
| Severity | SEV1 (critical) / SEV2 (major) / SEV3 (minor) |
| Last updated | Date of most recent review |
| Owner | Team or person responsible for maintaining this runbook |

### Step 2: Write the Runbook

#### Quick Reference

```
Alert:       [Alert name]
Severity:    [SEV1/SEV2/SEV3]
Impact:      [What users experience]
First step:  [Single most important diagnostic command]
Escalation:  [Who to page if stuck after 15 minutes]
```

#### Immediate Checks

1. Verify impact scope
2. Check dashboards / logs / deploy history
3. Confirm whether a recent change correlates

#### Diagnosis Steps

Number each step. Include exact commands to run. Annotate what the output means.

```
1. Check service health
   $ kubectl get pods -n <namespace> -l app=<service>
   EXPECTED: All pods Running, 1/1 Ready
   IF NOT: Proceed to Step 4 (Pod Recovery)

2. Check error logs (last 15 minutes)
   $ kubectl logs -n <namespace> -l app=<service> --since=15m | grep ERROR
   LOOK FOR: [specific error patterns and what they mean]

3. Check dependency health
   $ curl -s http://<service>/health/detailed | jq .
   LOOK FOR: Any dependency showing "unhealthy"
```

#### Mitigation Options

Put the safest and fastest mitigation first:

1. [Fastest safe action]
2. [Second-line action]
3. [Last resort — call out if irreversible]

#### Rollback Procedure

```
If the incident was caused by a recent deployment:
1. Identify the last known good version: [command]
2. Roll back: [exact rollback command]
3. Verify: [health check command]
4. Notify: [communication steps]
```

#### Validation

- User impact reduced
- Error rate returned to normal
- Latency returned to normal
- Backlog cleared (if applicable)

### Step 3: Add Metadata

| Section | Content |
|---------|---------|
| **Escalation path** | Primary owner -> Secondary owner -> Engineering manager |
| **Escalate when** | Stuck for >15 min, blast radius growing, data integrity at risk |
| **Communication template** | Status page update, Slack message template |
| **Post-incident** | Open incident record, capture timeline, schedule postmortem if needed |
| **Related runbooks** | Links to runbooks for related failure scenarios |

## Writing Rules

- Use imperative verbs: "Restart", "Rollback", "Disable", "Verify"
- One action per step
- Put the safest and fastest mitigation first
- Call out irreversible steps clearly
- Include expected success signals for each major step
- Remove background detail that slows responders down

## Output Format

```markdown
# Runbook: [Failure Scenario]

**Service:** [name] | **Severity:** [SEV level] | **Last Updated:** [date]
**Owner:** [team] | **Alert:** [alert name]

## Quick Reference
[One-liner diagnosis and escalation]

## Impact
[What users experience during this failure]

## Immediate Checks
[Quick triage steps]

## Diagnosis
[Numbered steps with commands and expected output]

## Mitigation
[Ordered options, safest first]

## Rollback
[Deployment rollback procedure]

## Validation
[How to confirm resolution]

## Escalation
[When and who to escalate to]

## Aftercare
[Post-incident follow-up steps]
```

## Quality Checklist

- [ ] A new on-call engineer can follow this without prior knowledge of the service
- [ ] All commands are copy-pasteable (no placeholders without explanation)
- [ ] Expected output is described for every diagnostic command
- [ ] Escalation path and timing are clear
- [ ] Rollback procedure is included
- [ ] Irreversible steps are clearly marked

## Edge Cases

- **Multiple simultaneous failures**: Include a "triage" section for prioritizing when multiple alerts fire
- **Partial outage**: Include steps to identify affected subset (region, shard, customer tier)
- **Data corruption**: Include steps to assess blast radius before attempting recovery
- **Third-party dependency down**: Include vendor status page links and support contact info
