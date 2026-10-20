---
name: local-llm-vram-cost-estimation
description: Estimate VRAM, hardware requirements, and cost for running any LLM locally — covering quantization levels, MoE activation fraction, KV cache for long contexts, and multi-node cluster sizing.
version: 1.0.0
author: Hermes Agent
license: MIT
dependencies: []
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [vram, cost-estimation, local-llm, quantization, gpu, hardware, inference, mxe, moe]
    triggers: [vram, cost estimation, can I run, hardware requirements, local model, gpu memory, inference cost, quantization memory]
    related_skills: [llama-cpp, outlines, huggingface-hub, vllm]
---

# Local LLM VRAM & Cost Estimation

Estimate VRAM, throughput, and TCO for running any LLM locally. Covers dense and MoE architectures, modern quantization formats (MXFP4, GGUF variants, AWQ, GPTQ), KV cache overhead, and multi-node scaling.

## When to Use

- User asks "can I run model X on my GPU?"
- Deciding which quant to download for available hardware
- Comparing cloud API cost vs. self-hosted TCO
- Sizing a multi-GPU or multi-node cluster
- Budgeting for inference hardware procurement

## Quick Reference Formulas

### 1. Base Model VRAM

**Dense model (full precision FP16):**
```
VRAM_GB = param_count_B * 2  (bytes per FP16 param × 1e9 → GB)
```
Example: 7B model → 7 × 2 = **14 GB** FP16

**Dense model (quantized):**
```
VRAM_GB = param_count_B × bits_per_param / 8
```
| Quant | Bits/param | 7B Model | 13B Model | 70B Model |
|-------|-----------|----------|-----------|-----------|
| FP16 | 16 | 14.0 GB | 26.0 GB | 140.0 GB |
| Q8_0 | 8 | 7.0 GB | 13.0 GB | 70.0 GB |
| Q6_K | 6.55 | 5.7 GB | 10.6 GB | 57.3 GB |
| Q5_K_M | 5.5 | 4.8 GB | 8.9 GB | 48.1 GB |
| Q4_K_M | 4.5 | 3.9 GB | 7.3 GB | 39.4 GB |
| Q3_K_M | 3.5 | 3.1 GB | 5.7 GB | 30.6 GB |
| Q2_K | 2.56 | 2.2 GB | 4.2 GB | 22.4 GB |

**MoE models (Mixture of Experts):**
```
VRAM_GB = total_params_B × bits_per_param / 8 × active_ratio
```
Where `active_ratio` = active_experts / total_experts × (1 + shared_overhead)

Common MoE activation fractions:
| Model | Total Params | Active Params | Active Ratio | Q4_K_M VRAM |
|-------|-------------|---------------|-------------|-------------|
| Mixtral 8×7B | 46.7B | 12.9B | 0.276 | ~10.5 GB |
| Qwen3.6-35B-A3B | 35B | 3B | 0.086 | ~3.9 GB |
| DeepSeek V2 | 236B | 21B | 0.089 | ~12.7 GB |
| DeepSeek-R1 | ~671B | ~37B | 0.055 | ~43.6 GB |

**MXFP4 quantization (4.25-bit, hardware-native):**
```
VRAM_GB = param_count_B × 4.25 / 8
```
Example: 70B model → 70 × 4.25 / 8 = **37.2 GB** MXFP4

### 2. KV Cache Overhead

**Per-token KV cache per layer:**
```
bytes_per_token = 2 × d_model × 2 × bytes_per_element
// key + value, each FP16 (2 bytes), scaled by 2 for split K/V
```

**Simplified:**
```
KV_Cache_GB = (context_length × d_model × 2 × 2 × num_layers) / 1e9
```

Or use the rule of thumb:

| Context | 7B (d=4096, 32 layers) | 13B (d=5120, 40 layers) | 70B (d=8192, 80 layers) |
|---------|------------------------|-------------------------|-------------------------|
| 4K | 4.3 GB | 8.2 GB | 41.9 GB |
| 8K | 8.6 GB | 16.4 GB | 83.9 GB |
| 32K | 34.4 GB | 65.5 GB | 335.5 GB |
| 128K | 137.4 GB | 262.1 GB | 1.3 TB |

**KV cache optimizations:**
- **GQA/MQA** — Multi-Query/GrOUP-Query Attention reduces KV heads by 4-8×, cutting cache proportionally
- **KV quantization** — KV cache at FP8 halves it; INT4 quarters it vs. FP16
- **Shared prefix / RadixAttention** (vLLM) — deduplicates KV across requests in high-throughput scenarios

### 3. Total VRAM Per Request

```
Total_GB ≈ model_weights_GB + KV_cache_GB + overhead_GB
```

Overhead includes:
- **CUDA kernels + activations**: 0.5–2 GB (batch_size=1), scales with batch
- **Tokenizer + misc buffers**: 0.1–0.5 GB
- **Speculative draft model** (if used): +30-100% of target model size

### 4. Throughput Estimation

```
tokens_per_second ≈ (GPU_FLOPS × utilization) / (2 × total_params × context_length)
```

| GPU | FP16 TFLOPS | 7B Q4 (4K ctx, bs=1) | 70B Q4 (4K ctx, bs=1) |
|-----|-------------|----------------------|----------------------|
| RTX 3090 | 35.6 | ~120 t/s | ~12 t/s |
| RTX 4090 | 82.6 | ~200 t/s | ~20 t/s |
| A100 (80GB) | 312 | ~450 t/s | ~45 t/s |
| H100 | 989 | ~800 t/s | ~80 t/s |
| Mac M2 Ultra (128GB) | ~18 | ~60 t/s | ~6 t/s |

### 5. Cost Estimation

**Hardware purchase:**
```
TCO_per_year = GPU_price / depreciation_years + power_cost + cooling_cost
```

| GPU | Price | VRAM | TDP | 3yr TCO (est) | Tokens/$ |
|-----|-------|------|-----|---------------|----------|
| RTX 3090 (used) | ~$700 | 24 GB | 350W | ~$1,150 | ~310M |
| RTX 4090 | ~$1,800 | 24 GB | 450W | ~$2,600 | ~550M |
| 2× RTX 3090 | ~$1,400 | 48 GB | 700W | ~$2,300 | ~620M |
| A100 80GB (cloud) | ~$3/hr | 80 GB | — | ~$26,280/yr | ~360M/hr |
| H100 (cloud) | ~$4/hr | 80 GB | — | ~$35,040/yr | ~640M/hr |

**Cloud rental comparison:**
```
cost_per_M_tokens = (hourly_rate × hours_for_1M_tokens) × 1e6
```

| Provider | GPU | Rate/hr | 7B Q4 per 1M tok | 70B Q4 per 1M tok |
|----------|-----|---------|------------------|-------------------|
| RunPod | RTX 4090 | $0.49 | ~$0.0006 | ~$0.006 |
| Vast.ai | RTX 3090 | $0.20 | ~$0.0003 | ~$0.003 |
| Lambda | A100 | $1.10 | ~$0.0007 | ~$0.007 |
| Together API | (API) | $0.20/M | — | $0.20/M (API) |
| OpenAI GPT-4o | (API) | $2.50/M | — | $2.50/M (API) |

**Rule of thumb:** Self-hosting is ~100-1000× cheaper per token for high-volume inference vs. API pricing.

## Step-by-Step Procedure

### Step 1: Identify Model Parameters

Get from model card or Hugging Face:
- `total_parameters` (e.g., 7B, 70B)
- Architecture: dense or MoE
- If MoE: `num_experts`, `num_active_experts`, optional shared expert
- Hidden dimension (`d_model`), number of layers, KV head count

### Step 2: Calculate Base Weight Size

Use the table above or formula for the target quant. Check the model's GGUF or AWQ offerings on Hugging Face first — actual quantized file sizes are always more accurate than theoretical formulas.

Formula shortcut (Q4_K_M): `weights_GB ≈ params_B × 0.56`

### Step 3: Add KV Cache

```
KV_GB = seq_len × d_model × num_layers × (kv_heads / query_heads) × 2 × 2 / 1e9
```

For GQA models (most modern archs), `kv_heads / query_heads` is typically 1/4 to 1/8.

**Quick KV cache rule of thumb:**
- 4K context on a 7B → ~3-4 GB
- 4K context on a 70B → ~30-40 GB  
- 32K context on a 7B → ~25-30 GB
- 128K context on a 7B → ~100-130 GB

### Step 4: Account for Overhead

Add 15-20% headroom over the calculated total for CUDA overhead, prompt processing spikes, and `torch.multiprocessing` allocator fragmentation.

### Step 5: Select Hardware

Match total VRAM to GPU memory:

| Available VRAM | Max Recommendable Model |
|----------------|------------------------|
| 6 GB | 1-3B Q4_K_M (short context) |
| 8 GB | 7B Q4_K_M (4K ctx) |
| 12 GB | 7B Q4_K_M (8K ctx) or 13B Q3_K_M |
| 16 GB | 13B Q4_K_M (4K ctx) |
| 24 GB | 13B Q5_K_M or 30B Q4_K_M or MoE model |
| 48 GB | 70B Q4_K_M (4K ctx) or 30B Q8_0 |
| 80 GB | 70B Q5_K_M (16K ctx) or DeepSeek V2 Q4 |
| 2×24 GB | 70B Q4_K_M (16K ctx, tensor parallel) |
| 8×80 GB | 671B Q4_K_M (DeepSeek-R1) |

### Step 6: Optional — Multi-Node Scaling

For models that exceed single-node VRAM:
```
nodes_needed = ceil(Total_VRAM_GB / VRAM_per_GPU / GPUs_per_node)
```

**Pipeline parallelism:** each node holds 1/N layers. Scales linearly but adds ~0.5-2 ms per network hop per token.

**Tensor parallelism:** each node holds 1/N of each layer. Requires NVLink or ≥25 Gbps inter-node. Highly sensitive to network latency — single-node is strongly preferred.

**Recommended:** Stay single-node unless your model exceeds ~300B parameters. For 671B models (DeepSeek-R1), use 2-4 nodes with tensor parallelism and InfiniBand.

## Verification

1. Check actual file size from Hugging Face tree API — theoretical and actual sizes match within 5%
2. Run `nvidia-smi` (or task manager on Windows) before and after loading the model — confirm VRAM usage matches estimate
3. Run a short inference benchmark — measured t/s should be within 30% of estimated throughput
4. Compare cloud costs: API pricing vs. self-hosted TCO over 1 month at expected usage volume

## References

- [llama.cpp — Advanced Quantization Guide](references/quantization.md)
- Hugging Face GGUF documentation: https://huggingface.co/docs/hub/gguf
- Model tree API: `https://huggingface.co/api/models/<repo>/tree/main?recursive=true`
- Local App view: `https://huggingface.co/<repo>?local-app=llama.cpp`

## Pitfalls

- **Don't trust FP16-only specs** for consumer GPUs — Q4_K_M is ~3.5× more memory efficient and barely degrades quality on modern models
- **Do not forget KV cache** — it often exceeds model weights at 32K+ context (see 70B 128K needing 1.3 TB)
- **MoE total_params ≠ active_params** — 46.7B MoE needs 10.5 GB Q4 (not 26 GB), but all 46.7B parameters must still be *loaded* into memory even if only 12.9B are computed per token
- **Batch-size scaling** — throughput scales sub-linearly with batch: a batch of 16 may need 6× the VRAM but only delivers 4× throughput. Find the VRAM-throughput sweet spot for your use case
- **Prompt processing is compute-bound, not memory-bound** — long prompts (document QA) are bottlenecked by attention compute, not VRAM. Short prompts (chat) are memory-bound by model weight loading
- **Windows GPU memory fragmentation** — CUDA on Windows can fragment ~1-2 GB more than Linux due to WDDM driver model. Account for this in overhead
- **Mac unified memory** — Apple Silicon uses shared RAM not dedicated VRAM. An M2 Ultra with 128 GB unified can run 70B Q4_K_M at 4K ctx (~48 GB total), but performance drops when other apps compete for bandwidth