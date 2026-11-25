---
name: zotero-research
description: Search and inspect the user's local Zotero library with OmniScholar. Use for collections, bibliographic metadata, notes, annotations, attachments, indexed text, local-paper matching, or selecting a PDF without modifying Zotero.
license: MIT
---

# Read-only Zotero research

Follow the user's language. Zotero is strictly GET-only: never create, edit, tag, move, or delete library data.

## Workflow

1. Use `zotero_collections` to list collections, read one collection, or list its top-level items.
2. Use `zotero_search` with DOI first, then distinctive title terms. Omit `query` or use `*` to browse; bound `limit` and pagination.
3. Match normalized DOI first. Otherwise compare normalized title, year, and first author. Report ambiguity instead of guessing.
4. Use `zotero_item` with `mode=item` for metadata-only work. Use `mode=aggregate` only when notes, annotations, attachments, indexed text, or PDF selection are needed.
5. If several PDFs are available, list their attachment keys and filenames and ask the user to confirm one `attachmentKey` before parsing or synchronizing. Never assume similarly named attachments are equivalent.
6. Treat unavailable or truncated indexed text as incomplete evidence, not an empty paper.
7. For necessary structured content, call `omnischolar_parse` directly after MinerU is configured and the selected PDF upload is authorized. The parse call checks cache or uploads before publication checks.
8. Use `omnischolar_sync action=plan` for an explicit managed-output synchronization decision, not as a mandatory parse preflight. `missing`, `excluded`, `conflict`, and `recovery_required` each retain their explicit publication workflow.

If Zotero is unavailable, ask the user to start Zotero and enable local application access. Keep `http://127.0.0.1:23119/api` on the local machine. If a local item is absent, use `scholar-search` only when online discovery matches the request.
