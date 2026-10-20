---
name: action-prediction-eval
description: Tests translating a user's natural language command into a structured executable action (function, arguments, status) for GUI interaction. It bridges high-level intent with precise, structured API-like calls. Use when the user wants to benchmark on GUI-360°-Bench, or asks about evaluating this task. Reports Step success rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.04307
  bibtex_key: mu2025gui360
  confidence: high
---

# action-prediction-eval

> GUI-360$^\circ$: A Comprehensive Dataset and Benchmark for Computer-Using Agents — Jian Mu et al. (2025) (arXiv:2511.04307, 2025)

## What this evaluates

Tests translating a user's natural language command into a structured executable action (function, arguments, status) for GUI interaction. It bridges high-level intent with precise, structured API-like calls.

## Datasets

- **GUI-360°-Bench** — total ?; splits: train (-1), test (-1)

## Metrics

- `Step success rate` **(primary)** — range: [0, 1]
  - Proportion of steps where the predicted function, arguments, and status flag all exactly match the ground truth simultaneously.
- `Function accuracy` — range: [0, 1]
  - Proportion of predictions where the predicted function type exactly matches the ground-truth function.
- `Argument accuracy` — range: [0, 1]
  - Conditional accuracy on arguments: coordinates must fall in GT bbox for spatial actions, or exact match for text/symbolic arguments.
- `Status accuracy` — range: [0, 1]
  - Proportion of predictions where the predicted status flag (continue/finish) matches the ground truth.

## Input / output format

**Input**: Natural language command + current GUI state. Evaluated in two settings: visual-only (screenshot) or visual+a11y (screenshot + accessibility metadata).

**Output**: Structured action call comprising a function type, a set of arguments (e.g., coordinates, text values), and a status flag (continue or finish).

## Scoring recipe

```python
def compute_step_success(predictions, ground_truths):
    correct = 0
    for pred, gt in zip(predictions, ground_truths):
        func_ok = pred.func == gt.func
        status_ok = pred.status == gt.status
        args_ok = check_args_match(pred.args, gt.args, gt.func)
        if func_ok and status_ok and args_ok:
            correct += 1
    return correct / len(predictions)

def check_args_match(pred_args, gt_args, func_type):
    if func_type in spatial_actions:
        return is_inside(pred_args.coord, gt_args.box)
    return pred_args == gt_args
```

## Common pitfalls

- Visual-only setting yields extremely low accuracy (<20%); models heavily rely on accessibility metadata for high performance.
- SFT benefits diminish when a11y information is provided, as the metadata already encodes structural alignment that SFT would otherwise learn.

## Evidence (verbatim from paper)

> The evaluation of action prediction is more nuanced than grounding, since each action step is composed of a function, a set of arguments, and a status flag (continue or finish). We therefore report three component accuracies and one aggregated metric... Step success rate (Acc_step): a step is considered correct only if all three components (function, arguments, status) are correct simultaneously.

## Citation

```bibtex
@misc{mu2025gui360,
  title={GUI-360$^\circ$: A Comprehensive Dataset and Benchmark for Computer-Using Agents},
  author={Jian Mu et al. (2025)},
  year={2025},
  note={arXiv:2511.04307}
}
```

- arXiv: 2511.04307
