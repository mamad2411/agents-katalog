---
name: okf-wiki-capture
description: Capture immutable inputs for an OKF Wiki. Use when adding a PDF, office document, web clipping, video transcript, existing Markdown note, or AI-assisted session conclusion to a vault's sources/ directory before ingestion.
---

# Capture sources

Read `wiki/governance/` before acting. Capture changes `sources/` only; never
create or update wiki concepts.

## Workflow

1. Classify the input as `original`, `capture`, `transcript`, or
   `knowledge-note`.
2. Preserve the original when one exists. Store it in `sources/originals/`.
3. Use MarkItDown only when conversion to Markdown adds value. Run
   `markitdown <input> -o <output.md>`, place the result in `sources/captures/`,
   and do not replace the original.
4. Record the converter version, exact command and output path in the source
   manifest. Compare the result with the original for page or section coverage,
   tables, images and attachments. For scanned material, enable OCR when
   available and flag any uncertain extraction; never claim completeness without
   this review.
5. For a web source, preserve the Markdown snapshot, canonical URL and capture
   date. A live URL alone is insufficient.
6. For an AI-assisted conclusion, store context, references, open questions,
   confidence and `origin: ai-assisted`. Do not present it as primary evidence.
7. Record source metadata in a sibling manifest or Markdown frontmatter:
   `origin`, `source_kind`, `sensitivity`, `created`, and source URL or path.
8. Once captured, do not modify the source. Add an erratum or revised conversion
   as a new linked source instead.

## Boundaries

- Respect the vault's sensitivity and provider policy before processing content.
- Do not ingest automatically. Tell the user what was captured and wait for an
  explicit ingest request.
- Do not preserve full AI chat transcripts unless the user explicitly requests
  it.

Read `references/source-metadata.md` when choosing metadata or handling an
AI-assisted session.
