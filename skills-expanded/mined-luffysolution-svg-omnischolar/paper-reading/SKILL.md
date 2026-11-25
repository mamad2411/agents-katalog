---
name: paper-reading
description: Select a local Zotero PDF and publish its MinerU Markdown and assets for downstream reading. Use when a paper has not yet been parsed or the user explicitly requests a fresh parse; hand interpretation to literature-reading.
license: MIT
---

# Prepare a paper for local reading

This Skill owns attachment selection and MinerU publication, not interpretation. Its successful handoff is an exact `publication.markdownPath`, paper identity, and parser limitations.

## Workflow

1. Resolve the bibliographic parent and attachments with `zotero_item` in aggregate mode. If more than one PDF is available, list attachment keys and filenames, ask the user to choose, and do not parse or synchronize until an explicit `attachmentKey` is confirmed.
2. Reuse an already known, readable `publication.markdownPath` unless the user requested a fresh parse or the source identity/version is inconsistent. Do not query or upload again merely because interpretation was requested.
3. When parsing is needed, call `omnischolar_parse` directly after the user has authorized the selected PDF's external upload. The parse call performs MinerU cache lookup or upload before publication safety checks; do not make `omnischolar_sync action=plan` a mandatory parse preflight.
4. Do not set `force` unless the user explicitly requests a fresh parse and understands that it may upload the PDF again. Never use it to bypass a conflict, exclusion, missing publication, or interrupted transaction.
5. From the result, verify `publication.markdownPath`, bibliographic frontmatter, `metadata.json`, and sibling assets. Parsed image filenames begin with the Zotero key. Report OCR, formula, table, image, or layout limitations that affect downstream reading.
6. Hand all interpretation, evidence location, and figure/table/equation reading to `literature-reading`. Do not write an interpretation file from this Skill.

Read [references/sync.md](references/sync.md) only for an explicit synchronization, repair, exclusion, conflict, or recovery request. Those states govern publication, not whether MinerU may probe its cache or process an explicitly authorized PDF first.

If MinerU is unavailable, Zotero indexed text may answer a narrow question when coverage is sufficient and the limitation is explicit. Do not claim a complete paper interpretation from metadata, notes, annotations, or incomplete indexed text.
