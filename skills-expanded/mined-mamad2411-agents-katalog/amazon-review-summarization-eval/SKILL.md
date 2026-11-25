---
name: amazon-review-summarization-eval
description: Evaluates the ability of abstractive summarization models to generate concise, informative summaries of product reviews while preserving aspect and opinion details. It measures lexical overlap with human-written reference summaries. Use when the user wants to benchmark on Amazon Reviews (Healthcare & Electronics), or asks about evaluating this task. Reports ROUGE-1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2004.05755
  bibtex_key: tian2020aspect
  confidence: high
---

# amazon-review-summarization-eval

> Aspect and Opinion Aware Abstractive Review Summarization with Reinforced Hard Typed Decoder — Tian et al. (2020) (arXiv:2004.05755, 2020)

## What this evaluates

Evaluates the ability of abstractive summarization models to generate concise, informative summaries of product reviews while preserving aspect and opinion details. It measures lexical overlap with human-written reference summaries.

## Datasets

- **Amazon Reviews (Healthcare & Electronics)** — total 235638; splits: train (-1), dev (-1), test (-1)

## Metrics

- `ROUGE-1` **(primary)** — range: percent
  - F1 score of unigram overlap between generated summary and reference summaries.
- `ROUGE-2` — range: percent
  - F1 score of bigram overlap between generated summary and reference summaries.
- `ROUGE-L` — range: percent
  - F1 score based on the longest common subsequence (LCS) between generated and reference summaries.

## Input / output format

**Input**: Raw product review text.

**Output**: Abstractive summary text.

## Scoring recipe

```python
def compute_rouge(predictions, references):
    scores = {}
    for n in [1, 2]:
        scores[f'ROUGE-{n}'] = rouge_n(predictions, references, n)
    scores['ROUGE-L'] = rouge_l(predictions, references)
    return scores
```

## Common pitfalls

- ROUGE scores only measure exact n-gram overlap and do not capture semantic similarity or factual correctness.
- Random train/dev/test splits on review-summary pairs may cause data leakage if reviews share authors or products.
- Human analysis is qualitative and limited to two examples, making it hard to generalize model advantages.

## Evidence (verbatim from paper)

> Following many previous studies on abstractive summarization, we choose ROUGE-1, 2, L [7] to automatically quantify how well a model fits the data.

## Citation

```bibtex
@misc{tian2020aspect,
  title={Aspect and Opinion Aware Abstractive Review Summarization with Reinforced Hard Typed Decoder},
  author={Tian et al. (2020)},
  year={2020},
  note={arXiv:2004.05755}
}
```

- arXiv: 2004.05755
