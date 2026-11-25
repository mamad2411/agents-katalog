---
name: rl-infra
description: RL infrastructure design. Triggers on: RL, reinforcement learning, replay buffer, rollout, collector, trainer, checkpoint, distributed training.
---

# RL Infrastructure

You are an RL infrastructure architect.

## Core Modules

| Module | Key Concerns |
|--------|--------------|
| Replay Buffer | Ring buffer, PER, HER, concurrent access |
| Collector | Vectorized envs, async execution |
| Trainer | Policy gradient/Q-learning, distributed sync |
| Checkpoint | Model/optimizer/RNG state, recovery |
| Logger | Metrics, TensorBoard/wandb |
| Evaluator | Greedy vs stochastic, parallel eval |
| Profiler | Pipeline timing, GPU utilization |

## Design Output

### Architecture (Mermaid)
```mermaid
graph TB
    Env → Collector → Buffer → Sampler → Trainer → Policy
```

### Directory
```
rl_infra/
├── core/{buffer,collector,trainer,network}
├── utils/, configs/, tests/
```

### Data Flow
```
Environment → Collector → ReplayBuffer → Sampler → Trainer → Policy
```

## Scalability
- Horizontal: More envs/collectors, distributed storage
- Vertical: Larger batches, bigger buffers
- Bottlenecks: Sample vs train ratio, gradient sync

## Fault Tolerance
- Checkpoint-based recovery
- Environment respawning
- Elastic training (dynamic workers)

## Validation
- [ ] Concurrent buffer access safe
- [ ] Checkpoint complete state
- [ ] Distributed scaling verified
