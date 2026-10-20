---
name: agrigpt-omni-eval
description: Evaluates a unified speech-vision-text model's capability in multilingual agricultural reasoning, covering text generation, vision-language QA, and multimodal speech understanding across open-ended and multiple-choice formats. Use when the user wants to benchmark on AgriBench-13K, AgriBench-VL-4K, AgriBench-Omni-2K, or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2512.10624
  bibtex_key: yang2025agrigptomni
  confidence: high
---

# agrigpt-omni-eval

> AgriGPT-Omni: A Unified Speech-Vision-Text Framework for Multilingual Agricultural Intelligence — Bo Yang et al. (2025) (arXiv:2512.10624, 2025)

## What this evaluates

Evaluates a unified speech-vision-text model's capability in multilingual agricultural reasoning, covering text generation, vision-language QA, and multimodal speech understanding across open-ended and multiple-choice formats.

## Datasets

- **AgriBench-13K** — total 13000; splits: test (-1)
- **AgriBench-VL-4K** — total 4000; splits: test (-1)
- **AgriBench-Omni-2K** — total 2000; splits: test (-1)

## Metrics

- `Accuracy` **(primary)** — range: percent
  - Fraction of correctly predicted answers on multiple-choice tasks. Calculated as the number of matches between model predictions and gold labels divided by the total number of instances.
- `Pairwise Win Rate` — range: percent
  - Proportion of head-to-head comparisons where the model's open-ended response is judged superior to a baseline's response on the same instance. Ties are counted separately and included in the denominator.

## Input / output format

**Input**: Multimodal inputs combining speech audio, text prompts, and/or images in four configurations: speech-only, speech+text, speech+image, and speech+image+text.

**Output**: Text responses, either open-ended answers or selected multiple-choice options.

## Scoring recipe

```python
# Accuracy (Multiple Choice)
correct = sum(1 for p, g in zip(predictions, gold) if p == g)
accuracy = correct / len(predictions)

# Pairwise Win Rate (Open QA)
wins = sum(1 for p, b in zip(preds, baselines) if judge(p) > judge(b))
ties = sum(1 for p, b in zip(preds, baselines) if judge(p) == judge(b))
losses = sum(1 for p, b in zip(preds, baselines) if judge(p) < judge(b))
win_rate = wins / (wins + ties + losses)
```

## Common pitfalls

- Pairwise win rates are computed against specific baselines rather than as absolute scores, making cross-model comparisons dependent on the chosen reference models.
- The evaluation aggregates results across six languages but reports per-language and overall metrics, which can mask performance disparities in low-resource dialects like Sichuanese or Cantonese.
- Real-world robustness is measured via synthetic vs. human speech pairwise comparisons, which does not directly translate to standard accuracy metrics and may obscure absolute performance degradation.

## Evidence (verbatim from paper)

> We adopt Win Rate for open-ended generation tasks and Accuracy for multiple-choice tasks to provide a comprehensive view of model behavior under different reasoning constraints.

## Citation

```bibtex
@misc{yang2025agrigptomni,
  title={AgriGPT-Omni: A Unified Speech-Vision-Text Framework for Multilingual Agricultural Intelligence},
  author={Bo Yang et al. (2025)},
  year={2025},
  note={arXiv:2512.10624}
}
```

- arXiv: 2512.10624
