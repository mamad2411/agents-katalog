# Llamaindex Basics

## Summary

**One-sentence:** Bootstraps a LlamaIndex VectorStoreIndex from documents and emits a minimum-viable index-spec decision-record.

**One-paragraph:** LlamaIndex hides production traps behind a 10-line quickstart: default chunk size, default embedder, in-memory store. This methodology converts a corpus profile (size, doc shape, query pattern) into a real index-spec: loader, node parser, embedding model, vectorstore, persistence config.

**Ефективно для:** solopreneur taking a LlamaIndex prototype from notebook to first production deploy.

## Applies If (ALL must hold)

- Using LlamaIndex (not LangChain).
- Corpus has ≥10 documents and ≤10M tokens.
- ≥1 vectorstore available.
- You can persist to disk or a hosted vector DB.
- Query pattern is known (factual / summarization / exploratory).

## Skip If (ANY kills it)

- Notebook prototype with <10 docs — defaults are fine.
- Need agent reasoning — use [[llamaindex-agents-eval]].
- Hybrid retrieval needed — use [[llamaindex-hybrid-retrieval]].
- SQL data — use [[llamaindex-sql-query]].

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `corpus-profile.yaml` | doc_count, avg_doc_chars, query_pattern, persistence_target | author |
| `Document folder/URL` | input docs | raw corpus |
| `OPENAI_API_KEY or equivalent` | embedding model creds | secret |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for index types, node parser, embedding model, persistence. | ~2400 |
| `content/02-output-contract.xml` | essential | index-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | In-mem default in prod, wrong chunk size, no metadata extractor. | ~700 |
| `content/04-procedure.xml` | recommended | 5-step bootstrap procedure. | ~800 |
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
| `templates/index-spec.md.j2` | Output. |
| `templates/index-spec.md` | Output. Generated from `templates/index-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/build_index.py` | Working VectorStoreIndex builder. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llamaindex-basics.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[llamaindex-ingestion-pipeline]]
- [[llamaindex-indexes-queries]]
- [[llamaindex-chat-engine]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on persistence_target (in-mem dev, chroma local, pinecone prod), then on query_pattern (factual → small chunks, summarization → larger chunks), then on doc count. Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
