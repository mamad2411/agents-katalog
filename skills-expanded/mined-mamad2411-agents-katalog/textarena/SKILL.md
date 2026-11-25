---
name: textarena
description: Text-based game suite for LLM training and evaluation (TextArena). 100+ single-player, two-player, and multi-player text games with an OpenAI Gym-style interface. Designed for benchmarking, self-play, multi-agent RL, and reasoning-focused LLM evaluation. Use for text-game environments, self-play RL, strategic reasoning evaluation, and agent-vs-agent tournaments.
license: MIT license
tags: [text-games, self-play-rl, llm-benchmarking, strategic-reasoning, textarena]
metadata:
    skill-author: K-Dense Inc.
-------|--------------------|
| Self-play RL for LLMs | Multi-turn competitive/cooperative games |
| Strategic reasoning evaluation | Games require planning, bluffing, memory, adaptation |
| Theory-of-mind research | Multi-agent hidden-state interactions |
| Tournament benchmarking | Standardized environment API across many games |
| Reward-model / policy evaluation | Outcome-driven game scoring |

### 5. Example: Random / Heuristic Agent

```python
import textarena as ta

class SimpleAgent:
    def __call__(self, observation: str) -> str:
        # Replace with parsing + strategy
        return "default_action"

agents = {0: SimpleAgent(), 1: SimpleAgent()}
env = ta.make(env_id="TicTacToe-v0")
env.reset(num_players=2)

done = False
while not done:
    player_id, observation = env.get_observation()
    action = agents[player_id](observation)
    done, step_info = env.step(action)

rewards, game_info = env.close()
print(rewards, game_info)
```

### 6. Tournament Loop

```python
import textarena as ta

def play_match(agent_a, agent_b, env_id="TicTacToe-v0"):
    env = ta.make(env_id=env_id)
    agents = {0: agent_a, 1: agent_b}
    env.reset(num_players=2)
    done = False
    while not done:
        pid, obs = env.get_observation()
        action = agents[pid](obs)
        done, _ = env.step(action)
    rewards, info = env.close()
    return rewards, info

# Round-robin tournament
results = []
for i, a in enumerate(agent_pool):
    for j, b in enumerate(agent_pool):
        if i >= j:
            continue
        rewards, info = play_match(a, b)
        results.append((i, j, rewards, info))
```

### 7. Self-Play RL Pattern

```python
# Pseudocode for policy optimization with self-play
for episode in range(num_episodes):
    env.reset(num_players=2)
    trajectories = {0: [], 1: []}
    done = False
    while not done:
        pid, obs = env.get_observation()
        action, logprob, value = policy.sample(obs)
        done, info = env.step(action)
        trajectories[pid].append((obs, action, logprob, value))

    rewards, game_info = env.close()
    update_policy(trajectories, rewards)
```

Useful for PPO/GRPO/RFT-style training where the environment is entirely linguistic.

### 8. Game Types

TextArena includes single-player, two-player, and multi-player games. Typical families include:
- board-game-like reasoning
- hidden-information games
- negotiation / dialogue games
- planning / puzzle-style tasks
- social and theory-of-mind games

Use the environment catalog in the repo to select games by capability target.

### 9. Benchmarking Recommendations

- Track win rate, draw rate, and average reward.
- Evaluate across multiple opponents, not one fixed baseline.
- Use same prompt wrappers and parsing rules across agents for fairness.
- Record per-turn observations/actions for failure analysis.
- Mix easy and hard games to separate syntax-following from real strategy.

### 10. Environment Design Guidance

When designing your own text RL environments:
- keep observation format stable
- keep valid action grammar explicit
- expose end-of-game rewards clearly
- include hidden information only when the benchmark needs it
- test with a dumb baseline first to validate transitions

## Key Patterns

1. **Observation/action are text only** — perfect for LLM-native RL.
2. **Self-play is the core paradigm** for many TextArena experiments.
3. **Benchmark against diverse opponents** to avoid overfitting one style.
4. **Turn logs matter** — inspect full game traces, not just win rate.
5. **Use strategic games for reasoning eval**, not just instruction following.

## References

- [TextArena Repository](https://github.com/LeonGuertler/TextArena)
- [TextArena site](https://textarena.ai)
- [Environment catalog](https://github.com/LeonGuertler/TextArena/blob/main/textarena/envs/README.md)
- [Paper](https://arxiv.org/abs/2504.11442)
