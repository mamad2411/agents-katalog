# Llamaindex Hybrid Retrieval

## Summary

**One-sentence:** Wires LlamaIndex hybrid retrieval (QueryFusionRetriever + cross-encoder rerank + AutoMerging) and emits a hybrid-retriever-spec.

**One-paragraph:** Vector-only retrieval misses keyword-exact hits; keyword-only misses paraphrases. Hybrid retrieval fuses both, then reranks. This methodology converts a retrieval profile (corpus heterogeneity, latency, rerank budget) into a deterministic hybrid-retriever-spec: which retrievers to fuse, k per retriever, rerank model, similarity threshold.

**Ефективно для:** solopreneur whose RAG misses obvious answers and needs the upgrade beyond vector-only.

## Applies If (ALL must hold)

- Vector-only baseline fails on a measurable subset (e.g., exact product codes).
- Latency budget allows ≥2 retrievers + rerank step.
- Corpus has both prose and structured/keyword-heavy chunks.
- Rerank model budget exists (or you can host a small cross-encoder).
- Labeled eval set or proxy metric is available.

## Skip If (ANY kills it)

- Vector-only already at target accuracy.
- Latency budget <500ms — hybrid adds 200-400ms.
- Corpus is homogeneous prose — vector-only is enough.
- No labeled set to measure improvement — you cannot prove hybrid is better.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `retrieval-profile.yaml` | corpus_heterogeneity, latency_target_ms, rerank_budget_usd, labeled_set_size | author |
| `Existing VectorStoreIndex` | as baseline | ingestion |
| `Cross-encoder model handle` | HF id or hosted endpoint | config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[llamaindex-basics]] | Index foundations. |
| [[llamaindex-indexes-queries]] | Retriever taxonomy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for QueryFusionRetriever, RRF, cross-encoder rerank, AutoMergingRetriever, threshold. | ~2000 |
| `content/02-output-contract.xml` | essential | hybrid-retriever-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Rerank-after-too-few, latency blow-up, threshold too tight, fusion fails on tiny corpus. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step wiring procedure. | ~800 |
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
| `templates/retrieval-profile.yaml` | Input. |
| `templates/hybrid-retriever-spec.md.j2` | Output. |
| `templates/hybrid-retriever-spec.md` | Output. Generated from `templates/hybrid-retriever-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/hybrid_retriever.py` | Working QueryFusion + rerank wiring. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llamaindex-hybrid-retrieval.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[llamaindex-basics]]
- [[llamaindex-indexes-queries]]
- [[llamaindex-production-gotchas]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on corpus_heterogeneity (mixed → vector+BM25 fusion; uniform-prose → vector-only with rerank), then on latency budget (<1s → smaller rerank model), then on rerank budget. Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
