---
name: cleanrl
description: Single-file deep reinforcement learning implementations (CleanRL). High-quality standalone implementations of PPO, DQN, C51, SAC, DDPG, TD3 with research-friendly features. Each algorithm is a self-contained file with ~300-500 lines. Includes Atari, MuJoCo, Procgen, PettingZoo multi-agent, and JAX variants. Use for RL algorithm reference, rapid prototyping, and understanding implementation details.
license: MIT license
tags: [ppo, dqn, sac, rl-reference-implementation, cleanrl]
metadata:
    skill-author: K-Dense Inc.
--------|------|----------------|
| **PPO** | `ppo.py` | `python cleanrl/ppo.py --env-id CartPole-v1` |
| **PPO Atari** | `ppo_atari.py` | `python cleanrl/ppo_atari.py --env-id BreakoutNoFrameskip-v4` |
| **PPO Continuous** | `ppo_continuous_action.py` | `python cleanrl/ppo_continuous_action.py --env-id HalfCheetah-v4` |
| **PPO Multi-Agent** | `ppo_pettingzoo_ma_atari.py` | `python cleanrl/ppo_pettingzoo_ma_atari.py --env-id pong_v3` |
| **DQN** | `dqn.py` | `python cleanrl/dqn.py --env-id CartPole-v1` |
| **DQN Atari** | `dqn_atari.py` | `python cleanrl/dqn_atari.py --env-id BreakoutNoFrameskip-v4` |
| **C51 Atari** | `c51_atari.py` | `python cleanrl/c51_atari.py --env-id BreakoutNoFrameskip-v4` |
| **SAC Continuous** | `sac_continuous_action.py` | `python cleanrl/sac_continuous_action.py --env-id HalfCheetah-v4` |
| **SAC Atari** | `sac_atari.py` | `python cleanrl/sac_atari.py --env-id BreakoutNoFrameskip-v4` |
| **DDPG** | `ddpg_continuous_action.py` | `python cleanrl/ddpg_continuous_action.py --env-id HalfCheetah-v4` |
| **TD3** | `td3_continuous_action.py` | `python cleanrl/td3_continuous_action.py --env-id HalfCheetah-v4` |

### 3. PPO Training Workflow

```bash
# Minimal PPO on CartPole
python cleanrl/ppo.py \
    --seed 1 \
    --env-id CartPole-v1 \
    --total-timesteps 50000 \
    --track \
    --wandb-project-name my-project

# PPO on Atari (standard config)
python cleanrl/ppo_atari.py \
    --seed 1 \
    --env-id BreakoutNoFrameskip-v4 \
    --total-timesteps 10000000 \
    --track \
    --capture-video

# PPO on MuJoCo continuous control
python cleanrl/ppo_continuous_action.py \
    --seed 1 \
    --env-id HalfCheetah-v4 \
    --total-timesteps 1000000
```

**Key PPO Hyperparameters:**
| Parameter | CartPole/Classic | Atari | MuJoCo |
|-----------|-----------------|-------|--------|
| `--total-timesteps` | 50K | 10M | 1M |
| `--learning-rate` | 2.5e-4 | 2.5e-4 | 3e-4 |
| `--num-envs` | 4 | 8 | 1 |
| `--num-steps` | 128 | 128 | 2048 |
| `--anneal-lr` | True | True | False |
| `--gae-lambda` | 0.95 | 0.95 | 0.95 |
| `--update-epochs` | 4 | 4 | 10 |
| `--norm-adv` | True | True | True |
| `--clip-coef` | 0.2 | 0.1 | 0.2 |
| `--ent-coef` | 0.01 | 0.01 | 0.0 |

### 4. DQN Training

```bash
# DQN on Atari
python cleanrl/dqn_atari.py \
    --seed 1 \
    --env-id BreakoutNoFrameskip-v4 \
    --total-timesteps 10000000 \
    --buffer-size 100000 \
    --learning-starts 80000 \
    --target-network-frequency 1000 \
    --batch-size 32 \
    --track
```

### 5. Multi-Agent RL with PettingZoo

```bash
# PPO on multi-agent Atari Pong
python cleanrl/ppo_pettingzoo_ma_atari.py \
    --seed 1 \
    --env-id pong_v3 \
    --total-timesteps 10000000 \
    --track

# Available MA environments:
# pong_v3, surround_v2, tennis_v3, space_invaders_v2,
# warlords_v3, combat_plane_v2, combat_tank_v2
```

### 6. Logging and Monitoring

```bash
# TensorBoard (runs in cleanrl/runs/)
tensorboard --logdir runs

# Weights & Biases (requires wandb login)
python cleanrl/ppo.py --track --wandb-project-name my-project --wandb-entity my-entity

# Video capture (every 100th evaluation)
python cleanrl/ppo_atari.py --capture-video --env-id BreakoutNoFrameskip-v4
```

### 7. JAX-Accelerated Variants

5-10x faster training via JAX compilation + EnvPool:
```bash
# Install JAX support
pip install -r requirements/requirements-jax.txt

# JAX PPO on Atari (ultra-fast)
python cleanrl/ppo_atari_envpool_xla_jax.py \
    --env-id BreakoutNoFrameskip-v4 \
    --total-timesteps 10000000

# JAX DQN on Atari
python cleanrl/dqn_atari_jax.py \
    --env-id BreakoutNoFrameskip-v4 \
    --total-timesteps 10000000
```

### 8. Docker and Cloud (AWS)

```bash
# Build Docker image
docker build -t cleanrl .

# Submit to AWS Batch
python cleanrl/ppo_atari.py \
    --env-id BreakoutNoFrameskip-v4 \
    --total-timesteps 10000000 \
    --track \
    --upload-model
```

### 9. Algorithm Structure (Reading an Implementation)

Each file follows a consistent structure:
```python
# 1. Imports
# 2. parse_args() — CLI arguments
# 3. make_env() — Environment creation
# 4. Agent class (if needed) — Neural network, usually simple MLP/CNN
# 5. main():
#    a. Setup: seeding, device, envs
#    b. Initialize agent, optimizer
#    c. Initialize storage (rollout buffer, replay buffer)
#    d. Training loop:
#       - Collect experience
#       - Compute returns/advantages
#       - Update policy/value/Q-network
#       - Log metrics
#    e. Save model, upload
```

Each file is ~300-500 lines and is meant to be read top-to-bottom.

### 10. Debugging and Development

```bash
# Minimal test run (fewer steps, more frequent logging)
python cleanrl/ppo.py \
    --env-id CartPole-v1 \
    --total-timesteps 5000 \
    --num-envs 1 \
    --num-steps 32 \
    --track

# Disable wandb (pure TensorBoard)
python cleanrl/ppo.py --env-id CartPole-v1 --total-timesteps 50000

# Check available env IDs
python -c "import gymnasium as gym; print([e for e in gym.envs.registry if 'CartPole' in e])"
```

## Key Patterns

1. **CleanRL is NOT a library** — don't `import cleanrl`, run the scripts directly
2. **Each file is self-contained** — copy `ppo.py` and modify it for your research
3. **Use `--track` for W&B logging**, omit for plain TensorBoard
4. **`--capture-video` saves agent gameplay** — great for qualitative evaluation
5. **JAX variants are fastest** but require understanding of `jax.lax.scan`
6. **All implementations are benchmarked** — see https://benchmark.cleanrl.dev

## References

- [CleanRL Documentation](https://docs.cleanrl.dev/)
- [Algorithm Benchmarks](https://benchmark.cleanrl.dev/)
- [JMLR Paper](https://www.jmlr.org/papers/volume23/21-1342/21-1342.pdf)
- [CORL (offline RL fork)](https://github.com/corl-team/CORL)
- [LeanRL (optimized PyTorch fork)](https://github.com/pytorch-labs/LeanRL)
