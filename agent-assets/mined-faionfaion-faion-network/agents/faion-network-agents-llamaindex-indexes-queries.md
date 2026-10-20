# Llamaindex Indexes Queries

## Summary

**One-sentence:** Picks the right LlamaIndex index type (Vector/Keyword/KnowledgeGraph/Tree/Summary) and query-engine shape and emits an indexing-spec.

**One-paragraph:** LlamaIndex ships five index types optimised for different query shapes. Picking VectorStoreIndex when the workload is multi-hop reasoning over a graph wastes time and tokens. This methodology converts a workload profile (query types, data shape, hop depth) into the right index + query_engine + response_synthesizer combo.

**Ефективно для:** solopreneur whose simple RAG plateaued and now needs to pick the right index shape for the workload.

## Applies If (ALL must hold)

- Using LlamaIndex.
- Workload has multiple distinct query types or data shapes.
- Latency allows experimentation (you can A/B index types).
- Eval signal exists or can be built.
- Corpus shape known (graph-like, narrative, FAQ, summary-heavy).

## Skip If (ANY kills it)

- Simple Q&A on prose — VectorStoreIndex is correct.
- Pure SQL workload — use [[llamaindex-sql-query]].
- Conversational follow-ups — use [[llamaindex-chat-engine]].
- No eval signal — measure before picking.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `workload-profile.yaml` | query_types, data_shape, hop_depth_max, eval_set_size | author |
| `Sample corpus` | ≥100 docs | raw |
| `LLM creds` | for response synthesis | secret |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[llamaindex-basics]] | Index foundations. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for index types, query engines, response synthesizers, retrievers. | ~3250 |
| `content/02-output-contract.xml` | essential | indexing-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Wrong index for workload, sub-question explosion, no-rerank. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step selection procedure. | ~800 |
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
| `templates/workload-profile.yaml` | Input. |
| `templates/indexing-spec.md.j2` | Output. |
| `templates/indexing-spec.md` | Output. Generated from `templates/indexing-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/query_engine.py` | Working engine wiring. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llamaindex-indexes-queries.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[llamaindex-basics]]
- [[llamaindex-hybrid-retrieval]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on data_shape (graph → KnowledgeGraphIndex; tree-hierarchical → TreeIndex; flat-prose → VectorStoreIndex; FAQ-keyword → KeywordTableIndex), then on hop_depth (>1 → sub_question / multi_step query engine), then on response synthesizer. Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
