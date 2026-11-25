---
name: document-chunker
description: "Use this skill when the task involves processing large files or document sets with Codex as the AI coworker: document ingestion, file inventory, parsing, chunking, structured extraction, embeddings preparation, retrieval QA, SEC/Form D processing, HypeStake knowledge ingestion, or auditing .chunks.jsonl outputs. All AI interpretation must be performed by Codex, not by bundled scripts."
---

# Document Chunker

This skill turns Codex into an advanced document-processing coworker.

The key rule: **all AI processing happens inside Codex**. Helper scripts are deterministic utilities for reading files, creating inventories, converting simple formats to text, slicing large text into stable packets, merging Codex-produced JSON, auditing artifacts, and running lexical retrieval canaries. They must not call LLM, embedding, rerank, OCR, or search APIs unless the user explicitly asks and the host repo already provides an approved path.

## Use this skill for

- Very large files that cannot be pasted into chat.
- Folders of PDFs, DOCX, Markdown, CSV, JSON, JSONL, XML, HTML, text, SEC filings, pitch decks, reports, transcripts, or scraped pages.
- HypeStake `ai-knowledge`, reference documents, Company Analysis, Portfolio Analysis, market intel, deal/finance/valuation, creator genome, and RAG artifacts.
- Existing `.chunks.jsonl`, embedding-input, vector payload, or retrieval output audits.
- Designing or implementing a document-processing pipeline where Codex runs local scripts during the conversation.

Do not use this skill for ordinary code edits that do not touch document processing or RAG.

## Core operating posture

1. **Codex is the AI processor.** Use Codex's reasoning, chat context, file access, subagents, and local command execution. Scripts only prepare, slice, validate, merge, and audit.
2. **Never paste huge files blindly.** First inventory, classify, convert, and slice. Work from stable packets with file paths, byte/line/char ranges, hashes, and task instructions.
3. **Parse deterministically before AI interpretation.** Use structure, headings, XML tags, tables, pages, rows, and schemas before asking Codex to summarize or infer.
4. **Exact facts are structured records.** IDs, dates, money, exemptions, investor counts, CIKs, jurisdictions, legal terms, route names, function names, table names, and model IDs must be captured as typed facts with source locators.
5. **Embeddings happen after final chunk boundaries.** This skill prepares `embedding_inputs.jsonl`; it does not require embeddings to decide primary chunking boundaries for structured documents.
6. **Separate display, retrieval, and exact facts.** Keep `display_text` for citations, `retrieval_text` for search, and `structured_facts` for exact queries.
7. **Parent-child chunks are the default.** Parent chunks support broad semantic retrieval; atomic chunks support precise evidence and citations.
8. **Quality gates come before indexing.** Quarantine or flag local path leakage, missing source locators, tiny contextless chunks, section mismatch, contradictory values, schema drift, and unsupported claims.
9. **Generated summaries do not outrank source records.** This is especially important for HypeStake finance, deal, ownership, compliance, and valuation surfaces.

## Default cowork workflow

When the user gives files/folders, execute this sequence unless the repo already has a stronger process.

### Phase 0 — Run brief

Create a run brief before scripts:

```text
Run goal:
Input paths:
Output path:
Document classes expected:
High-trust domains involved:
Schemas to produce:
AI work will be done by Codex:
Scripts may do only deterministic processing:
Approval gates:
Done means:
```

### Phase 1 — Inventory

Use Python to inspect the filesystem without loading everything into context:

```bash
python scripts/python/doc_cowork.py inventory --input <input> --out <out>/00_inventory
```

Read the resulting `inventory.md`, `file_inventory.csv`, and `file_inventory.json`. Classify files by size, type, likely parser, risk, and processing order.

### Phase 2 — Convert simple files to text

```bash
python scripts/python/doc_cowork.py to-text --input <input> --out <out>/01_text
```

This handles text-like files, JSON/JSONL, CSV, XML, HTML cleanup, and DOCX text extraction using Python stdlib. For PDFs and image-heavy files, use project-approved tools if available, or ask the user for converted text/Markdown when the environment cannot convert safely.

### Phase 3 — Slice into stable Codex packets

```bash
python scripts/python/doc_cowork.py slice --input <out>/01_text --out <out>/02_slices --target-chars 12000 --overlap-chars 600
python scripts/python/doc_cowork.py packets --slices <out>/02_slices/slices.jsonl --out <out>/03_packets --packet-size 4 --profile general_rag
```

Packet files are Markdown work orders for Codex. Each packet includes source paths, ranges, hashes, and strict output schema.

### Phase 4 — Codex AI packet processing

Codex reads packet Markdown files and writes JSON results to `<out>/04_ai_results/`.

For small jobs, the main Codex agent can process packets sequentially.

For large jobs, ask Codex to spawn subagents or use CSV fan-out if available. Use the project-scoped agent templates in `templates/project-codex/.codex/agents/` when you want dedicated document agents.

Each packet result must be valid JSON matching the schema in `references/output-schemas.md`.

### Phase 5 — Merge Codex outputs

```bash
python scripts/python/doc_cowork.py merge-ai --input <out>/04_ai_results --out <out>/05_merged
```

This script validates that JSON can be parsed, deduplicates stable IDs, emits `structured_facts.jsonl`, `parent_chunks.jsonl`, `atomic_chunks.jsonl`, `embedding_inputs.jsonl`, and a merge report. If JSON is malformed, Codex fixes the exact offending packet result.

### Phase 6 — Audit and canary retrieval

```bash
python scripts/python/doc_cowork.py audit-jsonl --input <out>/05_merged --out <out>/06_audit
python scripts/python/doc_cowork.py canary --chunks <out>/05_merged --queries <queries.json> --out <out>/07_canary
```

Canaries should include known exact questions and known semantic questions. A run is not healthy until the right parent and child chunks are retrieved.

### Phase 7 — Final handoff

The final handoff must include:

- What was processed.
- What was skipped and why.
- Artifacts produced.
- Blocking issues.
- Quality warnings.
- Retrieval eval result.
- Suggested repo integration path.
- Exact commands run.
- Any files that need human review.

## Script commands

All paths below are relative to the installed skill folder.

```bash
# Inspect files and produce inventory JSON/CSV/Markdown.
python scripts/python/doc_cowork.py inventory --input ./incoming --out ./out/00_inventory

# Convert supported text-like files to normalized .txt records.
python scripts/python/doc_cowork.py to-text --input ./incoming --out ./out/01_text

# Slice converted text into stable windows.
python scripts/python/doc_cowork.py slice --input ./out/01_text --out ./out/02_slices --target-chars 12000 --overlap-chars 600

# Generate Markdown packet work orders for Codex.
python scripts/python/doc_cowork.py packets --slices ./out/02_slices/slices.jsonl --out ./out/03_packets --packet-size 4 --profile sec_form_d

# Merge Codex-produced packet JSON files.
python scripts/python/doc_cowork.py merge-ai --input ./out/04_ai_results --out ./out/05_merged

# Audit chunks and JSONL artifacts.
python scripts/python/doc_cowork.py audit-jsonl --input ./out/05_merged --out ./out/06_audit

# Run lexical canary retrieval.
python scripts/python/doc_cowork.py canary --chunks ./out/05_merged --queries ./examples/form-d-canaries.json --out ./out/07_canary

# Redact obvious secrets/PII before packetization when needed.
python scripts/python/doc_cowork.py redact --input ./incoming --out ./out/redacted
```

## When files are too large for Codex context

Do not ask Codex to read the full file at once. Use this loop:

1. Inventory.
2. Convert to text or identify unsupported conversion.
3. Slice to packets.
4. Process packet summaries/facts one packet at a time.
5. Merge packet outputs.
6. Ask Codex to process only the merged intermediate artifacts for cross-document synthesis.
7. Re-open specific source slices only when evidence is missing or conflicting.

Use hash/range locators to keep source traceability:

```json
{
  "source_path": "...",
  "char_start": 12000,
  "char_end": 24000,
  "sha256_16": "a1b2c3d4e5f6...",
  "source_locator": "file#char=12000-24000"
}
```

## Output artifact contract

Produce these artifacts where possible:

```text
manifest.json
run_report.md
documents.jsonl
structured_facts.jsonl
parent_chunks.jsonl
atomic_chunks.jsonl
embedding_inputs.jsonl
quality_report.json
retrieval_canary_report.json
human_review_queue.jsonl
```

### Document record

```json
{
  "document_id": "doc_...",
  "source_path": "...",
  "source_uri": "...",
  "source_type": "sec_form_d_xml|pdf_text|docx_text|markdown|csv|json|html|unknown",
  "title": "...",
  "document_date": "YYYY-MM-DD|null",
  "source_hash": "sha256...",
  "canonical_metadata": {},
  "debug_metadata": {}
}
```

### Structured fact

```json
{
  "fact_id": "fact_...",
  "document_id": "doc_...",
  "fact_type": "sec_form_d.sales_amount|company_metric|legal_term|route_inventory|custom",
  "name": "amount_sold",
  "raw_value": "$230,958",
  "normalized_value": 230958,
  "unit": "USD",
  "source_locator": {
    "source_path": "...",
    "section": "Offering sales amounts",
    "char_start": 123,
    "char_end": 456
  },
  "confidence": "high|medium|low",
  "needs_review": false
}
```

### Parent chunk

```json
{
  "chunk_id": "chunk_parent_...",
  "document_id": "doc_...",
  "chunk_type": "parent_summary",
  "display_text": "...",
  "retrieval_text": "...",
  "child_chunk_ids": [],
  "canonical_metadata": {},
  "quality_flags": []
}
```

### Atomic chunk

```json
{
  "chunk_id": "chunk_atomic_...",
  "document_id": "doc_...",
  "parent_chunk_id": "chunk_parent_...",
  "chunk_type": "atomic_section|atomic_table|atomic_text",
  "section": "...",
  "sections": ["..."] ,
  "heading_path": ["..."],
  "display_text": "...",
  "retrieval_text": "...",
  "source_locator": {},
  "canonical_metadata": {},
  "quality_flags": []
}
```

### Embedding input

```json
{
  "embedding_input_id": "embin_...",
  "chunk_id": "chunk_...",
  "document_id": "doc_...",
  "embedding_text": "Document: ...\nSection: ...\nFacts: ...",
  "embedding_text_hash": "sha256...",
  "embedding_profile": {
    "intended_model": "cohere.embed-v4:0|local-bge|repo-default",
    "dimensions": null,
    "created_by": "codex-document-chunker"
  },
  "metadata_minimal": {}
}
```

## SEC / Form D playbook

For SEC Form D / Form D/A:

- Use XML/tag/field structure first.
- Extract issuer identity, related persons, offering data, security types, sales amounts, investor counts, sales compensation, use of proceeds, and signatures.
- Normalize `06b` to `Rule 506(b)` and `3C.1` to `Section 3(c)(1)` while preserving raw source values.
- Split `Use of proceeds` and `Signature` unless the source truly binds them together. If combined, use `sections: ["USE_OF_PROCEEDS", "SIGNATURE"]`.
- Flag contradictions such as `has_non_accredited_investors = Yes` with count `0`.
- Do not answer exact questions from embeddings. Exact money/dates/IDs must be facts.

## HypeStake mode

Activate this mode when the repo/files are HypeStake-related.

- Preserve canonical vocabulary: Creator, Brand, Creator Hub, Brand Hub, Offer, Deal Proposal, Offering, Deal, Stake, Shadow Cap Table, Trigger.dev Job, Edge Function.
- Remember route boundaries: Creator Hub uses `/creator/*`; Brand Hub uses `/company/*`; older `/finance`, `/influencer/*`, and `/startup/*` paths are often legacy/compatibility unless live code proves otherwise.
- Treat Supabase Postgres/RLS operational records as the source of truth. AI artifacts, chunks, embeddings, Mongo archives, and summaries support reasoning but do not outrank operational records.
- For high-trust finance/deal/ownership/compliance/valuation areas, follow: authoritative records → deterministic calculation → retrieved governed context/evidence → AI narrative/recommendation → validation/policy/caveat layer → persisted inspectable artifact → UI states.
- For Company Analysis and Portfolio Analysis, preserve validation gates, source grounding, cache reuse, blocked metric behavior, confidence reporting, and no-investment-advice posture.
- For Creator Genome, preserve four-type support when relevant: music, influencer, streamer, athlete.
- Do not invent Edge Function names, Trigger task IDs, table names, route names, or model IDs. Discover them from source.
- Generated ingestion artifacts should be suitable for `ai-knowledge`, `reference_documents`, `ai_outputs`, `ai_output_chunks`, or the host repo's existing ingestion path only after schema verification.

## Quality gates

Block or quarantine artifacts with:

- Missing `document_id`, `chunk_id`, `source_path`, or `source_locator`.
- Local machine paths in user-facing fields.
- Section/heading mismatch.
- Mixed sections represented as a single section.
- Tiny contextless chunks under ~80 tokens unless they are attached to a parent chunk.
- Exact facts only present in prose, not structured facts.
- Contradictory fields without warning flags.
- `retrieval_text` identical to contextless display tables.
- No parent chunks.
- No source hash.
- Unvalidated AI JSON.
- User-facing claims without evidence.

Warn on:

- Unsupported PDFs/images.
- OCR needed but unavailable.
- Large tables flattened into unreadable prose.
- Source freshness unknown.
- Duplicate documents/chunks.
- High-stakes finance/legal/compliance content needing human review.

## Final response shape

For a completed run, respond with:

```text
Done: [what was produced]
Inputs processed: [counts]
Artifacts: [paths]
Quality result: [pass/warn/fail]
Important warnings: [top issues]
Commands run: [exact commands]
Next best step: [one concrete step]
```

If the run cannot complete, say exactly what failed, what evidence was collected, and the next command/prompt to continue.


