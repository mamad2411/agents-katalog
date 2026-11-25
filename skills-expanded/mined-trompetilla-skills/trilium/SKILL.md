---
name: trilium
description: Work with Trilium Notes (notebook app) and automate via Trilium Notes ETAPI. This skill allows you to read, search, and create notes in your Trilium database. Use to manage notebook content or search for information within Trilium. To get started: (1) In Trilium, go to Options -> ETAPI and create a new ETAPI token. (2) Set TRILIUM_ETAPI_TOKEN and TRILIUM_SERVER_URL in your environment or .env file.
---

# Trilium Notes

Work with Trilium Notes via the [ETAPI](https://github.com/zadam/trilium/wiki/Etapi).

## Configuration

This skill requires a Trilium ETAPI token and the server URL. These should be stored in the environment or passed by the user.

- `TRILIUM_ETAPI_TOKEN`: Your ETAPI token (generated in Trilium -> Options -> ETAPI).
- `TRILIUM_SERVER_URL`: The URL of your Trilium server (e.g., `http://localhost:8080`).

## Core Concepts

- **Note ID**: A unique identifier for a note (e.g., `root`, `_day_2026-02-11`).
- **Attributes**: Metadata attached to notes (labels, relations).
- **ETAPI**: The External Trilium API, a REST API for interacting with the database.

## Common Workflows

### 1. Create a Note
To create a note, you need a `parentNoteId` and the note's content.
```bash
# Example using curl (conceptual)
curl -X POST "$TRILIUM_SERVER_URL/etapi/notes" \
     -H "Authorization: $TRILIUM_ETAPI_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "parentNoteId": "root",
       "title": "My New Note",
       "type": "text",
       "content": "Hello Trilium!"
     }'
```

### 2. Search Notes
Use the search endpoint to find notes by title or content.
```bash
curl "$TRILIUM_SERVER_URL/etapi/notes?search=My+Note" \
     -H "Authorization: $TRILIUM_ETAPI_TOKEN"
```

### 3. Get Note Content
```bash
curl "$TRILIUM_SERVER_URL/etapi/notes/$NOTE_ID/content" \
     -H "Authorization: $TRILIUM_ETAPI_TOKEN"
```

## Reference Documentation
For detailed API information, see [references/api.md](references/api.md).
