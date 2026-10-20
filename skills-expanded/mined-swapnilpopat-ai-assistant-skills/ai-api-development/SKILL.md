---
name: ai-api-development
description: LLM and AI API integration patterns across providers. Use when designing provider integrations, prompt pipelines, multimodal features, or production AI backends.
source: https://github.com/openai/openai-cookbook
---

# AI API Development

Provider-aware patterns for building reliable AI features and backends.

## GitHub Signals

- `openai/openai-cookbook` consistently emphasizes rate-limit-aware retries, batching, streaming, structured outputs, and multimodal request design
- Cookbook examples also show evaluation harnesses, concurrency controls, and token budgeting needed for production traffic
- Although the examples are vendor-specific, the integration patterns generalize well to Anthropic, Cohere, Azure OpenAI, and model gateway architectures

## When to Use

- Add chat, embeddings, image, speech, or tool-calling capabilities to an application
- Design backend services that must survive provider outages, rate limits, and cost pressure
- Build prompt contracts or structured response formats that downstream systems depend on
- Compare synchronous, streaming, and batch inference paths for the same user workflow

## Coverage Areas

### Request Architecture

- Choose models intentionally for quality, latency, price, and modality support
- Design prompts and schemas so outputs are machine-consumable instead of loosely formatted text
- Decide when streaming improves UX and when batch or asynchronous processing is the better fit

### Reliability And Cost

- Implement retries with exponential backoff, circuit breaking, and request pacing under provider rate limits
- Track token budgets, usage ceilings, and fallbacks before traffic grows large enough to surprise you
- Use caching, batching, and lower-cost models when the user journey tolerates them

### Evaluation And Observability

- Log prompts, outputs, refusals, latency, and failure class without leaking sensitive customer data
- Build eval sets for critical tasks before making prompt or model changes
- Treat model output as untrusted input that still needs validation, guardrails, and monitoring
