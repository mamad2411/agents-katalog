---
name: author-centric-review-eval
description: Evaluates an LLM's ability to generate structured, author-centric academic feedback (Summary, Strengths, Weaknesses, Questions) from long research papers. It probes the model's capacity to retrieve salient passages via graph-based retrieval and synthesize constructive pre-submission reviews without relying on full context or multi-agent systems. Use when the user wants to benchmark on ICLR 2024 (ICT), CNT_10, or asks about evaluating this task. Reports human evaluation.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.14376
  bibtex_key: chitale2025graphguided
  confidence: medium
---

# author-centric-review-eval

> Graph-Guided Passage Retrieval for Author-Centric Structured Feedback — Chitale et al. (2025) (arXiv:2505.14376, 2025)

## What this evaluates

Evaluates an LLM's ability to generate structured, author-centric academic feedback (Summary, Strengths, Weaknesses, Questions) from long research papers. It probes the model's capacity to retrieve salient passages via graph-based retrieval and synthesize constructive pre-submission reviews without relying on full context or multi-agent systems.

## Datasets

- **ICLR 2024 (ICT)** — total 5653; splits: train (-1), test (-1)
- **CNT_10** — total 10; splits: test (10)

## Metrics

- `human evaluation` **(primary)** — range: other
  - Human raters assess the generated Summary, Strengths, Weaknesses, and Questions sections against ground-truth reviews or predefined criteria for constructive feedback quality.

## Input / output format

**Input**: Parsed academic paper represented as a hierarchical graph (nodes: headings, passages, sentences) or raw text document.

**Output**: Structured review containing four sections: Summary, Strengths, Weaknesses, and Questions.

## Scoring recipe

```python
def score_human_eval(predictions, gold_reviews):
    scores = []
    for pred, gold in zip(predictions, gold_reviews):
        scores.append(human_rater_score(pred, gold))
    return sum(scores) / len(scores)
```

## Common pitfalls

- The evaluation explicitly excludes rating-based fields (Soundness, Presentation, Contribution, Confidence, Rating) to focus solely on constructive, author-centric feedback.
- Human evaluation is performed on a small supplementary set (CNT_10) alongside ICLR 2024 test data, so results may not generalize to larger unseen venues without caution.

## Evidence (verbatim from paper)

> Each paper is associated with multiple reviews containing sections such as Summary, Strengths, Weaknesses, Questions, Soundness, Presentation, Contribution, Confidence, and Rating. We retain only the Summary, Strengths, Weaknesses, and Questions sections, as these encode constructive feedback for authors-centric pre-submission support... To assess cross-venue performance, we curate a supplementary dataset of 10 papers from COLM and NeurIPS 2025 (CNT_10). This set complements the ICLR 2024 test data (ICT) for the human evaluation detailed in Section[6.3].

## Citation

```bibtex
@misc{chitale2025graphguided,
  title={Graph-Guided Passage Retrieval for Author-Centric Structured Feedback},
  author={Chitale et al. (2025)},
  year={2025},
  note={arXiv:2505.14376}
}
```

- arXiv: 2505.14376
