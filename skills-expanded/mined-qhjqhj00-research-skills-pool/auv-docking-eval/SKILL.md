---
name: auv-docking-eval
description: Evaluates the capability of deep reinforcement learning algorithms to perform continuous docking control of an autonomous underwater vehicle (AUV) in a physics-based simulator. It probes the agent's ability to navigate from random initial positions to a target docking station while optimizing a physics-informed reward function that accounts for proximity, orientation, and contact dynamics. Use when the user wants to benchmark on UUV Simulator (DeepLeng AUV model), or asks about evaluating this task. Reports average episodic return.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2108.02665
  bibtex_key: patil2021deeprl
  confidence: high
---

# auv-docking-eval

> Deep Reinforcement Learning for Continuous Docking Control of Autonomous Underwater Vehicles: A Benchmarking Study — Patil et al. (2021) (arXiv:2108.02665, 2021)

## What this evaluates

Evaluates the capability of deep reinforcement learning algorithms to perform continuous docking control of an autonomous underwater vehicle (AUV) in a physics-based simulator. It probes the agent's ability to navigate from random initial positions to a target docking station while optimizing a physics-informed reward function that accounts for proximity, orientation, and contact dynamics.

## Datasets

- **UUV Simulator (DeepLeng AUV model)** — total ?; splits: (unstated); repo https://github.com/uuvsimulator/uuv_simulator

## Metrics

- `average episodic return` **(primary)** — range: other
  - The sum of rewards collected over a single episode, averaged across multiple evaluation runs. Used as the main performance indicator for policy quality.
- `success rate` — range: percent
  - The number of episodes where the AUV successfully reaches the docking station out of the total evaluation episodes.
- `average steps to goal` — range: other
  - The average number of timesteps required by the agent to reach the goal pose from a random starting point.

## Input / output format

**Input**: Continuous state vector of the AUV (position, orientation, velocity) and docking station coordinates in a 2D x-y workspace. Initial states are sampled uniformly from a 9m square around the docking station.

**Output**: Continuous control actions (thruster forces/torques) applied to the AUV at each timestep.

## Scoring recipe

```python
def evaluate_policy(policy, env, num_episodes=10, max_steps=150):
    returns = []
    successes = 0
    steps_list = []
    for _ in range(num_episodes):
        obs = env.reset()  # Random start in 9m square
        done = False
        steps = 0
        episode_return = 0
        while not done and steps < max_steps:
            action = policy(obs)
            obs, reward, done, info = env.step(action)
            episode_return += reward
            steps += 1
            if info['docked']:
                successes += 1
                break
        returns.append(episode_return)
        steps_list.append(steps)
    return {
        'avg_return': np.mean(returns),
        'success_rate': successes / num_episodes,
        'avg_steps': np.mean(steps_list)
    }
```

## Common pitfalls

- Episodes are capped at 150 timesteps; failure to dock within this limit counts as failure regardless of trajectory quality.
- Evaluation is conducted over only 10 episodes (2 runs of 5), which may not robustly capture performance variance across the full initial state distribution.
- Comparing average episodic returns across different reward formulations (e.g., R_continuous vs R_anderlini) can be misleading if reward scaling or velocity penalties differ significantly.

## Evidence (verbatim from paper)

> In this work, we evaluate 3 state-of-the-art DRL algorithms, namely proximal policy optimization (PPO), twin delayed deep deterministic policy gradients (TD3) and soft actor-critic (SAC), using metrics such as average episodic rewards, average steps required to reach the docking station, success rate as well as demonstrations of the learned policies.

## Citation

```bibtex
@misc{patil2021deeprl,
  title={Deep Reinforcement Learning for Continuous Docking Control of Autonomous Underwater Vehicles: A Benchmarking Study},
  author={Patil et al. (2021)},
  year={2021},
  note={arXiv:2108.02665}
}
```

- arXiv: 2108.02665
