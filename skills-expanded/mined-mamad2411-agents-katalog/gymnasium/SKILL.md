---
name: gymnasium
description: Standard API for single-agent reinforcement learning environments (Gymnasium). Provides Classic Control, Box2D, Toy Text, MuJoCo, and Atari environments with a unified env.step()/env.reset() interface. For multi-agent RL, use PettingZoo. For algorithm implementations, use stable-baselines3 or CleanRL.
license: MIT license
tags: [single-agent-rl, rl-environments, control-benchmarks, environment-wrappers, gymnasium]
metadata:
    skill-author: K-Dense Inc.
-----|------|---------|
| `observation` | ndarray / dict | Current state observation |
| `reward` | float | Immediate reward |
| `terminated` | bool | Terminal state reached (success/failure) |
| `truncated` | bool | Episode ended by time limit/external signal |
| `info` | dict | Auxiliary diagnostic info |

**Critical distinction:** `terminated` means the MDP ended naturally. `truncated` means it hit a time limit. Both should trigger `reset()`, but your algorithm should handle them differently (no value bootstrap on `terminated`).

### 3. Available Environment Families

| Family | Examples | Install | Use Case |
|--------|----------|---------|----------|
| **Classic Control** | CartPole, MountainCar, Pendulum, Acrobot | `pip install gymnasium` | Algorithm debugging, quick tests |
| **Box2D** | LunarLander, BipedalWalker, CarRacing | `pip install "gymnasium[box2d]"` | Physics-based toy problems |
| **Toy Text** | FrozenLake, Taxi, Blackjack | `pip install gymnasium` | Discrete RL, teaching |
| **MuJoCo** | HalfCheetah, Hopper, Humanoid, Ant | `pip install "gymnasium[mujoco]"` | Continuous control benchmarks |
| **Atari** | Breakout, Pong, SpaceInvaders | `pip install "gymnasium[atari]"` (ALE) | Pixel-based RL, DQN development |

**Install all:**
```bash
pip install "gymnasium[all]"
```

### 4. Observation and Action Spaces

```python
import gymnasium as gym
from gymnasium import spaces

env = gym.make("CartPole-v1")

print(env.observation_space)  # Box([-4.8 ...], [4.8 ...], (4,), float32)
print(env.action_space)        # Discrete(2)

# Check space properties
assert isinstance(env.observation_space, spaces.Box)
print(env.observation_space.shape)   # (4,)
print(env.observation_space.dtype)   # float32
print(env.observation_space.low)     # [-4.8 -inf -0.418 -inf]
print(env.observation_space.high)    # [4.8 inf 0.418 inf]

assert isinstance(env.action_space, spaces.Discrete)
print(env.action_space.n)            # 2
```

### 5. Creating Custom Environments

```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class CustomEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(self, render_mode=None, size=5):
        super().__init__()

        self.size = size
        self.observation_space = spaces.Dict({
            "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
            "target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
        })
        self.action_space = spaces.Discrete(4)  # 0=up, 1=right, 2=down, 3=left

        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }
        self.render_mode = render_mode

    def _get_obs(self):
        return {"agent": self._agent_location, "target": self._target_location}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._agent_location = self.np_random.integers(0, self.size, size=2)
        self._target_location = self._agent_location.copy()
        while np.array_equal(self._target_location, self._agent_location):
            self._target_location = self.np_random.integers(0, self.size, size=2)
        return self._get_obs(), {}

    def step(self, action):
        direction = self._action_to_direction[action]
        self._agent_location = np.clip(
            self._agent_location + direction, 0, self.size - 1
        )
        terminated = np.array_equal(self._agent_location, self._target_location)
        reward = 1 if terminated else -0.01
        return self._get_obs(), reward, terminated, False, {}

    def render(self):
        if self.render_mode == "human":
            grid = np.full((self.size, self.size), ".")
            grid[self._target_location[0], self._target_location[1]] = "T"
            grid[self._agent_location[0], self._agent_location[1]] = "A"
            print("\n".join(" ".join(row) for row in grid) + "\n")

    def close(self):
        pass
```

**Register and use:**
```python
gym.register(id="CustomEnv-v0", entry_point=CustomEnv, max_episode_steps=100)
env = gym.make("CustomEnv-v0")
```

### 6. Essential Wrappers

```python
from gymnasium import wrappers

env = gym.make("CartPole-v1")

# Normalize observations (running mean/std)
env = wrappers.NormalizeObservation(env)

# Normalize rewards
env = wrappers.NormalizeReward(env, gamma=0.99)

# Clip actions to valid range
env = wrappers.ClipAction(env)

# Rescale actions from [-1,1] to environment bounds
env = wrappers.RescaleAction(env, min_action=-1, max_action=1)

# Convert to single observation (flatten dict spaces)
env = wrappers.FlattenObservation(env)

# Resize image observations
env = wrappers.ResizeObservation(env, shape=(84, 84))

# Frame stacking (Atari-style)
env = wrappers.FrameStackObservation(env, stack_size=4)

# Time limit enforcement
env = wrappers.TimeLimit(env, max_episode_steps=500)

# Record episodes as videos
env = wrappers.RecordVideo(env, "videos/", episode_trigger=lambda x: x % 100 == 0)

# Transform rewards
from gymnasium.wrappers import TransformReward
env = TransformReward(env, lambda r: np.clip(r, -1, 1))
```

### 7. Vectorized Environments

```python
from gymnasium.vector import SyncVectorEnv, AsyncVectorEnv

def make_env(env_id, seed):
    def _init():
        env = gym.make(env_id)
        env.reset(seed=seed)
        return env
    return _init

# Synchronous (sequential)
envs = SyncVectorEnv([make_env("CartPole-v1", i) for i in range(4)])
obs, _ = envs.reset()
obs, rewards, terminateds, truncateds, infos = envs.step(actions)

# Asynchronous (parallel processes)
envs = AsyncVectorEnv([make_env("CartPole-v1", i) for i in range(8)])
```

### 8. Environment Versioning

Gymnasium uses semantic versioning: `CartPole-v0`, `CartPole-v1`. When the dynamics, reward function, or observation space changes, the version number increments. **Always pin environment versions in your experiments for reproducibility.**

### 9. Checking Environment Validity

```python
from gymnasium.utils.env_checker import check_env

env = gym.make("CartPole-v1")
check_env(env, warn=True)  # Verifies API compliance
```

## Key Patterns

1. **Always use `seed` in `reset()`** for reproducible experiments
2. **Distinguish `terminated` from `truncated`** in value bootstrapping
3. **Use `wrappers.RecordVideo`** for debugging and sharing results
4. **Prefer Gymnasium over legacy Gym** — Gym is unmaintained
5. **Use `AsyncVectorEnv`** for CPU-bound environments, `SyncVectorEnv` for lightweight ones
6. **`info["terminal_observation"]`** is available after auto-reset in vectorized envs

## References

- [Gymnasium Documentation](https://gymnasium.farama.org/)
- [Environment List](https://gymnasium.farama.org/environments/)
- [API Reference](https://gymnasium.farama.org/api/env/)
- [Third-Party Environments](https://gymnasium.farama.org/environments/third_party_environments/)
- [Wrappers Reference](https://gymnasium.farama.org/api/wrappers/)
- [Vector API](https://gymnasium.farama.org/api/vector/)
