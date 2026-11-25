---
name: inference-deploy
description: Deploy trained models for inference with vLLM, TGI, Ollama, or llama.cpp including quantization, API setup, and latency benchmarking.
---

# Inference & Deploy

Use this skill to serve trained or fine-tuned models for production or local inference.
Covers quantization, serving frameworks, API endpoints, and performance validation.

## Serving Frameworks

Support deployment via:

- **vLLM** — high-throughput OpenAI-compatible server, PagedAttention.
- **TGI** (Text Generation Inference) — Hugging Face's production server.
- **Ollama** — local model serving with Modelfile-based packaging.
- **llama.cpp** — CPU/GPU inference for GGUF models.

Default to vLLM for GPU deployments, Ollama for local/desktop use.

## Quantization

Generate quantized variants when needed:

- **GGUF formats**: Q4_K_M, Q5_K_M, Q6_K, Q8_0
- **GPTQ**: 4-bit with calibration dataset
- **AWQ**: 4-bit activation-aware quantization

Report expected quality impact and memory savings for each variant.
Use `llama.cpp/convert` or `AutoGPTQ`/`AutoAWQ` tooling.

## API Endpoint Setup

Configure OpenAI-compatible API endpoints:

- `/v1/chat/completions`
- `/v1/completions`
- `/v1/models`

Include:

- model loading and warm-up validation
- configurable max tokens, temperature, top-p defaults
- request logging and error handling
- optional API key authentication

## Docker Deployment

Generate deployment configs:

- `Dockerfile` with model baked in or mounted as volume
- `docker-compose.yml` for multi-service setups
- GPU passthrough configuration (NVIDIA runtime)
- Health check endpoints

## Performance Validation

Run basic load tests before declaring deployment ready:

- time-to-first-token (TTFT)
- tokens per second (TPS)
- concurrent request throughput
- memory utilization under load

Report results in a table comparing configurations.

## Ollama Modelfile

When deploying via Ollama, generate a `Modelfile` with:

- base model reference (GGUF path or HF repo)
- system prompt template
- parameter defaults (temperature, top_p, etc.)
- license and model card metadata

## Deliverables

1. `deploy_config.yaml` (framework, model path, settings)
2. `Dockerfile` / `docker-compose.yml` (if containerized)
3. `Modelfile` (if Ollama)
4. `latency_report.md` (TTFT, TPS, memory benchmarks)
5. `deploy_checklist.md` (readiness validation)

## Python Dependencies

- `vllm`
- `text-generation-inference` (TGI client)
- `huggingface_hub`
- `auto-gptq` or `autoawq` (for quantization)
