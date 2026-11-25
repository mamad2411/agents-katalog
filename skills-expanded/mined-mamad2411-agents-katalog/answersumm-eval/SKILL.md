---
name: answersumm-eval
description: Evaluates multi-perspective answer summarization for community question answering, probing content selection, perspective clustering, abstractive summarization, and factual consistency/coverage. Use when the user wants to benchmark on AnswerSumm, or asks about evaluating this task. Reports F1, ROUGE-1/2/L.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2111.06474
  bibtex_key: fabbri2021answersumm
  confidence: high
---

# answersumm-eval

> AnswerSumm: A Manually-Curated Dataset and Pipeline for Answer Summarization — Fabbri et al. (2021) (arXiv:2111.06474, 2021)

## What this evaluates

Evaluates multi-perspective answer summarization for community question answering, probing content selection, perspective clustering, abstractive summarization, and factual consistency/coverage.

## Datasets

- **AnswerSumm** — total 4631; splits: test (-1)

## Metrics

- `F1` **(primary)** — range: [0, 1]
  - Standard F1 score for binary relevance classification in the SentSelect subtask.
- `ROUGE-1/2/L` **(primary)** — range: [0, 1]
  - Standard ROUGE recall/precision/F1 scores measuring n-gram overlap between generated summaries and gold references.
- `NLI` — range: [0, 1]
  - Natural Language Inference entailment score measuring factual consistency between input and output.
- `Semantic Area` — range: [0, 1]
  - Metric measuring semantic coverage of the generated summary relative to the source documents.

## Input / output format

**Input**: Question concatenated with source sentences or documents.

**Output**: Abstractive summary or bullet-point answers.

## Scoring recipe

```python
def compute_rouge(predictions, references):
    return rouge1, rouge2, rouge_l

def compute_f1(predictions, references):
    tp = sum(1 for p, r in zip(predictions, references) if p == r == 1)
    fp = sum(1 for p, r in zip(predictions, references) if p == 1 and r == 0)
    fn = sum(1 for p, r in zip(predictions, references) if p == 0 and r == 1)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    return 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
```

## Common pitfalls

- Low inter-annotator agreement (Fleiss Kappa 0.25) makes the SentSelect subtask highly subjective.
- Models tend to be overly extractive with low novel unigram rates (~4%) compared to gold summaries (~21%).
- ROUGE scores do not fully align with factual consistency (NLI) or semantic coverage (Semantic Area) metrics.

## Evidence (verbatim from paper)

> The best results for SentSelect are yielded by RoBERTa relevance classification as illustrated in Table 5. RoBERTa yields an F1 score of 0.49. ... Table 6: ROUGE scores for ClustSumm and Fusion summarization tasks... Table 8: A comparison of model ROUGE, NLI, and Semantic Area scores.

## Citation

```bibtex
@misc{fabbri2021answersumm,
  title={AnswerSumm: A Manually-Curated Dataset and Pipeline for Answer Summarization},
  author={Fabbri et al. (2021)},
  year={2021},
  note={arXiv:2111.06474}
}
```

- arXiv: 2111.06474
