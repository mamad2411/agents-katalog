---
name: 3d-vqa-eval
description: Evaluates a model's ability to answer natural language questions about 3D indoor scenes using only multi-view RGB images. It probes spatial reasoning, semantic understanding, and zero-shot generalization across different embodied agent scenarios. Use when the user wants to benchmark on ScanQA, SQA3D, MSR3D, or asks about evaluating this task. Reports EM@1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.06271
  bibtex_key: thai2025splattalk
  confidence: high
---

# 3d-vqa-eval

> SplatTalk: 3D VQA with Gaussian Splatting — Anh Thai et al. (arXiv:2503.06271, 2025)

## What this evaluates

Evaluates a model's ability to answer natural language questions about 3D indoor scenes using only multi-view RGB images. It probes spatial reasoning, semantic understanding, and zero-shot generalization across different embodied agent scenarios.

## Datasets

- **ScanQA** — total ?; splits: train (500), val (-1)
- **SQA3D** — total ?; splits: test (-1)
- **MSR3D** — total ?; splits: test (-1)

## Metrics

- `EM@1` **(primary)** — range: [0, 1]
  - Exact Match at rank 1: 1 if the predicted answer exactly matches any of the ground truth answers, 0 otherwise.
- `CIDEr` — range: [0, 1]
  - Standard n-gram based metric that weights rare n-grams higher to measure semantic similarity between prediction and reference.
- `METEOR` — range: [0, 1]
  - N-gram matching metric incorporating synonymy and stemming to measure semantic equivalence.
- `ROUGE` — range: [0, 1]
  - Recall-Oriented Understudy for Gisting Evaluation; measures n-gram overlap between prediction and reference.
- `EM@1-Refined` — range: [0, 1]
  - Refined exact match allowing for minor phrasing variations, punctuation differences, and case normalization.
- `LLM-Match` — range: [0, 1]
  - LLM-based scoring metric recommended by MSR3D authors to judge semantic equivalence between prediction and ground truth.

## Input / output format

**Input**: Multi-view RGB images (uniformly sampled around the scene) and a natural language question describing an object or spatial relationship.

**Output**: A natural language text answer to the question.

## Scoring recipe

```python
def compute_em1(predictions, gold_answers):
    correct = 0
    for pred, golds in zip(predictions, gold_answers):
        if pred.strip().lower() in [g.strip().lower() for g in golds]:
            correct += 1
    return correct / len(predictions)

# For CIDEr, METEOR, ROUGE, use standard NLTK/ROUGE libraries.
# For LLM-Match, pass (prediction, ground_truth) to the recommended LLM judge and average binary scores.
```

## Common pitfalls

- MSR3D evaluation is strictly zero-shot; fine-tuning on ScanQA/SQA3D can cause performance drops due to dataset distribution shift rather than model degradation.
- EM@1 uses strict string matching, so paraphrased but semantically correct answers are penalized unless EM@1-Refined is reported.
- Baselines vary in input modality (2D images vs 3D point clouds), making direct performance comparisons sensitive to input constraints rather than pure reasoning ability.

## Evidence (verbatim from paper)

> For ScanQA and SQA3D, we evaluate performance using standard n-gram-based metrics, specifically CIDEr, METEOR, ROUGE, EM@1, and EM@1-Refined for ScanQA, and EM@1 and EM@1-Refined for SQA3D. In contrast, for MSR3D, we utilize the LLM-Match score as recommended by the authors.

## Citation

```bibtex
@misc{thai2025splattalk,
  title={SplatTalk: 3D VQA with Gaussian Splatting},
  author={Anh Thai et al.},
  year={2025},
  note={arXiv:2503.06271}
}
```

- arXiv: 2503.06271
