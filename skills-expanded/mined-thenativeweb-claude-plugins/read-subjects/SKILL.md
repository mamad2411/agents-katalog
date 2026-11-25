---
name: read-subjects
description: Read subjects from an EventSourcingDB instance. Use when the user wants to list, browse, or discover which subjects exist in the event store.
allowed-tools: Bash, Read, AskUserQuestion
---

# Read Subjects

List subjects that have received events in an EventSourcingDB instance.

## Shared Instructions

First read `${CLAUDE_PLUGIN_ROOT}/shared/common.md`. It explains how to determine the base URL and API token, how to handle NDJSON responses, and which conventions apply. Follow it throughout this skill.

## Request

This endpoint returns NDJSON:

```bash
curl -s --no-buffer -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d '<REQUEST_BODY>' \
  "${ESDB_URL:-http://localhost:3000}/api/v1/read-subjects" \
  | grep -v '"type":"heartbeat"'
```

### Request Body

```json
{
  "baseSubject": "/"
}
```

### Example

```bash
curl -s --no-buffer -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d '{"baseSubject": "/"}' \
  "${ESDB_URL:-http://localhost:3000}/api/v1/read-subjects" \
  | grep -v '"type":"heartbeat"'
```

## Response

NDJSON stream with one line per subject:

```json
{"type":"subject","payload":{"subject":"/books/42"}}
```
