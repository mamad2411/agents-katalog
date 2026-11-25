---
name: embedding-model-choice
description: >
  Choose embedding models and dimensions for owned RAG/search: quality vs cost
  vs latency, multilingual needs, open vs API models, dimension/MRL tradeoffs,
  and migration cost. Use when selecting sentence-transformers, OpenAI/voyage/
  cohere embeddings, or dim reduction for vector DBs—not drift ops alone.
---

# Embedding Model Choice

## Scope And Authorization

- **In scope:** Model selection for applications and data you are allowed to process.
- **Out of scope:** Sending regulated data to third-party embed APIs without DPA/approval.
- Benchmark on **your** data; public MTEB ranks are a starting point only.
- Track license (Apache/MIT vs restrictive) for on-prem models.
- Pair with `embedding-drift-monitoring` before/after cutover.

## When To Use

- Greenfield vector search / RAG embedding selection.
- Replacing an embedding API for cost, privacy, or quality.
- Choosing dimensions (e.g. 384 vs 768 vs 1536) and storage cost.
- Multilingual or domain-specific (legal/code) requirements.
- Planning migration that requires full re-embed.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Ongoing drift / recall monitoring | `embedding-drift-monitoring` |
| Prompt injection on LLM layer | `llm-prompt-injection` |
| Feature store materialization | `feature-store-basics` |
| Secrets for API keys | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Task | Retrieval (asymmetric) vs similarity (symmetric) may need different models |
| Quality | Offline nDCG/Recall@k on labeled pairs |
| Latency | Batch embed throughput; p95 query embed time |
| Cost | $/1M tokens API vs GPU for self-host |
| Dim | Higher ≠ always better; consider Matryoshka/MRL truncation |
| Metric | Match index metric to model training (cosine common) |

## Workflow

### 1. Confirm scope and success criteria

1. Languages, domain, max doc length, QPS, privacy constraints.
2. Success metrics: Recall@10 target, p95 embed latency, monthly cost cap.

### 2. Inventory constraints

| Constraint | Questions |
| --- | --- |
| Data residency | Can text leave VPC? |
| Context length | Chunk size vs model max tokens |
| Languages | Mono vs multi |
| Updates | Full re-embed frequency |
| Infra | GPU available? |

### 3. Baseline current system (if any)

1. Record model id, dim, index size, monthly cost, Recall@k.
2. Freeze a golden evaluation set before trials.

### 4. Candidate shortlist

1. 2–4 candidates spanning API and/or open weights.
2. Include a strong small model (cost) and a larger one (quality ceiling).
3. Note distance metric and normalization requirements.

### 5. Evaluate fairly

```python
# Sketch evaluation loop
def evaluate(embed_q, embed_d, triples, k=10):
    # triples: (query, list[(doc_id, text)], relevant_ids)
    recalls = []
    for q, docs, rel in triples:
        qv = embed_q(q)
        ranked = top_k_by_cosine(qv, [(d, embed_d(t)) for d, t in docs], k)
        hits = sum(1 for d in ranked if d in rel)
        recalls.append(hits / max(len(rel), 1))
    return sum(recalls) / len(recalls)
```

1. Same chunking for all candidates unless chunking is part of the experiment (control it).
2. Measure: quality, embed QPS, index RAM/disk for dim, failure rates.
3. Test short queries and long docs separately if product uses both.

### 6. Decide dimensions and storage

| Dim | Tradeoff |
| --- | --- |
| 256–384 | Cheap ANN, may lose quality |
| 768 | Common open model default |
| 1024–3072 | API giants; cost/storage heavy |
| MRL | Train/use models that allow truncate-to-dim |

1. Prefer one dim for the collection; document metric.
2. Estimate re-embed wall clock for full corpus before approving switch.

### 7. Verify and hand off

1. Shadow traffic: embed with new model offline; compare retrieval overlap.
2. Canary users or tenant slice.
3. Version stamp all new vectors; plan decommission of old collection.
4. Hand monitoring to `embedding-drift-monitoring`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Decision | Eval on own gold set | “Highest MTEB Twitter thread” |
| Privacy | VPC model for sensitive text | Paste PHI to random API |
| Migration | Dual-write + cutover plan | Change model_id in place |
| Dim | Cost model attached | 3072-d for tiny FAQ bot |
| Metric | Cosine + normalized vectors | Mix IP and cosine randomly |

## Output Checklist

- [ ] Requirements (lang, privacy, QPS, cost) written
- [ ] Golden set prepared
- [ ] Candidates evaluated with Recall/nDCG + latency + cost
- [ ] Dimension and distance metric chosen
- [ ] Re-embed cost/time estimated
- [ ] Cutover + versioning plan documented
- [ ] API/key or model license reviewed
- [ ] Residual quality risk noted

## Rules

- Only embed data you are allowed to process with the chosen provider.
- Do not switch production models without re-embed and eval.
- Record model_id forever with vectors.
- Public leaderboards inform; they do not replace domain eval.
- Drift after choice → `embedding-drift-monitoring`.
