---
name: aitw-eval
description: Evaluates an agent's ability to infer and execute multi-step visual actions on Android devices from natural language instructions. It specifically probes Out-of-Distribution generalization across unseen Android OS versions, instruction language patterns (subjects/verbs), and app/web domains. Use when the user wants to benchmark on AITW, or asks about evaluating this task. Reports average score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2307.10088
  bibtex_key: rawles2023androidinthewild
  confidence: high
---

# aitw-eval

> Android in the Wild: A Large-Scale Dataset for Android Device Control — Rawles et al. (2023) (arXiv:2307.10088, 2023)

## What this evaluates

Evaluates an agent's ability to infer and execute multi-step visual actions on Android devices from natural language instructions. It specifically probes Out-of-Distribution generalization across unseen Android OS versions, instruction language patterns (subjects/verbs), and app/web domains.

## Datasets

- **AITW** — total ?; splits: train (-1), val (-1), test (-1); repo https://github.com/google-research/google-research

## Metrics

- `average score` **(primary)** — range: percent
  - Percentage of successfully completed episodes. Evaluated separately for each dataset/task type, then averaged across all datasets to account for differing sizes.

## Input / output format

**Input**: Natural language instruction and raw screen observations (UI screenshots) from an Android device.

**Output**: Sequence of device actions/gestures (e.g., taps, swipes, text input) to execute the requested task.

## Scoring recipe

```python
def compute_average_score(predictions, gold, datasets):
    dataset_scores = []
    for ds in datasets:
        correct = sum(1 for p, g in zip(predictions[ds], gold[ds]) if is_episode_success(p, g))
        dataset_scores.append(correct / len(predictions[ds]))
    return (sum(dataset_scores) / len(dataset_scores)) * 100
```

## Common pitfalls

- Splitting by exact instruction match instead of using extracted subject/verb templates, which leaks similar language patterns into the test set.
- Mixing Android versions in the test split, violating the protocol that reserves Android 13 exclusively for testing.
- Averaging scores across datasets without evaluating each dataset separately first, as instructed due to differing dataset sizes.

## Evidence (verbatim from paper)

> We randomly split each dataset (the four multi-step datasets and SINGLE) episode wise into a training, validation, and test set $(80 / 10 / 10\%)$. Because the datasets different sizes, we evaluate each of them separately, then take the average score across them; we do the same for OOD setups.

## Citation

```bibtex
@misc{rawles2023androidinthewild,
  title={Android in the Wild: A Large-Scale Dataset for Android Device Control},
  author={Rawles et al. (2023)},
  year={2023},
  note={arXiv:2307.10088}
}
```

- arXiv: 2307.10088
