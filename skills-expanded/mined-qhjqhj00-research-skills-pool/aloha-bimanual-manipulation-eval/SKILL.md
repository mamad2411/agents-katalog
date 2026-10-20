---
name: aloha-bimanual-manipulation-eval
description: This evaluation probes a robot policy's ability to perform precise, temporally extended bimanual manipulation tasks using only visual and proprioceptive inputs. It specifically tests the model's robustness to compounding errors, non-Markovian dynamics, and perception challenges like transparent or low-contrast objects. Use when the user wants to benchmark on ALOHA Fine Manipulation Tasks, or asks about evaluating this task. Reports success rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2304.13705
  bibtex_key: zhao2023learningfinegrained
  confidence: high
---

# aloha-bimanual-manipulation-eval

> Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware — Tony Z. Zhao et al. (2023) (arXiv:2304.13705, 2023)

## What this evaluates

This evaluation probes a robot policy's ability to perform precise, temporally extended bimanual manipulation tasks using only visual and proprioceptive inputs. It specifically tests the model's robustness to compounding errors, non-Markovian dynamics, and perception challenges like transparent or low-contrast objects.

## Datasets

- **ALOHA Fine Manipulation Tasks** — total ?; splits: test (25); repo https://tonyzhaozh.github.io/aloha/

## Metrics

- `success rate` **(primary)** — range: percent
  - The fraction of evaluation trials that successfully complete the entire task sequence. Calculated as (number of successful trials) / (total number of trials).

## Input / output format

**Input**: RGB images from top-down and wrist-mounted cameras, concatenated with current joint positions and robot state.

**Output**: Continuous action vector (e.g., joint velocities or end-effector poses) for the next control timestep.

## Scoring recipe

```python
def compute_success_rate(predictions, gold, n_trials=25):
    successes = 0
    for i in range(n_trials):
        # Run episode using predicted actions against gold environment state
        episode_success = check_episode_completion(predictions[i], gold[i])
        if episode_success:
            successes += 1
    return (successes / n_trials) * 100
```

## Common pitfalls

- Performance drops significantly when switching from scripted to human demonstration data due to stochasticity and multi-modality; results must be reported separately for each data type.
- Success is defined by completing the full multi-stage task (e.g., final insertion or strap securing), not just intermediate subtasks, though subtask rates are also tracked.
- Depth cameras are explicitly noted as ill-suited due to transparent/low-contrast objects; evaluations relying on depth may overestimate difficulty or fail perception.

## Evidence (verbatim from paper)

> As a detailed comparison with prior methods, we report the average success rate in Table I for two simulated and two real tasks. For simulated tasks, we average performance across 3 random seeds with 50 trials each. We report the success rate on both scripted data (left of separation bar) and human data (right of separation bar). For real-world tasks, we run one seed and evaluate with 25 trials.

## Citation

```bibtex
@misc{zhao2023learningfinegrained,
  title={Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware},
  author={Tony Z. Zhao et al. (2023)},
  year={2023},
  note={arXiv:2304.13705}
}
```

- arXiv: 2304.13705
