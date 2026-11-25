---
name: arbibench-eval
description: Evaluates the adversarial robustness of binarized neural networks (BNNs) against white-box and black-box attacks. It measures how well BNNs maintain prediction accuracy under controlled perturbation budgets compared to their clean accuracy, highlighting robustness trends across dataset scales. Use when the user wants to benchmark on CIFAR-10, ImageNet, or asks about evaluating this task. Reports ACC_norm.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2312.13575
  bibtex_key: zhao2023arbibench
  confidence: high
---

# arbibench-eval

> ARBiBench: Benchmarking Adversarial Robustness of Binarized Neural Networks — Peng Zhao et al. (arXiv:2312.13575, 2023)

## What this evaluates

Evaluates the adversarial robustness of binarized neural networks (BNNs) against white-box and black-box attacks. It measures how well BNNs maintain prediction accuracy under controlled perturbation budgets compared to their clean accuracy, highlighting robustness trends across dataset scales.

## Datasets

- **CIFAR-10** — total ?; splits: test (-1)
- **ImageNet** — total ?; splits: test (-1)

## Metrics

- `ACC_norm` **(primary)** — range: [0, 1]
  - Normalized adversarial accuracy, calculated as ACC* / ACC. It measures relative robustness by dividing adversarial accuracy by clean accuracy, allowing fair comparison across models with different baseline performance.
- `RS` — range: [0, N]
  - Robustness Score, defined as the sum of normalized adversarial accuracy across N attack methods: RS = sum(ACC_norm^i). The text describes it as a mean but provides a summation formula.
- `ACC` — range: [0, 1]
  - Clean accuracy: ACC = (1/N) * sum(1(C(x_i) = y_i)).
- `ACC*` — range: [0, 1]
  - Adversarial accuracy: ACC* = (1/N) * sum(1(C(A_{epsilon,p}(x_i)) = y_i)).

## Input / output format

**Input**: Image samples $x_i$ from CIFAR-10 or ImageNet test sets, paired with ground-truth labels $y_i$.

**Output**: Predicted class labels $C(x_i)$ for clean inputs and $C(\mathcal{A}_{\epsilon,p}(x_i))$ for adversarial inputs.

## Scoring recipe

```python
def compute_metrics(clean_preds, adv_preds, labels, num_attacks):
    acc = np.mean(clean_preds == labels)
    acc_star = np.mean(adv_preds == labels)
    acc_norm = acc_star / acc if acc > 0 else 0.0
    # RS aggregates acc_norm across attack methods
    rs = sum(acc_norm for _ in range(num_attacks))
    return acc, acc_star, acc_norm, rs
```

## Common pitfalls

- Using raw adversarial accuracy (ACC*) instead of normalized adversarial accuracy (ACC_norm) to compare models with different clean accuracies, which violates the paper's explicit protocol.
- Confusing evaluation subset sizes: CIFAR-10 uses the full test set for white-box attacks but only 500 images for black-box attacks, while ImageNet uses 1000 images for all attacks.
- Misinterpreting the Robustness Score (RS) formula: the text describes it as a 'mean' but the provided equation uses a summation ($\sum$), leading to incorrect aggregation if not handled carefully.

## Evidence (verbatim from paper)

> The accuracy of the classifier is defined as ACC=1/N sum... For specific adversarial attacks, the accuracy of the classifier against the attack can be calculated with the following expression: ACC*=1/N sum... However, we aim to evaluate the robustness among models with different clean accuracy. We used the normalized adversarial accuracy to measure the relative performance, which is calculated as follows: ACC_norm=ACC*/ACC... We employ the mean of ACC_norm as a Robustness Score (RS) to assess the adversarial robustness (higher values indicate a more robust model): RS=sum ACC_norm^i

## Citation

```bibtex
@misc{zhao2023arbibench,
  title={ARBiBench: Benchmarking Adversarial Robustness of Binarized Neural Networks},
  author={Peng Zhao et al.},
  year={2023},
  note={arXiv:2312.13575}
}
```

- arXiv: 2312.13575
