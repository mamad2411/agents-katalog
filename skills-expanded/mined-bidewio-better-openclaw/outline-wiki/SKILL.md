---
name: outline-wiki
description: "Manage team wiki and documentation using Outline at {{OUTLINE_HOST}}:{{OUTLINE_PORT}}."
metadata:
  openclaw:
    emoji: "📝"
---

# Outline Wiki

Outline is available at `http://{{OUTLINE_HOST}}:{{OUTLINE_PORT}}` within the Docker network.

## Search Documents

```bash
curl -X POST "http://{{OUTLINE_HOST}}:{{OUTLINE_PORT}}/api/documents.search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OUTLINE_API_KEY" \
  -d '{"query": "getting started"}'
```

## Create Document

```bash
curl -X POST "http://{{OUTLINE_HOST}}:{{OUTLINE_PORT}}/api/documents.create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OUTLINE_API_KEY" \
  -d '{"title": "Setup Guide", "text": "# Getting Started\n\nWelcome!", "collectionId": "{collection_id}", "publish": true}'
```

## Tips for AI Agents

- Outline uses Markdown for all documents with rich editing support.
- Organize documents in collections with nested structure.
- Full-text search across all documents and collections.
- Supports integrations with Slack, OIDC, and webhooks.
