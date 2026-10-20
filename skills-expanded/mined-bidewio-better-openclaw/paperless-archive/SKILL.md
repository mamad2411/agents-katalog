---
name: paperless-archive
description: "Archive and OCR documents using Paperless-ngx at {{PAPERLESS_HOST}}:{{PAPERLESS_PORT}}."
metadata:
  openclaw:
    emoji: "🗂️"
---

# Paperless Archive

Paperless-ngx is available at `http://{{PAPERLESS_HOST}}:{{PAPERLESS_PORT}}` within the Docker network.

## Upload Document

```bash
curl -X POST "http://{{PAPERLESS_HOST}}:{{PAPERLESS_PORT}}/api/documents/post_document/" \
  -H "Authorization: Token $PAPERLESS_TOKEN" \
  -F "document=@/data/input/invoice.pdf"
```

## Search Documents

```bash
curl "http://{{PAPERLESS_HOST}}:{{PAPERLESS_PORT}}/api/documents/?query=invoice" \
  -H "Authorization: Token $PAPERLESS_TOKEN"
```

## Tips for AI Agents

- Paperless-ngx automatically OCRs uploaded documents for full-text search.
- Supports PDF, PNG, JPG, TIFF, and other formats.
- Auto-tagging and correspondent matching based on content.
