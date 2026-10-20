---
name: androidcontrol-eval
description: Evaluates the ability of UI control agents to execute mobile app tasks by predicting correct actions given textual screen representations and instruction history. It probes in-domain and out-of-domain generalization, and measures how model performance scales with the volume of training demonstrations. Use when the user wants to benchmark on AndroidControl, or asks about evaluating this task. Reports step-wise accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2406.03679
  bibtex_key: li2024effectsofdatascale
  confidence: high
---

# androidcontrol-eval

> On the Effects of Data Scale on UI Control Agents — Wei Li et al. (2024) (arXiv:2406.03679, 2024)

## What this evaluates

Evaluates the ability of UI control agents to execute mobile app tasks by predicting correct actions given textual screen representations and instruction history. It probes in-domain and out-of-domain generalization, and measures how model performance scales with the volume of training demonstrations.

## Datasets

- **AndroidControl** — total 15283; splits: train (13604), test (500), ood_app_unseen (-1), ood_task_unseen (-1), ood_categ_unseen (-1); repo https://github.com/google-research/google-research

## Metrics

- `step-wise accuracy` **(primary)** — range: percent
  - Measures the success rate of individual task steps. A step is counted as successful if the predicted action type and its arguments (target UI element and text, if applicable) are correct. Uses a relaxed matching convention where semantically equivalent actions are treated as correct, not just exact string matches.

## Input / output format

**Input**: Natural language task instruction(s) (either high-level only or high-level plus low-level), a textual description of the current screen derived from the Android accessibility tree (filtered to elements with non-empty text or critical types), and a history of previously executed actions.

**Output**: A predicted action type (e.g., click, type, scroll, open_app, terminate) and its required arguments (target UI element, text to type, app name, scroll direction).

## Scoring recipe

```python
def compute_step_accuracy(predictions, golds):
    correct = 0
    for pred, gold in zip(predictions, golds):
        if pred.action_type != gold.action_type:
            continue
        # Relaxed matching for arguments (target element, text)
        if args_match_relaxed(pred.args, gold.args):
            correct += 1
    return (correct / len(golds)) * 100
```

## Common pitfalls

- Confusing the high-level (HL) and low-level (LL) instruction setups: HL prompts only contain the high-level instruction, while LL prompts include both high-level and low-level instructions, which significantly impacts performance.
- Assuming exact string matching is required: The evaluation explicitly uses a relaxed metric where equivalent actions count as correct, so strict exact-match evaluation will underestimate performance.
- Overlooking the terminate action: The agent must predict a terminate action when a task is complete or infeasible. This action is artificially inserted at the end of training episodes but must be correctly predicted during evaluation to properly terminate tasks.

## Evidence (verbatim from paper)

> As in prior work*[[43], [27]]*, as our evaluation metric we adopt step-wise accuracy, which measures the success of each task step. A step is successful if the predicted action and arguments (target element and text, if present) are correct. We adopt a relaxed metric that considers equivalent actions in additions to exact matches as successful (see Appendix[D.3] for details).

## Citation

```bibtex
@misc{li2024effectsofdatascale,
  title={On the Effects of Data Scale on UI Control Agents},
  author={Wei Li et al. (2024)},
  year={2024},
  note={arXiv:2406.03679}
}
```

- arXiv: 2406.03679
