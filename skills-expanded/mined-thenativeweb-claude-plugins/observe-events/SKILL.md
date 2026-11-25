---
name: observe-events
description: Observe events in real time from an EventSourcingDB instance. Use when the user wants to watch, monitor, or stream live events as they are written.
allowed-tools: Bash, Read, AskUserQuestion
---

# Observe Events

Observe events in real time from an EventSourcingDB instance. This opens a long-lived streaming connection.

## Shared Instructions

First read `${CLAUDE_PLUGIN_ROOT}/shared/common.md`. It explains how to determine the base URL and API token, how to handle NDJSON responses, and which conventions apply. Follow it throughout this skill.

Also read `${CLAUDE_PLUGIN_ROOT}/shared/cloudevents.md`. It explains how returned events are structured, including the EventSourcingDB-specific metadata fields.

## Request

This endpoint returns a long-lived NDJSON stream. Always use `--max-time` to ensure the connection terminates (default: 30 seconds):

```bash
curl -s --no-buffer --max-time 30 -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d '<REQUEST_BODY>' \
  "${ESDB_URL:-http://localhost:3000}/api/v1/observe-events" \
  | grep -v '"type":"heartbeat"'
```

When the user wants a custom timeout, use AskUserQuestion to ask for the desired duration in seconds.

### Request Body

```json
{
  "subject": "/<subject-path>",
  "options": {
    "recursive": false,
    "lowerBound": {
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

Options:

- **`recursive`** (boolean): Include sub-subjects.
- **`lowerBound`**: Resume from event ID. `type`: `"inclusive"` or `"exclusive"`.
- **`fromLatestEvent`**: Start from last event of given type. `ifEventIsMissing`: `"read-everything"` or `"wait-for-event"`. Cannot be combined with `lowerBound`.

### Example

```bash
curl -s --no-buffer --max-time 30 -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d "{
    \"subject\": \"/\",
    \"options\": {
      \"recursive\": true
    }
  }" \
  "${ESDB_URL:-http://localhost:3000}/api/v1/observe-events" \
  | grep -v '"type":"heartbeat"'
```

## Response

NDJSON stream with one line per event:

```json
{"type":"event","payload":{...}}
```
