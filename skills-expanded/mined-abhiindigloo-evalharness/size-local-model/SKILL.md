---
name: size-local-model
description: Estimate the GPU or unified memory needed to run an open-weight model locally, covering weights at a given precision or quantization plus KV cache for a chosen context length and concurrency, and compare it with available memory. Use whenever the user asks whether a model fits their GPU, Mac, or server, how much VRAM or RAM a model needs, what quantization to use, how context length or batch size affects memory, or how to size hardware for Ollama, llama.cpp, vLLM, or LM Studio, even if they don't say "memory". Gives estimates with stated assumptions, never a guarantee of fit.
metadata:
  author: Indigloo
  homepage: https://github.com/Abhiindigloo/EvalHarness
---

# Estimate local model memory

## Gather inputs from official sources

Read the model card or the model's `config.json` from its official repository. Do not guess architecture values.

| Input | Where it comes from |
|---|---|
| Total stored parameters (billions) | Model card. For mixture-of-experts models use **total** parameters, not active ones: all experts are loaded. |
| Effective bits per weight | 16 for BF16/FP16, 8 for 8-bit, about 4–5 for common 4-bit formats. Most accurate: `file size in bytes × 8 ÷ parameter count` from the actual download. |
| Layers | `num_hidden_layers` |
| KV heads | `num_key_value_heads`; if absent, the model uses standard multi-head attention, so use `num_attention_heads`. |
| Head dimension | `head_dim` if present, otherwise `hidden_size ÷ num_attention_heads`. |
| Context | Tokens the user plans to use per sequence, not the advertised maximum. |
| Concurrency | Sequences served at the same time (1 for a single user). |
| KV precision | 16 by default; 8 if the runtime is set to quantize the KV cache. |

## Run

```
python3 scripts/estimate_memory.py --params-b 8.03 --bits 16 \
    --layers 32 --kv-heads 8 --head-dim 128 --context 8192 \
    --concurrency 1 --overhead-pct 10 --available-gib 24
```

Add `--json` for machine-readable output. Without the KV inputs, only weights are estimated and the output says so.

The `modelfinder_estimate_memory` MCP tool runs the same calculation with the same inputs.

Formulas (binary GiB):

- weights = parameters × bits ÷ 8
- KV cache = 2 × layers × KV heads × head dimension × context × concurrency × KV bits ÷ 8

## Report

Give weights, KV cache, overhead, total, and headroom, then the assumptions. Always state:

- The KV formula assumes standard full attention (MHA or GQA). It does not apply to multi-head latent attention, sliding-window, hybrid, or linear attention; for those, use the runtime's documentation or measure.
- The overhead percentage is an allowance chosen by the user, not a measurement. Runtimes add buffers, activations, and fragmentation.
- Fitting in memory says nothing about speed or quality. Quantization can reduce quality; recommend testing the chosen quantization on the user's own examples with eval-models (local servers work through the `openai_compatible` provider).
- On shared or unified memory (for example Apple silicon), the operating system and other apps also need memory.

If the total exceeds available memory, suggest the levers in order of typical impact: shorter context, lower concurrency, KV-cache quantization, lower weight precision, a smaller model, or splitting across devices if the runtime supports it. Do not guarantee that any configuration will run.
