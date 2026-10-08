---
name: local-model-fit
description: "Compute the VRAM/RAM budget and pick a model size and quantization before downloading anything. Use when choosing local models, planning GPU hardware, or hitting out-of-memory errors."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [local-inference, gpu, vram, quantization, ollama, llamacpp, build]
    related_skills: [eval-first-development, agent-loop-safety]
    program_weeks: [8, 9]
---

# Local Model Fit

## 1 · Purpose

Turn "will this model run on my machine?" from a download-and-pray experiment into
arithmetic you do before touching the network.

## 2 · When to use

- Choosing any local model + quantization for a laptop, workstation, or server.
- Planning GPU purchases or cloud GPU instances.
- Debugging `CUDA out of memory` / Metal allocation failures.

## 3 · Inputs

- Your usable GPU VRAM (or unified memory on Apple Silicon, budget ~70% of total
  RAM for the GPU).
- The model's parameter count (from its card) and the context length you need.
- The quantization you are considering (FP16, Q8, Q6_K, Q5_K_M, Q4_K_M…).

## 4 · Procedure

1. Compute the **weights budget**: `params (B) × bytes-per-param`. FP16 ≈ 2 bytes,
   Q8 ≈ 1, Q6_K ≈ 0.80, Q5_K_M ≈ 0.68, Q4_K_M ≈ 0.60. A 14B at Q4_K_M ≈ 8.4 GB.
2. Compute the **KV-cache budget**: roughly `1 to 2 GB per 8k context for a 7 to 14B
   model`, scaling with layers and heads, when precision matters, serve once and
   read the actual allocation from the engine's log.
3. Add runtime overhead: ~1 to 2 GB for the engine, compute buffers, and the OS
   sharing the GPU.
4. Total = weights + KV cache + overhead. Require total ≤ 90% of usable VRAM.
   If over, drop one lever: smaller quant, shorter context, or smaller model, in
   that preference order for quality preservation.
5. Pick the model **class** by task before picking the quant: tool-calling agents
   need tool-tuned models (e.g. Hermes-class); embeddings need embedding models;
   chat quality tracks size within a family.
6. Then pick the quant: Q4_K_M is the default sweet spot; Q5_K_M/Q6_K when quality
   measurably matters and VRAM allows; Q8 near-lossless; below Q4 only when nothing
   else fits.
7. Download, load, and read the engine's actual memory report. Compare against your
   arithmetic. Investigate any gap over 15%, it means you miscounted the cache.
8. Benchmark tokens/sec on a representative prompt. A model that fits but crawls
   below your interactivity floor (often ~10 tok/s for chat) does not "fit".

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "The page says it runs on 16 GB." | Marketing pages quote weights only, at minimum context, before the OS takes its share. Do the arithmetic. |
| "I'll use the smallest quant to be safe." | Below Q4 the quality drop is real and task-visible. Spend VRAM on quality when you have it. |
| "Context length is free to crank up." | The KV cache grows linearly with context. 128k context on a 14B can cost more VRAM than the weights. |
| "It OOM'd once; just retry." | OOM is arithmetic announcing itself. Recompute, do not retry. |

## 6 · Red flags

- The plan names a model and quant but no context length.
- Total memory "should be fine" with no written number.
- The OS and other apps share the GPU but got 0 GB in the budget.
- Quality was never measured after the quant choice (see `eval-first-development`).

## 7 · Verify

- A written budget exists: weights + KV cache + overhead, total, and usable VRAM.
- The engine's measured allocation matches the budget within 15%.
- tokens/sec on a representative prompt is recorded.
- The chosen configuration clears the task eval (quality was not traded away blind).

## 8 · ZoroLogistics example

Week 8 to 9: the triage brain on a 16 GB MacBook. Usable ≈ 11 GB. Hermes-4-14B at
Q4_K_M: weights 8.4 GB + KV cache at 8k context ~1.5 GB + overhead ~1 GB ≈ 10.9 GB,
fits at the edge of the 90% rule. The alternative, 14B at Q5_K_M (9.5 GB), does not
fit with headroom; the 8B at Q6_K does and benchmarks 2× faster. The eval decides
between them, fit is the gate, accuracy is the vote.

---
© 2026 Zorost Intelligence LLC · zorost.com
