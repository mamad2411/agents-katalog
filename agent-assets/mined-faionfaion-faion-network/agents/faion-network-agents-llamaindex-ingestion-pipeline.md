# Llamaindex Ingestion Pipeline

## Summary

**One-sentence:** Designs a LlamaIndex IngestionPipeline (loaders + metadata extractors + node parsers + vector store persistence) and emits an ingestion-spec.

**One-paragraph:** Ad-hoc ingestion scripts re-embed on every restart and skip metadata. IngestionPipeline solves this by chaining loaders, metadata extractors (TitleExtractor, SummaryExtractor), node parsers, and a persistent vector store. This methodology converts a corpus profile into a deterministic ingestion-spec.

**Ефективно для:** solopreneur whose ingestion is a notebook one-liner and now needs to scale to thousands of docs without re-embedding.

## Applies If (ALL must hold)

- Using LlamaIndex.
- Corpus updates ≥1× per week.
- Embedding cost matters (≥$10/build).
- ≥1 persistent vector store available.
- Documents need metadata (title/summary/source) for retrieval filtering.

## Skip If (ANY kills it)

- One-off prototype with <100 docs.
- Corpus never changes.
- Custom non-LlamaIndex pipeline.
- Metadata isn't useful for retrieval (rare).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `corpus-profile.yaml` | doc_count, update_frequency, embedding_budget_usd, metadata_needs | author |
| `Vector store endpoint` | Chroma/Pinecone URL | infra |
| `LLM + embedder creds` | secret | config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[llamaindex-basics]] | Index foundations. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for IngestionPipeline composition, splitter choice, vector-store persistence. | ~1250 |
| `content/02-output-contract.xml` | essential | ingestion-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Re-embed on restart, missing dedup, splitter mismatch. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step pipeline procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/corpus-profile.yaml` | Input. |
| `templates/ingestion-spec.md.j2` | Output. |
| `templates/ingestion-spec.md` | Output. Generated from `templates/ingestion-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pipeline.py` | Working IngestionPipeline. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llamaindex-ingestion-pipeline.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[llamaindex-basics]]
- [[llamaindex-indexes-queries]]
- [[llamaindex-production-gotchas]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on update_frequency (high → docstore dedup required), then on embedding_budget (low → SentenceSplitter; high → SemanticSplitterNodeParser), then on metadata needs. Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
