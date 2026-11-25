---
name: register-event-schema
description: Register a JSON Schema for an event type on an EventSourcingDB instance. Use when the user wants to add validation, define a schema, or enforce structure for an event type.
allowed-tools: Bash, Read, AskUserQuestion
---

# Register Event Schema

Register a JSON Schema for an event type on an EventSourcingDB instance. Once registered, all incoming events of that type are validated against the schema.

## Shared Instructions

First read `${CLAUDE_PLUGIN_ROOT}/shared/common.md`. It explains how to determine the base URL and API token, how to handle NDJSON responses, and which conventions apply. Follow it throughout this skill.

Also read `${CLAUDE_PLUGIN_ROOT}/shared/cloudevents.md`. It explains how event types are validated and which constraints apply to the `data` field that the schema describes.

## Request

```bash
curl -s -i -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d '<REQUEST_BODY>' \
  "${ESDB_URL:-http://localhost:3000}/api/v1/register-event-schema"
```

### Request Body

```json
{
  "eventType": "<reverse.domain.event-type>",
  "schema": {
    "type": "object",
    "properties": {
      "title": { "type": "string" }
    },
    "required": ["title"],
    "additionalProperties": false
  }
}
```

### Example

```bash
curl -s -i -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d "{
    \"eventType\": \"io.eventsourcingdb.library.book-acquired\",
    \"schema\": {
      \"type\": \"object\",
      \"properties\": {
        \"title\": { \"type\": \"string\" },
        \"author\": { \"type\": \"string\" }
      },
      \"required\": [\"title\", \"author\"],
      \"additionalProperties\": false
    }
  }" \
  "${ESDB_URL:-http://localhost:3000}/api/v1/register-event-schema"
```

## Response

JSON in CloudEvents format on success.

Schemas cannot be modified or removed once registered. Returns `409 Conflict` if a schema already exists for the event type.
