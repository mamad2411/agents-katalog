---
name: androidworld-generalization-eval
description: Probes the zero-shot generalization capability of mobile agents trained via online reinforcement learning across increasingly challenging unseen scenarios in Android environments, including new task instances, UI templates, and entirely new applications. It measures how well learned interaction policies transfer to novel contexts without additional supervised fine-tuning. Use when the user wants to benchmark on AndroidWorld-Generalization, or asks about evaluating this task. Reports Success Rate (SR).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.07432
  bibtex_key: li2026generalization
  confidence: high
---

# androidworld-generalization-eval

> Generalization in Online Reinforcement Learning for Mobile Agents — Li Gu et al. (2026) (arXiv:2603.07432, 2026)

## What this evaluates

Probes the zero-shot generalization capability of mobile agents trained via online reinforcement learning across increasingly challenging unseen scenarios in Android environments, including new task instances, UI templates, and entirely new applications. It measures how well learned interaction policies transfer to novel contexts without additional supervised fine-tuning.

## Datasets

- **AndroidWorld-Generalization** — total ?; splits: test (-1); repo https://github.com/zihuanjiang/AndroidWorld-Generalization

## Metrics

- `Success Rate (SR)` **(primary)** — range: percent
  - Percentage of task instances completed successfully out of the total evaluated instances. Computed as (number of successful trajectories / total trajectories) × 100. A binary reward is assigned only at the final token of each trajectory to determine success.

## Input / output format

**Input**: Task instruction and sequential UI screenshots captured from an Android 13 emulator (API level 33) with 20 pre-installed apps.

**Output**: Discrete action tokens (e.g., click, type, scroll) executed within the Android environment.

## Scoring recipe

```python
def compute_success_rate(predictions, gold):
    # predictions: list of final trajectory outcomes per task
    # gold: list of expected completion status per task
    successful = sum(1 for p, g in zip(predictions, gold) if p == g)
    return (successful / len(gold)) * 100
```

## Common pitfalls

- Evaluation is strictly performed only after full training completes to avoid train-test leakage; querying the test set during training invalidates the generalization metric.
- Many reported baselines use proprietary APIs (e.g., GPT-4o, Claude) and lack public codebases, so their scores are reference points rather than strictly reproducible baselines.
- Few-shot adaptation experiments use non-overlapping instances per unseen app, which changes the data distribution compared to standard zero-shot evaluation.

## Evidence (verbatim from paper)

> All test curves are obtained by evaluating saved checkpoints only after the full training has completed, rather than querying the test set during training. This protocol prevents any train–test leakage and allows an assessment of the gap between training performance and generalization. This approach more than doubles the average success rate, yielding a 26.1% overall improvement with consistent gains across all difficulty levels.

## Citation

```bibtex
@misc{li2026generalization,
  title={Generalization in Online Reinforcement Learning for Mobile Agents},
  author={Li Gu et al. (2026)},
  year={2026},
  note={arXiv:2603.07432}
}
```

- arXiv: 2603.07432
