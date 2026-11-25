---
name: automathtext-math-eval
description: Evaluates the effectiveness of the AutoMathText dataset for continual pretraining by measuring downstream mathematical reasoning performance on the MATH benchmark. It compares models trained on auto-selected high-quality mathematical text versus uniformly sampled filtered text, controlling for token count. Use when the user wants to benchmark on MATH, AutoMathText, or asks about evaluating this task. Reports MATH test accuracy (%).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2402.07625
  bibtex_key: zhang2024automathtext
  confidence: high
---

# automathtext-math-eval

> Autonomous Data Selection with Zero-shot Generative Classifiers for Mathematical Texts — Zhang et al. (2024) (arXiv:2402.07625, 2024)

## What this evaluates

Evaluates the effectiveness of the AutoMathText dataset for continual pretraining by measuring downstream mathematical reasoning performance on the MATH benchmark. It compares models trained on auto-selected high-quality mathematical text versus uniformly sampled filtered text, controlling for token count.

## Datasets

- **MATH** — total ?; splits: test (-1)
- **AutoMathText** — total ?; splits: train (-1)

## Metrics

- `MATH test accuracy (%)` **(primary)** — range: percent
  - Percentage of correctly solved problems on the MATH test set, evaluated using the standard lm-eval-harness framework consistent with the Huggingface Leaderboard protocol.
- `Average training loss` — range: other
  - Mean cross-entropy loss averaged over all tokens during the 3-epoch continual pretraining run.

## Input / output format

**Input**: Mathematical problems from the MATH benchmark test set, processed according to the lm-eval-harness protocol.

**Output**: Predicted answers or solution steps for each math problem, evaluated for correctness per the Huggingface Leaderboard protocol.

## Scoring recipe

```python
# MATH Accuracy
correct = sum(1 for pred, gold in zip(predictions, gold_labels) if is_correct(pred, gold))
accuracy = (correct / len(gold_labels)) * 100

# Training Loss
loss = sum(token_losses) / total_tokens
```

## Common pitfalls

- Token counts must be strictly balanced between uniform and auto-selected baselines to avoid confounding data volume with data quality.
- The uniform baseline is already filtered by OpenWebMath's rule-based filter and classifier, so it does not represent raw unfiltered web text.
- SFT on MetaMathQA significantly boosts baseline accuracy, so pretraining-only gains must be isolated from fine-tuning effects.

## Evidence (verbatim from paper)

> Our evaluation methodology adheres to the standard eval harness framework (Gao et al., 2023b), consistent with the Huggingface Leaderboard’s protocol. The results, as detailed in the tables below, illuminate the efficacy of our AutoMathText dataset in enhancing the model’s performance. Table 2: MATH test accuracy post continual pretraining.

## Citation

```bibtex
@misc{zhang2024automathtext,
  title={Autonomous Data Selection with Zero-shot Generative Classifiers for Mathematical Texts},
  author={Zhang et al. (2024)},
  year={2024},
  note={arXiv:2402.07625}
}
```

- arXiv: 2402.07625
