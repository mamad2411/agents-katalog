---
name: rust-ml-llm-architecture
description: "Design Rust ML/LLM boundaries across Rig/Candle, data, RAG, agents, evals, or deployment."
---

# Rust ML LLM Architecture

Separate orchestration, ML runtime, data, API, evals, and deployment concerns; treat model output and retrieved documents as untrusted inputs.

## Trigger boundary

Use this skill when designing Rust ML/LLM boundaries across Rig/Candle orchestration, model runtime, data/API, RAG, agents, evals, or deployment, especially where model output or retrieved documents cross trust boundaries.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no architecture, trust-boundary, runtime, data, or deployment impact; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Cel dokumentu; Założenia architektoniczne; Decyzja: Rig, Candle czy oba
- [Shared model configuration](../_shared/references/rust-ml-llm/model-configuration.md) - wspólne fakty dla decyzji architektonicznych
- [Shared Rig providers, models, and agents](../_shared/references/rust-ml-llm/rig-providers-models-agents.md) - wspólne fakty dla projektowania orkiestracji
- [Shared Candle runtime and tensors](../_shared/references/rust-ml-llm/candle-runtime-tensors.md) - wspólne fakty dla projektowania runtime
- [Shared ML/LLM function API](../_shared/references/rust-ml-llm/function-api.md) - wspólne fakty dla API, bezpieczeństwa i RAG
- [Shared Candle training, inference, and jobs](../_shared/references/rust-ml-llm/candle-training-inference-jobs.md) - wspólne fakty dla usług, integracji, observability, testów i deploymentu
- [07-edge-case-y.md](./references/07-edge-case-y.md) - Edge case'y
