---
name: artifact-understanding-eval
description: Evaluates vision-language models on their ability to detect, spatially localize, and explain visual artifacts in AI-generated images. It probes the model's capacity for fine-grained visual reasoning and artifact-aware grounding beyond standard natural image understanding. Use when the user wants to benchmark on ArtiBench, LOKI, or asks about evaluating this task. Reports accuracy, mIoU, ROUGE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.20951
  bibtex_key: park2026seeandfix
  confidence: high
---

# artifact-understanding-eval

> See and Fix the Flaws: Enabling VLMs and Diffusion Models to Comprehend Visual Artifacts via Agentic Data Synthesis — Jaehyun Park et al. (2026) (arXiv:2602.20951, 2026)

## What this evaluates

Evaluates vision-language models on their ability to detect, spatially localize, and explain visual artifacts in AI-generated images. It probes the model's capacity for fine-grained visual reasoning and artifact-aware grounding beyond standard natural image understanding.

## Datasets

- **ArtiBench** — total ?; splits: test (-1)
- **LOKI** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Fraction of correctly classified images (artifact vs. clean) out of the total test set.
- `F1 score` — range: [0, 1]
  - Harmonic mean of precision and recall for binary artifact detection.
- `mIoU` **(primary)** — range: [0, 1]
  - Mean Intersection over Union between predicted artifact segmentation masks and ground truth masks across all test images.
- `ROUGE` **(primary)** — range: [0, 1]
  - Recall-Oriented Understudy for Gisting Evaluation, measuring n-gram overlap between generated explanations and reference texts.
- `CSS` — range: [0, 1]
  - Custom similarity metric used to evaluate the semantic alignment and quality of generated explanations against ground truth.

## Input / output format

**Input**: Image (AI-generated, potentially containing artifacts) paired with a visual question or prompt. For detection and localization, the input is the image alone or with a prompt asking to identify/locate artifacts. For explanation, the input is the image with a question asking for a description of the artifact.

**Output**: Binary label (artifact/clean) for detection; pixel-level segmentation mask or bounding box for localization; natural language text description for explanation.

## Scoring recipe

```python
def score_detection(preds, golds):
    acc = sum(p == g for p, g in zip(preds, golds)) / len(golds)
    f1 = f1_score(golds, preds)
    return acc, f1

def score_localization(pred_masks, gold_masks):
    ious = [intersection(m1, m2) / union(m1, m2) for m1, m2 in zip(pred_masks, gold_masks)]
    miou = sum(ious) / len(ious)
    f1 = f1_score(flatten(gold_masks), flatten(pred_masks))
    return miou, f1

def score_explanation(pred_texts, gold_texts):
    rouge = rouge_score(gold_texts, pred_texts)
    css = compute_css_similarity(gold_texts, pred_texts)
    return rouge, css
```

## Common pitfalls

- Confusing binary artifact detection with spatial localization, leading to incorrect metric assignment or evaluation setup.
- Evaluating on standard natural image datasets instead of artifact-specific benchmarks like ArtiBench or LOKI, which miss subtle AI-generation failures.
- Ignoring the paired clean/artifact data structure when training reward models, which degrades test-time scaling performance.

## Evidence (verbatim from paper)

> For evaluation metrics, we use accuracy and F1 score for detection, mIoU and F1 score for localization, and ROUGE and CSS for explanation.

## Citation

```bibtex
@misc{park2026seeandfix,
  title={See and Fix the Flaws: Enabling VLMs and Diffusion Models to Comprehend Visual Artifacts via Agentic Data Synthesis},
  author={Jaehyun Park et al. (2026)},
  year={2026},
  note={arXiv:2602.20951}
}
```

- arXiv: 2602.20951
