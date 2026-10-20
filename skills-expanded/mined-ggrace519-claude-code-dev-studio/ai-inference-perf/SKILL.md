---
name: ai-inference-perf
description: Inference performance and cost specialist. Auto-invoked when inference latency, throughput, token cost, batching, quantization, KV caching, or GPU scheduling is being tuned.
---

# AI Inference Perf

Serving-layer changes compound across every request — this is where the cost and
latency wins live. Every perf change is also a potential quality regression in
disguise, so measurement and quality gates travel together.

## When to reach for this

- TTFT, TPOT, or token cost needs to come down for an existing workload
- Choosing or tuning a serving stack (vLLM, TGI, TensorRT-LLM, llama.cpp, hosted APIs)
- Adding quantization, batching, KV/prefix caching, or speculative decoding
- Setting up perf regression guards alongside the quality gates

## Principles

1. **Measure before changing.** Baseline TTFT, TPOT (time per output token),
   throughput (tok/s), and cost per 1K tokens — at realistic concurrency, p50 *and*
   p95, never averages alone.
2. **Quality-gate every perf change.** Run the golden set before and after;
   quantization that drops task quality is a regression no matter what it saves.
3. **Cache before compute.** Prompt/prefix caching, then semantic caching, then
   response caching — in that order. On hosted APIs, structure prompts
   static-prefix-first so cached tokens hit the provider's discounted rate.
4. **Batch when latency allows.** Continuous batching (the vLLM/TGI default)
   multiplies throughput at a modest TPOT cost — tune max batch size against the
   p95 latency budget, not peak throughput.
5. **Long prompts dominate.** Chat-history and RAG workloads spend most compute on
   prefill; prefix caching and prompt trimming win disproportionately there.
6. **Track cost per successful interaction.** Per-token cost is a proxy; a cheaper
   model with a higher retry/failure rate costs more per useful outcome.

## Optimization order

| Lever | Typical win | Quality risk | Reach for it when |
|---|---|---|---|
| Prompt/prefix caching | large on shared-prefix workloads | none | always first |
| Trim prompt / cap output length | linear in tokens cut | low — still eval it | bloated system prompts, stale few-shots |
| Streaming + TTFT focus | perceived latency | none | any interactive surface |
| Continuous batching | 2–10× throughput | none (TPOT rises slightly) | self-hosted, concurrency > 1 |
| Quantization (INT8, AWQ/GPTQ 4-bit) | 2–4× memory, faster decode | real — task eval required | GPU memory-bound |
| Speculative decoding | 1.5–3× decode speedup | none (output distribution preserved) | latency-bound, draft model available |
| Smaller / distilled model | step change in cost | high — full eval | quality bar has headroom |

## Pitfalls

- Benchmarking at concurrency 1, deploying at 100 — batching changes every number
- Quantizing on "perplexity looks fine" — perplexity is not a task eval
- Streaming disabled, so users feel full generation time instead of TTFT
- Cache hit rate unmonitored — a prompt edit that shifts the static prefix
  silently doubles cost with no functional symptom
- Comparing serving stacks with different sampling params or max-token limits
- Optimizing per-token cost while retries and truncated outputs erase the savings

---
*Related: `ai-eval` (quality gates on perf changes), `ai-rag` (retrieval inside the
latency budget), `ai-finetune` (serving adapters) · domain agent: `ai-architect`
(model selection, serving topology, cost/latency budgets) · output/ADR format:
`playbook-conventions`*
