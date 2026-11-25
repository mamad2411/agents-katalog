---
name: "runbook-patterns"
description: "Runbook patterns: the 3AM test, symptom-cause-remedy structure, command documentation, ordered causes, verification after remediation, escalation gates, SLA awareness, a postmortem template, and anti-patterns. Use when writing or reviewing runbooks."
---

# Runbook Patterns

## The 3AM Test

A runbook passes the 3AM test if a competent on-call engineer can:
1. Find the runbook from the alert within 30 seconds (alert must link directly to runbook)
2. Understand the scope within 60 seconds (overview section)
3. Start diagnosing within 2 minutes (first command is on screen without scrolling)

If any of these fail, the runbook will be abandoned during an incident.

## Structure Pattern: Symptom → Cause → Remedy

The fundamental runbook pattern. Every diagnostic section follows this sequence:

```markdown
### Step N: Diagnose [hypothesis]

**Why check this**: [One sentence on why this matters / what it rules out]

**Command:**
```bash
kubectl logs -n production -l app=api --since=5m | tail -50
```

**If you see [specific output]**: This indicates [cause]. Go to [Step X].
**If you see [other output]**: This indicates [other cause]. Go to [Step Y].
**If the command fails**: [What to do if the command itself doesn't work].
```

Never leave the engineer without a next step. Every diagnosis branch must resolve to either a remediation or an escalation.

## Command Documentation Pattern

Commands in runbooks must be self-contained. The engineer should not have to look anything up:

```markdown
# Bad: requires knowledge outside the runbook
kubectl get pods | grep Crash

# Bad: requires substitution
kubectl describe pod <pod-name> -n <namespace>

# Good: complete, copy-paste ready
# First, find the pod name:
POD=$(kubectl get pods -n production -l app=api-server -o jsonpath='{.items[0].metadata.name}')

# Then describe it:
kubectl describe pod $POD -n production
```

Command blocks must include:
- Complete commands with no required substitution (or variable setup at top)
- Expected output for the "healthy" case
- Expected output for each "problem" case
- What the output means (do not leave interpretation to the engineer)

## Ordered Causes Pattern

List causes in frequency order. The engineer should try the most common diagnosis first:

```markdown
## Common Causes

This alert fires for three reasons, listed by frequency:

1. **Database connection pool exhaustion** (~55% of occurrences)
   Diagnose: [link to Step 2]

2. **Upstream service timeout** (~30% of occurrences)
   Diagnose: [link to Step 3]

3. **Memory leak after v2.4 deployment** (~15% of occurrences)
   Diagnose: [link to Step 4]
```

## Verification After Remediation

Every remediation step must end with a verification command and expected output:

```markdown
### Remediation: Restart the API service

**Run:**
```bash
kubectl rollout restart deployment/api-server -n production
kubectl rollout status deployment/api-server -n production --timeout=5m
```

**Expected output:**
```
Waiting for deployment "api-server" rollout to finish: 0 of 3 updated replicas are available...
Waiting for deployment "api-server" rollout to finish: 1 of 3 updated replicas are available...
deployment "api-server" successfully rolled out
```

**Verify resolution:**
Check [Error Rate Dashboard](https://app.datadoghq.com/dashboard/xyz) - error rate
should drop below 0.1% within 2 minutes. If it does not, proceed to Option B.
```

## Escalation Gate Pattern

Escalation conditions must be deterministic -- not judgment calls:

```markdown
# Bad: requires judgment
Escalate if the problem seems serious.

# Good: deterministic condition
Escalate to the platform-lead immediately if ANY of the following:
- Error rate has not decreased after 10 minutes of remediation
- kubectl commands return errors (cluster may be degraded)
- You observe any data loss symptoms (mismatched record counts, corrupted responses)
- This is a P1 and you are not 100% confident in your next action

When calling, have ready:
- Current error rate and trend (link to dashboard)
- Steps already attempted and their results
- Relevant log lines (paste them, do not describe them)
```

## SLA Awareness Pattern

On-call engineers need SLA budget context before making downtime decisions:

```markdown
> **Before taking the service offline**: Check current SLA status.
> SLA target: 99.9% uptime (43.8 minutes/month budget)
> Current status: [status.company.com](https://status.company.com)
>
> If budget is < 15 minutes remaining: escalate to platform-lead before
> any action that causes downtime, even for maintenance.
```

## Postmortem Template Pattern

Postmortems require blameless framing and actionable follow-up:

```markdown
## Incident: [Date] - [Brief description]

**Duration**: HH:MM (Detection: HH:MM, Resolution: HH:MM)
**Severity**: P[N]
**Impact**: [Users affected, requests failed, revenue impact if known]

## Timeline

| Time (UTC) | Event |
|-----------|-------|
| 14:23 | Alert fired: api_error_rate > 1% |
| 14:25 | On-call paged. Acknowledged. |
| 14:31 | Root cause identified: database connection pool exhausted |
| 14:38 | Remediation applied: pool size increased |
| 14:41 | Error rate dropped to 0.05%. Alert resolved. |

## Root Cause

[Technical description of what caused the incident. Blame the system, not people.]

## Contributing Factors

- [Factor 1: e.g., "Monitoring threshold was too high -- alert should have fired 10 minutes earlier"]
- [Factor 2: e.g., "Runbook did not cover this failure mode"]

## Action Items

| Action | Owner | Priority | Due |
|--------|-------|----------|-----|
| Lower alert threshold to fire earlier | Platform | P2 | 2024-04-01 |
| Update runbook to include connection pool diagnosis | Platform | P2 | 2024-03-25 |
| Add connection pool metric to dashboard | Platform | P3 | 2024-04-15 |
```

## Anti-Patterns

### The Tribal Knowledge Runbook
```
# Bad: requires context not in the runbook
Check the usual places. If it's the database thing, do the usual fix.

# Good: no assumed knowledge
Check the database connection pool:
[full diagnostic command with expected output]
```

### The Stale Runbook
A runbook with an old "last-tested" date is dangerous -- it implies the procedure is current when it may not be. Add to your CI or quarterly review:
```bash
# Find runbooks not tested in 90 days
find runbooks/ -name "*.md" | xargs grep -l "last-tested" | \
  xargs grep "last-tested" | awk -F: '{print $1, $NF}' | \
  awk '$2 < date -d "90 days ago"'
```

### The Vague Verification
```
# Bad: no verification
Restart the service if needed.

# Good: specific verification with expected outcome
kubectl rollout restart deployment/api -n production
# Wait until: kubectl rollout status deployment/api -n production
# shows: "successfully rolled out"
# Then verify on dashboard: error rate < 0.1% within 2 minutes
```

## References
- [Google SRE Book - On-Call](https://sre.google/sre-book/being-on-call/)
- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Atlassian Incident Management](https://www.atlassian.com/incident-management/runbook)
- [Blameless Postmortems (Etsy)](https://www.etsy.com/codeascraft/blameless-postmortems/)
