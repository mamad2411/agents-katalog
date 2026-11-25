---
name: write-events
description: Write events to an EventSourcingDB instance. Use when the user wants to store, append, or publish events, optionally with preconditions such as optimistic locking or subject constraints.
allowed-tools: Bash, Read, AskUserQuestion
---

# Write Events

Write one or more events to an EventSourcingDB instance.

## Shared Instructions

First read `${CLAUDE_PLUGIN_ROOT}/shared/common.md`. It explains how to determine the base URL and API token, how to handle NDJSON responses, and which conventions apply. Follow it throughout this skill.

Also read `${CLAUDE_PLUGIN_ROOT}/shared/cloudevents.md`. It explains which event fields you must provide, which are server-managed, and how the fields are validated.

## Request

```bash
curl -s -i -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d '<REQUEST_BODY>' \
  "${ESDB_URL:-http://localhost:3000}/api/v1/write-events"
```

### Request Body

```json
{
  "events": [
    {
      "source": "<source-url>",
      "subject": "/<subject-path>",
      "type": "<reverse.domain.event-type>",
      "data": { ... }
    }
  ],
  "preconditions": [
    {
      "type": "<precondition-type>",
      "payload": { ... }
    }
  ]
}
```

The `preconditions` field is optional. Available precondition types:

- **`isSubjectPristine`** – Subject must have no events yet.
  ```json
  { "type": "isSubjectPristine", "payload": { "subject": "/books/42" } }
  ```

- **`isSubjectPopulated`** – Subject must already have events.
  ```json
  { "type": "isSubjectPopulated", "payload": { "subject": "/books/42" } }
  ```

- **`isSubjectOnEventId`** – Optimistic locking: last event must match given ID.
  ```json
  { "type": "isSubjectOnEventId", "payload": { "subject": "/books/42", "eventId": "0" } }
  ```

- **`isEventQlQueryTrue`** – Custom condition via EventQL query.
  ```json
  { "type": "isEventQlQueryTrue", "payload": { "query": "FROM e IN events WHERE e.data.title == 'Some Title' PROJECT INTO COUNT() == 0" } }
  ```

### Example

```bash
curl -s -i -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d "{
    \"events\": [
      {
        \"source\": \"https://example.com\",
        \"subject\": \"/books/42\",
        \"type\": \"io.eventsourcingdb.library.book-acquired\",
        \"data\": {
          \"title\": \"2001 - A Space Odyssey\",
          \"author\": \"Arthur C. Clarke\"
        }
      }
    ]
  }" \
  "${ESDB_URL:-http://localhost:3000}/api/v1/write-events"
```

## Response

The response is JSON containing an array of stored events.

A precondition failure returns HTTP `409 Conflict`.
