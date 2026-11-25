---
name: data-pipeline
description: Build high-quality pretraining corpora from raw web/domain data with cleaning, dedup, filtering, and privacy safeguards.
---

# Data Pipeline (Pretraining-First)

Use this skill when the user needs dataset creation for **from-scratch LLM training**.
Default output is a reproducible corpus package ready for tokenizer training and pretraining.

## Scope

- Ingest raw text from web pages, documents, dumps, and domain sources.
- Extract clean text, normalize formatting, and preserve provenance metadata.
- Remove duplicates and near-duplicates before quality filtering.
- Filter noisy/low-value content and remove sensitive data.
- Balance domains to avoid over-representation in training data.

## Extraction

Preferred text extraction stack:

- `trafilatura` for robust web/article extraction.
- `resiliparse` for resilient HTML parsing and cleanup fallback.

Extraction requirements:

- Keep source URL / dataset id for each sample.
- Track extraction failures and retry queue separately.
- Store raw + cleaned snapshots when feasible for auditability.

## Deduplication

Use MinHash-based near-deduplication with `datasketch`:

- Exact dedup first (hash of normalized text).
- Near-dedup next (MinHash + LSH) to collapse paraphrased copies.
- Preserve one canonical copy per duplicate cluster.
- Report dedup ratio and retained sample counts by domain.

## Quality Filtering

Apply a FineWeb-Edu-style quality filter pipeline:

- Remove boilerplate, spam, machine-generated garbage, and template-heavy pages.
- Penalize low-information text (keyword stuffing, repetitive n-grams, nav clutter).
- Prefer coherent long-form educational or domain-relevant content.
- Keep configurable quality thresholds and log reasons for removals.

## PII and Safety

- Detect and remove likely PII (emails, phone numbers, government IDs, addresses where applicable).
- Redact or drop records containing sensitive personal information.
- Never include secrets/tokens from scraped configs, docs, or logs.
- Emit a PII-removal summary and residual-risk warning.

## Domain Balancing

Use balancing to avoid dataset collapse toward the largest source:

- Set target domain mix (for example: general, code, scientific, medical, legal).
- Downsample dominant domains; upsample scarce high-quality domains conservatively.
- Produce final domain histogram and token share per domain.

## Deliverables

Produce these artifacts:

1. Cleaned corpus shards (jsonl/parquet/txt).
2. `dataset_manifest.json` with source counts, dedup metrics, and filter stats.
3. `data_pipeline_report.md` with quality, PII, and domain-balance summaries.
4. Reproducible commands/configs used to generate the dataset.

## Dataset Versioning

Track dataset versions for reproducibility:

- Use **DVC** (Data Version Control) when project uses git, otherwise use manifest-based versioning.
- Support **git-lfs** for large artifact tracking when DVC is not available.
- Every pipeline run should produce a versioned `dataset_manifest.json` with:
  - corpus hash / content fingerprint
  - source file list with sizes and modification dates
  - pipeline config snapshot (filter thresholds, dedup settings)
  - parent version link for lineage tracking
- Tag versions with human-readable labels (e.g., `v1-raw`, `v2-deduped`, `v3-filtered`).
- Never overwrite previous versions — always create new version entries.

## Python Dependencies

Core dependencies for this skill:

- `trafilatura`
- `resiliparse`
- `datasketch`
- `pandas`
- `pyarrow`
- `regex`
- `ftfy`
- `langdetect`
