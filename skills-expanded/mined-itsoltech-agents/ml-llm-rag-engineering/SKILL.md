---
name: ml-llm-rag-engineering
description: "Engineer LLM/RAG changes to prompts, retrieval, structured output, tools, guardrails, or evals."
---

# ML LLM RAG Engineering

Build LLM and RAG systems around explicit trust boundaries: prompts, retrieved context, generated outputs, tool calls, and model artifacts are untrusted until validated.

## Trigger boundary

Use this skill when engineering an LLM/RAG flow with prompts, retrieval, embeddings/reranking, structured output, tool calls, guardrails, model artifacts, or private-domain evals crossing trust boundaries.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no model, prompt, retrieval, output-validation, tool, safety, or evaluation behavior impact; follow the repository's established convention directly.

## Process

1. Decide whether an LLM is fit for the task. Prefer rules, parsers, search, or classical classifiers when deterministic, cheaper, auditable code solves the problem.
2. Inspect pinned providers/models, tokenizer, prompt versions, retrieval stack, vector index, eval datasets, schema validators, tool permissions, latency/cost budgets, and privacy constraints before changing behavior.
3. For current provider, SDK, model, tokenizer, embedding, reranker, vector database, or fine-tuning choices, use `itsol-current-tech-context`; avoid static version claims.
4. Version prompts, schemas, retrieval config, model IDs/revisions, inference parameters, tool policies, and evals together.
5. Validate all generated output before use. Structured output still needs schema validation, bounds checks, escaping, authorization, and idempotency where applicable.
6. Treat retrieved documents as untrusted input. Separate retrieval relevance from answer correctness, groundedness, and citation correctness.
7. Add focused verification: malformed outputs, prompt injection in user input and retrieved documents, missing/false citations, tool-call argument validation, long context, retries, partial streams, cost limits, safety cases, and private domain evals.

## Coordination

Use with `ml-data-evaluation` for eval datasets, labels, leakage, metrics, and error analysis; `ml-training-experiments` for fine-tuning runs and training mechanics; `ml-serving-mlops-review` for serving contracts, monitoring, rollback, lineage, and production review; focused `security-*` skills for prompt injection, tenant boundaries, sensitive data, tool authorization, and output handling. For Rust/Rig/Candle/provider/runtime code, route first to the existing `rust-ml-llm-*` skills and use this skill for cross-cutting LLM/RAG design and evaluation.

## Reference Routing

- LLM fit/anti-fit, prompt versioning, structured outputs, inference parameters, and untrusted output validation: read [01-llm-fit-prompting-output.md](./references/01-llm-fit-prompting-output.md).
- RAG fit, ingestion, parsing, chunking, embeddings, retrieval, reranking, context trust, groundedness, citations, and retrieval evals: read [02-rag-retrieval-context.md](./references/02-rag-retrieval-context.md).
- Fine-tuning, PEFT/LoRA, SFT, preference optimization, pretraining decisions, tokenizer/context length, quantization, and distillation: read [03-finetuning-peft-distillation.md](./references/03-finetuning-peft-distillation.md).
- LLM evals, benchmark traps, safety guardrails, tool-calling, agent boundaries, privacy, security, and abuse tests: read [04-llm-evals-guardrails-agents.md](./references/04-llm-evals-guardrails-agents.md).

## Version Policy

- Existing repo: implement against pinned model/provider SDKs, prompt versions, tokenizer, embeddings, vector index, reranker, schema validators, tool policies, and eval harnesses.
- New model/provider/fine-tuning decisions: use `itsol-current-tech-context` and current official docs or vendor references before recommending exact versions, model IDs, SDK APIs, or serving modes.
- Pin model revisions or deployment IDs where reproducibility matters. Do not rely on public benchmark claims without private task evals.
