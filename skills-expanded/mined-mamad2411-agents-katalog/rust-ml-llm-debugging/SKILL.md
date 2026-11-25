---
name: rust-ml-llm-debugging
description: "Diagnose Rust ML/LLM failures across providers, prompts, tools, retrieval, runtime, or validation."
---

# Rust ML LLM Debugging

Debug ML/LLM behavior by separating provider, prompt, tool, retrieval, model runtime, validation, budget, observability, and deployment layers.

## Trigger boundary

Use this skill when a Rust ML/LLM symptom may cross provider/model, prompt, tool, retrieval, Candle/GPU runtime, output validation, budget, observability, or deployment layers.

Do not load it for a small local edit with a deterministic cause and no model, prompt, retrieval, runtime, safety, budget, or deployment behavior change; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [Shared Rig providers, models, and agents](../_shared/references/rust-ml-llm/rig-providers-models-agents.md) - wspólne fakty; rozpocznij od lokalnego [debugging wrapper](./references/01-overview.md)
- [Shared Candle runtime and tensors](../_shared/references/rust-ml-llm/candle-runtime-tensors.md) - wspólne fakty; w debugowaniu izoluj device, dtype, tokenizację, artefakt i inferencję
- [Shared ML/LLM function API](../_shared/references/rust-ml-llm/function-api.md) - wspólne fakty; w debugowaniu rozdziel kontrakt, provider, safety, retrieval i output
- [04-candle-trening-inference-service-i-joby.md](./references/04-candle-trening-inference-service-i-joby.md) - Candle: trening, inference service i joby; Integracja z frontendem; Observability, koszty i audyt; Testy i ewaluacje
- [05-edge-case-y.md](./references/05-edge-case-y.md) - Edge case'y; Minimalny zestaw CI
