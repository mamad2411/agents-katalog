---
name: investigate-alert
description: Investigate a production alert or error. Use when an alert fires in the oncall channel, or the user says "investigate alert", "troubleshoot", "oncall alert", or "what's breaking".
alwaysApply: false
---

# Alert Investigation

Systematically investigates production alerts by mapping to code areas, querying error data, and tracing through backend services.

## Trigger

"investigate alert [link or description]" or "what's breaking in [service]?"

## Pre-Run

1. Read `.claude/skills/investigate-alert/gotchas.md` (if it exists)
2. Read `engineering/oncall/README.md` for debugging tools and useful links
3. Check if a matching runbook exists in `engineering/oncall/`

## Input Parsing

1. **Check for Slack thread links first.** Extract any URLs matching your Slack workspace pattern.
2. If Slack links found, read the thread(s) to gather alert context.
3. If no Slack links, check for a service name or error description.
4. If nothing useful is provided, fall back to reading the latest alert from the oncall channel.

## Step 1: Gather the Alert

From the alert message (Slack thread, PagerDuty, etc.), extract:
- **Severity**: Critical / Warning / Info
- **Event source**: Which service or feature is affected
- **Description**: What users can't do
- **Time window**: When it started
- **Existing investigation**: Has someone already started looking?

## Step 2: Map to Code Area

Use your team's event source → code area mapping table. Example structure:

| Event Source | Feature Area | Code Path |
|-------------|-------------|-----------|
| `service.feature.critical-error` | Feature Name | `src/path/to/feature/` |
| `service.api.timeout` | API Layer | `src/path/to/api/` |

**Customize this table** for your team's services and code structure.

## Step 3: Check Error Data

Query your observability tools for the error pattern:

```
# Example Snowflake/data warehouse query for error distribution
SELECT
  error_type,
  COUNT(*) AS error_count,
  COUNT(DISTINCT user_id) AS affected_users,
  MIN(timestamp) AS first_seen,
  MAX(timestamp) AS last_seen
FROM error_events
WHERE service = '[service]'
  AND timestamp > DATEADD(hour, -4, CURRENT_TIMESTAMP())
GROUP BY error_type
ORDER BY error_count DESC
```

Also check:
- [ ] Error rate dashboard — is this a spike or steady state?
- [ ] Recent deployments — did something just ship?
- [ ] Dependent service health — is an upstream/downstream service degraded?

## Step 4: Trace the Request Path

For errors involving API calls, trace through the service chain:

| Step | Service | What to Check |
|------|---------|---------------|
| 1 | Frontend / Client | Error boundary, network tab, console errors |
| 2 | BFF / API Gateway | Request logs, response codes, latency |
| 3 | Backend service | Application logs, database queries, external calls |
| 4 | Data layer | Query performance, connection pool, timeouts |

## Step 5: Determine Root Cause & Resolution

Classify the issue:
- **Deploy-related**: Recent code change introduced the error → rollback or hotfix
- **Data-related**: Bad data in database/cache → data fix or cleanup
- **Infrastructure**: Service/database/cache degradation → escalate to platform team
- **External dependency**: Third-party service down → implement fallback or wait

## Step 6: Document & Report

Present findings as:

```markdown
## Alert Investigation: [Alert Name]

**Severity:** [level]
**Impact:** [who's affected, what they can't do]
**Duration:** [start time] to [current/resolved]

### Root Cause
[1-2 sentences]

### Evidence
- [Error query results]
- [Dashboard screenshots/links]
- [Relevant deploy or change]

### Resolution
- [ ] [Action 1]
- [ ] [Action 2]

### Follow-up
- [ ] Create runbook if one doesn't exist
- [ ] Add monitoring for this failure mode
```

If the alert type didn't have a runbook, create one in `engineering/oncall/` using the template.

## Post-Run

Append to `.claude/skills/investigate-alert/runs.log`:
```
[date] | [alert source] | [root cause category] | [resolution] | [runbook created? Y/N]
```
