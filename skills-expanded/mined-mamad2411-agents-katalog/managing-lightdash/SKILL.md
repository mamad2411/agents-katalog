---
name: managing-lightdash
description: |
  Use when working with Lightdash — lightdash BI management — monitor projects,
  dashboards, saved charts, spaces, and dbt model exploration. Use when
  reviewing dashboard health, inspecting chart queries, auditing project
  configuration, or checking scheduler status.
connection_type: lightdash
preload: false
---

# Managing Lightdash

Manage and monitor Lightdash BI — projects, dashboards, charts, spaces, and schedulers.

## Discovery Phase

```bash
#!/bin/bash

LIGHTDASH_API="$LIGHTDASH_URL/api/v1"
AUTH="Authorization: ApiKey $LIGHTDASH_API_KEY"

echo "=== Organization ==="
curl -s -H "$AUTH" "$LIGHTDASH_API/org" \
  | jq '.results | {name: .name, organizationUuid: .organizationUuid}'

echo ""
echo "=== Projects ==="
curl -s -H "$AUTH" "$LIGHTDASH_API/org/projects" \
  | jq -r '.results[] | [.projectUuid, .name, .type] | @tsv' | column -t | head -10

echo ""
echo "=== Spaces ==="
curl -s -H "$AUTH" "$LIGHTDASH_API/projects/$LIGHTDASH_PROJECT_UUID/spaces" \
  | jq -r '.results[] | [.uuid, .name, .isPrivate, .dashboardCount, .chartCount] | @tsv' | column -t | head -10

echo ""
echo "=== Dashboards ==="
curl -s -H "$AUTH" "$LIGHTDASH_API/projects/$LIGHTDASH_PROJECT_UUID/dashboards" \
  | jq -r '.results[] | [.uuid, .name, .spaceName, .updatedAt] | @tsv' | column -t | head -15
```

## Analysis Phase

```bash
#!/bin/bash

LIGHTDASH_API="$LIGHTDASH_URL/api/v1"
AUTH="Authorization: ApiKey $LIGHTDASH_API_KEY"

echo "=== Saved Charts ==="
curl -s -H "$AUTH" "$LIGHTDASH_API/projects/$LIGHTDASH_PROJECT_UUID/charts" \
  | jq -r '.results[] | [.uuid, .name, .chartType, .spaceName, .updatedAt] | @tsv' | column -t | head -15

echo ""
echo "=== Scheduler Jobs ==="
curl -s -H "$AUTH" "$LIGHTDASH_API/schedulers/jobs" \
  | jq -r '.results[:10][] | [.jobId, .jobType, .status, .createdAt] | @tsv' | column -t

echo ""
echo "=== Scheduler Logs (Recent) ==="
curl -s -H "$AUTH" "$LIGHTDASH_API/schedulers/logs?limit=10" \
  | jq -r '.results[] | [.schedulerUuid, .status, .createdAt, .details[:50] // ""] | @tsv' | column -t

echo ""
echo "=== dbt Explores (Models) ==="
curl -s -H "$AUTH" "$LIGHTDASH_API/projects/$LIGHTDASH_PROJECT_UUID/explores" \
  | jq -r '.results[] | [.name, .label, .tags // []] | @tsv' | column -t | head -15

echo ""
echo "=== Project Members ==="
curl -s -H "$AUTH" "$LIGHTDASH_API/projects/$LIGHTDASH_PROJECT_UUID/access" \
  | jq -r '.results[] | [.userUuid, .email, .role] | @tsv' | column -t | head -10
```

## Output Format

```
PROJECTS
UUID     Name             Type
<uuid>   <project-name>   <type>

DASHBOARDS
UUID     Name             Space           Updated
<uuid>   <dash-name>      <space-name>    <timestamp>

SAVED CHARTS
UUID     Name             Type        Space           Updated
<uuid>   <chart-name>     <type>      <space-name>    <timestamp>

SCHEDULER STATUS
Job ID   Type       Status      Created
<id>     <type>     <status>    <timestamp>

EXPLORES
Name             Label            Tags
<explore-name>   <label>          <tags>
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

