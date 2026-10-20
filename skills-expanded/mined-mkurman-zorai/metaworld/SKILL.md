---
name: metaworld
description: Robotics multi-task and meta-reinforcement learning benchmark (Meta-World). Standardized continuous-control benchmark built on Gymnasium with MT1, MT10, MT50 multi-task suites and ML1, ML10, ML45 meta-learning suites. Supports synchronous and asynchronous vector execution. Use for robotic manipulation benchmarking, multi-task RL, meta-RL adaptation, and evaluating generalization across tasks and goals.
license: MIT license
tags: [robotic-manipulation, multi-task-rl, meta-rl, continuous-control, metaworld]
metadata:
    skill-author: K-Dense Inc.
--------|---------|------|
| `MT1` | Multi-task learning on one selected task family | 1 task |
| `MT10` | Multi-task learning across 10 manipulation tasks | 10 tasks |
| `MT50` | Broad multi-task benchmark | 50 tasks |
| `ML1-train/test` | Meta-learning goal variation within one task family | 1 family |
| `ML10-train/test` | Meta-learning across train/test task split | 10 train + 5 test |
| `ML45-train/test` | Large-scale meta-learning split | 45 train + 5 test |

### 4. Multi-Task Benchmarks

**MT1:**
```python
import gymnasium as gym
import metaworld

env = gym.make("Meta-World/MT1", env_name="reach-v3", seed=42)
obs, info = env.reset()
action = env.action_space.sample()
obs, reward, terminated, truncated, info = env.step(action)
```

**MT10 synchronous vectorized:**
```python
import gymnasium as gym
import metaworld

envs = gym.make_vec("Meta-World/MT10", vector_strategy="sync", seed=42)
obs, info = envs.reset()
actions = envs.action_space.sample()
obs, rewards, terminations, truncations, infos = envs.step(actions)
```

**MT10 asynchronous vectorized:**
```python
envs = gym.make_vec("Meta-World/MT10", vector_strategy="async", seed=42)
```

**MT50:**
```python
envs = gym.make_vec("Meta-World/MT50", vector_strategy="sync", seed=42)
```

### 5. Meta-Learning Benchmarks

**ML1:**
```python
import gymnasium as gym
import metaworld

train_env = gym.make("Meta-World/ML1-train", env_name="reach-v3", seed=42)
test_env = gym.make("Meta-World/ML1-test", env_name="reach-v3", seed=42)
```

**ML10 / ML45:**
```python
train_envs = gym.make_vec("Meta-World/ML10-train", vector_strategy="sync", seed=42)
test_envs = gym.make_vec("Meta-World/ML10-test", vector_strategy="sync", seed=42)

train_envs = gym.make_vec("Meta-World/ML45-train", vector_strategy="async", seed=42)
test_envs = gym.make_vec("Meta-World/ML45-test", vector_strategy="async", seed=42)
```

### 6. Custom Benchmarks

Build your own custom multi-task or meta-learning benchmark:

```python
import gymnasium as gym
import metaworld

envs = gym.make_vec(
    "Meta-World/custom-mt-envs",
    vector_strategy="sync",
    envs_list=["reach-v3", "push-v3", "drawer-open-v3"],
    seed=42,
)

meta_envs = gym.make_vec(
    "Meta-World/custom-ml-envs",
    vector_strategy="async",
    envs_list=["reach-v3", "push-v3", "window-open-v3"],
    seed=42,
)
```

### 7. Observation Semantics

- Multi-task environments append one-hot task IDs for task-conditioned policies.
- Meta-learning environments are partially observable to force adaptation.
- Action spaces are continuous control, suitable for PPO/SAC/TD3-style algorithms.

### 8. Typical Training Patterns

**Single-task SAC / PPO:**
```python
env = gym.make("Meta-World/MT1", env_name="drawer-open-v3")
# Train with Stable-Baselines3 SAC/PPO or CleanRL continuous-control PPO
```

**Task-conditioned multi-task policy:**
```python
envs = gym.make_vec("Meta-World/MT10", vector_strategy="sync")
# Use policy network with task ID appended to observation
# Shared backbone + task-conditioned policy/value heads is common
```

**Meta-RL loop:**
```python
# Train on ML10-train, evaluate fast adaptation on ML10-test
# Measure reward after K adaptation episodes/gradient steps
```

### 9. Evaluation Recommendations

- Report mean success rate and mean return, not only reward.
- Separate train-task and held-out test-task performance for meta-RL.
- Fix seeds and benchmark version for comparability.
- Use sync mode for lower resource usage; async for more throughput.
- Document task subsets if using custom benchmarks.

### 10. Integration Notes

- API follows Gymnasium exactly.
- Works naturally with SB3 continuous-control algorithms and custom PyTorch loops.
- Often paired with SAC, PPO, PEARL, MAML-style meta-RL, and task-conditioned transformers.

## Key Patterns

1. **Use `MT10/MT50` for multi-task RL** and `ML10/ML45` for meta-RL.
2. **Task IDs in MT benchmarks matter** — exploit them in your policy architecture.
3. **Meta-learning benchmarks require separate train/test envs** by design.
4. **Async vectorization improves throughput** but increases process overhead.
5. **Custom benchmark subsets are valuable** for targeted ablations.

## References

- [Meta-World Documentation](https://metaworld.farama.org)
- [Benchmark paper / Meta-World+](https://openreview.net/forum?id=1de3azE606)
- [Farama Meta-World repository](https://github.com/Farama-Foundation/Metaworld)
