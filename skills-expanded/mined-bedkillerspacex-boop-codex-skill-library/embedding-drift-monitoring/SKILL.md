---
name: embedding-drift-monitoring
description: >
  Monitor embedding and retrieval drift for owned vector search/RAG systems:
  reference query sets, nearest-neighbor stability, distribution shifts, model
  version mismatches, and alert thresholds. Use when embedding drift, vector
  index quality, RAG recall regression, or re-embed pipelines. Not model
  selection alone (see embedding-model-choice).
---

# Embedding Drift Monitoring

## Scope And Authorization

- **In scope:** Vector indexes, embedding pipelines, and RAG stacks you operate.
- **Out of scope:** Scraping third-party embeddings/APIs beyond your contracts.
- Query sets and documents may contain PII—store evaluation corpora under access control.
- Prefer shadow evaluation before re-embedding production indexes.
- Pair with `embedding-model-choice` and `code-quality-standards`.

## When To Use

- Production RAG quality quietly degrades after content or model changes.
- Detecting accidental model/dimension swaps in deploy.
- Scheduling full or partial re-embeds when drift exceeds budget.
- Comparing ANN index freshness vs source-of-truth documents.
- Building golden-question eval harnesses for retrieval.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Choosing embedding model/dimensions | `embedding-model-choice` |
| LLM prompt injection testing | `llm-prompt-injection` |
| Generic metrics backends | `observability-metrics-tracing` |
| Feature store features | `feature-store-basics` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Causes | New model, new chunking, corpus shift, bad deploys, partial reindex |
| Signals | Recall@k on golden set; cosine to reference embeds; score distribution |
| Versioning | Store `model_id`, dim, distance metric with every vector |
| Alerts | Drop in recall; spike in empty retrievals; dim mismatch errors |
| Action | Freeze deploys; re-embed; rollback model |
| Cost | Sample-based monitoring daily; full sweep weekly |

## Workflow

### 1. Confirm scope and success criteria

1. Indexes, models, and applications in scope.
2. Success: detect material retrieval regression within one eval cycle; ownership for re-embed.

### 2. Inventory pipeline

```bash
# Find embed call sites / model ids
rg -n "embed|OpenAI|sentence-transform|vector|upsert" -i --glob '!node_modules' | head
```

1. Record model name, dimension, metric (`cosine`/`ip`/`l2`), chunking params.
2. Note whether online queries and index use the **same** model version.

### 3. Build reference assets

1. **Golden queries** (50–500): real user-like questions with labeled relevant doc ids.
2. **Canary documents**: fixed texts re-embedded each run; store reference vectors.
3. Hold-out period for content that must not be used for training of unrelated models.

### 4. Define drift metrics

| Metric | Method |
| --- | --- |
| Recall@k | Fraction of gold docs in top-k |
| MRR / nDCG | Ranking quality on gold set |
| Canary cosine | Cosine(new_embed(text), reference_vector) |
| Score histogram | Mean/p50 top-1 score shift |
| Null rate | Queries with no hits above threshold |
| Version mismatch | Query model_id ≠ index model_id |

```python
# Sketch: canary similarity
import numpy as np

def cosine(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

def canary_drift(embed_fn, text, reference_vec, min_cos=0.95):
    v = embed_fn(text)
    score = cosine(v, reference_vec)
    return score, score < min_cos
```

### 5. Schedule monitoring jobs

1. **On deploy:** run golden set; block if recall drops > threshold (e.g. 5 absolute points).
2. **Daily:** canary embeds + sample live queries (privacy-preserving).
3. **On corpus load:** compare new chunk embeddings stats to rolling baseline.
4. Emit metrics: `rag_recall_at_k`, `embedding_canary_cosine`, `index_model_id`.

### 6. Verify with evidence

1. Intentionally swap to wrong model in stage → alerts fire and traffic blocked.
2. Confirm partial reindex detection (mixed model versions in one collection)—fail closed.
3. Document false positive rate of thresholds over two weeks.

### 7. Hand off

1. Runbook: freeze → diagnose (model vs data) → re-embed → validate golden set → unfreeze.
2. Owners: ML platform + search app.
3. Retention for eval reports; redact query text if needed.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Version | model_id on every vector | Anonymous float arrays |
| Eval | Golden set in CI | Only “vibes” on demos |
| Alert | Recall drop + canary | CPU of embed service only |
| Mixed index | Prevent dual models | Silent dual-write |
| Action | Re-embed plan | Ignore drift for months |

## Output Checklist

- [ ] Model/dim/metric inventory complete
- [ ] Golden query set and canaries created
- [ ] Drift metrics and thresholds defined
- [ ] Deploy gate and daily job wired
- [ ] Stage fault-injection proves detection
- [ ] Re-embed runbook owned
- [ ] PII handling for eval corpora documented
- [ ] Residual risk noted

## Rules

- Owned systems only; respect data residency for corpora.
- Never mix embedding models in one index without migration plan.
- Prefer measurable recall over anecdotal quality.
- Pair model upgrades with full re-embed cost estimates.
- Selection of models → `embedding-model-choice`.
