---
name: ale-60-games-eval
description: This benchmark evaluates reinforcement learning agents across 60 Atari 2600 games using a stochastic environment variant with sticky actions. It measures sample efficiency and learning stability by tracking performance at multiple frame-count thresholds (10M to 200M). Use when the user wants to benchmark on Arcade Learning Environment (ALE), or asks about evaluating this task. Reports score averages.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1709.06009
  bibtex_key: machado2017revisiting
  confidence: high
---

# ale-60-games-eval

> Revisiting the Arcade Learning Environment: Evaluation Protocols and Open Problems for General Agents — Machado et al. (2017) (arXiv:1709.06009, 2017)

## What this evaluates

This benchmark evaluates reinforcement learning agents across 60 Atari 2600 games using a stochastic environment variant with sticky actions. It measures sample efficiency and learning stability by tracking performance at multiple frame-count thresholds (10M to 200M).

## Datasets

- **Arcade Learning Environment (ALE)** — total 60; splits: train (60)

## Metrics

- `score averages` **(primary)** — range: other
  - Average total reward obtained over the final 100 episodes of a trial up to a specified frame limit. Results are averaged across multiple independent trials.

## Input / output format

**Input**: Raw Atari 2600 game frames.

**Output**: Discrete action selection from the game's action space.

## Scoring recipe

```python
def compute_score(trial_episodes, frame_limit):
    relevant = [ep for ep in trial_episodes if ep.frames <= frame_limit]
    last_100 = relevant[-100:]
    return sum(ep.total_reward for ep in last_100) / len(last_100)
# Final metric: mean(compute_score(trial) for trial in trials)
```

## Common pitfalls

- Using the original deterministic ALE dynamics instead of the proposed sticky actions variant, which fundamentally changes the evaluation landscape.
- Reporting results based on a single trial (common in early DQN papers) rather than multiple independent trials, leading to unreliable statistical comparisons.
- Evaluating performance at only one frame count threshold instead of tracking learning progress across multiple milestones (10M, 50M, 100M, 200M).

## Evidence (verbatim from paper)

> We computed score averages of each trial using the 100 final episodes until the specified threshold, including the episode in which the total is exceeded. We report the average over 5 trials for DQN and the average over 24 trials for Sarsa $(\lambda) + \mathrm{Blob - PROST}$ .

## Citation

```bibtex
@misc{machado2017revisiting,
  title={Revisiting the Arcade Learning Environment: Evaluation Protocols and Open Problems for General Agents},
  author={Machado et al. (2017)},
  year={2017},
  note={arXiv:1709.06009}
}
```

- arXiv: 1709.06009
