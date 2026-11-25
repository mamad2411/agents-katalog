---
name: audio-visual-gfsl-eval
description: Evaluates audio-visual few-shot video classification by measuring how well models generalize to novel classes with limited training examples (1, 5, 10-shot). It reports both generalised few-shot learning (HM) and standard few-shot learning (FSL) accuracy to assess bias towards base classes. Use when the user wants to benchmark on VGGSound-FSL, UCF-FSL, ActivityNet-FSL, or asks about evaluating this task. Reports HM.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2309.03869
  bibtex_key: mercea2023texttofeaturediffusion
  confidence: high
---

# audio-visual-gfsl-eval

> Text-to-feature diffusion for audio-visual few-shot learning — Mercea et al. (2023) (arXiv:2309.03869, 2023)

## What this evaluates

Evaluates audio-visual few-shot video classification by measuring how well models generalize to novel classes with limited training examples (1, 5, 10-shot). It reports both generalised few-shot learning (HM) and standard few-shot learning (FSL) accuracy to assess bias towards base classes.

## Datasets

- **VGGSound-FSL** — total ?; splits: test (-1); repo https://github.com/ExplainableML/AVDIFF-GFSL
- **UCF-FSL** — total ?; splits: test (-1); repo https://github.com/ExplainableML/AVDIFF-GFSL
- **ActivityNet-FSL** — total ?; splits: test (-1); repo https://github.com/ExplainableML/AVDIFF-GFSL

## Metrics

- `HM` **(primary)** — range: percent
  - Harmonic mean of the mean class accuracies for base and novel classes. HM = 2 * (Acc_base * Acc_novel) / (Acc_base + Acc_novel).
- `FSL` — range: percent
  - Mean class accuracy computed only on the test subset of novel classes.

## Input / output format

**Input**: Pre-extracted audio and visual features from pre-trained classification networks, processed via cross-modal attention, and conditioned on text embeddings (word2vec) or class prototypes.

**Output**: Predicted class labels for video clips, used to compute per-class accuracy on base and novel sets.

## Scoring recipe

```python
def compute_metrics(predictions, gold, base_classes, novel_classes):
    acc_base = mean([accuracy(predictions[c], gold[c]) for c in base_classes])
    acc_novel = mean([accuracy(predictions[c], gold[c]) for c in novel_classes])
    FSL = acc_novel
    HM = 2 * (acc_base * acc_novel) / (acc_base + acc_novel)
    return HM, FSL
```

## Common pitfalls

- Confusing HM (generalised FSL) with FSL (novel-only accuracy); HM explicitly penalizes models biased towards base classes.
- ActivityNet-FSL contains very long videos requiring evaluation-time trimming to a maximum of 300 features, which significantly impacts temporal modeling compared to other datasets.
- Calibrated stacking is used to reduce base-class bias, which can alter the expected relationship between HM, novel accuracy (N), and FSL scores.

## Evidence (verbatim from paper)

> The harmonic mean (HM) of the mean class accuracies for base and novel classes are reported for GFSL. For the FSL performance, only the test subset of the novel classes is considered.

## Citation

```bibtex
@misc{mercea2023texttofeaturediffusion,
  title={Text-to-feature diffusion for audio-visual few-shot learning},
  author={Mercea et al. (2023)},
  year={2023},
  note={arXiv:2309.03869}
}
```

- arXiv: 2309.03869
