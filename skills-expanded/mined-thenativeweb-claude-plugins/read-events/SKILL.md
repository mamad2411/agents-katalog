---
name: read-events
description: Read events from an EventSourcingDB instance. Use when the user wants to fetch, list, or view events for a subject, with optional filtering, ordering, and bounds.
allowed-tools: Bash, Read, AskUserQuestion
---

# Read Events

Read events for a subject from an EventSourcingDB instance.

## Shared Instructions

First read `${CLAUDE_PLUGIN_ROOT}/shared/common.md`. It explains how to determine the base URL and API token, how to handle NDJSON responses, and which conventions apply. Follow it throughout this skill.

Also read `${CLAUDE_PLUGIN_ROOT}/shared/cloudevents.md`. It explains how returned events are structured, including the EventSourcingDB-specific metadata fields.

## Request

This endpoint returns NDJSON:

```bash
curl -s --no-buffer -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d '<REQUEST_BODY>' \
  "${ESDB_URL:-http://localhost:3000}/api/v1/read-events" \
  | grep -v '"type":"heartbeat"'
```

### Request Body

```json
{
  "subject": "/<subject-path>",
  "options": {
    "recursive": false,
    "order": "chronological",
    "lowerBound": {
      "id": "<event-id>",
      "type": "inclusive"
    },
    "upperBound": {
      "id": "<event-id>",
      "type": "exclusive"
    },
    "fromLatestEvent": {
      "subject": "/<subject-path>",
      "type": "<event-type>",
      "ifEventIsMissing": "read-everything"
    }
  }
}
```

Options (all optional except `recursive` in `options`):

- **`recursive`** (boolean): Include sub-subjects.
- **`order`**: `"chronological"` (default) or `"antichronological"`.
- **`lowerBound`**: Filter events from this ID. `type`: `"inclusive"` or `"exclusive"`.
- **`upperBound`**: Filter events up to this ID. `type`: `"inclusive"` or `"exclusive"`.
- **`fromLatestEvent`**: Start from last event of given type. `ifEventIsMissing`: `"read-everything"` or `"read-nothing"`. Cannot be combined with `lowerBound`.

### Example

```bash
curl -s --no-buffer -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d "{
    \"subject\": \"/books/42\",
    \"options\": {
      \"recursive\": false
    }
  }" \
  "${ESDB_URL:-http://localhost:3000}/api/v1/read-events" \
  | grep -v '"type":"heartbeat"'
```

## Response

NDJSON stream with one line per event:

```json
{"type":"event","payload":{...}}
```
