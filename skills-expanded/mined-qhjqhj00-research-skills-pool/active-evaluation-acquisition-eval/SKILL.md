---
name: active-evaluation-acquisition-eval
description: Evaluates the effectiveness of active learning policies in selecting a minimal subset of prompts to accurately predict an LLM's overall benchmark score, thereby reducing evaluation costs while maintaining predictive fidelity. Use when the user wants to benchmark on HuggingFace Open LLM Leaderboard, MMLU, HELM-Lite, AlpacaEval 2.0, Chatbot Arena, or asks about evaluating this task. Reports absolute differences.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2410.05952
  bibtex_key: li2024activeevaluationacquisition
  confidence: high
---

# active-evaluation-acquisition-eval

> Active Evaluation Acquisition for Efficient LLM Benchmarking — Yang Li et al. (arXiv:2410.05952, 2024)

## What this evaluates

Evaluates the effectiveness of active learning policies in selecting a minimal subset of prompts to accurately predict an LLM's overall benchmark score, thereby reducing evaluation costs while maintaining predictive fidelity.

## Datasets

- **HuggingFace Open LLM Leaderboard** — total 28659; splits: train (-1), test (-1)
- **MMLU** — total 14042; splits: train (-1), test (-1)
- **HELM-Lite** — total 13021; splits: train (-1), test (-1)
- **AlpacaEval 2.0** — total 805; splits: train (-1), test (-1)
- **Chatbot Arena** — total 80; splits: train (-1), test (-1)

## Metrics

- `absolute differences` **(primary)** — range: absolute value
  - The absolute difference between the predicted benchmark score and the actual benchmark score. The benchmark score is computed as a weighted average across its constituent datasets.

## Input / output format

**Input**: Prompt text, prompt embeddings, and observed evaluation scores for a subset of prompts per model.

**Output**: Predicted overall benchmark score and the selected subset of prompts for acquisition.

## Scoring recipe

```python
def compute_metric(predicted_scores, actual_scores):
    # Compute per-dataset scores
    pred_dataset_scores = neural_process.predict(unobserved_prompts)
    actual_dataset_scores = get_ground_truth(unobserved_prompts)
    # Aggregate to benchmark level
    pred_benchmark = weighted_average(pred_dataset_scores)
    actual_benchmark = weighted_average(actual_dataset_scores)
    # Metric
    return abs(pred_benchmark - actual_benchmark)
```

## Common pitfalls

- Model bias: Training on proprietary models and testing on open-source models (or vice versa) increases estimation error due to capability distribution shifts.
- Cold-start failure: Score-dependent policies (e.g., Clustering-Score) cannot acquire prompts from withheld subsets, leading to poor performance.
- Static policies optimized on training models often fail to generalize to new models due to distribution shift, requiring dynamic acquisition.

## Evidence (verbatim from paper)

> The final score for each benchmark is computed as a weighted average across datasets, and we report the absolute differences between the predicted scores and the actual scores.

## Citation

```bibtex
@misc{li2024activeevaluationacquisition,
  title={Active Evaluation Acquisition for Efficient LLM Benchmarking},
  author={Yang Li et al.},
  year={2024},
  note={arXiv:2410.05952}
}
```

- arXiv: 2410.05952
