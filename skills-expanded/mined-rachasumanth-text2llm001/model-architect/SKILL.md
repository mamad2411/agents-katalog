---
name: model-architect
description: Design transformer architectures by target scale and emit Hugging Face Transformers-compatible model configs.
---

# Model Architect (From Scratch)

Use this skill to design a model architecture for **pretraining from scratch**.
It should output practical configs that match compute, memory, and quality goals.

## Scale Templates

Provide architecture templates by parameter scale:

- **100M class**
- **300M–700M class**
- **1B–3B class**
- **7B+ class**

For each template, define reasonable defaults for:

- hidden size
- number of layers
- number of attention heads
- intermediate (FFN) size
- context length

## Component Selections

Use modern decoder-only transformer defaults unless user requests otherwise:

- **GQA** (Grouped Query Attention) for memory/throughput efficiency at scale.
- **SwiGLU** feed-forward activation.
- **RoPE** positional encoding.
- **RMSNorm** normalization.

When deviating from these defaults, explain why and expected tradeoffs.

## Config Output

Emit a Hugging Face Transformers-compatible `config.json` suitable for training scripts.
Include all required architecture fields and tokenizer special token ids.

## Parameter + Memory Calculator

Always provide estimates for:

- total parameter count (with per-block breakdown)
- optimizer state memory
- activation memory (approximate by batch/seq settings)
- checkpoint size (fp16/bf16 and optional fp32)

Report both training-time and inference-time memory expectations.

## Tokenizer Integration

Before generating `config.json`, import outputs from the **tokenizer-trainer** skill:

- Read `vocab_size` from trained tokenizer and set in config.
- Import `bos_token_id`, `eos_token_id`, `pad_token_id`, `unk_token_id` from `special_tokens_map.json`.
- Validate that `max_position_embeddings` aligns with tokenizer sequence length analysis.
- Fail explicitly if tokenizer artifacts are missing — never use placeholder token IDs.

## Decision Protocol

- Start with target quality, latency, and budget constraints.
- Produce at least two candidate designs when tradeoffs are non-trivial.
- Recommend one primary architecture with rationale.
- Highlight scaling path (for example 100M -> 1B -> 7B) for future expansion.

## Deliverables

1. `config.json` (HF-compatible)
2. `architecture_report.md` (tradeoffs + estimates)
3. `capacity_plan.md` (GPU/memory implications)
