---
name: ibm-granite-42-real-sandbox-agentic-rl
description: Apply IBM Granite 4.2's real-sandbox agentic RL training methodology for deploying open-weight reasoning LLMs with native tool-calling. Use when evaluating open-weight models for agent workloads, designing self-hostable agent deployments under Apache 2.0, or training agents with real-environment RL rather than synthetic trajectories.
---

# IBM Granite 4.2: Real-Sandbox Agentic RL Under Apache 2.0

## Overview

IBM Granite 4.2 (August 25, 2026) is a family of dense reasoning LLMs (3B, 8B, 30B) with native chain-of-thought, switchable thinking modes, and multi-stage agentic reinforcement learning trained in real sandboxes rather than synthetic simulations. All sizes ship under Apache 2.0, making this the most complete open-weight reasoning+agent release for self-hostable enterprise deployment.

## When to Use

- Evaluating open-weight models for agent workloads requiring local deployment
- Designing privacy-preserving agent systems where data cannot leave the organization
- Training coding agents using real-environment RL (not synthetic trajectories)
- Choosing between reasoning models by parameter budget and capability split
- Implementing OpenAI-compatible tool-calling agents on self-hosted infrastructure

## NOT for

- Single-turn answer quality comparisons against frontier closed models (Granite 4.2 targets agentic, not chatbot, workloads)
- Non-coding agent domains (the agentic RL is 69% software engineering; transfer to other domains is unverified)
- Deployment without GPU resources (30B needs A100/H100-class; 8B needs single modern GPU)

## Architecture

| Component | 3B | 8B | 30B |
|-----------|-----|-----|------|
| Layers | 40 | 40 | 64 |
| Embedding size | 2,560 | 4,096 | 4,096 |
| KV heads | 8 | 8 | 8 |
| Sequence length | 131,072 | 131,072 | 131,072 |
| Context (extended) | 512K | 512K | 512K |
| Agentic RL | No | Yes | Yes |
| Second SFT (coding) | No | No | Yes |

All models: GQA, RoPE (θ=10M), SwiGLU MLP, RMSNorm, bfloat16, speculative decoding.

## Core Differentiators

### 1. Switchable Three-Way Thinking Mode

Same weights, three runtime modes:
- **Full thinking**: Complete chain-of-thought output in dedicated tags
- **Low-effort thinking**: Short reasoning budget on easy questions
- **Non-thinking**: Direct answers, minimal latency

This gives a latency-vs-accuracy knob at inference time — run fast mode for simple queries, switch on reasoning for hard tasks, without swapping model weights.

### 2. Agentic RL on Real Environments

The 8B and 30B models are trained to call tools, run code, and drive terminals inside **real, not simulated** environments:

- **SWE stage**: Model edits real code repositories through OpenHands toolchain; reward = hidden test suite pass/fail
- **Terminal stage**: Model executes tasks in active Linux shell; up to 64 rounds of environment interaction
- **Search stage**: Multi-hop questions via real-time web search; reward from LLM judge

This contrasts with the industry trend of synthetic trajectory post-training ("fake execution" data from other models). Granite 4.2 chose the costlier path: real sandbox execution with outcome-based rewards.

### 3. OpenAI-Compatible Tool Calling Out of the Box

Served through vLLM or SGLang, the models emit tool calls in OpenAI function-calling format. Plug into existing agentic harnesses (OpenHands, SWE-agent, custom) without a translation layer.

## Training Pipeline

### Pre-training (all sizes)
- ~15 trillion tokens across five phases
- Phases 1-2: Foundational pre-training
- Phases 3-4: Mid-training with higher-quality data annealing
- Phase 5: Long-context training (128K → 512K)

### SFT (all sizes)
- ~7.2M samples (~100B tokens, ~65B trainable)
- 31.6% agentic, 68.4% non-agentic
- Agentic breakdown: SWE 69%, tool calling 12.1%, terminal 8.0%, math 3.5%, search 0.8%, action 0.2%
- Non-agentic: instruction 18.8%, coding 18.8%, math 14.6%, multilingual 7.0%, science 5.4%, reasoning 3.0%, safety 0.8%
- Quality control: GPT-OSS-120B and Gemma 4 as LLM judges; SHA-256 deduplication

### Second SFT (30B only)
- Agentic coding focus; upsamples SWE/coding data
- ~16% replay data from original corpus
- One additional epoch at lr=3.0e-6

### RL Pipeline (8B and 30B)

**Foundational RL (all sizes):**
1. RLVR — math (boxed-answer, Lean), competitive coding (hidden-test sandbox), science MCQA, instruction following, single-step tool calling, reasoning puzzles with abstention
2. Skill boosters — separate GRPO runs targeting code, science, or instruction following

**Agentic RL (8B and 30B only):**
3. SWE Agent — real repos via OpenHands, hidden test reward
4. Terminal — real Linux shell, 64 interaction rounds
5. Search — real web search, LLM judge reward

**Alignment (all sizes):**
6. RLHF — GenRM + safety reward, KL penalty, reasoning-length penalty

Algorithm: Asynchronous GRPO with leave-one-out baseline (no value network). 256 prompts × 16 responses = 4,096-example batches. Truncated importance sampling clamps train-vs-generation log-prob ratio.

## Benchmark Results (Vendor-Published)

| Benchmark | 30B | 8B | 3B |
|-----------|-----|-----|-----|
| SWE-Bench Verified | 57.0% | 47.7% | — |
| Terminal-Bench 2.1 | 29.2% | 20.6% | — |
| AIME25 | 89.2% | 86.7% | 78.3% |
| GPQA | 66.4% | 64.1% | — |
| RULER (128K) | 81.4% | 71.4% | 55.3% |

Treat as vendor-published until independently verified.

## Deployment Guidance

| Size | Target | Hardware | Use Case |
|------|--------|----------|----------|
| 3B | Edge, high-throughput | Laptop (Q4_K_M GGUF via Ollama/LM Studio) | Chain-of-thought reasoning without agentic tasks |
| 8B | Sweet spot | Single modern GPU | Agent workloads, tool calling, SWE tasks |
| 30B | Complex multi-step | A100/H100 or FP8/NVFP4 on vLLM | Multi-file code editing, terminal workflows, multi-hop search |

### Serving

```bash
# vLLM with OpenAI-compatible API
vllm serve ibm-granite/granite-4.2-8b --tool-call-parser hermes

# SGLang
python -m sglang.launch_server --model-path ibm-granite/granite-4.2-8b
```

### Thinking Mode Control

```python
# Non-thinking mode (fast)
response = client.chat.completions.create(
    model="granite-4.2-8b",
    messages=[...],
    extra_body={"chat_template_kwargs": {"thinking": False}}
)

# Low-effort thinking (balanced)
extra_body={"chat_template_kwargs": {"thinking": "low"}}

# Full thinking (max accuracy)
extra_body={"chat_template_kwargs": {"thinking": True}}
```

## Decision Framework

```
Need reasoning + agents + self-host + Apache 2.0?
├── Yes → Granite 4.2 is strongest open-weight option
│   ├── Single GPU / cost-sensitive → 8B (full agentic RL)
│   ├── Multi-GPU / complex tasks → 30B (second SFT + full RL)
│   └── Edge / no agents needed → 3B (reasoning only, no agentic RL)
└── No →
    ├── Need frontier single-turn quality → closed models
    ├── Need non-coding agents → verify transfer (agentic RL is SWE-heavy)
    └── Need MoE efficiency → Qwen3.8-Flash, DeepSeek-V4
```

## Key Insight: Real Environments vs Synthetic Trajectories

Granite 4.2 establishes a concrete technical reference for open-source agentic training:

| Dimension | Synthetic Trajectories | Real Sandboxes (Granite 4.2) |
|-----------|----------------------|---------------------------|
| Reward signal | Model judgment | Task outcome (tests pass/fail) |
| Environment | Simulated | Real repos, shells, web |
| Cost | Lower | Higher |
| Transfer risk | Higher (sim-to-real gap) | Lower (trained on target distribution) |
| Reproducibility | Depends on trajectory source | Documented harness (OpenHands, shell, search) |

The publication of these design details offers a reproducible path for the open-source community.

## Cross-References

- `open-weight-agentic-model-wave-august-2026` — August 2026 wave (GLM-5.3, Muse Glimmer, Qwen3.8, DeepSeek-V4, Nemotron)
- `agentic-coding-trends-2026` — Agentic coding adoption patterns
- `mcp-code-execution-agent-efficiency` — MCP tool-calling patterns
- `agentic-coding-returns-to-expertise` — Expertise drives agent success
- `codestruct-ast-action-space` — Structure-aware agent actions

## A-Tech Alignment

- **Open-source AI**: Apache 2.0 on everything — weights, instruct checkpoints, quantized variants; free for commercial use
- **Data privacy**: Self-hostable weights enable air-gapped, SCIF, VPC deployment; data never leaves organization
- **Financial freedom**: 3B runs on laptops; 8B on single GPU; eliminates per-token API costs
- **Practical implementation**: OpenAI-compatible tool calling, vLLM/SGLang serving, documented training recipe

## Limitations

- Agentic SFT data is 69% software engineering — transfer to non-coding domains unverified
- 3B skips agentic RL entirely — reasoning model, not agent-trained
- Reasoning-length penalty in final RLHF may hurt tasks needing long deliberation
- Benchmark numbers are vendor-published, not independently verified
- Training on CoreWeave GB200 NVL72 clusters — not reproducible at small scale

## Source

IBM Granite 4.2 release (August 25, 2026). IBM Research published model weights, instruct checkpoints, and quantized variants on Hugging Face and GitHub under Apache 2.0. Training details from IBM Research blog and Data Today coverage (Lars Cornelissen, August 26, 2026).

## References

- See [references/evidence-base.md](references/evidence-base.md) for full architecture details, training pipeline, benchmark tables, and deployment recipes.