---
name: ai-sovereignty-hardware-stack
description: Build and maintain local-first AI infrastructure using the three-pillar ownership model — open-source model replacement, owned inference hardware, and data sovereignty. Use when transitioning from cloud-dependent AI to owned infrastructure, designing edge deployment architectures, or advising clients on hardware procurement for privacy-first AI operations. NOT for cloud-native architectures where data egress is acceptable.
---

# AI Sovereignty Hardware Stack

## Overview

The AI Sovereignty Hardware Stack operationalizes A-Tech's core philosophy: stop renting intelligence, start owning it. By 2026, the convergence of powerful open-source models (Phi-4, Qwen3, Llama 3.1), affordable inference hardware (consumer GPUs, NUC clusters, edge accelerators), and mature local deployment tools (Ollama, llama.cpp, vLLM) makes full AI ownership practical for individuals, small teams, and enterprises.

This skill covers the three pillars of ownership: replacing proprietary models with open-source equivalents, deploying owned inference hardware at appropriate scale, and ensuring data never leaves environments you control.

## When to Use

- Transitioning from cloud AI APIs to local inference
- Designing on-premise or edge AI infrastructure
- Advising clients on hardware procurement for AI sovereignty
- Building offline-capable AI products for privacy-sensitive markets
- Calculating total cost of ownership for local vs. cloud AI
- NOT for: architectures where real-time cloud collaboration is mandatory, or where data residency requirements permit cloud processing

## Core Process / Workflow

### 1. The Three Pillars of AI Ownership

#### Pillar 1: Open-Source Model Replacement
Replace paid proprietary APIs with open-source alternatives you run yourself.

| Use Case | Proprietary | Open-Source Replacement | Hardware Needs |
|---|---|---|---|
| Text generation | GPT-4, Claude, Gemini | Llama 3.1 70B, Qwen3-8B, Phi-4 | 24–80GB VRAM |
| Code assistance | GitHub Copilot, Cursor | DeepSeek-Coder, CodeQwen, StarCoder2 | 8–24GB VRAM |
| Image generation | Midjourney, DALL-E | Stable Diffusion XL, Flux, Stable Diffusion 3 | 8–16GB VRAM |
| Embedding / RAG | OpenAI Ada, Cohere | BGE, Nomic Embed, E5 | 4–8GB VRAM |
| Speech-to-text | Whisper API | Whisper.cpp (local) | 4–8GB VRAM |
| Vision | GPT-4V, Gemini Vision | Llava, BakLLaVA, Qwen-VL | 8–16GB VRAM |

**A-Tech Principle**: The open-source model does not need to match proprietary quality at everything. It needs to match at *your specific use case* — and 80% match is often sufficient.

#### Pillar 2: Owned Inference Hardware
Own the physical infrastructure that runs inference.

**Tier 1: Individual Developer (~$1,000–$2,500)**
- Single GPU workstation: RTX 4090 (24GB), RTX 3090 Ti (24GB), or used server GPU
- Runs 7B–13B models fully, 70B models with quantization
- Suitable for: personal coding assistant, local chatbot, small RAG system

**Tier 2: Small Team / Studio (~$3,000–$8,000)**
- Multi-GPU or high-VRAM single GPU: RTX A6000 (48GB), dual RTX 4090
- NUC cluster for distributed inference
- Runs 70B models comfortably, multiple concurrent 13B sessions
- Suitable for: small dev team, content studio, prototype AI product

**Tier 3: Enterprise / Edge Deployment (~$10,000–$50,000)**
- Server-grade: 2–4× A100/H100 (40–80GB each), or AMD MI300X
- Edge accelerators: NVIDIA Jetson, Intel NUC with Movidius, Coral TPU
- Full model zoo, concurrent users, high-throughput RAG
- Suitable for: enterprise on-premise, data center, regulated industries

**Capital vs. Operational Math**:
- Cloud GPT-4 API: ~$0.03/1K tokens input, ~$0.06/1K output
- Local RTX 4090 running Llama 3.1 70B: ~$0.001/1K tokens (amortized over 2 years)
- Break-even: 500K–1M tokens/month for single-developer use; scales favorably with team size

#### Pillar 3: Data Sovereignty
Ensure your data never leaves environments you control.

- **Local-first default**: All inference happens on owned hardware unless user explicitly opts into cloud
- **No telemetry**: Open-source inference servers run without phone-home diagnostics
- **Air-gapped capable**: Full stack must function without internet connectivity
- **Encrypted at rest**: Model weights and user data encrypted on disk
- **Portable**: User data exportable in standard formats; no vendor lock-in

### 2. The Hardware Selection Framework

#### Step 1: Define Your Model Requirements
```
What is the largest model you need to run? → Determines VRAM requirement
What is your concurrent user load? → Determines GPU count and throughput
What is your acceptable latency? → Determines quantization level and batch size
What modalities? (text, image, vision, audio) → Determines specialization
```

#### Step 2: Match Hardware to Model
| Model Size | FP16 VRAM | Q4 VRAM | Recommended Hardware |
|---|---|---|---|
| 7B | 14GB | 4GB | RTX 3060 12GB, Apple M2 Pro |
| 13B | 26GB | 7GB | RTX 3090 24GB, RTX 4090 24GB |
| 70B | 140GB | 40GB | 2× RTX A6000, 1× A100 80GB |
| 405B | 810GB | 230GB | 8× A100 80GB, 2× MI300X 192GB |

#### Step 3: Select Deployment Stack
- **Personal / single-user**: Ollama (macOS, Linux, Windows) — one-command model pull and serve
- **Small team**: vLLM or llama.cpp with OpenAI-compatible API — multi-user, batching
- **Enterprise**: TensorRT-LLM or TGI with Kubernetes — auto-scaling, monitoring
- **Edge**: llama.cpp with quantized models on ARM or Intel NUC

### 3. The Migration Roadmap

**Phase 1: Audit (Week 1)**
- Inventory all cloud AI API calls: which models, which endpoints, token volume per month
- Classify by sensitivity: which data absolutely cannot leave premises
- Identify quick wins: high-volume, low-sensitivity use cases for first migration

**Phase 2: Proof of Concept (Weeks 2–4)**
- Deploy one local model for one use case
- Benchmark quality against cloud equivalent using your own evaluation set
- Measure latency, throughput, and user satisfaction

**Phase 3: Parallel Operation (Weeks 5–12)**
- Run local and cloud side by side
- Route traffic based on sensitivity: sensitive → local, tolerant → cloud
- Build operational confidence and identify gaps

**Phase 4: Full Transition (Weeks 13–24)**
- Migrate remaining use cases
- Decommission cloud subscriptions
- Document total cost of ownership and reinvest savings

**Phase 5: Optimization (Ongoing)**
- Fine-tune local models on proprietary data
- Quantize aggressively for latency-sensitive applications
- Scale hardware as team and model requirements grow

### 4. Security and Maintenance

- **Model provenance**: Download from verified sources (Hugging Face with GPG verification, official model cards)
- **Update cadence**: Evaluate new model releases quarterly; do not chase every release
- **Backup strategy**: Model weights backed up to encrypted offline storage
- **Physical security**: Edge deployments in locked enclosures; enterprise in access-controlled racks
- **Monitoring**: Local-only telemetry for GPU utilization, temperature, request latency — no cloud dashboards required

## References

- See [references/hardware-procurement-guide.md](references/hardware-procurement-guide.md) for vendor comparison, pricing benchmarks, and procurement templates.
- See [references/deployment-stack-configurations.md](references/deployment-stack-configurations.md) for Ollama, vLLM, TensorRT-LLM, and llama.cpp configuration examples.
- See [references/tco-calculator.md](references/tco-calculator.md) for cloud vs. local total cost of ownership spreadsheet methodology.
