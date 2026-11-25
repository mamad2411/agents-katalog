---
name: agentdb-learn
description: Train one of AgentDB's 9 RL algorithms on a stream of episodes. Use when the user has accumulated successful/failed episodes and wants to derive a policy, or when a task type is repeated enough to benefit from RL routing.
---

# Learn

Train an RL agent on episode data to derive a policy.

## When to use

- Repeated task type with measurable reward and 50+ episodes
- User asks to "train", "build a policy", "make it learn"
- Pre-deployment of an autonomous agent that should pick actions itself

## Algorithms (the bandit picks the right one)

| Algo | Best for |
|---|---|
| **Q-Learning** | Tabular state-spaces, discrete actions |
| **SARSA** | On-policy variant, conservative exploration |
| **DQN** | High-dimensional state, neural Q-fn |
| **PPO** | Continuous control, high-dim action |
| **Actor-Critic** | Baseline reduction, stable training |
| **Policy Gradient** | Direct policy parameterization |
| **Decision Transformer** | Offline RL on trajectories |
| **MCTS** | Tree-search planning under known dynamics |
| **Model-Based RL** | Sample-efficient when env model is learnable |

If you don't know which to pick, call `agentdb_learning_route` first — the bandit suggests one based on past performance on similar task signatures.

## API

```
agentdb_learning_train(
  algorithm:   <one of above>           // or 'auto' to let bandit pick
  episodes:    [<episodeId>, ...]       // or task name → fetch automatically
  hyperparams: { lr, gamma, epsilon, ... }
  iterations:  N
)
```

## After training

1. The bandit logs the resulting reward distribution on the chosen algorithm.
2. The trained model is stored in the AgentDB skill library as a callable skill.
3. Future calls to `agentdb_learning_route(task)` may pick this trained skill if it scores well.

## Don't

- Don't train on < 50 episodes — high-variance models overfit.
- Don't train multiple algorithms in parallel "to see which wins" — that's the bandit's job, and parallel training pollutes the reward signal.
- Don't ignore the route output. If `agentdb_learning_route` says "no algorithm has > 0.6 expected reward on this task", the answer is to gather more episodes, not to force-train.
