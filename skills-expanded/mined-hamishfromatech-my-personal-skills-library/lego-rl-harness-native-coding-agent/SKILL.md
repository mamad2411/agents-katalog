---
name: lego-rl-harness-native-coding-agent
description: Apply Lego-RL's harness-native reinforcement learning framework for training coding agents inside their actual runtime harnesses (Claude Code, OpenHands, OpenCode) rather than generic environments. Use when fine-tuning coding models for specific agent harnesses, evaluating harness-specific performance gaps, or designing RL training loops that preserve native agent control flow.
---

# Lego-RL: Harness-Native Reinforcement Learning for Coding Agents

## Overview

Lego-RL (Du et al., arXiv:2608.17393, August 2026, Apache 2.0) is an open-source framework for training coding agents with online reinforcement learning on real software-engineering tasks while keeping each agent's native control flow. It connects Claude Code, OpenHands, and OpenCode to the verl RL training engine, running each task in a fresh Harbor sandbox where the task verifier supplies the reward.

## When to Use

- Fine-tuning a coding model for a specific agent harness (Claude Code, OpenHands, OpenCode, or custom)
- Evaluating whether a model trained in one harness transfers to another
- Designing RL training loops that preserve native agent control flow
- Measuring harness-specific performance gaps in coding agents
- Training models on real repositories with executable verifier rewards

## NOT for

- Training models for non-coding tasks (framework is coding-agent-specific)
- Offline RL from static datasets (Lego-RL requires online rollouts in live sandboxes)
- Environments without verifiable rewards (needs test suites or verifiable task completion)

## Core Finding: Harness Specificity Matters

The headline finding: RL gains are **harness-specific**. Training in the harness the agent will actually run in produces gains that do not fully transfer to other harnesses.

| Harness | Base Model | After Lego-RL | Gain |
|---------|-----------|--------------|------|
| OpenHands SDK | 64.0% | 70.4% | +6.4 |
| Claude Code | 62.4% | 68.2% | +5.8 |
| OpenCode | 57.2% | 66.6% | +9.4 |

Model: Qwen3.5-35B-A3B, 3 epochs (126 steps), 2,699-task OpenSWE-derived index, SWE-bench Verified.

### KAT-Coder Cross-Harness Evidence

KAT-Coder-V2.5-Dev (post-trained from same base):
- Claude Code (its authors' harness): +3.4 points
- OpenCode: +0.6 points
- OpenHands SDK: -0.4 points

This asymmetry is exactly why Lego-RL trains inside the harness the agent will run in.

## Architecture

```
Agent (native harness) → Harbor sandbox → Verifier reward → verl policy update
     ↑                                                        |
     └────────────────────────────────────────────────────────┘
```

### Key Components

1. **Native agents**: Claude Code, OpenHands, OpenCode run through thin adapters. Custom scaffolds speaking OpenAI or Anthropic API use the same agent-loop interface.
2. **Faithful rollouts**: In-process proxy records token ids, masks, and log-probabilities at generation time. Handles history rewrites and serves OpenAI/Anthropic interfaces.
3. **RL and scaling**: PPO, GRPO, and GSPO on FSDP, VeOmni, or Megatron. Synchronous or fully asynchronous. MoE runs use R3 routing replay. Trajectory filtering removes broken/over-long rollouts.
4. **Sandboxed rewards**: Kubernetes or Docker runs each task in isolated Harbor environment. Task verifier provides reward. Image caching and reward-hacking checks available.
5. **Monitoring**: Live dashboard with training curves, validation, per-task results, individual trajectories.

## Why Harness-Native Training Works

Standard RL post-training treats the agent as a generic model generating text. Lego-RL recognizes that:

1. **Different harnesses expose different interfaces** — tool formats, context management, error handling vary
2. **The harness is part of the policy** — control flow, retry logic, and context assembly shape outcomes
3. **Training in harness = training on the target distribution** — no sim-to-real gap

Training Qwen3.5-35B-A3B for 3 epochs (126 steps):
- Beats both next base generation (Qwen3.6-35B-A3B) and KAT-Coder-V2.5-Dev (a model post-trained from it) in all three harnesses
- Gains are harness-specific — the same model scores differently across harnesses
- OpenCode shows largest gain (+9.4) because its base score was lowest (most room to improve)

## Core Process / Workflow

### 1. Setup

```bash
git clone https://github.com/LegoX/Lego-RL.git && cd Lego-RL
bash scripts/setup_env.sh  # pinned upstreams + self-contained venv

cp scripts/train/examples/demo.env scripts/train/configs/demo.env
# Edit: checkpoint path, train/val task index, kubeconfig
```

Requires: 8× A100/H100-class GPUs, uv, policy checkpoint, two task indexes, Kubernetes cluster (or Docker for single-machine).

### 2. Validation

```bash
PREFLIGHT_ONLY=1 bash scripts/train/train.sh scripts/train/configs/demo.env
```

Validates without launching. Checks: checkpoint, task index, sandbox connectivity.

### 3. Training

```bash
bash scripts/train/train.sh scripts/train/configs/demo.env
```

Demo run: 1/16 scale (8 prompts × 4 responses = 32 trials/step). Full scale: 256 prompts × 16 responses.

### 4. Claude Code Integration

```bash
# In Claude Code session
/rl:run scripts/train/configs/demo.env
/rl:status
/rl:dashboard
```

### 5. Live Monitoring

```bash
bash webui/start_dashboard.sh
```

Per-trial visibility: training curves, validation metrics, per-task results, individual trajectories.

## Decision Framework

```
Need to fine-tune a coding agent?
├── Know target harness → Lego-RL (train in-harness)
│   ├── Claude Code → use Claude Code adapter
│   ├── OpenHands → use OpenHands SDK adapter
│   ├── OpenCode → use OpenCode adapter
│   └── Custom (OpenAI/Anthropic API) → use agent-loop interface
├── Multiple target harnesses → train separately per harness
├── No specific harness → standard RL post-training (but expect transfer gaps)
└── No verifiable rewards → not applicable
```

## Key Insight: The Harness Is Part of the Policy

Lego-RL validates a pattern visible across the DevEx skill cluster:

- **Agent harness choice affects outcomes** (see `tool-architecture-coding-agent-behavior`)
- **Different harnesses have different capabilities** (see `multi-agent-coding-coordination-network`)
- **Training on the target distribution matters** (see `agentic-coding-prior-ai-exposure-moderation`)

The implication for model selection: a model's benchmark score in one harness does not predict its score in another. Evaluate in the harness you will deploy in.

## A-Tech Alignment

- **Open-source AI**: Apache 2.0; works with open-weight models (Qwen3.5, GPT-OSS, Nemotron, GLM)
- **Data privacy**: Self-hosted training; code never leaves your infrastructure
- **Financial freedom**: Train on your own GPUs; no per-token API costs during training
- **Practical implementation**: Working code, live dashboard, Claude Code integration, documented recipes

## Limitations

- Requires 8× A100/H100-class GPUs for training
- Currently supports three harnesses (Claude Code, OpenHands, OpenCode); extending requires adapter work
- Training cost dominated by sandbox execution (real repository tasks are slow to verify)
- Gains measured on SWE-bench Verified; transfer to other benchmarks untested
- Asynchronous training introduces policy-version mismatch (mitigated by truncated importance sampling)

## Cross-References

- `tool-architecture-coding-agent-behavior` — Tool architecture affects agent behavior
- `multi-agent-coding-coordination-network` — Multi-agent coordination patterns
- `agentic-coding-prior-ai-exposure-moderation` — Prior AI exposure moderates adoption
- `agentic-coding-returns-to-expertise` — Expertise drives agent success
- `codestruct-ast-action-space` — Structure-aware agent actions
- `swe-chat-real-world-coding-agent-dataset` — Real-world coding agent data

## Source

Lego-RL: Harness-Native Reinforcement Learning for Coding Agents (Du et al., arXiv:2608.17393, August 2026). Apache 2.0. github.com/LegoX/Lego-RL.

## References

- See [references/evidence-base.md](references/evidence-base.md) for full results tables, architecture details, and training recipes.