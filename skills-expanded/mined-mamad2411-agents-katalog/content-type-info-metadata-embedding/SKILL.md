---
name: content-type-info-metadata-embedding
description: Embed structured metadata per content type (mime_type, group, description, extensions, is_text) at codegen time so callers can convert predictions to human output or filter by group without lookup tables.
category: data
version: 1.0.0
version_origin: extracted
confidence: high
tags: [magika, data]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Content Type Info Metadata Embedding

**Trigger:** Building a classifier whose output needs human-readable enrichment (MIME type, file extensions, broad category) at every call site.

## Steps

- Source metadata from a single canonical JSON (assets/content_types_kb.min.json).
- Code generator emits a const TypeInfo struct per content type with all metadata fields.
- Add an info() / get_info() method on the ContentType enum that returns the struct.
- Standardize the group taxonomy (text, image, archive, executable, binary, …) and document it.
- Allow filtering: content_types.filter(ct => ct.is_text) or ct.group == 'text'.
- Test that every label has complete metadata at codegen time — missing fields fail the build.

## Counter / Caveats

- Metadata can be stale or wrong for obscure types; validate against real samples occasionally.
- MIME type is not 1-to-1 with label (e.g. .txt vs text/markdown); use is_text for binary/text filtering.
- Extensions list grows over time; document the preferred extension explicitly.
- Custom group taxonomy may not align with IANA / file(1) groups; document the difference for integrators.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `rust/gen/src/main.rs:65-82`
- `python/src/magika/types/content_type_info.py`
- `js/src/content-type-info.ts`
- `go/magika/content.go`
