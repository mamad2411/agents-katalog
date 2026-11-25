---
name: rag-retrieval-audit
description: "Diagnose missing evidence in a RAG pipeline with labeled queries, chunk/trace inspection, Recall@K/MRR/nDCG, and stage-isolated failure taxonomy. Use when retrieval looks fine but answers fail, or when index/chunk/filter/rerank changes need before/after proof."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-09-11"
tags: ["ai-workflows", "evaluation", "rag", "retrieval", "recall", "mrr", "ndcg", "chunking", "hybrid-search"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# RAG Retrieval Audit AI Skill Guide (Claude)

## Overview & Engine Architecture

A RAG system fails in stages. Most “the model is wrong” tickets are **retrieval, indexing, chunking, filter, or context-assembly** failures that a stronger generator only hides with fluent guesses. This skill audits the **retriever path only**: did the answer-bearing evidence enter the final model context at the application’s real cutoff `K`?

Claude operates as a Principal RAG Reliability Engineer, specializing in **stage-isolated failure taxonomy**, **ID-based Recall@K / MRR / nDCG**, **chunk-boundary forensics**, **hybrid-search arm health**, and **ACL-safe relevance denominators**.

```
┌─────────────────────────────────────────────────────────────┐
│                 RAG Retrieval Audit Stack                   │
│                                                             │
│  Corpus governance                                          │
│  ├── Source docs → parse → chunk → embed → index revision   │
│  └── Metadata: ACL, tenant, version/hash, embedding_model   │
│                                                             │
│  Query path                                                 │
│  ├── Rewrite / expand → dense ± sparse (BM25) → fuse (RRF)  │
│  ├── Optional rerank → filters/thresholds → context pack    │
│  └── Generator (out of scope for retrieval metrics)         │
│                                                             │
│  Audit harness                                              │
│  ├── Labeled queries + eligible relevant chunk/doc IDs      │
│  ├── Per-query traces (retrieved IDs, ranks, scores, filters│
│  └── Metrics @ app K: hit-rate, Recall@K, Precision@K, MRR, │
│      nDCG; separate faithfulness later                      │
└─────────────────────────────────────────────────────────────┘
```

---

## When to use / when not to

**Use when**

- Answers are confident but wrong, and you need to know if evidence was missing vs ignored.
- You are changing chunk size, embeddings, hybrid weights, filters, or rerankers.
- Production has zero-result or “wrong doc family” clusters.
- Compliance requires proving which sources were eligible for a user.

**Do not use when**

- The task is pure prompt/style polish with a fixed golden context (use generation evals).
- You lack any labeled relevant IDs **and** refuse LLM-as-judge proxies (build labels first via `@ai-evaluation-dataset`).
- Someone asks to bypass ACLs so recall looks better — refuse; shrink the relevance denominator instead.

---

## Operational Capabilities & Agent Directives

1. **Freeze one baseline**: index revision, embedding model ID, chunker version, `K`, filters, fusion weights, reranker, and prompt context budget before any experiment.
2. **Label at chunk (or passage) IDs**, not vague “the handbook.” Prefer `source_id + content_hash + chunk_id`.
3. **Evaluate at the application’s real K** — the count of chunks that actually reach the generator after truncation, not an aspirational top-50.
4. **Separate stages**: ingestion miss ≠ parse fail ≠ chunk split ≠ ranking miss ≠ filter drop ≠ context truncate ≠ faithfulness drift.
5. **Never compare raw cosine/dot scores across embedding models** as if calibrated.
6. **Change one variable at a time**; keep a frozen baseline run for every PR.
7. **ACL hygiene**: documents the user cannot access are not “misses”; exclude them from the relevance denominator.

---

## Failure taxonomy (diagnose in this order)

| Stage | Symptom | Typical root cause |
| :--- | :--- | :--- |
| **Ingestion** | Relevant `source_id` absent from index | Sync lag, failed job, wrong collection, deleted tombstone |
| **Parse** | Doc present; answer text garbled/missing | PDF/table/OCR loss; HTML boilerplate; empty extracted body |
| **Chunk** | Answer split across boundaries; half-table rows | Fixed-token splits; tiny overlap; footer pollution in embeddings |
| **Embed/index** | Near-zero or nonsense scores; empty after migration | Wrong `embedding_model` on query vs corpus; metric mismatch |
| **Retrieve** | Relevant ID never in top-K (any arm) | Weak dense match on IDs/codes; BM25 arm dead; too-small `fetch_k` |
| **Fuse/threshold** | Hybrid “works” but lexical-only hits vanish | Similarity floor applied **after** RRF to fused list |
| **Filter/ACL** | Empty or wrong-tenant hits | Post-filter after ANN (`fetch_k` then filter) vs pre-filter; over-tight metadata |
| **Rerank/pack** | ID retrieved then dropped from final prompt | Reranker demotion; duplicate collapse; token budget truncation |
| **Generate** | Correct chunks in prompt; answer still wrong | Faithfulness — **not** a retrieval fix (track separately) |

Practitioner pattern (r/Rag): treat “RAG is inaccurate” as retrieval until proven otherwise; only then score faithfulness against the assembled context.

---

## Metrics — what each number means

Use **ID-based** metrics when gold chunk/doc IDs exist (preferred). Use Ragas-style **context recall / context precision** (claim attribution vs reference) when you only have reference answers.

| Metric | Question | Order-sensitive | Reach for it when |
| :--- | :--- | :--- | :--- |
| **Hit-rate@K** | ≥1 relevant ID in top K? | no | Cheap CI smoke |
| **Recall@K** | Fraction of gold IDs in top K | no | Missing evidence is costly |
| **Precision@K** | Fraction of top K that are relevant | no | Context budget is tight |
| **MRR** | Reciprocal rank of first relevant | yes | Generator mostly uses top 1–2 |
| **nDCG@K** | Graded ranking quality | yes | Reranker / graded labels |
| **Context recall** (Ragas) | Reference claims supportable from retrieved text | n/a | No gold chunk IDs yet |
| **Context precision** (Ragas) | Relevant chunks ranked early vs noise | yes | Noise displaces signal |

**Diagnostic pairs**

- Recall↓, MRR irrelevant → chunking / embedding / not in index.
- Recall steady, MRR↓ → ranking / missing reranker / fusion weights.
- Both OK, answers wrong → faithfulness or packing/truncation (log **final** prompt context).
- Recall↑ but MRR↓ after a change → more gold in the set but buried — generation often worsens.

Do **not** gate releases only on end-to-end answer accuracy; it masks 20–40% retrieval regressions when the model bluffs.

---

## Audit procedure

### 1. Inputs to collect (block if missing)

- Bounded query set (≥30 real user questions; synthetic-only sets are optional extras).
- Per query: eligible relevant chunk IDs **under the same ACL** as production.
- Index revision / collection name, embedding model, chunker config, `K`, filters, hybrid weights, reranker ID.
- Authorization to mutate only a **test** index unless prod change is approved.

### 2. Per-query trace schema (mandatory fields)

Log for every audited query:

```json
{
  "query_id": "q-1042",
  "query_text": "...",
  "user_acl": ["tenant:acme", "role:support"],
  "index_revision": "idx-2026-10-01T12:00Z",
  "embedding_model": "bge-m3",
  "k_final": 8,
  "query_rewrite": null,
  "filters_applied": {"tenant": "acme"},
  "arms": {
    "dense": [{"id": "c1", "rank": 1, "score": 0.71}],
    "bm25": [{"id": "c9", "rank": 1, "score": 12.4}]
  },
  "fused": [{"id": "c1", "rank": 1, "rrf": 0.032, "sources": ["dense"]}],
  "after_rerank": [{"id": "c9", "rank": 1, "score": 0.88}],
  "final_context_ids": ["c9", "c1", "c3"],
  "final_context_chars": 6120,
  "gold_ids": ["c9"],
  "notes": ""
}
```

Critical: log **`final_context_ids`** (what the model saw), not only first-stage retrieval. Truncation and rerank drops are common silent failures.

### 3. Score and classify

For each query, mark primary failure stage from the taxonomy. Aggregate:

- Mean Hit-rate@K, Recall@K, Precision@K, MRR, nDCG@K at **production K**.
- Slice by: zero-result, filter-excluded gold, BM25-only share of top-K, document family, language.

### 4. Single-variable experiments

Preserve baseline. Typical order of levers (stop when Recall@K and MRR meet gate):

1. Confirm gold sources are indexed and parsed (spot-open chunk text).
2. Fix chunk boundaries around tables/codes; add overlap; strip repeated footers.
3. Raise candidate pool (`fetch_k` / multi-arm top-N) **before** filters when the store post-filters.
4. Prefer **pre-filter** (or filtered ANN) over fetch-then-filter when tenants are sparse in the ANN shortlist ([LangChain FAISS filter ordering](https://github.com/langchain-ai/langchain/issues/28413)).
5. Hybrid: ensure BM25-only hits are not killed by a post-fusion vector similarity floor ([r/Rag hybrid bug reports](https://www.reddit.com/r/Rag/comments/1uvl9cx/)).
6. Add cross-encoder rerank after fusion when RRF alone is flat on homogeneous jargon.
7. Only then retune embeddings or rembed the corpus — with `embedding_model` stamped on every chunk.

### 5. Deliverable

Ship:

1. Per-query failure table (query_id, stage, gold_ids, final_context_ids, hit, ranks).
2. Aggregate metrics before/after with identical `K` and ACL rules.
3. Reproducible config dump (models, chunker, index revision, fusion, filters).
4. Explicit “not retrieval” bucket for faithfulness follow-ups.
5. ACL note: inaccessible gold excluded from denominators — **no bypass recommendations**.

---

## Production example: ID-based retrieval eval harness

```python
"""Minimal RAG retrieval audit: Recall@K, Precision@K, MRR, hit-rate."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence


@dataclass(frozen=True)
class Case:
    query_id: str
    query: str
    gold_ids: frozenset[str]  # eligible under the same ACL


def recall_at_k(retrieved: Sequence[str], gold: frozenset[str], k: int) -> float:
    if not gold:
        return float("nan")  # exclude ACL-empty cases from means
    top = list(retrieved)[:k]
    return len(gold.intersection(top)) / len(gold)


def precision_at_k(retrieved: Sequence[str], gold: frozenset[str], k: int) -> float:
    top = list(retrieved)[:k]
    if not top:
        return 0.0
    return len(gold.intersection(top)) / len(top)


def mrr(retrieved: Sequence[str], gold: frozenset[str], k: int) -> float:
    for i, doc_id in enumerate(list(retrieved)[:k], start=1):
        if doc_id in gold:
            return 1.0 / i
    return 0.0


def hit_rate(retrieved: Sequence[str], gold: frozenset[str], k: int) -> float:
    return 1.0 if gold.intersection(list(retrieved)[:k]) else 0.0


def audit(
    cases: Sequence[Case],
    retrieve_final_context_ids: Callable[[str], Sequence[str]],
    k: int,
) -> list[dict]:
    rows = []
    for case in cases:
        ids = list(retrieve_final_context_ids(case.query))
        rows.append(
            {
                "query_id": case.query_id,
                "hit": hit_rate(ids, case.gold_ids, k),
                "recall": recall_at_k(ids, case.gold_ids, k),
                "precision": precision_at_k(ids, case.gold_ids, k),
                "mrr": mrr(ids, case.gold_ids, k),
                "retrieved": ids[:k],
                "gold": sorted(case.gold_ids),
            }
        )
    return rows


# Wire retrieve_final_context_ids to YOUR packer (post-filter, post-rerank, post-truncate).
# Prefer LlamaIndex RetrieverEvaluator or Ragas IDBasedContextRecall when already in-stack:
# https://developers.llamaindex.ai/python/examples/evaluation/retrieval/retriever_eval/
# https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/
```

### Canary without a full golden set

Log `fusion_source` per top-K hit (`dense` | `bm25` | `both`). If BM25-only share flatlines after a deploy, hybrid may be silently vector-only.

---

## Technical troubleshooting matrix

| Failure signature | Root cause | Diagnostic & fix |
| :--- | :--- | :--- |
| Empty results for one tenant | ANN then metadata filter; `fetch_k` too small | Pre-filter or raise `fetch_k`; verify filter field cardinality |
| Exact error codes / SKUs missed | Dense-only retrieval | Add BM25/sparse arm; query rewrite that keeps literals |
| Hybrid no better than dense | Post-RRF similarity threshold drops BM25-only | Threshold on dense arm only; keep lexical survivors |
| High similarity, wrong answer | Chunk lacks full fact (boundary/table split) | Structural chunking; inspect gold span vs chunk text |
| Correct doc, wrong chunk | Boilerplate-dominated embeddings | Strip headers/footers; smaller semantic units |
| Scores ~0 but “good” answers | Distance/metric or embed-model mismatch | Pin same `embed_model` on index build and query |
| Recall OK, users still complain | Faithfulness / truncation of packed context | Diff `retrieved` vs `final_context_ids`; generation eval |
| Metric improved, UX worse | Recall↑ MRR↓ | Add reranker; report both metrics in CI |

---

## Best practices

1. Build the eval set from **real** support/search queries, not only synthetic FAQ paraphrases.
2. Version corpus + chunker + embedding model together; stamp `embedding_model` on chunks for gradual rembeds.
3. Deduplicate near-identical chunks before fusion to stop footer clones from crowding top-K.
4. Keep retrieval CI separate from answer faithfulness CI (`@ai-evaluation-dataset`, `@ai-citation-verification`).
5. For evidence-dense docs, prefer structural/hierarchical chunk checks; for sparse factoid QA, simple token/sentence baselines are often enough — measure, don’t assume.
6. Gate merges on Hit-rate@K + Recall@K + MRR with thresholds chosen from your baseline, not internet folklore.

---

## Limitations

- This skill does not certify production quality for every vector DB or framework version.
- LLM-judge context metrics are proxies; disagreement with ID-based labels should be investigated.
- Multimodal/table-heavy corpora need parser-specific audits beyond text metrics.
- Stop and ask if ACL rules, index write permission, or success thresholds are missing.

---

## Related skills

- `@ai-evaluation-dataset` — build/version labeled query sets and gold IDs
- `@llm-json-contract-check` — structured judge / scorer outputs
- `@prompt-regression-gate` — prompt/packer changes with frozen retrieval
- `@ai-citation-verification` — citation support against retrieved passages
- `@ai-pii-redaction-review` — redact traces before sharing eval dumps
- `@llm-cost-latency-benchmark` — cost/latency of rerank + larger K
- `@qdrant` / `@chromadb` / `@elasticsearch` — store-specific filter and hybrid knobs

---

## Agent Operational Directive

> **MANDATORY**: Audit retrieval with stage isolation and metrics at production `K`. Log final packed context IDs. Change one variable at a time against a frozen baseline. Never recommend ACL bypasses to inflate recall. Report retrieval metrics separately from answer quality, latency, and cost.

---

## Source anchors (research)

- [Ragas Context Recall](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/) / [Context Precision](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/)
- [LlamaIndex RetrieverEvaluator](https://developers.llamaindex.ai/python/examples/evaluation/retrieval/retriever_eval/)
- [LangChain FAISS filter-after-ANN empty results](https://github.com/langchain-ai/langchain/issues/28413)
- [LlamaIndex zero/near-zero scores / embed mismatch](https://github.com/run-llama/llama_index/issues/18890)
- r/Rag: retrieval-vs-generation split; chunk boundary failures; post-RRF threshold killing BM25
