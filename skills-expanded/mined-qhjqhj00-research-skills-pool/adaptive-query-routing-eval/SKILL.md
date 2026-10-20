---
name: adaptive-query-routing-eval
description: Evaluates retrieval and answer generation methods across structured financial, legal, and medical documents. It probes how well different architectures handle varying query complexities, cross-references, and domain-specific structural requirements. Use when the user wants to benchmark on Controlled Multi-Domain Corpus, FinanceBench, or asks about evaluating this task. Reports Quality.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.14222
  bibtex_key: hashmi2026adaptive
  confidence: high
---

# adaptive-query-routing-eval

> Adaptive Query Routing: A Tier-Based Framework for Hybrid Retrieval Across Financial, Legal, and Medical Documents — Hashmi (2026) (arXiv:2604.14222, 2026)

## What this evaluates

Evaluates retrieval and answer generation methods across structured financial, legal, and medical documents. It probes how well different architectures handle varying query complexities, cross-references, and domain-specific structural requirements.

## Datasets

- **Controlled Multi-Domain Corpus** — total 22; splits: test (22)
- **FinanceBench** — total 50; splits: test (50)

## Metrics

- `Quality` **(primary)** — range: [0, 1]
  - LLM-as-Judge evaluation score on a 0-1 scale assessing answer correctness and relevance.
- `Recall` — range: [0, 1]
  - Proportion of relevant document sections correctly retrieved by the system.
- `Precision` — range: [0, 1]
  - Proportion of retrieved sections that are relevant to the query.
- `F1` — range: [0, 1]
  - Harmonic mean of precision and recall.
- `Latency` — range: seconds
  - End-to-end retrieval and generation time measured in seconds.

## Input / output format

**Input**: Natural language queries across financial, legal, and medical domains, categorized into four complexity tiers (simple, multi-section, cross-reference, multi-document synthesis).

**Output**: Retrieved document sections and generated answers.

## Scoring recipe

```python
precision = len(retrieved & relevant) / len(retrieved)
recall = len(retrieved & relevant) / len(relevant)
f1 = 2 * (precision * recall) / (precision + recall)
latency = end_time - start_time
quality = llm_as_judge_score(answer, query, context) # 0-1 scale
```

## Common pitfalls

- Assuming vector similarity reliably captures cross-references; it misses ~8.3% due to low semantic overlap with target sections.
- Treating performance as uniform across domains; Vector RAG leads in financial but lags in legal/medical where structural navigation is key.
- Ignoring latency trade-offs; reasoning-based methods incur ~2x latency for marginal quality gains on simple queries.

## Evidence (verbatim from paper)

> Both Tree Reasoning and Hybrid AHR achieve perfect section recall (1.00), correctly following internal references to appendices, exhibits, and notes. Vector RAG achieves 0.917 recall, missing cross-referenced sections with low semantic similarity to the query.

## Citation

```bibtex
@misc{hashmi2026adaptive,
  title={Adaptive Query Routing: A Tier-Based Framework for Hybrid Retrieval Across Financial, Legal, and Medical Documents},
  author={Hashmi (2026)},
  year={2026},
  note={arXiv:2604.14222}
}
```

- arXiv: 2604.14222
