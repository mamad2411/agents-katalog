---
name: ontology-guided-annotation
description: Use this skill whenever the user wants to build ontology-guided training data from an OWL/RDF/Turtle ontology plus source documents. It creates a human-reviewable ontology_profile.md, extracts text/OCR from PDFs, images, DOCX, HTML, or text, interactively annotates entities/classes/relations/properties for model training, audits labels against ontology constraints, visualizes review results in static HTML, and merges reviewed batches into JSONL datasets plus review.md. Use it for ontology-based information extraction, annotation dataset creation, entity/relation labeling, OWL-driven schema extraction, and workflows where human review is required before accepting labels.
---

# Ontology-Guided Annotation

This skill builds high-quality annotation data from an OWL ontology and heterogeneous source documents. The goal is not to directly populate RDF/OWL. The goal is to produce reviewed training data for traditional models such as BERT-style extractors or LLM fine-tuning.

The workflow is intentionally staged. Each stage has a separate role and a human review checkpoint where needed.

## Output Language

Use Chinese for generated prose, Markdown reports, review questions, and HTML dashboards by default. If the user explicitly asks for English output, use English and pass `--language en` to bundled scripts that support it.

Keep machine-readable JSON keys in English even when the surrounding report is Chinese, because downstream scripts depend on stable keys.

## Inputs

Accept these inputs when available:

- OWL ontology file, usually `.owl`, `.rdf`, or `.ttl`.
- Source documents: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.docx`, `.html`, `.txt`, or pasted text.
- Optional annotation policy from the user: target classes, relation types, negative examples, batch size, confidence threshold, and output format.

## PDF/OCR Integration

This skill is designed to be self-contained for classroom use. Students should be able to install only this skill and still process OWL files plus common source documents.

During development, local `pdf` and `ocr-document-processor` skills can be used as references for good PDF/OCR workflows when they are installed. Do not require those skills at runtime, and do not copy proprietary external skill files into this skill.

For actual use, prefer the bundled document reader:

```bash
python ontology-guided-annotation/scripts/extract_document.py <source-file> --output <output-dir>/document_profile.json
```

Keep this skill focused on ontology-guided annotation and training-data quality. Normalize every upstream extraction result into `document_profile.json`.

For detailed document ingestion rules, read `references/document_reader.md`.
For annotation batch rules, read `references/annotation_workflow.md`.
For audit and integration rules, read `references/audit_and_integration.md`.
For visualization rules, read `references/visualization.md`.

## Outputs

Prefer these outputs:

- `ontology_profile.md`: human-reviewable ontology summary.
- `document_profile.json`: extracted text blocks with source locations.
- `annotation_batch_*.jsonl`: accepted and pending annotation examples.
- `questions_for_user.md`: ambiguous cases that require user decisions.
- `audit_report.md`: ontology and label quality review.
- `review.md`: low-confidence items, conflicts, unresolved decisions, and next recommended batch.
- `review_dashboard.html`: static visual review page for summaries, annotations, pending decisions, and audit findings.
- `training_data/`: final reviewed exports for canonical extraction results, LLM fine-tuning, relation extraction, and NER/span conversion.

## Role 1: Ontology Reader

Use this role first when the user provides an OWL/RDF/Turtle ontology.

1. Parse the ontology. Extract classes, object properties, data properties, annotation properties, domain, range, labels, comments, superclass relations, restrictions, and named individuals.
2. Generate `ontology_profile.md`.
3. Stop and ask the user to review `ontology_profile.md` before annotation starts.
4. Ask the user to mark abstract classes, forbidden labels, preferred labels, synonyms, and any domain-specific rules missing from the ontology.

When the ontology is RDF/XML OWL, run:

```bash
python ontology-guided-annotation/scripts/build_ontology_profile.py <input.owl> --output <output-dir>/ontology_profile.md --language zh
```

Do not treat generated ontology profiles as final truth. OWL files often encode restrictions in ways that are syntactically correct but still need domain review for annotation.

## Role 2: Document Reader

Use this role after the ontology profile is reviewed or when the user asks to inspect source documents.

Extract content into stable text blocks. Preserve enough provenance for every future label:

- document path or URL
- page number or section
- image filename if OCR was used
- text span offsets when possible
- table cell coordinates when possible
- OCR confidence if available

Recommended tooling:

- Text PDFs: PyMuPDF or pdfplumber.
- Scanned PDFs/images: PaddleOCR, Tesseract, or a multimodal model when local OCR is weak.
- DOCX: python-docx or pandoc.
- HTML: BeautifulSoup or readability-style extraction.

If the input is PDF or OCR-heavy image material, use the bundled extractor first. Normalize all output into the block schema below even if another extraction tool returns Markdown, plain text, HTML, or tool-specific JSON.

For the bundled extractor, run:

```bash
python ontology-guided-annotation/scripts/extract_document.py <source-file> --output <output-dir>/document_profile.json
```

Use `--ocr-lang chi_sim+eng` or another installed Tesseract language code when OCRing multilingual material.

Create `document_profile.json` with a list of blocks:

```json
{
  "document_id": "menu-001",
  "blocks": [
    {
      "block_id": "p1-b3",
      "source": "menu.pdf",
      "page": 1,
      "text": "Example item A is made with material B and comes from place C.",
      "layout_type": "paragraph",
      "confidence": 0.98
    }
  ]
}
```

## Role 3: Interactive Annotator

Use this role to create training data in small batches. Do not attempt to label the whole corpus in one pass.

1. Select a small batch of document blocks.
2. Propose entity mentions, class labels, relations, and property labels using `ontology_profile.md`.
3. Attach evidence to every label: source block, span text, and rationale.
4. Mark uncertain items as `needs_user_review` instead of forcing a label.
5. Ask the user focused questions for ambiguous cases, with 2-4 concrete options and a short reason for each option.

Annotation examples should be JSONL-friendly:

```json
{
  "id": "ann-0001",
  "source": {"document_id": "menu-001", "block_id": "p1-b3"},
  "text": "Example item A is made with material B and comes from place C.",
  "entities": [
    {"id": "e1", "text": "Example item A", "class": "DomainItem", "start": 0, "end": 14, "confidence": 0.92},
    {"id": "e2", "text": "material B", "class": "Material", "start": 28, "end": 38, "confidence": 0.90}
  ],
  "relations": [
    {"subject": "e1", "predicate": "hasMaterial", "object": "e2", "confidence": 0.86}
  ],
  "status": "accepted"
}
```

For fine-tuning, include both positive and useful negative examples where the ontology could plausibly apply but should not.

For a stricter batching and user-question protocol, read `references/annotation_workflow.md`.

## Role 4: Quality Auditor

Use this role after each annotation batch.

Check:

- Every class exists in `ontology_profile.md`.
- Every relation/property exists in the ontology profile.
- Object property subject and object types match domain/range when domain/range is declared.
- Data property values match expected datatype when declared.
- Labels have evidence in the source block.
- Low-confidence labels are not silently accepted.
- Similar mentions are labeled consistently across the batch.

When the auditor finds ambiguity, ask the user rather than overwriting the annotation. Save findings to `audit_report.md`.

For audit severity levels and report format, read `references/audit_and_integration.md`.

For mechanical checks on JSONL batches, run:

```bash
python ontology-guided-annotation/scripts/validate_annotations.py <ontology_profile.md> <annotation_batch.jsonl> --output <output-dir>/audit_report.md --language zh
```

## Role 5: Data Integrator

Use this role only after user review and audit.

1. Merge accepted annotations into clean JSONL.
2. Keep pending and rejected examples in separate files.
3. Deduplicate repeated examples while preserving source provenance.
4. Export accepted annotations into training-friendly formats.
5. Generate `review.md` listing unresolved questions, low-confidence labels, conflicts, and recommended next batches.

Do not export RDF/OWL unless the user explicitly asks for it. The default target is training data.

For dataset split, accepted/pending/rejected files, and `review.md` conventions, read `references/audit_and_integration.md`.

After user review is complete, run:

```bash
python ontology-guided-annotation/scripts/export_training_data.py \
  --accepted <accepted.jsonl> \
  --output-dir <training_data_dir> \
  --language zh
```

This writes `canonical_accepted.jsonl`, `llm_finetune.jsonl`, `relation_extraction.jsonl`, `ner_spans.jsonl`, and a README. Pending review items are intentionally excluded until the user resolves them.

## Role 6: Result Visualizer

Use this role after annotation, audit, or integration creates JSONL/Markdown outputs that need easier review.

1. Generate a static HTML dashboard with summary counts, document blocks, accepted annotations, pending review items, rejected/negative examples, and audit findings.
2. Keep the design simple and academic: readable tables/cards, restrained colors, no decorative layout.
3. Include interactive controls for pending review items so the user can choose accept, modify, reject, or defer and add notes.
4. Let the user export `feedback.json` or copy a feedback prompt. The next annotation pass should consume this feedback and update pending items.
5. Treat the HTML page as a review layer. The canonical data remains JSONL plus Markdown reports. Do not use pending items for final training export until they are accepted.

Run:

```bash
python ontology-guided-annotation/scripts/visualize_results.py \
  --document-profile <document_profile.json> \
  --accepted <accepted.jsonl> \
  --pending <pending_review.jsonl> \
  --rejected <rejected_or_negative.jsonl> \
  --audit-report <audit_report.md> \
  --output <review_dashboard.html> \
  --language zh
```

For visualization details, read `references/visualization.md`.

## Human Review Policy

Human review is required after:

- `ontology_profile.md` generation.
- First annotation batch.
- Any batch with unresolved class/property ambiguity.
- Any audit report that finds constraint violations.

When asking the user, keep questions concrete. Prefer:

```text
In block p1-b3, should "spicy" be labeled as:
1. Spiciness/Hot
2. Domain-specific quality or attribute
3. no entity
```

Avoid asking broad questions like "Is this ontology correct?"

## Domain Neutrality

This skill is ontology-driven and should not assume a fixed domain. It should work for food, traditional culture, cultural heritage, biology, medicine, education, manufacturing, archives, or any other domain where the user provides an ontology and source documents.

Use examples only as examples. Always let the user's ontology profile determine the valid classes, properties, constraints, and annotation policy.
