---
name: managing-census
description: |
  Use when working with Census — census reverse ETL management — monitor syncs,
  destinations, models, source connections, and sync run health. Use when
  debugging sync failures, inspecting record delivery, auditing destination
  mappings, or reviewing sync schedules.
connection_type: census
preload: false
---

# Managing Census

Manage and monitor Census reverse ETL — syncs, destinations, models, and sync run health.

## Discovery Phase

```bash
#!/bin/bash

CENSUS_API="https://app.getcensus.com/api/v1"
AUTH="Authorization: Bearer $CENSUS_API_TOKEN"

echo "=== Sources ==="
curl -s -H "$AUTH" "$CENSUS_API/sources" \
  | jq -r '.data[] | [.id, .name, .type, .connection_details.host // "cloud"] | @tsv' | column -t | head -10

echo ""
echo "=== Destinations ==="
curl -s -H "$AUTH" "$CENSUS_API/destinations" \
  | jq -r '.data[] | [.id, .name, .type, .connection_details.instance_url // ""] | @tsv' | column -t | head -10

echo ""
echo "=== Models ==="
curl -s -H "$AUTH" "$CENSUS_API/models" \
  | jq -r '.data[] | [.id, .name, .source_id, .query[:50]] | @tsv' | column -t | head -15

echo ""
echo "=== Syncs ==="
curl -s -H "$AUTH" "$CENSUS_API/syncs" \
  | jq -r '.data[] | [.id, .label, .destination_object, .schedule_frequency, .paused] | @tsv' | column -t | head -15
```

## Analysis Phase

```bash
#!/bin/bash

CENSUS_API="https://app.getcensus.com/api/v1"
AUTH="Authorization: Bearer $CENSUS_API_TOKEN"

echo "=== Recent Sync Runs ==="
curl -s -H "$AUTH" "$CENSUS_API/sync_runs?limit=15&order=desc" \
  | jq -r '.data[] | [.id, .sync_id, .status, .records_processed, .records_failed, .created_at] | @tsv' | column -t

echo ""
echo "=== Failed Sync Runs ==="
curl -s -H "$AUTH" "$CENSUS_API/sync_runs?status=failed&limit=10" \
  | jq -r '.data[] | [.id, .sync_id, .created_at, .error_message[:60]] | @tsv' | column -t

echo ""
echo "=== Sync Health Summary ==="
for SYNC_ID in $(curl -s -H "$AUTH" "$CENSUS_API/syncs" | jq -r '.data[:5][].id'); do
  SYNC_NAME=$(curl -s -H "$AUTH" "$CENSUS_API/syncs/$SYNC_ID" | jq -r '.data.label')
  LAST_RUN=$(curl -s -H "$AUTH" "$CENSUS_API/syncs/$SYNC_ID/sync_runs?limit=1" \
    | jq '{status: .data[0].status, records_processed: .data[0].records_processed, records_failed: .data[0].records_failed}')
  echo "$SYNC_NAME: $LAST_RUN"
done

echo ""
echo "=== Sync Field Mappings ==="
curl -s -H "$AUTH" "$CENSUS_API/syncs/$CENSUS_SYNC_ID" \
  | jq -r '.data.mappings[] | [.from.data, .to, .operation] | @tsv' | column -t | head -10
```

## Output Format

```
SOURCES
ID       Name             Type         Host
<id>     <source-name>    <type>       <host>

DESTINATIONS
ID       Name             Type         Instance
<id>     <dest-name>      <type>       <url>

SYNCS
ID       Label            Object          Frequency   Paused
<id>     <sync-label>     <dest-object>   <freq>      false

SYNC RUNS
ID       Sync ID  Status      Processed  Failed   Created
<id>     <sid>    completed   <n>        <n>      <timestamp>

FAILED RUNS
ID       Sync ID  Created         Error
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

