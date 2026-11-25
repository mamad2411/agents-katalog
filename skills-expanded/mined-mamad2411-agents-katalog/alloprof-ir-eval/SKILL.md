---
name: alloprof-ir-eval
description: Evaluates information retrieval capabilities in an educational context by testing a model's ability to retrieve relevant reference pages or similar past questions given a student's query. It probes handling of noisy text (spelling/grammar errors), multimodal inputs (images, formulas), and grade-aware language complexity. Use when the user wants to benchmark on Alloprof, or asks about evaluating this task. Reports nDCG.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2302.07738
  bibtex_key: lefebvrebrossard2023alloprof
  confidence: medium
---

# alloprof-ir-eval

> Alloprof: a new French question-answer education dataset and its use in an information retrieval case study — Lefebvre-Brossard et al. (2023) (arXiv:2302.07738, 2023)

## What this evaluates

Evaluates information retrieval capabilities in an educational context by testing a model's ability to retrieve relevant reference pages or similar past questions given a student's query. It probes handling of noisy text (spelling/grammar errors), multimodal inputs (images, formulas), and grade-aware language complexity.

## Datasets

- **Alloprof** — total 29349; splits: test (-1)

## Metrics

- `nDCG` **(primary)** — range: [0, 1]
  - Normalized Discounted Cumulative Gain: measures ranking quality by discounting the relevance of documents at lower ranks, normalized by the ideal DCG.
- `MRR` — range: [0, 1]
  - Mean Reciprocal Rank: averages the reciprocal of the rank of the first relevant document across all queries.

## Input / output format

**Input**: Student question (text, optionally with images, grade level, and subject)

**Output**: Ranked list of retrieved reference pages or similar past questions

## Scoring recipe

```python
def compute_metrics(predictions, gold_links):
    mrr_scores, ndcg_scores = [], []
    for pred, gold in zip(predictions, gold_links):
        rr = 1.0 / (next((i+1 for i, doc in enumerate(pred) if doc in gold), len(pred)+1))
        mrr_scores.append(rr)
        dcg = sum(1.0 / math.log2(i+2) for i, doc in enumerate(pred) if doc in gold)
        idcg = sum(1.0 / math.log2(i+2) for i in range(min(len(gold), len(pred))))
        ndcg_scores.append(dcg / idcg if idcg > 0 else 0.0)
    return {'MRR': sum(mrr_scores)/len(mrr_scores), 'nDCG': sum(ndcg_scores)/len(ndcg_scores)}
```

## Common pitfalls

- Relevance is proxied by links in accepted answers, meaning many truly relevant documents without links are treated as negatives.
- Multimodal elements (images, math formulas, spelling errors) are often ignored by standard text-only retrievers, hurting performance.
- Grade-level complexity varies significantly; models trained on high-school data may fail on elementary queries due to vocabulary and syntax differences.

## Evidence (verbatim from paper)

> For around half the questions in the dataset (55.1%), the explanation has at least one link either to another question or to a reference page on the website and these are the ones considered relevant to the question. Because other documents can also be relevant, appropriate metrics and the ones we present in section 3.1 should focus on the presence of these linked documents and not their absence. A case study evaluates information retrieval performance using BERT-based models, achieving 58.5% prediction accuracy (MRR: 0.54, nDCG: 0.62) outperforming TF-IDF, while maintaining acceptable inference speed (0.7s), highlighting the need for multimodal and grade-aware retrieval systems in educational contexts.

## Citation

```bibtex
@misc{lefebvrebrossard2023alloprof,
  title={Alloprof: a new French question-answer education dataset and its use in an information retrieval case study},
  author={Lefebvre-Brossard et al. (2023)},
  year={2023},
  note={arXiv:2302.07738}
}
```

- arXiv: 2302.07738
