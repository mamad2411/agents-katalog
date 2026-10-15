---
name: mla-analysis
description: >
  MLA (Multi-Latent Attention) cost models, regime analysis, and kernel selection guide.
  Use when: (1) reasoning about which kernel approach to use for a given regime,
  (2) understanding cost model tradeoffs between FlashMLA, FlashAttention, and MLAvar6+,
  (3) analyzing roofline behavior across decode/speculative/prefill regimes,
  (4) setting optimization targets, (5) understanding MLA math and absorption trick.
---

# MLA Cost Analysis & Regime Guide

## Regime Selection

| Regime | s Range | Best Kernel | Why |
|--------|---------|------------|-----|
| Decode | s=1 | FlashMLA | 16x latency reduction vs FlashAttention (compressed KV) |
| Speculative | s=2-32 | MLAvar6+ or FlashMLA | MLAvar6+ should be able to beat FlashMLA and FlashAttention |
| Prefill | s>128 | FlashAttention | Avoids 4x FLOP penalty of latent-space compute |

**Crossover point**: FlashAttention becomes faster than FlashMLA at approximately s=16-32 for DeepSeek-V3 parameters.

## Cost Models (DeepSeek-V3-like: h=128, d=128, k=512, p=64)

### FlashAttention
- FLOPs: `2bhst(2d + p)` = `2bhst * 320`
- Bytes: `w * bh(s+t)(2d + p)` = `w * bh(s+t) * 320`
- At s=1: AI ≈ 1 FLOP/byte (deeply memory-bound)
- At s=1024: AI ≈ 819 FLOP/byte (deeply compute-bound)

### FlashMLA (latent-space attention via absorption)
- FLOPs: `2bhst(2k + p)` = `2bhst * 1088`
- Bytes: `w * (bhs(2k+p) + bt(k+p))`
- At s=1: AI ≈ 228 FLOP/byte (compute-bound even at decode)
- **Problem**: FLOPs grow linearly with s at k=512 instead of d=128 — 3.4x more FLOPs per token

### MLAvar6+ (split latent + decompressed)
- FLOPs: `2bhstp + 4bhsnd + 4bhsok`
- Bytes: `w * (bhsp + bhsd + bhsk + bok + btp + bhnd + bhnd + bhsd + bhsk)`
- **Key**: choosing n tunes operational intensity near roofline ridge point

## Absorption Trick (FlashMLA)

```
Score:  Q @ K^T = Q @ (Z @ Wk)^T = (Q @ Wk^T) @ Z^T = Qz @ Z^T
Value:  softmax(A) @ V = softmax(A) @ (Z @ Wv) = (softmax(A) @ Z) @ Wv
```

Operate entirely in latent space (k-dim), with output decompression `O_latent @ W_kvb2^T` done by a separate kernel.

## MLAvar6+ Design

Split KV cache into:
- **o old tokens**: latent Z (b, o, k) — compute-heavy, low bandwidth
- **n new tokens**: decompressed K,V (b, n, h, d) — bandwidth-heavy, low compute
- t = o + n

Interpolates: n=0 → FlashMLA-like, o=0 → FlashAttention-like.

## Historical Baselines (RTX 5090, b=32, t=4096, bfloat16)

> **Note**: These results are from RTX 5090 development. Reprofile on the current device before using as optimization targets. Ridge point, bandwidth, and compute ceilings differ across devices — see `src/mla_var3/conf/devices.json`.

| Config | FlashMLA | FlashAttention | MLAvar6+ V3 (best) |
|--------|----------|----------------|---------------------|
| s=1 | **419 μs** | 6,781 μs | 829 μs (V2) |
| s=16 | 5,161 μs | 6,727 μs | **4,444 μs** |

MLAvar6+ V3 is the current best for speculative decoding (s=16), beating FlashMLA by 14%.

## Tensor Shapes (DeepSeek-V3 defaults)

| Symbol | Description | Default |
|--------|-------------|---------|
| b | Batch size | 64 |
| h | Number of heads | 128 |
| s | Query sequence length | varies |
| t | KV context length | 4096 |
| d | Head dimension | 128 |
| p | Positional embedding dim | 64 |
| k | Latent (compressed) dim | 512 |

**Tensor layouts**:
- Q, Qc: `[B, H, S, D]` or `[B, H, S, K]`
- K, V: `[B, T, H, D]` (decompressed)
- Z: `[B, T, K]` (latent KV cache)
- QPE, KPE: `[B, H, S, P]` or `[B, T, P]`

## Detailed Analysis

Full cost model derivations and roofline analysis: `docs/cost-analysis.md`
