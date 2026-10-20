---
name: pettingzoo
description: Multi-agent reinforcement learning environment API (PettingZoo). Standard API for multi-agent RL extending Gymnasium with Agent Environment Cycle (AEC) and Parallel APIs. Includes Atari, Butterfly, Classic, MPE, and SISL environments. For single-agent RL, use Gymnasium. For algorithm implementations, use stable-baselines3 or CleanRL.
license: MIT license
tags: [multi-agent-rl, marl-environments, turn-based-games, parallel-envs, pettingzoo]
metadata:
    skill-author: K-Dense Inc.
--------|-----|----------|
| Turn-based games (card, board games) | ✅ Best fit | ❌ Not appropriate |
| Simultaneous action (robotics, MPE) | ⚠️ Works but awkward | ✅ Best fit |
| Compatible with CleanRL | ✅ Via wrappers | ❌ Needs conversion |
| Compatible with SB3 | ❌ Not directly | ❌ Needs conversion |

### 3. Key AEC Methods

```python
# Iterate over agents in turn order
for agent in env.agent_iter():
    # Get the observation/reward for the CURRENT agent
    observation, reward, termination, truncation, info = env.last()

    # Check if the agent is done
    if termination or truncation:
        action = None
    else:
        action = policy(observation, agent)

    # Submit action — this steps the environment AND advances to next agent
    env.step(action)

# After loop: check which agents are still active
print(env.agents)  # List of active agents
```

### 4. Available Environments

| Category | Environments | API Style | Description |
|----------|-------------|-----------|-------------|
| **MPE** | simple_spread, simple_adversary, simple_tag, simple_world_comm | Parallel | Multi-agent particle environments, cooperative/competitive |
| **Atari** | pong, space_invaders, surround, tennis, warlords | Parallel | Multi-agent versions of classic Atari games |
| **Butterfly** | pistonball, cooperative_pong, knights_archers_zombies | Parallel | Cooperative multi-agent games |
| **Classic** | chess, go, rps, backgammon, texas_holdem, tictactoe | AEC | Classic board and card games |
| **SISL** | waterworld, pursuit | Parallel | Multi-agent control tasks |

**List all available:**
```python
from pettingzoo.utils import all_modules
print(all_modules)
```

### 5. Utility Wrappers

```python
from pettingzoo.utils import wrappers

# AEC → Parallel conversion
from pettingzoo.utils.conversions import aec_to_parallel
parallel_env = aec_to_parallel(aec_env)

# Parallel → AEC conversion
from pettingzoo.utils.conversions import parallel_to_aec
aec_env = parallel_to_aec(parallel_env)

# Pad observations for different-sized agents
env = wrappers.PadObservations(env)

# Flatten dict observations
env = wrappers.FlattenObservations(env)
```

### 6. MPE Example — Cooperative Navigation

```python
from pettingzoo.mpe import simple_spread_v3

env = simple_spread_v3.parallel_env(
    N=3,            # Number of agents
    local_ratio=0.5, # How much agents see
    max_cycles=100,
    render_mode="human",
)

observations, infos = env.reset(seed=42)

for cycle in range(100):
    actions = {}
    for agent in env.agents:
        # observations[agent] is the local observation for that agent
        actions[agent] = env.action_space(agent).sample()

    observations, rewards, terminations, truncations, infos = env.step(actions)

    if all(terminations.values()) or all(truncations.values()):
        break

env.close()
```

### 7. Observation and Action Spaces

```python
from pettingzoo.mpe import simple_spread_v3

env = simple_spread_v3.env(N=3)

# Per-agent spaces
for agent in env.possible_agents:
    print(f"{agent} obs: {env.observation_space(agent)}")
    print(f"{agent} act: {env.action_space(agent)}")

# Agent-specific policies
policies = {
    "agent_0": policy_0,
    "agent_1": policy_1,
    "agent_2": policy_2,
}
```

### 8. Multi-Agent Atari

```python
from pettingzoo.atari import pong_v3

env = pong_v3.parallel_env(render_mode="human")
observations, infos = env.reset()

# Two agents: "first_0" and "second_0"
# Each sees the game from their perspective
for agent in env.agents:
    print(env.observation_space(agent))  # Box(210, 160, 3)
    print(env.action_space(agent))       # Discrete(6)
```

### 9. CleanRL Integration

CleanRL has built-in support for multi-agent PettingZoo Atari:
```python
# See: cleanrl/ppo_pettingzoo_ma_atari.py
from cleanrl.ppo_pettingzoo_ma_atari import make_env

envs = make_env("pong_v3", seed=1)
```

### 10. Custom Multi-Agent Environment

```python
from pettingzoo import ParallelEnv
import functools
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class CustomMARLEnv(ParallelEnv):
    metadata = {"name": "custom_marl_v0"}

    def __init__(self, render_mode=None):
        super().__init__()
        self.possible_agents = ["agent_0", "agent_1"]
        self.observation_spaces = {
            a: spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)
            for a in self.possible_agents
        }
        self.action_spaces = {
            a: spaces.Discrete(3) for a in self.possible_agents
        }
        self.render_mode = render_mode

    def reset(self, seed=None, options=None):
        self.agents = self.possible_agents[:]
        self.state = np.zeros(4, dtype=np.float32)
        observations = {a: self.state.copy() for a in self.agents}
        infos = {a: {} for a in self.agents}
        return observations, infos

    def step(self, actions):
        # Apply actions, update state
        for agent, action in actions.items():
            self.state[0] += (action - 1) * 0.1
        self.state = np.clip(self.state, 0, 1)

        rewards = {a: float(self.state[0]) for a in self.agents}
        terminations = {a: False for a in self.agents}
        truncations = {a: False for a in self.agents}
        observations = {a: self.state.copy() for a in self.agents}
        infos = {a: {} for a in self.agents}

        # Remove dead agents
        if self.state[0] > 0.9:
            self.agents = []

        return observations, rewards, terminations, truncations, infos

    def render(self):
        if self.render_mode == "human":
            print(f"State: {self.state}")

    def close(self):
        pass
```

### 11. Supersuit Integration (RL Preprocessing)

```bash
pip install supersuit
```

```python
from pettingzoo.atari import space_invaders_v2
from supersuit import (
    resize_v1, frame_skip_v0, frame_stack_v1,
    color_reduction_v0, dtype_v0, pettingzoo_env_to_vec_env_v1,
)

env = space_invaders_v2.parallel_env()
env = resize_v1(env, (84, 84))
env = frame_skip_v0(env, 4)
env = frame_stack_v1(env, 4)
# Convert to Gymnasium VecEnv for SB3/CleanRL compat
env = pettingzoo_env_to_vec_env_v1(env)
```

## Key Patterns

1. **Use AEC API for turn-based games** (chess, poker) — sequential logic is natural
2. **Use Parallel API for simultaneous actions** (MPE, multi-agent Atari)
3. **Always check `env.agents`** — it changes as agents are added/removed
4. **Use `env.observation_space(agent)` and `env.action_space(agent)`** — they can differ per agent
5. **Supersuit provides RL-ready preprocessing** — frame stack, resize, skip
6. **PettingZoo uses Gymnasium under the hood** — observation/action spaces are from `gymnasium.spaces`

## References

- [PettingZoo Documentation](https://pettingzoo.farama.org/)
- [Environment List](https://pettingzoo.farama.org/environments/)
- [AEC API Tutorial](https://pettingzoo.farama.org/api/aec/)
- [Parallel API Tutorial](https://pettingzoo.farama.org/api/parallel/)
- [Supersuit](https://github.com/Farama-Foundation/SuperSuit) — RL preprocessing wrappers
