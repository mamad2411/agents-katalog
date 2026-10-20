# Rerank Before Reasoning

## Summary

**One-sentence:** Produces a RAG-stage spec inserting a cross-encoder reranker between retrieval and the reasoning model so top-k matches what the model needs, not what the embedder thought was close.

**One-paragraph:** Embedding-based retrieval returns top-k by cosine similarity, which doesn't match what the LLM needs to reason. A cross-encoder reranker reads (query, candidate) pairs and produces a relevance score; the LLM sees k_final relevant candidates instead of k_retrieved noisy ones. Saves context tokens and improves answer quality.

**Ефективно для:** RAG product whose top-1 hit is often related-but-wrong; the right doc sits at position 6.

## Applies If (ALL must hold)

- RAG pipeline retrieves top-k > 5 candidates.
- Top-1 cosine miss rate > 20%.
- Context budget tight; can't pass all k to LLM.

## Skip If (ANY kills it)

- Embedding hits top-1 reliably.
- Latency-critical path (rerank adds 100-300ms).
- k_retrieved == 1.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `pipeline-stages.yaml` | {embed_model, k_retrieved, k_final, reranker_model} | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| none | Self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-rerank-required; r2-k-retrieved-bigger; r3-reranker-model-shipped; r4-monitor-mrr-improvement; r5-fallback-on-rerank-timeout. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec artefact. | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with detector + repair. | ~700 |
| `content/04-procedure.xml` | recommended | Step-by-step procedure. | ~600 |
| `content/05-examples.xml` | recommended | Worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision branches mapped to rule ids. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_input` | haiku | Mechanical. |
| `classify_drivers` | sonnet | Subjective tradeoffs. |
| `audit_output` | opus | Cross-cutting subtleties. |
| `emit_spec` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/rerank-before-reasoning-spec.md.j2` | Markdown wrapper for the JSON spec. |
| `templates/rerank-before-reasoning-spec.md` | Markdown wrapper for the JSON spec. Generated from `templates/rerank-before-reasoning-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-rerank-before-reasoning.py` | Validates spec against the schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Sibling methodologies in `geek/ai/ai-agents/`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Walks the drivers and picks a rule id per leaf. Each conclusion cites a rule in 01-core-rules.xml so the spec records the audit chain.
