---
name: paperless-ngx-docs
description: Document management with Paperless-ngx
version: 1.0.0
tags: [documents, ocr, archiving, self-hosted]
---

# Paperless-ngx – Document Management System

Paperless-ngx transforms physical documents into searchable digital
archives with OCR, tagging, and automated workflows.

- **GitHub**: github.com/paperless-ngx/paperless-ngx (25 000+ ⭐)
- **License**: GPL-3.0
- **Security**: Community-maintained. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{PAPERLESS_URL}}` | Base URL |
| `{{PAPERLESS_TOKEN}}` | API authentication token |

## Usage Examples

### List documents

```bash
curl -s "{{PAPERLESS_URL}}/api/documents/" \
  -H "Authorization: Token {{PAPERLESS_TOKEN}}"
```

### Upload a document

```bash
curl -s -X POST "{{PAPERLESS_URL}}/api/documents/post_document/" \
  -H "Authorization: Token {{PAPERLESS_TOKEN}}" \
  -F "document=@receipt.pdf"
```

### Search documents

```bash
curl -s "{{PAPERLESS_URL}}/api/documents/?query=invoice" \
  -H "Authorization: Token {{PAPERLESS_TOKEN}}"
```

## AI Agent Tips

- Automatic OCR on uploaded documents (Tesseract).
- AI-powered auto-tagging and correspondent matching.
- Consumption folder watches for new documents automatically.
- Full REST API for programmatic document management.
