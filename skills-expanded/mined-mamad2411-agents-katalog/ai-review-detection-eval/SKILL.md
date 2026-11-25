---
name: ai-review-detection-eval
description: Evaluates a style-based classifier's ability to detect AI-generated text in academic peer reviews and measures temporal generalization by tracking detection rates across consecutive years. Use when the user wants to benchmark on ICLR Peer Reviews, Nature Communications Peer Reviews, or asks about evaluating this task. Reports percentage_ai_detected.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.00319
  bibtex_key: shen2026detecting
  confidence: medium
---

# ai-review-detection-eval

> Detecting AI-Generated Content in Academic Peer Reviews — Shen et al. (2026) (arXiv:2602.00319, 2026)

## What this evaluates

Evaluates a style-based classifier's ability to detect AI-generated text in academic peer reviews and measures temporal generalization by tracking detection rates across consecutive years.

## Datasets

- **ICLR Peer Reviews** — total ?; splits: train (320), test (1937), test (1887), test (1818), test (1961)
- **Nature Communications Peer Reviews** — total ?; splits: train (240), test (-1), test (-1), test (-1), test (-1)

## Metrics

- `percentage_ai_detected` **(primary)** — range: percent
  - Calculated as the number of reviews classified as AI-generated divided by the total number of reviews in a given year or quarter, multiplied by 100.

## Input / output format

**Input**: Raw text of academic peer review reports.

**Output**: Binary classification label: 'real' or 'AI-generated'.

## Scoring recipe

```python
def compute_percentage_ai_detected(predictions, total_reviews):
    ai_detected_count = sum(1 for p in predictions if p == 'AI-generated')
    return (ai_detected_count / total_reviews) * 100
```

## Common pitfalls

- Training data uses perfectly synthetic AI reviews, leading to 100% training accuracy which may not reflect real-world noise or generalization.
- Temporal evaluation assumes human writing style remains constant; stylistic drift in human reviews over time could be misclassified as AI-generated.
- Detection thresholds and confidence cutoffs are not specified, so reported percentages depend heavily on the classifier's decision boundary.

## Evidence (verbatim from paper)

> The detection model is trained on ICLR 2021 reviews and evaluated on reviews from 2022 to 2025.

#### 4.1.1 Model Performance on Training Set (ICLR 2021)

The detection model achieves perfect classification performance on ICLR reviews from 2021.
Specifically, all 160 real reviews are predicted as real, and all 160 AI-generated reviews are predicted as AI.

#### 4.1.2 Model Inference Results (ICLR 2022–2025)

Figure[1] ‣ 4.1 ICLR Results ‣ 4 Results ‣ Detecting AI-Generated Content in Academic Peer Reviews") presents the percentage of ICLR reviews classified as AI-generated for each evaluation year from 2022 to 2025.
Table[1] ‣ 4.1 ICLR Results ‣ 4 Results ‣ Detecting AI-Generated Content in Academic Peer Reviews") reports the corresponding counts and percentages.
The proportion of reviews classified as AI-generated increases across successive evaluation years.

## Citation

```bibtex
@misc{shen2026detecting,
  title={Detecting AI-Generated Content in Academic Peer Reviews},
  author={Shen et al. (2026)},
  year={2026},
  note={arXiv:2602.00319}
}
```

- arXiv: 2602.00319
