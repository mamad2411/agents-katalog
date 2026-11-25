---
name: build-enhanced-epub
description: Build reproducible, validated EPUB 3 books from authorized PDF, HTML, text, or chapter-file sources, with offline story-map navigation by arc, reading intent, character, location, faction, concept, and event. Use when Codex must ingest or normalize a long-form book, create a personal offline EPUB, recover chapter structure, add spoiler-friendly semantic indexes, build an Apple Books-compatible reading artifact, or audit and repair an existing enhanced-EPUB pipeline.
---

# Build Enhanced EPUB

Create the book as a reproducible data pipeline, not a one-off scrape. Keep source
content, normalized chapters, editorial indexes, EPUB generation, and QA separate.

## Apply the rights gate

Before downloading or copying substantial source content, establish that the user
owns it, has permission, or is making a lawful personal copy. Require an explicit
acknowledgement in automated download commands. Do not bypass DRM, authentication,
paywalls, access controls, or technical restrictions. Do not publish source content.

Keep downloaded books and chapter corpora out of shared skill repositories. Record
source attribution and personal-use rights in EPUB metadata.

## Choose the workflow

1. Inspect the source and determine PDF text, scanned PDF/OCR, HTML chapters, plain
   text, or existing structured files.
2. Read [references/source-ingestion.md](references/source-ingestion.md) for the
   selected source type.
3. Normalize the result according to
   [references/data-contracts.md](references/data-contracts.md).
4. Audit the complete corpus before narrative analysis.
5. If semantic navigation is requested, read
   [references/editorial-indexing.md](references/editorial-indexing.md).
6. Build EPUB structure according to
   [references/epub3-layout.md](references/epub3-layout.md).
7. Run every relevant check in
   [references/qa-checklist.md](references/qa-checklist.md).

For a large book and user-requested parallel work, read
[references/collaboration.md](references/collaboration.md). Keep one orchestrator as
the only writer of canonical IDs and merged indexes.

## Establish the project contract

Confirm or infer safely:

- title, author, language, source URL/file, and intended output name;
- user's rights acknowledgement and personal/shared distribution boundary;
- expected chapter count when the source exposes one;
- whether spoilers are allowed;
- whether the user wants plain EPUB or enhanced semantic navigation.

Create separate directories for `library/`, `analysis/`, `index/`, `src/`, `tests/`,
`dist/`, and `docs/`. Cache the original source and extraction output so rebuilds do
not repeatedly hit a website.

## Ingest and normalize

Preserve a stable `order` independent from source chapter IDs. Store one UTF-8 JSON
file per chapter, zero-padded by reading order. Keep paragraph boundaries rather
than flattening the chapter into one string.

Repair structural source defects only when evidence is clear. Record every repair
in metadata or QA notes. Never silently rewrite prose.

Reject the corpus if chapter order is duplicated, discontinuous, unexpectedly
short, empty, or polluted by table-of-contents/header/footer text. Run:

```bash
python3 scripts/audit_library.py /path/to/library
```

## Build evidence before interpretation

Generate a corpus manifest, searchable JSONL, checksums, candidate proper nouns, and
an explicit concordance for likely names. Use machine extraction only to locate
evidence; do not promote candidates to canonical entities without editorial review.

Inspect chapter text around every proposed arc boundary. Do not infer the story map
from titles alone. Make summaries spoiler-aware or spoiler-complete according to the
project contract.

## Create the semantic layer

Maintain four canonical documents: `arcs.json`, `entities.json`, `events.json`, and
`intents.json`. Give every record a stable lowercase ASCII slug. Resolve aliases and
renames before emitting cross-references.

For long novels, target readable high-level stages rather than tiny plot beats. A
novel over 400 chapters commonly needs 25–45 arcs and 75–150 reading intents. Scale
down for shorter works. Every chapter must belong to an arc, and every destination
must explain why the reader should jump there.

Validate the index before building:

```bash
python3 scripts/validate_index.py /path/to/index /path/to/library
```

## Build EPUB 3

Include cover, metadata, stylesheet, EPUB 3 navigation, NCX fallback, reading spine,
and chapter XHTML. For enhanced books add these offline guide pages before chapters:

- Start here
- Story map
- I want to reread…
- Characters
- Locations
- Factions and concepts
- Events

Link guide records directly to chapter XHTML and link related records to one another.
Do not use JavaScript or network dependencies in guide pages. Keep full chapter TOC
nested behind a parent entry so the high-level map remains scannable in Apple Books.

## Validate and deliver

Build atomically to a temporary file, then replace the final EPUB. Run:

```bash
python3 scripts/validate_epub.py /path/to/book.epub
```

Also run EPUBCheck when Java and EPUBCheck are available. Test the target reader when
possible. Report corpus counts, index counts, test results, file size, checksum,
known source repairs, and any validation tool that could not run.

Deliver the EPUB plus the reproducible project and QA report. Give short import
instructions for the user's reader. Treat Apple Books or another EPUB reader as the
offline app unless the user explicitly asks for a separate native application.
