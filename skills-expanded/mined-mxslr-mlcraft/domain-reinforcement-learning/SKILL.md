---
name: domain-reinforcement-learning
description: "Use for reinforcement learning and sequential decision making: game or control agents, robotics, continuous or discrete control, offline RL from logged data, and contextual bandits. Picks the algorithm by setting, defines reward and state carefully, and evaluates with proper multi-seed protocol. For aligning an LLM (RLHF) use domain-nlp-llm. Triggers on 'reinforcement learning', 'RL agent', 'policy', 'reward', 'control', 'robotics', 'game playing', 'PPO', 'DQN', 'bandit'."
---

# Reinforcement Learning - Method Selection

A good simulator or a solid logged dataset is a prerequisite. Define reward, state, action, and episode boundaries carefully before choosing an algorithm.

## Decision table
| Setting | Recommended | Notes |
|---|---|---|
| Discrete actions, online | DQN family (Rainbow), or PPO | experience replay and target networks stabilize DQN. |
| Continuous control, online | SAC (off-policy, sample-efficient) or PPO (on-policy, stable) | SAC when interactions are expensive; PPO when parallel simulation is cheap. |
| Learn from a fixed logged dataset (no simulator) | Offline RL: CQL or IQL | do not use vanilla off-policy methods offline, they overestimate. |
| Simple contextual decisions, no long horizon | contextual bandits (LinUCB, Thompson sampling) | when there is no long-term credit assignment. |

## Cross-cutting practice
- Reward shaping strongly affects behavior. Guard against reward hacking.
- Evaluation: average return over MANY seeds and episodes, and report mean and variance across seeds because RL is high-variance. Also report sample efficiency (return versus environment steps). For offline RL use off-policy evaluation. Never report a single lucky seed.
- Caveats: sim-to-real gap, instability, and sensitivity to hyperparameters.
- Explainability: value and advantage maps, saliency over states, and recorded policy rollouts or videos.
- Recent directions (2021-2025): Decision Transformer (offline RL as sequence modeling) and Diffusion Policy (expressive policies for robotics). PPO and SAC remain the practical workhorses; reach for the newer methods when they fit offline or multimodal-action settings.
- Improve results: use `accuracy-improvement-loop` (reward shaping, better exploration, or offline pretraining).
