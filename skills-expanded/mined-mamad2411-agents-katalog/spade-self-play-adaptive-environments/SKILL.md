---
name: spade-self-play-adaptive-environments
description: Apply SPADE's self-play framework where a single language model learns both to design executable training environments and to solve them, creating an adaptive curriculum that moves with the learner. Use when designing RL post-training pipelines that avoid fixed-environment saturation, when environment generation is the bottleneck, or when exploring open-ended self-improvement for coding agents.
---

# SPADE: Self-Play in Adaptive Synthetic Executable Environments

## Overview

SPADE (Liu et al., arXiv:2608.19197, August 2026, MIT license) is a self-play framework where a single language model learns in two roles: an **environment designer** that writes complete multi-turn environments as executable Python with `reset()` and `step()` interfaces, and a **reasoning agent** that learns by acting in them. The designer is trained with **hint-based regret** — the gap between the agent's return with and without a privileged hint — which steers generation toward environments at the agent's capability frontier while keeping them feasible.

## When to Use

- Designing RL post-training pipelines that avoid fixed-environment saturation
- When environment generation (not model scaling) is the training bottleneck
- Exploring open-ended self-improvement for coding/reasoning agents
- Generating adaptive curricula that move with the learner
- Training models on cognitive games or multi-turn tool use with self-generated tasks

## NOT for

- Supervised fine-tuning (SPADE is an RL framework)
- Domains without verifiable rewards (environments need executable verification)
- Models below 4B parameters (self-play requires minimum capability in both roles)
- Production deployment without safety review (open-ended generation can produce unexpected environments)

## The Problem It Solves

Current RL post-training for reasoning (RLVR, agentic RL) draws reward from **fixed, hand-built environment pools** that stop adapting once the learner masters them. Two failure modes:

1. **Saturation**: Model masters all environments; no learning signal remains
2. **Stagnation**: Environment pool fixed at creation; cannot discover new capability frontiers

SPADE addresses this by making **environment design itself a learnable component**. The model generates its own training tasks, creating an adaptive curriculum that keeps moving with the learner.

## Architecture

```
                    ┌─────────────────────┐
                    │   Shared Policy     │
                    │  (one model, two    │
                    │   roles)            │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
    ┌───────────▼──────────┐     ┌────────────▼───────────┐
    │  Environment Designer │     │   Reasoning Agent      │
    │  - Samples grounding  │     │   - Plays environment  │
    │    context from corpus│     │   - With hint          │
    │  - Writes executable  │     │   - Without hint       │
    │    Python environment │     │   - Task return →      │
    │  - Generates hint     │     │     trains agent role  │
    │  - Structural +      │     │   - Hint-based regret  │
    │    runtime validation │     │     → trains designer  │
    └──────────────────────┘     └────────────────────────┘
```

### Key Mechanism: Hint-Based Regret

The designer is trained to generate environments at the agent's capability frontier:

- **Regret** = Return_with_hint - Return_without_hint
- High regret = environment is at the frontier (hint helps a lot)
- Zero regret = too easy (both succeed) or too hard (both fail)
- Designer trained to maximize regret → generates solvable-but-challenging environments

### Per-Role Advantage Normalization

A single policy plays both roles. Per-role advantage normalization keeps the joint update stable:
- Agent role: advantage from task return
- Designer role: advantage from hint-based regret
- Normalization prevents one role's gradient from dominating

## Training Pipeline

### Supported Models

| Family | Models |
|--------|--------|
| **Qwen3** | 4B, 8B, 30B-A3B (trained in paper) |
| Qwen3.5 | 4B, 9B, 35B-A3B |
| GPT-OSS | 20B, 120B |
| Nemotron | Nano-30B-A3B, Super-120B-A12B |
| GLM | 5.2, 5.3 |

Model-agnostic: any chat-capable policy your backend can fine-tune.

### Two Settings

1. **Cognitive games**: Multi-turn reasoning games with verifiable win/loss
2. **Multi-turn tool use**: Tool-calling tasks with executable verification

### Training Commands

```bash
# Clone with pinned submodules
git clone --recurse-submodules git@github.com:spade-rl/spade.git && cd spade
python -m venv .venv && source venv/bin/activate
python -m pip install -e .

# SPADE games self-play (30B)
bash cmd/games/train_spade_30b.sh

# SPADE tool use (30B)
bash cmd/tool_use/train_spade_30b.sh

# Fixed-environment baselines (for comparison)
bash cmd/games/train_fixed_gpt55_30b.sh  # GPT-5.5 corpus
bash cmd/games/train_fixed_rlve_30b.sh   # RLVE corpus
```

### Distributed Training

- **Slime/SGLang integration**: SGLang inference + Megatron-LM policy updates + Ray orchestration
- **Tinker integration**: Thinking Machines' distributed training framework
- 400 rollouts on single 8-GPU node for 30B-A3B

## Key Results

SPADE outperforms fixed-environment baselines on held-out benchmarks **past the saturation point**:

### Cognitive Games

| Model | SPADE | Fixed (GPT-5.5 corpus) | Fixed (RLVE) |
|-------|-------|----------------------|--------------|
| Qwen3-4B | ✓ | Baseline | Baseline |
| Qwen3-8B | ✓ | Baseline | Baseline |
| Qwen3-30B-A3B | ✓ | Baseline | Baseline |

All SPADE models improve on held-out math, science, code, and procedural-reasoning benchmarks past the point where fixed-environment baselines saturate.

### Adaptive Curriculum Properties

- Designer produces **progressively harder, more interactive environments** over training
- Environment difficulty tracks the agent's improving capability
- Curriculum never saturates because the designer evolves with the agent

## Comparison with Related Approaches

| Approach | Environment Source | Adaptivity | Saturation Risk |
|----------|-------------------|------------|----------------|
| RLVR (fixed tasks) | Hand-built pool | None | High |
| Agentic RL (Granite 4.2) | Real sandboxes | None (fixed task set) | Medium |
| Ornith self-proposed tasks | Model generates tasks | Medium | Medium |
| **SPADE** | Model generates + validates | **High (hint-based regret)** | **Low** |

### vs Ornith Self-Proposed Task RL

Both generate tasks from the model itself. Key difference:
- **Ornith**: Task reward = validity × novelty × difficulty (targets 0.2 success rate)
- **SPADE**: Designer reward = hint-based regret (gap between with/without hint)

SPADE's regret signal is more direct: it measures whether the environment is at the frontier, not just whether it's novel or difficult. Ornith optimizes for solvability; SPADE optimizes for frontier-calibration.

Critical caveat from Ornith skill: self-proposed tasks optimize for solvability, not real-world impact. SPADE shares this risk — the adaptive curriculum may improve on benchmarks but not on real deployment tasks.

## Decision Framework

```
Environment design bottleneck for RL post-training?
├── Yes → SPADE (generate adaptive curriculum)
│   ├── Cognitive games → cmd/games/
│   ├── Multi-turn tool use → cmd/tool_use/
│   └── Custom domain → implement reset()/step() interface
├── No, have good fixed task pool →
│   ├── Pool saturating → SPADE (curriculum adaptation)
│   └── Pool not saturating → standard RLVR
└── Need real-world task performance →
    ├── SPADE for exploration + real-task fine-tuning
    └── Granite 4.2 style real-sandbox RL for deployment
```

## A-Tech Alignment

- **Open-source AI**: MIT license; model-agnostic; works with open-weight Qwen, GPT-OSS, Nemotron, GLM
- **Data privacy**: Self-hosted training; no external API calls during environment generation
- **Financial freedom**: Generate training environments without human task creation; reduces RL post-training cost
- **Practical implementation**: Working code, Slime/SGLang integration, Tinker support, evaluation suite

## Limitations

- Self-proposed tasks optimize for solvability, not real-world impact (shared with Ornith)
- Environments are synthetic Python — may not capture real-world messiness
- Requires minimum model capability (4B+) for meaningful self-play
- Designer quality depends on grounding corpus quality
- Open-ended generation can produce unexpected environments — safety review needed
- Training cost: 400 rollouts per step on 8-GPU node for 30B

## Cross-References

- `ornith-self-proposed-task-rl` — Alternative self-proposed task approach (validity × novelty × difficulty)
- `ibm-granite-42-real-sandbox-agentic-rl` — Real-sandbox agentic RL (fixed task set, real environments)
- `lego-rl-harness-native-coding-agent` — Harness-native RL for coding agents
- `ouroboros-self-developing-coding-agent` — Self-developing agent with reviewed core evolution
- `open-weight-agentic-model-wave-august-2026` — August 2026 open-weight model landscape

## Source

SPADE: Self-Play in Adaptive Synthetic Executable Environments (Liu et al., arXiv:2608.19197, August 2026). MIT license. github.com/spade-rl/spade. Models and data on HuggingFace (spade-rl).

## References

- See [references/evidence-base.md](references/evidence-base.md) for full architecture, training commands, and comparison tables.