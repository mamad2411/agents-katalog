---
name: slm-enterprise-deployment
description: Deploy Small Language Models (SLMs) as the default compute tier for enterprise AI applications. Covers model selection, cost-efficiency analysis, local-first architecture, tiered routing, and domain-specific fine-tuning. Use when designing AI infrastructure for cost-sensitive deployments, building edge/on-device capabilities, or advising clients on model tier strategy. NOT for use cases requiring frontier-reasoning depth (complex multi-step theorem proving, frontier research synthesis) where LLMs remain necessary.
---

# SLM Enterprise Deployment

## Overview

Small Language Models (7B–14B parameters) now rival 100B+ frontier models on coding, reasoning, and domain tasks while costing 10–30× less in latency, energy, and inference spend. Microsoft Phi-4 (14B) achieves 88.0% MMLU — surpassing GPT-3.5 (175B) at 92% less energy. This skill operationalizes SLM deployment for A-Tech's local-first, privacy-preserving, cost-efficient philosophy.

## When to Use

- Designing AI product architecture with cost constraints
- Building edge or on-device AI capabilities
- Creating tiered model routing (local SLM default, cloud LLM on opt-in)
- Advising enterprise clients on infrastructure spend reduction
- Fine-tuning models for narrow domain tasks
- Reducing API dependency and carbon footprint

NOT for:
- Frontier-reasoning tasks requiring multi-step mathematical proofs
- Real-time multilingual translation at scale
- Generating novel scientific hypotheses across domains

## Core Process / Workflow

### Step 1: Model Selection Matrix

| Model | Size | MMLU | Coding | Latency (A100) | License | Best For |
|-------|------|------|--------|----------------|---------|----------|
| Phi-4 | 14B | 88.0% | Strong | ~45ms/token | MIT | General enterprise, Microsoft ecosystem |
| Qwen3-8B | 8B | ~82% | Strong | ~35ms/token | Apache 2.0 | Open-source preference, multilingual |
| Mistral Small 3 | 24B | ~85% | Very Strong | ~60ms/token | Apache 2.0 | High-quality code generation |
| Gemma 3 | 4B–27B | 75–86% | Moderate | ~20–55ms/token | Apache 2.0 | Edge deployment, Google ecosystem |
| Llama 3.1 | 8B | ~79% | Moderate | ~40ms/token | Llama 3.1 | Meta ecosystem, permissive license |

**Selection rule:** Start with the smallest model that achieves 95% accuracy on your validation set. Scale up only when the smaller model fails on real user data.

### Step 2: Cost-Efficiency Analysis

**NVIDIA benchmark (June 2025):** Serving a 7B SLM is 10–30× cheaper than a 70–175B LLM across:
- Latency (tokens/second)
- Energy consumption (kWh per 1K requests)
- Inference cost ($ per 1M tokens)
- Hardware requirements (GPU memory)

**A-Tech pricing example:**
```
Scenario: 10K daily coding assistant users, 500 tokens/request

LLM tier (GPT-4o-class):
  API cost: ~$0.005/request × 10K × 30 = $1,500/month
  Latency p99: ~800ms
  Data egress: 500 tokens × 10K × 30 = 150M tokens/month to cloud

SLM tier (Phi-4 local):
  Infrastructure: 2× A100 @ $3/hr = ~$4,320/month
  Latency p99: ~150ms
  Data egress: 0 tokens (local processing)
  Break-even: ~2.9× LLM API cost at this scale
  Privacy: Complete (no data leaves device/network)
```

At enterprise scale (>50K users), local SLM deployment becomes cheaper than API-dependent LLM usage. Below 1K users, API calls remain cost-efficient.

### Step 3: Tiered Routing Architecture

```
┌─────────────────────────────────────────────┐
│          Request Classification Layer         │
│  (intent, complexity, sensitivity, urgency)   │
└──────────────┬──────────────────┬─────────────┘
               │                  │
     ┌─────────▼────────┐  ┌─────▼──────────┐
     │   Local SLM      │  │   Cloud LLM    │
     │  (default path)  │  │  (opt-in path) │
     │                  │  │                  │
     │  • Code complete │  │  • Complex arch │
     │  • Simple refactor│  │  • Novel patterns│
     │  • Doc generation│  │  • Cross-domain │
     │  • Unit tests    │  │  • Research synth│
     │  • Privacy-critical│  │  • Non-sensitive│
     └─────────┬────────┘  └─────┬──────────┘
               │                  │
     ┌─────────▼──────────────────▼──────────┐
     │        Unified Response Formatter        │
     │    (consistent UX regardless of tier)    │
     └──────────────────────────────────────────┘
```

**Routing rules:**
1. Default to SLM for all requests
2. LLM path triggers only when:
   - User explicitly requests "deep reasoning" or "research mode"
   - SLM confidence score < 0.7 on two consecutive turns
   - Request matches a known LLM-strength pattern (theorem proving, legal precedent synthesis)
3. Privacy-critical data always uses SLM or stays local
4. User can override default in settings (autonomy-supportive design)

### Step 4: Domain-Specific Fine-Tuning

SLMs excel when fine-tuned for narrow domains. The smaller parameter count trains faster and requires less data.

**Fine-tuning protocol:**
1. **Data collection:** 1K–10K high-quality examples from target domain
2. **Base model:** Start with 7B–8B general model
3. **Method:** LoRA or QLoRA (4-bit quantization) for memory efficiency
4. **Duration:** 3–5 epochs, early stopping on validation loss
5. **Evaluation:** Holdout test set + human evaluation on 50 examples
6. **Deployment:** ONNX Runtime or vLLM for serving

**A-Tech domains:**
- A-Coder: Fine-tuned on internal codebase patterns, API conventions
- Be Practical: Fine-tuned on curriculum content, pedagogical dialogue
- Builder's Club: Fine-tuned on open-source contribution patterns, PR review style

### Step 5: Local-First Deployment Patterns

**On-device (consumer):**
- Model: Gemma 3 4B or Qwen3-1.8B
- Runtime: ONNX Runtime Mobile, MLC LLM
- Memory: 2–4GB available RAM
- Use case: Offline code completion, privacy-first editing

**Edge server (SMB):**
- Model: Qwen3-8B or Phi-4 14B
- Runtime: vLLM, TGI (Text Generation Inference)
- Hardware: Single A10 or RTX 4090
- Use case: Team-level assistant with zero cloud dependency

**Data center (enterprise):**
- Model: Mistral Small 3 24B or clustered SLMs
- Runtime: vLLM with tensor parallelism
- Hardware: 2–4× A100
- Use case: Organization-wide replacement for API-dependent LLM usage

### Step 6: Measurement Framework

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cost per 1M tokens | <$0.50 (SLM) vs $5–30 (LLM API) | Infrastructure spend / token volume |
| Latency p99 | <200ms for SLM, <1s for LLM | Synthetic request benchmarking |
| Task accuracy | ≥95% of LLM accuracy on domain tasks | Human-evaluated holdout set |
| Energy per request | <10% of LLM equivalent | GPU power monitoring |
| User override rate | <15% (indicates routing quality) | Analytics on explicit tier switches |
| Privacy score | 100% for SLM path (zero egress) | Network egress monitoring |

## A-Tech Product Applications

### A-Coder
- Tiered model router: SLM default for autocomplete, LLM opt-in for architecture review
- Local-first mode: Gemma 3 4B on laptop for offline coding
- Enterprise tier: Phi-4 on internal GPU cluster for team-wide deployment

### Be Practical
- "SLM-First Strategy" chapter in curriculum
- Cost modeling spreadsheet for solo founders
- Domain fine-tuning guide for niche expertise monetization

### Builder's Club
- Open-source fine-tuning recipes for popular domains
- Community benchmark: SLM vs. LLM on real coding tasks
- GPU sharing pool for members without local hardware

## References

- See [references/slm-market-data.md](references/slm-market-data.md) for market size, growth projections, and vendor comparisons.
- See [references/slm-fine-tuning-playbook.md](references/slm-fine-tuning-playbook.md) for step-by-step fine-tuning recipes, hardware requirements, and evaluation templates.
- See [references/tiered-routing-implementation.md](references/tiered-routing-implementation.md) for code architecture, request classification models, and deployment templates.
