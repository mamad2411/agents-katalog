---
name: read-event-type
description: Read details about a single event type from an EventSourcingDB instance. Use when the user wants to inspect a specific event type, check if it has a schema, or see its details.
allowed-tools: Bash, Read, AskUserQuestion
---

# Read Event Type

Get details about a single event type from an EventSourcingDB instance.

## Shared Instructions

First read `${CLAUDE_PLUGIN_ROOT}/shared/common.md`. It explains how to determine the base URL and API token, how to handle NDJSON responses, and which conventions apply. Follow it throughout this skill.

## Request

```bash
curl -s -i -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d '<REQUEST_BODY>' \
  "${ESDB_URL:-http://localhost:3000}/api/v1/read-event-type"
```

### Request Body

```json
{
  "eventType": "<reverse.domain.event-type>"
}
```

### Example

```bash
curl -s -i -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d '{"eventType": "io.eventsourcingdb.library.book-acquired"}' \
  "${ESDB_URL:-http://localhost:3000}/api/v1/read-event-type"
```

## Response

JSON object:

```json
{
  "eventType": "io.eventsourcingdb.library.book-acquired",
  "isPhantom": false,
  "schema": { ... }
}
```
