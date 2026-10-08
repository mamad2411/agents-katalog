---
title: Dateiverwaltungs-Skill
description: Lade Dateien hoch, herunter, liste, suche und verwalte Dateien mit companyFILES MCP-Tools.
---

Verwende diesen Skill, wenn du Dateien hochladen oder finden, Download-Links abrufen, ZIP-Archive erstellen oder Text- und Code-Dateien speichern möchtest.

## Skill

````markdown
---
name: file-management-skill
description: Upload, download, list, search, and manage files with companyFILES MCP tools. Use when asked to upload a file, find a document, list stored files, get a download link, search documents by name or type, create a ZIP archive, or save a text/code file. Also covers discovering LibreChat file IDs for use in other tools.
---

# File Management Skill

Tools for uploading, listing, searching, downloading, archiving, and creating text files in companyFILES.

## Tools in This Skill

| Tool | Purpose |
|------|---------|
| `upload_file` | Upload any file (base64) for storage — returns document ID |
| `download_stored_file` | Get a download URL for a stored file |
| `list_documents` | List all your documents (optionally filter by folder) |
| `search_documents` | Search documents by filename, type, folder, or date range |
| `list_my_files` | List all accessible files (LibreChat + PVC storage) |
| `create_zip_from_stored_files` | Bundle stored documents into a ZIP archive |
| `create_text_file` | Create and store any text/code file (.sql, .csv, .json, .py, etc.) |

## Decision Guide

```
User wants to upload a file                   → upload_file
User wants a download link for a stored file  → download_stored_file
User wants to browse / list documents         → list_documents  (or open_companyfiles_ui from settings-ui-skill)
User wants to find a specific document        → search_documents
User wants to see all files including chat uploads → list_my_files
User wants to bundle files into a ZIP         → create_zip_from_stored_files
User wants to create a code/text file         → create_text_file
```

## Tool Usage

### upload_file

Max size: 50 MB by default (configurable via `MAX_FILE_SIZE_MB`). Content must be base64-encoded.

```json
{
  "content": "<base64-encoded file content>",
  "filename": "logo.png",
  "mime_type": "image/png",
  "folder": "assets"
}
```

Returns `{id, filename, downloadUrl, markdownLink}`. Use `id` as `document_id` in other tools.

---

### download_stored_file

```json
{
  "document_id": "abc12345-...",
  "return_content": false
}
```

Set `return_content: true` to also get base64 content (files < 1 MB only).

> To **read** the contents of Excel/Word/PDF files, use `read_excel` / `read_word` / `read_pdf` — not this tool.

---

### list_documents

```json
{
  "folder": "invoices"
}
```

Omit `folder` to list all documents. Also opens an embedded UI view for interactive browsing.

---

### search_documents

```json
{
  "search": "invoice",
  "type": "pdf",
  "folder": "invoices",
  "created_after": "2025-01-01",
  "created_before": "2025-06-01"
}
```

All parameters are optional. `search` is a case-insensitive substring match on filename. `type` values: `word`, `excel`, `powerpoint`, `pdf`, `text`, `image`, `archive`, `file`.

---

### list_my_files

```json
{}
```

Returns files from both LibreChat (chat uploads) and PVC (companyFILES storage). Each entry has either `file_id` (LibreChat) or `document_id` (PVC) or both. Use these IDs in read tools (`read_excel`, `read_word`, `read_pdf`) and `convert_document`.

---

### create_zip_from_stored_files

Max total uncompressed size: 50 MB.

```json
{
  "document_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "filename": "project_files",
  "compression_level": 6,
  "folder": "archives"
}
```

ZIP archives are **temporary** (auto-deleted after 1 day by default). They do not appear in `list_documents`. If some `document_ids` can't be resolved the ZIP is still created from the rest, and the unresolved IDs are returned in a `missingDocumentIds` field plus a `warning` (rather than failing).

---

### create_text_file

Works with essentially **any** text/code extension (`.sql`, `.csv`, `.json`, `.xml`, `.html`, `.css`, `.js`, `.ts`, `.tsx`, `.jsx`, `.py`, `.java`, `.kt`, `.swift`, `.scala`, `.go`, `.rs`, `.rb`, `.php`, `.c`, `.h`, `.cpp`, `.cs`, `.yaml`, `.yml`, `.toml`, `.md`, `.txt`, `.log`, `.sh`, `.bash`, `.zsh`, `.env`, `.ini`, `.cfg`, `.conf`, `.properties`, `.graphql`, `.proto`, …). The list is a **blocklist, not an allowlist** — any unblocked text extension is accepted. A few executable extensions are blocked for security (e.g. `.ps1`, `.bat`, `.exe`) and will be rejected even though they're text.

```json
{
  "content": "SELECT * FROM orders WHERE status = 'pending';",
  "filename": "pending_orders.sql",
  "folder": "queries"
}
```

```json
{
  "content": "#!/bin/bash\necho 'Hello World'",
  "filename": "hello.sh",
  "folder": "scripts"
}
```

## Key Notes

- `upload_file` validates file size (max 50 MB by default, via `MAX_FILE_SIZE_MB`) and extension.
- `document_id` from any create/upload tool can be reused in ZIP creation, template image injection (`document_id` in image placeholders), and `doc:` URI references in Markdown/HTML.
- Documents are auto-deleted after `DOCUMENT_RETENTION_DAYS` (default 365 days).
- For interactive file browsing, use `open_companyfiles_ui` from the **settings-ui-skill**.
````
