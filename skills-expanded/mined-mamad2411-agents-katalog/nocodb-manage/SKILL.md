---
name: nocodb-manage
description: "Manage spreadsheet-style databases using NocoDB REST API at {{NOCODB_HOST}}:{{NOCODB_PORT}}."
metadata:
  openclaw:
    emoji: "📋"
---

# NocoDB Manage

NocoDB is available at `http://{{NOCODB_HOST}}:{{NOCODB_PORT}}` within the Docker network.

## List Records

```bash
curl -X GET "http://{{NOCODB_HOST}}:{{NOCODB_PORT}}/api/v1/db/data/noco/{project_id}/{table_id}" \
  -H "xc-auth: $NOCODB_AUTH_TOKEN"
```

## Create Record

```bash
curl -X POST "http://{{NOCODB_HOST}}:{{NOCODB_PORT}}/api/v1/db/data/noco/{project_id}/{table_id}" \
  -H "Content-Type: application/json" \
  -H "xc-auth: $NOCODB_AUTH_TOKEN" \
  -d '{"Title": "New Item", "Status": "Active"}'
```

## Tips for AI Agents

- NocoDB turns any database into a smart spreadsheet via REST API.
- Use filters and sorting in query parameters for efficient data retrieval.
- Supports webhooks for event-driven automation.
