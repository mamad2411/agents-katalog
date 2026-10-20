---
name: amo-bench-eval
description: Evaluates large language models' ability to solve high school and IMO-level mathematics competition problems. It probes complex mathematical reasoning, problem-solving under strict constraints, and the model's capacity to scale reasoning effort with test-time compute. Use when the user wants to benchmark on AMO-Bench, or asks about evaluating this task. Reports AVG@32.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.26768
  bibtex_key: an2025amo_bench
  confidence: high
---

# amo-bench-eval

> AMO-Bench: Large Language Models Still Struggle in High School Math Competitions — An et al. (2025) (arXiv:2510.26768, 2025)

## What this evaluates

Evaluates large language models' ability to solve high school and IMO-level mathematics competition problems. It probes complex mathematical reasoning, problem-solving under strict constraints, and the model's capacity to scale reasoning effort with test-time compute.

## Datasets

- **AMO-Bench** — total 50; splits: test (50)

## Metrics

- `AVG@32` **(primary)** — range: [0, 1]
  - The average accuracy across 32 independent sampling runs for each model. Accuracy per run is computed as the fraction of problems where the model's final answer matches the ground truth via parser-based exact match.

## Input / output format

**Input**: A single high school or IMO-level mathematics competition problem presented as text.

**Output**: The model's generated reasoning steps and final answer. For evaluation, only the final answer is extracted and compared against the ground truth using a parser.

## Scoring recipe

```python
def compute_avg32(predictions_32_runs, gold_answers):
    accuracies = []
    for run_outputs in predictions_32_runs:
        correct = 0
        for pred, gold in zip(run_outputs, gold_answers):
            if extract_final_answer(pred) == gold:
                correct += 1
        accuracies.append(correct / len(gold_answers))
    return sum(accuracies) / len(accuracies)
```

## Common pitfalls

- AVG@32 is the mean of per-run accuracies, not the accuracy of a single generation or an average of token counts.
- Sampling hyperparameters differ by model type: temperature=1.0 for reasoning models vs. 0.7 for non-reasoning models, which affects direct performance comparisons.
- Grading relies strictly on parser-based exact match of the final answer; partial credit or step-by-step verification is not applied.

## Evidence (verbatim from paper)

> To ensure the stability of the final evaluation results, we sampled the results from each model 32 times and reported the average performance of these 32 results as the final metric (denoted as AVG@32). We set the temperature of sampling to 1.0 for reasoning models and 0.7 for non-reasoning models. For all evaluated models, we use top-k=50 and top-p=0.95 during sampling.

## Citation

```bibtex
@misc{an2025amo_bench,
  title={AMO-Bench: Large Language Models Still Struggle in High School Math Competitions},
  author={An et al. (2025)},
  year={2025},
  note={arXiv:2510.26768}
}
```

- arXiv: 2510.26768
