---
name: managing-grouparoo
description: |
  Use when working with Grouparoo — grouparoo reverse ETL management — monitor
  apps, sources, destinations, groups, properties, and sync runs. Use when
  debugging data sync issues, inspecting group membership, auditing property
  mappings, or reviewing run status.
connection_type: grouparoo
preload: false
---

# Managing Grouparoo

Manage and monitor Grouparoo reverse ETL — apps, sources, destinations, groups, and sync runs.

## Discovery Phase

```bash
#!/bin/bash

GROUPAROO_API="${GROUPAROO_URL:-http://localhost:3000}/api/v1"
AUTH="apiKey=$GROUPAROO_API_KEY"

echo "=== Status ==="
curl -s "$GROUPAROO_API/status?$AUTH" \
  | jq '{version: .version, uptime: .uptime, workers: .workers}'

echo ""
echo "=== Apps (Connections) ==="
curl -s "$GROUPAROO_API/apps?$AUTH" \
  | jq -r '.apps[] | [.id, .name, .type, .state] | @tsv' | column -t | head -10

echo ""
echo "=== Sources ==="
curl -s "$GROUPAROO_API/sources?$AUTH" \
  | jq -r '.sources[] | [.id, .name, .type, .appId, .state] | @tsv' | column -t | head -10

echo ""
echo "=== Destinations ==="
curl -s "$GROUPAROO_API/destinations?$AUTH" \
  | jq -r '.destinations[] | [.id, .name, .type, .appId, .state] | @tsv' | column -t | head -10

echo ""
echo "=== Groups ==="
curl -s "$GROUPAROO_API/groups?$AUTH" \
  | jq -r '.groups[] | [.id, .name, .type, .matchType, .calculatedMembersCount] | @tsv' | column -t | head -10
```

## Analysis Phase

```bash
#!/bin/bash

GROUPAROO_API="${GROUPAROO_URL:-http://localhost:3000}/api/v1"
AUTH="apiKey=$GROUPAROO_API_KEY"

echo "=== Recent Runs ==="
curl -s "$GROUPAROO_API/runs?$AUTH&limit=15&order=desc" \
  | jq -r '.runs[] | [.id, .creatorType, .state, .importsCreated, .profilesCreated, .completedAt] | @tsv' | column -t

echo ""
echo "=== Failed Runs ==="
curl -s "$GROUPAROO_API/runs?$AUTH&state=failed&limit=10" \
  | jq -r '.runs[] | [.id, .creatorType, .createdAt, .error[:60]] | @tsv' | column -t

echo ""
echo "=== Properties ==="
curl -s "$GROUPAROO_API/properties?$AUTH" \
  | jq -r '.properties[] | [.id, .key, .type, .sourceId, .state] | @tsv' | column -t | head -15

echo ""
echo "=== Exports (Recent) ==="
curl -s "$GROUPAROO_API/exports?$AUTH&limit=10&order=desc" \
  | jq -r '.exports[] | [.id, .destinationId, .state, .completedAt, .errorMessage // ""] | @tsv' | column -t

echo ""
echo "=== Profile Stats ==="
curl -s "$GROUPAROO_API/profiles?$AUTH&limit=1" \
  | jq '{totalProfiles: .total}'

echo ""
echo "=== Schedules ==="
curl -s "$GROUPAROO_API/schedules?$AUTH" \
  | jq -r '.schedules[] | [.id, .sourceId, .recurring, .recurringFrequency, .state] | @tsv' | column -t | head -10
```

## Output Format

```
STATUS
Version:     <version>
Workers:     <n>

APPS
ID       Name         Type       State
<id>     <app-name>   <type>     ready

SOURCES / DESTINATIONS
ID       Name         Type       App      State
<id>     <name>       <type>     <app>    ready

GROUPS
ID       Name         Type       Match    Members
<id>     <group>      <type>     <match>  <count>

RECENT RUNS
ID       Creator      State      Imports  Profiles  Completed
<id>     <type>       complete   <n>      <n>       <timestamp>
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

