---
name: local-llm
description: Local LLM architecture, quantized inference (GGUF Q4_K_M/Q8_0), Ollama, llama.cpp, Apple Silicon MLX, vLLM, SGLang, WebLLM/Transformers.js, KV-cache tuning, GBNF structured grammars, in-process local RAG, and 3-tier hybrid routing.
---

# Local LLM & Edge Inference (`/local-llm`)

> **Philosophy**: *Compute exact VRAM + KV-cache budgets before loading weights, enforce GBNF/schema grammars at logit sampling, keep RAG in-process, and never silently leak local prompts to cloud APIs.*

---

## 1. Progressive Disclosure References

| Resource | Purpose |
| :--- | :--- |
| [references/quantized-inference-and-gguf.md](references/quantized-inference-and-gguf.md) | `Q4_K_M`/`Q5_K_M`/`Q8_0` sizing math, Apple `MLX`, Ollama SSE cancellation & health probes. |
| [references/serving-engines-and-kv-cache.md](references/serving-engines-and-kv-cache.md) | `vLLM` / `SGLang` PagedAttention, `Transformers.js` WebGPU, `q8_0` KV-cache, prefix caching, speculative decoding. |
| [references/gbnf-grammars-and-local-rag.md](references/gbnf-grammars-and-local-rag.md) | GBNF logit-level JSON schemas, `sqlite-vec` & `DuckDB vss` in-process hybrid RAG. |
| [scripts/verify_local_llm_hygiene.py](scripts/verify_local_llm_hygiene.py) | Audits degraded `Q2/Q3` quantizations, missing timeouts, `-ngl 0`, unconstrained JSON prompts, and unbounded `num_ctx`. |

---

## 2. Heterogeneous Inference Runtime Matrix

| Runtime | Formats | Best Target | Key Capabilities |
| :--- | :--- | :--- | :--- |
| **`llama.cpp` (`llama-server`)** | GGUF (`Q4_K_M`+) | Linux / Docker / CUDA | Continuous batching (`-cb`), `-ngl 999`, GBNF grammars, `-fa`. |
| **`Ollama`** | GGUF | Workstations / Local Dev | Declarative `Modelfile`, OpenAI `/v1`, `format` JSON schema. |
| **Apple Silicon `MLX`** | MLX 4-bit / 8-bit | macOS M1–M4 UMA | Zero-PCIe-copy Metal execution (`80–130+ tok/s`). |
| **`vLLM` / `SGLang`** | FP8 / AWQ / GPTQ | Multi-user GPU servers | PagedAttention, RadixAttention prefix reuse, high concurrency. |
| **`WebLLM` / `Transformers.js`** | Wasm + WebGPU | Client Browsers | 100% private in-browser execution inside Web Workers. |

---

## 3. Core Quantization, RAG & Hybrid Routing Invariants

1. **VRAM Budget Formula**: $\text{VRAM}_{\text{req}} = (\text{Params} \times \text{Bpw} / 8) + \text{KV Cache} + \text{Scratch (0.4–1.0 GB)}$. Default to `Q4_K_M` (chat/routing), `Q5_K_M` (code/logic), or `Q8_0` (embeddings); reject `Q2/Q3` collapse. Pin `num_ctx` (`8192` default) and enable `-fa` + `q8_0` KV cache for long contexts.
2. **Deterministic GBNF / Schema Grammars**: Constrain local `3B–8B` JSON output at token logit sampling (`grammar` in `llama.cpp`, `format` in Ollama) so markdown fences and malformed JSON cannot be sampled.
3. **In-Process Local RAG**: Use `sqlite-vec` or `DuckDB vss` (`doc_hash` + `embedding_model` version tracking, `top_k <= 6`) instead of heavyweight external vector DB containers.
4. **3-Tier Hybrid Cascade**: Route `Tier 1 (3B edge <150ms)` -> `Tier 2 (32B–70B local)` -> `Tier 3 (Gemini Frontier)` ONLY with `3s/15s` timeouts and explicit `AI_PRIVACY_MODE=hybrid_consent` (`/ai-integration`).

---

## 4. Automated Local LLM Hygiene Audit

```bash
python3 skills/local-llm/scripts/verify_local_llm_hygiene.py --path .
```
