---
name: ai-integration
description: Universal cross-project integration layer for Computer Vision, VLM, Local LLM, and Cloud Gemini via a provider-agnostic ModelGateway, CV-before-VLM cost cascade, SSE AbortController streaming, and privacy-consent fallback gates.
---

# Universal AI, CV, VLM & Local LLM Integration (`/ai-integration`)

> **Philosophy**: *Write domain logic once against a typed `ModelGateway` contract, filter with cheap CV before burning VLM tokens, cancel stale streams deterministically, and never leak local-only prompts to cloud APIs.*

---

## 1. Progressive Disclosure References

| Resource | Purpose |
| :--- | :--- |
| [references/unified-provider-gateway.md](references/unified-provider-gateway.md) | Provider-agnostic Python/TS `ModelGateway`, `.env.example` config matrix, `/health/models` probes, privacy consent gate. |
| [references/cv-vlm-llm-cascade-and-streaming.md](references/cv-vlm-llm-cascade-and-streaming.md) | `CV -> ROI Crop -> Local VLM/LLM -> Cloud` cost cascade, SSE cancellation, circuit breakers. |
| [scripts/verify_ai_integration.py](scripts/verify_ai_integration.py) | Audits hardcoded model URLs, unguarded cloud fallbacks, missing `AbortController` stream cleanup, and leaked keys. |

---

## 2. Cross-Project Provider Matrix

| Env Profile (`AI_PROVIDER`) | Transport Protocol | Typical Use Case | Swap Effort |
| :--- | :--- | :--- | :--- |
| `ollama` / `llama_cpp` / `mlx` | OpenAI-compat `/v1` or local REST | Private workstation / macOS / on-prem | `0` code edits (`env` only) |
| `vllm` / `sglang` | OpenAI-compat `/v1` | Multi-user GPU microservice | `0` code edits (`env` only) |
| `webllm` / `onnx_webgpu` | In-browser Worker RPC | Zero-server-cost client execution | Shared TypeScript interface |
| `gemini` | `google-genai` SDK | Frontier multimodal / fallback | Consented tier-3 escalation |

---

## 3. Core Integration Invariants

1. **Zero Hardcoded Endpoints or Models**: Inject `AI_BASE_URL`, `AI_TEXT_MODEL`, `AI_VLM_MODEL`, and `CV_MODEL_PATH` via validated environment config—never hardcode `localhost:11434` inside business services.
2. **CV-Before-VLM Token Funnel**: Run lightweight CV detection / motion delta (`~5 ms`, `0` LLM tokens) and crop the ROI before calling a VLM (`70–95%` token savings).
3. **Explicit Privacy Gate (`AI_PRIVACY_MODE`)**: Default to `local_only`; cloud fallback (`gemini`) may execute ONLY when `AI_PRIVACY_MODE=hybrid_consent` is explicitly configured.
4. **Cancelable Streaming & Health Probes**: Every streaming UI/client MUST pass an `AbortSignal` (`reader.cancel()` on unmount); backends expose `/health/models` with `1.5s` non-blocking startup probes.

---

## 4. Automated Integration Hygiene Audit

```bash
python3 skills/ai-integration/scripts/verify_ai_integration.py --path . --strict
```
