---
name: docling-pdf-ingest
description: >
  Ingest PDFs with IBM Docling (or similar) into structured documents for RAG/ETL: conversion
  pipelines, OCR options, table extraction, chunking handoff, quality checks, and PII-safe
  storage. Use when Docling PDF, document conversion to markdown/json, PDF ETL for owned
  corpora, or preparing enterprise PDFs for search/LLM — not for bypassing paywalls or
  processing data without authorization.
---

# Docling PDF Ingest

## Scope And Authorization

- **In scope:** Document corpora you own or are licensed/authorized to process.
- **Out of scope:** Scraping copyrighted PDFs without rights; feeding customer PDFs into public LLMs against policy.
- Prefer on-prem/VPC Docling pipelines for sensitive docs; redact PII in logs.
- Pair with `deepeval-llm-tests` for RAG quality, `secrets-management-hygiene`, and `code-quality-standards`.

## When To Use

- Building PDF → markdown/JSON pipelines for RAG or search.
- Evaluating Docling for tables, layout, and scanned OCR quality.
- Batch ETL of technical manuals, policies, or tickets-as-PDF.
- Normalizing mixed scanned/digital PDFs before chunking.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| RAG answer quality eval | `deepeval-llm-tests` |
| General LLM security | `ai-ml-security` / `llm-prompt-injection` |
| Object storage security | cloud storage skills |
| Zip/PDF path safety | `zip-slip-path-safety` if unpacking archives |
| Code quality baseline | `code-quality-standards` |

## Pipeline overview

```text
PDF (object store) → Docling convert → structured doc (md/json) →
  clean/normalize → chunk → embed/index → retrieve
```

| Concern | Notes |
| --- | --- |
| Digital PDF | Text extract preferred; faster |
| Scanned | OCR path; quality variance |
| Tables | Structure preservation critical for RAG |
| Images | Optional captioning; storage cost |
| Metadata | Source path, page, hash, version |

## Workflow

### 1. Confirm scope and success criteria

1. Corpus sensitivity, language, volume, SLA, target format (md/json).
2. Success: conversion success rate; table fidelity sample; PII policy met; reproducible job IDs.
3. License of Docling/models and OCR engines reviewed.

### 2. Inventory corpus

```bash
# Owned dataset layout
find /data/pdfs -name '*.pdf' | wc -l
# Sample problematic: scans, huge, encrypted, forms
```

1. Flag password-protected PDFs—handle keys via secret store, not code.
2. Record max pages/size limits for DoS protection.

### 3. Install and convert (illustrative)

```bash
pip install docling
# CLI patterns evolve — check current Docling docs for exact commands
```

```python
# Illustrative API sketch — verify against installed Docling version
from pathlib import Path
# from docling.document_converter import DocumentConverter
# converter = DocumentConverter()
# result = converter.convert(Path("sample.pdf"))
# result.document.export_to_markdown()
```

1. Pin Docling and model versions for reproducibility.
2. Run on sample set first (digital + scan + table-heavy).

### 4. Quality gates

| Check | Method |
| --- | --- |
| Empty extract | Fail job; quarantine PDF |
| OCR garbage | Language detect / confidence thresholds |
| Table sample | Human review checklist |
| Page coverage | Pages in ≈ pages out |
| Encoding | UTF-8 normalize |

1. Store side-by-side samples for regression when upgrading Docling.
2. Do not auto-delete source PDFs until QA passes.

### 5. Security and privacy

1. Virus/malware scan uploads if from users.
2. Limit zip bombs if batch archives (`zip-slip-path-safety`).
3. Strip or encrypt stored extracts per data class.
4. Prompt-injection: PDFs may contain adversarial text for RAG—treat retrieved text as untrusted (`llm-prompt-injection`).
5. No secrets in converted markdown committed to git.

### 6. Handoff to chunk/index

1. Preserve page anchors and headings for citations.
2. Chunk by structure (headings) not only fixed tokens when possible.
3. Embed pipeline versions in metadata for reindex.

### 7. Operate

```bash
# Batch job metrics
# - convert_success_rate
# - p95_convert_seconds
# - quarantine_count
```

1. Scale workers; GPU if OCR models need.
2. Idempotent jobs keyed by content hash.
3. Apply `code-quality-standards` to ETL code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| AuthZ | Licensed corpus | Random web PDF dump |
| Versions | Pinned Docling | Floating latest mid-prod |
| QA | Sample scorecards | Assume perfect extract |
| RAG | Cite page metadata | Unsourced chunks |
| Security | Scan + PII policy | User PDF → public LLM |
| Ops | Hash idempotent jobs | Overwrite without audit |

## Output Checklist

- [ ] Authorization and data class documented
- [ ] Sample conversion quality accepted
- [ ] Pipeline pinned versions
- [ ] Quarantine path for failures
- [ ] PII/malware controls applied
- [ ] Metadata (page, source, hash) preserved
- [ ] Chunk/index handoff defined
- [ ] Metrics and alerts for convert failures
- [ ] Reindex strategy on model upgrade
- [ ] `code-quality-standards` applied

## Rules

- Only authorized documents; respect copyright and privacy.
- Treat extracted text as untrusted in LLM contexts.
- Preserve provenance for every chunk.
- Verify APIs against current Docling release—APIs evolve.
- Focus on PDF ingest quality and safe ETL.
