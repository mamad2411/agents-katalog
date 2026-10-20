---
name: alfred-eval
description: Embodied instruction following in a simulated household environment, requiring an agent to execute long-horizon navigation and object manipulation tasks based on natural language commands. Use when the user wants to benchmark on ALFRED, or asks about evaluating this task. Reports Success Rate (SR).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2211.03267
  bibtex_key: inoue2022prompter
  confidence: medium
---

# alfred-eval

> Prompter: Utilizing Large Language Model Prompting for a Data Efficient Embodied Instruction Following — Inoue et al. (2022) (arXiv:2211.03267, 2022)

## What this evaluates

Embodied instruction following in a simulated household environment, requiring an agent to execute long-horizon navigation and object manipulation tasks based on natural language commands.

## Datasets

- **ALFRED** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `Success Rate (SR)` **(primary)** — range: percent
  - Percentage of episodes where the agent successfully completes the instructed task within the step limit and without exceeding the bad interaction threshold.

## Input / output format

**Input**: Natural language instructions (high-level or step-by-step) and visual observations from the AI2-THOR simulator at each time step.

**Output**: One discrete action per step: 5 navigation actions (RotateRight, RotateLeft, MoveAhead, LookUp, LookDown) or 7 object interaction actions (PickupObject, PutObject, OpenObject, CloseObject, ToggleObjectOn, ToggleObjectOff, SliceObject) accompanied by an image mask specifying the interaction target location.

## Scoring recipe

```python
def compute_sr(predictions, gold):
    successes = 0
    for pred, gold_inst in zip(predictions, gold):
        steps = 0
        bad_interactions = 0
        finished = False
        for action in pred:
            steps += 1
            if action == 'bad_interaction': bad_interactions += 1
            if action == 'task_complete': finished = True; break
        if finished and steps <= 1000 and bad_interactions < 10:
            successes += 1
    return (successes / len(predictions)) * 100
```

## Common pitfalls

- Confusing high-level instructions with step-by-step instructions, which are evaluated separately.
- Ignoring the discrete constraints on navigation actions (90° rotations, 25cm moves, 15° looks) and the requirement for image masks during object interaction.
- Failing to account for the episode termination conditions: 1000-step limit or 10 bad interactions (collisions, non-interactive objects).

## Evidence (verbatim from paper)

> At each time step, an agent makes one action from five navigation actions (RotateRight, RotateLeft, MoveAhead, LookUp, LookDown) or seven object interaction actions (PickupObject, PutObject, OpenObject, CloseObject, ToggleObjectOn, ToggleObjectOff, SliceObject). ... An episode ends when the task is finished, 1000 steps are taken, or 10 bad interactions (*e.g*. collisions, interacting with non-interactive object) occur.

## Citation

```bibtex
@misc{inoue2022prompter,
  title={Prompter: Utilizing Large Language Model Prompting for a Data Efficient Embodied Instruction Following},
  author={Inoue et al. (2022)},
  year={2022},
  note={arXiv:2211.03267}
}
```

- arXiv: 2211.03267
