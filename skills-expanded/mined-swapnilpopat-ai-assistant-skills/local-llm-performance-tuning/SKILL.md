---
name: local-llm-performance-tuning
description: Squeeze more throughput, lower latency, and longer usable context out of a local LLM via GPU offload, KV cache settings, flash attention, speculative decoding, and prompt caching. Use when a local model fits but feels slow, OOMs at long context, or has poor first-token latency.
source: self
date_added: 2026-05-01
---

# Local LLM Performance Tuning

Make a model you already have run faster and more reliably without changing the model. Most "local LLMs are too slow" complaints come from defaults that leave 2–5× performance on the table.

## When to Use

- Tokens/sec is below the rule-of-thumb floor (~10 tok/s CPU 7B-Q4, ~40 tok/s GPU 7B-Q4, ~20 tok/s GPU 14B-Q4)
- First-token latency is high even on short prompts
- Long-context requests OOM or fall back to CPU mid-generation
- Concurrent clients (IDE autocomplete + chat) cause queueing or stalls

## The Big Levers (Highest Impact First)

1. **Get fully on the GPU.**
   - llama.cpp / Ollama: set `n_gpu_layers` (or `OLLAMA_NUM_GPU` / model `num_gpu`) to `999` (all layers). If you OOM, drop the quant or model size — *partial offload is dramatically slower than full offload*.
   - Verify with `nvidia-smi` / `radeontop` / Activity Monitor that VRAM use matches expectations and CPU is mostly idle during generation.
2. **Enable Flash Attention.**
   - llama.cpp: `--flash-attn` (or `flash_attn: true` in Ollama Modelfile). Reduces KV memory and speeds long contexts on supported GPUs.
3. **Quantize the KV cache for long contexts.**
   - llama.cpp: `--cache-type-k q8_0 --cache-type-v q8_0` halves KV memory with minimal quality impact. `q4_0` halves again with measurable but often acceptable loss.
4. **Right-size the context window.**
   - Do not load `-c 131072` if your prompts are 4k. KV cache memory scales linearly with context. Set `-c` to the realistic max you actually use.
5. **Batch / parallel slots for serving.**
   - llama-server: `--parallel N --cont-batching` lets multiple clients share the GPU efficiently.
   - vLLM handles this natively and beats llama.cpp on multi-client throughput.
6. **Prompt caching.**
   - llama.cpp `--prompt-cache` and Ollama keep-alive avoid re-prefilling stable system prompts. Massive win for IDE chat sessions with a long system prompt.
7. **Speculative decoding.**
   - Pair a small "draft" model (0.5B–1.5B) with the main one: `--model main.gguf --model-draft small.gguf`. 1.5–2.5× speedups on code-like outputs when the draft agrees often.

## Lower-Impact Knobs

- `--threads` ≈ physical cores (not hyperthreads) for CPU paths.
- `--mlock` to prevent the model from being paged out (Linux/macOS).
- `--numa distribute` on multi-socket boxes.
- Disable mmap (`--no-mmap`) only if you see thrashing; usually the default is fine.
- Sampling: greedy (`temperature 0`) is fastest. `top_k` is cheaper than `top_p`. Avoid `min_p` + `top_p` + `typical_p` stacks unless you measured a quality need.

## Latency vs. Throughput

- **Interactive chat / autocomplete**: optimize first-token latency. Short context, small batch, prompt cache, draft model.
- **Bulk processing / evals**: optimize throughput. Larger batch, more parallel slots, longer context if needed.

These goals conflict; run two endpoints if you need both (e.g. Ollama on `:11434` for chat, vLLM on `:8000` for batch).

## Diagnosing Slowness

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| GPU at 30% util, CPU pegged | Partial offload | Increase `n_gpu_layers` or shrink model |
| Fast first token, slow stream | Sampler overhead, CPU bottleneck | Simplify sampling, raise threads |
| Slow first token on long prompt | No prompt cache, no flash-attn | Enable both |
| OOM mid-generation at long context | KV cache growth | Quantize KV cache, lower `-c`, or use a smaller model |
| Throughput collapses with 2 clients | No continuous batching | Enable `--parallel` + `--cont-batching` or move to vLLM |
| Quality dropped after tuning | Over-aggressive KV quant or wrong template | Revert KV to `f16`, recheck chat template |

## Measurement Discipline

- Always measure with the same prompt set before/after each change.
- Report **prompt-eval tok/s** and **generation tok/s** separately — they have different bottlenecks.
- Warm up the model first (one throwaway request) before timing.
- Track VRAM/RAM peak, not just average.

Example (llama.cpp prints these in `--verbose`):

```
prompt eval time =  812.3 ms /  640 tokens (   1.27 ms/token,  788.1 tok/s)
       eval time = 4123.7 ms /  256 tokens (  16.11 ms/token,   62.1 tok/s)
```

## Anti-Patterns

- Tuning sampler params before fixing GPU offload.
- Loading a 128k context "to be safe" then wondering why VRAM is full.
- Comparing tok/s across runners without matching quant, context, and batch size.
- Turning on every flag at once — change one variable per measurement.
- Speculative decoding with a poorly matched draft model — verify acceptance rate > 50% or it slows you down.

## References

- llama.cpp server docs: <https://github.com/ggerganov/llama.cpp/tree/master/examples/server>
- Flash Attention notes: <https://github.com/ggerganov/llama.cpp/pull/5021>
- vLLM performance guide: <https://docs.vllm.ai/en/latest/performance/optimization.html>
