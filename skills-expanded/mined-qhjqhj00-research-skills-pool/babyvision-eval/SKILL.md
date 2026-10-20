---
name: babyvision-eval
description: Evaluates fundamental visual reasoning capabilities in multimodal large language models independent of linguistic priors. It probes early-vision abilities such as visual tracking, spatial perception, fine-grained discrimination, and visual pattern recognition through image-based tasks. Use when the user wants to benchmark on BabyVision, or asks about evaluating this task. Reports Avg@3.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.06521
  bibtex_key: chen2026babyvision
  confidence: high
---

# babyvision-eval

> BabyVision: Visual Reasoning Beyond Language — Chen et al. (2026) (arXiv:2601.06521, 2026)

## What this evaluates

Evaluates fundamental visual reasoning capabilities in multimodal large language models independent of linguistic priors. It probes early-vision abilities such as visual tracking, spatial perception, fine-grained discrimination, and visual pattern recognition through image-based tasks.

## Datasets

- **BabyVision** — total 388; splits: test (388); repo https://github.com/UniPat-AI/BabyVision

## Metrics

- `Avg@3` **(primary)** — range: percent
  - Average Pass@1 accuracy computed across three independent inference runs. For each run, accuracy is the fraction of correctly answered questions out of the total. The final score is the mean of the three run accuracies.

## Input / output format

**Input**: Image-text pairs presenting visual reasoning tasks with multiple-choice or open-ended prompts.

**Output**: Text responses for BabyVision; generated images for BabyVision-Gen.

## Scoring recipe

```python
def compute_avg3(predictions_per_run, gold_labels, n_runs=3):
    accuracies = []
    for run_preds in predictions_per_run:
        correct = sum(1 for p, g in zip(run_preds, gold_labels) if p == g)
        accuracies.append(correct / len(gold_labels))
    return sum(accuracies) / n_runs
```

## Common pitfalls

- BabyVision (MLLM text output) and BabyVision-Gen (image generation output) use different evaluation methodologies and are not directly comparable.
- Assuming model scaling monotonically improves performance; the paper notes smaller models (e.g., 4B) can slightly outperform larger ones (e.g., 8B) on certain tasks.
- Overestimating model performance by relying on language priors; the benchmark is explicitly designed to minimize linguistic cues to isolate pure visual reasoning.

## Evidence (verbatim from paper)

> We report the Avg@3 results for all evaluated models. Reported values represent the average Pass@1 accuracy across three random runs, accompanied by the standard deviation.

## Citation

```bibtex
@misc{chen2026babyvision,
  title={BabyVision: Visual Reasoning Beyond Language},
  author={Chen et al. (2026)},
  year={2026},
  note={arXiv:2601.06521}
}
```

- arXiv: 2601.06521
