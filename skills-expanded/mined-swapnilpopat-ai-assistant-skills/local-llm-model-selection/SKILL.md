---
name: local-llm-model-selection
description: Choose the right open-weights model and quantization for your hardware and task (coding, chat, RAG, tool use). Use when picking among Qwen, Llama, Gemma, DeepSeek, Mistral, Phi, etc., and matching them to a quant level that fits VRAM/RAM.
source: self
date_added: 2026-05-01
---

# Local LLM Model Selection

Match model family, parameter count, and quantization to your hardware and your actual task. Wrong choices waste hours; right choices make a local model feel close to a hosted one for many workflows.

## When to Use

- You have a fixed VRAM/RAM budget and want the strongest model that still fits
- You are choosing between many open-weights families and need a decision rubric
- You need a different model for coding vs. chat vs. embeddings vs. tool calling
- A model "works" but is slow, dumb, or hallucinates — and you suspect the wrong size or quant

## Decision Rubric

1. **Pick the task profile first.**
   - Code completion / edits → coder-tuned model (e.g. Qwen2.5-Coder, DeepSeek-Coder, Codestral-class)
   - General chat / reasoning → instruct-tuned generalist (Qwen2.5-Instruct, Llama 3.x Instruct, Gemma 2/3 IT)
   - Tool / function calling → model with documented tool-use training (Qwen2.5, Llama 3.x, Hermes fine-tunes)
   - RAG over long docs → model with honest long context (≥ 32k effective)
   - Embeddings → dedicated embedding model (`bge-*`, `nomic-embed-text`, `e5-*`), not a chat model
2. **Size to your hardware.** See the table below.
3. **Pick a quant.** `Q4_K_M` is the default sweet spot. Go up to `Q5_K_M` or `Q6_K` if you have headroom and care about quality; only drop to `Q3_K_M`/`IQ3` when nothing else fits.
4. **Verify on your own prompts.** Benchmarks lie about your workload. Keep a personal eval set of 10–20 representative prompts.

## Hardware → Model Size Cheat Sheet

Assumes a single dense model loaded with ~8k context. Add room for KV cache at longer contexts.

| Available VRAM (or RAM, CPU-only) | Comfortable model size | Typical pick |
| --- | --- | --- |
| 6 GB | 3B–7B at Q4 | Phi-3.5-mini, Qwen2.5-3B, Llama 3.2 3B |
| 8 GB | 7B–8B at Q4 | Qwen2.5-Coder-7B, Llama 3.1 8B |
| 12 GB | 7B at Q6 or 13B–14B at Q4 | Qwen2.5-14B, DeepSeek-Coder-V2-Lite |
| 16 GB | 14B at Q5 / small MoE | Qwen2.5-Coder-14B, Mistral Small |
| 24 GB | 24B–32B at Q4–Q5 | Qwen2.5-32B, Codestral-22B |
| 48 GB | 70B at Q4 (tight) | Llama 3.x 70B Instruct |
| 2× 24 GB / 1× 80 GB | 70B at Q5–Q6 | Llama 3.x 70B, Qwen2.5-72B |

CPU-only is viable for ≤ 7B at Q4 if you have AVX2 + ≥ 16 GB RAM and tolerate ~5–15 tok/s.

## MoE Note

Mixture-of-Experts models (e.g. Mixtral, DeepSeek-V2/V3 family, Qwen MoE variants) need RAM/VRAM for **all** experts but only compute through active ones. They are fast for their parameter count but memory-hungry — verify the full-weight footprint, not the active-parameter count, fits in memory.

## Quantization Quick Guide

- `Q8_0` — near-lossless, large. Use only if you have generous memory.
- `Q6_K` — very small quality drop, good default if it fits.
- `Q5_K_M` — strong quality/size balance.
- `Q4_K_M` — recommended default; small, capable, broadly tested.
- `IQ4_XS` / `IQ3_M` — "imatrix" quants; better quality at small sizes than legacy Q3, slightly slower on some backends.
- `Q3_K_M` and below — noticeable quality loss; use only when forced.

Always prefer `K`-quants over legacy `Q4_0`/`Q4_1` unless your runner does not support them.

## Coding-Specific Picks (as of 2026)

- 8 GB VRAM → Qwen2.5-Coder-7B-Instruct Q4_K_M
- 12–16 GB → Qwen2.5-Coder-14B-Instruct Q4_K_M / Q5_K_M
- 24 GB+ → Qwen2.5-Coder-32B-Instruct or DeepSeek-Coder-V2 family
- Repo-wide edit / agent loops → prefer instruct models with tool-calling training; pair with `local-llm-coding-assistant` patterns

## Anti-Patterns

- Loading a 70B at `Q2` "because it fits" — quality is usually worse than a 14B at `Q5`.
- Using a chat model for embeddings — slow and weak vs. a 100M-param embedder.
- Picking by leaderboard score without trying it on your own prompts.
- Ignoring the tokenizer / chat template; a mismatched template silently destroys quality.
- Comparing a hosted frontier model to a 7B local and concluding "local LLMs don't work". Compare to the right tier.

## Verification

- Run the same 10 prompts through 2–3 candidate models; record latency, token count, and a 1–5 quality score.
- Keep the winner pinned by exact tag (`qwen2.5-coder:14b-instruct-q4_K_M`).
- Re-evaluate every 1–2 months; the open-weights frontier moves fast.
