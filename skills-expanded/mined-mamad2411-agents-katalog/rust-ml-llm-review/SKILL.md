---
name: rust-ml-llm-review
description: "Review Rust ML/LLM changes to Rig/Candle, prompts, tools, RAG trust, output validation, or budgets."
---

# Rust ML LLM Review

Review LLM systems for layer boundaries, prompt/tool safety, provider abstraction, RAG trust, output validation, resource budgets, observability, evals, and deployment constraints.

## Trigger boundary

Use this skill when a Rust ML/LLM diff changes Rig/Candle layers, prompts or tools, provider abstraction, RAG trust, output validation, streaming, resource budgets, evals, observability, or deployment.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no ML/LLM runtime, trust-boundary, safety, evaluation, or deployment impact; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Założenia architektoniczne; Decyzja: Rig, Candle czy oba; Warstwy systemu
- [Shared model configuration](../_shared/references/rust-ml-llm/model-configuration.md) - wspólne fakty; oceń diff według review flow
- [Shared Rig providers, models, and agents](../_shared/references/rust-ml-llm/rig-providers-models-agents.md) - wspólne fakty; użyj ich jako review rubryku orkiestracji
- [Shared Candle runtime and tensors](../_shared/references/rust-ml-llm/candle-runtime-tensors.md) - wspólne fakty; użyj ich jako review rubryku runtime
- [Shared ML/LLM function API](../_shared/references/rust-ml-llm/function-api.md) - wspólne fakty; użyj ich jako review rubryku API, safety i RAG
- [Shared Candle training, inference, and jobs](../_shared/references/rust-ml-llm/candle-training-inference-jobs.md) - wspólne fakty; użyj ich jako review rubryku usług, testów i deploymentu
- [07-edge-case-y.md](./references/07-edge-case-y.md) - Edge case'y; Checklist do code review; Minimalny zestaw CI; Przykładowe reguły merge requestu
