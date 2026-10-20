---
name: audiomotionbench-eval
description: Evaluates large audio-language models' ability to perceive and reason about spatial motion in binaural audio. It probes whether models can correctly infer motion direction and trajectories from interaural cues, rather than relying on linguistic or spectral heuristics. Use when the user wants to benchmark on AudioMotionBench, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.13273
  bibtex_key: sun2025audiomotionbench
  confidence: high
---

# audiomotionbench-eval

> Spatial Blind Spot: Auditory Motion Perception Deficits in Audio LLMs — Sun et al. (2025) (arXiv:2511.13273, 2025)

## What this evaluates

Evaluates large audio-language models' ability to perceive and reason about spatial motion in binaural audio. It probes whether models can correctly infer motion direction and trajectories from interaural cues, rather than relying on linguistic or spectral heuristics.

## Datasets

- **AudioMotionBench** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Mean accuracy across all task variants and noise levels, averaged over three random seeds. Calculated as the proportion of correctly normalized predictions (A-D or TRUE/FALSE) against ground truth.
- `Acc-MCQ` — range: percent
  - Accuracy on multiple-choice questions: 1/N sum_{i=1}^N I[f_MCQ(x_i) = y_i], where f_MCQ is the predicted option and y_i is the ground truth.
- `Acc-T/F` — range: percent
  - Accuracy on true/false verification: 1/(2N) sum_{i=1}^N (I[hat{z}_i^T = True] + I[hat{z}_i^F = False]), where hat{z}^T and hat{z}^F are model outputs paired with the true and false statements respectively.
- `TPR` — range: percent
  - True-statement hit rate: Pr(z_hat = True | z = True). Measures the probability the model correctly affirms a true statement.
- `TNR` — range: percent
  - False-statement rejection rate: Pr(z_hat = False | z = False). Measures the probability the model correctly rejects a false statement.
- `YesBias` — range: percent
  - False-to-True misjudgment probability: Pr(z_hat = True | z = False). Measures the tendency to incorrectly accept false statements.

## Input / output format

**Input**: Binaural audio clip paired with a motion-related question (multiple-choice with 4 options or a true/false statement describing a motion trajectory).

**Output**: Canonical labels: A–D for multiple-choice questions, or TRUE/FALSE for true/false questions.

## Scoring recipe

```python
def compute_metrics(preds, golds, tf_true_preds, tf_false_preds, tf_golds):
    # Overall Accuracy
    accuracy = sum(1 for p, g in zip(preds, golds) if p == g) / len(golds)
    # Acc-MCQ (subset of preds/golds)
    acc_mcq = sum(1 for p, g in zip(mcq_preds, mcq_golds) if p == g) / len(mcq_golds)
    # Acc-T/F
    acc_tf = (sum(1 for p, g in zip(tf_true_preds, tf_true_golds) if p == g) +
              sum(1 for p, g in zip(tf_false_preds, tf_false_golds) if p == g)) / (2 * len(golds))
    # TPR, TNR, YesBias
    n_true = sum(1 for g in tf_golds if g == 'True')
    n_false = sum(1 for g in tf_golds if g == 'False')
    tpr = sum(1 for p, g in zip(tf_preds, tf_golds) if p == 'True' and g == 'True') / n_true
    tnr = sum(1 for p, g in zip(tf_preds, tf_golds) if p == 'False' and g == 'False') / n_false
    yes_bias = sum(1 for p, g in zip(tf_preds, tf_golds) if p == 'True' and g == 'False') / n_false
    return accuracy, acc_mcq, acc_tf, tpr, tnr, yes_bias
```

## Common pitfalls

- Models may rely on superficial spectral or linguistic cues rather than robust spatial representations, leading to chance-level performance.
- Near-constant accuracy across SNR levels does not indicate robustness to acoustic degradation, but rather failure to leverage spatial cues that deteriorate in noise.
- Chance-level baselines (25% for 4-way MCQ, 50% for balanced T/F) indicate a lack of genuine discriminative ability in spatial auditory reasoning.

## Evidence (verbatim from paper)

> Responses are normalized into canonical labels (A–D or TRUE/FALSE) using a rule-based parser, and any unrecognized output is counted as incorrect. Accuracy is averaged over three random seeds and across all task variants, following standard benchmark evaluation.

## Citation

```bibtex
@misc{sun2025audiomotionbench,
  title={Spatial Blind Spot: Auditory Motion Perception Deficits in Audio LLMs},
  author={Sun et al. (2025)},
  year={2025},
  note={arXiv:2511.13273}
}
```

- arXiv: 2511.13273
