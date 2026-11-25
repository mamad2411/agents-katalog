---
name: managing-hightouch
description: |
  Use when working with Hightouch — hightouch reverse ETL management — monitor
  syncs, destinations, models, sources, and sync run health. Use when debugging
  sync failures, inspecting record delivery, auditing field mappings, or
  reviewing sync schedules and performance.
connection_type: hightouch
preload: false
---

# Managing Hightouch

Manage and monitor Hightouch reverse ETL — syncs, destinations, models, and sync run health.

## Discovery Phase

```bash
#!/bin/bash

HIGHTOUCH_API="https://api.hightouch.com/api/v1"
AUTH="Authorization: Bearer $HIGHTOUCH_API_KEY"

echo "=== Sources ==="
curl -s -H "$AUTH" "$HIGHTOUCH_API/sources" \
  | jq -r '.data[] | [.id, .name, .type, .slug] | @tsv' | column -t | head -10

echo ""
echo "=== Destinations ==="
curl -s -H "$AUTH" "$HIGHTOUCH_API/destinations" \
  | jq -r '.data[] | [.id, .name, .type, .slug] | @tsv' | column -t | head -10

echo ""
echo "=== Models ==="
curl -s -H "$AUTH" "$HIGHTOUCH_API/models" \
  | jq -r '.data[] | [.id, .name, .slug, .sourceId, .primaryKey] | @tsv' | column -t | head -15

echo ""
echo "=== Syncs ==="
curl -s -H "$AUTH" "$HIGHTOUCH_API/syncs" \
  | jq -r '.data[] | [.id, .slug, .destinationId, .modelId, .schedule.type, .disabled] | @tsv' | column -t | head -15
```

## Analysis Phase

```bash
#!/bin/bash

HIGHTOUCH_API="https://api.hightouch.com/api/v1"
AUTH="Authorization: Bearer $HIGHTOUCH_API_KEY"

echo "=== Recent Sync Runs ==="
curl -s -H "$AUTH" "$HIGHTOUCH_API/syncs/runs?limit=15&orderBy=createdAt&order=desc" \
  | jq -r '.data[] | [.id, .syncId, .status, .recordsProcessed, .recordsFailed, .completedAt] | @tsv' | column -t

echo ""
echo "=== Failed Sync Runs ==="
curl -s -H "$AUTH" "$HIGHTOUCH_API/syncs/runs?status=failed&limit=10" \
  | jq -r '.data[] | [.id, .syncId, .startedAt, .error[:60]] | @tsv' | column -t

echo ""
echo "=== Sync Performance Summary ==="
for SYNC_ID in $(curl -s -H "$AUTH" "$HIGHTOUCH_API/syncs" | jq -r '.data[:5][].id'); do
  SYNC_SLUG=$(curl -s -H "$AUTH" "$HIGHTOUCH_API/syncs/$SYNC_ID" | jq -r '.data.slug')
  LAST_RUN=$(curl -s -H "$AUTH" "$HIGHTOUCH_API/syncs/$SYNC_ID/runs?limit=1" \
    | jq '{status: .data[0].status, processed: .data[0].recordsProcessed, failed: .data[0].recordsFailed, duration: .data[0].duration}')
  echo "$SYNC_SLUG: $LAST_RUN"
done

echo ""
echo "=== Sync Configuration ==="
curl -s -H "$AUTH" "$HIGHTOUCH_API/syncs/$HIGHTOUCH_SYNC_ID" \
  | jq '{slug: .data.slug, schedule: .data.schedule, destination: .data.destinationId, model: .data.modelId, configuration: .data.configuration | keys}'

echo ""
echo "=== Sync Alerts ==="
curl -s -H "$AUTH" "$HIGHTOUCH_API/syncs/$HIGHTOUCH_SYNC_ID/alerts" \
  | jq -r '.data[] | [.type, .status, .threshold, .lastTriggeredAt] | @tsv' | column -t | head -5
```

## Output Format

```
SOURCES
ID       Name             Type        Slug
<id>     <source-name>    <type>      <slug>

DESTINATIONS
ID       Name             Type        Slug
<id>     <dest-name>      <type>      <slug>

SYNCS
ID       Slug             Dest ID   Model ID   Schedule    Disabled
<id>     <sync-slug>      <did>     <mid>      <type>      false

SYNC RUNS
ID       Sync ID  Status      Processed  Failed   Completed
<id>     <sid>    success     <n>        <n>      <timestamp>

FAILED RUNS
ID       Sync ID  Started         Error
<id>     <sid>    <timestamp>     <message>
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

