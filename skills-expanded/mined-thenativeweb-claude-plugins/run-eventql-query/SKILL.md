---
name: run-eventql-query
description: Run an EventQL query against an EventSourcingDB instance. Use when the user wants to query, filter, aggregate, or analyze events using the EventQL query language.
allowed-tools: Bash, Read, AskUserQuestion
---

# Run EventQL Query

Run an EventQL query against an EventSourcingDB instance.

## Shared Instructions

First read `${CLAUDE_PLUGIN_ROOT}/shared/common.md`. It explains how to determine the base URL and API token, how to handle NDJSON responses, and which conventions apply. Follow it throughout this skill.

Also read `${CLAUDE_PLUGIN_ROOT}/shared/cloudevents.md` when query results contain full events. It explains how events are structured, including the EventSourcingDB-specific metadata fields.

## Request

This endpoint returns NDJSON:

```bash
curl -s --no-buffer -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d '<REQUEST_BODY>' \
  "${ESDB_URL:-http://localhost:3000}/api/v1/run-eventql-query" \
  | grep -v '"type":"heartbeat"'
```

### Request Body

```json
{
  "query": "<EventQL query>"
}
```

### Example

```bash
curl -s --no-buffer -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  -H "content-type: application/json" \
  -d "{\"query\": \"FROM e IN events PROJECT INTO e\"}" \
  "${ESDB_URL:-http://localhost:3000}/api/v1/run-eventql-query" \
  | grep -v '"type":"heartbeat"'
```

## Common EventQL Patterns

- All events: `FROM e IN events PROJECT INTO e`
- Filter by type: `FROM e IN events WHERE e.type == "io.eventsourcingdb.library.book-acquired" PROJECT INTO e`
- Filter by subject: `FROM e IN events WHERE e.subject == "/books/42" PROJECT INTO e`
- Count: `FROM e IN events WHERE e.type == "io.eventsourcingdb.library.book-borrowed" PROJECT INTO { total: COUNT() }`
- Group by type: `FROM e IN events GROUP BY e.type PROJECT INTO { type: UNIQUE(e.type), count: COUNT() }`
- Latest N events: `FROM e IN events ORDER BY e.time DESC TOP 10 PROJECT INTO e`

## Response

NDJSON stream with one line per result row:

```json
{"type":"row","payload":{...}}
```
