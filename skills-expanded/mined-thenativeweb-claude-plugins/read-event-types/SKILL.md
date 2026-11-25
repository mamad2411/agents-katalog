---
name: read-event-types
description: Read all event types from an EventSourcingDB instance. Use when the user wants to list or discover all event types that exist in the event store.
allowed-tools: Bash, Read, AskUserQuestion
---

# Read Event Types

List all event types from an EventSourcingDB instance.

## Shared Instructions

First read `${CLAUDE_PLUGIN_ROOT}/shared/common.md`. It explains how to determine the base URL and API token, how to handle NDJSON responses, and which conventions apply. Follow it throughout this skill.

## Request

This endpoint returns NDJSON. No request body is required.

```bash
curl -s --no-buffer -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  "${ESDB_URL:-http://localhost:3000}/api/v1/read-event-types" \
  | grep -v '"type":"heartbeat"'
```

## Response

NDJSON stream with one line per event type:

```json
{"type":"eventType","payload":{"eventType":"io.eventsourcingdb.library.book-acquired","isPhantom":false,"schema":{...}}}
```
